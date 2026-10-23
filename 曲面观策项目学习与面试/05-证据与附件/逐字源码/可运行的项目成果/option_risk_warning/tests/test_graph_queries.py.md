---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_graph_queries.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py>)

SHA-256：`778182ac3be820f76e5ecfa0f58d060cc1003ed721d3d89c72bf0797442ba53a`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import inspect
import json

import pandas as pd
import pytest

from graph_fixtures import graph_and_paths, graph_context, make_feature_evidence
from option_risk.contracts import ExplanationSection, KnowledgeGraphResult
from option_risk.decision import DecisionPolicy
from option_risk.graph_queries import GraphQueryService, UnknownGraphNodeError
from option_risk.graph_reasoner import build_graph_result
from option_risk.knowledge_graph import KnowledgeGraphError, build_knowledge_graph


def _result(*, alert_level: int = 2, alert_name: str = "警告") -> KnowledgeGraphResult:
    graph = build_knowledge_graph(
        **graph_context(alert_level=alert_level, alert_name=alert_name),
        evidence=[
            make_feature_evidence("atm_iv", 1.15),
            make_feature_evidence("term_inversion", 1.6),
            make_feature_evidence("coverage_shortfall", 1.4),
        ],
        policy=DecisionPolicy(),
    )
    return build_graph_result(graph, missing_evidence=("vega_hhi",))


def test_quality_paths_never_appear_as_alert_support() -> None:
    """Catches a quality-confidence limitation being promoted to alert support."""
    graph = build_knowledge_graph(
        **graph_context(),
        evidence=[make_feature_evidence("coverage_shortfall", 1.4)],
        policy=DecisionPolicy(),
    )
    service = GraphQueryService(build_graph_result(graph, missing_evidence=[]))

    assert service.paths_to_alert() == []
    limitations = service.quality_limitations()
    assert len(limitations) == 1
    assert limitations[0]["relation_semantics"][-1] == "REDUCES_CONFIDENCE"


def test_preset_queries_return_ranked_flat_json_safe_records() -> None:
    """Catches nested node wrappers, non-JSON timestamps, or query ordering drift."""
    result = _result()
    service = GraphQueryService(result)

    roots = service.root_evidence(limit=2)
    alerts = service.paths_to_alert()
    consequences = service.possible_consequences()
    limitations = service.quality_limitations()

    assert [row["feature_name"] for row in roots] == ["term_inversion", "atm_iv"]
    assert all(row["node_type"] == "Evidence" and "properties" not in row for row in roots)
    assert all(isinstance(row["source_timestamp"], str) for row in roots)
    assert all(path["conclusion_node_id"].startswith("warning:") for path in alerts)
    assert all(row["node_type"] == "RiskConsequence" for row in consequences)
    assert all(path["conclusion_node_id"].startswith("confidence:") for path in limitations)
    json.dumps(
        {
            "roots": roots,
            "alerts": alerts,
            "consequences": consequences,
            "limitations": limitations,
        },
        ensure_ascii=False,
        allow_nan=False,
    )


@pytest.mark.parametrize("bad_limit", [-1, True, 1.0, "1", None])
def test_root_evidence_requires_a_strict_non_negative_integer(bad_limit) -> None:
    """Catches coercion of booleans, floats, strings, nulls, or negative limits."""
    service = GraphQueryService(_result())

    with pytest.raises((TypeError, ValueError)):
        service.root_evidence(limit=bad_limit)


def test_exact_node_and_anomaly_queries_reject_unknown_or_wrong_types() -> None:
    """Catches fuzzy matching, silent fallback, or non-Anomaly path lookup."""
    result = _result()
    service = GraphQueryService(result)
    anomaly_id = result.active_paths[0].anomaly_node_id
    evidence_id = result.active_paths[0].evidence_node_id

    assert service.inspect_node(anomaly_id)["node_id"] == anomaly_id
    assert all(row["anomaly_node_id"] == anomaly_id for row in service.paths_from_anomaly(anomaly_id))

    for unknown in ("anomaly:term", "TERM INVERSION", "", None):
        with pytest.raises(UnknownGraphNodeError):
            service.inspect_node(unknown)
    with pytest.raises(UnknownGraphNodeError):
        service.paths_from_anomaly(evidence_id)
    with pytest.raises(UnknownGraphNodeError):
        service.paths_from_anomaly("anomaly:not-present")


def test_query_results_are_deep_copies_isolated_from_service_and_result() -> None:
    """Catches callers mutating cached node/path data through query return values."""
    result = _result()
    original_graph_json = deepcopy(result.graph_json)
    service = GraphQueryService(result)
    snapshot_id = next(
        row["node_id"]
        for row in result.graph_json["nodes"]
        if row["node_type"] == "RiskSnapshot"
    )

    node = service.inspect_node(snapshot_id)
    node["data_quality"]["clean_rate"] = -1
    path = service.paths_to_alert()[0]
    path["relation_semantics"][0] = "FORGED"

    assert service.inspect_node(snapshot_id)["data_quality"]["clean_rate"] == 1.0
    assert service.paths_to_alert()[0]["relation_semantics"][0] in {
        "NEAR_THRESHOLD",
        "EXCEEDS",
        "VIOLATES",
    }
    assert result.graph_json == original_graph_json


def test_service_requires_a_ready_result_and_restores_only_valid_node_link_data() -> None:
    """Catches unavailable results or serialized graph tampering crossing the boundary."""
    result = _result()
    unavailable = KnowledgeGraphResult.unavailable(
        product=result.product,
        timestamp=result.timestamp,
    )
    with pytest.raises(KnowledgeGraphError, match="ready"):
        GraphQueryService(unavailable)

    graph_json = deepcopy(result.graph_json)
    graph_json["graph"]["rule_version"] = "forged-rule-v9"
    with pytest.raises(KnowledgeGraphError, match="rule version"):
        GraphQueryService(replace(result, graph_json=graph_json))


@pytest.mark.parametrize(
    "mutation",
    [
        lambda result: replace(result, schema_version="kg-schema-v9"),
        lambda result: replace(result, rule_version="kg-rule-v9"),
        lambda result: replace(result, product="au"),
        lambda result: replace(result, timestamp=pd.Timestamp("2025-04-07 10:16")),
        lambda result: replace(result, node_count=result.node_count + 1),
        lambda result: replace(result, edge_count=result.edge_count + 1),
        lambda result: replace(result, active_path_count=result.active_path_count + 1),
        lambda result: replace(result, active_paths=tuple(reversed(result.active_paths))),
        lambda result: replace(
            result,
            active_paths=(
                replace(result.active_paths[0], path_id="path:forged"),
                *result.active_paths[1:],
            ),
        ),
        lambda result: replace(
            result,
            active_paths=(
                result.active_paths[0],
                result.active_paths[0],
                *result.active_paths[2:],
            ),
        ),
        lambda result: replace(result, root_evidence=("evidence:not-present",)),
        lambda result: replace(result, possible_consequences=("consequence:not-present",)),
        lambda result: replace(
            result,
            explanation_sections=(
                ExplanationSection(
                    section_id="forged",
                    title="伪造",
                    content="不可追溯",
                    path_ids=("path:not-present",),
                ),
            ),
        ),
    ],
    ids=[
        "schema-version",
        "rule-version",
        "product",
        "timestamp",
        "node-count",
        "edge-count",
        "path-count",
        "path-order",
        "unknown-path",
        "duplicate-path-id",
        "root-index",
        "consequence-index",
        "explanation-reference",
    ],
)
def test_service_rejects_tampered_result_contract(mutation) -> None:
    """Catches trust in cached result metadata, indexes, or noncanonical paths."""
    with pytest.raises(KnowledgeGraphError):
        GraphQueryService(mutation(_result()))


def _canonical_query_index() -> dict[str, object]:
    term_consequence = (
        "path:ag:20250407T101500:term_inversion:"
        "riskconsequence:risk_consequence_term_inversion"
    )
    term_warning = (
        "path:ag:20250407T101500:term_inversion:warningstate:warning_2"
    )
    atm_consequence = (
        "path:ag:20250407T101500:atm_iv:riskconsequence:risk_consequence_atm_iv"
    )
    atm_warning = "path:ag:20250407T101500:atm_iv:warningstate:warning_2"
    quality = (
        "path:ag:20250407T101500:coverage_shortfall:"
        "confidencestate:confidence_coverage_shortfall"
    )
    return {
        "root_evidence": [
            "evidence:ag:20250407T101500:term_inversion",
            "evidence:ag:20250407T101500:atm_iv",
            "evidence:ag:20250407T101500:coverage_shortfall",
        ],
        "paths_to_alert": [term_warning, atm_warning],
        "possible_consequences": [
            "consequence:risk_consequence_term_inversion",
            "consequence:risk_consequence_atm_iv",
        ],
        "quality_limitations": [quality],
        "paths_from_anomaly": {
            "anomaly:anomaly_term_inversion": [term_consequence, term_warning],
            "anomaly:anomaly_atm_iv": [atm_consequence, atm_warning],
            "anomaly:anomaly_coverage_shortfall": [quality],
        },
    }


def test_result_and_service_require_the_exact_canonical_five_key_query_index() -> None:
    """Catches query-index fields, IDs, or ranked ordering drifting from the graph."""
    result = _result()

    service = GraphQueryService(result)

    assert result.query_index == _canonical_query_index()
    assert [row["node_id"] for row in service.root_evidence()] == result.query_index[
        "root_evidence"
    ]


def _query_index_mutations() -> list[object]:
    canonical = _canonical_query_index()
    nonexistent = deepcopy(canonical)
    nonexistent["root_evidence"][0] = "evidence:not-present"
    duplicate = deepcopy(canonical)
    duplicate["paths_to_alert"].append(duplicate["paths_to_alert"][0])
    reversed_rows = deepcopy(canonical)
    reversed_rows["root_evidence"].reverse()
    nonfinite = deepcopy(canonical)
    nonfinite["quality_limitations"][0] = float("nan")
    extra_key = deepcopy(canonical)
    extra_key["extra"] = []
    missing_key = deepcopy(canonical)
    del missing_key["possible_consequences"]
    return [
        nonexistent,
        duplicate,
        reversed_rows,
        None,
        nonfinite,
        extra_key,
        missing_key,
        [],
    ]


@pytest.mark.parametrize(
    "forged_index",
    _query_index_mutations(),
    ids=[
        "nonexistent-id",
        "duplicate-id",
        "reversed-order",
        "none",
        "nan",
        "extra-key",
        "missing-key",
        "not-a-dict",
    ],
)
def test_service_rejects_any_noncanonical_cached_query_index(forged_index) -> None:
    """Catches trust-boundary acceptance of malformed or forged cached indexes."""
    with pytest.raises(KnowledgeGraphError):
        GraphQueryService(replace(_result(), query_index=forged_index))


def test_service_does_not_consume_query_index_after_validation() -> None:
    """Catches query methods retaining the caller-owned query-index cache as truth."""
    result = _result()
    service = GraphQueryService(result)
    result.query_index["root_evidence"][0] = "evidence:not-present"
    result.query_index["paths_to_alert"].clear()

    assert service.root_evidence()[0]["node_id"] == result.root_evidence[0]
    assert [path["path_id"] for path in service.paths_to_alert()] == [
        "path:ag:20250407T101500:term_inversion:warningstate:warning_2",
        "path:ag:20250407T101500:atm_iv:warningstate:warning_2",
    ]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda result: replace(result, active_paths=(object(),)),
        lambda result: replace(result, explanation_sections=(object(),)),
    ],
    ids=["malformed-active-path", "malformed-explanation-section"],
)
def test_service_rejects_malformed_cached_records_with_a_graph_domain_error(
    mutation,
) -> None:
    """Catches malformed cached records leaking AttributeError past the trust boundary."""
    with pytest.raises(KnowledgeGraphError):
        GraphQueryService(mutation(_result()))


def test_public_query_api_has_only_the_six_preset_methods_and_no_question_input() -> None:
    """Catches accidental exposure of a free-form natural-language query surface."""
    public = {
        name: member
        for name, member in inspect.getmembers(GraphQueryService, inspect.isfunction)
        if not name.startswith("_")
    }

    assert set(public) == {
        "inspect_node",
        "paths_from_anomaly",
        "paths_to_alert",
        "possible_consequences",
        "quality_limitations",
        "root_evidence",
    }
    assert str(inspect.signature(public["root_evidence"])) == "(self, limit=3)"
    assert str(inspect.signature(public["inspect_node"])) == "(self, node_id)"
    assert str(inspect.signature(public["paths_from_anomaly"])) == "(self, anomaly_id)"
    assert all(
        parameter.name not in {"question", "query", "prompt", "text"}
        for method in public.values()
        for parameter in inspect.signature(method).parameters.values()
    )
````

</details>
