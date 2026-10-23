---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py>)

SHA-256：`9505d0bff2320b7746b907a010ecd29fdc0bacfa976b116f38a8fe345c0b3ebd`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import replace
import json

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from graph_fixtures import graph_and_paths, make_feature_evidence
from option_risk.contracts import AgentResult, KnowledgeGraphResult
from option_risk.graph_explanation import render_graph_explanation
from option_risk.graph_queries import GraphQueryService
from option_risk.graph_reasoner import build_graph_result
from option_risk.graph_visualization import knowledge_graph_figure
from option_risk.knowledge_graph import (
    KnowledgeGraphError,
    KnowledgeGraphValidationError,
    graph_from_node_link,
)


def _ready_result() -> KnowledgeGraphResult:
    graph, paths = graph_and_paths(
        [
            make_feature_evidence("atm_iv", 1.6),
            make_feature_evidence("term_inversion", 1.3),
            make_feature_evidence("gamma_hhi", 1.2),
            make_feature_evidence("coverage_shortfall", 1.4),
        ]
    )
    sections, text, confidence = render_graph_explanation(graph, paths)
    return build_graph_result(
        graph,
        missing_evidence=(),
        explanation_sections=sections,
        explanation_text=text,
        explanation_confidence=confidence,
    )


def _node_points(figure):
    return next(trace for trace in figure.data if trace.name == "图谱节点")


def test_figure_uses_fixed_layers_canonical_path_cap_and_meta_provenance() -> None:
    """Catches non-layered/random layouts, reordered paths, or untraceable display data."""
    result = _ready_result()

    figure = knowledge_graph_figure(result, max_paths=3)
    points = _node_points(figure)
    selected_paths = result.active_paths[:3]

    graph = graph_from_node_link(result.graph_json)
    expected_nodes = []
    expected_edges = []
    tracks = {}
    for track, path in enumerate(selected_paths):
        for node_id in (path.evidence_node_id, path.anomaly_node_id, path.mechanism_node_id, path.conclusion_node_id):
            if node_id not in expected_nodes:
                expected_nodes.append(node_id)
            tracks.setdefault(node_id, []).append(-track)
        for edge_id in path.edge_ids:
            if edge_id not in expected_edges:
                expected_edges.append(edge_id)
    expected_x = {"Evidence": 0, "Anomaly": 1, "Mechanism": 2, "RiskConsequence": 3, "WarningState": 3, "ConfidenceState": 3}
    point_rows = {row[0]: (row[1], points.x[index], points.y[index]) for index, row in enumerate(points.customdata)}

    assert tuple(figure.layout.meta["path_ids"]) == tuple(path.path_id for path in selected_paths)
    assert tuple(figure.layout.meta["node_ids"]) == tuple(expected_nodes)
    assert tuple(figure.layout.meta["edge_ids"]) == tuple(expected_edges)
    assert tuple(row[0] for row in points.customdata) == tuple(expected_nodes)
    for node_id in expected_nodes:
        node_type, x, y = point_rows[node_id]
        assert x == expected_x[node_type]
        assert y == sum(tracks[node_id]) / len(tracks[node_id])
        assert node_type == graph.nodes[node_id]["node_type"]
    arrow_annotations = [item for item in figure.layout.annotations if item.showarrow]
    edge_relation = {row["edge_id"]: row["relation_type"] for row in result.graph_json["edges"]}
    assert len(arrow_annotations) == len(expected_edges)
    assert tuple(item.text for item in arrow_annotations) == tuple(edge_relation[item] for item in expected_edges)
    assert figure.layout.clickmode == "event+select"


def test_figure_deduplicates_shared_nodes_edges_and_is_repeatable() -> None:
    """Catches duplicate shared state nodes/edges or unstable Figure serialization."""
    result = _ready_result()

    first = knowledge_graph_figure(result, max_paths=3)
    second = knowledge_graph_figure(result, max_paths=3)
    points = _node_points(first)

    assert len(points.customdata) == len(tuple(dict.fromkeys(row[0] for row in points.customdata)))
    assert len(first.layout.annotations) == len(first.layout.meta["edge_ids"])
    restored = KnowledgeGraphResult.from_dict(result.to_dict())
    round_tripped = knowledge_graph_figure(restored, max_paths=3)
    assert first.to_plotly_json() == second.to_plotly_json() == round_tripped.to_plotly_json()
    assert json.loads(first.to_json()) == json.loads(second.to_json()) == json.loads(round_tripped.to_json())


def test_evidence_hover_and_quality_path_are_registered_and_visible() -> None:
    """Catches hover values inferred outside graph records or an invisible confidence path."""
    result = _ready_result()

    figure = knowledge_graph_figure(result, max_paths=3)
    points = _node_points(figure)
    evidence_row = next(
        row for row in points.customdata if str(row[0]).startswith("evidence:")
    )

    evidence_index = next(index for index, row in enumerate(points.customdata) if row[0] == result.active_paths[0].evidence_node_id)
    evidence = graph_from_node_link(result.graph_json).nodes[result.active_paths[0].evidence_node_id]
    assert points.hovertext[evidence_index] == (
        f"<b>{evidence['label']}</b><br>类型：Evidence<br>品种：{evidence['product']}"
        f"<br>时间：{evidence['source_timestamp']}<br>当前值：{evidence['current_value']}"
        f"<br>动态阈值：{evidence['reference_value']}<br>压力：{evidence['pressure_ratio']}"
        f"<br>方向：{evidence['direction']}<br>数据源：{evidence['source']}"
        f"<br>规则ID：{evidence['rule_id']}"
    )
    assert evidence_row[1] == "Evidence"
    quality_graph, quality_paths = graph_and_paths(
        [make_feature_evidence("coverage_shortfall", 1.4)]
    )
    assert len(quality_paths) == 1
    quality = knowledge_graph_figure(
        build_graph_result(quality_graph, missing_evidence=()), max_paths=1
    )
    assert "置信度路径" in " ".join(annotation.text for annotation in quality.layout.annotations)


def test_edge_annotations_are_exact_registered_relations_and_quality_label_is_separate() -> None:
    """Catches a quality badge mutating an edge's registered relation_type text."""
    result = _ready_result()
    figure = knowledge_graph_figure(result, max_paths=3)
    graph, quality_paths = graph_and_paths([make_feature_evidence("coverage_shortfall", 1.4)])
    quality = knowledge_graph_figure(build_graph_result(graph, missing_evidence=()), max_paths=1)

    expected = {
        relation
        for path in result.active_paths[:3]
        for relation in path.relation_semantics
    }
    arrows = [item for item in figure.layout.annotations if item.showarrow]
    quality_arrows = [item for item in quality.layout.annotations if item.showarrow]

    assert all(item.text in expected for item in arrows)
    assert [item.text for item in quality_arrows] == list(quality_paths[0].relation_semantics)
    assert any(
        item.text == "置信度路径" and not item.showarrow
        for item in quality.layout.annotations
    )


@pytest.mark.parametrize("invalid", [True, 0, -1, 1.0, 4])
def test_figure_rejects_non_strict_or_out_of_range_path_cap(invalid) -> None:
    """Catches bool/float or an unsupported number of rendered canonical paths."""
    with pytest.raises((TypeError, ValueError)):
        knowledge_graph_figure(_ready_result(), max_paths=invalid)


def test_figure_shows_a_true_empty_state_without_invented_nodes_or_edges() -> None:
    """Catches a zero-active-path graph being drawn as a synthetic relationship."""
    graph, paths = graph_and_paths([make_feature_evidence("atm_iv", 0.5)])
    assert paths == []
    result = build_graph_result(graph, missing_evidence=())

    figure = knowledge_graph_figure(result)

    assert figure.layout.meta == {"path_ids": [], "node_ids": [], "edge_ids": []}
    assert len(figure.data) == 0
    assert "没有活跃异常/接近阈值证据路径" in figure.layout.annotations[0].text


def test_figure_revalidates_and_rejects_unavailable_or_tampered_results() -> None:
    """Catches visualization trusting unavailable or forged graph payloads."""
    result = _ready_result()
    forged = replace(result, node_count=result.node_count + 1)

    with pytest.raises(KnowledgeGraphValidationError):
        knowledge_graph_figure(forged)
    with pytest.raises(KnowledgeGraphValidationError):
        knowledge_graph_figure(
            KnowledgeGraphResult.unavailable(product="ag", timestamp=pd.Timestamp("2025-04-07 10:15"))
        )


def test_dashboard_preset_queries_and_stale_node_ids_use_only_validated_service() -> None:
    """Catches preset labels bypassing GraphQueryService or stale Plotly selections crashing."""
    from option_risk.dashboard import _preset_query_rows, _selected_node_detail

    service = GraphQueryService(_ready_result())
    labels = [
        "为什么是当前预警等级？",
        "最主要的三项直接数据根因是什么？",
        "风险可能如何传导？",
        "可能影响哪些风险维度？",
        "当前结论的数据可信度如何？",
        "查看全部证据路径",
    ]

    result = _ready_result()
    rows = [_preset_query_rows(service, result, label) for label in labels]

    assert [row["path_id"] for row in rows[0]] == [
        path.path_id
        for path in result.active_paths
        if path.conclusion_node_id.startswith("warning:")
    ]
    assert [row["node_id"] for row in rows[1]] == list(result.root_evidence[:3])
    assert [row["path_id"] for row in rows[2]] == [
        path.path_id for path in result.active_paths[:3]
    ]
    assert [row["node_id"] for row in rows[3]] == list(result.possible_consequences)
    assert [row["path_id"] for row in rows[4]] == [
        path.path_id
        for path in result.active_paths
        if path.conclusion_node_id.startswith("confidence:")
    ]
    assert [row["path_id"] for row in rows[5]] == [
        path.path_id for path in result.active_paths
    ]
    assert _selected_node_detail(service, "node:stale") is None
    assert _selected_node_detail(service, service.root_evidence()[0]["node_id"])["node_type"] == "Evidence"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda result: replace(result, explanation_sections=()),
        lambda result: replace(result, explanation_sections=tuple(reversed(result.explanation_sections))),
        lambda result: replace(result, explanation_sections=(replace(result.explanation_sections[0], title="<b>forged-title</b>"), *result.explanation_sections[1:])),
        lambda result: replace(result, explanation_sections=(replace(result.explanation_sections[0], content="forged path text"), *result.explanation_sections[1:])),
        lambda result: replace(result, explanation_confidence="forged"),
        lambda result: replace(result, explanation_text="forged complete explanation"),
    ],
    ids=["missing", "reordered", "title", "content", "confidence", "text"],
)
def test_dashboard_requires_canonical_explanation_before_any_graph_display(mutation) -> None:
    """Catches arbitrary cached prose, titles, section order, or confidence crossing into the UI."""
    from option_risk.dashboard import _validated_graph_view

    with pytest.raises(KnowledgeGraphError, match="解释"):
        _validated_graph_view(mutation(_ready_result()), _agent_result())


def _agent_result() -> AgentResult:
    graph = _ready_result()
    warning = next(
        data
        for _, data in graph_from_node_link(graph.graph_json).nodes(data=True)
        if data["node_type"] == "WarningState"
    )
    return AgentResult(
        product=graph.product,
        timestamp=graph.timestamp,
        status="ready",
        alert_level=2,
        alert_name="警告",
        alert_emitted=warning["alert_emitted"],
        risk_score=warning["risk_score"],
        price_source="reconstructed_proxy",
        data_quality={}, surfaces={}, feature_evidence=[], trigger_reasons=[],
        timeline=pd.DataFrame(), evaluation=None,
        policy_version="validated-dynamic-state-v2", policy_parameter_hash=warning["policy_hash"],
        transition_reason=warning["transition_reason"], knowledge_graph=graph,
    )


def test_validated_graph_view_cross_checks_problem_one_warning_state() -> None:
    """Catches the graph tab caption trusting a mismatched outer AgentResult."""
    from option_risk.dashboard import _validated_graph_view

    graph = _ready_result()
    service, sections, confidence, warning = _validated_graph_view(graph, _agent_result())

    assert service.paths_to_alert()
    assert sections == graph.explanation_sections
    assert confidence == graph.explanation_confidence
    assert warning["alert_level"] == 2
    with pytest.raises(KnowledgeGraphError, match="WarningState"):
        _validated_graph_view(graph, replace(_agent_result(), alert_name="伪造"))


def test_exact_plotly_selection_round_trip_rejects_malformed_payloads() -> None:
    """Catches a click selecting anything other than the rendered node-id customdata."""
    from option_risk.dashboard import _selected_node_detail, _selection_node_id

    node_id = _ready_result().active_paths[0].evidence_node_id
    payload = {"selection": {"points": [{"customdata": [node_id, "Evidence"]}]}}

    assert _selection_node_id(payload) == node_id
    assert _selected_node_detail(GraphQueryService(_ready_result()), _selection_node_id(payload))["node_id"] == node_id
    class AttributeSelection:
        selection = {"points": [{"customdata": [node_id, "Evidence"]}]}
    assert _selection_node_id(AttributeSelection()) == node_id
    assert _selection_node_id({"selection": {"points": [{"customdata": []}]}}) is None
    assert _selection_node_id({"selection": {"points": []}}) is None


def test_unavailable_graph_isolated_to_its_tab_rendering() -> None:
    """Catches graph validation failure preventing existing Problem 1 content from rendering."""
    app = AppTest.from_string(
        '''
import pandas as pd
import streamlit as st
from option_risk.contracts import AgentResult, KnowledgeGraphResult
from option_risk.dashboard import _render_knowledge_graph

result = AgentResult(
    product="ag", timestamp=pd.Timestamp("2025-04-07 10:15"), status="ready",
    alert_level=2, alert_name="警告", alert_emitted=False, risk_score=0.5,
    price_source="reconstructed_proxy", data_quality={}, surfaces={},
    feature_evidence=[], trigger_reasons=[], timeline=pd.DataFrame(), evaluation=None,
    policy_version="validated-dynamic-state-v2", policy_parameter_hash="hash",
    transition_reason="normal",
    knowledge_graph=KnowledgeGraphResult.unavailable(product="ag", timestamp="2025-04-07 10:15"),
)
st.write("问题一仍可用")
_render_knowledge_graph(result)
'''
    ).run()

    assert len(app.exception) == 0
    assert any("问题一仍可用" in item.value for item in app.markdown)
    assert any("风险知识图谱暂不可用" in item.value for item in app.warning)
````

</details>
