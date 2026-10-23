---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/quality.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/quality.py>)

SHA-256：`5cac0b1574499eb9c0b4c3be5d0736de2e8573cf62b28347571dca124d45530b`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import PipelineConfig
from .io import contract_product


CORE_REQUIRED = [
    "datetime",
    "contract",
    "underlying",
    "option_type",
    "strike",
    "close",
    "open_interest",
    "suspend_flag",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "dte",
    "moneyness",
]


def clean_and_profile(
    raw: pd.DataFrame, config: PipelineConfig, ingest_profile: dict[str, object] | None = None
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Apply deterministic quality gates while retaining explicit quality flags."""

    data = raw.copy()
    initial_rows = len(data)
    data["product"] = contract_product(data["contract"])

    duplicate_mask = data.duplicated(["datetime", "contract"], keep="first")
    duplicate_rows = int(duplicate_mask.sum())
    data = data.loc[~duplicate_mask].copy()

    for column in [
        "strike",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "open_interest",
        "settlement_price",
        "pre_close",
        "suspend_flag",
        "iv",
        "delta",
        "gamma",
        "theta",
        "vega",
        "dte",
        "moneyness",
    ]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    missing_core = data[CORE_REQUIRED].isna().any(axis=1)
    wrong_product = ~data["product"].eq(config.product)
    bad_type = ~data["option_type"].astype("string").str.lower().isin(["call", "put"])
    suspended = data["suspend_flag"].ne(0)
    bad_price = (
        data["strike"].le(0)
        | data["close"].lt(0)
        | data["high"].lt(data["low"])
        | data["open"].lt(data["low"])
        | data["open"].gt(data["high"])
        | data["close"].lt(data["low"])
        | data["close"].gt(data["high"])
    )
    bad_iv = ~data["iv"].between(config.iv_min, config.iv_max, inclusive="both")
    bad_greeks = (
        ~data["delta"].between(-1.0001, 1.0001, inclusive="both")
        | data["gamma"].lt(0)
        | data["vega"].lt(0)
    )
    bad_dte = ~data["dte"].between(config.min_dte, config.max_dte, inclusive="both")
    bad_moneyness = ~data["moneyness"].between(
        config.min_moneyness, config.max_moneyness, inclusive="both"
    )

    data["iv_at_solver_floor"] = np.isclose(
        data["iv"], config.iv_solver_floor, atol=config.iv_floor_tolerance, rtol=0
    )
    data["quality_exclusion"] = (
        missing_core
        | wrong_product
        | bad_type
        | suspended
        | bad_price
        | bad_iv
        | bad_greeks
        | bad_dte
        | bad_moneyness
    )

    cleaned = data.loc[~data["quality_exclusion"]].copy()
    cleaned["option_type"] = cleaned["option_type"].astype("string").str.lower()
    cleaned["dte"] = cleaned["dte"].astype("int32")
    cleaned["volume"] = cleaned["volume"].fillna(0).astype("int64")
    cleaned["open_interest"] = cleaned["open_interest"].fillna(0).astype("int64")
    cleaned["log_moneyness"] = np.log(cleaned["moneyness"].clip(lower=1e-9))
    cleaned["time_to_expiry"] = cleaned["dte"] / 365.0
    cleaned["underlying_price"] = cleaned["strike"] / cleaned["moneyness"]
    x = cleaned["log_moneyness"]
    cleaned["surface_eligible"] = (
        x.abs().le(config.atm_log_band)
        | ((x < -config.atm_log_band) & cleaned["option_type"].eq("put"))
        | ((x > config.atm_log_band) & cleaned["option_type"].eq("call"))
    )

    exclusion_counts = {
        "missing_core": int(missing_core.sum()),
        "wrong_product": int(wrong_product.sum()),
        "bad_option_type": int(bad_type.sum()),
        "suspended": int(suspended.sum()),
        "bad_price": int(bad_price.sum()),
        "bad_iv": int(bad_iv.sum()),
        "bad_greeks": int(bad_greeks.sum()),
        "bad_dte": int(bad_dte.sum()),
        "bad_moneyness": int(bad_moneyness.sum()),
    }
    profile = {
        **(ingest_profile or {}),
        "initial_rows_after_product_filter": int(initial_rows),
        "duplicate_primary_key_rows_removed": duplicate_rows,
        "clean_rows": int(len(cleaned)),
        "clean_rate": float(len(cleaned) / initial_rows) if initial_rows else 0.0,
        "iv_solver_floor_rows_in_clean_data": int(cleaned["iv_at_solver_floor"].sum()),
        "iv_solver_floor_rate_in_clean_data": float(cleaned["iv_at_solver_floor"].mean())
        if len(cleaned)
        else 0.0,
        "surface_eligible_rows": int(cleaned["surface_eligible"].sum()),
        "datetime_min": cleaned["datetime"].min().isoformat() if len(cleaned) else None,
        "datetime_max": cleaned["datetime"].max().isoformat() if len(cleaned) else None,
        "distinct_contracts": int(cleaned["contract"].nunique()),
        "distinct_underlyings": int(cleaned["underlying"].nunique()),
        "exclusion_counts_before_overlap": exclusion_counts,
    }
    return cleaned.sort_values(["datetime", "underlying", "strike", "option_type"]), profile

````

</details>
