---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py>)

SHA-256：`eaed89807dfdad5e37173210c0efdfae8b0632b55eca1baffeb997ef21e57bfb`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


SURFACE_METRICS = ["iv", "delta", "gamma", "vega", "theta"]


@dataclass(slots=True)
class SurfaceGrid:
    timestamp: pd.Timestamp
    metric: str
    log_moneyness: np.ndarray
    dte: np.ndarray
    values: np.ndarray
    fit_diagnostics: dict[str, object] | None = None


def build_surface_nodes(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Combine OTM quotes (and both ATM sides) into one node per strike and expiry."""

    eligible = cleaned.loc[cleaned["surface_eligible"] & ~cleaned["iv_at_solver_floor"]].copy()
    if eligible.empty:
        raise ValueError("No surface-eligible rows remain after quality filtering")

    nodes = (
        eligible.groupby(["datetime", "product", "underlying", "dte", "strike"], observed=True)
        .agg(
            log_moneyness=("log_moneyness", "median"),
            time_to_expiry=("time_to_expiry", "median"),
            underlying_price=("underlying_price", "median"),
            iv=("iv", "median"),
            delta=("delta", "median"),
            gamma=("gamma", "median"),
            vega=("vega", "median"),
            theta=("theta", "median"),
            volume=("volume", "sum"),
            open_interest=("open_interest", "sum"),
            quote_sides=("option_type", "nunique"),
        )
        .reset_index()
    )
    return nodes.sort_values(["datetime", "dte", "log_moneyness"])


def _total_variance_iv_grid(
    snapshot: pd.DataFrame,
    *,
    timestamp: pd.Timestamp,
) -> SurfaceGrid:
    """Build the formal IV grid with the approved no-arbitrage fallback chain."""

    # Imported lazily because the diagnostic orchestrator also reuses
    # ``build_surface_nodes`` while loading raw data.
    from .surface_fit_diagnostics import diagnose_timestamp
    from .total_variance_fit import FitPolicy, SurfaceGridStatus

    products = snapshot["product"].dropna().astype(str).unique()
    if len(products) != 1:
        raise ValueError("IV surface snapshot must contain exactly one product")

    fit_input = snapshot.loc[
        :,
        [
            "product",
            "datetime",
            "dte",
            "time_to_expiry",
            "strike",
            "iv",
            "log_moneyness",
        ],
    ].copy()
    fit_input["forward_price"] = np.nan
    fit_input["forward_source"] = "underlying_price_proxy"
    diagnostic = diagnose_timestamp(
        fit_input,
        product=str(products[0]),
        timestamp=timestamp,
        policy=FitPolicy(),
    )
    if diagnostic.surface_grid_status is not SurfaceGridStatus.AVAILABLE:
        raise ValueError("Total-variance IV surface has no supported expiry")

    fit_diagnostics: dict[str, object] = {
        "policy_version": diagnostic.policy_version,
        "overall_status": diagnostic.overall_status.value,
        "usable_expiry_count": diagnostic.usable_expiry_count,
        "unusable_expiry_count": diagnostic.unusable_expiry_count,
        "attempts": [
            {
                "attempt_id": attempt.attempt_id,
                "maturity_id": attempt.maturity_id,
                "method": attempt.method.value.lower(),
                "attempt_status": attempt.attempt_status.value,
                "success": attempt.success,
                "raw_node_count": attempt.raw_node_count,
                "node_count": attempt.node_count,
                "rmse_total_variance": attempt.rmse_total_variance,
                "nrmse_total_variance": attempt.nrmse_total_variance,
                "rmse_iv": attempt.rmse_iv,
                "checks": {
                    name: check.status.value
                    for name, check in attempt.checks.items()
                },
                "failure_code": attempt.failure_code,
                "failure_reason": attempt.failure_reason,
            }
            for attempt in diagnostic.attempts
        ],
        "expiries": [
            {
                "maturity_id": result.maturity_id,
                "time_to_expiry": result.time_to_expiry,
                "method": result.method.value.lower(),
                "success": result.success,
                "usable": result.usable,
                "node_count": len(result.raw_k),
                "selected_attempt_id": result.selected_attempt_id,
                "checks": {
                    name: check.status.value
                    for name, check in result.final_checks.items()
                },
                "failure_code": result.failure_code,
                "failure_reason": result.failure_reason,
            }
            for result in diagnostic.expiry_results
        ],
    }

    return SurfaceGrid(
        timestamp=timestamp,
        metric="iv",
        log_moneyness=np.asarray(
            diagnostic.surface_log_moneyness,
            dtype=float,
        ),
        dte=np.asarray(
            [float(result.maturity_id) for result in diagnostic.expiry_results],
            dtype=float,
        ),
        values=np.asarray(
            [
                [np.nan if value is None else float(value) for value in row]
                for row in diagnostic.surface_iv
            ],
            dtype=float,
        ),
        fit_diagnostics=fit_diagnostics,
    )


def surface_grid(
    nodes: pd.DataFrame,
    metric: str,
    timestamp: pd.Timestamp | str | None = None,
    x_min: float = -0.20,
    x_max: float = 0.20,
    x_points: int = 33,
) -> SurfaceGrid:
    """Interpolate each observed expiry only inside its supported moneyness range."""

    if metric not in SURFACE_METRICS:
        raise ValueError(f"Unsupported metric={metric!r}; choose from {SURFACE_METRICS}")
    if timestamp is None:
        timestamp = nodes["datetime"].max()
    timestamp = pd.Timestamp(timestamp)
    snapshot = nodes.loc[nodes["datetime"].eq(timestamp)].copy()
    if snapshot.empty:
        raise ValueError(f"No surface nodes for timestamp={timestamp}")

    if metric == "iv":
        return _total_variance_iv_grid(snapshot, timestamp=timestamp)

    x_grid = np.linspace(x_min, x_max, x_points)
    expiries = np.array(sorted(snapshot["dte"].unique()), dtype=float)
    matrix = np.full((len(expiries), len(x_grid)), np.nan, dtype=float)

    for row_index, dte in enumerate(expiries):
        curve = snapshot.loc[snapshot["dte"].eq(dte), ["log_moneyness", metric]].dropna()
        curve = curve.groupby("log_moneyness", as_index=False)[metric].median().sort_values(
            "log_moneyness"
        )
        if len(curve) < 3:
            continue
        x = curve["log_moneyness"].to_numpy(dtype=float)
        y = curve[metric].to_numpy(dtype=float)
        supported = (x_grid >= x.min()) & (x_grid <= x.max())
        matrix[row_index, supported] = np.interp(x_grid[supported], x, y)

    return SurfaceGrid(
        timestamp=timestamp,
        metric=metric,
        log_moneyness=x_grid,
        dte=expiries,
        values=matrix,
    )


def choose_latest_complete_snapshot(
    nodes: pd.DataFrame, min_expiries: int = 2, min_nodes: int = 20
) -> pd.Timestamp:
    summary = nodes.groupby("datetime", observed=True).agg(
        expiries=("dte", "nunique"), nodes=("iv", "size")
    )
    eligible = summary.loc[(summary["expiries"] >= min_expiries) & (summary["nodes"] >= min_nodes)]
    if eligible.empty:
        raise ValueError("No timestamp has enough expiries and nodes for a surface")
    return pd.Timestamp(eligible.index.max())
````

</details>
