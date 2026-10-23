---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py>)

SHA-256：`b39d5558831c5b38496edeada764b8068890b1cf4788ee440f5f884bbc8c6160`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import replace
import json

import pandas as pd
import pytest

from graph_fixtures import graph_and_paths, graph_context, make_feature_evidence
from option_risk.contracts import ExplanationSection
from option_risk.decision import DecisionPolicy
from option_risk.graph_reasoner import (
    build_graph_result,
    discover_risk_paths,
    rank_risk_paths,
)
from option_risk.knowledge_graph import (
    KnowledgeGraphError,
    build_knowledge_graph,
    graph_to_node_link,
)
from option_risk.knowledge_schema import FEATURE_RULES, KG_RULE_VERSION


def _feature_for_path(path) -> str:
    marker = "evidence:ag:20250407T101500:"
    assert path.evidence_node_id.startswith(marker)
    return path.evidence_node_id.removeprefix(marker)


def test_reasoner_returns_every_legal_four_layer_path() -> None:
    """Catches omitted legal terminals or traversal outside the approved four layers."""
    graph = build_knowledge_graph(
        **graph_context(alert_level=2, alert_name="警告"),
        evidence=[
            make_feature_evidence("atm_iv", 1.15),
            make_feature_evidence("coverage_shortfall", 1.4),
        ],
        policy=DecisionPolicy(),
    )

    paths = discover_risk_paths(graph)

    assert len(paths) == 3
    assert [graph.nodes[path.conclusion_node_id]["node_type"] for path in paths] == [
        "RiskConsequence",
        "WarningState",
        "ConfidenceState",
    ]
    for path in paths:
        node_ids = (
            path.evidence_node_id,
            path.anomaly_node_id,
            path.mechanism_node_id,
            path.conclusion_node_id,
        )
        assert tuple(graph.nodes[node_id]["node_type"] for node_id in node_ids[:3]) == (
            "Evidence",
            "Anomaly",
            "Mechanism",
        )
        assert len(path.edge_ids) == 3


def test_reasoner_carries_registered_identity_and_event_metadata() -> None:
    """Catches paths losing ordered relations, versioned rule identity, or event data."""
    graph, paths = graph_and_paths([make_feature_evidence("gamma_hhi", 1.6)])

    assert [path.relation_semantics for path in paths] == [
        ("EXCEEDS", "SUPPORTS", "MAY_AMPLIFY"),
        ("EXCEEDS", "SUPPORTS", "SUPPORTS"),
    ]
    assert all(path.rule_ids == (f"{KG_RULE_VERSION}:gamma_hhi",) for path in paths)
    assert all(path.timestamp == pd.Timestamp("2025-04-07 10:15") for path in paths)
    assert all(path.pressure_ratio == 1.6 for path in paths)
    assert all(path.severity == "danger" for path in paths)
    assert len({path.path_id for path in paths}) == 2
    assert all("ag" in path.path_id and "20250407T101500" in path.path_id for path in paths)
    assert all(graph.nodes[path.conclusion_node_id]["product"] == "ag" for path in paths)


def test_reasoner_uses_dynamic_first_relation_and_excludes_inactive_evidence() -> None:
    """Catches hard-coded threshold semantics or inactive evidence entering paths."""
    graph = build_knowledge_graph(
        **graph_context(),
        evidence=[
            make_feature_evidence("atm_iv", 0.95),
            make_feature_evidence("atm_iv_chg_4", 0.89),
            make_feature_evidence("convexity_violation_ratio", 1.2),
        ],
        policy=DecisionPolicy(),
    )

    paths = discover_risk_paths(graph)

    assert [(_feature_for_path(path), path.relation_semantics[0]) for path in paths] == [
        ("convexity_violation_ratio", "VIOLATES"),
        ("atm_iv", "NEAR_THRESHOLD"),
    ]


def test_reasoner_calls_task2_full_validator_before_traversal() -> None:
    """Catches reasoning over a graph whose registered edge provenance was tampered."""
    graph, _ = graph_and_paths([make_feature_evidence("atm_iv", 1.15)])
    first_edge = next(iter(graph.edges(keys=True)))
    graph.edges[first_edge]["rule_version"] = "forged-rule-v9"

    with pytest.raises(KnowledgeGraphError, match="rule version"):
        discover_risk_paths(graph)


def test_rank_risk_paths_uses_the_complete_deterministic_total_order() -> None:
    """Catches quality-first, low-severity-first, registry drift, or terminal drift."""
    graph, paths = graph_and_paths(
        [
            make_feature_evidence("coverage_shortfall", 2.0),
            make_feature_evidence("term_inversion", 1.6),
            make_feature_evidence("atm_iv", 1.1),
            make_feature_evidence("atm_iv_chg_4", 1.6),
        ]
    )

    ranked = rank_risk_paths(tuple(reversed(paths)))

    assert [
        (_feature_for_path(path), graph.nodes[path.conclusion_node_id]["node_type"])
        for path in ranked
    ] == [
        ("atm_iv_chg_4", "RiskConsequence"),
        ("atm_iv_chg_4", "WarningState"),
        ("term_inversion", "RiskConsequence"),
        ("term_inversion", "WarningState"),
        ("atm_iv", "RiskConsequence"),
        ("atm_iv", "WarningState"),
        ("coverage_shortfall", "ConfidenceState"),
    ]
    assert [path.path_id for path in ranked] == [
        path.path_id for path in rank_risk_paths(paths)
    ]


def test_rank_risk_paths_puts_nonfinite_and_missing_pressure_last() -> None:
    """Catches NaN/None pressure producing an unstable numeric sort order."""
    _, paths = graph_and_paths([make_feature_evidence("atm_iv", 1.15)], alert_level=0, alert_name="无预警")
    base = paths[0]
    finite = replace(base, path_id="path-z", pressure_ratio=1.0)
    missing = replace(base, path_id="path-b", pressure_ratio=None)
    not_a_number = replace(base, path_id="path-a", pressure_ratio=float("nan"))

    assert [path.path_id for path in rank_risk_paths([not_a_number, missing, finite])] == [
        "path-z",
        "path-a",
        "path-b",
    ]


def test_build_graph_result_keeps_all_paths_and_builds_ranked_unique_indexes() -> None:
    """Catches top-three truncation, duplicate roots, or count/index drift."""
    graph = build_knowledge_graph(
        **graph_context(alert_level=2, alert_name="警告"),
        evidence=[
            make_feature_evidence("term_inversion", 1.2),
            make_feature_evidence("atm_iv", 1.6),
            make_feature_evidence("coverage_shortfall", 1.8),
        ],
        policy=DecisionPolicy(),
    )

    result = build_graph_result(
        graph,
        missing_evidence=("vega_hhi", "atm_iv_chg_4", "vega_hhi"),
    )

    assert result.status == "ready"
    assert result.node_count == graph.number_of_nodes()
    assert result.edge_count == graph.number_of_edges()
    assert result.active_path_count == 5
    assert len(result.active_paths) == 5
    assert result.root_evidence == tuple(
        dict.fromkeys(path.evidence_node_id for path in result.active_paths)
    )
    assert result.possible_consequences == tuple(
        dict.fromkeys(
            path.conclusion_node_id
            for path in result.active_paths
            if graph.nodes[path.conclusion_node_id]["node_type"] == "RiskConsequence"
        )
    )
    assert result.missing_evidence == ("atm_iv_chg_4", "vega_hhi")
    json.dumps(result.query_index, ensure_ascii=False, allow_nan=False)


def test_build_graph_result_copies_explanations_and_rejects_unknown_path_references() -> None:
    """Catches mutable explanation input or untraceable explanation path IDs."""
    graph, paths = graph_and_paths([make_feature_evidence("atm_iv", 1.15)])
    section = ExplanationSection(
        section_id="market",
        title="市场风险",
        content="可追溯说明",
        path_ids=(paths[0].path_id,),
    )

    result = build_graph_result(
        graph,
        missing_evidence=(),
        explanation_sections=[section],
        explanation_text="说明",
        explanation_confidence="normal",
    )

    assert result.explanation_sections == (section,)
    assert result.explanation_text == "说明"
    assert result.explanation_confidence == "normal"

    bad = replace(section, path_ids=("path:not-present",))
    with pytest.raises(KnowledgeGraphError, match="path"):
        build_graph_result(graph, missing_evidence=(), explanation_sections=(bad,))


@pytest.mark.parametrize("invalid", ["atm_iv", b"atm_iv", 7, None])
def test_build_graph_result_rejects_non_iterable_or_scalar_missing_evidence(
    invalid,
) -> None:
    """Catches scalar missing-evidence input being split or leaking a native TypeError."""
    graph, _ = graph_and_paths([make_feature_evidence("atm_iv", 1.15)])

    with pytest.raises(KnowledgeGraphError, match="missing_evidence"):
        build_graph_result(graph, missing_evidence=invalid)


def test_build_graph_result_accepts_any_iterable_of_strings_and_deduplicates_it() -> None:
    """Catches valid one-shot iterables being rejected or deduplicated unstably."""
    graph, _ = graph_and_paths([make_feature_evidence("atm_iv", 1.15)])
    missing = (value for value in ("vega_hhi", "atm_iv_chg_4", "vega_hhi"))

    result = build_graph_result(graph, missing_evidence=missing)

    assert result.missing_evidence == ("atm_iv_chg_4", "vega_hhi")


def test_discovery_is_independent_of_evidence_input_order() -> None:
    """Catches graph insertion order leaking into path identity or ranking."""
    evidence = [
        make_feature_evidence("term_inversion", 1.2),
        make_feature_evidence("atm_iv", 1.6),
        make_feature_evidence("coverage_shortfall", 1.8),
    ]
    first, first_paths = graph_and_paths(evidence)
    second, second_paths = graph_and_paths(list(reversed(evidence)))

    assert [path.to_dict() for path in first_paths] == [
        path.to_dict() for path in second_paths
    ]
    assert first.graph == second.graph
    assert [rule.order for rule in FEATURE_RULES] == list(range(1, 13))


def test_reasoner_restores_serialized_input_only_through_the_validated_boundary() -> None:
    """Catches serialized graph input being rejected or traversed without restoration."""
    graph, expected = graph_and_paths([make_feature_evidence("atm_iv", 1.15)])

    actual = discover_risk_paths(graph_to_node_link(graph))

    assert [path.to_dict() for path in actual] == [path.to_dict() for path in expected]
````

</details>
