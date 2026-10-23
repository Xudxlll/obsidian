---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py>)

SHA-256：`2c38295d2b78caa058536672c8aae8b094e264d6c937e2cb1845dcd03ecd1349`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, replace
import json

import networkx as nx
import numpy as np
import pandas as pd
import pytest

from graph_fixtures import graph_context, make_feature_evidence
from option_risk.decision import DECISION_POLICY_VERSION, DecisionPolicy
from option_risk.knowledge_graph import (
    KnowledgeGraphValidationError,
    build_knowledge_graph,
    graph_from_node_link,
    graph_to_node_link,
    validate_knowledge_graph,
)
from option_risk.knowledge_schema import KG_RULE_VERSION, KG_SCHEMA_VERSION


SNAPSHOT = pd.Timestamp("2025-04-07 10:15")
STAMP = "20250407T101500"


def _build(
    evidence=None,
    *,
    alert_level: int = 0,
    alert_name: str = "无预警",
    product: str = "ag",
    policy: DecisionPolicy | None = None,
    **context_overrides,
) -> nx.MultiDiGraph:
    context = graph_context(alert_level=alert_level, alert_name=alert_name)
    context["product"] = product
    context.update(context_overrides)
    return build_knowledge_graph(
        **context,
        evidence=list(evidence or []),
        policy=policy or DecisionPolicy(),
    )


def _nodes_of_type(graph: nx.MultiDiGraph, node_type: str) -> dict[str, dict]:
    return {
        node_id: data
        for node_id, data in graph.nodes(data=True)
        if data["node_type"] == node_type
    }


def _only_node(graph: nx.MultiDiGraph, node_type: str) -> tuple[str, dict]:
    nodes = _nodes_of_type(graph, node_type)
    assert len(nodes) == 1
    return next(iter(nodes.items()))


def _valid_market_graph() -> nx.MultiDiGraph:
    return _build(
        [make_feature_evidence("atm_iv", 1.15)],
        alert_level=1,
        alert_name="关注",
    )


def _node_for_feature(
    graph: nx.MultiDiGraph, node_type: str, feature_name: str
) -> tuple[str, dict]:
    matches = {
        node_id: data
        for node_id, data in graph.nodes(data=True)
        if data["node_type"] == node_type and data.get("feature_name") == feature_name
    }
    assert len(matches) == 1
    return next(iter(matches.items()))


def _edge_attributes(
    *,
    source: str,
    target: str,
    relation_type: str,
    rule_id: str,
    semantic_class: str,
    wording_template: str = "攻击探针非空模板",
) -> tuple[str, dict]:
    edge_id = f"edge:{source}:{relation_type.lower()}:{target}"
    return edge_id, {
        "edge_id": edge_id,
        "relation_type": relation_type,
        "rule_id": rule_id,
        "rule_version": KG_RULE_VERSION,
        "semantic_class": semantic_class,
        "source_timestamp": SNAPSHOT,
        "wording_template": wording_template,
    }


def _remove_edges_between(
    graph: nx.MultiDiGraph, source: str, target: str
) -> None:
    for key in list(graph[source][target]):
        graph.remove_edge(source, target, key)


def test_builder_uses_deterministic_event_ids_and_graph_metadata() -> None:
    """Catches random IDs, unsanitized product codes, or a non-event timestamp."""
    graph = _build(
        [make_feature_evidence("atm_iv", 1.15)],
        alert_level=1,
        alert_name="关注",
        product=" AG 主力! ",
    )

    assert graph.graph == {
        "schema_version": KG_SCHEMA_VERSION,
        "rule_version": KG_RULE_VERSION,
        "product": "ag",
        "timestamp": SNAPSHOT,
        "attention_pressure": 0.90,
        "policy_parameters": asdict(DecisionPolicy()),
        "policy_parameter_hash": DecisionPolicy().parameter_hash,
    }
    assert set(graph.nodes) == {
        "product:ag",
        f"snapshot:ag:{STAMP}",
        f"evidence:ag:{STAMP}:atm_iv",
        "anomaly:anomaly_atm_iv",
        "mechanism:mechanism_atm_iv",
        "consequence:risk_consequence_atm_iv",
        f"warning:ag:{STAMP}:1",
        f"confidence:ag:{STAMP}:normal",
    }
    assert all(node_id == data["node_id"] for node_id, data in graph.nodes(data=True))


def test_builder_keeps_all_finite_evidence_but_only_activates_attention_pressure() -> None:
    """Catches normal evidence being dropped or a below-attention path being fabricated."""
    nonfinite_current = replace(
        make_feature_evidence("term_inversion", 1.2), current_value=np.nan
    )
    graph = _build(
        [
            make_feature_evidence("atm_iv", 0.89),
            make_feature_evidence("gamma_hhi", 0.95),
            nonfinite_current,
        ]
    )

    evidence_nodes = _nodes_of_type(graph, "Evidence")
    assert {data["feature_name"] for data in evidence_nodes.values()} == {
        "atm_iv",
        "gamma_hhi",
    }
    snapshot_id, _ = _only_node(graph, "RiskSnapshot")
    attached = {
        target
        for _, target, data in graph.out_edges(snapshot_id, data=True)
        if data["relation_type"] == "HAS_EVIDENCE"
    }
    assert attached == set(evidence_nodes)

    atm_id = next(
        node_id
        for node_id, data in evidence_nodes.items()
        if data["feature_name"] == "atm_iv"
    )
    gamma_id = next(
        node_id
        for node_id, data in evidence_nodes.items()
        if data["feature_name"] == "gamma_hhi"
    )
    assert list(graph.out_edges(atm_id, keys=True, data=True)) == []
    assert {
        data["relation_type"]
        for _, _, _, data in graph.out_edges(gamma_id, keys=True, data=True)
    } == {"NEAR_THRESHOLD"}


@pytest.mark.parametrize(
    ("feature_name", "pressure", "current_value", "expected_relation"),
    [
        ("atm_iv", 0.90, 0.2, "NEAR_THRESHOLD"),
        ("atm_iv", 0.999999, 0.2, "NEAR_THRESHOLD"),
        ("atm_iv", 1.0, 0.2, "EXCEEDS"),
        ("convexity_violation_ratio", 0.95, 0.2, "VIOLATES"),
        ("calendar_variance_violation_ratio", 1.2, 0.2, "VIOLATES"),
        ("convexity_violation_ratio", 1.2, 0.0, "EXCEEDS"),
    ],
)
def test_builder_selects_the_registered_dynamic_evidence_relation(
    feature_name: str,
    pressure: float,
    current_value: float,
    expected_relation: str,
) -> None:
    """Catches wrong 0.90/1.00 boundaries or false constraint violations."""
    row = replace(
        make_feature_evidence(feature_name, pressure), current_value=current_value
    )
    graph = _build([row])
    evidence_id, _ = _only_node(graph, "Evidence")

    assert [
        data["relation_type"]
        for _, _, data in graph.out_edges(evidence_id, data=True)
    ] == [expected_relation]


def test_nonfinite_pressure_is_retained_as_null_but_never_activates_a_path() -> None:
    """Catches NaN/inf leaking into JSON or activating an explanatory branch."""
    row = replace(
        make_feature_evidence("atm_iv", None),
        reference_value=np.inf,
        pressure_ratio=np.nan,
        change_rate=-np.inf,
    )
    graph = _build([row])
    evidence_id, node = _only_node(graph, "Evidence")

    assert node["reference_value"] is None
    assert node["pressure_ratio"] is None
    assert node["change_rate"] is None
    assert node["direction"] == "不可用"
    assert list(graph.out_edges(evidence_id)) == []


@pytest.mark.parametrize(
    ("change_rate", "expected"),
    [(0.1, "上升"), (-0.1, "下降"), (0.0, "持平"), (None, "不可用"), (np.nan, "不可用")],
)
def test_evidence_direction_comes_only_from_change_rate(
    change_rate: float | None, expected: str
) -> None:
    """Catches direction inferred from a fabricated previous raw value."""
    row = replace(make_feature_evidence("atm_iv", 0.5), change_rate=change_rate)
    graph = _build([row])
    _, evidence_node = _only_node(graph, "Evidence")

    assert evidence_node["direction"] == expected


def test_market_path_has_exact_layers_and_only_supports_a_positive_warning() -> None:
    """Catches a missing propagation layer or support for a formal level zero."""
    raised = _valid_market_graph()
    node_types = [data["node_type"] for _, data in raised.nodes(data=True)]
    assert node_types.count("Evidence") == 1
    assert node_types.count("Anomaly") == 1
    assert node_types.count("Mechanism") == 1
    assert node_types.count("RiskConsequence") == 1
    mechanism_id, _ = _only_node(raised, "Mechanism")
    assert {
        raised.nodes[target]["node_type"]: data["relation_type"]
        for _, target, data in raised.out_edges(mechanism_id, data=True)
    } == {"RiskConsequence": "MAY_LEAD_TO", "WarningState": "SUPPORTS"}

    level_zero = _build([make_feature_evidence("atm_iv", 1.15)])
    mechanism_id, _ = _only_node(level_zero, "Mechanism")
    assert {
        level_zero.nodes[target]["node_type"]
        for _, target in level_zero.out_edges(mechanism_id)
    } == {"RiskConsequence"}


def test_quality_paths_end_only_at_one_limited_confidence_state() -> None:
    """Catches quality evidence being used to justify a market warning."""
    graph = _build(
        [
            make_feature_evidence("coverage_shortfall", 1.4),
            make_feature_evidence("zero_volume_share", 0.95),
        ],
        alert_level=1,
        alert_name="关注",
    )
    confidence_id, confidence = _only_node(graph, "ConfidenceState")
    warning_id, _ = _only_node(graph, "WarningState")

    assert confidence_id == f"confidence:ag:{STAMP}:limited"
    assert confidence["level"] == "limited"
    assert confidence["quality_reasons"] == [
        "zero_volume_share",
        "coverage_shortfall",
    ]
    quality_evidence = _nodes_of_type(graph, "Evidence")
    for evidence_id in quality_evidence:
        descendants = nx.descendants(graph, evidence_id)
        assert confidence_id in descendants
        assert warning_id not in descendants
        assert {
            graph.nodes[node_id]["node_type"] for node_id in descendants
        } <= {"Anomaly", "Mechanism", "ConfidenceState"}


def test_builder_rejects_unknown_duplicate_features_and_empty_safe_product() -> None:
    """Catches ambiguous evidence identity and unsafe product IDs."""
    unknown = replace(make_feature_evidence("atm_iv", 1.0), feature_name="not_canonical")
    with pytest.raises(KnowledgeGraphValidationError):
        _build([unknown])

    duplicate = make_feature_evidence("atm_iv", 1.0)
    with pytest.raises(KnowledgeGraphValidationError):
        _build([duplicate, duplicate])

    with pytest.raises(KnowledgeGraphValidationError):
        _build([], product="主力合约")


def test_every_node_and_edge_carries_the_required_audit_contract() -> None:
    """Catches a graph that cannot be inspected without consulting runtime state."""
    graph = _valid_market_graph()
    common_node_fields = {"node_id", "node_type", "label", "product", "source_timestamp"}
    type_fields = {
        "Product": {"product_code", "product_label"},
        "RiskSnapshot": {"timestamp", "data_quality", "price_source", "policy_version"},
        "Evidence": {
            "feature_name",
            "group",
            "current_value",
            "reference_value",
            "pressure_ratio",
            "change_rate",
            "direction",
            "status",
            "source",
        },
        "Anomaly": {"anomaly_code", "category"},
        "Mechanism": {"mechanism_code", "scope", "wording_boundary"},
        "RiskConsequence": {"consequence_code", "non_directional"},
        "WarningState": {
            "alert_level",
            "alert_name",
            "risk_score",
            "alert_emitted",
            "transition_reason",
            "policy_hash",
        },
        "ConfidenceState": {"level", "quality_reasons"},
    }
    for _, data in graph.nodes(data=True):
        assert common_node_fields | type_fields[data["node_type"]] <= set(data)
        assert data["product"] == "ag"
        assert data["source_timestamp"] == SNAPSHOT

    required_edge_fields = {
        "edge_id",
        "relation_type",
        "rule_id",
        "rule_version",
        "semantic_class",
        "source_timestamp",
        "wording_template",
    }
    for _, _, key, data in graph.edges(keys=True, data=True):
        assert required_edge_fields <= set(data)
        assert key == data["edge_id"]
        assert data["rule_id"].startswith(f"{KG_RULE_VERSION}:")
        assert data["rule_version"] == KG_RULE_VERSION
        assert data["semantic_class"] in {
            "context",
            "observed",
            "constraint",
            "support",
            "possible",
            "confidence",
        }
        assert data["wording_template"].strip()

    validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("node_type", "field"),
    [
        ("Product", "product_code"),
        ("RiskSnapshot", "timestamp"),
        ("Evidence", "feature_name"),
        ("Anomaly", "anomaly_code"),
        ("Mechanism", "mechanism_code"),
        ("RiskConsequence", "consequence_code"),
        ("WarningState", "alert_level"),
        ("ConfidenceState", "level"),
    ],
)
def test_validator_rejects_a_missing_type_specific_node_attribute(
    node_type: str, field: str
) -> None:
    """Catches validation that checks node type names but not their payloads."""
    graph = _valid_market_graph()
    node_id, _ = _only_node(graph, node_type)
    del graph.nodes[node_id][field]

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_unknown_node_and_relation_types() -> None:
    """Catches permissive schema drift in graph records."""
    graph = _valid_market_graph()
    evidence_id, _ = _only_node(graph, "Evidence")
    graph.nodes[evidence_id]["node_type"] = "UnknownNode"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    graph[source][target][key]["relation_type"] = "UNKNOWN_RELATION"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    "field",
    [
        "edge_id",
        "rule_id",
        "rule_version",
        "semantic_class",
        "source_timestamp",
        "wording_template",
    ],
)
def test_validator_rejects_a_missing_edge_audit_attribute(field: str) -> None:
    """Catches partially sourced edges crossing the public audit boundary."""
    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    del graph[source][target][key][field]

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_bad_edge_identity_semantics_and_rule_version() -> None:
    """Catches edge-key drift, invented semantic classes, and mixed rule registries."""
    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    graph[source][target][key]["edge_id"] = "edge:different"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    graph[source][target][key]["semantic_class"] = "causal"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    graph[source][target][key]["rule_version"] = "kg-rule-v0"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_future_node_and_edge_timestamps() -> None:
    """Catches future information being attached to the selected event snapshot."""
    future = SNAPSHOT + pd.Timedelta(seconds=1)
    graph = _valid_market_graph()
    evidence_id, _ = _only_node(graph, "Evidence")
    graph.nodes[evidence_id]["source_timestamp"] = future
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    graph[source][target][key]["source_timestamp"] = future
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_graph_product_and_timestamp_mismatches() -> None:
    """Catches a graph envelope describing a different product or event."""
    graph = _valid_market_graph()
    graph.graph["product"] = "au"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    graph.graph["timestamp"] = SNAPSHOT + pd.Timedelta(minutes=1)
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_evidence_to_conclusion_shortcuts() -> None:
    """Catches an explanation that skips the anomaly and mechanism layers."""
    graph = _valid_market_graph()
    evidence_id, _ = _only_node(graph, "Evidence")
    consequence_id, _ = _only_node(graph, "RiskConsequence")
    mechanism_id, _ = _only_node(graph, "Mechanism")
    _, _, template_key, template = next(
        iter(graph.edges(mechanism_id, keys=True, data=True))
    )
    assert template_key == template["edge_id"]
    edge_id = "edge:malformed:evidence-conclusion-shortcut"
    graph.add_edge(
        evidence_id,
        consequence_id,
        key=edge_id,
        **{**template, "edge_id": edge_id},
    )

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_any_quality_route_to_warning_state() -> None:
    """Catches a structurally valid SUPPORTS edge laundering quality into risk."""
    graph = _build(
        [make_feature_evidence("coverage_shortfall", 1.2)],
        alert_level=1,
        alert_name="关注",
    )
    mechanism_id, _ = _only_node(graph, "Mechanism")
    warning_id, _ = _only_node(graph, "WarningState")
    anomaly_id, _ = _only_node(graph, "Anomaly")
    _, _, _, support = next(iter(graph.edges(anomaly_id, keys=True, data=True)))
    edge_id = "edge:malformed:quality-warning-support"
    graph.add_edge(
        mechanism_id,
        warning_id,
        key=edge_id,
        **{**support, "edge_id": edge_id},
    )

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_non_multidigraph_and_non_multigraph_payload() -> None:
    """Catches loss of parallel-edge keys at validation or deserialization."""
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(nx.DiGraph())  # type: ignore[arg-type]

    payload = graph_to_node_link(_valid_market_graph())
    payload["multigraph"] = False
    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


def test_node_link_serialization_is_json_safe_sorted_and_deterministic() -> None:
    """Catches insertion-order output, Timestamp leakage, and unstable multiedges."""
    first = _build(
        [
            make_feature_evidence("gamma_hhi", 1.2),
            make_feature_evidence("atm_iv", 0.95),
        ],
        alert_level=1,
        alert_name="关注",
    )
    second = _build(
        [
            make_feature_evidence("atm_iv", 0.95),
            make_feature_evidence("gamma_hhi", 1.2),
        ],
        alert_level=1,
        alert_name="关注",
    )
    first_payload = graph_to_node_link(first)
    second_payload = graph_to_node_link(second)

    encoded_first = json.dumps(first_payload, ensure_ascii=False, sort_keys=True)
    encoded_second = json.dumps(second_payload, ensure_ascii=False, sort_keys=True)
    assert encoded_first == encoded_second
    assert [row["id"] for row in first_payload["nodes"]] == sorted(first.nodes)
    assert [
        (row["source"], row["target"], row["relation_type"], row["edge_id"])
        for row in first_payload["edges"]
    ] == sorted(
        (
            row["source"],
            row["target"],
            row["relation_type"],
            row["edge_id"],
        )
        for row in first_payload["edges"]
    )
    assert first_payload["graph"]["timestamp"] == "2025-04-07T10:15:00"


def test_node_link_round_trip_restores_timestamps_keys_and_exact_payload() -> None:
    """Catches audit payloads that deserialize without their temporal or edge identity."""
    graph = _valid_market_graph()
    payload = graph_to_node_link(graph)
    restored = graph_from_node_link(deepcopy(payload))

    assert isinstance(restored, nx.MultiDiGraph)
    assert restored.graph["timestamp"] == SNAPSHOT
    assert all(
        isinstance(data["source_timestamp"], pd.Timestamp)
        for _, data in restored.nodes(data=True)
    )
    assert all(
        isinstance(data["source_timestamp"], pd.Timestamp)
        for _, _, data in restored.edges(data=True)
    )
    assert {
        key for _, _, key in restored.edges(keys=True)
    } == {
        data["edge_id"] for _, _, data in restored.edges(data=True)
    }
    assert graph_to_node_link(restored) == payload


# Review fix round 1: adversarial semantic-validation probes.


def test_validator_rejects_market_mechanism_rewired_to_confidence() -> None:
    """Catches a market FeatureRule being allowed to terminate as data quality."""
    graph = _build([make_feature_evidence("atm_iv", 1.15)])
    mechanism_id, _ = _node_for_feature(graph, "Mechanism", "atm_iv")
    consequence_id, _ = _node_for_feature(graph, "RiskConsequence", "atm_iv")
    confidence_id, _ = _only_node(graph, "ConfidenceState")
    _remove_edges_between(graph, mechanism_id, consequence_id)
    graph.remove_node(consequence_id)
    edge_id, attributes = _edge_attributes(
        source=mechanism_id,
        target=confidence_id,
        relation_type="REDUCES_CONFIDENCE",
        rule_id=f"{KG_RULE_VERSION}:atm_iv",
        semantic_class="confidence",
    )
    graph.add_edge(mechanism_id, confidence_id, key=edge_id, **attributes)

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_quality_mechanism_rewired_to_risk_consequence() -> None:
    """Catches a quality FeatureRule being promoted to a market consequence."""
    graph = _build([make_feature_evidence("coverage_shortfall", 1.2)])
    mechanism_id, _ = _node_for_feature(graph, "Mechanism", "coverage_shortfall")
    confidence_id, _ = _only_node(graph, "ConfidenceState")
    _remove_edges_between(graph, mechanism_id, confidence_id)

    market = _build([make_feature_evidence("atm_iv", 1.2)])
    consequence_id, consequence = _node_for_feature(
        market, "RiskConsequence", "atm_iv"
    )
    graph.add_node(consequence_id, **deepcopy(consequence))
    edge_id, attributes = _edge_attributes(
        source=mechanism_id,
        target=consequence_id,
        relation_type="MAY_LEAD_TO",
        rule_id=f"{KG_RULE_VERSION}:coverage_shortfall",
        semantic_class="possible",
    )
    graph.add_edge(mechanism_id, consequence_id, key=edge_id, **attributes)

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_cross_feature_layer_mixing() -> None:
    """Catches Evidence from one rule feeding another rule's Anomaly."""
    graph = _build(
        [
            make_feature_evidence("atm_iv", 1.2),
            make_feature_evidence("gamma_hhi", 1.2),
        ]
    )
    evidence_id, _ = _node_for_feature(graph, "Evidence", "atm_iv")
    own_anomaly_id, _ = _node_for_feature(graph, "Anomaly", "atm_iv")
    other_anomaly_id, _ = _node_for_feature(graph, "Anomaly", "gamma_hhi")
    _remove_edges_between(graph, evidence_id, own_anomaly_id)
    edge_id, attributes = _edge_attributes(
        source=evidence_id,
        target=other_anomaly_id,
        relation_type="EXCEEDS",
        rule_id=f"{KG_RULE_VERSION}:atm_iv",
        semantic_class="observed",
    )
    graph.add_edge(evidence_id, other_anomaly_id, key=edge_id, **attributes)

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_warning_support_when_formal_level_is_zero() -> None:
    """Catches a fabricated alert-support path for an authoritative level zero."""
    graph = _build([make_feature_evidence("atm_iv", 1.2)])
    mechanism_id, _ = _node_for_feature(graph, "Mechanism", "atm_iv")
    warning_id, _ = _only_node(graph, "WarningState")
    edge_id, attributes = _edge_attributes(
        source=mechanism_id,
        target=warning_id,
        relation_type="SUPPORTS",
        rule_id=f"{KG_RULE_VERSION}:atm_iv",
        semantic_class="support",
    )
    graph.add_edge(mechanism_id, warning_id, key=edge_id, **attributes)

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("original_pressure", "changed_pressure", "changed_relation", "semantic_class"),
    [
        (0.95, 0.89, None, None),
        (0.95, None, "EXCEEDS", "observed"),
        (0.95, None, "VIOLATES", "constraint"),
    ],
)
def test_validator_recomputes_activation_and_first_relation(
    original_pressure: float,
    changed_pressure: float | None,
    changed_relation: str | None,
    semantic_class: str | None,
) -> None:
    """Catches 0.89+NEAR, 0.95+EXCEEDS, and ordinary-feature VIOLATES."""
    graph = _build([make_feature_evidence("atm_iv", original_pressure)])
    evidence_id, evidence = _node_for_feature(graph, "Evidence", "atm_iv")
    if changed_pressure is not None:
        evidence["pressure_ratio"] = changed_pressure
    source, target, key, data = next(iter(graph.out_edges(evidence_id, keys=True, data=True)))
    assert source == evidence_id
    if changed_relation is not None:
        data["relation_type"] = changed_relation
        data["semantic_class"] = semantic_class

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_noncanonical_node_and_edge_ids() -> None:
    """Catches IDs that are internally equal but not deterministically derived."""
    graph = _valid_market_graph()
    product_id, _ = _only_node(graph, "Product")
    nx.relabel_nodes(graph, {product_id: "product:arbitrary"}, copy=False)
    graph.nodes["product:arbitrary"]["node_id"] = "product:arbitrary"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    source, target, key, data = next(iter(graph.edges(keys=True, data=True)))
    graph.remove_edge(source, target, key)
    data["edge_id"] = "edge:arbitrary"
    graph.add_edge(source, target, key="edge:arbitrary", **data)
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_rejects_noncanonical_wording_template() -> None:
    """Catches a nonempty but unregistered explanatory wording template."""
    graph = _valid_market_graph()
    source, target, key = next(iter(graph.edges(keys=True)))
    graph[source][target][key]["wording_template"] = "任意非空话术"

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("field", "changed_value"),
    [
        ("group", "错误分组"),
        ("label", "错误标签"),
        ("rule_id", f"{KG_RULE_VERSION}:gamma_hhi"),
        ("source", "错误来源"),
        ("status", "危险"),
        ("direction", "持平"),
        ("severity", 3),
    ],
)
def test_validator_rejects_evidence_field_drift(
    field: str, changed_value: object
) -> None:
    """Catches canonical Evidence identity or derived state being overwritten."""
    graph = _build([make_feature_evidence("atm_iv", 0.95)])
    _, evidence = _only_node(graph, "Evidence")
    evidence[field] = changed_value

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("node_type", "field", "changed_value"),
    [
        ("Anomaly", "anomaly_code", "anomaly_gamma_hhi"),
        ("Anomaly", "label", "错误异常"),
        ("Anomaly", "category", "错误分组"),
        ("Mechanism", "mechanism_code", "mechanism_gamma_hhi"),
        ("Mechanism", "label", "错误机理"),
        ("Mechanism", "scope", "confidence"),
        ("Mechanism", "wording_boundary", "错误边界"),
        ("RiskConsequence", "consequence_code", "risk_consequence_gamma_hhi"),
        ("RiskConsequence", "label", "错误后果"),
        ("RiskConsequence", "non_directional", False),
    ],
)
def test_validator_rejects_registered_semantic_node_drift(
    node_type: str, field: str, changed_value: object
) -> None:
    """Catches semantic nodes that no longer match their FeatureRule."""
    graph = _valid_market_graph()
    node_id, _ = _only_node(graph, node_type)
    graph.nodes[node_id][field] = changed_value

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize("alert_level", [9, True])
def test_builder_rejects_invalid_formal_alert_level(alert_level: object) -> None:
    """Catches out-of-range or bool values masquerading as a formal level."""
    alert_name = "关注" if alert_level is True else "危险"
    with pytest.raises(KnowledgeGraphValidationError):
        _build([], alert_level=alert_level, alert_name=alert_name)  # type: ignore[arg-type]


def test_builder_rejects_invalid_warning_scalar_types() -> None:
    """Catches bool/nonfinite risk scores and non-bool emission flags."""
    with pytest.raises(KnowledgeGraphValidationError):
        _build([], risk_score=True)
    with pytest.raises(KnowledgeGraphValidationError):
        _build([], risk_score=np.nan)
    with pytest.raises(KnowledgeGraphValidationError):
        _build([], alert_emitted=1)


def test_validator_rejects_warning_and_confidence_state_drift() -> None:
    """Catches formal alert names and recomputed quality state being overwritten."""
    graph = _valid_market_graph()
    _, warning = _only_node(graph, "WarningState")
    warning["alert_name"] = "危险"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _build([make_feature_evidence("coverage_shortfall", 1.2)])
    _, confidence = _only_node(graph, "ConfidenceState")
    confidence["level"] = "normal"
    confidence["quality_reasons"] = []
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_node_link_preflight_rejects_pressure_tamper_with_active_edge() -> None:
    """Catches raw payload activation drift before returning a graph."""
    payload = graph_to_node_link(
        _build([make_feature_evidence("atm_iv", 0.95)])
    )
    evidence = next(row for row in payload["nodes"] if row["node_type"] == "Evidence")
    evidence["pressure_ratio"] = 0.89

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


def test_node_link_preflight_rejects_nonfinite_numbers() -> None:
    """Catches raw NaN being silently converted or accepted as a missing value."""
    payload = graph_to_node_link(_valid_market_graph())
    warning = next(
        row for row in payload["nodes"] if row["node_type"] == "WarningState"
    )
    warning["risk_score"] = float("nan")

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


def test_node_link_preflight_rejects_duplicate_edge_records() -> None:
    """Catches NetworkX overwriting a duplicate multiedge before validation."""
    payload = graph_to_node_link(_valid_market_graph())
    payload["edges"].append(deepcopy(payload["edges"][0]))

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


def test_node_link_preflight_rejects_duplicate_node_records() -> None:
    """Catches NetworkX overwriting a duplicate node before validation."""
    payload = graph_to_node_link(_valid_market_graph())
    payload["nodes"].append(deepcopy(payload["nodes"][0]))

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


# Review fix round 2: policy binding, strict public fields, and raw-cycle probes.


def _custom_policy() -> DecisionPolicy:
    return DecisionPolicy(
        attention_pressure=0.80,
        attention_release_pressure=0.75,
        warning_pressure=0.82,
        warning_upper_pressure=0.90,
        danger_pressure=0.90,
        danger_core_pressure=1.20,
    )


def test_custom_policy_drives_severity_activation_and_round_trip() -> None:
    """Catches validation or severity silently falling back to a default policy."""
    policy = _custom_policy()
    graph = _build(
        [make_feature_evidence("atm_iv", 0.85)],
        policy=policy,
        policy_parameter_hash=policy.parameter_hash,
    )
    evidence_id, evidence = _only_node(graph, "Evidence")

    assert graph.graph["attention_pressure"] == 0.80
    assert graph.graph["policy_parameters"] == asdict(policy)
    assert graph.graph["policy_parameter_hash"] == policy.parameter_hash
    assert evidence["severity"] == 2
    assert evidence["status"] == "警告"
    assert {
        data["relation_type"]
        for _, _, data in graph.out_edges(evidence_id, data=True)
    } == {"NEAR_THRESHOLD"}

    payload = graph_to_node_link(graph)
    restored = graph_from_node_link(payload)
    assert graph_to_node_link(restored) == payload
    _, restored_evidence = _only_node(restored, "Evidence")
    assert restored_evidence["severity"] == 2


def test_validator_rejects_coordinated_state_tamper_that_ignores_full_policy() -> None:
    """Catches attention/pressure/status/path edits not bound to policy parameters."""
    policy = _custom_policy()
    graph = _build(
        [make_feature_evidence("atm_iv", 0.85)],
        policy=policy,
        policy_parameter_hash=policy.parameter_hash,
    )
    graph.graph["attention_pressure"] = 0.90
    _, evidence = _only_node(graph, "Evidence")
    evidence["pressure_ratio"] = 0.95
    evidence["severity"] = 1
    evidence["status"] = "关注"

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("mutation", "value"),
    [
        ("hash", "not-the-policy-hash"),
        ("integer_type", True),
        ("float_type", "0.82"),
    ],
)
def test_validator_rejects_policy_parameter_or_hash_drift(
    mutation: str, value: object
) -> None:
    """Catches policy metadata that cannot reconstruct the hashed policy."""
    policy = _custom_policy()
    graph = _build(
        [make_feature_evidence("atm_iv", 0.85)],
        policy=policy,
        policy_parameter_hash=policy.parameter_hash,
    )
    graph.graph["policy_parameters"] = asdict(policy)
    graph.graph["policy_parameter_hash"] = policy.parameter_hash
    if mutation == "hash":
        graph.graph["policy_parameter_hash"] = value
    elif mutation == "integer_type":
        graph.graph["policy_parameters"]["multi_signal_count"] = value
    else:
        graph.graph["policy_parameters"]["warning_pressure"] = value

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_validator_binds_optional_snapshot_and_warning_policy_identity() -> None:
    """Catches optional policy mirrors disagreeing with the reconstructed policy."""
    graph = _valid_market_graph()
    _, snapshot = _only_node(graph, "RiskSnapshot")
    snapshot["policy_version"] = "wrong-policy-version"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)

    graph = _valid_market_graph()
    _, warning = _only_node(graph, "WarningState")
    warning["policy_hash"] = "wrong-policy-hash"
    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("node_type", "field", "value"),
    [
        ("RiskSnapshot", "policy_version", 7),
        ("RiskSnapshot", "price_source", ""),
        ("WarningState", "transition_reason", 7),
        ("WarningState", "policy_hash", 7),
    ],
)
def test_validator_rejects_invalid_public_field_types(
    node_type: str, field: str, value: object
) -> None:
    """Catches present-but-wrongly-typed public node fields."""
    graph = _build([])
    _, node = _only_node(graph, node_type)
    node[field] = value

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    ("owner", "field"),
    [
        ("graph", "causal_probability"),
        ("node", "causal_probability"),
        ("edge", "causal_probability"),
        ("graph", "confidence_weight"),
        ("node", "confidence_weight"),
        ("edge", "confidence_weight"),
        ("graph", "causal_confidence"),
        ("node", "causal_confidence"),
        ("edge", "causal_confidence"),
    ],
)
def test_validator_rejects_forbidden_causal_or_confidence_weights(
    owner: str, field: str
) -> None:
    """Catches prohibited numeric confidence semantics hidden as extra attributes."""
    graph = _valid_market_graph()
    if owner == "graph":
        graph.graph[field] = 0.5
    elif owner == "node":
        node_id = next(iter(graph.nodes))
        graph.nodes[node_id][field] = 0.5
    else:
        source, target, key = next(iter(graph.edges(keys=True)))
        graph[source][target][key][field] = 0.5

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    "location",
    ["graph", "snapshot", "node_source", "edge_source"],
)
def test_validator_requires_in_memory_contract_times_to_be_timestamps(
    location: str,
) -> None:
    """Catches parseable strings being accepted inside an in-memory graph."""
    graph = _valid_market_graph()
    if location == "graph":
        graph.graph["timestamp"] = SNAPSHOT.isoformat()
    elif location == "snapshot":
        _, snapshot = _only_node(graph, "RiskSnapshot")
        snapshot["timestamp"] = SNAPSHOT.isoformat()
    elif location == "node_source":
        node_id = next(iter(graph.nodes))
        graph.nodes[node_id]["source_timestamp"] = SNAPSHOT.isoformat()
    else:
        source, target, key = next(iter(graph.edges(keys=True)))
        graph[source][target][key]["source_timestamp"] = SNAPSHOT.isoformat()

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    "raw_timestamp",
    [SNAPSHOT.value, [2025, 4, 7], {"year": 2025, "month": 4, "day": 7}],
)
def test_node_link_preflight_rejects_non_string_timestamps(
    raw_timestamp: object,
) -> None:
    """Catches integer nanoseconds and collection values at the ISO boundary."""
    payload = graph_to_node_link(_valid_market_graph())
    payload["graph"]["timestamp"] = raw_timestamp
    for node in payload["nodes"]:
        node["source_timestamp"] = raw_timestamp
        if node["node_type"] == "RiskSnapshot":
            node["timestamp"] = raw_timestamp
    for edge in payload["edges"]:
        edge["source_timestamp"] = raw_timestamp

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


def test_node_link_preflight_rejects_noncanonical_iso_timestamp() -> None:
    """Catches a parseable timestamp string that does not losslessly round-trip."""
    payload = graph_to_node_link(_valid_market_graph())
    payload["edges"][0]["source_timestamp"] = "2025-04-07T10:15:00.000000"

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


@pytest.mark.parametrize("container_kind", ["mapping", "list"])
def test_node_link_preflight_rejects_cyclic_payloads(container_kind: str) -> None:
    """Catches raw self-references escaping as RecursionError or hanging validation."""
    payload = graph_to_node_link(_valid_market_graph())
    if container_kind == "mapping":
        cycle: dict[str, object] = {}
        cycle["self"] = cycle
    else:
        cycle = []
        cycle.append(cycle)
    payload["cycle"] = cycle

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


# Review fix round 3: authoritative version, lossless mappings, and key normalization.


def test_validator_rejects_coordinated_formal_policy_version_tamper() -> None:
    """Catches an internally coordinated policy version outside the formal contract."""
    graph = _valid_market_graph()
    graph.graph["policy_parameters"]["policy_version"] = "evil-v9"
    _, snapshot = _only_node(graph, "RiskSnapshot")
    snapshot["policy_version"] = "evil-v9"

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


def test_builder_rejects_non_authoritative_policy_version() -> None:
    """Catches custom thresholds smuggling a non-formal policy version."""
    policy = replace(_custom_policy(), policy_version="evil-v9")

    with pytest.raises(KnowledgeGraphValidationError):
        _build(
            [],
            policy=policy,
            policy_version="evil-v9",
            policy_parameter_hash=policy.parameter_hash,
        )


@pytest.mark.parametrize(
    "data_quality",
    [
        {1: "int", "1": "str"},
        {"nested": {1: "int-key"}},
    ],
)
def test_graph_to_node_link_rejects_non_string_mapping_keys(
    data_quality: dict[object, object],
) -> None:
    """Catches JSON conversion overwriting or renaming Mapping keys."""
    graph = _build([], data_quality=data_quality)

    with pytest.raises(KnowledgeGraphValidationError):
        graph_to_node_link(graph)


@pytest.mark.parametrize("extra_key", ["arbitrary", "causal_probability"])
def test_node_link_preflight_rejects_extra_top_level_keys(extra_key: str) -> None:
    """Catches top-level data that NetworkX would silently discard."""
    payload = graph_to_node_link(_valid_market_graph())
    payload[extra_key] = 0.5

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


@pytest.mark.parametrize(
    "missing_key", ["directed", "multigraph", "graph", "nodes", "edges"]
)
def test_node_link_preflight_rejects_missing_top_level_keys(
    missing_key: str,
) -> None:
    """Catches an incomplete node-link envelope before NetworkX defaults fields."""
    payload = graph_to_node_link(_valid_market_graph())
    del payload[missing_key]

    with pytest.raises(KnowledgeGraphValidationError):
        graph_from_node_link(payload)


@pytest.mark.parametrize(
    ("owner", "field"),
    [
        (owner, field)
        for owner in ("graph", "node", "edge")
        for field in (
            "confidenceWeight",
            "causalProbability",
            "causal-confidence",
            "probabilityWeight",
        )
    ],
)
def test_validator_normalizes_forbidden_weight_key_spellings(
    owner: str, field: str
) -> None:
    """Catches camelCase and hyphenated aliases of forbidden numeric weights."""
    graph = _valid_market_graph()
    if owner == "graph":
        graph.graph[field] = 0.5
    elif owner == "node":
        node_id = next(iter(graph.nodes))
        graph.nodes[node_id][field] = 0.5
    else:
        source, target, key = next(iter(graph.edges(keys=True)))
        graph[source][target][key][field] = 0.5

    with pytest.raises(KnowledgeGraphValidationError):
        validate_knowledge_graph(graph)


@pytest.mark.parametrize(
    "policy",
    [
        replace(DecisionPolicy(), attention_pressure=np.float32(0.90)),
        replace(DecisionPolicy(), multi_signal_count=np.int64(3)),
    ],
)
def test_builder_normalizes_numpy_policy_scalar_errors(
    policy: DecisionPolicy,
) -> None:
    """Catches raw json.dumps TypeError escaping the graph error boundary."""
    assert policy.policy_version == DECISION_POLICY_VERSION

    with pytest.raises(KnowledgeGraphValidationError):
        _build([], policy=policy)
````

</details>
