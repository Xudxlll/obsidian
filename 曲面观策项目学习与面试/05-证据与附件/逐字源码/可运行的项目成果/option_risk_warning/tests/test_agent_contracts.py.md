---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py>)

SHA-256：`3659f846260ac4022ffc9245b3c9152347178ca95a2a5942b76fda2eda82e813`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import numpy as np
import pandas as pd

from option_risk.config import AgentConfig
from option_risk.contracts import (
    AgentResult,
    ExplanationSection,
    GraphEdgeRecord,
    GraphNodeRecord,
    KnowledgeGraphResult,
    RiskPath,
    SurfacePayload,
    TriggerReason,
)
from tests.graph_fixtures import make_agent_result


POLICY_HASH = "df74c842c88bc54a54d0f57a40aa704cfcb7177bcd39297525de45dee69dd5d3"
POLICY_VERSION = "validated-dynamic-state-v2"


def test_agent_result_to_dict_serializes_nested_market_data() -> None:
    surface = SurfacePayload(
        metric="iv",
        timestamp=pd.Timestamp("2025-04-07 10:15"),
        log_moneyness=np.array([-0.1, 0.0, 0.1]),
        time_to_expiry=np.array([20 / 365, 50 / 365]),
        values=np.array([[0.3, 0.2, 0.25], [0.28, np.nan, 0.24]]),
    )
    reason = TriggerReason(
        feature_name="atm_iv",
        label="ATM隐含波动率",
        current_value=0.384,
        reference_value=0.390,
        pressure_ratio=0.984615,
        change_direction="上升",
        severity=2,
        message="ATM隐含波动率接近动态阈值",
    )
    result = AgentResult(
        product="ag",
        timestamp=pd.Timestamp("2025-04-07 10:15"),
        status="ready",
        alert_level=2,
        alert_name="警告",
        alert_emitted=True,
        risk_score=np.float64(0.98),
        price_source="reconstructed_proxy",
        data_quality={"clean_rate": np.float64(0.99)},
        surfaces={"iv": surface},
        feature_evidence=[],
        trigger_reasons=[reason],
        timeline=pd.DataFrame(
            {
                "alert_level": [1, 2],
                "alert_emitted": [False, True],
                "policy_version": [
                    POLICY_VERSION,
                    POLICY_VERSION,
                ],
                "policy_parameter_hash": [POLICY_HASH, POLICY_HASH],
                "transition_reason": ["watch_started", "warning_emitted"],
            },
            index=pd.to_datetime(["2025-04-07 10:00", "2025-04-07 10:15"]),
        ),
        evaluation=None,
        policy_version=POLICY_VERSION,
        policy_parameter_hash=POLICY_HASH,
        transition_reason="warning_emitted",
    )

    payload = result.to_dict()

    assert payload["timestamp"] == "2025-04-07T10:15:00"
    assert payload["risk_score"] == 0.98
    assert payload["data_quality"]["clean_rate"] == 0.99
    assert payload["surfaces"]["iv"]["values"][1][1] is None
    assert payload["trigger_reasons"][0]["label"] == "ATM隐含波动率"
    assert payload["timeline"][1]["datetime"] == "2025-04-07T10:15:00"
    assert payload["alert_emitted"] is True
    assert payload["policy_version"] == POLICY_VERSION
    assert payload["policy_parameter_hash"] == POLICY_HASH
    assert payload["transition_reason"] == "warning_emitted"

    restored = AgentResult.from_dict(payload)

    assert restored.to_dict() == payload


def test_agent_result_from_dict_accepts_legacy_payload_without_policy_identity() -> None:
    payload = {
        "product": "ag",
        "timestamp": "2025-04-07T10:15:00",
        "status": "ready",
        "alert_level": 0,
        "alert_name": "无预警",
        "risk_score": 0.5,
        "price_source": "reconstructed_proxy",
        "data_quality": {},
        "surfaces": {},
        "feature_evidence": [],
        "trigger_reasons": [],
        "timeline": [],
        "evaluation": None,
    }

    restored = AgentResult.from_dict(payload)

    assert restored.policy_version is None
    assert restored.policy_parameter_hash is None
    assert restored.transition_reason is None
    assert restored.alert_emitted is False
    assert restored.knowledge_graph is None


def test_knowledge_graph_result_round_trips_inside_agent_result() -> None:
    """Catches graph records being lost or made non-JSON-safe in agent cache payloads."""
    timestamp = pd.Timestamp("2025-04-07 10:15")
    graph = KnowledgeGraphResult(
        status="ready",
        schema_version="kg-schema-v1",
        rule_version="kg-rule-v1",
        product="ag",
        timestamp=timestamp,
        graph_json={"nodes": [], "edges": []},
        node_count=2,
        edge_count=1,
        active_path_count=1,
        active_paths=(
            RiskPath(
                path_id="path_atm_iv",
                evidence_node_id="evidence_atm_iv",
                anomaly_node_id="anomaly_atm_iv",
                mechanism_node_id="mechanism_atm_iv",
                conclusion_node_id="consequence_atm_iv",
                edge_ids=(
                    "edge_evidence_anomaly",
                    "edge_anomaly_mechanism",
                    "edge_mechanism_consequence",
                ),
                pressure_ratio=1.2,
                severity="warning",
                relation_semantics=("EXCEEDS", "SUPPORTS", "MAY_LEAD_TO"),
                rule_ids=("kg-rule-v1:atm_iv",),
                timestamp=timestamp,
            ),
        ),
        root_evidence=("evidence_atm_iv",),
        possible_consequences=("consequence_atm_iv",),
        explanation_sections=(
            ExplanationSection(
                section_id="summary",
                title="风险概览",
                content="ATM IV异常抬升。",
                path_ids=("path_atm_iv",),
            ),
        ),
        explanation_text="ATM IV异常抬升。",
        explanation_confidence="normal",
        missing_evidence=("term_inversion",),
        query_index={"path_ids": ["path_atm_iv"]},
        error_type=None,
        error_message=None,
    )
    result = make_agent_result(knowledge_graph=graph)

    payload = result.to_dict()

    assert payload["knowledge_graph"]["timestamp"] == "2025-04-07T10:15:00"
    assert payload["knowledge_graph"]["active_paths"][0]["edge_ids"] == [
        "edge_evidence_anomaly",
        "edge_anomaly_mechanism",
        "edge_mechanism_consequence",
    ]
    assert AgentResult.from_dict(payload).to_dict() == payload
    assert payload["knowledge_graph"]["error_type"] is None


def test_knowledge_graph_result_accepts_legacy_error_payload_and_round_trips_type() -> None:
    timestamp = pd.Timestamp("2025-04-07 10:15")
    legacy_payload = KnowledgeGraphResult.unavailable(
        product="ag",
        timestamp=timestamp,
        error_message="legacy graph failure",
    ).to_dict()
    legacy_payload.pop("error_type")

    restored_legacy = KnowledgeGraphResult.from_dict(legacy_payload)
    structured = KnowledgeGraphResult.unavailable(
        product="ag",
        timestamp=timestamp,
        error_type="KnowledgeGraphValidationError",
        error_message="registered topology mismatch",
    )

    assert restored_legacy.error_type is None
    assert restored_legacy.error_message == "legacy graph failure"
    assert structured.to_dict()["error_type"] == "KnowledgeGraphValidationError"
    assert KnowledgeGraphResult.from_dict(structured.to_dict()) == structured


def test_graph_record_contracts_round_trip_json_safe_nested_values() -> None:
    """Catches nested node and edge metadata escaping graph serialization."""
    node = GraphNodeRecord(
        node_id="evidence_atm_iv",
        node_type="Evidence",
        label="ATM隐含波动率",
        properties={
            "observed_at": pd.Timestamp("2025-04-07 10:15"),
            "weights": (0.2, 0.8),
        },
    )
    edge = GraphEdgeRecord(
        edge_id="edge_evidence_anomaly",
        source_node_id="evidence_atm_iv",
        target_node_id="anomaly_atm_iv",
        relation_type="EXCEEDS",
        properties={"pressure": 1.2},
    )

    assert GraphNodeRecord.from_dict(node.to_dict()).to_dict() == {
        "node_id": "evidence_atm_iv",
        "node_type": "Evidence",
        "label": "ATM隐含波动率",
        "properties": {"observed_at": "2025-04-07T10:15:00", "weights": [0.2, 0.8]},
    }
    assert GraphEdgeRecord.from_dict(edge.to_dict()).to_dict() == {
        "edge_id": "edge_evidence_anomaly",
        "source_node_id": "evidence_atm_iv",
        "target_node_id": "anomaly_atm_iv",
        "relation_type": "EXCEEDS",
        "properties": {"pressure": 1.2},
    }


def test_agent_config_resolves_and_creates_runtime_directories(tmp_path) -> None:
    config = AgentConfig(
        data_source=tmp_path / "data",
        cache_dir=tmp_path / "cache",
        output_dir=tmp_path / "outputs",
    )

    config.ensure_directories()

    assert config.data_source == (tmp_path / "data").resolve()
    assert config.cache_dir.is_dir()
    assert config.output_dir.is_dir()
    assert config.pipeline_config("CU").product == "cu"
    assert config.lookback_calendar_days == 45
````

</details>
