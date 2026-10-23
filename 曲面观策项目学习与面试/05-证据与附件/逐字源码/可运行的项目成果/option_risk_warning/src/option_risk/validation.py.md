---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/validation.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/validation.py>)

SHA-256：`606c5c3f099b4d38b36c0d17029fa329642ea0b16a39a1aaf78f2fa87046b5dd`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, datetime
import inspect
import json
import math
from numbers import Integral, Real
from pathlib import Path
import tempfile
from typing import Any

import numpy as np
import pandas as pd

from .agent import OptionRiskAgent
from .config import AgentConfig
from .contracts import (
    AgentResult,
    ExplanationSection,
    FeatureEvidence,
    KnowledgeGraphResult,
    RiskPath,
)
from .errors import OptionRiskAgentError
from .graph_explanation import (
    UnsafeGraphExplanationError,
    render_graph_explanation,
    validate_explanation_language,
)
from .graph_queries import GraphQueryService
from .graph_reasoner import discover_risk_paths
from .knowledge_graph import (
    KnowledgeGraphError,
    graph_from_node_link,
    graph_to_node_link,
)
from .knowledge_schema import (
    FEATURE_RULES,
    KG_RULE_VERSION,
    KG_SCHEMA_VERSION,
    NodeType,
)


EXPECTED_SURFACES = {"iv", "delta", "gamma", "vega", "theta"}
EXPECTED_FEATURE_GROUPS = {
    "曲面水平与形态",
    "期限结构",
    "无套利风险",
    "Greeks集中风险",
    "质量与流动性",
}
MANDATORY_GLOBAL_CHECK_NAMES = frozenset(
    {"deterministic", "no_future", "content_safety"}
)


def _require_graph_contract(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _strict_json_ready(value: Any, active: set[int] | None = None) -> Any:
    """Convert only registered scalar containers; never repair invalid values."""

    active = set() if active is None else active
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            raise TypeError("NaT is not valid JSON data")
        return value.isoformat()
    if isinstance(value, np.generic):
        return _strict_json_ready(value.item(), active)
    if isinstance(value, Integral):
        return int(value)
    if isinstance(value, Real):
        # Keep NaN and infinities intact so allow_nan=False rejects them.
        return float(value)
    if is_dataclass(value) and not isinstance(value, type):
        identity = id(value)
        if identity in active:
            raise TypeError("cyclic dataclass value")
        active.add(identity)
        try:
            return {
                field.name: _strict_json_ready(getattr(value, field.name), active)
                for field in fields(value)
            }
        finally:
            active.remove(identity)
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise TypeError("cyclic mapping value")
        active.add(identity)
        try:
            result: dict[str, Any] = {}
            for key, item in value.items():
                if not isinstance(key, str):
                    raise TypeError("JSON object keys must be strings")
                result[key] = _strict_json_ready(item, active)
            return result
        finally:
            active.remove(identity)
    if isinstance(value, np.ndarray):
        return _strict_json_ready(value.tolist(), active)
    if isinstance(value, (list, tuple)):
        identity = id(value)
        if identity in active:
            raise TypeError("cyclic sequence value")
        active.add(identity)
        try:
            return [_strict_json_ready(item, active) for item in value]
        finally:
            active.remove(identity)
    return value


def _strict_json_document(value: Any, *, owner: str) -> str:
    try:
        return json.dumps(
            _strict_json_ready(value),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise AssertionError(f"{owner}不满足严格JSON序列化要求：{error}") from error


def _same_exact_json_structure(actual: Any, expected: Any) -> bool:
    if type(actual) is not type(expected):
        return False
    if is_dataclass(expected) and not isinstance(expected, type):
        return all(
            _same_exact_json_structure(
                getattr(actual, field.name),
                getattr(expected, field.name),
            )
            for field in fields(expected)
        )
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            _same_exact_json_structure(actual[key], value)
            for key, value in expected.items()
        )
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            _same_exact_json_structure(left, right)
            for left, right in zip(actual, expected, strict=True)
        )
    return actual == expected


def _finite_number(value: Any) -> float | None:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value, (Real, np.integer, np.floating)
    ):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _require_builtin_string(value: Any, owner: str) -> None:
    _require_graph_contract(type(value) is str, f"{owner}必须是原生字符串类型")


def _require_optional_builtin_float(value: Any, owner: str) -> None:
    _require_graph_contract(
        value is None or (type(value) is float and math.isfinite(value)),
        f"{owner}必须是None或有限原生float数值类型",
    )


def _require_string_tuple(value: Any, owner: str) -> None:
    _require_graph_contract(type(value) is tuple, f"{owner}必须是规范tuple元组类型")
    _require_graph_contract(
        all(type(item) is str for item in value),
        f"{owner}中的ID必须是原生字符串类型",
    )


def _require_feature_evidence_contract(row: Any) -> None:
    _require_graph_contract(
        type(row) is FeatureEvidence,
        "Problem 1 Evidence包含非法记录",
    )
    for field_name in ("group", "feature_name", "label", "status"):
        _require_builtin_string(
            getattr(row, field_name),
            f"Problem 1 Evidence字段{field_name}",
        )
    for field_name in (
        "current_value",
        "reference_value",
        "pressure_ratio",
        "change_rate",
    ):
        _require_optional_builtin_float(
            getattr(row, field_name),
            f"Problem 1 Evidence字段{field_name}",
        )
    _strict_json_document(row, owner="Problem 1 FeatureEvidence")


def _require_risk_path_contract(path: Any) -> None:
    _require_graph_contract(type(path) is RiskPath, "知识图谱路径path包含非法记录")
    for field_name in (
        "path_id",
        "evidence_node_id",
        "anomaly_node_id",
        "mechanism_node_id",
        "conclusion_node_id",
    ):
        _require_builtin_string(
            getattr(path, field_name),
            f"知识图谱路径path字段{field_name}",
        )
    for field_name in ("edge_ids", "relation_semantics", "rule_ids"):
        _require_string_tuple(
            getattr(path, field_name),
            f"知识图谱路径path字段{field_name}",
        )
    _require_builtin_string(path.severity, "知识图谱路径path字段severity")
    _require_optional_builtin_float(
        path.pressure_ratio,
        "知识图谱路径path字段pressure_ratio",
    )
    _require_graph_contract(
        type(path.timestamp) is pd.Timestamp,
        "知识图谱路径path字段timestamp必须是Timestamp类型",
    )


def _require_explanation_section_contract(section: Any) -> None:
    _require_graph_contract(
        type(section) is ExplanationSection,
        "知识图谱explanation section必须是精确ExplanationSection类型",
    )
    for field_name in ("section_id", "title", "content"):
        _require_builtin_string(
            getattr(section, field_name),
            f"知识图谱explanation section字段{field_name}",
        )
    _require_string_tuple(
        section.path_ids,
        "知识图谱explanation section字段path_ids",
    )
    _strict_json_document(section, owner="KnowledgeGraphResult explanation section")


def _one_graph_node(graph, node_type: NodeType) -> tuple[str, dict[str, Any]]:
    rows = [
        (str(node_id), data)
        for node_id, data in graph.nodes(data=True)
        if data["node_type"] == node_type.value
    ]
    _require_graph_contract(
        len(rows) == 1,
        f"知识图谱必须恰有一个{node_type.value}节点",
    )
    return rows[0]


def validate_knowledge_graph_result(
    result: AgentResult,
    requested_product: str,
    requested_timestamp: pd.Timestamp,
) -> dict[str, Any]:
    """Validate one ready Problem 2 result without trusting cached graph fields."""

    selected_time = pd.Timestamp(requested_timestamp)
    _require_graph_contract(
        isinstance(result, AgentResult),
        "知识图谱验收需要AgentResult",
    )
    graph_result = result.knowledge_graph
    _require_graph_contract(
        isinstance(graph_result, KnowledgeGraphResult),
        "AgentResult缺少KnowledgeGraphResult",
    )
    # Audit the raw frozen result.  Do not call to_dict(): its normalizers would
    # hide NumPy scalars and equality-compatible container/type drift.
    _strict_json_document(graph_result, owner="KnowledgeGraphResult完整结果")
    for field_name in (
        "status",
        "schema_version",
        "rule_version",
        "product",
        "explanation_text",
        "explanation_confidence",
    ):
        _require_builtin_string(
            getattr(graph_result, field_name),
            f"KnowledgeGraphResult字段{field_name}",
        )
    _require_graph_contract(
        graph_result.status == "ready",
        f"知识图谱状态不是ready：{graph_result.status}",
    )
    _require_graph_contract(
        graph_result.error_type is None and graph_result.error_message is None,
        "ready KnowledgeGraphResult的error_type/error_message必须严格为None",
    )
    _require_graph_contract(
        type(graph_result.active_paths) is tuple,
        "KnowledgeGraphResult active_paths必须是规范tuple元组类型",
    )
    for path in graph_result.active_paths:
        _require_risk_path_contract(path)
    _require_string_tuple(graph_result.root_evidence, "root_evidence根因索引")
    _require_string_tuple(
        graph_result.possible_consequences,
        "possible_consequences后果索引",
    )
    _require_string_tuple(graph_result.missing_evidence, "missing_evidence缺失索引")
    _require_graph_contract(
        type(graph_result.explanation_sections) is tuple,
        "explanation_sections必须是规范tuple元组类型",
    )
    for section in graph_result.explanation_sections:
        _require_explanation_section_contract(section)

    for field_name in (
        "product",
        "status",
        "alert_name",
        "price_source",
        "policy_version",
        "policy_parameter_hash",
        "transition_reason",
    ):
        _require_builtin_string(
            getattr(result, field_name),
            f"AgentResult字段{field_name}",
        )
    _require_graph_contract(
        type(result.alert_level) is int and 0 <= result.alert_level <= 3,
        "WarningState预警字段alert_level必须是0-3原生整数类型",
    )
    _require_graph_contract(
        type(result.alert_emitted) is bool,
        "WarningState预警字段alert_emitted必须是原生布尔类型",
    )
    _require_optional_builtin_float(
        result.risk_score,
        "WarningState预警字段risk_score",
    )
    _require_graph_contract(
        type(result.feature_evidence) is list,
        "Problem 1 FeatureEvidence集合必须是list类型",
    )
    for row in result.feature_evidence:
        _require_feature_evidence_contract(row)

    _require_graph_contract(
        graph_result.schema_version == KG_SCHEMA_VERSION,
        "知识图谱schema版本不是当前版本",
    )
    _require_graph_contract(
        graph_result.rule_version == KG_RULE_VERSION,
        "知识图谱rule版本不是当前版本",
    )
    _require_graph_contract(
        result.product == requested_product,
        "AgentResult品种product与请求不一致",
    )
    _require_graph_contract(
        isinstance(result.timestamp, pd.Timestamp)
        and result.timestamp == selected_time,
        "AgentResult时间timestamp与请求不一致",
    )
    _require_graph_contract(
        graph_result.product == requested_product
        and graph_result.product == result.product,
        "KnowledgeGraphResult品种product与请求或AgentResult不一致",
    )
    _require_graph_contract(
        isinstance(graph_result.timestamp, pd.Timestamp)
        and graph_result.timestamp == selected_time
        and graph_result.timestamp == result.timestamp,
        "KnowledgeGraphResult时间timestamp与请求或AgentResult不一致",
    )

    _strict_json_document(graph_result.graph_json, owner="graph payload")
    _strict_json_document(graph_result.active_paths, owner="path payload")
    _strict_json_document(
        {
            "sections": graph_result.explanation_sections,
            "text": graph_result.explanation_text,
            "confidence": graph_result.explanation_confidence,
        },
        owner="explanation payload",
    )
    _strict_json_document(graph_result.query_index, owner="query payload")

    try:
        graph = graph_from_node_link(graph_result.graph_json)
    except KnowledgeGraphError as error:
        raise AssertionError(
            f"知识图谱结构或时间验证失败：{error}"
        ) from error
    _require_graph_contract(
        graph.graph["schema_version"] == KG_SCHEMA_VERSION
        and graph.graph["schema_version"] == graph_result.schema_version,
        "graph schema身份与结果不一致",
    )
    _require_graph_contract(
        graph.graph["rule_version"] == KG_RULE_VERSION
        and graph.graph["rule_version"] == graph_result.rule_version,
        "graph rule身份与结果不一致",
    )
    _require_graph_contract(
        graph.graph["product"] == requested_product
        and graph.graph["product"] == result.product
        and graph.graph["product"] == graph_result.product,
        "graph品种product与请求、AgentResult或结果信封不一致",
    )
    _require_graph_contract(
        graph.graph["timestamp"] == selected_time
        and graph.graph["timestamp"] == result.timestamp
        and graph.graph["timestamp"] == graph_result.timestamp,
        "graph时间timestamp与请求、AgentResult或结果信封不一致",
    )

    for node_id, data in graph.nodes(data=True):
        source_time = data["source_timestamp"]
        _require_graph_contract(
            isinstance(source_time, pd.Timestamp) and source_time <= selected_time,
            f"节点{node_id}包含未来时间",
        )
        if data["node_type"] == NodeType.EVIDENCE.value:
            _require_graph_contract(
                source_time == selected_time,
                f"Evidence节点{node_id}必须使用所选时间",
            )
    for source, target, key, data in graph.edges(keys=True, data=True):
        source_time = data["source_timestamp"]
        _require_graph_contract(
            isinstance(source_time, pd.Timestamp) and source_time <= selected_time,
            f"边{key}（{source}->{target}）包含未来时间",
        )

    _require_graph_contract(
        type(graph_result.node_count) is int
        and graph_result.node_count == graph.number_of_nodes(),
        "知识图谱node count数量与重算结果不一致",
    )
    _require_graph_contract(
        type(graph_result.edge_count) is int
        and graph_result.edge_count == graph.number_of_edges(),
        "知识图谱edge count数量与重算结果不一致",
    )
    try:
        canonical_paths = tuple(discover_risk_paths(graph))
    except KnowledgeGraphError as error:
        raise AssertionError(f"知识图谱路径path推理失败：{error}") from error
    for path in graph_result.active_paths:
        _require_graph_contract(
            path.timestamp == selected_time,
            f"路径path {path.path_id}必须使用所选时间",
        )
        if (
            path.evidence_node_id in graph
            and path.conclusion_node_id in graph
            and graph.nodes[path.evidence_node_id].get("group") == "质量与流动性"
        ):
            _require_graph_contract(
                graph.nodes[path.conclusion_node_id]["node_type"]
                == NodeType.CONFIDENCE_STATE.value,
                "质量quality路径不得到达WarningState",
            )
    _require_graph_contract(
        type(graph_result.active_path_count) is int
        and graph_result.active_path_count == len(canonical_paths),
        "知识图谱path count路径数量与重算结果不一致",
    )
    _require_graph_contract(
        _same_exact_json_structure(graph_result.active_paths, canonical_paths),
        "知识图谱active_paths不是规范有序路径path或存在类型漂移",
    )

    expected_roots = tuple(dict.fromkeys(path.evidence_node_id for path in canonical_paths))
    expected_consequences = tuple(
        dict.fromkeys(
            path.conclusion_node_id
            for path in canonical_paths
            if graph.nodes[path.conclusion_node_id]["node_type"]
            == NodeType.RISK_CONSEQUENCE.value
        )
    )
    _require_graph_contract(
        _same_exact_json_structure(graph_result.root_evidence, expected_roots),
        "知识图谱root根因索引与规范路径不一致",
    )
    _require_graph_contract(
        _same_exact_json_structure(
            graph_result.possible_consequences,
            expected_consequences,
        ),
        "知识图谱consequence后果索引与规范路径不一致",
    )

    # Recompute the canonical query index without consuming the cached index.
    paths_to_alert = [
        path.path_id
        for path in canonical_paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.WARNING_STATE.value
    ]
    quality_path_ids = [
        path.path_id
        for path in canonical_paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.CONFIDENCE_STATE.value
    ]
    paths_from_anomaly: dict[str, list[str]] = {}
    for path in canonical_paths:
        paths_from_anomaly.setdefault(path.anomaly_node_id, []).append(path.path_id)
    expected_query_index = {
        "root_evidence": list(expected_roots),
        "paths_to_alert": paths_to_alert,
        "possible_consequences": list(expected_consequences),
        "quality_limitations": quality_path_ids,
        "paths_from_anomaly": paths_from_anomaly,
    }
    _require_graph_contract(
        _same_exact_json_structure(graph_result.query_index, expected_query_index),
        "知识图谱query查询索引与实际图不一致",
    )

    _, snapshot = _one_graph_node(graph, NodeType.RISK_SNAPSHOT)
    _strict_json_document(result.data_quality, owner="Problem 1 data quality")
    _require_graph_contract(
        _strict_json_document(snapshot["data_quality"], owner="RiskSnapshot data quality")
        == _strict_json_document(result.data_quality, owner="Problem 1 data quality"),
        "RiskSnapshot快照数据质量与Problem 1不一致",
    )
    _require_graph_contract(
        snapshot["price_source"] == result.price_source,
        "RiskSnapshot快照价格来源与Problem 1不一致",
    )
    _require_graph_contract(
        snapshot["policy_version"] == result.policy_version,
        "RiskSnapshot快照策略版本与Problem 1不一致",
    )

    rules_by_feature = {rule.feature_name: rule for rule in FEATURE_RULES}
    problem_one_evidence: dict[str, FeatureEvidence] = {}
    for row in result.feature_evidence:
        _require_graph_contract(
            isinstance(row, FeatureEvidence),
            "Problem 1 Evidence包含非法记录",
        )
        _require_graph_contract(
            row.feature_name in rules_by_feature,
            f"Problem 1 Evidence包含未知证据{row.feature_name!r}",
        )
        _require_graph_contract(
            row.feature_name not in problem_one_evidence,
            f"Problem 1 Evidence包含重复证据{row.feature_name!r}",
        )
        problem_one_evidence[row.feature_name] = row
    finite_evidence = {
        name: row
        for name, row in problem_one_evidence.items()
        if _finite_number(row.current_value) is not None
    }
    expected_missing = tuple(
        rule.feature_name
        for rule in FEATURE_RULES
        if rule.feature_name not in finite_evidence
    )
    _require_graph_contract(
        graph_result.missing_evidence == expected_missing,
        "知识图谱missing缺失证据与FEATURE_RULES规范顺序不一致",
    )
    graph_evidence = {
        data["feature_name"]: data
        for _, data in graph.nodes(data=True)
        if data["node_type"] == NodeType.EVIDENCE.value
    }
    _require_graph_contract(
        set(graph_evidence) == set(finite_evidence),
        "图谱Evidence证据与Problem 1有限值证据不一致或存在伪造证据",
    )
    for feature_name, row in finite_evidence.items():
        node = graph_evidence[feature_name]
        expected_values = {
            "label": row.label,
            "group": row.group,
            "current_value": _finite_number(row.current_value),
            "reference_value": _finite_number(row.reference_value),
            "pressure_ratio": _finite_number(row.pressure_ratio),
            "change_rate": _finite_number(row.change_rate),
            "status": row.status,
            "source": result.price_source,
        }
        for field_name, expected_value in expected_values.items():
            _require_graph_contract(
                node[field_name] == expected_value,
                f"Evidence证据{feature_name}的{field_name}与Problem 1不一致",
            )

    warning_node_id, warning = _one_graph_node(graph, NodeType.WARNING_STATE)
    raw_warning_rows = [
        row
        for row in graph_result.graph_json["nodes"]
        if row.get("node_id") == warning_node_id
        and row.get("node_type") == NodeType.WARNING_STATE.value
    ]
    _require_graph_contract(
        len(raw_warning_rows) == 1,
        "知识图谱原始payload必须恰有一个对应WarningState节点",
    )
    raw_warning = raw_warning_rows[0]
    warning_expectations = {
        "alert_level": result.alert_level,
        "alert_name": result.alert_name,
        "risk_score": _finite_number(result.risk_score),
        "alert_emitted": result.alert_emitted,
        "transition_reason": result.transition_reason,
        "policy_hash": result.policy_parameter_hash,
    }
    for field_name, expected_value in warning_expectations.items():
        _require_graph_contract(
            _same_exact_json_structure(raw_warning[field_name], expected_value)
            and _same_exact_json_structure(warning[field_name], expected_value),
            f"WarningState预警字段{field_name}与Problem 1不一致",
        )
    _require_graph_contract(
        graph.graph["policy_parameter_hash"] == result.policy_parameter_hash,
        "graph策略参数哈希与Problem 1不一致",
    )
    _require_graph_contract(
        graph.graph["policy_parameters"]["policy_version"] == result.policy_version,
        "graph策略版本与Problem 1不一致",
    )

    alert_paths = [
        path
        for path in canonical_paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.WARNING_STATE.value
    ]
    quality_paths = [
        path
        for path in canonical_paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.CONFIDENCE_STATE.value
    ]
    for path in alert_paths:
        _require_graph_contract(
            graph.nodes[path.evidence_node_id]["group"] != "质量与流动性",
            "质量quality路径不得作为WarningState预警支持",
        )
    if result.alert_level in {2, 3}:
        _require_graph_contract(
            bool(alert_paths),
            "2/3级预警必须至少有一条市场风险预警路径alert path",
        )

    try:
        sections, explanation_text, explanation_confidence = render_graph_explanation(
            graph,
            canonical_paths,
        )
    except (KnowledgeGraphError, UnsafeGraphExplanationError) as error:
        raise AssertionError(f"知识图谱规范解释生成失败：{error}") from error
    _require_graph_contract(
        tuple((section.section_id, section.title) for section in sections)
        == (
            ("conclusion", "当前结论"),
            ("root_evidence", "直接数据根因"),
            ("propagation", "风险传导过程"),
            ("consequences", "可能后果"),
            ("limitations", "可信度与限制"),
        ),
        "知识图谱解释不是规范五段式",
    )
    _require_graph_contract(
        _same_exact_json_structure(
            graph_result.explanation_sections,
            tuple(sections),
        ),
        "知识图谱explanation解释段落不是重新渲染的规范结果",
    )
    _require_graph_contract(
        graph_result.explanation_text == explanation_text,
        "知识图谱explanation解释全文不是重新渲染的规范结果",
    )
    _require_graph_contract(
        graph_result.explanation_confidence == explanation_confidence,
        "知识图谱explanation confidence解释置信度不一致",
    )

    try:
        service = GraphQueryService(graph_result)
        root_records = service.root_evidence(limit=3)
        alert_records = service.paths_to_alert()
        consequence_records = service.possible_consequences()
        quality_records = service.quality_limitations()
        node_records = [service.inspect_node(node_id) for node_id in sorted(graph.nodes)]
        anomaly_records = {
            node_id: service.paths_from_anomaly(node_id)
            for node_id, data in sorted(graph.nodes(data=True))
            if data["node_type"] == NodeType.ANOMALY.value
        }
    except KnowledgeGraphError as error:
        raise AssertionError(f"知识图谱query查询契约验证失败：{error}") from error
    query_outputs = {
        "root_evidence": root_records,
        "paths_to_alert": alert_records,
        "possible_consequences": consequence_records,
        "quality_limitations": quality_records,
        "inspect_node": node_records,
        "paths_from_anomaly": anomaly_records,
    }
    _strict_json_document(query_outputs, owner="query output")
    query_record_counts = {
        "root_evidence": len(root_records),
        "paths_to_alert": len(alert_records),
        "possible_consequences": len(consequence_records),
        "quality_limitations": len(quality_records),
        "inspect_node": len(node_records),
        "paths_from_anomaly": sum(len(rows) for rows in anomaly_records.values()),
    }

    return {
        "status": "ready",
        "product": result.product,
        "timestamp": selected_time.isoformat(),
        "schema_version": graph_result.schema_version,
        "rule_version": graph_result.rule_version,
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "active_path_count": len(canonical_paths),
        "alert_path_count": len(alert_paths),
        "quality_path_count": len(quality_paths),
        "missing_evidence_count": len(expected_missing),
        "explanation_status": "canonical",
        "explanation_confidence": explanation_confidence,
        "query_record_counts": query_record_counts,
    }


def validate_public_agent_surface() -> dict[str, Any]:
    """Verify that the package exposes one, and only one, business Agent class."""

    import option_risk

    agent_classes = sorted(
        name
        for name, value in inspect.getmembers(option_risk, inspect.isclass)
        if name.endswith("Agent")
    )
    return {
        "agent_classes": agent_classes,
        "passed": agent_classes == ["OptionRiskAgent"],
    }


def validate_agent_result(
    result: AgentResult,
    requested_product: str,
    requested_timestamp: pd.Timestamp,
) -> dict[str, Any]:
    """Assert the complete competition Problem 1 response contract."""

    requested_timestamp = pd.Timestamp(requested_timestamp)
    surface_metrics = set(result.surfaces)
    feature_groups = {item.group for item in result.feature_evidence}
    issues: list[str] = []
    if result.product != requested_product:
        issues.append(f"返回品种{result.product!r}与请求{requested_product!r}不一致")
    if result.timestamp != requested_timestamp:
        issues.append(f"返回时间{result.timestamp}与请求{requested_timestamp}不一致")
    if result.status != "ready":
        issues.append(f"结果状态不是ready：{result.status}")
    if surface_metrics != EXPECTED_SURFACES:
        missing = sorted(EXPECTED_SURFACES - surface_metrics)
        extra = sorted(surface_metrics - EXPECTED_SURFACES)
        issues.append(f"曲面集合不完整，缺少{missing}，多出{extra}")
    if feature_groups != EXPECTED_FEATURE_GROUPS:
        missing = sorted(EXPECTED_FEATURE_GROUPS - feature_groups)
        extra = sorted(feature_groups - EXPECTED_FEATURE_GROUPS)
        issues.append(f"风险特征组不完整，缺少{missing}，多出{extra}")
    if result.alert_level not in {0, 1, 2, 3}:
        issues.append(f"预警等级越界：{result.alert_level}")
    if not result.trigger_reasons:
        issues.append("缺少可解释触发原因")
    if result.timeline.empty:
        issues.append("缺少过去时点预警时间轴")
    elif pd.Timestamp(result.timeline.index.max()) > requested_timestamp:
        issues.append("预警时间轴包含所选时间之后的数据")
    else:
        timeline = result.timeline.sort_index()
        last = timeline.iloc[-1]
        if "alert_level" not in timeline:
            issues.append("预警时间轴缺少alert_level")
        elif int(last["alert_level"]) != result.alert_level:
            issues.append(
                f"时间轴末行预警等级{int(last['alert_level'])}与顶层{result.alert_level}不一致"
            )
        if "alert_emitted" not in timeline:
            issues.append("预警时间轴缺少新发通知标记")
        elif bool(last["alert_emitted"]) is not result.alert_emitted:
            issues.append("时间轴末行新发通知标记与顶层不一致")
        for column, current_value, label in [
            ("policy_version", result.policy_version, "策略版本"),
            ("policy_parameter_hash", result.policy_parameter_hash, "策略参数哈希"),
        ]:
            if not current_value:
                issues.append(f"顶层缺少{label}")
            elif column not in timeline:
                issues.append(f"预警时间轴缺少{label}")
            elif not timeline[column].eq(current_value).all():
                issues.append(f"时间轴{label}与顶层不一致")
        if not result.transition_reason:
            issues.append("顶层缺少迁移原因")
        elif "transition_reason" not in timeline:
            issues.append("预警时间轴缺少迁移原因")
        elif str(last["transition_reason"]) != result.transition_reason:
            issues.append("时间轴末行迁移原因与顶层不一致")
    for metric, surface in result.surfaces.items():
        if surface.timestamp != requested_timestamp:
            issues.append(f"{metric}曲面时间与请求时间不一致")
        if surface.values.shape != (
            len(surface.time_to_expiry),
            len(surface.log_moneyness),
        ):
            issues.append(f"{metric}曲面网格维度不一致")
    if issues:
        raise AssertionError("；".join(issues))
    return {
        "product": result.product,
        "timestamp": result.timestamp.isoformat(),
        "status": result.status,
        "alert_level": int(result.alert_level),
        "alert_name": result.alert_name,
        "alert_emitted": bool(result.alert_emitted),
        "surface_metrics": sorted(surface_metrics),
        "feature_groups": sorted(feature_groups),
        "evidence_count": len(result.feature_evidence),
        "reason_count": len(result.trigger_reasons),
        "timeline_rows": len(result.timeline),
        "price_source": result.price_source,
        "evaluation_available": bool(result.evaluation and result.evaluation.available),
        "policy_version": result.policy_version,
        "policy_parameter_hash": result.policy_parameter_hash,
        "transition_reason": result.transition_reason,
    }


def _canonical_graph_audit_document(result: AgentResult) -> str:
    """Independently restore and serialize every judge-facing graph view."""

    graph_result = result.knowledge_graph
    _require_graph_contract(
        isinstance(graph_result, KnowledgeGraphResult),
        "确定性检查缺少KnowledgeGraphResult",
    )
    graph = graph_from_node_link(graph_result.graph_json)
    paths = tuple(discover_risk_paths(graph))
    sections, text, confidence = render_graph_explanation(graph, paths)
    service = GraphQueryService(graph_result)
    queries = {
        "root_evidence": service.root_evidence(limit=3),
        "paths_to_alert": service.paths_to_alert(),
        "possible_consequences": service.possible_consequences(),
        "quality_limitations": service.quality_limitations(),
        "inspect_node": [
            service.inspect_node(node_id) for node_id in sorted(graph.nodes)
        ],
        "paths_from_anomaly": {
            node_id: service.paths_from_anomaly(node_id)
            for node_id, data in sorted(graph.nodes(data=True))
            if data["node_type"] == NodeType.ANOMALY.value
        },
    }
    return _strict_json_document(
        {
            "graph": graph_to_node_link(graph),
            "result": {
                "status": graph_result.status,
                "schema_version": graph_result.schema_version,
                "rule_version": graph_result.rule_version,
                "product": graph_result.product,
                "timestamp": graph_result.timestamp,
                "node_count": graph_result.node_count,
                "edge_count": graph_result.edge_count,
                "active_path_count": graph_result.active_path_count,
                "active_paths": paths,
                "root_evidence": graph_result.root_evidence,
                "possible_consequences": graph_result.possible_consequences,
                "missing_evidence": graph_result.missing_evidence,
                "query_index": graph_result.query_index,
            },
            "queries": queries,
            "explanation": {
                "sections": sections,
                "text": text,
                "confidence": confidence,
            },
        },
        owner="deterministic graph audit",
    )


def _result_has_no_future_graph_data(result: AgentResult) -> bool:
    graph_result = result.knowledge_graph
    _require_graph_contract(
        isinstance(graph_result, KnowledgeGraphResult),
        "无未来检查缺少KnowledgeGraphResult",
    )
    selected_time = result.timestamp
    graph = graph_from_node_link(graph_result.graph_json)
    paths = tuple(discover_risk_paths(graph))
    node_checks = [
        isinstance(data["source_timestamp"], pd.Timestamp)
        and data["source_timestamp"] <= selected_time
        and (
            data["node_type"] != NodeType.EVIDENCE.value
            or data["source_timestamp"] == selected_time
        )
        for _, data in graph.nodes(data=True)
    ]
    edge_checks = [
        isinstance(data["source_timestamp"], pd.Timestamp)
        and data["source_timestamp"] <= selected_time
        for _, _, _, data in graph.edges(keys=True, data=True)
    ]
    path_checks = [path.timestamp == selected_time for path in paths]
    return all((*node_checks, *edge_checks, *path_checks))


def _future_fixture_rows(
    product: str,
    timestamps: pd.DatetimeIndex,
    *,
    first_bar: int,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for offset, timestamp in enumerate(timestamps):
        bar = first_bar + offset
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
                        "gamma": 0.001
                        + 0.004 * np.exp(-15 * log_moneyness**2),
                        "theta": -0.01 - 0.00001 * bar,
                        "vega": 0.08
                        * np.sqrt(dte / 365)
                        * (1 + 0.0001 * bar),
                        "dte": dte,
                        "moneyness": moneyness,
                        "moneyness_type": (
                            "ATM" if abs(log_moneyness) <= 0.03 else "OTM"
                        ),
                        "date": timestamp.date(),
                    }
                )
    return pd.DataFrame(rows)


def _write_future_fixture_partition(
    source: Path,
    product: str,
    frame: pd.DataFrame,
    month: pd.Timestamp,
) -> Path:
    path = (
        source
        / "期权课题"
        / "archive"
        / "SF"
        / f"{product}2506"
        / "options"
        / month.strftime("%Y")
        / month.strftime("%m")
        / f"options_{month:%Y%m}.parquet"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=False)
    return path


def _future_append_rejection_fixture() -> bool:
    """Re-run the real Agent at one history point after a future-only partition."""

    try:
        with tempfile.TemporaryDirectory(prefix="option-risk-no-future-") as temp_name:
            root = Path(temp_name)
            source = root / "source"
            product = "ag"
            historical_times = pd.date_range(
                "2025-01-02 09:00",
                periods=120,
                freq="15min",
            )
            january_path = _write_future_fixture_partition(
                source,
                product,
                _future_fixture_rows(product, historical_times, first_bar=0),
                historical_times[0],
            )
            january_before = january_path.read_bytes()
            selected_timestamp = historical_times[-1]

            before_agent = OptionRiskAgent(
                AgentConfig(
                    data_source=source,
                    cache_dir=root / "cache-before",
                    output_dir=root / "output-before",
                )
            )
            before_result = before_agent.analyze(product, selected_timestamp)
            validate_agent_result(before_result, product, selected_timestamp)
            validate_knowledge_graph_result(
                before_result,
                product,
                selected_timestamp,
            )

            future_time = pd.DatetimeIndex([pd.Timestamp("2025-02-03 09:00")])
            future_path = _write_future_fixture_partition(
                source,
                product,
                _future_fixture_rows(
                    product,
                    future_time,
                    first_bar=len(historical_times),
                ),
                future_time[0],
            )
            after_agent = OptionRiskAgent(
                AgentConfig(
                    data_source=source,
                    cache_dir=root / "cache-after",
                    output_dir=root / "output-after",
                )
            )
            after_result = after_agent.analyze(product, selected_timestamp)
            validate_agent_result(after_result, product, selected_timestamp)
            validate_knowledge_graph_result(
                after_result,
                product,
                selected_timestamp,
            )

            before_graph = _strict_json_document(
                before_result.knowledge_graph,
                owner="before future replay KnowledgeGraphResult",
            )
            after_graph = _strict_json_document(
                after_result.knowledge_graph,
                owner="after future replay KnowledgeGraphResult",
            )
            before_audit = _canonical_graph_audit_document(before_result)
            after_audit = _canonical_graph_audit_document(after_result)
            return (
                january_path.read_bytes() == january_before
                and future_path.is_file()
                and before_graph == after_graph
                and before_audit == after_audit
            )
    except Exception:
        return False


def _executed_global_graph_checks(
    successful_results: list[tuple[str, AgentResult]],
    *,
    total_products: int,
) -> dict[str, dict[str, Any]]:
    successful_count = len(successful_results)
    complete = total_products > 0 and successful_count == total_products

    deterministic_records: list[bool] = []
    for _, result in successful_results:
        first = _canonical_graph_audit_document(result)
        second = _canonical_graph_audit_document(result)
        deterministic_records.append(first == second)

    no_future_records = [
        _result_has_no_future_graph_data(result)
        for _, result in successful_results
    ]
    no_future_records.append(_future_append_rejection_fixture())

    safety_records: list[bool] = []
    for _, result in successful_results:
        graph_result = result.knowledge_graph
        _require_graph_contract(
            isinstance(graph_result, KnowledgeGraphResult),
            "解释安全检查缺少KnowledgeGraphResult",
        )
        try:
            validate_explanation_language(graph_result.explanation_text)
        except UnsafeGraphExplanationError:
            safety_records.append(False)
        else:
            safety_records.append(True)
    for approved_phrase in (
        "不提供交易建议。",
        "不预测标的价格涨跌方向。",
    ):
        try:
            validate_explanation_language(approved_phrase)
        except UnsafeGraphExplanationError:
            safety_records.append(False)
        else:
            safety_records.append(True)
    for unsafe_phrase in (
        "建议买入",
        "建议卖出",
        "建议做多",
        "建议做空",
        "一定上涨",
        "一定下跌",
        "必然导致",
    ):
        unsafe_rejected = False
        try:
            validate_explanation_language(unsafe_phrase)
        except UnsafeGraphExplanationError:
            unsafe_rejected = True
        safety_records.append(unsafe_rejected)

    return {
        "deterministic": {
            "passed": complete and all(deterministic_records),
            "checked_count": len(deterministic_records),
            "scope": (
                f"成功图谱{successful_count}/{total_products}；"
                "每个图谱重复独立恢复，并比较图、路径、查询与解释的规范序列化"
            ),
        },
        "no_future": {
            "passed": complete and all(no_future_records),
            "checked_count": len(no_future_records),
            "scope": (
                f"成功图谱{successful_count}/{total_products}；审计节点、边和路径未来信息，"
                "并执行1个真实OptionRiskAgent同历史时点、"
                "追加未来记录且写入新月份分区的回放fixture"
            ),
        },
        "content_safety": {
            "passed": complete and all(safety_records),
            "checked_count": len(safety_records),
            "scope": (
                f"成功图谱{successful_count}/{total_products}；逐个验证生成解释的语言安全，"
                "并执行7个不安全与2个安全限制措辞fixture"
            ),
        },
    }


def validate_knowledge_graph_deployment(
    agent: OptionRiskAgent,
    *,
    product_codes: list[str] | None = None,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Run formal Problem 1 + Problem 2 validation for each selected product."""

    public_surface = validate_public_agent_surface()
    available = {item.code: item for item in agent.list_products()}
    selected = sorted(list(product_codes) if product_codes is not None else available)
    rows: list[dict[str, Any]] = []
    successful_results: list[tuple[str, AgentResult]] = []
    expected_failures = (AssertionError, OptionRiskAgentError, KnowledgeGraphError)
    for number, product in enumerate(selected, start=1):
        row: dict[str, Any] = {"product": product, "status": "failed"}
        try:
            if product not in available:
                raise AssertionError(f"数据目录不存在品种：{product}")
            timestamps = agent.list_timestamps(product)
            if len(timestamps) == 0:
                raise AssertionError("没有满足曲面和历史要求的可选时间点")
            selected_timestamp = timestamps[-1]
            row.update(
                {
                    "timestamp_count": len(timestamps),
                    "first_timestamp": timestamps[0].isoformat(),
                    "last_timestamp": selected_timestamp.isoformat(),
                }
            )
            result = agent.analyze(product, selected_timestamp)
            row["analysis"] = validate_agent_result(
                result,
                product,
                selected_timestamp,
            )
            graph_error: Exception | None = None
            try:
                row["knowledge_graph"] = validate_knowledge_graph_result(
                    result,
                    product,
                    selected_timestamp,
                )
            except Exception as error:
                graph_error = error
                row["knowledge_graph"] = {
                    "status": "failed",
                    "error_type": type(error).__name__,
                    "error": str(error),
                }
                row["error_type"] = type(error).__name__
                row["error"] = str(error)
            if graph_error is None:
                row["status"] = "passed"
                successful_results.append((product, result))
        except expected_failures as error:
            row["error_type"] = type(error).__name__
            row["error"] = str(error)
        rows.append(row)
        if progress is not None:
            progress(
                f"[{number}/{len(selected)}] {product}: {row['status']}"
                + (f" - {row.get('error')}" if row["status"] != "passed" else "")
            )

    global_checks = _executed_global_graph_checks(
        successful_results,
        total_products=len(rows),
    )
    passed_products = sum(row["status"] == "passed" for row in rows)
    global_checks_passed = (
        type(global_checks) is dict
        and MANDATORY_GLOBAL_CHECK_NAMES.issubset(global_checks)
        and all(
            type(check) is dict and check.get("passed") is True
            for check in global_checks.values()
        )
    )
    overall_passed = (
        public_surface["passed"]
        and bool(rows)
        and passed_products == len(rows)
        and global_checks_passed
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "full",
        "public_agent_surface": public_surface,
        "summary": {
            "status": "passed" if overall_passed else "failed",
            "product_count": len(rows),
            "passed_products": passed_products,
            "failed_products": len(rows) - passed_products,
        },
        "products": rows,
        "global_checks": global_checks,
    }


def validate_deployment(
    agent: OptionRiskAgent,
    *,
    analyze: bool = True,
    product_codes: list[str] | None = None,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Validate every catalog product and optionally run one full query per product."""

    public_surface = validate_public_agent_surface()
    available = {item.code: item for item in agent.list_products()}
    selected = sorted(product_codes or available)
    rows: list[dict[str, Any]] = []
    for number, product in enumerate(selected, start=1):
        row: dict[str, Any] = {"product": product, "status": "failed"}
        try:
            if product not in available:
                raise AssertionError(f"数据目录不存在品种：{product}")
            timestamps = agent.list_timestamps(product)
            if timestamps.empty:
                raise AssertionError("没有满足曲面和历史要求的可选时间点")
            row.update(
                {
                    "timestamp_count": len(timestamps),
                    "first_timestamp": timestamps[0].isoformat(),
                    "last_timestamp": timestamps[-1].isoformat(),
                }
            )
            if analyze:
                result = agent.analyze(product, timestamps[-1])
                row["analysis"] = validate_agent_result(result, product, timestamps[-1])
            row["status"] = "passed"
        except Exception as exc:  # continue to audit the remaining products
            row["error_type"] = type(exc).__name__
            row["error"] = str(exc)
        rows.append(row)
        if progress is not None:
            progress(
                f"[{number}/{len(selected)}] {product}: {row['status']}"
                + (f" - {row.get('error')}" if row["status"] != "passed" else "")
            )
    passed_products = sum(row["status"] == "passed" for row in rows)
    overall_passed = public_surface["passed"] and passed_products == len(rows) and bool(rows)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "full" if analyze else "catalog",
        "public_agent_surface": public_surface,
        "summary": {
            "status": "passed" if overall_passed else "failed",
            "product_count": len(rows),
            "passed_products": passed_products,
            "failed_products": len(rows) - passed_products,
        },
        "products": rows,
    }
````

</details>
