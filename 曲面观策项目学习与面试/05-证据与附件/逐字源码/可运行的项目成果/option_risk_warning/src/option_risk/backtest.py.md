---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/backtest.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/backtest.py>)

SHA-256：`abad29bcf942793596b8d1943c6dc3496bf38cc40db02b813094afd58b7eba58`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import numpy as np
import pandas as pd


def _cvar95(returns: pd.Series) -> float:
    values = returns.dropna().astype(float)
    if values.empty:
        return np.nan
    cutoff = values.quantile(0.05)
    return float(-values.loc[values <= cutoff].mean())


def _trading_day(timestamp: pd.Timestamp) -> pd.Timestamp:
    day = timestamp.normalize() + (pd.Timedelta(days=1) if timestamp.hour >= 20 else pd.Timedelta(0))
    if day.weekday() == 5:
        day += pd.Timedelta(days=2)
    elif day.weekday() == 6:
        day += pd.Timedelta(days=1)
    return day


def _strategy_return(
    daily: pd.DataFrame,
    baseline: pd.Series,
    effective_date: pd.Timestamp | None,
    sign: float,
) -> tuple[pd.Series, pd.Series]:
    strategy = baseline.copy()
    exposure = pd.Series(1.0, index=baseline.index)
    if effective_date is None or effective_date not in strategy.index:
        return strategy, exposure
    after = strategy.index > effective_date
    strategy.loc[after] = baseline.loc[after] * 0.5
    exposure.loc[strategy.index >= effective_date] = 0.5
    previous_close = daily["close"].shift(1).loc[effective_date]
    if pd.notna(previous_close) and previous_close != 0:
        split_day_long = (
            (daily.loc[effective_date, "open"] - previous_close)
            + 0.5 * (daily.loc[effective_date, "close"] - daily.loc[effective_date, "open"])
        ) / previous_close
        strategy.loc[effective_date] = sign * split_day_long
    return strategy, exposure


def _improvement_for_date(
    daily: pd.DataFrame, effective_date: pd.Timestamp | None
) -> tuple[list[dict[str, object]], float, pd.DataFrame]:
    daily_return = daily["close"].pct_change().dropna()
    rows: list[dict[str, object]] = []
    detail = daily.loc[daily_return.index].copy()
    exposure_result: pd.Series | None = None
    for side, sign in [("long", 1.0), ("short", -1.0)]:
        baseline = sign * daily_return
        strategy, exposure = _strategy_return(daily, baseline, effective_date, sign)
        exposure_result = exposure
        baseline_cvar = _cvar95(baseline)
        strategy_cvar = _cvar95(strategy)
        improvement = (
            (baseline_cvar - strategy_cvar) / baseline_cvar
            if effective_date is not None and baseline_cvar > 0
            else 0.0
        )
        detail[f"{side}_baseline_return"] = baseline
        detail[f"{side}_warning_return"] = strategy
        rows.append(
            {
                "side": side,
                "baseline_cvar95": baseline_cvar,
                "warning_cvar95": strategy_cvar,
                "improvement_rate": float(improvement),
            }
        )
    detail["warning_strategy_exposure"] = exposure_result
    return rows, float(np.mean([row["improvement_rate"] for row in rows])), detail


def cvar_warning_backtest(
    alerts: pd.DataFrame, simulations: int = 1000, random_state: int = 42
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame]:
    """Competition-style long/short CVaR comparison using the reconstructed future proxy."""

    test = alerts.loc[alerts["split"].eq("test")].copy()
    test["trading_day"] = [_trading_day(pd.Timestamp(value)) for value in test.index]
    daily = test.groupby("trading_day", observed=True)["reference_underlying_price"].agg(
        open="first", close="last"
    ).dropna()
    daily_return = daily["close"].pct_change().dropna()
    warning_times = test.index[test["alert_emitted"].fillna(False).astype(bool)]
    first_warning = pd.Timestamp(warning_times.min()) if len(warning_times) else None

    effective_date: pd.Timestamp | None = None
    if first_warning is not None:
        warning_trading_day = _trading_day(first_warning)
        later_days = daily_return.index[daily_return.index > warning_trading_day]
        if len(later_days):
            effective_date = pd.Timestamp(later_days[0])

    rows, model_improvement, detail = _improvement_for_date(daily, effective_date)
    detail["underlying_return"] = daily_return
    comparison = pd.DataFrame(rows)

    rng = np.random.default_rng(random_state)
    # A warning on the first test trading day can make the first return-bearing
    # day a valid next-day half-exposure date, so the random comparator must
    # sample the exact same eligible domain as the formal strategy.
    eligible_dates = daily_return.index
    random_rows: list[dict[str, object]] = []
    if len(eligible_dates):
        for simulation, random_date in enumerate(
            rng.choice(eligible_dates.to_numpy(), size=simulations, replace=True), start=1
        ):
            _, improvement, _ = _improvement_for_date(daily, pd.Timestamp(random_date))
            random_rows.append(
                {
                    "simulation": simulation,
                    "random_half_exposure_date": pd.Timestamp(random_date),
                    "average_improvement_rate": improvement,
                }
            )
    random_baseline = pd.DataFrame(random_rows)
    if len(random_baseline):
        random_quantiles = random_baseline["average_improvement_rate"].quantile(
            [0.05, 0.50, 0.95]
        )
        random_summary = {
            "simulations": int(len(random_baseline)),
            "eligible_date_count": int(len(eligible_dates)),
            "eligible_start": pd.Timestamp(eligible_dates[0]),
            "eligible_end": pd.Timestamp(eligible_dates[-1]),
            "p05": float(random_quantiles.loc[0.05]),
            "median": float(random_quantiles.loc[0.50]),
            "p95": float(random_quantiles.loc[0.95]),
            "model_percentile_among_random_dates": float(
                random_baseline["average_improvement_rate"].le(model_improvement).mean()
            ),
            "model_excess_over_random_median": float(
                model_improvement - random_quantiles.loc[0.50]
            ),
        }
    else:
        random_summary = {
            "simulations": 0,
            "eligible_date_count": 0,
            "eligible_start": None,
            "eligible_end": None,
        }
    metrics = {
        "price_proxy": "median reconstructed underlying price from strike/moneyness; trading-day first/last",
        "trading_day_rule": "timestamps at or after 20:00 are assigned to the next weekday trading day",
        "first_level_2_or_3_warning": first_warning,
        "first_alert_emission": first_warning,
        "half_exposure_effective_date": effective_date,
        "test_trading_days": int(len(daily_return)),
        "long": comparison.loc[comparison["side"].eq("long")].iloc[0].to_dict(),
        "short": comparison.loc[comparison["side"].eq("short")].iloc[0].to_dict(),
        "average_improvement_rate": model_improvement,
        "random_warning_date_baseline": random_summary,
        "interpretation": "The raw improvement includes mechanical exposure halving; compare it with the random-date distribution before attributing value to the warning model.",
    }
    return metrics, detail, random_baseline
````

</details>
