"""股票因子研究教学实验台：透明计算、统一交易日网格、无网络请求。

本模块的模拟数据不代表任何真实股票、A 股收益或可交易策略。
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class Panel:
    """所有字段均已对齐到完整的 date × asset 网格，价格不填补。"""

    data: pd.DataFrame
    sessions: pd.DatetimeIndex
    assets: pd.Index
    quality: dict

    def wide(self, column: str) -> pd.DataFrame:
        if column not in self.data.columns:
            raise ValueError(f"数据缺少字段：{column}")
        return self.data[column].unstack("asset").reindex(index=self.sessions, columns=self.assets)


def read_sessions(sessions) -> pd.DatetimeIndex:
    """读取显式交易日历。真实数据不得以股票已有行替代交易所日历。"""
    if isinstance(sessions, (str, Path)):
        table = pd.read_csv(sessions)
        if "date" not in table:
            raise ValueError("日历 CSV 必须有 date 列。")
        sessions = table["date"]
    elif isinstance(sessions, pd.DataFrame):
        sessions = sessions["date"]
    dates = pd.DatetimeIndex(pd.to_datetime(sessions, errors="raise"))
    if dates.tz is not None or dates.hasnans or not dates.equals(dates.normalize()):
        raise ValueError("交易日历须为无时区、不带时分秒的有效日期。")
    if dates.has_duplicates or not dates.is_monotonic_increasing or len(dates) < 2:
        raise ValueError("交易日历须严格递增、无重复，且至少包含两个日期。")
    return dates.rename("date")


def load_panel(source, *, sessions, already_adjusted: bool = False) -> Panel:
    """加载 CSV/长表并校验。价格复权乘数为 adj_factor；禁止猜测复权状态。

    必需列 date,asset,open,close。未声明 already_adjusted=True 时还需
    adj_factor，调整后价格=原价格×adj_factor。amount,industry,log_mv 可选。
    因子计算依赖当时可得字段；本函数无法替代数据供应商的历史时点核验。
    """
    calendar = read_sessions(sessions)
    if isinstance(source, (str, Path)):
        frame = pd.read_csv(source, dtype={"asset": "string"})
    else:
        frame = source.copy()
    required = {"date", "asset", "open", "close"}
    if not required.issubset(frame):
        raise ValueError(f"缺少必需字段：{sorted(required - set(frame.columns))}")
    frame["asset"] = frame["asset"].astype("string")
    if frame.empty:
        raise ValueError("价格长表不能为空。")
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    dates = pd.DatetimeIndex(frame["date"])
    if dates.tz is not None or dates.hasnans or not dates.equals(dates.normalize()):
        raise ValueError("date 须为无时区、不带时分秒的有效日期。")
    if frame["asset"].isna().any() or frame["asset"].str.strip().eq("").any():
        raise ValueError("asset 不可缺失或为空。")
    if frame.duplicated(["date", "asset"]).any():
        raise ValueError("存在重复 date×asset，须先查清来源，不能自动取最后一行。")
    if not dates.isin(calendar).all():
        raise ValueError("价格表包含交易日历以外的日期。")
    numeric = [c for c in ["open", "close", "adj_factor", "amount", "log_mv"] if c in frame]
    for col in numeric:
        frame[col] = pd.to_numeric(frame[col], errors="raise")
        if np.isinf(frame[col].dropna()).any():
            raise ValueError(f"{col} 不可为无穷大。")
    for col in ["open", "close"]:
        if frame[col].dropna().le(0).any():
            raise ValueError(f"{col} 必须为正数，缺价应留空，不可写 0。")
    if "amount" in frame and frame["amount"].dropna().lt(0).any():
        raise ValueError("amount 不可为负数。")
    if not already_adjusted:
        if "adj_factor" not in frame:
            raise ValueError("缺少 adj_factor；确已复权时请显式传 already_adjusted=True。")
        priced = frame[["open", "close"]].notna().any(axis=1)
        if (priced & (frame["adj_factor"].isna() | frame["adj_factor"].le(0))).any():
            raise ValueError("有价格的行必须有正数 adj_factor。")
        frame["open"] = frame["open"] * frame["adj_factor"]
        frame["close"] = frame["close"] * frame["adj_factor"]
    assets = pd.Index(sorted(frame["asset"].unique()), name="asset")
    grid = pd.MultiIndex.from_product([calendar, assets], names=["date", "asset"])
    observed = len(frame)
    full = frame.set_index(["date", "asset"]).sort_index().reindex(grid)
    quality = {
        "observed_rows": observed, "expected_grid_rows": len(grid),
        "missing_grid_rows": len(grid) - observed,
        "missing_open_cells": int(full["open"].isna().sum()),
        "missing_close_cells": int(full["close"].isna().sum()),
        "n_sessions": len(calendar), "n_assets": len(assets),
        "already_adjusted": already_adjusted,
        "price_rule": "声明已复权" if already_adjusted else "原价格乘 adj_factor",
    }
    return Panel(full, calendar, assets, quality)


def reversal_factor(panel: Panel, lookback: int = 5) -> pd.DataFrame:
    """t 日收盘形成 -[close(t)/close(t-L)-1]；完整回看窗口缺价则留空。"""
    if lookback < 1:
        raise ValueError("lookback 必须为正整数。")
    close = panel.wide("close")
    raw = -(close / close.shift(lookback) - 1)
    full_window = close.rolling(lookback + 1, min_periods=lookback + 1).count().eq(lookback + 1)
    return raw.where(full_window)


def standardize_factor(raw: pd.DataFrame, lower: float = 0.01, upper: float = 0.99,
                       min_assets: int = 5) -> pd.DataFrame:
    """逐日截面分位数缩尾后 zscore，标准差 ddof=0；不使用跨日参数。"""
    if not 0 <= lower < upper <= 1:
        raise ValueError("分位数应满足 0≤lower<upper≤1。")
    output = pd.DataFrame(np.nan, index=raw.index, columns=raw.columns)
    for date, row in raw.iterrows():
        values = row.dropna()
        if len(values) < min_assets:
            continue
        clipped = values.clip(values.quantile(lower), values.quantile(upper))
        scale = clipped.std(ddof=0)
        if scale > 0:
            output.loc[date, clipped.index] = (clipped - clipped.mean()) / scale
    return output


def neutralize_factor(score: pd.DataFrame, panel: Panel, min_extra: int = 2) -> pd.DataFrame:
    """可选教学 OLS：截距+历史行业虚拟变量+历史 log_mv，残差再标准化。

    两项都须有真实当日历史字段。它只是简单风格控制，不是 Barra 模型。
    """
    if not {"industry", "log_mv"}.issubset(panel.data):
        raise ValueError("中性化需要历史 industry 和 log_mv；不能用当前行业回填过去。")
    industries, sizes = panel.wide("industry"), panel.wide("log_mv")
    result = pd.DataFrame(np.nan, index=score.index, columns=score.columns)
    for date, row in score.iterrows():
        sample = pd.DataFrame({"score": row, "industry": industries.loc[date],
                               "log_mv": sizes.loc[date]}).dropna()
        if sample.empty:
            continue
        dummies = pd.get_dummies(sample["industry"].astype(str), drop_first=True, dtype=float)
        design = np.column_stack([np.ones(len(sample)), sample["log_mv"].to_numpy(), dummies])
        if len(sample) < design.shape[1] + min_extra:
            continue
        coef = np.linalg.lstsq(design, sample["score"].to_numpy(), rcond=None)[0]
        residual = sample["score"].to_numpy() - design @ coef
        scale = residual.std(ddof=0)
        if scale > 1e-12:
            result.loc[date, sample.index] = residual / scale
    return result


def forward_returns(panel: Panel, horizon: int = 5) -> pd.DataFrame:
    """标签 r(t,H)=open(t+1+H)/open(t+1)-1，按统一日历移动。"""
    if horizon < 1:
        raise ValueError("horizon 必须为正整数。")
    opens = panel.wide("open")
    return opens.shift(-(1 + horizon)) / opens.shift(-1) - 1


def time_splits(sessions, fractions=(0.6, 0.2, 0.2)) -> dict:
    """按交易日时间顺序分段；测试集只作最终留出，不用其结果挑参数。"""
    dates = read_sessions(sessions)
    if len(fractions) != 3 or min(fractions) <= 0 or not np.isclose(sum(fractions), 1):
        raise ValueError("三段比例必须为正且合计为 1。")
    first = int(len(dates) * fractions[0])
    second = int(len(dates) * (fractions[0] + fractions[1]))
    if first < 1 or second <= first or second >= len(dates):
        raise ValueError("交易日太少，无法切出三个非空区间。")
    return {"训练": (dates[0], dates[first - 1]),
            "验证": (dates[first], dates[second - 1]),
            "留出": (dates[second], dates[-1])}


def sample_dates(sessions, start, end, horizon: int = 5) -> pd.DatetimeIndex:
    """信号、入场、出场均落在同一区间；出场跨区间的标签剔除。"""
    calendar = read_sessions(sessions)
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    if horizon < 1:
        raise ValueError("horizon 必须为正整数。")
    rows = []
    for i, signal in enumerate(calendar):
        exit_i = i + 1 + horizon
        if exit_i < len(calendar) and signal >= start and calendar[exit_i] <= end:
            rows.append(signal)
    return pd.DatetimeIndex(rows, name="date")


def daily_rank_ic(score: pd.DataFrame, labels: pd.DataFrame, dates=None,
                  min_assets: int = 10) -> pd.DataFrame:
    """每日截面 Spearman = 两边平均名次的 Pearson；无 scipy 依赖。"""
    rows = []
    for date in score.index if dates is None else dates:
        pair = pd.concat([score.loc[date].rename("score"), labels.loc[date].rename("return")], axis=1).dropna()
        value = np.nan
        if len(pair) >= min_assets and pair["score"].nunique() > 1 and pair["return"].nunique() > 1:
            value = pair["score"].rank(method="average").corr(pair["return"].rank(method="average"))
        rows.append({"date": date, "rank_ic": value, "n_assets": len(pair)})
    return pd.DataFrame(rows).set_index("date") if rows else pd.DataFrame(columns=["rank_ic", "n_assets"])


def summarize_ic(ic: pd.DataFrame) -> dict:
    values = ic["rank_ic"].dropna()
    mean = values.mean() if len(values) else np.nan
    std = values.std(ddof=1) if len(values) > 1 else np.nan
    return {"n_dates": len(values), "mean_rank_ic": mean, "std_rank_ic": std,
            "icir_unannualized": mean / std if pd.notna(std) and std > 0 else np.nan,
            "positive_fraction": values.gt(0).mean() if len(values) else np.nan}


def assign_groups(row: pd.Series, groups: int = 5) -> pd.Series:
    """保留并列名次；若无法形成全部分组就拒绝，不靠股票名强拆并列。"""
    values = row.dropna()
    if len(values) < groups or values.nunique() < groups:
        raise ValueError("有效股票或不同因子值不足，不能形成完整分层。")
    labels = pd.qcut(values.rank(method="average"), q=groups, labels=False, duplicates="drop") + 1
    if labels.nunique() != groups:
        raise ValueError("并列值导致不足五层，须检查该日截面。")
    return labels.astype(int)


def trade_to_target(pre_weights: pd.Series, target_weights: pd.Series,
                    fee_rate: float = 0.001) -> dict:
    """精确计单边费率：成交买卖总额×c，目标权重占扣费后净资产。

    令 x=扣费后资产/扣费前资产，解 x=1-c*Σ|x*w_i-p_i|。
    初始现金 p_i=0 时 x=1/(1+c)；最后全清仓时 x=1-c。
    返回成交额与费用均相对扣费前资产，不把总成交额除以 2。
    """
    if not 0 <= fee_rate < 0.5:
        raise ValueError("教学单边费率须位于 [0, 0.5)。")
    assets = pre_weights.index.union(target_weights.index)
    before = pre_weights.reindex(assets, fill_value=0.0).astype(float)
    target = target_weights.reindex(assets, fill_value=0.0).astype(float)
    if before.isna().any() or target.isna().any() or min(before.min(), target.min()) < -1e-12:
        raise ValueError("这里只支持非负有限权重。")
    if not np.isfinite(before).all() or not np.isfinite(target).all():
        raise ValueError("权重不可含无穷大。")
    if before.sum() > 1 + 1e-9 or not (np.isclose(target.sum(), 1) or np.isclose(target.sum(), 0)):
        raise ValueError("初始风险仓位之和不可超过 1；目标须为满仓或全现金。")
    low, high = 0.0, 1.0
    for _ in range(80):
        middle = (low + high) / 2
        equation = middle + fee_rate * (middle * target - before).abs().sum() - 1
        if equation > 0:
            high = middle
        else:
            low = middle
    remaining = (low + high) / 2
    change = remaining * target - before
    bought, sold = change.clip(lower=0).sum(), -change.clip(upper=0).sum()
    turnover = bought + sold
    return {"remaining_fraction": remaining, "buy_fraction": float(bought),
            "sell_fraction": float(sold), "turnover_total": float(turnover),
            "cost_fraction": float(turnover * fee_rate)}


def backtest_groups(panel: Panel, score: pd.DataFrame, *, start, end, horizon: int = 5,
                    fee_rate: float = 0.001, groups: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """每 H 个交易日调仓；t 收盘信号，t+1 开盘买，t+1+H 开盘卖/调。

    Q1…Q5 与等权样本基准分别独立记账。Q5-Q1 是两条多头收益之差，
    不模拟融券、保证金或做空，不能当成可交易多空组合。持仓缺进/出场价
    会报错，不能因未来无价而事先删除股票。未模拟停牌、涨跌停或冲击成本。
    """
    if horizon < 1:
        raise ValueError("horizon 必须为正整数。")
    opens = panel.wide("open")
    candidates = sample_dates(panel.sessions, start, end, horizon)
    # 只用当日因子是否可分层确定首个信号；以后保持固定 H 日节奏。
    first = None
    for date in candidates:
        if score.loc[date].notna().sum() >= groups and score.loc[date].nunique() >= groups:
            first = panel.sessions.get_loc(date)
            break
    if first is None:
        raise ValueError("区间内没有可形成分层的因子截面。")
    selected = [d for d in candidates if panel.sessions.get_loc(d) >= first
                and (panel.sessions.get_loc(d) - first) % horizon == 0]
    names = [f"Q{i}" for i in range(1, groups + 1)] + ["等权样本"]
    state = {name: {"nav": 1.0, "weights": pd.Series(0.0, index=panel.assets)} for name in names}
    periods, trades = [], []
    for step, signal in enumerate(selected):
        position = panel.sessions.get_loc(signal)
        entry, exit_date = panel.sessions[position + 1], panel.sessions[position + 1 + horizon]
        allocation = assign_groups(score.loc[signal], groups)
        for name in names:
            members = allocation.index if name == "等权样本" else allocation.index[allocation == int(name[1:])]
            target = pd.Series(0.0, index=panel.assets)
            target.loc[members] = 1 / len(members)
            if opens.loc[entry, members].isna().any() or opens.loc[exit_date, members].isna().any():
                raise ValueError(f"{signal.date()} 的 {name} 持仓缺进/出场开盘价；本实验台停止记账，请补充停牌/退市处置规则。")
            current = state[name]
            # current.weights 已由前一持有期的实际涨跌漂移，不是旧目标权重。
            trade = trade_to_target(current["weights"], target, fee_rate)
            before_nav = current["nav"]
            after_trade_nav = before_nav * trade["remaining_fraction"]
            asset_growth = opens.loc[exit_date, members] / opens.loc[entry, members]
            gross_growth = float((target.loc[members] * asset_growth).sum())
            end_nav = after_trade_nav * gross_growth
            drifted = pd.Series(0.0, index=panel.assets)
            drifted.loc[members] = target.loc[members] * asset_growth / gross_growth
            trades.append({"portfolio": name, "date": entry, "event": "首次建仓" if step == 0 else "调仓",
                           "before_nav": before_nav, "after_nav": after_trade_nav, **trade})
            final_cost = 0.0
            if step == len(selected) - 1:
                liquidation = trade_to_target(drifted, pd.Series(0.0, index=panel.assets), fee_rate)
                liquidated_nav = end_nav * liquidation["remaining_fraction"]
                trades.append({"portfolio": name, "date": exit_date, "event": "最后平仓",
                               "before_nav": end_nav, "after_nav": liquidated_nav, **liquidation})
                final_cost = liquidation["cost_fraction"]
                end_nav = liquidated_nav
            periods.append({"portfolio": name, "signal_date": signal, "entry_date": entry,
                            "exit_date": exit_date, "n_assets": len(members),
                            "gross_return": gross_growth - 1,
                            "net_return": end_nav / before_nav - 1,
                            "nav": end_nav, "rebalance_turnover_total": trade["turnover_total"],
                            "rebalance_cost": trade["cost_fraction"], "final_liquidation_cost": final_cost})
            current["nav"], current["weights"] = end_nav, drifted
    return pd.DataFrame(periods), pd.DataFrame(trades)


def make_synthetic_panel(n_sessions: int = 600, n_assets: int = 50, seed: int = 573):
    """纯教学模拟：工作日日历不是交易所日历，行业/市值不属于真实股票。"""
    if n_sessions < 60 or n_assets < 10:
        raise ValueError("演示至少需要 60 个工作日和 10 只模拟股票。")
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2022-01-03", periods=n_sessions, name="date")
    assets = [f"SIM{i:03d}" for i in range(n_assets)]
    sector = np.arange(n_assets) % 5
    log_size = rng.normal(23, 0.8, n_assets)
    adjusted_close = np.empty((n_sessions, n_assets))
    adjusted_open = np.empty_like(adjusted_close)
    prior = rng.uniform(10, 100, n_assets)
    previous_idio = np.zeros(n_assets)
    for t in range(n_sessions):
        market = rng.normal(0.00015, 0.006)
        industry_move = rng.normal(0, 0.003, 5)[sector]
        idio = 0.12 * previous_idio + rng.normal(0, 0.012, n_assets)
        # 一点弱动量用于展示：反转假设可能失败，不为美化结果校准种子。
        overnight = rng.normal(0, 0.0025, n_assets)
        adjusted_open[t] = prior * np.exp(overnight)
        adjusted_close[t] = adjusted_open[t] * np.exp(market + industry_move + idio)
        prior, previous_idio = adjusted_close[t], idio
    factors = np.ones_like(adjusted_close)
    factors[n_sessions // 2:, 0] = 2.0  # 模拟拆股，复权后价格连续。
    grid = pd.MultiIndex.from_product([dates, assets], names=["date", "asset"])
    frame = pd.DataFrame({"open": (adjusted_open / factors).ravel(),
                          "close": (adjusted_close / factors).ravel(),
                          "adj_factor": factors.ravel(),
                          "amount": rng.lognormal(17, 0.7, n_sessions * n_assets),
                          "industry": np.tile([f"模拟行业{x + 1}" for x in sector], n_sessions),
                          "log_mv": (log_size[None, :] + np.log(adjusted_close / adjusted_close[0])).ravel()}, index=grid).reset_index()
    return frame, dates


def save_demo_outputs(root: Path) -> dict:
    """固定参数运行一次离线演示；不挑选收益最好的种子或参数。"""
    root = Path(root)
    data_dir, output_dir = root / "demo_data", root / "demo_outputs"
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    frame, sessions = make_synthetic_panel()
    frame.to_csv(data_dir / "synthetic_panel.csv", index=False, float_format="%.10g")
    pd.DataFrame({"date": sessions}).to_csv(data_dir / "synthetic_sessions.csv", index=False)
    panel = load_panel(frame, sessions=sessions)
    score = standardize_factor(reversal_factor(panel, 5))
    neutral = neutralize_factor(score, panel)
    splits = time_splits(sessions)
    labels = forward_returns(panel, 5)
    summaries, all_ics = [], []
    for name, (start, end) in splits.items():
        dates = sample_dates(sessions, start, end, 5)
        ic = daily_rank_ic(score, labels, dates)
        all_ics.append(ic.assign(split=name))
        summaries.append({"split": name, "start": str(start.date()), "end": str(end.date()), **summarize_ic(ic)})
    ic_table = pd.concat(all_ics)
    ic_table.to_csv(output_dir / "daily_ic_by_split.csv", float_format="%.10g")
    pd.DataFrame(summaries).to_csv(output_dir / "ic_summary.csv", index=False)
    start, end = splits["留出"]
    # 衰减使用共同信号日期，避免各 H 因尾部剔除不同而不可比。
    common_dates = sample_dates(sessions, start, end, 20)
    decay = []
    for horizon in [1, 5, 10, 20]:
        ic = daily_rank_ic(score, forward_returns(panel, horizon), common_dates)
        decay.append({"horizon": horizon, **summarize_ic(ic)})
    pd.DataFrame(decay).to_csv(output_dir / "ic_decay_common_dates.csv", index=False)
    periods, trades = backtest_groups(panel, score, start=start, end=end, horizon=5, fee_rate=0.001)
    periods.to_csv(output_dir / "portfolio_periods_oos.csv", index=False, float_format="%.10g")
    trades.to_csv(output_dir / "trade_costs_oos.csv", index=False, float_format="%.10g")
    score.to_csv(output_dir / "factor_scores.csv", float_format="%.10g")
    neutral.to_csv(output_dir / "factor_scores_neutralized.csv", float_format="%.10g")
    gross = periods.pivot(index="exit_date", columns="portfolio", values="gross_return")
    net = periods.pivot(index="exit_date", columns="portfolio", values="net_return")
    diagnostic = pd.DataFrame({"Q5_minus_Q1_gross": gross["Q5"] - gross["Q1"],
                               "Q5_minus_sample_net": net["Q5"] - net["等权样本"]})
    diagnostic.to_csv(output_dir / "diagnostics_oos.csv", float_format="%.10g")
    exposure_rows = []
    for signal in periods["signal_date"].drop_duplicates():
        groups = assign_groups(score.loc[signal])
        selected = groups.index[groups == 5]
        sizes = panel.wide("log_mv").loc[signal]
        industry = panel.wide("industry").loc[signal]
        exposure_rows.append({"signal_date": signal, "Q5_log_mv": sizes.loc[selected].mean(),
                              "sample_log_mv": sizes.loc[groups.index].mean(),
                              **{str(k) + "_weight": float(v) for k, v in industry.loc[selected].value_counts(normalize=True).items()}})
    pd.DataFrame(exposure_rows).fillna(0).to_csv(output_dir / "simple_style_exposure_oos.csv", index=False)
    final_nav = periods.groupby("portfolio", sort=False)["nav"].last()
    summary = {
        "data_label": "纯教学模拟；不代表真实 A 股表现", "seed": 573,
        "lookback": 5, "holding_sessions": 5, "single_side_fee": 0.001,
        "cost_rule": "买卖总成交额×单边费率；含首次建仓和最后平仓；扣费后目标权重精确记账",
        "icir_rule": "每日 Rank IC 均值/样本标准差；未年化；H>1 的逐日标签重叠",
        "portfolio_rule": "每5交易日非重叠开盘到开盘；留出样本；无融券模拟",
        "quality": panel.quality, "ic_summary": summaries,
        "final_nav_oos": final_nav.to_dict(),
        "periods_oos": int(periods.loc[periods["portfolio"].eq("Q5")].shape[0]),
        "limitations": ["模拟日历仅排除周末，非交易所日历", "无停牌涨跌停撮合、冲击、融券或退市回收模型",
                        "等权样本不是沪深300等可投资指数", "简易行业与规模控制不是Barra", "未做统计显著性推断"],
    }
    (output_dir / "run_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    plot_demo_outputs(root, periods, ic_table, pd.DataFrame(decay))
    return summary


def plot_demo_outputs(root: Path, periods, ic_table, decay):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    plt.rcParams.update({"figure.figsize": (10, 4.8), "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.18, "figure.dpi": 130})
    out = Path(root) / "demo_outputs"
    fig, ax = plt.subplots()
    colors = {"Q1": "#b8c9db", "Q2": "#8da8c5", "Q3": "#688baa", "Q4": "#426c91", "Q5": "#16496d", "等权样本": "#b57e31"}
    for name in ["Q1", "Q2", "Q3", "Q4", "Q5", "等权样本"]:
        sample = periods[periods["portfolio"].eq(name)]
        x = [sample["entry_date"].iloc[0]] + sample["exit_date"].tolist()
        y = [1.0] + sample["nav"].tolist()
        ax.plot(x, y, label="Equal-weight sample" if name == "等权样本" else name,
                color=colors[name], linewidth=2 if name in ["Q5", "等权样本"] else 1.2,
                linestyle="--" if name == "等权样本" else "-")
    ax.set(title="Synthetic out-of-sample NAV | every 5 sessions | fees included", ylabel="NAV (initial = 1)", xlabel="Execution date")
    ax.legend(ncol=3, fontsize=9)
    fig.autofmt_xdate(rotation=0)
    fig.tight_layout(); fig.savefig(out / "01_oos_nav.png"); plt.close(fig)
    fig, ax = plt.subplots()
    for name, color in [("训练", "#688baa"), ("验证", "#b57e31"), ("留出", "#16496d")]:
        sample = ic_table[ic_table["split"].eq(name)]["rank_ic"]
        ax.plot(sample.index, sample.rolling(20, min_periods=20).mean(), color=color,
                label={"训练": "Train", "验证": "Validation", "留出": "OOS"}[name])
    ax.axhline(0, color="#454545", linewidth=0.8)
    ax.set(title="Synthetic daily Rank IC | trailing 20-date mean | H=5", ylabel="Rank IC", xlabel="Signal date")
    ax.legend(); fig.autofmt_xdate(rotation=0); fig.tight_layout(); fig.savefig(out / "02_rank_ic.png"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(decay["horizon"].astype(str), decay["mean_rank_ic"], color="#16496d", width=0.55)
    ax.axhline(0, color="#454545", linewidth=0.8)
    ax.set(title="Synthetic OOS IC decay | same signal dates for all horizons",
           xlabel="Holding sessions after next open", ylabel="Mean daily Rank IC")
    fig.tight_layout(); fig.savefig(out / "03_ic_decay.png"); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    mean_returns = periods.groupby("portfolio")["net_return"].mean().reindex(["Q1", "Q2", "Q3", "Q4", "Q5", "等权样本"])
    ax.bar(["Q1", "Q2", "Q3", "Q4", "Q5", "Sample"], mean_returns, color=[colors[n] for n in mean_returns.index])
    ax.axhline(0, color="#454545", linewidth=0.8)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.set(title="Synthetic OOS mean 5-session net return | not annualized", ylabel="Mean period return")
    fig.tight_layout(); fig.savefig(out / "04_group_returns.png"); plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="运行纯教学模拟股票因子全流程；不联网、不读取 token。")
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = save_demo_outputs(args.output_root)
    print("教学模拟运行完成，结果保存在：", args.output_root / "demo_outputs")
    print(json.dumps({"留出最终净值": result["final_nav_oos"], "留出非重叠期数": result["periods_oos"]}, ensure_ascii=False, indent=2))
