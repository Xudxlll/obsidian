---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py>)

SHA-256：`32c4429987d42bbf1d3b317c276f76df02943c433d699331993c9175b92bb4ea`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from graph_fixtures import (
    graph_and_paths,
    graph_context,
    make_agent_result,
    make_feature_evidence,
)
from option_risk import validation
from option_risk.agent import OptionRiskAgent
from option_risk.config import AgentConfig
from option_risk.contracts import (
    AgentResult,
    ExplanationSection,
    KnowledgeGraphResult,
    ProductOption,
    SurfacePayload,
    TriggerReason,
)
from option_risk.decision import DecisionPolicy
from option_risk.graph_explanation import (
    UnsafeGraphExplanationError,
    render_graph_explanation,
)
from option_risk.graph_queries import GraphQueryService
from option_risk.graph_reasoner import build_graph_result, discover_risk_paths
from option_risk.knowledge_graph import KnowledgeGraphError, build_knowledge_graph
from option_risk.knowledge_schema import FEATURE_RULES


SELECTED_PRODUCT = "ag"
SELECTED_TIME = pd.Timestamp("2025-04-07 10:15")


def _ready_agent_result(
    evidence,
    *,
    alert_level: int = 2,
    alert_name: str = "警告",
    transition_reason: str = "normal",
    risk_score: float | None = 0.5,
) -> AgentResult:
    evidence = list(evidence)
    context = graph_context(alert_level=alert_level, alert_name=alert_name)
    context["transition_reason"] = transition_reason
    context["risk_score"] = risk_score
    graph = build_knowledge_graph(
        **context,
        evidence=evidence,
        policy=DecisionPolicy(),
    )
    paths = discover_risk_paths(graph)
    sections, text, confidence = render_graph_explanation(graph, paths)
    present = {item.feature_name for item in evidence}
    missing = tuple(
        rule.feature_name for rule in FEATURE_RULES if rule.feature_name not in present
    )
    knowledge_graph = build_graph_result(
        graph,
        missing_evidence=missing,
        explanation_sections=sections,
        explanation_text=text,
        explanation_confidence=confidence,
    )
    # OptionRiskAgent publishes this registry order after the lower-level builder.
    knowledge_graph = replace(knowledge_graph, missing_evidence=missing)
    return replace(
        make_agent_result(knowledge_graph),
        alert_level=alert_level,
        alert_name=alert_name,
        risk_score=risk_score,
        feature_evidence=evidence,
        transition_reason=transition_reason,
    )


def test_single_result_validator_accepts_a_canonical_ready_level_two_graph() -> None:
    """Catches a validator that rejects the real Task 1-6 canonical result."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])

    summary = validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )

    assert summary == {
        "status": "ready",
        "product": "ag",
        "timestamp": "2025-04-07T10:15:00",
        "schema_version": "kg-schema-v1",
        "rule_version": "kg-rule-v1",
        "node_count": 8,
        "edge_count": 6,
        "active_path_count": 2,
        "alert_path_count": 1,
        "quality_path_count": 0,
        "missing_evidence_count": 11,
        "explanation_status": "canonical",
        "explanation_confidence": "normal",
        "query_record_counts": {
            "root_evidence": 1,
            "paths_to_alert": 1,
            "possible_consequences": 1,
            "quality_limitations": 0,
            "inspect_node": 8,
            "paths_from_anomaly": 2,
        },
    }


def test_single_result_validator_accepts_level_zero_with_no_active_path() -> None:
    """Catches formal acceptance inventing a path for sub-attention evidence."""
    result = _ready_agent_result(
        [make_feature_evidence("atm_iv", 0.5)],
        alert_level=0,
        alert_name="无预警",
    )

    summary = validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )

    assert result.knowledge_graph.active_paths == ()
    assert summary == {
        "status": "ready",
        "product": "ag",
        "timestamp": "2025-04-07T10:15:00",
        "schema_version": "kg-schema-v1",
        "rule_version": "kg-rule-v1",
        "node_count": 5,
        "edge_count": 2,
        "active_path_count": 0,
        "alert_path_count": 0,
        "quality_path_count": 0,
        "missing_evidence_count": 11,
        "explanation_status": "canonical",
        "explanation_confidence": "normal",
        "query_record_counts": {
            "root_evidence": 0,
            "paths_to_alert": 0,
            "possible_consequences": 0,
            "quality_limitations": 0,
            "inspect_node": 5,
            "paths_from_anomaly": 0,
        },
    }


def test_single_result_validator_accepts_watch_held_without_current_market_path() -> None:
    """Catches persistence-only level 1 being rejected for lacking a current path."""
    result = _ready_agent_result(
        [make_feature_evidence("atm_iv", 0.5)],
        alert_level=1,
        alert_name="关注",
        transition_reason="watch_held",
    )

    summary = validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )

    assert result.knowledge_graph.active_paths == ()
    assert "当前市场特征已回落" in result.knowledge_graph.explanation_text
    assert summary == {
        "status": "ready",
        "product": "ag",
        "timestamp": "2025-04-07T10:15:00",
        "schema_version": "kg-schema-v1",
        "rule_version": "kg-rule-v1",
        "node_count": 5,
        "edge_count": 2,
        "active_path_count": 0,
        "alert_path_count": 0,
        "quality_path_count": 0,
        "missing_evidence_count": 11,
        "explanation_status": "canonical",
        "explanation_confidence": "normal",
        "query_record_counts": {
            "root_evidence": 0,
            "paths_to_alert": 0,
            "possible_consequences": 0,
            "quality_limitations": 0,
            "inspect_node": 5,
            "paths_from_anomaly": 0,
        },
    }


def test_single_result_validator_accepts_quality_only_path_as_limited_confidence() -> None:
    """Catches a quality limitation being rejected or promoted to market alert."""
    result = _ready_agent_result(
        [make_feature_evidence("coverage_shortfall", 1.4)],
        alert_level=0,
        alert_name="无预警",
    )

    summary = validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )

    assert all(
        path.conclusion_node_id.startswith("confidence:")
        for path in result.knowledge_graph.active_paths
    )
    assert summary == {
        "status": "ready",
        "product": "ag",
        "timestamp": "2025-04-07T10:15:00",
        "schema_version": "kg-schema-v1",
        "rule_version": "kg-rule-v1",
        "node_count": 7,
        "edge_count": 5,
        "active_path_count": 1,
        "alert_path_count": 0,
        "quality_path_count": 1,
        "missing_evidence_count": 11,
        "explanation_status": "canonical",
        "explanation_confidence": "limited",
        "query_record_counts": {
            "root_evidence": 1,
            "paths_to_alert": 0,
            "possible_consequences": 0,
            "quality_limitations": 1,
            "inspect_node": 7,
            "paths_from_anomaly": 1,
        },
    }


def test_single_result_validator_rejects_an_unavailable_graph() -> None:
    """Catches formal acceptance silently passing local graph degradation."""
    graph = KnowledgeGraphResult.unavailable(
        product=SELECTED_PRODUCT,
        timestamp=SELECTED_TIME,
        error_type="RuntimeError",
        error_message="synthetic unavailable graph",
    )
    result = make_agent_result(graph)

    with pytest.raises(AssertionError, match="unavailable"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("error_type", "RuntimeError"),
        ("error_message", "latent ready-result error"),
        ("error_type", object()),
        ("error_message", object()),
    ],
    ids=[
        "string-error-type",
        "string-error-message",
        "object-error-type",
        "object-error-message",
    ],
)
def test_single_result_validator_rejects_ready_graph_with_any_error_payload(
    field_name: str,
    invalid_value,
) -> None:
    """Catches ready envelopes retaining latent or non-JSON error objects."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])

    with pytest.raises(AssertionError, match="error|错误|ready|JSON"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, **{field_name: invalid_value}),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    ("invalid_level", "canonical_level", "alert_name", "pressure"),
    [
        (False, 0, "无预警", 0.5),
        (True, 1, "关注", 1.15),
        (2.0, 2, "警告", 1.15),
        (np.int64(2), 2, "警告", 1.15),
    ],
    ids=["false", "true", "float", "numpy-int"],
)
def test_single_result_validator_rejects_non_builtin_integer_warning_level(
    invalid_level,
    canonical_level: int,
    alert_name: str,
    pressure: float,
) -> None:
    """Catches equality-compatible bool/float/numpy WarningState levels."""
    result = _ready_agent_result(
        [make_feature_evidence("atm_iv", pressure)],
        alert_level=canonical_level,
        alert_name=alert_name,
    )

    with pytest.raises(AssertionError, match="alert_level|预警等级|Warning|整数|类型"):
        validation.validate_knowledge_graph_result(
            replace(result, alert_level=invalid_level),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    "invalid_emitted",
    [0, np.bool_(False)],
    ids=["integer-zero", "numpy-bool"],
)
def test_single_result_validator_rejects_non_builtin_warning_boolean(
    invalid_emitted,
) -> None:
    """Catches equality-compatible integers/numpy booleans in WarningState."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])

    with pytest.raises(AssertionError, match="alert_emitted|通知|Warning|布尔|类型"):
        validation.validate_knowledge_graph_result(
            replace(result, alert_emitted=invalid_emitted),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    ("invalid_score", "graph_score"),
    [
        (True, None),
        (1, 1.0),
        (np.float64(0.5), 0.5),
        (np.int64(1), 1.0),
        ("0.5", None),
        (object(), None),
        (float("nan"), None),
        (float("inf"), None),
        (float("-inf"), None),
    ],
    ids=[
        "boolean",
        "builtin-integer",
        "numpy-float",
        "numpy-int",
        "string",
        "object",
        "nan",
        "positive-infinity",
        "negative-infinity",
    ],
)
def test_single_result_validator_rejects_non_builtin_or_nonfinite_warning_score(
    invalid_score,
    graph_score: float | None,
) -> None:
    """Catches malformed outer scores collapsing to a legal graph None/number."""
    result = _ready_agent_result(
        [make_feature_evidence("atm_iv", 1.15)],
        risk_score=graph_score,
    )

    with pytest.raises(AssertionError, match="risk_score|风险分|Warning|有限|数值|类型"):
        validation.validate_knowledge_graph_result(
            replace(result, risk_score=invalid_score),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_accepts_none_for_feature_numbers() -> None:
    """Locks legal nulls for all four FeatureEvidence numeric fields."""
    evidence = replace(
        make_feature_evidence("atm_iv", None),
        reference_value=None,
        pressure_ratio=None,
        change_rate=None,
    )
    result = _ready_agent_result(
        [evidence],
        alert_level=0,
        alert_name="无预警",
    )

    summary = validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )

    assert summary["status"] == "ready"
    assert summary["active_path_count"] == 0


@pytest.mark.parametrize(
    "field_name",
    ["current_value", "reference_value", "pressure_ratio", "change_rate"],
)
@pytest.mark.parametrize(
    "invalid_value",
    [object(), "not-a-number", False, float("nan"), float("inf")],
    ids=["object", "string", "boolean", "nan", "infinity"],
)
def test_single_result_validator_rejects_invalid_feature_number(
    field_name: str,
    invalid_value,
) -> None:
    """Catches invalid optional Evidence values being collapsed to graph None."""
    evidence = replace(
        make_feature_evidence("atm_iv", None),
        reference_value=None,
        pressure_ratio=None,
        change_rate=None,
    )
    result = _ready_agent_result(
        [evidence],
        alert_level=0,
        alert_name="无预警",
    )
    forged = replace(evidence, **{field_name: invalid_value})

    with pytest.raises(AssertionError, match="Evidence|证据|JSON|有限|数值|类型"):
        validation.validate_knowledge_graph_result(
            replace(result, feature_evidence=[forged]),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    "field_name",
    ["current_value", "reference_value", "pressure_ratio", "change_rate"],
)
@pytest.mark.parametrize(
    "invalid_value",
    [1, np.float64(1.0)],
    ids=["integer-for-canonical-float", "numpy-float"],
)
def test_single_result_validator_rejects_feature_number_type_drift(
    field_name: str,
    invalid_value,
) -> None:
    """Catches equality-compatible non-canonical FeatureEvidence scalars."""
    evidence = replace(
        make_feature_evidence("atm_iv", 1.0),
        current_value=1.0,
        reference_value=1.0,
        pressure_ratio=1.0,
        change_rate=1.0,
    )
    result = _ready_agent_result([evidence])
    forged = replace(evidence, **{field_name: invalid_value})

    with pytest.raises(AssertionError, match="Evidence|证据|JSON|有限|数值|类型"):
        validation.validate_knowledge_graph_result(
            replace(result, feature_evidence=[forged]),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


class _StringSubclass(str):
    """Equality-compatible non-canonical JSON string scalar."""


class _ExplanationSectionSubclass(ExplanationSection):
    """Constructible non-exact section type with the canonical fields."""


@pytest.mark.parametrize(
    "field_name",
    ["group", "feature_name", "label", "status"],
)
def test_single_result_validator_rejects_feature_string_subclass(
    field_name: str,
) -> None:
    """Catches a validator auditing only FeatureEvidence numeric fields."""
    evidence = make_feature_evidence("atm_iv", 1.15)
    result = _ready_agent_result([evidence])
    forged = replace(evidence, **{field_name: _StringSubclass(getattr(evidence, field_name))})

    with pytest.raises(AssertionError, match="Evidence|证据|JSON|字符串|类型"):
        validation.validate_knowledge_graph_result(
            replace(result, feature_evidence=[forged]),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_active_path_numeric_type_drift() -> None:
    """Catches canonical float 1.0 being accepted as integer 1 in a RiskPath."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.0)])
    paths = list(result.knowledge_graph.active_paths)
    assert type(paths[0].pressure_ratio) is float and paths[0].pressure_ratio == 1.0
    paths[0] = replace(paths[0], pressure_ratio=1)

    with pytest.raises(AssertionError, match="path|路径|类型|规范"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, active_paths=tuple(paths)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "active_paths",
        "root_evidence",
        "possible_consequences",
        "missing_evidence",
    ],
)
def test_single_result_validator_rejects_list_for_canonical_tuple_field(
    field_name: str,
) -> None:
    """Catches tuple(list_value) comparisons hiding public container drift."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    canonical_value = getattr(result.knowledge_graph, field_name)

    with pytest.raises(AssertionError, match="tuple|元组|类型|规范|路径|索引|missing"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, **{field_name: list(canonical_value)}),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    "field_name",
    ["root_evidence", "possible_consequences", "missing_evidence"],
)
def test_single_result_validator_rejects_string_subclass_in_id_tuple(
    field_name: str,
) -> None:
    """Catches equality-compatible non-builtin IDs in canonical tuple indexes."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    canonical_value = getattr(result.knowledge_graph, field_name)
    assert canonical_value
    forged = (
        _StringSubclass(canonical_value[0]),
        *canonical_value[1:],
    )

    with pytest.raises(AssertionError, match="ID|标识|字符串|类型|索引|missing"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, **{field_name: forged}),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    "path_field",
    [
        "path_id",
        "evidence_node_id",
        "anomaly_node_id",
        "mechanism_node_id",
        "conclusion_node_id",
    ],
)
def test_single_result_validator_rejects_string_subclass_for_active_path_id(
    path_field: str,
) -> None:
    """Catches dataclass equality hiding a non-builtin canonical path ID."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    paths = list(result.knowledge_graph.active_paths)
    paths[0] = replace(
        paths[0],
        **{path_field: _StringSubclass(getattr(paths[0], path_field))},
    )

    with pytest.raises(AssertionError, match="path|路径|ID|标识|字符串|类型"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, active_paths=tuple(paths)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_evidence_from_after_the_selected_time() -> None:
    """Catches future Evidence source time entering formal acceptance."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    payload = deepcopy(result.knowledge_graph.graph_json)
    evidence = next(row for row in payload["nodes"] if row["node_type"] == "Evidence")
    evidence["source_timestamp"] = "2025-04-07T10:15:01"
    tampered_graph = replace(result.knowledge_graph, graph_json=payload)

    with pytest.raises(AssertionError, match="Evidence|未来|时间"):
        validation.validate_knowledge_graph_result(
            replace(result, knowledge_graph=tampered_graph),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_level_two_without_a_market_alert_path() -> None:
    """Catches a formal level-2 warning unsupported by any current market path."""
    result = _ready_agent_result(
        [make_feature_evidence("atm_iv", 0.5)],
        alert_level=2,
        alert_name="警告",
    )

    assert result.knowledge_graph.active_path_count == 0
    with pytest.raises(AssertionError, match="市场|预警路径|alert"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def _replace_graph_result(result: AgentResult, **changes) -> AgentResult:
    assert result.knowledge_graph is not None
    return replace(
        result,
        knowledge_graph=replace(result.knowledge_graph, **changes),
    )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda result: _replace_graph_result(
                result,
                schema_version="kg-schema-v0",
            ),
            "schema",
        ),
        (
            lambda result: _replace_graph_result(
                result,
                rule_version="kg-rule-v0",
            ),
            "rule",
        ),
        (lambda result: replace(result, product="au"), "品种|product"),
        (
            lambda result: _replace_graph_result(result, product="au"),
            "品种|product",
        ),
        (
            lambda result: replace(
                result,
                timestamp=SELECTED_TIME + pd.Timedelta(minutes=1),
            ),
            "时间|timestamp",
        ),
        (
            lambda result: _replace_graph_result(
                result,
                timestamp=SELECTED_TIME + pd.Timedelta(minutes=1),
            ),
            "时间|timestamp",
        ),
    ],
    ids=[
        "stale-schema-envelope",
        "stale-rule-envelope",
        "outer-product-mismatch",
        "graph-result-product-mismatch",
        "outer-timestamp-mismatch",
        "graph-result-timestamp-mismatch",
    ],
)
def test_single_result_validator_rejects_version_or_identity_drift(
    mutation,
    message: str,
) -> None:
    """Catches stale versions or cross-envelope product/time identity drift."""
    result = mutation(
        _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    )

    with pytest.raises(AssertionError, match=message):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    "count_field",
    ["node_count", "edge_count", "active_path_count"],
    ids=["node-count", "edge-count", "path-count"],
)
def test_single_result_validator_rejects_cached_structure_count_drift(
    count_field: str,
) -> None:
    """Catches cached node, edge, or path counts replacing recomputed truth."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    graph_result = result.knowledge_graph
    forged_count = getattr(graph_result, count_field) + 1

    with pytest.raises(AssertionError, match="数量|count"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, **{count_field: forged_count}),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_noncanonical_active_path_order() -> None:
    """Catches caller-controlled path ordering replacing deterministic ranking."""
    result = _ready_agent_result(
        [
            make_feature_evidence("atm_iv", 1.15),
            make_feature_evidence("gamma_hhi", 1.25),
        ]
    )
    reversed_paths = tuple(reversed(result.knowledge_graph.active_paths))

    with pytest.raises(AssertionError, match="路径|path"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, active_paths=reversed_paths),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_root_and_consequence_cache_drift() -> None:
    """Catches cached root/consequence indexes diverging from canonical paths."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])

    with pytest.raises(AssertionError, match="根因|后果|root|consequence"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(
                result,
                root_evidence=(),
                possible_consequences=(),
            ),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_query_index_drift_from_the_graph() -> None:
    """Catches UI/query caches suppressing a real alert path."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    forged_index = deepcopy(result.knowledge_graph.query_index)
    forged_index["paths_to_alert"] = []

    with pytest.raises(AssertionError, match="查询|query"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, query_index=forged_index),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def _tamper_explanation_content(result: AgentResult) -> AgentResult:
    sections = list(result.knowledge_graph.explanation_sections)
    sections[0] = replace(sections[0], content=sections[0].content + "篡改")
    return _replace_graph_result(result, explanation_sections=tuple(sections))


@pytest.mark.parametrize(
    "mutation",
    [
        _tamper_explanation_content,
        lambda result: _replace_graph_result(
            result,
            explanation_sections=tuple(
                reversed(result.knowledge_graph.explanation_sections)
            ),
        ),
        lambda result: _replace_graph_result(
            result,
            explanation_text=result.knowledge_graph.explanation_text + "篡改",
        ),
        lambda result: _replace_graph_result(
            result,
            explanation_confidence="limited",
        ),
    ],
    ids=["section-content", "section-order", "full-text", "confidence"],
)
def test_single_result_validator_rejects_noncanonical_explanation(mutation) -> None:
    """Catches stored prose or confidence replacing a fresh canonical rendering."""
    result = mutation(
        _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    )

    with pytest.raises(AssertionError, match="解释|explanation|confidence"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_review_r3_accepts_exact_canonical_explanation_sections() -> None:
    """Locks the exact section and nested scalar/container representation."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    sections = result.knowledge_graph.explanation_sections

    assert type(sections) is tuple and sections
    assert all(type(section) is ExplanationSection for section in sections)
    for section in sections:
        assert type(section.section_id) is str
        assert type(section.title) is str
        assert type(section.content) is str
        assert type(section.path_ids) is tuple
        assert all(type(path_id) is str for path_id in section.path_ids)

    summary = validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )
    assert summary["explanation_status"] == "canonical"


@pytest.mark.parametrize(
    "field_name",
    ["section_id", "title", "content"],
    ids=["section-id", "title", "content"],
)
def test_review_r3_rejects_explanation_string_subclass(field_name: str) -> None:
    """Catches equality-compatible string subclasses in explanation fields."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    sections = list(result.knowledge_graph.explanation_sections)
    sections[0] = replace(
        sections[0],
        **{field_name: _StringSubclass(getattr(sections[0], field_name))},
    )

    with pytest.raises(AssertionError, match="解释|explanation|section|字符串|类型|规范"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, explanation_sections=tuple(sections)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_review_r3_rejects_explanation_path_id_string_subclass() -> None:
    """Catches equality-compatible string subclasses nested in path_ids."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    sections = list(result.knowledge_graph.explanation_sections)
    index = next(
        index for index, section in enumerate(sections) if section.path_ids
    )
    section = sections[index]
    sections[index] = replace(
        section,
        path_ids=(
            _StringSubclass(section.path_ids[0]),
            *section.path_ids[1:],
        ),
    )

    with pytest.raises(AssertionError, match="解释|explanation|path_ids|路径|字符串|类型"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, explanation_sections=tuple(sections)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_review_r3_rejects_explanation_list_for_path_ids_tuple() -> None:
    """Catches a constructible list replacing the canonical path_ids tuple."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    sections = list(result.knowledge_graph.explanation_sections)
    index = next(
        index for index, section in enumerate(sections) if section.path_ids
    )
    sections[index] = replace(
        sections[index],
        path_ids=list(sections[index].path_ids),
    )

    with pytest.raises(AssertionError, match="解释|explanation|path_ids|元组|tuple|类型"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, explanation_sections=tuple(sections)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_review_r3_rejects_explanation_section_subclass() -> None:
    """Catches an ExplanationSection subclass crossing the formal boundary."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    sections = list(result.knowledge_graph.explanation_sections)
    section = sections[0]
    sections[0] = _ExplanationSectionSubclass(
        section_id=section.section_id,
        title=section.title,
        content=section.content,
        path_ids=section.path_ids,
    )
    assert type(sections[0]) is _ExplanationSectionSubclass

    with pytest.raises(AssertionError, match="解释|explanation|section|类型|规范"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, explanation_sections=tuple(sections)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize("mutation", ["fabricated", "reordered"])
def test_single_result_validator_rejects_wrong_feature_rules_missing_evidence(
    mutation: str,
) -> None:
    """Catches missing-evidence membership or FEATURE_RULES ordering drift."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    assert result.knowledge_graph.missing_evidence == (
        "atm_iv_chg_4",
        "term_inversion",
        "convexity_violation_ratio",
        "max_local_iv_jump",
        "put_call_parity_p95_error",
        "calendar_variance_violation_ratio",
        "gamma_hhi",
        "vega_hhi",
        "zero_volume_share",
        "iv_floor_share",
        "coverage_shortfall",
    )
    forged_missing = (
        ("atm_iv", *result.knowledge_graph.missing_evidence)
        if mutation == "fabricated"
        else tuple(reversed(result.knowledge_graph.missing_evidence))
    )

    with pytest.raises(AssertionError, match="缺失|missing"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, missing_evidence=forged_missing),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("alert_level", 3),
        ("alert_name", "危险"),
        ("risk_score", 0.6),
        ("alert_emitted", True),
        ("transition_reason", "warning_started"),
        ("policy_version", "legacy-policy-v0"),
        ("policy_parameter_hash", "forged-hash"),
    ],
    ids=[
        "level",
        "name",
        "score",
        "emission",
        "transition",
        "policy-version",
        "policy-hash",
    ],
)
def test_single_result_validator_rejects_warning_cross_layer_drift(
    field: str,
    value,
) -> None:
    """Catches Problem 1 Warning fields disagreeing with WarningState."""
    result = replace(
        _ready_agent_result([make_feature_evidence("atm_iv", 1.15)]),
        **{field: value},
    )

    with pytest.raises(AssertionError, match="Warning|预警|策略|迁移|risk"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_review_r3_rejects_warning_graph_integer_for_outer_float_risk_score() -> None:
    """Catches JSON integer 1 comparing equal to canonical outer float 1.0."""
    result = _ready_agent_result(
        [make_feature_evidence("atm_iv", 1.15)],
        risk_score=1.0,
    )
    assert type(result.risk_score) is float and result.risk_score == 1.0
    graph_json = deepcopy(result.knowledge_graph.graph_json)
    warning = next(
        row for row in graph_json["nodes"] if row["node_type"] == "WarningState"
    )
    assert type(warning["risk_score"]) is float and warning["risk_score"] == 1.0
    warning["risk_score"] = 1

    with pytest.raises(AssertionError, match="Warning|risk_score|预警|类型|规范"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, graph_json=graph_json),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("current_value", 0.21),
        ("reference_value", 0.18),
        ("pressure_ratio", 1.16),
        ("status", "危险"),
    ],
    ids=["current-value", "reference-value", "pressure", "status"],
)
def test_single_result_validator_rejects_evidence_cross_layer_drift(
    field: str,
    value,
) -> None:
    """Catches graph Evidence values diverging from Problem 1 evidence."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    forged_evidence = [replace(result.feature_evidence[0], **{field: value})]

    with pytest.raises(AssertionError, match="Evidence|证据"):
        validation.validate_knowledge_graph_result(
            replace(result, feature_evidence=forged_evidence),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_fabricated_graph_evidence() -> None:
    """Catches graph Evidence being invented for a feature absent from Problem 1."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])

    with pytest.raises(AssertionError, match="Evidence|证据|缺失"):
        validation.validate_knowledge_graph_result(
            replace(result, feature_evidence=[]),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("price_source", "real_futures"),
        ("data_quality", {"clean_rate": 0.5}),
    ],
    ids=["price-source", "data-quality"],
)
def test_single_result_validator_rejects_snapshot_cross_layer_drift(
    field: str,
    value,
) -> None:
    """Catches RiskSnapshot provenance disagreeing with Problem 1."""
    result = replace(
        _ready_agent_result([make_feature_evidence("atm_iv", 1.15)]),
        **{field: value},
    )

    with pytest.raises(AssertionError, match="RiskSnapshot|快照|质量|价格"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def _tamper_node_time(result: AgentResult, node_type: str, timestamp: str) -> AgentResult:
    payload = deepcopy(result.knowledge_graph.graph_json)
    node = next(row for row in payload["nodes"] if row["node_type"] == node_type)
    node["source_timestamp"] = timestamp
    return _replace_graph_result(result, graph_json=payload)


def _tamper_edge_time(result: AgentResult, timestamp: str) -> AgentResult:
    payload = deepcopy(result.knowledge_graph.graph_json)
    payload["edges"][0]["source_timestamp"] = timestamp
    return _replace_graph_result(result, graph_json=payload)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda result: _tamper_node_time(
            result,
            "Anomaly",
            "2025-04-07T10:15:01",
        ),
        lambda result: _tamper_edge_time(result, "2025-04-07T10:15:01"),
        lambda result: _replace_graph_result(
            result,
            active_paths=(
                replace(
                    result.knowledge_graph.active_paths[0],
                    timestamp=SELECTED_TIME + pd.Timedelta(seconds=1),
                ),
                *result.knowledge_graph.active_paths[1:],
            ),
        ),
        lambda result: _tamper_node_time(
            result,
            "Evidence",
            "2025-04-07T10:14:59",
        ),
    ],
    ids=["future-node", "future-edge", "future-path", "earlier-evidence"],
)
def test_single_result_validator_rejects_temporal_leakage_or_stale_evidence(
    mutation,
) -> None:
    """Catches future graph data and non-event-time Evidence provenance."""
    result = mutation(
        _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    )

    with pytest.raises(AssertionError, match="时间|未来|Evidence|path"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def _inject_graph_object(result: AgentResult) -> AgentResult:
    payload = deepcopy(result.knowledge_graph.graph_json)
    snapshot = next(row for row in payload["nodes"] if row["node_type"] == "RiskSnapshot")
    snapshot["data_quality"]["nonserializable"] = object()
    return _replace_graph_result(result, graph_json=payload)


def _inject_path_nan(result: AgentResult) -> AgentResult:
    paths = list(result.knowledge_graph.active_paths)
    paths[0] = replace(paths[0], pressure_ratio=float("nan"))
    return _replace_graph_result(result, active_paths=tuple(paths))


@pytest.mark.parametrize(
    "mutation",
    [
        _inject_graph_object,
        _inject_path_nan,
        lambda result: _replace_graph_result(
            result,
            explanation_text=float("nan"),
        ),
        lambda result: _replace_graph_result(
            result,
            query_index={"nonserializable": object()},
        ),
    ],
    ids=["graph-object", "path-nan", "explanation-nan", "query-object"],
)
def test_single_result_validator_rejects_non_strict_json_payloads(mutation) -> None:
    """Catches NaN or default-based serialization hiding invalid graph payloads."""
    result = mutation(
        _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    )

    with pytest.raises(AssertionError, match="JSON|序列|有限|NaN"):
        validation.validate_knowledge_graph_result(
            result,
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_rejects_a_quality_path_reaching_warning_state() -> None:
    """Catches quality limitations being forged into market-alert support."""
    result = _ready_agent_result(
        [make_feature_evidence("coverage_shortfall", 1.4)],
        alert_level=0,
        alert_name="无预警",
    )
    path = result.knowledge_graph.active_paths[0]
    warning_id = next(
        row["node_id"]
        for row in result.knowledge_graph.graph_json["nodes"]
        if row["node_type"] == "WarningState"
    )
    forged = replace(
        path,
        conclusion_node_id=warning_id,
        relation_semantics=(*path.relation_semantics[:-1], "SUPPORTS"),
    )

    with pytest.raises(AssertionError, match="质量|quality|Warning"):
        validation.validate_knowledge_graph_result(
            _replace_graph_result(result, active_paths=(forged,)),
            SELECTED_PRODUCT,
            SELECTED_TIME,
        )


def test_single_result_validator_does_not_mutate_the_agent_result() -> None:
    """Catches validation normalizing caller-owned graph or query state in place."""
    result = _ready_agent_result([make_feature_evidence("atm_iv", 1.15)])
    before = deepcopy(result.to_dict())

    validation.validate_knowledge_graph_result(
        result,
        SELECTED_PRODUCT,
        SELECTED_TIME,
    )

    assert result.to_dict() == before


def _complete_ready_result(product: str, timestamp: pd.Timestamp) -> AgentResult:
    timestamp = pd.Timestamp(timestamp)
    policy = DecisionPolicy()
    evidence = [
        make_feature_evidence("atm_iv", 1.15),
        make_feature_evidence("term_inversion", 0.5),
        make_feature_evidence("convexity_violation_ratio", 0.5),
        make_feature_evidence("gamma_hhi", 0.5),
        make_feature_evidence("coverage_shortfall", 0.5),
    ]
    data_quality = {"clean_rate": 1.0}
    graph = build_knowledge_graph(
        product=product,
        timestamp=timestamp,
        evidence=evidence,
        alert_level=2,
        alert_name="警告",
        risk_score=0.5,
        alert_emitted=False,
        transition_reason="normal",
        policy_version=policy.policy_version,
        policy_parameter_hash=policy.parameter_hash,
        data_quality=data_quality,
        price_source="reconstructed_proxy",
        policy=policy,
    )
    paths = discover_risk_paths(graph)
    sections, text, confidence = render_graph_explanation(graph, paths)
    present = {row.feature_name for row in evidence}
    missing = tuple(
        rule.feature_name for rule in FEATURE_RULES if rule.feature_name not in present
    )
    graph_result = build_graph_result(
        graph,
        missing_evidence=missing,
        explanation_sections=sections,
        explanation_text=text,
        explanation_confidence=confidence,
    )
    graph_result = replace(graph_result, missing_evidence=missing)
    surfaces = {
        metric: SurfacePayload(
            metric=metric,
            timestamp=timestamp,
            log_moneyness=np.array([-0.1, 0.0, 0.1]),
            time_to_expiry=np.array([20 / 365, 50 / 365]),
            values=np.ones((2, 3)),
        )
        for metric in ["iv", "delta", "gamma", "vega", "theta"]
    }
    timeline = pd.DataFrame(
        {
            "alert_level": [2],
            "alert_emitted": [False],
            "policy_version": [policy.policy_version],
            "policy_parameter_hash": [policy.parameter_hash],
            "transition_reason": ["normal"],
        },
        index=pd.DatetimeIndex([timestamp], name="datetime"),
    )
    return AgentResult(
        product=product,
        timestamp=timestamp,
        status="ready",
        alert_level=2,
        alert_name="警告",
        alert_emitted=False,
        risk_score=0.5,
        price_source="reconstructed_proxy",
        data_quality=data_quality,
        surfaces=surfaces,
        feature_evidence=evidence,
        trigger_reasons=[
            TriggerReason(
                feature_name="atm_iv",
                label="ATM隐含波动率",
                current_value=0.2,
                reference_value=0.2 / 1.15,
                pressure_ratio=1.15,
                change_direction="上升",
                severity=2,
                message="ATM隐含波动率超过自身动态阈值。",
            )
        ],
        timeline=timeline,
        evaluation=None,
        policy_version=policy.policy_version,
        policy_parameter_hash=policy.parameter_hash,
        transition_reason="normal",
        knowledge_graph=graph_result,
    )


class _RecordingCatalogAgent:
    def __init__(
        self,
        results: dict[str, AgentResult],
        timestamps: dict[str, pd.DatetimeIndex],
        *,
        catalog_order: list[str] | None = None,
    ) -> None:
        self.results = results
        self.timestamps = timestamps
        self.catalog_order = list(catalog_order or results)
        self.list_products_calls = 0
        self.list_timestamp_calls: list[str] = []
        self.analyze_calls: list[tuple[str, pd.Timestamp]] = []

    def list_products(self):
        self.list_products_calls += 1
        return [ProductOption(code=code, label=code.upper()) for code in self.catalog_order]

    def list_timestamps(self, product: str):
        self.list_timestamp_calls.append(product)
        return self.timestamps[product]

    def analyze(self, product: str, timestamp: pd.Timestamp):
        selected = pd.Timestamp(timestamp)
        self.analyze_calls.append((product, selected))
        if selected != self.timestamps[product][-1]:
            raise AssertionError("deployment did not select the exact last timestamp")
        return self.results[product]


def _expected_problem_one_analysis(product: str, timestamp: pd.Timestamp) -> dict:
    return {
        "product": product,
        "timestamp": pd.Timestamp(timestamp).isoformat(),
        "status": "ready",
        "alert_level": 2,
        "alert_name": "警告",
        "alert_emitted": False,
        "surface_metrics": ["delta", "gamma", "iv", "theta", "vega"],
        "feature_groups": [
            "Greeks集中风险",
            "无套利风险",
            "曲面水平与形态",
            "期限结构",
            "质量与流动性",
        ],
        "evidence_count": 5,
        "reason_count": 1,
        "timeline_rows": 1,
        "price_source": "reconstructed_proxy",
        "evaluation_available": False,
        "policy_version": "validated-dynamic-state-v2",
        "policy_parameter_hash": DecisionPolicy().parameter_hash,
        "transition_reason": "normal",
    }


def _expected_graph_analysis(product: str, timestamp: pd.Timestamp) -> dict:
    return {
        "status": "ready",
        "product": product,
        "timestamp": pd.Timestamp(timestamp).isoformat(),
        "schema_version": "kg-schema-v1",
        "rule_version": "kg-rule-v1",
        "node_count": 12,
        "edge_count": 10,
        "active_path_count": 2,
        "alert_path_count": 1,
        "quality_path_count": 0,
        "missing_evidence_count": 7,
        "explanation_status": "canonical",
        "explanation_confidence": "normal",
        "query_record_counts": {
            "root_evidence": 1,
            "paths_to_alert": 1,
            "possible_consequences": 1,
            "quality_limitations": 0,
            "inspect_node": 12,
            "paths_from_anomaly": 2,
        },
    }


def _assert_executed_global_checks(report: dict, product_count: int) -> None:
    checks = report["global_checks"]
    assert set(checks) == {"deterministic", "no_future", "content_safety"}
    for name in checks:
        assert set(checks[name]) == {"passed", "checked_count", "scope"}
        assert checks[name]["passed"] is True
        assert type(checks[name]["checked_count"]) is int
        assert isinstance(checks[name]["scope"], str) and checks[name]["scope"].strip()
    assert checks["deterministic"]["checked_count"] == product_count
    assert "重复" in checks["deterministic"]["scope"]
    assert checks["no_future"]["checked_count"] >= product_count + 1
    assert "未来" in checks["no_future"]["scope"] and "追加" in checks["no_future"]["scope"]
    assert checks["content_safety"]["checked_count"] >= product_count + 2
    assert "解释" in checks["content_safety"]["scope"] and "安全" in checks["content_safety"]["scope"]


def _assert_incomplete_global_checks(report: dict, successful_graph_count: int) -> None:
    checks = report["global_checks"]
    assert set(checks) == {"deterministic", "no_future", "content_safety"}
    for name in checks:
        assert set(checks[name]) == {"passed", "checked_count", "scope"}
        assert type(checks[name]["passed"]) is bool
        assert type(checks[name]["checked_count"]) is int
        assert isinstance(checks[name]["scope"], str) and checks[name]["scope"].strip()
        assert str(successful_graph_count) in checks[name]["scope"]
    assert not all(check["passed"] for check in checks.values())
    assert checks["deterministic"]["checked_count"] == successful_graph_count
    assert checks["no_future"]["checked_count"] >= successful_graph_count + 1
    assert checks["content_safety"]["checked_count"] >= successful_graph_count + 2


def test_graph_deployment_sorts_two_products_and_validates_each_exact_last_once() -> None:
    """Catches unsorted, repeated, partial, or fabricated deployment validation."""
    timestamps = {
        "ag": pd.DatetimeIndex(["2025-04-07 10:00", "2025-04-07 10:15"]),
        "cu": pd.DatetimeIndex(["2025-05-08 14:45", "2025-05-08 15:00"]),
    }
    results = {
        product: _complete_ready_result(product, rows[-1])
        for product, rows in timestamps.items()
    }
    agent = _RecordingCatalogAgent(results, timestamps, catalog_order=["cu", "ag"])
    requested = ["cu", "ag"]
    before_requested = list(requested)
    before_results = {product: deepcopy(result.to_dict()) for product, result in results.items()}
    progress: list[str] = []

    report = validation.validate_knowledge_graph_deployment(
        agent,
        product_codes=requested,
        progress=progress.append,
    )

    assert requested == before_requested
    assert [row["product"] for row in report["products"]] == ["ag", "cu"]
    assert agent.list_products_calls == 1
    assert agent.list_timestamp_calls == ["ag", "cu"]
    assert agent.analyze_calls == [
        ("ag", timestamps["ag"][-1]),
        ("cu", timestamps["cu"][-1]),
    ]
    assert progress == ["[1/2] ag: passed", "[2/2] cu: passed"]
    for row in report["products"]:
        product = row["product"]
        selected = timestamps[product][-1]
        assert row == {
            "product": product,
            "status": "passed",
            "timestamp_count": 2,
            "first_timestamp": timestamps[product][0].isoformat(),
            "last_timestamp": selected.isoformat(),
            "analysis": _expected_problem_one_analysis(product, selected),
            "knowledge_graph": _expected_graph_analysis(product, selected),
        }
    assert report["mode"] == "full"
    assert report["public_agent_surface"] == {
        "agent_classes": ["OptionRiskAgent"],
        "passed": True,
    }
    assert report["summary"] == {
        "status": "passed",
        "product_count": 2,
        "passed_products": 2,
        "failed_products": 0,
    }
    assert report["summary"]["passed_products"] == sum(
        row["status"] == "passed" for row in report["products"]
    )
    _assert_executed_global_checks(report, 2)
    assert {
        product: result.to_dict() for product, result in results.items()
    } == before_results


def test_graph_deployment_preserves_problem_one_and_continues_after_graph_failure() -> None:
    """Catches one graph failure erasing Problem 1 or stopping later products."""
    timestamps = {
        "ag": pd.DatetimeIndex(["2025-04-07 10:00", "2025-04-07 10:15"]),
        "cu": pd.DatetimeIndex(["2025-05-08 14:45", "2025-05-08 15:00"]),
        "zn": pd.DatetimeIndex(["2025-06-09 09:45", "2025-06-09 10:00"]),
    }
    results = {
        product: _complete_ready_result(product, rows[-1])
        for product, rows in timestamps.items()
    }
    results["cu"] = replace(
        results["cu"],
        knowledge_graph=KnowledgeGraphResult.unavailable(
            product="cu",
            timestamp=timestamps["cu"][-1],
            error_type="RuntimeError",
            error_message="synthetic graph outage",
        ),
    )
    agent = _RecordingCatalogAgent(results, timestamps, catalog_order=["zn", "cu", "ag"])
    progress: list[str] = []

    report = validation.validate_knowledge_graph_deployment(
        agent,
        product_codes=["zn", "cu", "ag"],
        progress=progress.append,
    )

    assert [row["product"] for row in report["products"]] == ["ag", "cu", "zn"]
    assert agent.list_timestamp_calls == ["ag", "cu", "zn"]
    assert agent.analyze_calls == [
        ("ag", timestamps["ag"][-1]),
        ("cu", timestamps["cu"][-1]),
        ("zn", timestamps["zn"][-1]),
    ]
    failed = report["products"][1]
    assert failed["analysis"] == _expected_problem_one_analysis(
        "cu", timestamps["cu"][-1]
    )
    assert failed["knowledge_graph"] == {
        "status": "failed",
        "error_type": "AssertionError",
        "error": "知识图谱状态不是ready：unavailable",
    }
    assert failed["status"] == "failed"
    assert failed["error_type"] == "AssertionError"
    assert failed["error"] == "知识图谱状态不是ready：unavailable"
    assert report["products"][2]["status"] == "passed"
    assert report["summary"] == {
        "status": "failed",
        "product_count": 3,
        "passed_products": 2,
        "failed_products": 1,
    }
    assert progress == [
        "[1/3] ag: passed",
        "[2/3] cu: failed - 知识图谱状态不是ready：unavailable",
        "[3/3] zn: passed",
    ]
    _assert_incomplete_global_checks(report, 2)


def test_graph_deployment_reports_unknown_product_without_catalog_io() -> None:
    """Catches an unknown requested product reaching timestamp or analysis I/O."""
    timestamps = {"ag": pd.DatetimeIndex(["2025-04-07 10:15"])}
    results = {"ag": _complete_ready_result("ag", timestamps["ag"][-1])}
    agent = _RecordingCatalogAgent(results, timestamps)
    progress: list[str] = []

    report = validation.validate_knowledge_graph_deployment(
        agent,
        product_codes=["xx"],
        progress=progress.append,
    )

    assert report["products"] == [
        {
            "product": "xx",
            "status": "failed",
            "error_type": "AssertionError",
            "error": "数据目录不存在品种：xx",
        }
    ]
    assert report["summary"] == {
        "status": "failed",
        "product_count": 1,
        "passed_products": 0,
        "failed_products": 1,
    }
    assert agent.list_timestamp_calls == []
    assert agent.analyze_calls == []
    assert progress == ["[1/1] xx: failed - 数据目录不存在品种：xx"]
    _assert_incomplete_global_checks(report, 0)


def test_graph_deployment_rejects_an_empty_catalog_without_fabricating_rows() -> None:
    """Catches an empty data source being reported as a successful acceptance."""
    agent = _RecordingCatalogAgent({}, {}, catalog_order=[])
    progress: list[str] = []

    report = validation.validate_knowledge_graph_deployment(agent, progress=progress.append)

    assert report["products"] == []
    assert report["summary"] == {
        "status": "failed",
        "product_count": 0,
        "passed_products": 0,
        "failed_products": 0,
    }
    assert agent.list_products_calls == 1
    assert agent.list_timestamp_calls == []
    assert agent.analyze_calls == []
    assert progress == []
    _assert_incomplete_global_checks(report, 0)


def _review_r3_passing_global_checks() -> dict[str, dict[str, object]]:
    return {
        "deterministic": {
            "passed": True,
            "checked_count": 1,
            "scope": "one repeated graph",
        },
        "no_future": {
            "passed": True,
            "checked_count": 2,
            "scope": "one graph plus appended-future replay",
        },
        "content_safety": {
            "passed": True,
            "checked_count": 10,
            "scope": "one explanation plus nine mandatory fixtures",
        },
    }


def _review_r3_invalid_global_checks(
    case: str,
) -> dict[str, dict[str, object]]:
    checks = _review_r3_passing_global_checks()
    if case == "only-deterministic":
        return {"deterministic": checks["deterministic"]}
    if case == "unknown-only-foo":
        return {"foo": checks["deterministic"]}
    if case.startswith("omit-"):
        checks.pop(case.removeprefix("omit-"))
        return checks
    raise AssertionError(f"unknown review case: {case}")


@pytest.mark.parametrize(
    "case",
    [
        "only-deterministic",
        "unknown-only-foo",
        "omit-deterministic",
        "omit-no_future",
        "omit-content_safety",
    ],
)
def test_review_r3_graph_deployment_fails_without_exact_mandatory_global_checks(
    monkeypatch,
    case: str,
) -> None:
    """Catches nonempty partial/unknown global checks authorizing deployment."""
    timestamp = pd.Timestamp("2025-04-07 10:15")
    agent = _RecordingCatalogAgent(
        {"ag": _complete_ready_result("ag", timestamp)},
        {"ag": pd.DatetimeIndex([timestamp])},
    )
    checks = _review_r3_invalid_global_checks(case)
    monkeypatch.setattr(
        validation,
        "_executed_global_graph_checks",
        lambda successful_results, *, total_products: checks,
    )

    report = validation.validate_knowledge_graph_deployment(agent)

    assert report["products"][0]["status"] == "passed"
    assert report["global_checks"] == checks
    assert report["summary"] == {
        "status": "failed",
        "product_count": 1,
        "passed_products": 1,
        "failed_products": 0,
    }


def test_review_r3_graph_deployment_accepts_exact_three_passing_global_checks(
    monkeypatch,
) -> None:
    """Keeps the exact mandatory three-check success contract green."""
    timestamp = pd.Timestamp("2025-04-07 10:15")
    agent = _RecordingCatalogAgent(
        {"ag": _complete_ready_result("ag", timestamp)},
        {"ag": pd.DatetimeIndex([timestamp])},
    )
    checks = _review_r3_passing_global_checks()
    monkeypatch.setattr(
        validation,
        "_executed_global_graph_checks",
        lambda successful_results, *, total_products: checks,
    )

    report = validation.validate_knowledge_graph_deployment(agent)

    assert report["global_checks"] == checks
    assert report["summary"] == {
        "status": "passed",
        "product_count": 1,
        "passed_products": 1,
        "failed_products": 0,
    }


def test_graph_deployment_summary_fails_when_any_executed_global_check_fails(
    monkeypatch,
) -> None:
    """Catches all-pass product rows masking a failed executed global check."""
    timestamp = pd.Timestamp("2025-04-07 10:15")
    agent = _RecordingCatalogAgent(
        {"ag": _complete_ready_result("ag", timestamp)},
        {"ag": pd.DatetimeIndex([timestamp])},
    )
    checks = {
        "deterministic": {
            "passed": True,
            "checked_count": 1,
            "scope": "one real graph",
        },
        "no_future": {
            "passed": False,
            "checked_count": 2,
            "scope": "one real graph plus failed append fixture",
        },
        "content_safety": {
            "passed": True,
            "checked_count": 10,
            "scope": "one explanation plus nine mandatory fixtures",
        },
    }
    monkeypatch.setattr(
        validation,
        "_executed_global_graph_checks",
        lambda successful_results, *, total_products: checks,
    )

    report = validation.validate_knowledge_graph_deployment(agent)

    assert report["products"][0]["status"] == "passed"
    assert report["global_checks"] == checks
    assert report["summary"] == {
        "status": "failed",
        "product_count": 1,
        "passed_products": 1,
        "failed_products": 0,
    }


def test_graph_deployment_executes_all_mandatory_content_safety_phrases(
    monkeypatch,
) -> None:
    """Catches the global check sampling only one unsafe and one safe phrase."""
    timestamp = pd.Timestamp("2025-04-07 10:15")
    agent = _RecordingCatalogAgent(
        {"ag": _complete_ready_result("ag", timestamp)},
        {"ag": pd.DatetimeIndex([timestamp])},
    )
    real_validator = validation.validate_explanation_language
    calls: list[tuple[str, str]] = []

    def recording_validator(text: str) -> None:
        try:
            real_validator(text)
        except UnsafeGraphExplanationError:
            calls.append((text, "rejected"))
            raise
        calls.append((text, "accepted"))

    monkeypatch.setattr(
        validation,
        "validate_explanation_language",
        recording_validator,
    )

    report = validation.validate_knowledge_graph_deployment(agent)

    expected_fixture_outcomes = {
        "建议买入": "rejected",
        "建议卖出": "rejected",
        "建议做多": "rejected",
        "建议做空": "rejected",
        "一定上涨": "rejected",
        "一定下跌": "rejected",
        "必然导致": "rejected",
        "不提供交易建议。": "accepted",
        "不预测标的价格涨跌方向。": "accepted",
    }
    actual_fixture_outcomes = {
        text: outcome
        for text, outcome in calls
        if text in expected_fixture_outcomes
    }
    assert actual_fixture_outcomes == expected_fixture_outcomes
    assert report["global_checks"]["content_safety"] == {
        "passed": True,
        "checked_count": 10,
        "scope": (
            "成功图谱1/1；逐个验证生成解释的语言安全，并执行"
            "7个不安全与2个安全限制措辞fixture"
        ),
    }


class _RuntimeItemsMapping(dict):
    def items(self):
        raise RuntimeError("synthetic graph mapping failure")


def test_graph_deployment_contains_mapping_runtime_error_at_graph_stage_only() -> None:
    """Catches graph Mapping runtime errors aborting later catalog products."""
    timestamps = {
        "ag": pd.DatetimeIndex(["2025-04-07 10:15"]),
        "cu": pd.DatetimeIndex(["2025-05-08 15:00"]),
    }
    results = {
        product: _complete_ready_result(product, rows[-1])
        for product, rows in timestamps.items()
    }
    ag_graph = results["ag"].knowledge_graph
    results["ag"] = replace(
        results["ag"],
        knowledge_graph=replace(
            ag_graph,
            graph_json=_RuntimeItemsMapping(ag_graph.graph_json),
        ),
    )
    agent = _RecordingCatalogAgent(results, timestamps, catalog_order=["cu", "ag"])
    progress: list[str] = []

    report = validation.validate_knowledge_graph_deployment(
        agent,
        progress=progress.append,
    )

    assert agent.analyze_calls == [
        ("ag", timestamps["ag"][-1]),
        ("cu", timestamps["cu"][-1]),
    ]
    assert report["products"][0] == {
        "product": "ag",
        "status": "failed",
        "timestamp_count": 1,
        "first_timestamp": "2025-04-07T10:15:00",
        "last_timestamp": "2025-04-07T10:15:00",
        "analysis": _expected_problem_one_analysis("ag", timestamps["ag"][-1]),
        "knowledge_graph": {
            "status": "failed",
            "error_type": "RuntimeError",
            "error": "synthetic graph mapping failure",
        },
        "error_type": "RuntimeError",
        "error": "synthetic graph mapping failure",
    }
    assert report["products"][1]["status"] == "passed"
    assert progress == [
        "[1/2] ag: failed - synthetic graph mapping failure",
        "[2/2] cu: passed",
    ]
    assert report["summary"] == {
        "status": "failed",
        "product_count": 2,
        "passed_products": 1,
        "failed_products": 1,
    }


def test_graph_deployment_does_not_swallow_runtime_error_before_graph_stage() -> None:
    """Guards against broadening RuntimeError handling around the whole loop."""
    timestamp = pd.Timestamp("2025-04-07 10:15")
    agent = _RecordingCatalogAgent(
        {"ag": _complete_ready_result("ag", timestamp)},
        {"ag": pd.DatetimeIndex([timestamp])},
    )

    def fail_analysis(product: str, selected_timestamp: pd.Timestamp):
        raise RuntimeError("synthetic pre-graph analysis bug")

    agent.analyze = fail_analysis

    with pytest.raises(RuntimeError, match="pre-graph analysis bug"):
        validation.validate_knowledge_graph_deployment(agent)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUERY_SCRIPT = PROJECT_ROOT / "scripts" / "query_knowledge_graph.py"
VALIDATION_SCRIPT = PROJECT_ROOT / "scripts" / "validate_knowledge_graph.py"


def _write_cli_product_history(
    root: Path,
    product: str,
    start: str,
    *,
    periods: int = 120,
) -> pd.DatetimeIndex:
    timestamps = pd.date_range(start, periods=periods, freq="15min")
    rows: list[dict[str, object]] = []
    for bar, timestamp in enumerate(timestamps):
        forward = 6000.0 * (1 + 0.0002 * bar)
        for dte in (20, 50, 80):
            underlying = f"{product}{2506 + dte}"
            for moneyness in (0.84, 0.90, 0.95, 0.98, 1.02, 1.05, 1.10, 1.16):
                strike = round(forward * moneyness / 10) * 10
                log_moneyness = np.log(moneyness)
                option_type = "put" if moneyness < 1 else "call"
                iv = (
                    0.18
                    + 0.25 * log_moneyness**2
                    + 0.00035 * dte
                    + 0.00015 * bar
                )
                intrinsic = (
                    max(forward - strike, 0)
                    if option_type == "call"
                    else max(strike - forward, 0)
                )
                close = max(
                    10.0,
                    intrinsic + forward * iv * np.sqrt(dte / 365) * 0.08,
                )
                rows.append(
                    {
                        "timestamp": int(timestamp.strftime("%Y%m%d%H%M%S")),
                        "contract": f"{underlying}{option_type[0].upper()}{strike}",
                        "underlying": underlying,
                        "option_type": option_type,
                        "strike": strike,
                        "open": close,
                        "high": close * 1.01,
                        "low": close * 0.99,
                        "close": close,
                        "volume": 10,
                        "amount": close * 10,
                        "open_interest": 100 + bar,
                        "settlement_price": close,
                        "pre_close": close,
                        "suspend_flag": 0,
                        "iv": iv,
                        "delta": 0.45 if option_type == "call" else -0.45,
                        "gamma": 0.001 + 0.004 * np.exp(-15 * log_moneyness**2),
                        "theta": -0.01 - 0.00001 * bar,
                        "vega": 0.08 * np.sqrt(dte / 365) * (1 + 0.0001 * bar),
                        "dte": dte,
                        "moneyness": moneyness,
                        "moneyness_type": "ATM" if abs(log_moneyness) <= 0.03 else "OTM",
                        "date": timestamp.date(),
                    }
                )
    frame = pd.DataFrame(rows)
    path = (
        root
        / "期权课题"
        / "archive"
        / "SF"
        / f"{product}2506"
        / "options"
        / timestamps[0].strftime("%Y")
        / timestamps[0].strftime("%m")
        / f"options_{timestamps[0]:%Y%m}.parquet"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=False)
    return timestamps


def _parquet_source_state(root: Path) -> dict[str, object]:
    """Return observable raw-row and byte state without trusting agent caches."""
    root = Path(root).resolve()
    files: list[tuple[str, int, int | None, str]] = []
    for path in sorted(root.rglob("*.parquet")):
        timestamps = pd.read_parquet(path, columns=["timestamp"])["timestamp"]
        numeric = pd.to_numeric(timestamps, errors="raise")
        maximum = int(numeric.max()) if len(numeric) else None
        files.append(
            (
                path.relative_to(root).as_posix(),
                len(numeric),
                maximum,
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
        )
    return {
        "source": str(root),
        "files": tuple(files),
        "row_count": sum(row_count for _, row_count, _, _ in files),
        "max_raw_timestamp": max(
            (maximum for _, _, maximum, _ in files if maximum is not None),
            default=None,
        ),
    }


def test_no_future_global_check_replays_real_agent_after_physical_future_append(
    tmp_path,
    monkeypatch,
) -> None:
    """Catches a graph-tamper fixture that never re-runs the real data pipeline."""
    source = tmp_path / "source"
    timestamps = _write_cli_product_history(
        source,
        "ag",
        "2025-01-02 09:00",
    )
    original_source_state = _parquet_source_state(source)
    analysis_events: list[dict[str, object]] = []
    audit_events: list[tuple[int, str]] = []
    real_analyze = OptionRiskAgent.analyze
    real_audit = validation._canonical_graph_audit_document

    def recording_analyze(
        self: OptionRiskAgent,
        product: str,
        selected_timestamp: pd.Timestamp | str,
    ) -> AgentResult:
        source_state = _parquet_source_state(self.config.data_source)
        result = real_analyze(self, product, selected_timestamp)
        analysis_events.append(
            {
                "agent": self,
                "agent_id": id(self),
                "cache_dir": str(self.config.cache_dir),
                "product": product,
                "selected_timestamp": pd.Timestamp(selected_timestamp),
                "source_state": source_state,
                "result": result,
                "result_id": id(result),
            }
        )
        return result

    def recording_audit(result: AgentResult) -> str:
        document = real_audit(result)
        audit_events.append((id(result), document))
        return document

    monkeypatch.setattr(OptionRiskAgent, "analyze", recording_analyze)
    monkeypatch.setattr(
        validation,
        "_canonical_graph_audit_document",
        recording_audit,
    )
    agent = OptionRiskAgent(
        AgentConfig(
            data_source=source,
            cache_dir=tmp_path / "main-cache",
            output_dir=tmp_path / "main-output",
        )
    )

    report = validation.validate_knowledge_graph_deployment(
        agent,
        product_codes=["ag"],
    )

    replay_pairs: list[tuple[dict[str, object], dict[str, object]]] = []
    for before, after in combinations(analysis_events, 2):
        before_state = before["source_state"]
        after_state = after["source_state"]
        assert isinstance(before_state, dict) and isinstance(after_state, dict)
        if (
            before["agent_id"] != after["agent_id"]
            and before["cache_dir"] != after["cache_dir"]
            and before["product"] == after["product"]
            and before["selected_timestamp"] == after["selected_timestamp"]
            and before_state["source"] == after_state["source"]
            and before_state["row_count"] < after_state["row_count"]
            and before_state["files"] != after_state["files"]
        ):
            replay_pairs.append((before, after))

    assert replay_pairs, (
        "no_future fixture must use two distinct real OptionRiskAgent instances and "
        "physically append future raw rows between analyses of the same history"
    )
    before, after = replay_pairs[0]
    before_state = before["source_state"]
    after_state = after["source_state"]
    assert isinstance(before_state, dict) and isinstance(after_state, dict)
    selected_raw = int(
        pd.Timestamp(before["selected_timestamp"]).strftime("%Y%m%d%H%M%S")
    )
    assert before_state["max_raw_timestamp"] == selected_raw
    assert after_state["max_raw_timestamp"] > selected_raw
    assert before["selected_timestamp"] == after["selected_timestamp"]
    assert before["agent_id"] != after["agent_id"]
    assert before["cache_dir"] != after["cache_dir"]
    before_files = {row[0]: row[1:] for row in before_state["files"]}
    after_files = {row[0]: row[1:] for row in after_state["files"]}
    common_paths = set(before_files) & set(after_files)
    new_paths = set(after_files) - set(before_files)
    assert common_paths == set(before_files)
    assert {path: before_files[path] for path in common_paths} == {
        path: after_files[path] for path in common_paths
    }
    assert new_paths
    assert all(path.endswith("/2025/02/options_202502.parquet") for path in new_paths)

    documents_by_result: dict[int, list[str]] = {}
    for result_id, document in audit_events:
        documents_by_result.setdefault(result_id, []).append(document)
    before_documents = documents_by_result.get(before["result_id"], [])
    after_documents = documents_by_result.get(after["result_id"], [])
    assert before_documents and after_documents
    assert len(set(before_documents)) == len(set(after_documents)) == 1
    assert before_documents[0] == after_documents[0]
    canonical_payload = json.loads(before_documents[0])
    assert set(canonical_payload) == {"graph", "result", "queries", "explanation"}
    assert "active_paths" in canonical_payload["result"]

    before_result = before["result"]
    after_result = after["result"]
    assert isinstance(before_result, AgentResult) and isinstance(after_result, AgentResult)
    before_graph_document = validation._strict_json_document(
        before_result.knowledge_graph,
        owner="before future replay KnowledgeGraphResult",
    )
    after_graph_document = validation._strict_json_document(
        after_result.knowledge_graph,
        owner="after future replay KnowledgeGraphResult",
    )
    assert before_graph_document == after_graph_document
    assert set(json.loads(before_graph_document)) == {
        "status",
        "schema_version",
        "rule_version",
        "product",
        "timestamp",
        "graph_json",
        "node_count",
        "edge_count",
        "active_path_count",
        "active_paths",
        "root_evidence",
        "possible_consequences",
        "explanation_sections",
        "explanation_text",
        "explanation_confidence",
        "missing_evidence",
        "query_index",
        "error_type",
        "error_message",
    }

    assert _parquet_source_state(source) == original_source_state
    assert report["global_checks"]["no_future"] == {
        "passed": True,
        "checked_count": 2,
        "scope": (
            "成功图谱1/1；审计节点、边和路径未来信息，并执行1个真实"
            "OptionRiskAgent同历史时点、追加未来记录且写入新月份分区的回放fixture"
        ),
    }


@pytest.fixture(scope="module")
def real_query_cli_case(tmp_path_factory):
    root = tmp_path_factory.mktemp("knowledge-graph-query-cli")
    data_dir = root / "data"
    _write_cli_product_history(data_dir, "ag", "2025-01-02 09:00")
    _write_cli_product_history(data_dir, "cu", "2025-03-03 09:00")
    cache_dir = root / "cache"
    output_dir = root / "outputs"
    agent = OptionRiskAgent(
        AgentConfig(
            data_source=data_dir,
            cache_dir=cache_dir,
            output_dir=output_dir,
        )
    )
    products = [item.code for item in agent.list_products()]
    assert products == ["ag", "cu"]
    timestamp = agent.list_timestamps("ag")[-1]
    result = agent.analyze("ag", timestamp)
    assert result.knowledge_graph is not None
    assert result.knowledge_graph.status == "ready"
    service = GraphQueryService(result.knowledge_graph)
    evidence_id = next(
        row["node_id"]
        for row in result.knowledge_graph.graph_json["nodes"]
        if row["node_type"] == "Evidence" and row["feature_name"] == "atm_iv"
    )
    return {
        "data_dir": data_dir,
        "cache_dir": cache_dir,
        "output_dir": output_dir,
        "timestamp": timestamp,
        "result": result,
        "service": service,
        "node_id": evidence_id,
    }


def _run_script(path: Path, arguments: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(path), *arguments],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
    )


def _query_cli_arguments(case: dict, query: str, *, node_id: str | None = None) -> list[str]:
    arguments = [
        "--data-dir",
        str(case["data_dir"]),
        "--cache-dir",
        str(case["cache_dir"]),
        "--output-dir",
        str(case["output_dir"]),
        "--product",
        "ag",
        "--timestamp",
        case["timestamp"].isoformat(),
        "--query",
        query,
    ]
    if node_id is not None:
        arguments.extend(["--node-id", node_id])
    return arguments


def _expected_query_records(case: dict, query: str) -> list[dict]:
    service = case["service"]
    if query == "root-evidence":
        return service.root_evidence(limit=3)
    if query == "alert-paths":
        return service.paths_to_alert()
    if query == "consequences":
        return service.possible_consequences()
    if query == "quality-limitations":
        return service.quality_limitations()
    if query == "node-detail":
        return [service.inspect_node(case["node_id"])]
    raise AssertionError(f"unregistered test query: {query}")


@pytest.mark.parametrize(
    "query",
    [
        "root-evidence",
        "alert-paths",
        "consequences",
        "quality-limitations",
        "node-detail",
    ],
)
def test_query_cli_maps_each_fixed_query_to_exact_real_records(
    real_query_cli_case,
    query: str,
) -> None:
    """Catches a CLI query name forwarding to the wrong public graph method."""
    node_id = real_query_cli_case["node_id"] if query == "node-detail" else None

    completed = _run_script(
        QUERY_SCRIPT,
        _query_cli_arguments(real_query_cli_case, query, node_id=node_id),
    )

    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    stdout = completed.stdout.decode("utf-8", errors="strict")
    payload = json.loads(stdout)
    records = _expected_query_records(real_query_cli_case, query)
    assert payload == {
        "product": "ag",
        "timestamp": real_query_cli_case["timestamp"].isoformat(),
        "schema_version": "kg-schema-v1",
        "rule_version": "kg-rule-v1",
        "query": query,
        "record_count": len(records),
        "records": records,
    }
    assert "generated_at" not in payload


def test_query_cli_stdout_is_utf8_json_only_and_byte_deterministic(
    real_query_cli_case,
) -> None:
    """Catches timestamps, progress, or escaping making identical queries unstable."""
    arguments = _query_cli_arguments(
        real_query_cli_case,
        "node-detail",
        node_id=real_query_cli_case["node_id"],
    )

    first = _run_script(QUERY_SCRIPT, arguments)
    second = _run_script(QUERY_SCRIPT, arguments)

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert b"\r\n" not in first.stdout
    decoded = first.stdout.decode("utf-8", errors="strict")
    assert json.loads(decoded)["query"] == "node-detail"
    assert "ATM隐含波动率" in decoded
    assert not decoded.startswith("[")
    assert "progress" not in decoded.lower() and "error" not in decoded.lower()


@pytest.mark.parametrize(
    ("case_name", "expected_stderr"),
    [
        ("node-detail-without-id", "--node-id"),
        ("surplus-node-id", "--node-id"),
        ("bad-query", "invalid choice"),
        ("missing-source", "--data-dir"),
        ("both-sources", "not allowed with argument"),
    ],
)
def test_query_cli_usage_errors_exit_two_without_stdout(
    real_query_cli_case,
    case_name: str,
    expected_stderr: str,
) -> None:
    """Catches query/source grammar errors leaking into domain exit code 1."""
    if case_name == "node-detail-without-id":
        arguments = _query_cli_arguments(real_query_cli_case, "node-detail")
    elif case_name == "surplus-node-id":
        arguments = _query_cli_arguments(
            real_query_cli_case,
            "root-evidence",
            node_id=real_query_cli_case["node_id"],
        )
    elif case_name == "bad-query":
        arguments = _query_cli_arguments(real_query_cli_case, "free-text")
    elif case_name == "missing-source":
        arguments = [
            "--product",
            "ag",
            "--timestamp",
            real_query_cli_case["timestamp"].isoformat(),
            "--query",
            "root-evidence",
        ]
    else:
        arguments = [
            *_query_cli_arguments(real_query_cli_case, "root-evidence"),
            "--archive-path",
            str(Path(real_query_cli_case["data_dir"]).with_suffix(".rar")),
        ]

    completed = _run_script(QUERY_SCRIPT, arguments)

    stderr = completed.stderr.decode("utf-8", errors="replace").lower()
    assert completed.returncode == 2
    assert completed.stdout == b""
    assert "can't open file" not in stderr
    assert expected_stderr.lower() in stderr


@pytest.mark.parametrize(
    ("case_name", "expected_stderr"),
    [
        ("unknown-node", "node"),
        ("unknown-product", "品种"),
        ("unknown-timestamp", "时间"),
    ],
)
def test_query_cli_real_domain_errors_exit_one_without_stdout(
    real_query_cli_case,
    case_name: str,
    expected_stderr: str,
) -> None:
    """Catches real catalog/query domain failures becoming usage errors or JSON."""
    if case_name == "unknown-node":
        arguments = _query_cli_arguments(
            real_query_cli_case,
            "node-detail",
            node_id="evidence:not-present",
        )
    elif case_name == "unknown-product":
        arguments = _query_cli_arguments(real_query_cli_case, "root-evidence")
        arguments[arguments.index("ag")] = "xx"
    else:
        arguments = _query_cli_arguments(real_query_cli_case, "root-evidence")
        arguments[arguments.index(real_query_cli_case["timestamp"].isoformat())] = (
            "1900-01-01T00:00:00"
        )

    completed = _run_script(QUERY_SCRIPT, arguments)

    stderr = completed.stderr.decode("utf-8", errors="strict")
    assert completed.returncode == 1
    assert completed.stdout == b""
    assert expected_stderr in stderr


def _load_script_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("failure_mode", "expected_stderr"),
    [
        ("unavailable", "unavailable"),
        ("domain", "synthetic graph domain failure"),
        ("serialization", "json"),
    ],
)
def test_query_cli_injected_runtime_failures_exit_one_without_partial_json(
    tmp_path,
    monkeypatch,
    capsys,
    failure_mode: str,
    expected_stderr: str,
) -> None:
    """Catches graph/serialization failures printing partial stdout or traceback exit."""
    module = _load_script_module(
        QUERY_SCRIPT,
        f"_query_knowledge_graph_{failure_mode}",
    )
    timestamp = pd.Timestamp("2025-04-07 10:15")
    base = _complete_ready_result("ag", timestamp)
    if failure_mode == "unavailable":
        result = replace(
            base,
            knowledge_graph=KnowledgeGraphResult.unavailable(
                product="ag",
                timestamp=timestamp,
                error_type="RuntimeError",
                error_message="synthetic unavailable graph",
            ),
        )
    else:
        result = base

    class FakeAgent:
        def __init__(self, config):
            self.config = config

        def analyze(self, product, selected_timestamp):
            if failure_mode == "domain":
                raise KnowledgeGraphError("synthetic graph domain failure")
            return result

    class NonSerializableQueryService:
        def __init__(self, graph_result):
            self.graph_result = graph_result

        def root_evidence(self, limit=3):
            return [{"bad": object()}]

    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    if failure_mode == "serialization":
        monkeypatch.setattr(module, "GraphQueryService", NonSerializableQueryService)

    exit_code = module.main(
        [
            "--data-dir",
            str(tmp_path / "data"),
            "--product",
            "ag",
            "--timestamp",
            timestamp.isoformat(),
            "--query",
            "root-evidence",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert expected_stderr.lower() in captured.err.lower()


@pytest.mark.parametrize("status", ["passed", "failed"])
def test_validation_cli_writes_the_same_strict_json_it_prints_and_routes_progress(
    tmp_path,
    monkeypatch,
    capsys,
    status: str,
) -> None:
    """Catches report/stdout drift, wrong status exit, or progress on stdout."""
    module = _load_script_module(
        VALIDATION_SCRIPT,
        f"_validate_knowledge_graph_{status}",
    )
    payload = {
        "summary": {
            "status": status,
            "product_count": 1,
            "passed_products": 1 if status == "passed" else 0,
            "failed_products": 0 if status == "passed" else 1,
        },
        "products": [{"product": "ag", "status": status, "说明": "验收"}],
        "global_checks": {},
    }

    class FakeAgent:
        last_config = None

        def __init__(self, config):
            FakeAgent.last_config = config

    def fake_validate(agent, *, product_codes=None, progress=None):
        assert product_codes == ["ag"]
        assert progress is not None
        progress(f"[1/1] ag: {status}")
        return payload

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    monkeypatch.setattr(module, "validate_knowledge_graph_deployment", fake_validate)
    report_path = tmp_path / f"{status}.json"

    exit_code = module.main(
        [
            "--data-dir",
            str(tmp_path / "data"),
            "--products",
            "ag",
            "--report",
            str(report_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == (0 if status == "passed" else 1)
    assert json.loads(captured.out) == payload
    assert json.loads(report_path.read_text(encoding="utf-8")) == payload
    assert captured.out.rstrip("\r\n").encode("utf-8") == report_path.read_bytes()
    assert captured.err == f"[1/1] ag: {status}\n"
    assert FakeAgent.last_config.cache_dir == (tmp_path / "data/agent_cache").resolve()
    assert FakeAgent.last_config.output_dir == (tmp_path / "outputs").resolve()


def test_validation_cli_exits_one_when_global_check_fails_despite_passed_summary(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    """Catches a crafted passed summary overriding a failed executed check."""
    module = _load_script_module(
        VALIDATION_SCRIPT,
        "_validate_knowledge_graph_failed_global_check",
    )
    payload = {
        "summary": {
            "status": "passed",
            "product_count": 1,
            "passed_products": 1,
            "failed_products": 0,
        },
        "products": [{"product": "ag", "status": "passed"}],
        "global_checks": {
            "deterministic": {
                "passed": True,
                "checked_count": 1,
                "scope": "one graph",
            },
            "no_future": {
                "passed": False,
                "checked_count": 2,
                "scope": "failed future append replay",
            },
            "content_safety": {
                "passed": True,
                "checked_count": 10,
                "scope": "one explanation plus mandatory fixtures",
            },
        },
    }

    class FakeAgent:
        def __init__(self, config):
            self.config = config

    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    monkeypatch.setattr(
        module,
        "validate_knowledge_graph_deployment",
        lambda agent, **kwargs: payload,
    )
    report_path = tmp_path / "failed-global-check.json"

    exit_code = module.main(
        [
            "--data-dir",
            str(tmp_path / "data"),
            "--report",
            str(report_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert json.loads(captured.out) == payload
    assert json.loads(report_path.read_text(encoding="utf-8")) == payload


def _review_r3_passed_cli_payload(global_checks) -> dict:
    return {
        "summary": {
            "status": "passed",
            "product_count": 1,
            "passed_products": 1,
            "failed_products": 0,
        },
        "products": [{"product": "ag", "status": "passed"}],
        "global_checks": global_checks,
    }


@pytest.mark.parametrize(
    "case",
    [
        "only-deterministic",
        "unknown-only-foo",
        "omit-deterministic",
        "omit-no_future",
        "omit-content_safety",
    ],
)
def test_review_r3_validation_cli_rejects_nonempty_incomplete_global_checks(
    tmp_path,
    monkeypatch,
    capsys,
    case: str,
) -> None:
    """Catches a passed summary bypassing the exact mandatory check set."""
    module = _load_script_module(
        VALIDATION_SCRIPT,
        f"_validate_knowledge_graph_review_r3_{case.replace('-', '_')}",
    )
    payload = _review_r3_passed_cli_payload(
        _review_r3_invalid_global_checks(case)
    )

    class FakeAgent:
        def __init__(self, config):
            self.config = config

    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    monkeypatch.setattr(
        module,
        "validate_knowledge_graph_deployment",
        lambda agent, **kwargs: payload,
    )
    report_path = tmp_path / f"review-r3-{case}.json"

    helper_allowed = module._global_checks_allow_success(payload)
    exit_code = module.main(
        [
            "--data-dir",
            str(tmp_path / "data"),
            "--report",
            str(report_path),
        ]
    )
    captured = capsys.readouterr()

    assert (helper_allowed, exit_code) == (False, 1)
    assert json.loads(captured.out) == payload
    assert json.loads(report_path.read_text(encoding="utf-8")) == payload


@pytest.mark.parametrize(
    ("case", "checks"),
    [
        ("none", None),
        ("empty", {}),
        ("exact-three", _review_r3_passing_global_checks()),
    ],
)
def test_review_r3_validation_cli_preserves_approved_global_check_controls(
    tmp_path,
    monkeypatch,
    capsys,
    case: str,
    checks,
) -> None:
    """Locks None/empty compatibility and exact-three-check success."""
    module = _load_script_module(
        VALIDATION_SCRIPT,
        f"_validate_knowledge_graph_review_r3_control_{case.replace('-', '_')}",
    )
    payload = _review_r3_passed_cli_payload(checks)

    class FakeAgent:
        def __init__(self, config):
            self.config = config

    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    monkeypatch.setattr(
        module,
        "validate_knowledge_graph_deployment",
        lambda agent, **kwargs: payload,
    )
    report_path = tmp_path / f"review-r3-control-{case}.json"

    helper_allowed = module._global_checks_allow_success(payload)
    exit_code = module.main(
        [
            "--data-dir",
            str(tmp_path / "data"),
            "--report",
            str(report_path),
        ]
    )
    captured = capsys.readouterr()

    assert (helper_allowed, exit_code) == (True, 0)
    assert json.loads(captured.out) == payload
    assert json.loads(report_path.read_text(encoding="utf-8")) == payload


def test_validation_cli_real_subprocess_keeps_report_and_stdout_bytes_platform_stable(
    real_query_cli_case,
    tmp_path,
) -> None:
    """Catches Windows text translation making report/stdout JSON bytes drift."""
    report_path = tmp_path / "knowledge_graph_acceptance.json"
    completed = _run_script(
        VALIDATION_SCRIPT,
        [
            "--data-dir",
            str(real_query_cli_case["data_dir"]),
            "--cache-dir",
            str(real_query_cli_case["cache_dir"]),
            "--output-dir",
            str(tmp_path / "outputs"),
            "--products",
            "ag",
            "--report",
            str(report_path),
        ],
    )

    assert completed.returncode == 0, completed.stderr.decode(
        "utf-8", errors="replace"
    )
    payload = json.loads(
        completed.stdout.decode("utf-8", errors="strict"),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    assert payload["summary"] == {
        "status": "passed",
        "product_count": 1,
        "passed_products": 1,
        "failed_products": 0,
    }
    assert b"\r\n" not in completed.stdout
    assert completed.stdout.rstrip(b"\r\n") == report_path.read_bytes()


@pytest.mark.parametrize(
    ("arguments", "expected_stderr"),
    [
        ([], "--data-dir"),
        (
            ["--data-dir", "data", "--archive-path", "archive.rar"],
            "not allowed with argument",
        ),
    ],
)
def test_validation_cli_source_usage_errors_exit_two_without_stdout(
    arguments: list[str],
    expected_stderr: str,
) -> None:
    """Catches missing/ambiguous deployment sources reaching runtime validation."""
    completed = _run_script(VALIDATION_SCRIPT, arguments)

    stderr = completed.stderr.decode("utf-8", errors="replace").lower()
    assert completed.returncode == 2
    assert completed.stdout == b""
    assert "can't open file" not in stderr
    assert expected_stderr.lower() in stderr


def test_validation_cli_optional_report_uses_output_default_with_archive_source(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    """Catches optional report or archive configuration ignoring registered defaults."""
    module = _load_script_module(VALIDATION_SCRIPT, "_validate_knowledge_graph_defaults")
    payload = {
        "summary": {
            "status": "passed",
            "product_count": 1,
            "passed_products": 1,
            "failed_products": 0,
        },
        "products": [{"product": "ag", "status": "passed"}],
        "global_checks": {},
    }

    class FakeAgent:
        last_config = None

        def __init__(self, config):
            FakeAgent.last_config = config

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    monkeypatch.setattr(
        module,
        "validate_knowledge_graph_deployment",
        lambda agent, **kwargs: payload,
    )
    output_dir = tmp_path / "formal-output"
    archive_path = tmp_path / "期权数据.rar"

    exit_code = module.main(
        [
            "--archive-path",
            str(archive_path),
            "--output-dir",
            str(output_dir),
        ]
    )
    captured = capsys.readouterr()
    default_report = output_dir / "knowledge_graph_acceptance_full.json"

    assert exit_code == 0
    assert json.loads(captured.out) == payload
    assert json.loads(default_report.read_text(encoding="utf-8")) == payload
    assert FakeAgent.last_config.archive_path == archive_path.resolve()
    assert FakeAgent.last_config.cache_dir == (tmp_path / "data/agent_cache").resolve()
    assert FakeAgent.last_config.output_dir == output_dir.resolve()


def test_validation_cli_rejects_non_strict_json_before_stdout_or_report(
    tmp_path,
    monkeypatch,
    capsys,
) -> None:
    """Catches allow_nan/default serialization emitting an invalid formal artifact."""
    module = _load_script_module(VALIDATION_SCRIPT, "_validate_knowledge_graph_nan")
    payload = {
        "summary": {
            "status": "passed",
            "product_count": 1,
            "passed_products": 1,
            "failed_products": 0,
        },
        "probe": float("nan"),
    }

    class FakeAgent:
        def __init__(self, config):
            self.config = config

    monkeypatch.setattr(module, "OptionRiskAgent", FakeAgent)
    monkeypatch.setattr(
        module,
        "validate_knowledge_graph_deployment",
        lambda agent, **kwargs: payload,
    )
    report_path = tmp_path / "must-not-exist.json"

    exit_code = module.main(
        [
            "--data-dir",
            str(tmp_path / "data"),
            "--report",
            str(report_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert not report_path.exists()
    assert any(word in captured.err.lower() for word in ("json", "nan", "finite"))
````

</details>
