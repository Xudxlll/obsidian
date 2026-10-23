---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/graph_fixtures.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/graph_fixtures.py>)

SHA-256：`a951172bf14cf90b5b076c8abb80e612d305002f97ebe406a5ae40b4c702d7ad`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import networkx as nx
import pandas as pd

from option_risk.contracts import AgentResult, FeatureEvidence, RiskPath
from option_risk.decision import DecisionPolicy, PRESSURE_SPECS
from option_risk.knowledge_graph import build_knowledge_graph


def make_feature_evidence(feature_name: str, pressure: float | None) -> FeatureEvidence:
    pressure_column, spec = next(
        (column, value)
        for column, value in PRESSURE_SPECS.items()
        if value[1] == feature_name
    )
    del pressure_column
    group, _, label = spec
    status = (
        "危险"
        if pressure is not None and pressure >= 1.5
        else "警告"
        if pressure is not None and pressure >= 0.98
        else "关注"
        if pressure is not None and pressure >= 0.9
        else "无预警"
    )
    return FeatureEvidence(
        group=group,
        feature_name=feature_name,
        label=label,
        current_value=0.2,
        reference_value=0.2 / pressure if pressure not in (None, 0) else None,
        pressure_ratio=pressure,
        change_rate=0.01,
        status=status,
    )


def make_agent_result(knowledge_graph=None) -> AgentResult:
    return AgentResult(
        product="ag",
        timestamp=pd.Timestamp("2025-04-07 10:15"),
        status="ready",
        alert_level=0,
        alert_name="无预警",
        alert_emitted=False,
        risk_score=0.5,
        price_source="reconstructed_proxy",
        data_quality={"clean_rate": 1.0},
        surfaces={},
        feature_evidence=[],
        trigger_reasons=[],
        timeline=pd.DataFrame(),
        evaluation=None,
        policy_version="validated-dynamic-state-v2",
        policy_parameter_hash=DecisionPolicy().parameter_hash,
        transition_reason="normal",
        knowledge_graph=knowledge_graph,
    )


def graph_context(*, alert_level: int = 0, alert_name: str = "无预警") -> dict[str, object]:
    return {
        "product": "ag",
        "timestamp": pd.Timestamp("2025-04-07 10:15"),
        "alert_level": alert_level,
        "alert_name": alert_name,
        "risk_score": 0.5,
        "alert_emitted": False,
        "transition_reason": "normal",
        "policy_version": "validated-dynamic-state-v2",
        "policy_parameter_hash": DecisionPolicy().parameter_hash,
        "data_quality": {"clean_rate": 1.0},
        "price_source": "reconstructed_proxy",
    }


def graph_and_paths(
    evidence: list[FeatureEvidence],
    *,
    alert_level: int = 2,
    alert_name: str = "警告",
) -> tuple[nx.MultiDiGraph, list[RiskPath]]:
    from option_risk.graph_reasoner import discover_risk_paths

    graph = build_knowledge_graph(
        **graph_context(alert_level=alert_level, alert_name=alert_name),
        evidence=evidence,
        policy=DecisionPolicy(),
    )
    return graph, discover_risk_paths(graph)
````

</details>
