---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/knowledge_graph.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_graph.py>)

SHA-256：`d9fc4baa1737fa9c15db6b209f41660604bcb7ce8449b566b35a6f03b6da6d5c`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict
import math
from numbers import Integral, Real
import re
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

from .contracts import FeatureEvidence
from .decision import ALERT_NAMES, DECISION_POLICY_VERSION, DecisionPolicy
from .knowledge_schema import (
    FEATURE_RULES,
    KG_RULE_VERSION,
    KG_SCHEMA_VERSION,
    FeatureRule,
    NodeType,
    RelationType,
)


class KnowledgeGraphError(RuntimeError):
    """Base error raised at the dynamic knowledge-graph boundary."""


class KnowledgeGraphValidationError(KnowledgeGraphError):
    """Raised when graph input or structure violates the registered contract."""


_RULE_BY_FEATURE = {rule.feature_name: rule for rule in FEATURE_RULES}
_QUALITY_GROUP = "质量与流动性"
_CONSTRAINT_FEATURES = {
    "convexity_violation_ratio",
    "calendar_variance_violation_ratio",
}
_SEMANTIC_CLASS = {
    RelationType.HAS_SNAPSHOT.value: "context",
    RelationType.HAS_EVIDENCE.value: "context",
    RelationType.NEAR_THRESHOLD.value: "observed",
    RelationType.EXCEEDS.value: "observed",
    RelationType.VIOLATES.value: "constraint",
    RelationType.SUPPORTS.value: "support",
    RelationType.MAY_AMPLIFY.value: "possible",
    RelationType.MAY_LEAD_TO.value: "possible",
    RelationType.REDUCES_CONFIDENCE.value: "confidence",
}
_WORDING_TEMPLATE = {
    RelationType.HAS_SNAPSHOT.value: "{source}包含当前风险快照{target}",
    RelationType.HAS_EVIDENCE.value: "{source}记录特征证据{target}",
    RelationType.NEAR_THRESHOLD.value: "{source}已接近动态阈值并支持识别{target}",
    RelationType.EXCEEDS.value: "{source}已达到或超过动态阈值并支持识别{target}",
    RelationType.VIOLATES.value: "{source}显示约束违反并支持识别{target}",
    RelationType.SUPPORTS.value: "{source}为{target}提供当前证据支持",
    RelationType.MAY_AMPLIFY.value: "{source}可能放大{target}",
    RelationType.MAY_LEAD_TO.value: "{source}可能带来{target}",
    RelationType.REDUCES_CONFIDENCE.value: "{source}降低{target}",
}
_COMMON_NODE_FIELDS = {
    "node_id",
    "node_type",
    "label",
    "product",
    "source_timestamp",
}
_TYPE_NODE_FIELDS = {
    NodeType.PRODUCT.value: {"product_code", "product_label"},
    NodeType.RISK_SNAPSHOT.value: {
        "timestamp",
        "data_quality",
        "price_source",
        "policy_version",
    },
    NodeType.EVIDENCE.value: {
        "feature_name",
        "group",
        "current_value",
        "reference_value",
        "pressure_ratio",
        "change_rate",
        "direction",
        "status",
        "source",
        "severity",
        "rule_id",
    },
    NodeType.ANOMALY.value: {"anomaly_code", "category", "feature_name", "rule_id"},
    NodeType.MECHANISM.value: {
        "mechanism_code",
        "scope",
        "wording_boundary",
        "feature_name",
        "rule_id",
    },
    NodeType.RISK_CONSEQUENCE.value: {
        "consequence_code",
        "non_directional",
        "feature_name",
        "rule_id",
    },
    NodeType.WARNING_STATE.value: {
        "alert_level",
        "alert_name",
        "risk_score",
        "alert_emitted",
        "transition_reason",
        "policy_hash",
    },
    NodeType.CONFIDENCE_STATE.value: {"level", "quality_reasons"},
}
_EDGE_FIELDS = {
    "edge_id",
    "relation_type",
    "rule_id",
    "rule_version",
    "semantic_class",
    "source_timestamp",
    "wording_template",
}
_POLICY_FLOAT_FIELDS = {
    "attention_pressure",
    "attention_release_pressure",
    "warning_pressure",
    "warning_upper_pressure",
    "danger_pressure",
    "danger_core_pressure",
}
_POLICY_INT_FIELDS = {
    "multi_signal_count",
    "cooldown_bars",
    "persistence_bars",
    "max_watch_bars",
}
_POLICY_FIELDS = _POLICY_FLOAT_FIELDS | _POLICY_INT_FIELDS | {"policy_version"}
_FORBIDDEN_WEIGHT_KEYS = {
    "causal_probability",
    "confidence_weight",
    "causal_confidence",
    "causal_weight",
    "probability_weight",
}
_FORBIDDEN_WEIGHT_COMPACT_KEYS = {
    re.sub(r"[^a-z0-9]+", "", key.lower()) for key in _FORBIDDEN_WEIGHT_KEYS
}
_NODE_LINK_TOP_LEVEL_KEYS = {"directed", "multigraph", "graph", "nodes", "edges"}
def _safe_code(value: object) -> str:
    code = re.sub(r"[^a-z0-9_]+", "", str(value).strip().lower()).strip("_")
    if not code or re.fullmatch(r"[a-z0-9][a-z0-9_]*", code) is None:
        raise KnowledgeGraphValidationError(f"Unsafe or empty graph code: {value!r}")
    return code


def _as_timestamp(value: object, *, field: str) -> pd.Timestamp:
    try:
        timestamp = pd.Timestamp(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise KnowledgeGraphValidationError(f"Invalid {field}: {value!r}") from error
    if pd.isna(timestamp):
        raise KnowledgeGraphValidationError(f"Invalid {field}: {value!r}")
    return timestamp


def _strict_in_memory_timestamp(value: object, *, field: str) -> pd.Timestamp:
    if not isinstance(value, pd.Timestamp) or pd.isna(value):
        raise KnowledgeGraphValidationError(f"{field} must be a pd.Timestamp")
    return value


def _is_finite_real(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, (bool, np.bool_)) and math.isfinite(float(value))


def _finite_or_none(value: object) -> float | None:
    return float(value) if _is_finite_real(value) else None


def _direction(change_rate: float | None) -> str:
    if change_rate is None:
        return "不可用"
    if change_rate > 0:
        return "上升"
    if change_rate < 0:
        return "下降"
    return "持平"


def _severity(pressure: float | None, policy: DecisionPolicy) -> int:
    if pressure is None:
        return 0
    if pressure >= policy.danger_core_pressure:
        return 3
    if pressure >= policy.warning_pressure:
        return 2
    if pressure >= policy.attention_pressure:
        return 1
    return 0


def _strict_alert_level(value: object) -> int:
    if type(value) is not int or value not in ALERT_NAMES:
        raise KnowledgeGraphValidationError(
            "alert_level must be a strict integer in the range 0..3"
        )
    return value


def _strict_risk_score(value: object) -> float | None:
    if value is None:
        return None
    if not _is_finite_real(value):
        raise KnowledgeGraphValidationError("risk_score must be finite or null")
    return float(value)


def _strict_bool(value: object, *, field: str) -> bool:
    if type(value) is not bool:
        raise KnowledgeGraphValidationError(f"{field} must be a strict bool")
    return value


def _strict_attention_pressure(value: object) -> float:
    if not _is_finite_real(value):
        raise KnowledgeGraphValidationError("attention_pressure must be finite")
    pressure = float(value)
    if not 0 < pressure <= 1.0:
        raise KnowledgeGraphValidationError("attention_pressure must be in (0, 1]")
    return pressure


def _strict_optional_string(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise KnowledgeGraphValidationError(f"{field} must be a string or null")
    return value


def _rebuild_policy(
    parameters: object,
    parameter_hash: object,
    *,
    require_hash: bool = True,
) -> DecisionPolicy:
    if not isinstance(parameters, Mapping) or set(parameters) != _POLICY_FIELDS:
        raise KnowledgeGraphValidationError(
            "policy_parameters must contain exactly the DecisionPolicy fields"
        )
    normalized: dict[str, Any] = {}
    for field in _POLICY_FLOAT_FIELDS:
        value = parameters[field]
        if type(value) is not float or not math.isfinite(value):
            raise KnowledgeGraphValidationError(
                f"Policy field {field} must be a finite float"
            )
        normalized[field] = value
    for field in _POLICY_INT_FIELDS:
        value = parameters[field]
        if type(value) is not int or value <= 0:
            raise KnowledgeGraphValidationError(
                f"Policy field {field} must be a positive strict integer"
            )
        normalized[field] = value
    policy_version = parameters["policy_version"]
    if policy_version != DECISION_POLICY_VERSION:
        raise KnowledgeGraphValidationError(
            "Policy field policy_version does not match the formal decision version"
        )
    normalized["policy_version"] = policy_version
    policy = DecisionPolicy(**normalized)
    _strict_attention_pressure(policy.attention_pressure)
    if policy.attention_release_pressure > policy.attention_pressure:
        raise KnowledgeGraphValidationError(
            "attention_release_pressure may not exceed attention_pressure"
        )
    if policy.warning_pressure < policy.attention_pressure:
        raise KnowledgeGraphValidationError(
            "warning_pressure may not be below attention_pressure"
        )
    if require_hash and (
        not isinstance(parameter_hash, str) or parameter_hash != policy.parameter_hash
    ):
        raise KnowledgeGraphValidationError("Policy parameter hash mismatch")
    return policy


def _stamp(timestamp: pd.Timestamp) -> str:
    return timestamp.strftime("%Y%m%dT%H%M%S")


def _base_node(
    *, node_id: str, node_type: NodeType, label: str, product: str, timestamp: pd.Timestamp
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "node_type": node_type.value,
        "label": str(label),
        "product": product,
        "source_timestamp": timestamp,
    }


def _edge_id(source: str, target: str, relation: RelationType) -> str:
    return f"edge:{source}:{relation.value.lower()}:{target}"


def _add_edge(
    graph: nx.MultiDiGraph,
    source: str,
    target: str,
    relation: RelationType,
    *,
    rule_id: str,
    timestamp: pd.Timestamp,
) -> None:
    edge_id = _edge_id(source, target, relation)
    graph.add_edge(
        source,
        target,
        key=edge_id,
        edge_id=edge_id,
        relation_type=relation.value,
        rule_id=rule_id,
        rule_version=KG_RULE_VERSION,
        semantic_class=_SEMANTIC_CLASS[relation.value],
        source_timestamp=timestamp,
        wording_template=_WORDING_TEMPLATE[relation.value],
    )


def _active_relation(
    row: FeatureEvidence, rule: FeatureRule, policy: DecisionPolicy
) -> RelationType | None:
    pressure = _finite_or_none(row.pressure_ratio)
    if pressure is None or pressure < policy.attention_pressure:
        return None
    current = _finite_or_none(row.current_value)
    if (
        rule.feature_name in _CONSTRAINT_FEATURES
        and current is not None
        and current > 0
    ):
        return RelationType.VIOLATES
    return RelationType.NEAR_THRESHOLD if pressure < 1.0 else RelationType.EXCEEDS


def build_knowledge_graph(
    *,
    product: str,
    timestamp: pd.Timestamp,
    evidence: Sequence[FeatureEvidence],
    alert_level: int,
    alert_name: str,
    risk_score: float | None,
    alert_emitted: bool,
    transition_reason: str | None,
    policy_version: str | None,
    policy_parameter_hash: str | None,
    data_quality: Mapping[str, Any],
    price_source: str,
    policy: DecisionPolicy,
) -> nx.MultiDiGraph:
    """Build one deterministic event-centred graph from Problem 1 evidence."""
    if not isinstance(policy, DecisionPolicy):
        raise KnowledgeGraphValidationError("policy must be a DecisionPolicy")
    policy = _rebuild_policy(asdict(policy), None, require_hash=False)
    product_code = _safe_code(product)
    event_timestamp = _as_timestamp(timestamp, field="timestamp")
    event_stamp = _stamp(event_timestamp)
    formal_alert_level = _strict_alert_level(alert_level)
    if alert_name != ALERT_NAMES[formal_alert_level]:
        raise KnowledgeGraphValidationError("alert_name does not match alert_level")
    formal_risk_score = _strict_risk_score(risk_score)
    formal_alert_emitted = _strict_bool(alert_emitted, field="alert_emitted")
    attention_pressure = _strict_attention_pressure(policy.attention_pressure)
    if not isinstance(data_quality, Mapping):
        raise KnowledgeGraphValidationError("data_quality must be a mapping")
    if not isinstance(price_source, str) or not price_source:
        raise KnowledgeGraphValidationError("price_source must be a non-empty string")
    _strict_optional_string(policy_version, field="policy_version")
    _strict_optional_string(policy_parameter_hash, field="policy_parameter_hash")
    _strict_optional_string(transition_reason, field="transition_reason")

    rows_by_feature: dict[str, FeatureEvidence] = {}
    for row in evidence:
        feature_name = str(row.feature_name)
        if feature_name not in _RULE_BY_FEATURE:
            raise KnowledgeGraphValidationError(
                f"Unknown canonical evidence feature: {feature_name!r}"
            )
        if feature_name in rows_by_feature:
            raise KnowledgeGraphValidationError(
                f"Duplicate evidence feature: {feature_name!r}"
            )
        rows_by_feature[feature_name] = row

    active_quality_features = [
        rule.feature_name
        for rule in FEATURE_RULES
        if rule.evidence_group == _QUALITY_GROUP
        and rule.feature_name in rows_by_feature
        and _is_finite_real(rows_by_feature[rule.feature_name].current_value)
        and _active_relation(rows_by_feature[rule.feature_name], rule, policy) is not None
    ]
    confidence_level = "limited" if active_quality_features else "normal"

    graph = nx.MultiDiGraph()
    graph.graph.update(
        schema_version=KG_SCHEMA_VERSION,
        rule_version=KG_RULE_VERSION,
        product=product_code,
        timestamp=event_timestamp,
        attention_pressure=attention_pressure,
        policy_parameters=asdict(policy),
        policy_parameter_hash=policy.parameter_hash,
    )

    product_id = f"product:{product_code}"
    snapshot_id = f"snapshot:{product_code}:{event_stamp}"
    warning_id = f"warning:{product_code}:{event_stamp}:{formal_alert_level}"
    confidence_id = f"confidence:{product_code}:{event_stamp}:{confidence_level}"

    graph.add_node(
        product_id,
        **_base_node(
            node_id=product_id,
            node_type=NodeType.PRODUCT,
            label=product_code.upper(),
            product=product_code,
            timestamp=event_timestamp,
        ),
        product_code=product_code,
        product_label=product_code.upper(),
    )
    graph.add_node(
        snapshot_id,
        **_base_node(
            node_id=snapshot_id,
            node_type=NodeType.RISK_SNAPSHOT,
            label=f"{product_code.upper()}风险快照",
            product=product_code,
            timestamp=event_timestamp,
        ),
        timestamp=event_timestamp,
        data_quality=dict(data_quality),
        price_source=str(price_source),
        policy_version=policy_version,
    )
    graph.add_node(
        warning_id,
        **_base_node(
            node_id=warning_id,
            node_type=NodeType.WARNING_STATE,
            label=str(alert_name),
            product=product_code,
            timestamp=event_timestamp,
        ),
        alert_level=formal_alert_level,
        alert_name=str(alert_name),
        risk_score=formal_risk_score,
        alert_emitted=formal_alert_emitted,
        transition_reason=transition_reason,
        policy_hash=policy_parameter_hash,
    )
    graph.add_node(
        confidence_id,
        **_base_node(
            node_id=confidence_id,
            node_type=NodeType.CONFIDENCE_STATE,
            label="解释置信度受限" if active_quality_features else "解释置信度正常",
            product=product_code,
            timestamp=event_timestamp,
        ),
        level=confidence_level,
        quality_reasons=active_quality_features,
    )
    _add_edge(
        graph,
        product_id,
        snapshot_id,
        RelationType.HAS_SNAPSHOT,
        rule_id=f"{KG_RULE_VERSION}:context:has_snapshot",
        timestamp=event_timestamp,
    )

    for rule in FEATURE_RULES:
        row = rows_by_feature.get(rule.feature_name)
        if row is None or not _is_finite_real(row.current_value):
            continue
        current_value = float(row.current_value)
        reference_value = _finite_or_none(row.reference_value)
        pressure_ratio = _finite_or_none(row.pressure_ratio)
        change_rate = _finite_or_none(row.change_rate)
        evidence_id = f"evidence:{product_code}:{event_stamp}:{_safe_code(rule.feature_name)}"
        graph.add_node(
            evidence_id,
            **_base_node(
                node_id=evidence_id,
                node_type=NodeType.EVIDENCE,
            label=rule.label,
                product=product_code,
                timestamp=event_timestamp,
            ),
            feature_name=rule.feature_name,
            group=rule.evidence_group,
            current_value=current_value,
            reference_value=reference_value,
            pressure_ratio=pressure_ratio,
            change_rate=change_rate,
            direction=_direction(change_rate),
            status=ALERT_NAMES[_severity(pressure_ratio, policy)],
            severity=_severity(pressure_ratio, policy),
            source=str(price_source),
            rule_id=rule.rule_id,
        )
        _add_edge(
            graph,
            snapshot_id,
            evidence_id,
            RelationType.HAS_EVIDENCE,
            rule_id=rule.rule_id,
            timestamp=event_timestamp,
        )

        first_relation = _active_relation(row, rule, policy)
        if first_relation is None:
            continue

        anomaly_id = f"anomaly:{_safe_code(rule.anomaly_code)}"
        mechanism_id = f"mechanism:{_safe_code(rule.mechanism_code)}"
        graph.add_node(
            anomaly_id,
            **_base_node(
                node_id=anomaly_id,
                node_type=NodeType.ANOMALY,
                label=rule.anomaly,
                product=product_code,
                timestamp=event_timestamp,
            ),
            anomaly_code=rule.anomaly_code,
            category=rule.evidence_group,
            feature_name=rule.feature_name,
            rule_id=rule.rule_id,
        )
        graph.add_node(
            mechanism_id,
            **_base_node(
                node_id=mechanism_id,
                node_type=NodeType.MECHANISM,
                label=rule.mechanism,
                product=product_code,
                timestamp=event_timestamp,
            ),
            mechanism_code=rule.mechanism_code,
            scope="confidence" if rule.evidence_group == _QUALITY_GROUP else "market",
            wording_boundary=rule.boundary,
            feature_name=rule.feature_name,
            rule_id=rule.rule_id,
        )
        _add_edge(
            graph,
            evidence_id,
            anomaly_id,
            first_relation,
            rule_id=rule.rule_id,
            timestamp=event_timestamp,
        )
        _add_edge(
            graph,
            anomaly_id,
            mechanism_id,
            rule.relation_types[0],
            rule_id=rule.rule_id,
            timestamp=event_timestamp,
        )

        if rule.conclusion_type is NodeType.CONFIDENCE_STATE:
            _add_edge(
                graph,
                mechanism_id,
                confidence_id,
                rule.relation_types[1],
                rule_id=rule.rule_id,
                timestamp=event_timestamp,
            )
            continue

        consequence_id = f"consequence:{_safe_code(rule.conclusion_code)}"
        graph.add_node(
            consequence_id,
            **_base_node(
                node_id=consequence_id,
                node_type=NodeType.RISK_CONSEQUENCE,
                label=rule.conclusion,
                product=product_code,
                timestamp=event_timestamp,
            ),
            consequence_code=rule.conclusion_code,
            non_directional=True,
            feature_name=rule.feature_name,
            rule_id=rule.rule_id,
        )
        _add_edge(
            graph,
            mechanism_id,
            consequence_id,
            rule.relation_types[1],
            rule_id=rule.rule_id,
            timestamp=event_timestamp,
        )
        if formal_alert_level > 0:
            _add_edge(
                graph,
                mechanism_id,
                warning_id,
                RelationType.SUPPORTS,
                rule_id=rule.rule_id,
                timestamp=event_timestamp,
            )

    validate_knowledge_graph(graph)
    return graph


def _require_fields(record: Mapping[str, Any], fields: set[str], *, owner: str) -> None:
    missing = sorted(fields.difference(record))
    if missing:
        raise KnowledgeGraphValidationError(f"{owner} missing required fields: {missing}")


def _require_exact_values(
    record: Mapping[str, Any], expected: Mapping[str, Any], *, owner: str
) -> None:
    for field, expected_value in expected.items():
        if record[field] != expected_value or (
            type(expected_value) in {bool, int}
            and type(record[field]) is not type(expected_value)
        ):
            raise KnowledgeGraphValidationError(f"{owner} {field} drift")


def _ensure_not_future(value: object, snapshot: pd.Timestamp, *, owner: str) -> pd.Timestamp:
    timestamp = _strict_in_memory_timestamp(value, field=f"{owner} timestamp")
    try:
        is_future = timestamp > snapshot
    except TypeError as error:
        raise KnowledgeGraphValidationError(
            f"{owner} timestamp timezone is incompatible with the snapshot"
        ) from error
    if is_future:
        raise KnowledgeGraphValidationError(f"{owner} timestamp is later than the snapshot")
    return timestamp


def _reject_forbidden_attributes(
    value: object,
    *,
    owner: str,
    active_containers: set[int] | None = None,
) -> None:
    active = set() if active_containers is None else active_containers
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise KnowledgeGraphValidationError(f"Cyclic attributes in {owner}")
        active.add(identity)
        try:
            for key, item in value.items():
                normalized = str(key).strip().lower()
                compact = re.sub(r"[^a-z0-9]+", "", normalized)
                if (
                    normalized in _FORBIDDEN_WEIGHT_KEYS
                    or compact in _FORBIDDEN_WEIGHT_COMPACT_KEYS
                    or "causal" in normalized
                    or normalized.endswith(("_weight", "_probability"))
                ):
                    raise KnowledgeGraphValidationError(
                        f"Forbidden causal/confidence weight key {key!r} in {owner}"
                    )
                _reject_forbidden_attributes(
                    item, owner=owner, active_containers=active
                )
        finally:
            active.remove(identity)
    elif isinstance(value, (list, tuple)):
        identity = id(value)
        if identity in active:
            raise KnowledgeGraphValidationError(f"Cyclic attributes in {owner}")
        active.add(identity)
        try:
            for item in value:
                _reject_forbidden_attributes(
                    item, owner=owner, active_containers=active
                )
        finally:
            active.remove(identity)


def validate_knowledge_graph(graph: nx.MultiDiGraph) -> None:
    """Validate a graph's records and topology without trusting the builder."""
    if not isinstance(graph, nx.MultiDiGraph) or not graph.is_directed():
        raise KnowledgeGraphValidationError("Knowledge graph must be a directed MultiDiGraph")
    _reject_forbidden_attributes(graph.graph, owner="graph metadata")
    _require_fields(
        graph.graph,
        {
            "schema_version",
            "rule_version",
            "product",
            "timestamp",
            "attention_pressure",
            "policy_parameters",
            "policy_parameter_hash",
        },
        owner="graph metadata",
    )
    if graph.graph["schema_version"] != KG_SCHEMA_VERSION:
        raise KnowledgeGraphValidationError("Unknown knowledge-graph schema version")
    if graph.graph["rule_version"] != KG_RULE_VERSION:
        raise KnowledgeGraphValidationError("Unknown knowledge-graph rule version")
    product = _safe_code(graph.graph["product"])
    if product != graph.graph["product"]:
        raise KnowledgeGraphValidationError("Graph product is not normalized")
    snapshot = _strict_in_memory_timestamp(
        graph.graph["timestamp"], field="graph timestamp"
    )
    policy = _rebuild_policy(
        graph.graph["policy_parameters"], graph.graph["policy_parameter_hash"]
    )
    attention_pressure = _strict_attention_pressure(graph.graph["attention_pressure"])
    if (
        type(graph.graph["attention_pressure"])
        is not type(policy.attention_pressure)
        or attention_pressure != policy.attention_pressure
    ):
        raise KnowledgeGraphValidationError(
            "attention_pressure does not match policy_parameters"
        )
    event_stamp = _stamp(snapshot)

    nodes_by_type: dict[str, list[str]] = {node_type.value: [] for node_type in NodeType}
    feature_nodes: dict[str, dict[str, str]] = {
        NodeType.EVIDENCE.value: {},
        NodeType.ANOMALY.value: {},
        NodeType.MECHANISM.value: {},
        NodeType.RISK_CONSEQUENCE.value: {},
    }
    for node_id, data in graph.nodes(data=True):
        _reject_forbidden_attributes(data, owner=f"node {node_id!r}")
        _require_fields(data, _COMMON_NODE_FIELDS, owner=f"node {node_id!r}")
        try:
            node_type = NodeType(data["node_type"]).value
        except (TypeError, ValueError) as error:
            raise KnowledgeGraphValidationError(
                f"Unknown node type on {node_id!r}: {data.get('node_type')!r}"
            ) from error
        _require_fields(
            data,
            _TYPE_NODE_FIELDS[node_type],
            owner=f"{node_type} node {node_id!r}",
        )
        if not isinstance(node_id, str) or not node_id:
            raise KnowledgeGraphValidationError("Node IDs must be non-empty strings")
        if data["node_id"] != node_id:
            raise KnowledgeGraphValidationError(f"Node key/ID mismatch on {node_id!r}")
        if not isinstance(data["label"], str) or not data["label"].strip():
            raise KnowledgeGraphValidationError(f"Node {node_id!r} has an empty label")
        if data["product"] != product:
            raise KnowledgeGraphValidationError(f"Node {node_id!r} product mismatch")
        _ensure_not_future(data["source_timestamp"], snapshot, owner=f"node {node_id!r}")
        nodes_by_type[node_type].append(node_id)

        if node_type == NodeType.RISK_SNAPSHOT.value:
            node_timestamp = _strict_in_memory_timestamp(
                data["timestamp"], field="RiskSnapshot timestamp"
            )
            if node_timestamp != snapshot:
                raise KnowledgeGraphValidationError("RiskSnapshot timestamp mismatch")
        elif node_type == NodeType.PRODUCT.value:
            if data["product_code"] != product:
                raise KnowledgeGraphValidationError("Product node code mismatch")
        elif node_type == NodeType.EVIDENCE.value:
            feature_name = data["feature_name"]
            if feature_name not in _RULE_BY_FEATURE:
                raise KnowledgeGraphValidationError("Evidence has an unknown canonical feature")
            if feature_name in feature_nodes[node_type]:
                raise KnowledgeGraphValidationError("Graph has duplicate Evidence features")
            if type(data["current_value"]) is not float or not math.isfinite(
                data["current_value"]
            ):
                raise KnowledgeGraphValidationError(
                    "Evidence current_value must be a finite float"
                )
            for field in ("reference_value", "pressure_ratio", "change_rate"):
                value = data[field]
                if value is not None and (
                    type(value) is not float or not math.isfinite(value)
                ):
                    raise KnowledgeGraphValidationError(
                        f"Evidence {field} must be a finite float or null"
                    )
            feature_nodes[node_type][str(feature_name)] = node_id
        elif node_type in {
            NodeType.ANOMALY.value,
            NodeType.MECHANISM.value,
            NodeType.RISK_CONSEQUENCE.value,
        }:
            feature_name = data["feature_name"]
            if feature_name not in _RULE_BY_FEATURE:
                raise KnowledgeGraphValidationError(
                    f"{node_type} has an unknown canonical feature"
                )
            if feature_name in feature_nodes[node_type]:
                raise KnowledgeGraphValidationError(
                    f"Graph has duplicate {node_type} nodes for {feature_name!r}"
                )
            feature_nodes[node_type][str(feature_name)] = node_id

    for required_type in (
        NodeType.PRODUCT.value,
        NodeType.RISK_SNAPSHOT.value,
        NodeType.WARNING_STATE.value,
        NodeType.CONFIDENCE_STATE.value,
    ):
        if len(nodes_by_type[required_type]) != 1:
            raise KnowledgeGraphValidationError(
                f"Graph must contain exactly one {required_type} node"
            )

    product_node = nodes_by_type[NodeType.PRODUCT.value][0]
    snapshot_node = nodes_by_type[NodeType.RISK_SNAPSHOT.value][0]
    warning_node = nodes_by_type[NodeType.WARNING_STATE.value][0]
    confidence_node = nodes_by_type[NodeType.CONFIDENCE_STATE.value][0]

    expected_product_id = f"product:{product}"
    expected_snapshot_id = f"snapshot:{product}:{event_stamp}"
    product_data = graph.nodes[product_node]
    snapshot_data = graph.nodes[snapshot_node]
    if product_node != expected_product_id:
        raise KnowledgeGraphValidationError("Product node ID is not canonical")
    if snapshot_node != expected_snapshot_id:
        raise KnowledgeGraphValidationError("RiskSnapshot node ID is not canonical")
    if product_data["label"] != product.upper() or product_data["product_label"] != product.upper():
        raise KnowledgeGraphValidationError("Product node label drift")
    if snapshot_data["label"] != f"{product.upper()}风险快照":
        raise KnowledgeGraphValidationError("RiskSnapshot label drift")
    if not isinstance(snapshot_data["data_quality"], Mapping):
        raise KnowledgeGraphValidationError("RiskSnapshot data_quality must be a mapping")
    if not isinstance(snapshot_data["price_source"], str) or not snapshot_data[
        "price_source"
    ]:
        raise KnowledgeGraphValidationError(
            "RiskSnapshot price_source must be a non-empty string"
        )
    snapshot_policy_version = _strict_optional_string(
        snapshot_data["policy_version"], field="RiskSnapshot policy_version"
    )
    if snapshot_policy_version is not None and snapshot_policy_version != policy.policy_version:
        raise KnowledgeGraphValidationError(
            "RiskSnapshot policy_version does not match policy_parameters"
        )

    warning = graph.nodes[warning_node]
    alert_level = _strict_alert_level(warning["alert_level"])
    expected_alert_name = ALERT_NAMES[alert_level]
    if warning["alert_name"] != expected_alert_name or warning["label"] != expected_alert_name:
        raise KnowledgeGraphValidationError("WarningState alert name drift")
    _strict_risk_score(warning["risk_score"])
    _strict_bool(warning["alert_emitted"], field="WarningState alert_emitted")
    _strict_optional_string(
        warning["transition_reason"], field="WarningState transition_reason"
    )
    warning_policy_hash = _strict_optional_string(
        warning["policy_hash"], field="WarningState policy_hash"
    )
    if (
        warning_policy_hash is not None
        and warning_policy_hash != policy.parameter_hash
    ):
        raise KnowledgeGraphValidationError(
            "WarningState policy_hash does not match policy_parameters"
        )
    expected_warning_id = f"warning:{product}:{event_stamp}:{alert_level}"
    if warning_node != expected_warning_id:
        raise KnowledgeGraphValidationError("WarningState node ID is not canonical")

    active_features: list[str] = []
    active_quality_features: list[str] = []
    expected_first_relations: dict[str, RelationType] = {}
    for rule in FEATURE_RULES:
        evidence_node = feature_nodes[NodeType.EVIDENCE.value].get(rule.feature_name)
        if evidence_node is None:
            continue
        evidence_data = graph.nodes[evidence_node]
        expected_evidence_id = f"evidence:{product}:{event_stamp}:{_safe_code(rule.feature_name)}"
        if evidence_node != expected_evidence_id:
            raise KnowledgeGraphValidationError("Evidence node ID is not canonical")
        pressure = _finite_or_none(evidence_data["pressure_ratio"])
        change_rate = _finite_or_none(evidence_data["change_rate"])
        severity = _severity(pressure, policy)
        expected_evidence = {
            "label": rule.label,
            "group": rule.evidence_group,
            "direction": _direction(change_rate),
            "status": ALERT_NAMES[severity],
            "severity": severity,
            "source": snapshot_data["price_source"],
            "rule_id": rule.rule_id,
        }
        _require_exact_values(
            evidence_data,
            expected_evidence,
            owner=f"Evidence {rule.feature_name!r}",
        )
        if pressure is None or pressure < attention_pressure:
            continue
        current = float(evidence_data["current_value"])
        relation = (
            RelationType.VIOLATES
            if rule.feature_name in _CONSTRAINT_FEATURES and current > 0
            else RelationType.NEAR_THRESHOLD
            if pressure < 1.0
            else RelationType.EXCEEDS
        )
        active_features.append(rule.feature_name)
        expected_first_relations[rule.feature_name] = relation
        if rule.evidence_group == _QUALITY_GROUP:
            active_quality_features.append(rule.feature_name)

    expected_active_set = set(active_features)
    for node_type in (NodeType.ANOMALY.value, NodeType.MECHANISM.value):
        if set(feature_nodes[node_type]) != expected_active_set:
            raise KnowledgeGraphValidationError(
                f"Active {node_type} nodes do not match Evidence activation"
            )
    expected_market_features = {
        feature_name
        for feature_name in active_features
        if _RULE_BY_FEATURE[feature_name].evidence_group != _QUALITY_GROUP
    }
    if set(feature_nodes[NodeType.RISK_CONSEQUENCE.value]) != expected_market_features:
        raise KnowledgeGraphValidationError(
            "RiskConsequence nodes do not match active market Evidence"
        )

    for feature_name in active_features:
        rule = _RULE_BY_FEATURE[feature_name]
        anomaly_id = feature_nodes[NodeType.ANOMALY.value][feature_name]
        mechanism_id = feature_nodes[NodeType.MECHANISM.value][feature_name]
        anomaly = graph.nodes[anomaly_id]
        mechanism = graph.nodes[mechanism_id]
        expected_anomaly_id = f"anomaly:{_safe_code(rule.anomaly_code)}"
        expected_mechanism_id = f"mechanism:{_safe_code(rule.mechanism_code)}"
        if anomaly_id != expected_anomaly_id or mechanism_id != expected_mechanism_id:
            raise KnowledgeGraphValidationError("Semantic node ID is not canonical")
        expected_anomaly = {
            "label": rule.anomaly,
            "anomaly_code": rule.anomaly_code,
            "category": rule.evidence_group,
            "feature_name": feature_name,
            "rule_id": rule.rule_id,
        }
        expected_mechanism = {
            "label": rule.mechanism,
            "mechanism_code": rule.mechanism_code,
            "scope": "confidence" if rule.evidence_group == _QUALITY_GROUP else "market",
            "wording_boundary": rule.boundary,
            "feature_name": feature_name,
            "rule_id": rule.rule_id,
        }
        _require_exact_values(anomaly, expected_anomaly, owner="Anomaly")
        _require_exact_values(mechanism, expected_mechanism, owner="Mechanism")
        if rule.evidence_group == _QUALITY_GROUP:
            continue
        consequence_id = feature_nodes[NodeType.RISK_CONSEQUENCE.value][feature_name]
        consequence = graph.nodes[consequence_id]
        expected_consequence_id = f"consequence:{_safe_code(rule.conclusion_code)}"
        if consequence_id != expected_consequence_id:
            raise KnowledgeGraphValidationError("RiskConsequence node ID is not canonical")
        expected_consequence = {
            "label": rule.conclusion,
            "consequence_code": rule.conclusion_code,
            "non_directional": True,
            "feature_name": feature_name,
            "rule_id": rule.rule_id,
        }
        _require_exact_values(
            consequence, expected_consequence, owner="RiskConsequence"
        )

    confidence = graph.nodes[confidence_node]
    confidence_level = "limited" if active_quality_features else "normal"
    expected_confidence_id = f"confidence:{product}:{event_stamp}:{confidence_level}"
    expected_confidence_label = (
        "解释置信度受限" if active_quality_features else "解释置信度正常"
    )
    if confidence_node != expected_confidence_id:
        raise KnowledgeGraphValidationError("ConfidenceState node ID is not canonical")
    if (
        confidence["level"] != confidence_level
        or confidence["quality_reasons"] != active_quality_features
        or confidence["label"] != expected_confidence_label
    ):
        raise KnowledgeGraphValidationError("ConfidenceState derived state drift")

    expected_edges: dict[tuple[str, str, str], tuple[RelationType, str]] = {}

    def expect_edge(
        source: str, target: str, relation: RelationType, rule_id: str
    ) -> None:
        edge_id = _edge_id(source, target, relation)
        expected_edges[(source, target, edge_id)] = (relation, rule_id)

    expect_edge(
        product_node,
        snapshot_node,
        RelationType.HAS_SNAPSHOT,
        f"{KG_RULE_VERSION}:context:has_snapshot",
    )
    for rule in FEATURE_RULES:
        evidence_node = feature_nodes[NodeType.EVIDENCE.value].get(rule.feature_name)
        if evidence_node is None:
            continue
        expect_edge(
            snapshot_node,
            evidence_node,
            RelationType.HAS_EVIDENCE,
            rule.rule_id,
        )
        if rule.feature_name not in expected_first_relations:
            continue
        anomaly_id = feature_nodes[NodeType.ANOMALY.value][rule.feature_name]
        mechanism_id = feature_nodes[NodeType.MECHANISM.value][rule.feature_name]
        expect_edge(
            evidence_node,
            anomaly_id,
            expected_first_relations[rule.feature_name],
            rule.rule_id,
        )
        expect_edge(
            anomaly_id,
            mechanism_id,
            rule.relation_types[0],
            rule.rule_id,
        )
        if rule.evidence_group == _QUALITY_GROUP:
            expect_edge(
                mechanism_id,
                confidence_node,
                rule.relation_types[1],
                rule.rule_id,
            )
        else:
            consequence_id = feature_nodes[NodeType.RISK_CONSEQUENCE.value][
                rule.feature_name
            ]
            expect_edge(
                mechanism_id,
                consequence_id,
                rule.relation_types[1],
                rule.rule_id,
            )
            if alert_level > 0:
                expect_edge(
                    mechanism_id,
                    warning_node,
                    RelationType.SUPPORTS,
                    rule.rule_id,
                )

    seen_edges: set[tuple[str, str, str]] = set()
    for source, target, key, data in graph.edges(keys=True, data=True):
        _reject_forbidden_attributes(data, owner=f"edge {key!r}")
        if source not in graph or target not in graph:
            raise KnowledgeGraphValidationError("Edge endpoint does not exist")
        _require_fields(data, _EDGE_FIELDS, owner=f"edge {key!r}")
        if not isinstance(key, str) or data["edge_id"] != key:
            raise KnowledgeGraphValidationError(f"Edge key/ID mismatch on {key!r}")
        try:
            relation = RelationType(data["relation_type"])
        except (TypeError, ValueError) as error:
            raise KnowledgeGraphValidationError(
                f"Unknown relation type on edge {key!r}"
            ) from error
        identity = (source, target, key)
        expected = expected_edges.get(identity)
        if expected is None:
            raise KnowledgeGraphValidationError(f"Unexpected edge {key!r}")
        expected_relation, expected_rule_id = expected
        if relation is not expected_relation:
            raise KnowledgeGraphValidationError(f"Edge {key!r} relation drift")
        if key != _edge_id(source, target, relation):
            raise KnowledgeGraphValidationError(f"Edge {key!r} ID is not canonical")
        if data["rule_id"] != expected_rule_id:
            raise KnowledgeGraphValidationError(f"Edge {key!r} rule ID mismatch")
        if data["rule_version"] != KG_RULE_VERSION:
            raise KnowledgeGraphValidationError(f"Edge {key!r} rule version mismatch")
        if data["semantic_class"] != _SEMANTIC_CLASS[relation.value]:
            raise KnowledgeGraphValidationError(f"Edge {key!r} semantic class mismatch")
        if data["wording_template"] != _WORDING_TEMPLATE[relation.value]:
            raise KnowledgeGraphValidationError(f"Edge {key!r} wording template drift")
        _ensure_not_future(data["source_timestamp"], snapshot, owner=f"edge {key!r}")
        seen_edges.add(identity)

    if len(seen_edges) != graph.number_of_edges() or seen_edges != set(expected_edges):
        raise KnowledgeGraphValidationError("Graph has missing or duplicate expected edges")


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            raise KnowledgeGraphValidationError("NaT is not JSON-safe")
        return value.isoformat()
    if isinstance(value, Integral):
        return int(value)
    if isinstance(value, Real):
        if not math.isfinite(float(value)):
            raise KnowledgeGraphValidationError(
                "Non-finite numbers are not allowed at the JSON audit boundary"
            )
        return float(value)
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise KnowledgeGraphValidationError(
                    "Mapping keys must be strings at the JSON audit boundary"
                )
            result[key] = _json_safe(item)
        return result
    if isinstance(value, np.ndarray):
        return [_json_safe(item) for item in value.tolist()]
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    raise KnowledgeGraphValidationError(
        f"Unsupported value at JSON audit boundary: {type(value).__name__}"
    )


def graph_to_node_link(graph: nx.MultiDiGraph) -> dict[str, Any]:
    """Return a stable, JSON-safe NetworkX node-link payload."""
    validate_knowledge_graph(graph)
    payload = nx.node_link_data(graph, edges="edges")
    payload["nodes"] = sorted(payload["nodes"], key=lambda row: str(row["id"]))
    payload["edges"] = sorted(
        payload["edges"],
        key=lambda row: (
            str(row["source"]),
            str(row["target"]),
            str(row["relation_type"]),
            str(row["edge_id"]),
        ),
    )
    return _json_safe(payload)


def _validate_raw_json_value(
    value: Any,
    *,
    path: str,
    active_containers: set[int] | None = None,
) -> None:
    active = set() if active_containers is None else active_containers
    if value is None or type(value) in {str, bool, int}:
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise KnowledgeGraphValidationError(
                f"Non-finite number in node-link payload at {path}"
            )
        return
    if isinstance(value, list):
        identity = id(value)
        if identity in active:
            raise KnowledgeGraphValidationError(
                f"Cyclic container in node-link payload at {path}"
            )
        active.add(identity)
        try:
            for index, item in enumerate(value):
                _validate_raw_json_value(
                    item,
                    path=f"{path}[{index}]",
                    active_containers=active,
                )
        finally:
            active.remove(identity)
        return
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise KnowledgeGraphValidationError(
                f"Cyclic container in node-link payload at {path}"
            )
        active.add(identity)
        try:
            for key, item in value.items():
                if not isinstance(key, str):
                    raise KnowledgeGraphValidationError(
                        f"Non-string JSON object key at {path}"
                    )
                _validate_raw_json_value(
                    item,
                    path=f"{path}.{key}",
                    active_containers=active,
                )
        finally:
            active.remove(identity)
        return
    raise KnowledgeGraphValidationError(
        f"Non-JSON value {type(value).__name__} in node-link payload at {path}"
    )


def _require_raw_iso_timestamp(value: object, *, path: str) -> None:
    if not isinstance(value, str):
        raise KnowledgeGraphValidationError(
            f"Node-link timestamp at {path} must be an ISO string"
        )
    try:
        restored = pd.Timestamp(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise KnowledgeGraphValidationError(
            f"Invalid ISO timestamp at {path}"
        ) from error
    if pd.isna(restored) or restored.isoformat() != value:
        raise KnowledgeGraphValidationError(
            f"Timestamp at {path} is not a lossless pd.Timestamp.isoformat value"
        )


def _preflight_node_link(payload: Mapping[str, Any]) -> None:
    try:
        _validate_raw_json_value(payload, path="payload")
    except RecursionError as error:
        raise KnowledgeGraphValidationError(
            "Node-link payload recursion depth is invalid"
        ) from error
    if set(payload) != _NODE_LINK_TOP_LEVEL_KEYS:
        raise KnowledgeGraphValidationError(
            "Node-link payload must contain exactly the approved top-level keys"
        )
    if payload.get("directed") is not True or payload.get("multigraph") is not True:
        raise KnowledgeGraphValidationError(
            "Node-link payload must describe a directed multigraph"
        )
    if not isinstance(payload.get("graph"), Mapping):
        raise KnowledgeGraphValidationError("Node-link graph metadata must be an object")
    _require_raw_iso_timestamp(
        payload["graph"].get("timestamp"), path="payload.graph.timestamp"
    )
    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise KnowledgeGraphValidationError(
            "Node-link payload must contain node and edge arrays"
        )

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, Mapping):
            raise KnowledgeGraphValidationError(
                f"Node-link node {index} must be an object"
            )
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            raise KnowledgeGraphValidationError(
                f"Node-link node {index} has an invalid ID"
            )
        if node_id in node_ids:
            raise KnowledgeGraphValidationError(
                f"Duplicate node-link node ID: {node_id!r}"
            )
        node_ids.add(node_id)
        _require_raw_iso_timestamp(
            node.get("source_timestamp"),
            path=f"payload.nodes[{index}].source_timestamp",
        )
        if node.get("node_type") == NodeType.RISK_SNAPSHOT.value:
            _require_raw_iso_timestamp(
                node.get("timestamp"),
                path=f"payload.nodes[{index}].timestamp",
            )

    edge_identities: set[tuple[str, str, str]] = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, Mapping):
            raise KnowledgeGraphValidationError(
                f"Node-link edge {index} must be an object"
            )
        source = edge.get("source")
        target = edge.get("target")
        key = edge.get("key")
        if not all(isinstance(value, str) and value for value in (source, target, key)):
            raise KnowledgeGraphValidationError(
                f"Node-link edge {index} has invalid source, target, or key"
            )
        if source not in node_ids or target not in node_ids:
            raise KnowledgeGraphValidationError(
                f"Node-link edge {index} references a missing endpoint"
            )
        identity = (source, target, key)
        if identity in edge_identities:
            raise KnowledgeGraphValidationError(
                f"Duplicate node-link multiedge identity: {identity!r}"
            )
        edge_identities.add(identity)
        _require_raw_iso_timestamp(
            edge.get("source_timestamp"),
            path=f"payload.edges[{index}].source_timestamp",
        )


def graph_from_node_link(payload: Mapping[str, Any]) -> nx.MultiDiGraph:
    """Restore and fully validate a graph from the public node-link boundary."""
    if not isinstance(payload, Mapping):
        raise KnowledgeGraphValidationError("Node-link payload must be a mapping")
    _preflight_node_link(payload)
    restored_payload = deepcopy(dict(payload))
    try:
        graph = nx.node_link_graph(
            restored_payload,
            directed=True,
            multigraph=True,
            edges="edges",
        )
    except (KeyError, TypeError, ValueError, nx.NetworkXError) as error:
        raise KnowledgeGraphValidationError("Malformed node-link payload") from error
    if not isinstance(graph, nx.MultiDiGraph):
        raise KnowledgeGraphValidationError("Payload did not restore a MultiDiGraph")
    graph.graph["timestamp"] = _as_timestamp(
        graph.graph.get("timestamp"), field="graph timestamp"
    )
    for node_id, data in graph.nodes(data=True):
        if "source_timestamp" in data:
            data["source_timestamp"] = _as_timestamp(
                data["source_timestamp"], field=f"node {node_id!r} source_timestamp"
            )
        if data.get("node_type") == NodeType.RISK_SNAPSHOT.value and "timestamp" in data:
            data["timestamp"] = _as_timestamp(
                data["timestamp"], field="RiskSnapshot timestamp"
            )
    for _, _, key, data in graph.edges(keys=True, data=True):
        if "source_timestamp" in data:
            data["source_timestamp"] = _as_timestamp(
                data["source_timestamp"], field=f"edge {key!r} source_timestamp"
            )
    validate_knowledge_graph(graph)
    return graph


__all__ = [
    "KnowledgeGraphError",
    "KnowledgeGraphValidationError",
    "build_knowledge_graph",
    "graph_from_node_link",
    "graph_to_node_link",
    "validate_knowledge_graph",
]
````

</details>
