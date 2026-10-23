---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_reasoner.py>)

SHA-256：`0fb10525458152f1f6602428feb5b956a0473dcb2d5acc47d40643de27fd199a`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
import math
from typing import Any

import networkx as nx
import pandas as pd

from .contracts import ExplanationSection, KnowledgeGraphResult, RiskPath
from .knowledge_graph import (
    KnowledgeGraphValidationError,
    graph_from_node_link,
    graph_to_node_link,
    validate_knowledge_graph,
)
from .knowledge_schema import (
    FEATURE_RULES,
    KG_RULE_VERSION,
    KG_SCHEMA_VERSION,
    FeatureRule,
    NodeType,
    RelationType,
)


_SEVERITY_LABELS = {
    0: "normal",
    1: "watch",
    2: "warning",
    3: "danger",
}
_SEVERITY_RANK = {label: rank for rank, label in _SEVERITY_LABELS.items()}
_RULE_BY_ID = {rule.rule_id: rule for rule in FEATURE_RULES}
_FIRST_RELATIONS = {
    RelationType.NEAR_THRESHOLD.value,
    RelationType.EXCEEDS.value,
    RelationType.VIOLATES.value,
}


def _nodes_for_feature(
    graph: nx.MultiDiGraph,
    *,
    node_type: NodeType,
    feature_name: str,
) -> list[str]:
    return [
        str(node_id)
        for node_id, data in graph.nodes(data=True)
        if data.get("node_type") == node_type.value
        and data.get("feature_name") == feature_name
    ]


def _one_feature_node(
    graph: nx.MultiDiGraph,
    *,
    node_type: NodeType,
    feature_name: str,
) -> str | None:
    matches = _nodes_for_feature(
        graph,
        node_type=node_type,
        feature_name=feature_name,
    )
    if len(matches) > 1:
        raise KnowledgeGraphValidationError(
            f"Duplicate {node_type.value} candidate for {feature_name!r}"
        )
    return matches[0] if matches else None


def _state_node(graph: nx.MultiDiGraph, node_type: NodeType) -> str:
    matches = [
        str(node_id)
        for node_id, data in graph.nodes(data=True)
        if data.get("node_type") == node_type.value
    ]
    if len(matches) != 1:
        raise KnowledgeGraphValidationError(
            f"Expected exactly one {node_type.value} node"
        )
    return matches[0]


def _checked_edge(
    graph: nx.MultiDiGraph,
    source: str,
    target: str,
    *,
    allowed_relations: set[str],
    rule: FeatureRule,
    product: str,
    timestamp: pd.Timestamp,
    optional: bool = False,
) -> tuple[str, str] | None:
    matches: list[tuple[str, str]] = []
    for key, data in (graph.get_edge_data(source, target) or {}).items():
        relation = data.get("relation_type")
        if relation not in allowed_relations:
            continue
        if (
            data.get("edge_id") != key
            or data.get("rule_id") != rule.rule_id
            or data.get("rule_version") != KG_RULE_VERSION
            or data.get("source_timestamp") != timestamp
        ):
            raise KnowledgeGraphValidationError(
                f"Path edge provenance mismatch for {rule.feature_name!r}"
            )
        if graph.nodes[source].get("product") != product or graph.nodes[target].get(
            "product"
        ) != product:
            raise KnowledgeGraphValidationError(
                f"Path edge endpoint product mismatch for {rule.feature_name!r}"
            )
        matches.append((str(key), str(relation)))
    if not matches and optional:
        return None
    if len(matches) != 1:
        raise KnowledgeGraphValidationError(
            f"Expected one registered path edge for {rule.feature_name!r}"
        )
    return matches[0]


def _check_node_chain(
    graph: nx.MultiDiGraph,
    node_ids: tuple[str, str, str, str],
    *,
    terminal_type: NodeType,
    rule: FeatureRule,
    product: str,
    timestamp: pd.Timestamp,
) -> None:
    expected_types = (
        NodeType.EVIDENCE.value,
        NodeType.ANOMALY.value,
        NodeType.MECHANISM.value,
        terminal_type.value,
    )
    for node_id, expected_type in zip(node_ids, expected_types, strict=True):
        data = graph.nodes[node_id]
        if data.get("node_type") != expected_type:
            raise KnowledgeGraphValidationError("Path node type mismatch")
        if data.get("product") != product or data.get("source_timestamp") != timestamp:
            raise KnowledgeGraphValidationError("Path node event identity mismatch")
    for node_id in node_ids[:3]:
        data = graph.nodes[node_id]
        if (
            data.get("feature_name") != rule.feature_name
            or data.get("rule_id") != rule.rule_id
        ):
            raise KnowledgeGraphValidationError("Path feature or rule identity mismatch")
    if terminal_type is NodeType.RISK_CONSEQUENCE:
        terminal = graph.nodes[node_ids[-1]]
        if (
            terminal.get("feature_name") != rule.feature_name
            or terminal.get("rule_id") != rule.rule_id
            or terminal.get("consequence_code") != rule.conclusion_code
        ):
            raise KnowledgeGraphValidationError("Risk consequence identity mismatch")


def _terminal_code(
    graph: nx.MultiDiGraph,
    terminal_node_id: str,
    terminal_type: NodeType,
    rule: FeatureRule,
) -> str:
    terminal = graph.nodes[terminal_node_id]
    if terminal_type is NodeType.RISK_CONSEQUENCE:
        return str(terminal["consequence_code"])
    if terminal_type is NodeType.WARNING_STATE:
        return f"warning_{terminal['alert_level']}"
    return rule.conclusion_code


def _make_path(
    graph: nx.MultiDiGraph,
    *,
    rule: FeatureRule,
    evidence_id: str,
    anomaly_id: str,
    mechanism_id: str,
    conclusion_id: str,
    terminal_type: NodeType,
    edge_parts: tuple[tuple[str, str], tuple[str, str], tuple[str, str]],
) -> RiskPath:
    product = str(graph.graph["product"])
    timestamp = graph.graph["timestamp"]
    if not isinstance(timestamp, pd.Timestamp):
        raise KnowledgeGraphValidationError("Graph timestamp must be a pd.Timestamp")
    node_ids = (evidence_id, anomaly_id, mechanism_id, conclusion_id)
    _check_node_chain(
        graph,
        node_ids,
        terminal_type=terminal_type,
        rule=rule,
        product=product,
        timestamp=timestamp,
    )
    evidence = graph.nodes[evidence_id]
    severity_number = evidence.get("severity")
    if type(severity_number) is not int or severity_number not in _SEVERITY_LABELS:
        raise KnowledgeGraphValidationError("Evidence severity is outside 0..3")
    terminal_code = _terminal_code(graph, conclusion_id, terminal_type, rule)
    path_id = ":".join(
        (
            "path",
            product,
            timestamp.strftime("%Y%m%dT%H%M%S"),
            rule.feature_name,
            terminal_type.value.lower(),
            terminal_code,
        )
    )
    return RiskPath(
        path_id=path_id,
        evidence_node_id=evidence_id,
        anomaly_node_id=anomaly_id,
        mechanism_node_id=mechanism_id,
        conclusion_node_id=conclusion_id,
        edge_ids=tuple(edge_id for edge_id, _ in edge_parts),
        pressure_ratio=evidence.get("pressure_ratio"),
        severity=_SEVERITY_LABELS[severity_number],
        relation_semantics=tuple(relation for _, relation in edge_parts),
        rule_ids=(rule.rule_id,),
        timestamp=timestamp,
    )


def discover_risk_paths(
    graph: nx.MultiDiGraph | Mapping[str, Any],
) -> list[RiskPath]:
    """Enumerate only registered Evidence→Anomaly→Mechanism→terminal paths."""
    if isinstance(graph, Mapping):
        graph = graph_from_node_link(graph)
    else:
        validate_knowledge_graph(graph)
    product = str(graph.graph["product"])
    timestamp = graph.graph["timestamp"]
    warning_id = _state_node(graph, NodeType.WARNING_STATE)
    confidence_id = _state_node(graph, NodeType.CONFIDENCE_STATE)
    paths: list[RiskPath] = []

    for rule in FEATURE_RULES:
        evidence_id = _one_feature_node(
            graph,
            node_type=NodeType.EVIDENCE,
            feature_name=rule.feature_name,
        )
        anomaly_id = _one_feature_node(
            graph,
            node_type=NodeType.ANOMALY,
            feature_name=rule.feature_name,
        )
        mechanism_id = _one_feature_node(
            graph,
            node_type=NodeType.MECHANISM,
            feature_name=rule.feature_name,
        )
        if anomaly_id is None and mechanism_id is None:
            continue
        if evidence_id is None or anomaly_id is None or mechanism_id is None:
            raise KnowledgeGraphValidationError("Incomplete registered path layers")

        first = _checked_edge(
            graph,
            evidence_id,
            anomaly_id,
            allowed_relations=_FIRST_RELATIONS,
            rule=rule,
            product=product,
            timestamp=timestamp,
        )
        second = _checked_edge(
            graph,
            anomaly_id,
            mechanism_id,
            allowed_relations={RelationType.SUPPORTS.value},
            rule=rule,
            product=product,
            timestamp=timestamp,
        )
        assert first is not None and second is not None

        if rule.conclusion_type is NodeType.CONFIDENCE_STATE:
            third = _checked_edge(
                graph,
                mechanism_id,
                confidence_id,
                allowed_relations={RelationType.REDUCES_CONFIDENCE.value},
                rule=rule,
                product=product,
                timestamp=timestamp,
            )
            assert third is not None
            paths.append(
                _make_path(
                    graph,
                    rule=rule,
                    evidence_id=evidence_id,
                    anomaly_id=anomaly_id,
                    mechanism_id=mechanism_id,
                    conclusion_id=confidence_id,
                    terminal_type=NodeType.CONFIDENCE_STATE,
                    edge_parts=(first, second, third),
                )
            )
            continue

        consequence_id = _one_feature_node(
            graph,
            node_type=NodeType.RISK_CONSEQUENCE,
            feature_name=rule.feature_name,
        )
        if consequence_id is None:
            raise KnowledgeGraphValidationError("Missing registered market consequence")
        terminal_relation = rule.relation_types[1].value
        third = _checked_edge(
            graph,
            mechanism_id,
            consequence_id,
            allowed_relations={terminal_relation},
            rule=rule,
            product=product,
            timestamp=timestamp,
        )
        assert third is not None
        paths.append(
            _make_path(
                graph,
                rule=rule,
                evidence_id=evidence_id,
                anomaly_id=anomaly_id,
                mechanism_id=mechanism_id,
                conclusion_id=consequence_id,
                terminal_type=NodeType.RISK_CONSEQUENCE,
                edge_parts=(first, second, third),
            )
        )
        warning_edge = _checked_edge(
            graph,
            mechanism_id,
            warning_id,
            allowed_relations={RelationType.SUPPORTS.value},
            rule=rule,
            product=product,
            timestamp=timestamp,
            optional=True,
        )
        if warning_edge is not None:
            paths.append(
                _make_path(
                    graph,
                    rule=rule,
                    evidence_id=evidence_id,
                    anomaly_id=anomaly_id,
                    mechanism_id=mechanism_id,
                    conclusion_id=warning_id,
                    terminal_type=NodeType.WARNING_STATE,
                    edge_parts=(first, second, warning_edge),
                )
            )

    path_ids = [path.path_id for path in paths]
    if len(path_ids) != len(set(path_ids)):
        raise KnowledgeGraphValidationError("Discovered duplicate deterministic path IDs")
    return rank_risk_paths(paths)


def _path_rule(path: RiskPath) -> FeatureRule:
    if len(path.rule_ids) != 1 or path.rule_ids[0] not in _RULE_BY_ID:
        raise KnowledgeGraphValidationError("RiskPath must carry one registered rule ID")
    return _RULE_BY_ID[path.rule_ids[0]]


def _terminal_order(path: RiskPath) -> int:
    if path.conclusion_node_id.startswith("consequence:"):
        return 0
    if path.conclusion_node_id.startswith("warning:"):
        return 1
    if path.conclusion_node_id.startswith("confidence:"):
        return 2
    raise KnowledgeGraphValidationError("RiskPath has an unknown terminal identity")


def rank_risk_paths(paths: Sequence[RiskPath]) -> list[RiskPath]:
    """Return a stable total order without mutating caller-owned paths."""
    rows = list(paths)

    def key(path: RiskPath) -> tuple[Any, ...]:
        if not isinstance(path, RiskPath):
            raise KnowledgeGraphValidationError("rank_risk_paths accepts RiskPath values")
        if path.severity not in _SEVERITY_RANK:
            raise KnowledgeGraphValidationError("RiskPath severity is not registered")
        rule = _path_rule(path)
        terminal_order = _terminal_order(path)
        quality = terminal_order == 2
        pressure = path.pressure_ratio
        finite = (
            isinstance(pressure, (int, float))
            and not isinstance(pressure, bool)
            and math.isfinite(float(pressure))
        )
        return (
            1 if quality else 0,
            -_SEVERITY_RANK[path.severity],
            0 if finite else 1,
            -float(pressure) if finite else 0.0,
            rule.order,
            terminal_order,
            path.path_id,
        )

    return sorted(rows, key=key)


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _build_query_index(
    graph: nx.MultiDiGraph,
    paths: Sequence[RiskPath],
) -> dict[str, Any]:
    roots = _unique(path.evidence_node_id for path in paths)
    consequences = _unique(
        path.conclusion_node_id
        for path in paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.RISK_CONSEQUENCE.value
    )
    alert_paths = [
        path.path_id
        for path in paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.WARNING_STATE.value
    ]
    quality_paths = [
        path.path_id
        for path in paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.CONFIDENCE_STATE.value
    ]
    paths_by_anomaly: dict[str, list[str]] = {}
    for path in paths:
        paths_by_anomaly.setdefault(path.anomaly_node_id, []).append(path.path_id)
    return {
        "root_evidence": list(roots),
        "paths_to_alert": alert_paths,
        "possible_consequences": list(consequences),
        "quality_limitations": quality_paths,
        "paths_from_anomaly": paths_by_anomaly,
    }


def build_graph_result(
    graph: nx.MultiDiGraph,
    *,
    missing_evidence,
    explanation_sections=(),
    explanation_text="",
    explanation_confidence="normal",
) -> KnowledgeGraphResult:
    """Assemble one validated, fully ranked serializable graph result."""
    paths = discover_risk_paths(graph)
    path_ids = {path.path_id for path in paths}
    sections = tuple(deepcopy(tuple(explanation_sections)))
    for section in sections:
        if not isinstance(section, ExplanationSection):
            raise KnowledgeGraphValidationError(
                "explanation_sections must contain ExplanationSection values"
            )
        if any(path_id not in path_ids for path_id in section.path_ids):
            raise KnowledgeGraphValidationError(
                "Explanation section references an unknown path ID"
            )
    if isinstance(missing_evidence, (str, bytes)):
        raise KnowledgeGraphValidationError(
            "missing_evidence must be an iterable of strings, not a scalar"
        )
    try:
        missing_rows = tuple(missing_evidence)
    except TypeError as error:
        raise KnowledgeGraphValidationError(
            "missing_evidence must be an iterable of strings"
        ) from error
    if any(not isinstance(value, str) for value in missing_rows):
        raise KnowledgeGraphValidationError("missing_evidence values must be strings")
    missing = tuple(sorted(set(missing_rows)))
    roots = _unique(path.evidence_node_id for path in paths)
    consequences = _unique(
        path.conclusion_node_id
        for path in paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.RISK_CONSEQUENCE.value
    )
    query_index = _build_query_index(graph, paths)
    return KnowledgeGraphResult(
        status="ready",
        schema_version=KG_SCHEMA_VERSION,
        rule_version=KG_RULE_VERSION,
        product=str(graph.graph["product"]),
        timestamp=graph.graph["timestamp"],
        graph_json=graph_to_node_link(graph),
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        active_path_count=len(paths),
        active_paths=tuple(paths),
        root_evidence=roots,
        possible_consequences=consequences,
        explanation_sections=sections,
        explanation_text=str(explanation_text),
        explanation_confidence=str(explanation_confidence),
        missing_evidence=missing,
        query_index=query_index,
    )


__all__ = [
    "build_graph_result",
    "discover_risk_paths",
    "rank_risk_paths",
]
````

</details>
