"""SQL→机器学习的最小教学桥接：固定两特征、固定 Ridge alpha=10。

只读取现有真实小样本，不联网、不读取密钥、不做交易回测。
2025年结果已在本课程展示，不能再称为完全未见样本。
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from lab import (daily_rank_ic, forward_returns, load_panel, reversal_factor,
                 sample_dates, summarize_ic)

HERE = Path(__file__).resolve().parent
FEATURES = ["reversal_5d", "lowvol_20d"]
ALPHA = 10.0
HORIZON = 5
SPLITS = {
    "训练": ("2023-01-01", "2023-12-31"),
    "验证": ("2024-01-01", "2024-12-31"),
    "研究留出（已展示）": ("2025-01-01", "2025-12-31"),
}
SQL = """
WITH windows AS (
  SELECT date, asset, adj_close,
         LAG(adj_close, 5) OVER (
           PARTITION BY asset ORDER BY date
         ) AS close_lag5,
         COUNT(adj_close) OVER (
           PARTITION BY asset ORDER BY date
           ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
         ) AS n_valid
  FROM bars_calendar_aligned
)
SELECT date, asset,
       CASE WHEN n_valid = 6 AND close_lag5 > 0
            THEN -(1.0 * adj_close / close_lag5 - 1.0)
            ELSE NULL END AS reversal_5d
FROM windows
ORDER BY date, asset
"""


def sql_reversal(panel) -> pd.DataFrame:
    """由已补完整日历的 Panel 建 SQLite 内存表，缺任何回看价就不评分。"""
    # load_panel 已把原始 close×adj_factor，并补全 date×asset 网格。
    bars = panel.data[["close"]].reset_index().rename(columns={"close": "adj_close"})
    bars["date"] = bars["date"].dt.strftime("%Y-%m-%d")
    with sqlite3.connect(":memory:") as connection:
        bars.to_sql("bars_calendar_aligned", connection, index=False, if_exists="replace")
        result = pd.read_sql_query(SQL, connection, parse_dates=["date"])
    return result.pivot(index="date", columns="asset", values="reversal_5d").reindex(
        index=panel.sessions, columns=panel.assets
    )


def feature_frames(panel) -> dict[str, pd.DataFrame]:
    """两个特征只用截至t收盘的数据；低波为20个日收益的负样本标准差。"""
    close = panel.wide("close")
    returns = close / close.shift(1) - 1  # 不使用会自动填价的默认 pct_change。
    lowvol = -returns.rolling(20, min_periods=20).std(ddof=1)
    return {"reversal_5d": sql_reversal(panel), "lowvol_20d": lowvol}


def fit_ridge_train(x: pd.DataFrame, y, alpha: float = ALPHA) -> dict:
    """只用训练数据拟合均值、ddof=0标准差与系数；截距不受L2惩罚。"""
    if x.empty or not np.isfinite(x.to_numpy()).all():
        raise ValueError("训练特征须非空且全部为有限值。")
    target = np.asarray(y, dtype=float)
    if target.shape != (len(x),) or not np.isfinite(target).all() or alpha <= 0:
        raise ValueError("训练标签须与特征逐行对齐、有限，alpha须为正。")
    mean, scale = x.mean(), x.std(ddof=0)
    if scale.le(1e-12).any():
        raise ValueError("训练特征存在常数列，需先说明处理政策，不能偷偷除以零。")
    z = ((x - mean) / scale).to_numpy()
    intercept = float(target.mean())
    coef = np.linalg.solve(z.T @ z + alpha * np.eye(x.shape[1]), z.T @ (target - intercept))
    return {"mean": mean, "scale": scale, "coef": coef,
            "intercept": intercept, "alpha": float(alpha)}


def predict_ridge(model: dict, x: pd.DataFrame) -> np.ndarray:
    """验证与研究留出仅复用训练处理参数，不重新估计。"""
    if list(x.columns) != list(model["mean"].index) or not np.isfinite(x.to_numpy()).all():
        raise ValueError("预测特征列顺序必须与训练相同，并且全部为有限值。")
    z = ((x - model["mean"]) / model["scale"]).to_numpy()
    return model["intercept"] + z @ model["coef"]


def run(data_dir: Path, output_dir: Path) -> dict:
    panel = load_panel(data_dir / "panel.csv", sessions=data_dir / "sessions.csv")
    frames = feature_frames(panel)
    np.testing.assert_allclose(
        frames["reversal_5d"].to_numpy(), reversal_factor(panel, 5).to_numpy(),
        rtol=1e-12, atol=1e-12, equal_nan=True,
        err_msg="SQL反转与lab主线不一致，请先检查日历、复权与窗口。",
    )
    # 所有宽表索引/列均来自同一 Panel；保留空格，最后仅为统计拟合剔除缺失。
    labels = forward_returns(panel, HORIZON)
    table = pd.DataFrame({
        **{name: frame.stack(future_stack=True) for name, frame in frames.items()},
        "label_h5": labels.stack(future_stack=True),
    })
    parts, coverage_rows = {}, []
    for name, (start, end) in SPLITS.items():
        dates = sample_dates(panel.sessions, start, end, HORIZON)
        candidate = table.loc[table.index.get_level_values("date").isin(dates)]
        complete = candidate.dropna(subset=FEATURES + ["label_h5"]).copy()
        if complete.empty:
            raise ValueError(f"{name}没有完整特征与成熟标签，停止教学实验。")
        complete["split"] = name
        parts[name] = complete
        last_signal = complete.index.get_level_values("date").max()
        last_exit = panel.sessions[panel.sessions.get_loc(last_signal) + 1 + HORIZON]
        coverage_rows.append({"split": name, "candidate_rows": len(candidate),
                              "complete_rows": len(complete),
                              "missing_rows": len(candidate) - len(complete),
                              "signal_dates": complete.index.get_level_values("date").nunique(),
                              "last_signal_date": str(last_signal.date()),
                              "last_label_end_date": str(last_exit.date())})
    train = parts["训练"]
    model = fit_ridge_train(train[FEATURES], train["label_h5"].to_numpy(), alpha=ALPHA)
    ic_rows, diagnostic_rows = [], []
    for split_name, part in parts.items():
        part["ridge_score"] = predict_ridge(model, part[FEATURES])
        # 等权基线使用同一训练期均值/标准差，固定方向，不优化组合权重。
        part["equal_score"] = ((part[FEATURES] - model["mean"]) / model["scale"]).mean(axis=1)
        prediction_error = part["ridge_score"] - part["label_h5"]
        aligned_labels = part["label_h5"].unstack("asset")
        for score_name in ["reversal_5d", "lowvol_20d", "equal_score", "ridge_score"]:
            scores = part[score_name].unstack("asset")
            ic = daily_rank_ic(scores, aligned_labels, min_assets=10)
            ic_rows.append(ic.reset_index().assign(split=split_name, score_name=score_name))
            diagnostic_rows.append({"split": split_name, "score_name": score_name,
                                    "rows": len(part), **summarize_ic(ic),
                                    "ridge_rmse": float(np.sqrt((prediction_error ** 2).mean())) if score_name == "ridge_score" else None,
                                    "ridge_mae": float(prediction_error.abs().mean()) if score_name == "ridge_score" else None})
    output_dir.mkdir(parents=True, exist_ok=True)
    pd.concat(parts.values()).reset_index().to_csv(output_dir / "predictions.csv", index=False)
    pd.concat(ic_rows, ignore_index=True).to_csv(output_dir / "daily_ic.csv", index=False)
    pd.DataFrame(diagnostic_rows).to_csv(output_dir / "diagnostics.csv", index=False)
    pd.DataFrame(coverage_rows).to_csv(output_dir / "coverage_and_boundaries.csv", index=False)
    summary = {
        "status": "固定20股教学研究；2025年已展示，不是完全未见的独立证据",
        "sql_matches_lab": True, "alpha": ALPHA,
        "objective": "sum((y-intercept-Z@coef)^2)+alpha*sum(coef^2)；不惩罚截距",
        "features": FEATURES, "feature_rule": "反转5；20日收益负样本标准差ddof=1；缺值不填补",
        "preprocessing": "仅2023训练期拟合均值与ddof=0标准差；2024/2025原样复用",
        "label": "t收盘后信号，t+1至t+6调整开盘价收益；所有年度按sample_dates剔除跨界标签",
        "split_rule": "按完整日期分段，禁止随机拆股票行；固定alpha不搜索、不用验证年重拟合",
        "training_mean": model["mean"].to_dict(), "training_scale": model["scale"].to_dict(),
        "coef": dict(zip(FEATURES, model["coef"].tolist())), "intercept": model["intercept"],
        "quality": panel.quality, "coverage_and_boundaries": coverage_rows,
        "limitations": ["事后固定20股，不能代表历史A股全市场", "供应商当前历史视图仍可能修订",
                        "无中性化、无成本和可交易性引擎；这些IC不是策略收益",
                        "每日H5标签重叠；未做显著性和多重检验推断",
                        "未证明Ridge或等权合成有样本外增量"],
    }
    (output_dir / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SQL反转已与lab逐格核对一致；Ridge固定alpha=10，仅训练期拟合。")
    print(pd.DataFrame(diagnostic_rows)[["split", "score_name", "n_dates", "mean_rank_ic", "ridge_rmse"]].to_string(index=False))
    print("仅教学诊断：2025年已经展示，不是新的独立预测证据。输出位置：", output_dir)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从现有CSV演示SQL与固定Ridge；不联网、不交易、不搜索参数。")
    parser.add_argument("--data-dir", type=Path, default=HERE / "real_data")
    parser.add_argument("--output-dir", type=Path, default=HERE / "sql_ml_outputs")
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)
