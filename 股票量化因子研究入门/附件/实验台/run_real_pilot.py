"""固定真实小样本教学研究：不调参、不改方向、不模拟完整A股撮合。"""
from pathlib import Path
import hashlib
import json
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

from lab import (load_panel, reversal_factor, standardize_factor, forward_returns,
                 sample_dates, daily_rank_ic, summarize_ic, backtest_groups, assign_groups)

HERE = Path(__file__).resolve().parent


def run():
    data, out = HERE / "real_data", HERE / "real_outputs"
    out.mkdir(exist_ok=True)
    manifest = json.loads((data / "manifest.json").read_text())
    if not manifest.get("complete"):
        raise RuntimeError("真实数据下载不完整。先查 manifest 中的失败分段。")
    for name, key in [("panel.csv", "panel_sha256"), ("sessions.csv", "sessions_sha256")]:
        if hashlib.sha256((data / name).read_bytes()).hexdigest() != manifest[key]:
            raise RuntimeError(f"{name} 与下载记录哈希不同，需另建数据版本后再研究。")
    panel = load_panel(data / "panel.csv", sessions=data / "sessions.csv")
    score = standardize_factor(reversal_factor(panel, 5))
    labels = forward_returns(panel, 5)
    # 分割与方向在下载前的 pilot_protocol.json 已固定，无基于表现的搜索。
    splits = {"训练": ("2023-01-01", "2023-12-31"),
              "验证": ("2024-01-01", "2024-12-31"),
              "留出": ("2025-01-01", "2025-12-31")}
    summaries, ics, periods_all, trades_all = [], [], [], []
    for split, (start, end) in splits.items():
        dates = sample_dates(panel.sessions, start, end, 5)
        ic = daily_rank_ic(score, labels, dates)
        ics.append(ic.assign(split=split))
        periods, trades = backtest_groups(panel, score, start=start, end=end, horizon=5, fee_rate=0.001)
        periods_all.append(periods.assign(split=split))
        trades_all.append(trades.assign(split=split))
        final = periods.groupby("portfolio")["nav"].last()
        summaries.append({"split": split, "start": start, "end": end,
                          **summarize_ic(ic), "nonoverlap_periods": int(periods.portfolio.eq("Q5").sum()),
                          "q5_net_final_nav": float(final["Q5"]),
                          "sample_net_final_nav": float(final["等权样本"])})
    all_ic = pd.concat(ics)
    all_periods = pd.concat(periods_all, ignore_index=True)
    all_trades = pd.concat(trades_all, ignore_index=True)
    pd.DataFrame(summaries).to_csv(out / "ic_and_portfolio_summary.csv", index=False)
    all_ic.to_csv(out / "daily_rank_ic.csv")
    all_periods.to_csv(out / "portfolio_periods.csv", index=False)
    all_trades.to_csv(out / "trades_and_costs.csv", index=False)
    score.to_csv(out / "factor_scores.csv")

    # 费用压力仅用于诊断，不从中选最佳费用或改变样本外主结果。
    stress = []
    for fee in [0.0, 0.0005, 0.001, 0.002]:
        p, _ = backtest_groups(panel, score, start=splits["留出"][0], end=splits["留出"][1], fee_rate=fee)
        final = p.groupby("portfolio")["nav"].last()
        stress.append({"single_side_fee": fee, "q5_final_nav": final["Q5"],
                       "sample_final_nav": final["等权样本"]})
    pd.DataFrame(stress).to_csv(out / "oos_cost_stress.csv", index=False)
    common_dates = sample_dates(panel.sessions, *splits["留出"], horizon=20)
    decay = [{"horizon": h, **summarize_ic(daily_rank_ic(score, forward_returns(panel, h), common_dates))}
             for h in [1, 5, 10, 20]]
    pd.DataFrame(decay).to_csv(out / "oos_ic_decay_common_dates.csv", index=False)

    # 当时已知20日成交额，只给“整笔新建仓占全日ADV”的粗略情景，不冒充开盘容量。
    adv20 = panel.wide("amount").rolling(20, min_periods=20).mean()
    capacity_rows = []
    oos = all_periods[all_periods.split.eq("留出")]
    for date in oos.signal_date.drop_duplicates():
        groups = assign_groups(score.loc[date])
        names = groups.index[groups.eq(5)]
        values = adv20.loc[date, names]
        capacity_rows.append({"signal_date": date, "n_q5": len(names), "assumed_full_day_participation": 0.05,
                              "minimum_adv20_yuan": values.min(),
                              "full_new_position_capital_scenario_yuan": values.min() * 0.05 * len(names)})
    pd.DataFrame(capacity_rows).to_csv(out / "oos_adv_capacity_scenario.csv", index=False)
    summary = {
        "label": "真实固定20股教学样本；非全A股因子有效性或可交易业绩证明",
        "protocol": manifest["protocol"], "quality": panel.quality,
        "input_panel_sha256": manifest["panel_sha256"],
        "code_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                        for name in ["lab.py", "run_real_pilot.py", "download_tushare_pilot.py"]},
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__},
        "splits": summaries, "cost_stress": stress, "decay": decay,
        "cost_rule": "单边10bps作用于买卖总成交额；漂移后权重；含首建末平；理想化同费率",
        "split_rule": "各年份独立从现金开始并平仓；仅保留入场和出场均在该段内的样本；不是连续跨年实盘账本",
        "limitations": ["事后人工固定20股，选择与幸存者偏差", "当前供应商历史数据视图，未验证历史修订快照",
                        "缺少历史行业/市值，未做真实中性化和Barra", "开盘理想化成交，无涨跌停/停牌队列/手数/冲击/历史非对称税费",
                        "基准为样本等权而非市场指数，Q5-Q1仅统计诊断", "H5逐日标签重叠，未做显著性推断",
                        "容量仅全日ADV粗略情景，不能代表开盘可成交容量", "首次留出已在教学中展示，再调整将使其成为研究样本"],
    }
    (out / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    plt.rcParams.update({"figure.figsize": (10, 4.7), "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.17, "figure.dpi": 130})
    fig, ax = plt.subplots()
    for name, color in [("Q1", "#bac6d2"), ("Q2", "#97b0c6"), ("Q3", "#7798b5"),
                        ("Q4", "#517b9b"), ("Q5", "#154b70"), ("等权样本", "#ac762d")]:
        p = oos[oos.portfolio.eq(name)]
        ax.plot([p.entry_date.iloc[0]] + p.exit_date.tolist(), [1.] + p.nav.tolist(),
                label="Equal-weight sample" if name == "等权样本" else name, color=color,
                linewidth=2 if name in ["Q5", "等权样本"] else 1.1,
                linestyle="--" if name == "等权样本" else "-")
    ax.set(title="Fixed 20-stock teaching sample | 2025 holdout | idealized fills", xlabel="Execution date", ylabel="NAV (initial = 1; 10 bps one-side fee)")
    ax.legend(ncol=3, fontsize=9); fig.autofmt_xdate(rotation=0); fig.tight_layout()
    fig.savefig(out / "01_real_nav.png"); plt.close(fig)
    fig, ax = plt.subplots()
    for split, color in [("训练", "#7798b5"), ("验证", "#ac762d"), ("留出", "#154b70")]:
        values = all_ic.loc[all_ic.split.eq(split), "rank_ic"]
        ax.plot(values.index, values.rolling(20, min_periods=20).mean(), color=color,
                label={"训练": "2023 Train", "验证": "2024 Validation", "留出": "2025 Holdout"}[split])
    ax.axhline(0, color="#444", linewidth=.8)
    ax.set(title="Daily Rank IC | trailing 20 signal dates | H=5 labels overlap", xlabel="Signal date", ylabel="Rank IC (not statistical significance)")
    ax.legend(); fig.autofmt_xdate(rotation=0); fig.tight_layout()
    fig.savefig(out / "02_real_ic.png"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    means = oos.groupby("portfolio").net_return.mean().reindex(["Q1", "Q2", "Q3", "Q4", "Q5", "等权样本"])
    ax.bar(["Q1", "Q2", "Q3", "Q4", "Q5", "Sample"], means, color="#154b70")
    ax.axhline(0, color="#444", linewidth=.8); ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.set(title="2025 fixed-sample mean 5-session net returns | not annualized", ylabel="Mean period return")
    fig.tight_layout(); fig.savefig(out / "03_real_groups.png"); plt.close(fig)
    print(pd.DataFrame(summaries).to_string(index=False))
    return summary


if __name__ == "__main__":
    run()
