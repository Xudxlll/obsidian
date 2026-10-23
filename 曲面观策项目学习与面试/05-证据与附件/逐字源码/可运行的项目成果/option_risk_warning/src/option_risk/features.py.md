---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/features.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/features.py>)

SHA-256：`1fd5e57a9449d28e6c2b0668aaf2e1a0b3b00450ac7794e667536c690a6d344b`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import PipelineConfig


FEATURE_SCHEMA_VERSION = "risk-features-v2-12-pressure-signals"
# Ratios above this level all convey the same operational message (extreme
# deterioration).  Saturation prevents sparse zero-baseline signals from
# dominating diagnostics or destabilising the optional ML comparator.
PRESSURE_RATIO_CAP = 25.0
RISK_SIGNALS = (
    "atm_iv",
    "atm_iv_chg_4",
    "term_inversion",
    "convexity_violation_ratio",
    "max_local_iv_jump",
    "put_call_parity_p95_error",
    "calendar_variance_violation_ratio",
    "gamma_hhi",
    "vega_hhi",
    "zero_volume_share",
    "iv_floor_share",
    "coverage_shortfall",
)


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / denominator.replace(0, np.nan)


def _term_features(atm_by_term: pd.DataFrame) -> pd.DataFrame:
    if atm_by_term.empty:
        return pd.DataFrame(
            columns=["term_slope", "near_far_spread", "term_inversion"],
            index=pd.DatetimeIndex([], name="datetime"),
        )
    rows: list[dict[str, float | pd.Timestamp]] = []
    for timestamp, group in atm_by_term.groupby("datetime", sort=True):
        group = group.dropna().sort_values("dte")
        if len(group) < 2:
            rows.append(
                {
                    "datetime": timestamp,
                    "term_slope": np.nan,
                    "near_far_spread": np.nan,
                    "term_inversion": np.nan,
                }
            )
            continue
        x = group["dte"].to_numpy(dtype=float) / 365.0
        y = group["atm_term_iv"].to_numpy(dtype=float)
        slope = float(np.polyfit(x, y, 1)[0]) if np.ptp(x) > 0 else np.nan
        spread = float(y[0] - y[-1])
        rows.append(
            {
                "datetime": timestamp,
                "term_slope": slope,
                "near_far_spread": spread,
                "term_inversion": max(spread, 0.0),
            }
        )
    return pd.DataFrame(rows).set_index("datetime")


def _geometry_features(cleaned: pd.DataFrame) -> pd.DataFrame:
    quotes = cleaned.sort_values(
        ["datetime", "underlying", "option_type", "strike", "contract"]
    ).copy()
    group_keys = ["datetime", "underlying", "option_type"]
    grouped = quotes.groupby(group_keys, observed=True, sort=False)
    quotes["strike_step"] = grouped["strike"].diff()
    quotes["price_step"] = grouped["close"].diff()
    quotes["slope"] = quotes["price_step"] / quotes["strike_step"].replace(0, np.nan)
    quotes["slope_change"] = grouped["slope"].diff()

    call_violation = quotes["option_type"].eq("call") & quotes["price_step"].gt(1e-8)
    put_violation = quotes["option_type"].eq("put") & quotes["price_step"].lt(-1e-8)
    quotes["monotonic_violation"] = call_violation | put_violation
    quotes["monotonic_comparable"] = quotes["price_step"].notna()
    quotes["convexity_violation"] = quotes["slope_change"].lt(-1e-10)
    quotes["convexity_comparable"] = quotes["slope_change"].notna()

    by_time = quotes.groupby("datetime", observed=True)
    result = pd.DataFrame(index=by_time.size().index)
    result["monotonic_violation_ratio"] = _safe_divide(
        by_time["monotonic_violation"].sum(), by_time["monotonic_comparable"].sum()
    )
    result["convexity_violation_ratio"] = _safe_divide(
        by_time["convexity_violation"].sum(), by_time["convexity_comparable"].sum()
    )
    result["max_convexity_violation"] = (
        (-quotes["slope_change"].clip(upper=0)).groupby(quotes["datetime"]).max()
    )
    return result


def _put_call_parity_features(cleaned: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    paired = cleaned.pivot_table(
        index=["datetime", "underlying", "dte", "strike"],
        columns="option_type",
        values="close",
        aggfunc="median",
    ).reset_index()
    if "call" not in paired or "put" not in paired:
        return pd.DataFrame(index=cleaned["datetime"].drop_duplicates().sort_values())
    forward = (
        cleaned.groupby(["datetime", "underlying", "dte"], observed=True)["underlying_price"]
        .median()
        .rename("forward")
        .reset_index()
    )
    paired = paired.merge(forward, on=["datetime", "underlying", "dte"], how="left")
    discount = np.exp(-config.risk_free_rate * paired["dte"] / 365.0)
    theoretical = discount * (paired["forward"] - paired["strike"])
    paired["parity_abs_error"] = (
        (paired["call"] - paired["put"] - theoretical).abs()
        / paired["forward"].replace(0, np.nan)
    )
    return paired.groupby("datetime", observed=True).agg(
        put_call_parity_pair_count=("parity_abs_error", "count"),
        put_call_parity_median_error=("parity_abs_error", "median"),
        put_call_parity_p95_error=("parity_abs_error", lambda x: x.quantile(0.95)),
        put_call_parity_max_error=("parity_abs_error", "max"),
    )


def _calendar_variance_features(nodes: pd.DataFrame) -> pd.DataFrame:
    ordered = nodes.copy()
    ordered["moneyness_bucket"] = ordered["log_moneyness"].round(2)
    ordered["total_variance"] = ordered["iv"].pow(2) * ordered["time_to_expiry"]
    ordered = ordered.sort_values(["datetime", "moneyness_bucket", "dte"])
    groups = ordered.groupby(["datetime", "moneyness_bucket"], observed=True)
    ordered["calendar_variance_change"] = groups["total_variance"].diff()
    ordered["calendar_variance_comparable"] = ordered["calendar_variance_change"].notna()
    ordered["calendar_variance_violation"] = ordered["calendar_variance_change"].lt(-1e-10)
    ordered["calendar_variance_violation_size"] = (
        -ordered["calendar_variance_change"].clip(upper=0)
    )
    by_time = ordered.groupby("datetime", observed=True)
    result = pd.DataFrame(index=by_time.size().index)
    result["calendar_variance_violation_ratio"] = _safe_divide(
        by_time["calendar_variance_violation"].sum(),
        by_time["calendar_variance_comparable"].sum(),
    )
    result["max_calendar_variance_violation"] = by_time[
        "calendar_variance_violation_size"
    ].max()
    return result


def _surface_roughness(nodes: pd.DataFrame) -> pd.DataFrame:
    ordered = nodes.sort_values(["datetime", "dte", "log_moneyness"]).copy()
    keys = ["datetime", "dte"]
    groups = ordered.groupby(keys, observed=True)["iv"]
    ordered["iv_jump"] = groups.diff().abs()
    ordered["iv_second_diff"] = groups.diff().groupby(
        [ordered["datetime"], ordered["dte"]], observed=True
    ).diff().abs()
    return ordered.groupby("datetime", observed=True).agg(
        max_local_iv_jump=("iv_jump", "max"),
        surface_roughness=("iv_second_diff", "median"),
    )


def _hhi(weight: pd.Series, timestamp: pd.Series) -> pd.Series:
    total = weight.groupby(timestamp).sum()
    squared = weight.pow(2).groupby(timestamp).sum()
    return squared / total.pow(2).replace(0, np.nan)


def extract_risk_features(
    cleaned: pd.DataFrame, nodes: pd.DataFrame, config: PipelineConfig
) -> pd.DataFrame:
    """Create interpretable geometry, term, Greek, liquidity, and quality features."""

    grouped = cleaned.groupby("datetime", observed=True)
    features = pd.DataFrame(index=grouped.size().index)
    features["n_quotes"] = grouped.size()
    features["n_contracts"] = grouped["contract"].nunique()
    features["n_expiries"] = grouped["dte"].nunique()
    features["iv_median"] = grouped["iv"].median()
    features["iv_p90"] = grouped["iv"].quantile(0.90)
    features["total_volume"] = grouped["volume"].sum()
    features["total_open_interest"] = grouped["open_interest"].sum()
    features["zero_volume_share"] = grouped["volume"].apply(lambda x: float(x.eq(0).mean()))
    features["iv_floor_share"] = grouped["iv_at_solver_floor"].mean()

    atm = cleaned.loc[cleaned["log_moneyness"].abs().le(config.atm_log_band)]
    features["atm_iv"] = atm.groupby("datetime", observed=True)["iv"].median()
    left = cleaned.loc[
        cleaned["log_moneyness"].between(
            -config.wing_log_max, -config.wing_log_min, inclusive="both"
        )
    ]
    right = cleaned.loc[
        cleaned["log_moneyness"].between(
            config.wing_log_min, config.wing_log_max, inclusive="both"
        )
    ]
    features["left_wing_iv"] = left.groupby("datetime", observed=True)["iv"].median()
    features["right_wing_iv"] = right.groupby("datetime", observed=True)["iv"].median()
    features["downside_skew"] = features["left_wing_iv"] - features["atm_iv"]
    features["upside_skew"] = features["right_wing_iv"] - features["atm_iv"]
    features["skew_asymmetry"] = features["left_wing_iv"] - features["right_wing_iv"]
    features["smile_curvature"] = (
        0.5 * (features["left_wing_iv"] + features["right_wing_iv"])
        - features["atm_iv"]
    )

    atm_by_term = (
        atm.groupby(["datetime", "dte"], observed=True)["iv"]
        .median()
        .rename("atm_term_iv")
        .reset_index()
    )
    features = features.join(_term_features(atm_by_term), how="left")
    features = features.join(_geometry_features(cleaned), how="left")
    features = features.join(_put_call_parity_features(cleaned, config), how="left")
    features = features.join(_surface_roughness(nodes), how="left")
    features = features.join(_calendar_variance_features(nodes), how="left")

    gamma_weight = cleaned["gamma"].abs() * cleaned["open_interest"].clip(lower=0)
    vega_weight = cleaned["vega"].abs() * cleaned["open_interest"].clip(lower=0)
    features["gamma_hhi"] = _hhi(gamma_weight, cleaned["datetime"])
    features["vega_hhi"] = _hhi(vega_weight, cleaned["datetime"])
    features["gamma_near_share"] = _safe_divide(
        gamma_weight.where(cleaned["dte"].le(30), 0).groupby(cleaned["datetime"]).sum(),
        gamma_weight.groupby(cleaned["datetime"]).sum(),
    )
    features["gamma_atm_share"] = _safe_divide(
        gamma_weight.where(cleaned["log_moneyness"].abs().le(0.05), 0)
        .groupby(cleaned["datetime"])
        .sum(),
        gamma_weight.groupby(cleaned["datetime"]).sum(),
    )

    reference = (
        cleaned.groupby(["datetime", "dte"], observed=True)["underlying_price"]
        .median()
        .reset_index()
        .sort_values(["datetime", "dte"])
        .drop_duplicates("datetime", keep="first")
        .set_index("datetime")
    )
    features["reference_underlying_price"] = reference["underlying_price"]
    features["underlying_return_1"] = features["reference_underlying_price"].pct_change()
    features["surface_coverage"] = (
        features["n_quotes"]
        / (features["n_expiries"].clip(lower=1) * config.expected_quotes_per_expiry)
    ).clip(upper=1.0)
    features["coverage_shortfall"] = 1.0 - features["surface_coverage"]
    features["data_ready"] = (
        features["n_quotes"].ge(config.min_quotes_per_snapshot)
        & features["n_expiries"].ge(config.min_expiries_per_snapshot)
        & features["atm_iv"].notna()
    )
    features["product"] = config.product
    features = features.sort_index()
    return add_temporal_features(features, config)


def add_temporal_features(features: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    result = features.copy()
    change_columns = [
        "atm_iv",
        "skew_asymmetry",
        "smile_curvature",
        "term_inversion",
        "convexity_violation_ratio",
        "max_local_iv_jump",
        "put_call_parity_p95_error",
        "calendar_variance_violation_ratio",
        "gamma_hhi",
        "vega_hhi",
        "zero_volume_share",
        "iv_floor_share",
        "coverage_shortfall",
    ]
    for column in change_columns:
        result[f"{column}_chg_1"] = result[column].diff()
        result[f"{column}_chg_{config.short_change_bars}"] = result[column].diff(
            config.short_change_bars
        )

    risk_signals = [
        f"atm_iv_chg_{config.short_change_bars}" if column == "atm_iv_chg_4" else column
        for column in RISK_SIGNALS
    ]
    pressure_columns: list[str] = []
    for column in risk_signals:
        positive = result[column].clip(lower=0)
        threshold = (
            positive.rolling(
                config.historical_window_bars, min_periods=config.min_history_bars
            )
            .quantile(config.deterioration_quantile)
            .shift(1)
        )
        pressure_name = f"pressure__{column}"
        result[f"history_q95__{column}"] = threshold
        denominator = threshold.clip(lower=1e-12)
        result[pressure_name] = (positive / denominator).clip(
            lower=0.0,
            upper=PRESSURE_RATIO_CAP,
        )
        result.loc[threshold.isna(), pressure_name] = np.nan
        pressure_columns.append(pressure_name)

    result["risk_pressure"] = result[pressure_columns].replace(
        [np.inf, -np.inf], np.nan
    ).max(axis=1)
    # The competition's core event definition is deliberately narrower than the
    # full diagnostic score: ATM IV level OR convexity-violation degree above its
    # own rolling 95% threshold.  Other pressures remain predictors/explanations.
    result["core_risk_pressure"] = result[
        ["pressure__atm_iv", "pressure__convexity_violation_ratio"]
    ].replace([np.inf, -np.inf], np.nan).max(axis=1)
    result["history_ready"] = result[pressure_columns].notna().sum(axis=1).ge(4)
    return result
````

</details>
