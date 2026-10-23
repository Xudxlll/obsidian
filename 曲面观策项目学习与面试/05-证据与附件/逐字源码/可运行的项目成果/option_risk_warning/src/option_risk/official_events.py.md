---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/official_events.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/official_events.py>)

SHA-256：`a30824c6e90a49efa512efd6820e1694799cf67e4d701a44658481c6bc1bd781`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .config import PipelineConfig


PRODUCT_SECTORS = {
    "ag": {"全板块", "贵金属"},
    "au": {"全板块", "贵金属"},
    "cu": {"全板块", "有色（铜）", "有色金属"},
    "al": {"全板块", "有色金属"},
    "sc": {"全板块", "能源，化工", "能源"},
}


def find_official_event_file(data_dir: str | Path) -> Path | None:
    matches = sorted(Path(data_dir).rglob("extreme_event.csv"))
    return matches[0] if matches else None


def load_official_events(path: str | Path) -> pd.DataFrame:
    events = pd.read_csv(path, encoding="gb18030")
    events["start_date"] = pd.to_datetime(events["start_date"], errors="coerce")
    events["end_date"] = pd.to_datetime(events["end_date"], errors="coerce")
    events = events.dropna(subset=["start_date", "end_date"]).copy()
    events["official_event_id"] = np.arange(1, len(events) + 1)
    events.attrs["source_file"] = str(Path(path))
    return events


def evaluate_official_events(
    events: pd.DataFrame,
    alerts: pd.DataFrame,
    config: PipelineConfig,
) -> tuple[dict[str, object], pd.DataFrame]:
    sectors = PRODUCT_SECTORS.get(config.product, {"全板块"})
    applicable = events.loc[events["sectors_affected"].isin(sectors)].copy()
    start = alerts.index.min().normalize()
    end = alerts.index.max().normalize()
    applicable = applicable.loc[
        (applicable["end_date"] >= start) & (applicable["start_date"] <= end)
    ].copy()

    timestamps = pd.DatetimeIndex(alerts.index)
    emitted = alerts["alert_emitted"].fillna(False).astype(bool).to_numpy()
    rows: list[dict[str, object]] = []
    for event in applicable.itertuples(index=False):
        event_mask = (
            (timestamps.normalize() >= pd.Timestamp(event.start_date).normalize())
            & (timestamps.normalize() <= pd.Timestamp(event.end_date).normalize())
        )
        event_positions = np.flatnonzero(event_mask)
        if not len(event_positions):
            continue
        first_position = int(event_positions[0])
        pre_positions = np.arange(max(0, first_position - config.horizon_bars), first_position)
        pre_alert_positions = pre_positions[emitted[pre_positions]]
        in_event_alert_positions = event_positions[emitted[event_positions]]
        pre_position = int(pre_alert_positions[0]) if len(pre_alert_positions) else None
        during_position = (
            int(in_event_alert_positions[0]) if len(in_event_alert_positions) else None
        )
        first_timestamp = timestamps[first_position]
        rows.append(
            {
                "official_event_id": event.official_event_id,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "event_description": event.event_description,
                "sectors_affected": event.sectors_affected,
                "split_at_start": alerts.iloc[first_position]["split"],
                "prewarned_within_8_bars": pre_position is not None,
                "prewarning_time": timestamps[pre_position] if pre_position is not None else pd.NaT,
                "prewarning_lead_bars": first_position - pre_position
                if pre_position is not None
                else np.nan,
                "prewarning_lead_minutes": 15 * (first_position - pre_position)
                if pre_position is not None
                else np.nan,
                "alerted_during_event": during_position is not None,
                "first_alert_during_event": timestamps[during_position]
                if during_position is not None
                else pd.NaT,
                "first_market_bar": first_timestamp,
            }
        )
    detail = pd.DataFrame(rows)
    test = detail.loc[detail["split_at_start"].eq("test")] if len(detail) else detail
    summary = {
        "source_file": str(Path(events.attrs.get("source_file", "extreme_event.csv"))),
        "official_row_count": int(len(events)),
        "note": "Source file contains 17 data rows although the brief describes 18 events.",
        "applicable_overlapping_events": int(len(detail)),
        "prewarned_events": int(detail["prewarned_within_8_bars"].sum()) if len(detail) else 0,
        "alerted_during_events": int(detail["alerted_during_event"].sum()) if len(detail) else 0,
        "test_events": int(len(test)),
        "test_prewarned_events": int(test["prewarned_within_8_bars"].sum()) if len(test) else 0,
        "test_alerted_during_events": int(test["alerted_during_event"].sum()) if len(test) else 0,
    }
    return summary, detail
````

</details>
