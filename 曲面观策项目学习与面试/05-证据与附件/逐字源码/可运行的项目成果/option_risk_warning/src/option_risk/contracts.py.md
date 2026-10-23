---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/contracts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/contracts.py>)

SHA-256：`9e7764d505c9af9eae84115d7d1b26916c253d08611f69fa2dff71449d240937`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _json_ready(value: Any) -> Any:
    if value is pd.NA:
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (np.integer, np.floating, np.bool_)):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, np.ndarray):
        return [_json_ready(item) for item in value.tolist()]
    if isinstance(value, pd.DataFrame):
        frame = value.reset_index(names="datetime")
        return [_json_ready(row) for row in frame.to_dict(orient="records")]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


@dataclass(frozen=True, slots=True)
class ProductOption:
    code: str
    label: str
    start: pd.Timestamp | None = None
    end: pd.Timestamp | None = None


@dataclass(frozen=True, slots=True)
class TriggerReason:
    feature_name: str
    label: str
    current_value: float | None
    reference_value: float | None
    pressure_ratio: float | None
    change_direction: str
    severity: int
    message: str


@dataclass(frozen=True, slots=True)
class FeatureEvidence:
    group: str
    feature_name: str
    label: str
    current_value: float | None
    reference_value: float | None
    pressure_ratio: float | None
    change_rate: float | None
    status: str


@dataclass(frozen=True, slots=True)
class SurfacePayload:
    metric: str
    timestamp: pd.Timestamp
    log_moneyness: np.ndarray
    time_to_expiry: np.ndarray
    values: np.ndarray

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SurfacePayload":
        return cls(
            metric=str(payload["metric"]),
            timestamp=pd.Timestamp(payload["timestamp"]),
            log_moneyness=np.asarray(payload["log_moneyness"], dtype=float),
            time_to_expiry=np.asarray(payload["time_to_expiry"], dtype=float),
            values=np.asarray(payload["values"], dtype=float),
        )


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    available: bool
    status: str
    metrics: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvaluationResult":
        return cls(
            available=bool(payload["available"]),
            status=str(payload["status"]),
            metrics=dict(payload.get("metrics") or {}),
        )


@dataclass(frozen=True, slots=True)
class GraphNodeRecord:
    node_id: str
    node_type: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GraphNodeRecord":
        return cls(
            node_id=str(payload["node_id"]),
            node_type=str(payload["node_type"]),
            label=str(payload["label"]),
            properties=dict(payload.get("properties") or {}),
        )


@dataclass(frozen=True, slots=True)
class GraphEdgeRecord:
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation_type: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GraphEdgeRecord":
        return cls(
            edge_id=str(payload["edge_id"]),
            source_node_id=str(payload["source_node_id"]),
            target_node_id=str(payload["target_node_id"]),
            relation_type=str(payload["relation_type"]),
            properties=dict(payload.get("properties") or {}),
        )


@dataclass(frozen=True, slots=True)
class RiskPath:
    path_id: str
    evidence_node_id: str
    anomaly_node_id: str
    mechanism_node_id: str
    conclusion_node_id: str
    edge_ids: tuple[str, ...]
    pressure_ratio: float | None
    severity: str
    relation_semantics: tuple[str, ...]
    rule_ids: tuple[str, ...]
    timestamp: pd.Timestamp

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RiskPath":
        return cls(
            path_id=str(payload["path_id"]),
            evidence_node_id=str(payload["evidence_node_id"]),
            anomaly_node_id=str(payload["anomaly_node_id"]),
            mechanism_node_id=str(payload["mechanism_node_id"]),
            conclusion_node_id=str(payload["conclusion_node_id"]),
            edge_ids=tuple(str(value) for value in payload.get("edge_ids") or ()),
            pressure_ratio=(
                float(payload["pressure_ratio"])
                if payload.get("pressure_ratio") is not None
                else None
            ),
            severity=str(payload["severity"]),
            relation_semantics=tuple(
                str(value) for value in payload.get("relation_semantics") or ()
            ),
            rule_ids=tuple(str(value) for value in payload.get("rule_ids") or ()),
            timestamp=pd.Timestamp(payload["timestamp"]),
        )


@dataclass(frozen=True, slots=True)
class ExplanationSection:
    section_id: str
    title: str
    content: str
    path_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExplanationSection":
        return cls(
            section_id=str(payload["section_id"]),
            title=str(payload["title"]),
            content=str(payload["content"]),
            path_ids=tuple(str(value) for value in payload.get("path_ids") or ()),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeGraphResult:
    status: str
    schema_version: str
    rule_version: str
    product: str
    timestamp: pd.Timestamp
    graph_json: dict[str, Any]
    node_count: int
    edge_count: int
    active_path_count: int
    active_paths: tuple[RiskPath, ...] = ()
    root_evidence: tuple[str, ...] = ()
    possible_consequences: tuple[str, ...] = ()
    explanation_sections: tuple[ExplanationSection, ...] = ()
    explanation_text: str = ""
    explanation_confidence: str = "unavailable"
    missing_evidence: tuple[str, ...] = ()
    query_index: dict[str, Any] = field(default_factory=dict)
    error_type: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _json_ready(asdict(self))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "KnowledgeGraphResult":
        return cls(
            status=str(payload["status"]),
            schema_version=str(payload["schema_version"]),
            rule_version=str(payload["rule_version"]),
            product=str(payload["product"]),
            timestamp=pd.Timestamp(payload["timestamp"]),
            graph_json=dict(payload.get("graph_json") or {}),
            node_count=int(payload["node_count"]),
            edge_count=int(payload["edge_count"]),
            active_path_count=int(payload["active_path_count"]),
            active_paths=tuple(
                RiskPath.from_dict(item) for item in payload.get("active_paths") or ()
            ),
            root_evidence=tuple(str(value) for value in payload.get("root_evidence") or ()),
            possible_consequences=tuple(
                str(value) for value in payload.get("possible_consequences") or ()
            ),
            explanation_sections=tuple(
                ExplanationSection.from_dict(item)
                for item in payload.get("explanation_sections") or ()
            ),
            explanation_text=str(payload.get("explanation_text") or ""),
            explanation_confidence=str(payload.get("explanation_confidence") or "unavailable"),
            missing_evidence=tuple(
                str(value) for value in payload.get("missing_evidence") or ()
            ),
            query_index=dict(payload.get("query_index") or {}),
            error_type=(
                str(payload["error_type"])
                if payload.get("error_type") is not None
                else None
            ),
            error_message=(
                str(payload["error_message"])
                if payload.get("error_message") is not None
                else None
            ),
        )

    @classmethod
    def unavailable(
        cls,
        *,
        product: str,
        timestamp: pd.Timestamp | str,
        error_type: str | None = None,
        error_message: str | None = None,
        schema_version: str = "kg-schema-v1",
        rule_version: str = "kg-rule-v1",
    ) -> "KnowledgeGraphResult":
        return cls(
            status="unavailable",
            schema_version=schema_version,
            rule_version=rule_version,
            product=product,
            timestamp=pd.Timestamp(timestamp),
            graph_json={"nodes": [], "edges": []},
            node_count=0,
            edge_count=0,
            active_path_count=0,
            explanation_text="知识图谱暂不可用。",
            explanation_confidence="unavailable",
            error_type=error_type,
            error_message=error_message,
        )


@dataclass(frozen=True, slots=True)
class AgentResult:
    product: str
    timestamp: pd.Timestamp
    status: str
    alert_level: int
    alert_name: str
    alert_emitted: bool
    risk_score: float | None
    price_source: str
    data_quality: dict[str, Any]
    surfaces: dict[str, SurfacePayload]
    feature_evidence: list[FeatureEvidence]
    trigger_reasons: list[TriggerReason]
    timeline: pd.DataFrame
    evaluation: EvaluationResult | None
    policy_version: str | None = None
    policy_parameter_hash: str | None = None
    transition_reason: str | None = None
    knowledge_graph: KnowledgeGraphResult | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        return _json_ready(payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AgentResult":
        timeline_rows = list(payload.get("timeline") or [])
        timeline = pd.DataFrame(timeline_rows)
        if "datetime" in timeline:
            timeline.index = pd.to_datetime(timeline.pop("datetime"), errors="raise")
        timeline.index.name = "datetime"
        evaluation_payload = payload.get("evaluation")
        knowledge_graph_payload = payload.get("knowledge_graph")
        return cls(
            product=str(payload["product"]),
            timestamp=pd.Timestamp(payload["timestamp"]),
            status=str(payload["status"]),
            alert_level=int(payload["alert_level"]),
            alert_name=str(payload["alert_name"]),
            alert_emitted=bool(payload.get("alert_emitted", False)),
            risk_score=(
                float(payload["risk_score"])
                if payload.get("risk_score") is not None
                else None
            ),
            price_source=str(payload["price_source"]),
            data_quality=dict(payload.get("data_quality") or {}),
            surfaces={
                str(metric): SurfacePayload.from_dict(surface)
                for metric, surface in dict(payload.get("surfaces") or {}).items()
            },
            feature_evidence=[
                FeatureEvidence(**item) for item in list(payload.get("feature_evidence") or [])
            ],
            trigger_reasons=[
                TriggerReason(**item) for item in list(payload.get("trigger_reasons") or [])
            ],
            timeline=timeline,
            evaluation=(
                EvaluationResult.from_dict(evaluation_payload)
                if isinstance(evaluation_payload, dict)
                else None
            ),
            policy_version=(
                str(payload["policy_version"])
                if payload.get("policy_version") is not None
                else None
            ),
            policy_parameter_hash=(
                str(payload["policy_parameter_hash"])
                if payload.get("policy_parameter_hash") is not None
                else None
            ),
            transition_reason=(
                str(payload["transition_reason"])
                if payload.get("transition_reason") is not None
                else None
            ),
            knowledge_graph=(
                KnowledgeGraphResult.from_dict(knowledge_graph_payload)
                if isinstance(knowledge_graph_payload, dict)
                else None
            ),
        )
````

</details>
