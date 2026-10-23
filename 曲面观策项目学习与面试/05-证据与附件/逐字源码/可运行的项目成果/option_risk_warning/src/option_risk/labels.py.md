---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/labels.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/labels.py>)

SHA-256：`86f89fd456fd789b0809ef6c48540ab2e8de400fb425170b963c0bc104796aec`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import PipelineConfig


def build_forward_labels(features: pd.DataFrame, config: PipelineConfig) -> pd.DataFrame:
    """Label warnings only when a new deterioration event starts 30-120 minutes ahead."""

    labels = pd.DataFrame(index=features.index)
    event_pressure = features.get("core_risk_pressure", features["risk_pressure"])
    eligible_breach = (
        event_pressure.ge(1.0)
        & features["data_ready"].fillna(False)
        & features["history_ready"].fillna(False)
    )
    breach_values = eligible_breach.to_numpy(dtype=bool)
    event_start = np.zeros(len(features), dtype=bool)
    last_start = -10_000
    for index, is_breach in enumerate(breach_values):
        previous = breach_values[index - 1] if index else False
        if is_breach and not previous and index - last_start >= config.event_cooldown_bars:
            event_start[index] = True
            last_start = index

    labels["deterioration_breach"] = eligible_breach
    labels["event_start"] = event_start

    future_events = []
    future_pressure = []
    for offset in range(config.lead_bars, config.horizon_bars + 1):
        future_events.append(labels["event_start"].shift(-offset).fillna(False))
        future_pressure.append(event_pressure.shift(-offset))
    labels["label"] = pd.concat(future_events, axis=1).max(axis=1).astype("int8")
    labels["future_severity"] = pd.concat(future_pressure, axis=1).max(axis=1)
    labels["label_available"] = (
        features["history_ready"].fillna(False) & features["data_ready"].fillna(False)
    )
    if len(labels) >= config.horizon_bars:
        labels.iloc[-config.horizon_bars :, labels.columns.get_loc("label_available")] = False
    return labels


def purge_split_boundary_labels(
    labels: pd.DataFrame,
    splits: pd.Series,
    horizon_bars: int,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Invalidate labels whose row-based forward window enters the next split."""

    if horizon_bars < 0:
        raise ValueError("horizon_bars must be non-negative")
    if not labels.index.equals(splits.index):
        raise ValueError("labels and splits must have the same ordered index")
    if "label_available" not in labels:
        raise ValueError("labels must contain label_available")

    split_values = splits.astype("string").to_numpy()
    purge = np.zeros(len(labels), dtype=bool)
    transition_counts = {
        "train_to_validation_rows": 0,
        "validation_to_test_rows": 0,
    }
    transition_names = {
        ("train", "validation"): "train_to_validation_rows",
        ("validation", "test"): "validation_to_test_rows",
    }
    boundaries = np.flatnonzero(split_values[1:] != split_values[:-1]) + 1
    for boundary in boundaries:
        transition = (str(split_values[boundary - 1]), str(split_values[boundary]))
        count_name = transition_names.get(transition)
        if count_name is None:
            continue
        start = max(0, int(boundary) - int(horizon_bars))
        purge[start:boundary] = True
        transition_counts[count_name] += int(boundary - start)

    result = labels.copy()
    available = result["label_available"].fillna(False).astype(bool).to_numpy()
    result["label_available"] = available & ~purge
    diagnostics: dict[str, object] = {
        "policy": "forward_label_window_must_remain_within_split",
        "horizon_bars": int(horizon_bars),
        **transition_counts,
        "total_rows": int(purge.sum()),
    }
    return result, diagnostics


def event_table(labels: pd.DataFrame) -> pd.DataFrame:
    events = labels.loc[labels["event_start"], ["future_severity"]].copy()
    events.index.name = "event_time"
    events["event_id"] = np.arange(1, len(events) + 1)
    return events.reset_index()
````

</details>
