---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_report.py>)

SHA-256：`de8cd63bee5138773e82bc9cbb4689a59fb3b710cfa3ce0ad34aea11ee0629ee`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
import csv
import hashlib
from html import escape
import json
import math
import os
from pathlib import Path
import re
import tempfile
from typing import Any

from option_risk.contracts import KnowledgeGraphResult
from option_risk.graph_queries import GraphQueryService
from option_risk.knowledge_schema import (
    FEATURE_RULES,
    KG_RULE_VERSION,
    KG_SCHEMA_VERSION,
    NodeType,
    RelationType,
)


MANDATORY_CHECKS = ("deterministic", "no_future", "content_safety")
EXPECTED_SCENARIOS = (
    "level_0",
    "level_1",
    "level_2",
    "level_3",
    "quality_limited",
)
SUMMARY_COLUMNS = (
    "target_status",
    "overall_mean",
    "clarity_mean",
    "evidence_mean",
    "logic_mean",
    "wording_mean",
    "safety_mean",
    "reviewer_count",
    "case_count",
    "value_count",
    "row_count",
    "reviewed_at_min",
    "reviewed_at_max",
)


def _reject_constant(value: str) -> object:
    raise ValueError(f"Non-standard JSON constant: {value}")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=_reject_constant,
    )
    if type(payload) is not dict:
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def _strict_int(value: object, *, field: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{field} must be an integer >= {minimum}")
    return value


def _nonempty(value: object, *, field: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _reconcile_acceptance(payload: dict[str, Any]) -> dict[str, Any]:
    products = payload.get("products")
    summary = payload.get("summary")
    public = payload.get("public_agent_surface")
    if type(products) is not list or len(products) != 35:
        raise ValueError("Formal acceptance must contain exactly 35 product rows")
    if type(summary) is not dict or type(public) is not dict:
        raise ValueError("Formal acceptance summary/public Agent evidence is missing")
    if public.get("agent_classes") != ["OptionRiskAgent"] or public.get("passed") is not True:
        raise ValueError("Formal acceptance does not prove the single-Agent surface")

    product_codes: list[str] = []
    passed = 0
    failed = 0
    total_nodes = 0
    total_edges = 0
    total_paths = 0
    total_alert_paths = 0
    total_quality_paths = 0
    total_missing = 0
    normal_confidence = 0
    limited_confidence = 0
    for index, row in enumerate(products):
        if type(row) is not dict:
            raise ValueError(f"Product row {index} is not an object")
        product = _nonempty(row.get("product"), field=f"products[{index}].product")
        if product in product_codes:
            raise ValueError(f"Duplicate formal product: {product}")
        product_codes.append(product)
        status = row.get("status")
        if status == "passed":
            passed += 1
        else:
            failed += 1
        analysis = row.get("analysis")
        graph = row.get("knowledge_graph")
        if type(analysis) is not dict or type(graph) is not dict:
            raise ValueError(f"Formal product {product} is missing result objects")
        timestamp = _nonempty(analysis.get("timestamp"), field=f"{product}.timestamp")
        if (
            status != "passed"
            or analysis.get("status") != "ready"
            or analysis.get("product") != product
            or graph.get("status") != "ready"
            or graph.get("product") != product
            or graph.get("timestamp") != timestamp
            or graph.get("schema_version") != KG_SCHEMA_VERSION
            or graph.get("rule_version") != KG_RULE_VERSION
        ):
            raise ValueError(f"Formal product row does not reconcile: {product}")
        level = _strict_int(analysis.get("alert_level"), field=f"{product}.alert_level")
        if level not in {0, 1, 2, 3}:
            raise ValueError(f"Invalid alert level for {product}")
        total_nodes += _strict_int(graph.get("node_count"), field=f"{product}.nodes")
        total_edges += _strict_int(graph.get("edge_count"), field=f"{product}.edges")
        total_paths += _strict_int(
            graph.get("active_path_count"), field=f"{product}.paths"
        )
        total_alert_paths += _strict_int(
            graph.get("alert_path_count"), field=f"{product}.alert_paths"
        )
        total_quality_paths += _strict_int(
            graph.get("quality_path_count"), field=f"{product}.quality_paths"
        )
        total_missing += _strict_int(
            graph.get("missing_evidence_count"), field=f"{product}.missing"
        )
        confidence = graph.get("explanation_confidence")
        if confidence == "normal":
            normal_confidence += 1
        elif confidence == "limited":
            limited_confidence += 1
        else:
            raise ValueError(f"Unexpected explanation confidence for {product}")

    if product_codes != sorted(product_codes):
        raise ValueError("Formal products must retain deterministic sorted order")
    if (
        summary.get("status") != "passed"
        or summary.get("product_count") != len(products)
        or summary.get("passed_products") != passed
        or summary.get("failed_products") != failed
        or passed != 35
        or failed != 0
    ):
        raise ValueError("Formal acceptance summary conflicts with product rows")

    checks = payload.get("global_checks")
    if type(checks) is not dict or set(checks) != set(MANDATORY_CHECKS):
        raise ValueError("Formal acceptance must contain exactly three global checks")
    normalized_checks: dict[str, dict[str, Any]] = {}
    for name in MANDATORY_CHECKS:
        check = checks.get(name)
        if type(check) is not dict or check.get("passed") is not True:
            raise ValueError(f"Formal global check did not pass: {name}")
        count = _strict_int(check.get("checked_count"), field=f"{name}.count", minimum=1)
        scope = _nonempty(check.get("scope"), field=f"{name}.scope")
        normalized_checks[name] = {"passed": True, "checked_count": count, "scope": scope}

    return {
        "products": products,
        "product_count": len(products),
        "passed": passed,
        "failed": failed,
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "total_paths": total_paths,
        "total_alert_paths": total_alert_paths,
        "total_quality_paths": total_quality_paths,
        "total_missing": total_missing,
        "normal_confidence": normal_confidence,
        "limited_confidence": limited_confidence,
        "checks": normalized_checks,
        "generated_at": _nonempty(payload.get("generated_at"), field="generated_at"),
    }


def _reconcile_snapshot(
    payload: dict[str, Any],
    *,
    acceptance_sha256: str,
) -> list[dict[str, Any]]:
    if (
        payload.get("format_version") != "kg-snapshot-v1"
        or payload.get("schema_version") != KG_SCHEMA_VERSION
        or payload.get("rule_version") != KG_RULE_VERSION
        or payload.get("formal_acceptance_sha256") != acceptance_sha256
    ):
        raise ValueError("Representative snapshot identity does not match formal evidence")
    cases = payload.get("cases")
    if type(cases) is not list or len(cases) != 5:
        raise ValueError("Representative snapshot must contain exactly five cases")
    if [case.get("scenario") for case in cases] != list(EXPECTED_SCENARIOS):
        raise ValueError("Representative cases must retain the canonical scenario order")
    if payload.get("case_count") != len(cases):
        raise ValueError("Representative case count does not reconcile")
    real_count = 0
    synthetic_count = 0
    case_ids: set[str] = set()
    for case in cases:
        if type(case) is not dict:
            raise ValueError("Representative case must be an object")
        case_id = _nonempty(case.get("case_id"), field="case_id")
        if case_id in case_ids:
            raise ValueError(f"Duplicate representative case: {case_id}")
        case_ids.add(case_id)
        origin = case.get("origin")
        if origin == "real":
            real_count += 1
        elif origin == "synthetic_contract":
            synthetic_count += 1
        else:
            raise ValueError(f"Invalid case origin: {origin!r}")
        graph_payload = case.get("graph")
        if type(graph_payload) is not dict:
            raise ValueError(f"Case {case_id} has no graph")
        graph = KnowledgeGraphResult.from_dict(graph_payload)
        service = GraphQueryService(graph)
        if (
            graph.product != case.get("product")
            or graph.timestamp.isoformat() != case.get("timestamp")
            or graph.schema_version != KG_SCHEMA_VERSION
            or graph.rule_version != KG_RULE_VERSION
        ):
            raise ValueError(f"Case {case_id} graph identity drift")
        level = _strict_int(case.get("alert_level"), field=f"{case_id}.alert_level")
        if level not in {0, 1, 2, 3}:
            raise ValueError(f"Case {case_id} alert level is invalid")
        query = case.get("query")
        if type(query) is not dict:
            raise ValueError(f"Case {case_id} query evidence is missing")
        if (
            query.get("root_evidence") != service.root_evidence(limit=3)
            or query.get("paths_to_alert") != service.paths_to_alert()
            or query.get("possible_consequences") != service.possible_consequences()
            or query.get("quality_limitations") != service.quality_limitations()
        ):
            raise ValueError(f"Case {case_id} preset query evidence drift")
        inspect = query.get("inspect_node")
        anomaly = query.get("paths_from_anomaly")
        if type(inspect) is not dict or inspect.get("record") != service.inspect_node(
            inspect.get("node_id")
        ):
            raise ValueError(f"Case {case_id} node-detail query drift")
        if type(anomaly) is not dict:
            raise ValueError(f"Case {case_id} anomaly query is missing")
        anomaly_id = anomaly.get("anomaly_id")
        expected_paths = service.paths_from_anomaly(anomaly_id) if anomaly_id else []
        if anomaly.get("records") != expected_paths:
            raise ValueError(f"Case {case_id} anomaly-path query drift")

        explanation = case.get("explanation")
        if type(explanation) is not dict:
            raise ValueError(f"Case {case_id} explanation is missing")
        sections = [section.to_dict() for section in graph.explanation_sections]
        active_ids = {path.path_id for path in graph.active_paths}
        referenced = {
            path_id for section in sections for path_id in section.get("path_ids", [])
        }
        if (
            explanation.get("sections") != sections
            or explanation.get("text") != graph.explanation_text
            or explanation.get("confidence") != graph.explanation_confidence
            or explanation.get("traceability_passed") is not True
            or not referenced <= active_ids
        ):
            raise ValueError(f"Case {case_id} explanation is not traceable")

    if (
        payload.get("real_case_count") != real_count
        or payload.get("synthetic_contract_case_count") != synthetic_count
        or real_count != 4
        or synthetic_count != 1
        or cases[3]["origin"] != "synthetic_contract"
        or cases[3]["alert_level"] != 3
        or any(cases[index]["origin"] != "real" for index in (0, 1, 2, 4))
    ):
        raise ValueError("Real/synthetic scenario accounting is not honest")
    return cases


def _load_review_summary(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != SUMMARY_COLUMNS:
            raise ValueError("Human review summary columns are not canonical")
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError("Human review summary must contain exactly one row")
    row = rows[0]
    means: dict[str, float] = {}
    for field in ("overall_mean", "clarity_mean", "evidence_mean", "logic_mean", "wording_mean", "safety_mean"):
        try:
            value = float(row[field])
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid human review value: {field}") from error
        if not math.isfinite(value) or not 1 <= value <= 5:
            raise ValueError(f"Human review value out of range: {field}")
        means[field] = value
    counts: dict[str, int] = {}
    for field in ("reviewer_count", "case_count", "value_count", "row_count"):
        try:
            value = int(row[field])
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid human review count: {field}") from error
        if str(value) != row[field].strip() or value <= 0:
            raise ValueError(f"Invalid human review count: {field}")
        counts[field] = value
    dimension_mean = sum(
        means[f"{name}_mean"] for name in ("clarity", "evidence", "logic", "wording", "safety")
    ) / 5
    if (
        not math.isclose(means["overall_mean"], dimension_mean, abs_tol=1e-12)
        or counts["value_count"] != counts["row_count"] * 5
        or counts["reviewer_count"] > counts["row_count"]
        or counts["case_count"] > counts["row_count"]
        or row["target_status"]
        != ("passed" if means["overall_mean"] >= 4.0 else "failed")
        or not row["reviewed_at_min"].strip()
        or not row["reviewed_at_max"].strip()
    ):
        raise ValueError("Human review summary arithmetic does not reconcile")
    return {**row, **means, **counts}


def _fmt_number(value: int | float) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    return f"{value:.3f}"


def _node_records(case: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row["node_id"]): row
        for row in case["graph"]["graph_json"]["nodes"]
    }


def _svg_label(label: object, limit: int = 12) -> tuple[str, str]:
    text = str(label)
    if len(text) <= limit:
        return text, ""
    return text[:limit], text[limit : limit * 2]


def _representative_svg(case: dict[str, Any]) -> str:
    paths = case["graph"]["active_paths"][:3]
    nodes = _node_records(case)
    height = max(250, 100 + len(paths) * 100)
    column_x = (115, 360, 605, 850)
    layer_names = ("Evidence", "Anomaly", "Mechanism", "Conclusion")
    parts = [
        f'<svg class="graph-svg" viewBox="0 0 970 {height}" role="img" '
        f'aria-label="{escape(str(case["product"]), quote=True)} 四层风险传导图，最多三条活动路径">',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" '
        'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L8,3 z" fill="#536272"/></marker></defs>',
    ]
    for x, name in zip(column_x, layer_names, strict=True):
        parts.append(
            f'<text x="{x}" y="30" text-anchor="middle" class="svg-layer">{name}</text>'
        )
    for track, path in enumerate(paths):
        y = 90 + track * 100
        path_nodes = (
            path["evidence_node_id"],
            path["anomaly_node_id"],
            path["mechanism_node_id"],
            path["conclusion_node_id"],
        )
        for left, right in zip(column_x[:-1], column_x[1:], strict=True):
            parts.append(
                f'<line x1="{left + 88}" y1="{y}" x2="{right - 88}" y2="{y}" '
                'stroke="#536272" stroke-width="2" marker-end="url(#arrow)"/>'
            )
        for position, (x, node_id) in enumerate(zip(column_x, path_nodes, strict=True)):
            record = nodes[node_id]
            first, second = _svg_label(record.get("label", node_id))
            fill = "#f7c873" if position == 3 else "#dbeafe"
            stroke = "#8a6420" if position == 3 else "#235a97"
            parts.append(
                f'<g aria-label="{escape(str(record.get("node_type")), quote=True)}: '
                f'{escape(str(record.get("label")), quote=True)}">'
                f'<rect x="{x - 88}" y="{y - 31}" width="176" height="62" rx="8" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
                f'<text x="{x}" y="{y - (4 if second else -3)}" text-anchor="middle" class="svg-node">'
                f"{escape(first)}"
            )
            if second:
                parts.append(
                    f'<tspan x="{x}" dy="18">{escape(second)}</tspan>'
                )
            parts.append("</text></g>")
    if not paths:
        parts.append(
            '<text x="485" y="125" text-anchor="middle" class="svg-empty">该真实0级案例没有活动异常路径</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _representative_mobile(case: dict[str, Any]) -> str:
    nodes = _node_records(case)
    cards: list[str] = []
    for index, path in enumerate(case["graph"]["active_paths"][:3], start=1):
        path_nodes = (
            ("Evidence", path["evidence_node_id"]),
            ("Anomaly", path["anomaly_node_id"]),
            ("Mechanism", path["mechanism_node_id"]),
            ("Conclusion", path["conclusion_node_id"]),
        )
        steps = '<span class="mobile-arrow">↓</span>'.join(
            f'<div class="mobile-node"><small>{escape(layer)}</small>'
            f'<strong>{escape(str(nodes[node_id].get("label", node_id)))}</strong></div>'
            for layer, node_id in path_nodes
        )
        cards.append(
            f'<article class="mobile-path"><div class="mono">路径 {index}</div>{steps}</article>'
        )
    return '<div class="graph-mobile">' + "".join(cards) + "</div>"


def _requirement_rows() -> str:
    rows = (
        ("读取曲面与Greeks", "同一 OptionRiskAgent 保留问题1五张曲面和12项FeatureEvidence", "已实现"),
        ("构建风险知识图谱", "NetworkX MultiDiGraph；Schema与规则均有版本", "已实现"),
        ("风险关联与传播", "Evidence→Anomaly→Mechanism→Conclusion 四层确定性路径", "已实现"),
        ("动态预警", "图谱只解释问题1的0—3级结果，不改写等级", "已实现"),
        ("可解释推理", "固定五段解释；每句路径前缀可回查", "已实现"),
        ("自适应优化", "本方案未启用；避免在缺乏真实反馈时伪造闭环", "可选项未启用"),
        ("人工解释评分", "已生成空白评分模板；需真实评审人完成", "待完成"),
    )
    return "".join(
        f'<tr><td data-label="要求">{escape(requirement)}</td>'
        f'<td data-label="交付证据">{escape(evidence)}</td>'
        f'<td data-label="状态">{escape(status)}</td></tr>'
        for requirement, evidence, status in rows
    )


def _schema_rows() -> str:
    node_descriptions = {
        NodeType.PRODUCT: "品种上下文",
        NodeType.RISK_SNAPSHOT: "所选时点与问题1结果",
        NodeType.EVIDENCE: "12项当前值、阈值和压力证据",
        NodeType.ANOMALY: "规则定义的异常或临界状态",
        NodeType.MECHANISM: "谨慎措辞的风险作用机理",
        NodeType.RISK_CONSEQUENCE: "可能风险后果，不含方向预测",
        NodeType.WARNING_STATE: "问题1原始0—3级状态",
        NodeType.CONFIDENCE_STATE: "质量证据对解释置信度的限制",
    }
    return "".join(
        f'<tr><td data-label="节点类型">{escape(node.value)}</td>'
        f'<td data-label="职责">{escape(description)}</td></tr>'
        for node, description in node_descriptions.items()
    )


def _mapping_rows() -> str:
    return "".join(
        "<tr>"
        f'<td data-label="#">{rule.order}</td>'
        f'<td data-label="问题1 Evidence"><code>{escape(rule.feature_name)}</code><br>{escape(rule.label)}</td>'
        f'<td data-label="Anomaly">{escape(rule.anomaly)}</td>'
        f'<td data-label="Mechanism">{escape(rule.mechanism)}</td>'
        f'<td data-label="Conclusion">{escape(rule.conclusion)}</td>'
        f'<td data-label="语义边界">{escape(rule.boundary)}</td>'
        f'<td data-label="规则ID"><code>{escape(rule.rule_id)}</code></td>'
        "</tr>"
        for rule in FEATURE_RULES
    )


def _case_cards(cases: list[dict[str, Any]]) -> str:
    labels = {
        "level_0": "0级：无预警",
        "level_1": "1级：关注",
        "level_2": "2级：警告",
        "level_3": "3级：危险",
        "quality_limited": "质量受限：只降低解释置信度",
    }
    cards: list[str] = []
    for case in cases:
        origin = case["origin"]
        origin_label = "真实Agent案例" if origin == "real" else "合成契约案例"
        graph = case["graph"]
        synthetic_note = (
            "该案例只验证3级规则、查询与解释契约，不代表真实市场观测，也不计入35品种表现。"
            if origin == "synthetic_contract"
            else "该案例由真实数据经 OptionRiskAgent 生成。"
        )
        root_count = len(case["query"]["root_evidence"])
        cards.append(
            f'<article class="case-card" data-scenario="{escape(case["scenario"], quote=True)}" '
            f'data-origin="{escape(origin, quote=True)}">'
            f'<div class="case-head"><span class="tag">{escape(origin_label)}</span>'
            f'<span class="mono">{escape(case["case_id"])}</span></div>'
            f'<h3>{escape(labels[case["scenario"]])}</h3>'
            f'<p><strong>品种/时间：</strong>{escape(case["product"].upper())} / '
            f'{escape(case["timestamp"])}</p>'
            f'<p><strong>图谱：</strong>{graph["node_count"]}节点、{graph["edge_count"]}边、'
            f'{graph["active_path_count"]}条活动路径；根证据查询返回{root_count}条；'
            f'解释置信度 <code>{escape(graph["explanation_confidence"])}</code>。</p>'
            f'<p>{escape(synthetic_note)}</p>'
            f'<details><summary>查看五段解释</summary><pre>{escape(case["explanation"]["text"])}</pre></details>'
            "</article>"
        )
    return "".join(cards)


def _product_rows(products: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for row in products:
        analysis = row["analysis"]
        graph = row["knowledge_graph"]
        rows.append(
            f'<tr data-product="{escape(row["product"], quote=True)}">'
            f'<td data-label="品种"><code>{escape(row["product"])}</code></td>'
            f'<td data-label="所选时点">{escape(analysis["timestamp"])}</td>'
            f'<td data-label="预警">{analysis["alert_level"]} / {escape(analysis["alert_name"])}</td>'
            f'<td data-label="节点">{graph["node_count"]}</td>'
            f'<td data-label="边">{graph["edge_count"]}</td>'
            f'<td data-label="路径">{graph["active_path_count"]}</td>'
            f'<td data-label="预警路径">{graph["alert_path_count"]}</td>'
            f'<td data-label="质量路径">{graph["quality_path_count"]}</td>'
            f'<td data-label="置信度"><code>{escape(graph["explanation_confidence"])}</code></td>'
            "</tr>"
        )
    return "".join(rows)


def _check_cards(checks: dict[str, dict[str, Any]]) -> str:
    names = {
        "deterministic": "确定性",
        "no_future": "无未来数据",
        "content_safety": "内容安全",
    }
    return "".join(
        f'<article class="check-card"><span class="tag">PASS</span><h3>{escape(names[name])}</h3>'
        f'<p><strong>{check["checked_count"]}</strong> 次已执行检查</p>'
        f'<p>{escape(check["scope"])}</p><code>{escape(name)}</code></article>'
        for name, check in checks.items()
    )


def _review_panel(review: dict[str, Any] | None) -> str:
    if review is None:
        return (
            '<div class="review pending"><span class="tag">待验证</span>'
            '<h3>人工评分待完成</h3><p>已提供逐案例空白模板，但尚无真实评审人、评分和时间记录，'
            '因此不生成汇总，也不声称达到4.0/5.0硬门槛。</p></div>'
        )
    status = "达到门槛" if review["target_status"] == "passed" else "未达门槛"
    return (
        '<div class="review"><span class="tag">真实评分汇总</span>'
        f'<h3>{escape(status)}：{review["overall_mean"]:.2f}/5.00</h3>'
        f'<p>{review["reviewer_count"]}名评审人、{review["case_count"]}个案例、'
        f'{review["value_count"]}个有效维度评分。时间范围：'
        f'{escape(review["reviewed_at_min"])} 至 {escape(review["reviewed_at_max"])}。</p></div>'
    )


def _html_document(
    *,
    evidence: dict[str, Any],
    cases: list[dict[str, Any]],
    review: dict[str, Any] | None,
) -> str:
    representative = next(case for case in cases if case["scenario"] == "level_2")
    relations = " / ".join(relation.value for relation in RelationType)
    python_example = """from option_risk.graph_queries import GraphQueryService
graph = result.knowledge_graph
query = GraphQueryService(graph)
roots = query.root_evidence(limit=3)
paths = query.paths_to_alert()
consequences = query.possible_consequences()
quality = query.quality_limitations()"""
    cli_example = """python scripts/query_knowledge_graph.py --data-dir ./data/demo \\
  --product ag --timestamp "2025-04-07 10:15:00" --query root-evidence"""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>问题2 · 风险知识图谱验收报告</title>
<style>
:root{{--ink:#17212b;--muted:#596776;--line:#d9e1e8;--paper:#ffffff;--soft:#f4f7fa;--blue:#235a97;--blue-open:#dbeafe;--gold:#8a6420;--gold-open:#f7e4b8;}}
*{{box-sizing:border-box}} html{{background:#eef2f5;color:var(--ink);font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",Arial,sans-serif}}
body{{margin:0;line-height:1.65;overflow-x:hidden}} .page{{width:min(1180px,calc(100% - 32px));margin:24px auto;background:var(--paper);box-shadow:0 12px 42px rgba(23,33,43,.09)}}
header{{padding:46px 52px 34px;border-bottom:1px solid var(--line)}} .eyebrow{{color:var(--blue);font-weight:700;letter-spacing:.08em}} h1{{font-size:clamp(30px,4vw,52px);line-height:1.15;margin:10px 0 16px}} h2{{font-size:26px;line-height:1.3;margin:0 0 12px}} h3{{margin:8px 0;font-size:18px}} p{{margin:8px 0}} .lead{{font-size:18px;max-width:900px;color:var(--muted)}}
main{{padding:0 52px 48px}} section{{padding:38px 0;border-bottom:1px solid var(--line)}} section:last-child{{border-bottom:0}} .note{{color:var(--muted);max-width:920px}}
.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:22px}} .kpi{{background:var(--soft);border-left:4px solid var(--blue);padding:16px}} .kpi strong{{display:block;font:700 28px Consolas,monospace}} .kpi span{{color:var(--muted)}}
.architecture{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;align-items:stretch;margin-top:22px}} .arch{{border:1px solid var(--line);padding:15px;background:var(--soft);position:relative}} .arch:not(:last-child)::after{{content:"→";position:absolute;right:-13px;top:34%;z-index:2;color:var(--blue);font-weight:700}}
.table-wrap{{max-width:100%;overflow-x:auto;border:1px solid var(--line);margin-top:18px}} table{{border-collapse:collapse;width:100%;min-width:720px}} th,td{{padding:10px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);overflow-wrap:anywhere}} th{{background:var(--soft);position:sticky;top:0}} tr:last-child td{{border-bottom:0}} code,.mono{{font-family:Consolas,"SFMono-Regular",monospace;font-size:.92em;overflow-wrap:anywhere}}
.checks,.cases{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:20px}} .check-card,.case-card,.review{{border:1px solid var(--line);padding:18px;background:var(--paper)}} .case-card{{grid-column:span 1}} .case-head{{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}} .tag{{display:inline-block;background:var(--blue-open);color:var(--blue);padding:3px 8px;font-size:12px;font-weight:700;border-radius:999px}} .pending .tag{{background:var(--gold-open);color:var(--gold)}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--soft);border:1px solid var(--line);padding:14px;font:13px/1.6 Consolas,"SFMono-Regular",monospace}} summary{{cursor:pointer;color:var(--blue);font-weight:700}} .graph-frame{{border:1px solid var(--line);padding:12px;margin-top:18px;background:#fbfcfd}} .graph-svg{{display:block;width:100%;height:auto;max-height:460px}} .svg-layer{{font:700 15px Arial,sans-serif;fill:#17212b}} .svg-node{{font:13px "Microsoft YaHei","PingFang SC",sans-serif;fill:#17212b}} .svg-empty{{font:16px "Microsoft YaHei","PingFang SC",sans-serif;fill:#596776}} .graph-mobile{{display:none}} .mobile-path{{border:1px solid var(--line);padding:12px;background:#fff}} .mobile-node{{padding:10px;border-left:4px solid var(--blue);background:var(--blue-open)}} .mobile-node:last-child{{border-color:var(--gold);background:var(--gold-open)}} .mobile-node small,.mobile-node strong{{display:block}} .mobile-arrow{{display:block;text-align:center;color:var(--muted);font-weight:700}}
.limitations{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:0;list-style:none}} .limitations li{{border-left:4px solid var(--gold);background:#fffaf0;padding:14px}} footer{{padding:24px 52px;background:var(--soft);color:var(--muted);font-size:13px}}
@media (max-width: 900px){{.kpis{{grid-template-columns:repeat(2,minmax(0,1fr))}}.architecture{{grid-template-columns:1fr}}.arch:not(:last-child)::after{{content:"↓";right:50%;top:auto;bottom:-21px}}.checks,.cases{{grid-template-columns:1fr 1fr}}}}
@media (max-width: 430px){{.page{{width:100%;margin:0;box-shadow:none}}header,main,footer{{padding-left:18px;padding-right:18px}}header{{padding-top:28px}}section{{padding:28px 0}}.kpis,.checks,.cases,.limitations{{grid-template-columns:1fr}}.kpi strong{{font-size:24px}}.case-head{{display:block}}.graph-frame{{padding:8px}}.graph-svg{{display:none}}.graph-mobile{{display:grid;grid-template-columns:1fr;gap:12px}}.table-wrap{{overflow:visible;border:0}}table,tbody,tr,td{{display:block;width:100%;min-width:0}}thead{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}tbody tr{{border:1px solid var(--line);margin:0 0 12px;background:#fff}}td{{display:grid;grid-template-columns:minmax(88px,34%) minmax(0,1fr);gap:8px;padding:8px 10px;font-size:13px}}td::before{{content:attr(data-label);font-weight:700;color:var(--muted)}}}}
</style>
</head>
<body><div class="page">
<header><div class="eyebrow">宁证期货赛题 · 问题2 · 技术验收</div><h1>一个Agent，把风险证据连成可追溯知识图谱</h1>
<p class="lead">结论：问题1的正式预警结果保持不变；同一个 <code>OptionRiskAgent</code> 已增加版本化NetworkX图谱、固定查询和五段解释。正式证据覆盖35/35品种，确定性、无未来数据和内容安全检查均实际执行并通过。人工解释评分尚未由真实评审人完成，因此该硬门槛如实标记为待完成。</p></header>
<main>
<section><h2>技术摘要：35个品种全部形成可查询图谱</h2><p class="note">口径：每个品种取正式验收中的最后一个有效时点；节点、边和路径总数均由本报告从35行逐行重算，不读取预填总计。生成时间（UTC记录）：{escape(evidence['generated_at'])}。</p>
<div class="kpis"><div class="kpi"><strong>35/35</strong><span>正式品种通过</span></div><div class="kpi" data-total-nodes="{evidence['total_nodes']}"><strong>{_fmt_number(evidence['total_nodes'])}</strong><span>节点总数</span></div><div class="kpi" data-total-edges="{evidence['total_edges']}"><strong>{_fmt_number(evidence['total_edges'])}</strong><span>边总数</span></div><div class="kpi" data-total-paths="{evidence['total_paths']}"><strong>{_fmt_number(evidence['total_paths'])}</strong><span>活动路径总数</span></div></div></section>
<section><h2>赛题要求与证据一一对应</h2><div class="table-wrap"><table><thead><tr><th>要求</th><th>交付证据</th><th>状态</th></tr></thead><tbody>{_requirement_rows()}</tbody></table></div></section>
<section><h2>架构：用户入口不变，图谱只是同一结果的解释层</h2><div class="architecture"><div class="arch"><strong>品种</strong><br>数据中已有选项</div><div class="arch"><strong>有效时间点</strong><br>仅显示可分析时点</div><div class="arch"><strong>OptionRiskAgent</strong><br>问题1曲面、Greeks、预警</div><div class="arch"><strong>NetworkX四层图</strong><br>确定性规则传播</div><div class="arch"><strong>六个结果页签</strong><br>固定查询与解释</div></div><p class="note">没有第二个业务Agent、没有自由文本问答、没有图数据库服务，也没有用图谱改写0—3级预警。</p></section>
<section><h2>Schema与规则：12项证据映射完全注册</h2><p class="note"><code>schema_version={KG_SCHEMA_VERSION}</code>；<code>rule_version={KG_RULE_VERSION}</code>。节点类型覆盖上下文、四层路径、预警和置信度；关系全集为 <code>{escape(relations)}</code>。</p><div class="table-wrap"><table><thead><tr><th>节点类型</th><th>职责</th></tr></thead><tbody>{_schema_rows()}</tbody></table></div>
<div class="table-wrap"><table><thead><tr><th>#</th><th>问题1 Evidence</th><th>Anomaly</th><th>Mechanism</th><th>Conclusion</th><th>语义边界</th><th>规则ID</th></tr></thead><tbody>{_mapping_rows()}</tbody></table></div></section>
<section><h2>代表图：真实2级案例最多展示三条四层路径</h2><p class="note">图形只展示排序最高的三条活动路径，完整路径仍由查询服务返回。节点位置表示语义层，不表示因果强度或价格方向；蓝色表示前三层，金色表示结论层，且每列有直接文本标签，不依赖颜色识别。</p><div class="graph-frame">{_representative_svg(representative)}{_representative_mobile(representative)}</div><p class="mono">案例：{escape(representative['case_id'])} · {escape(representative['product'])} · {escape(representative['timestamp'])}</p></section>
<section><h2>0—3级与质量场景：真实和合成严格分开</h2><p class="note">真实0/1/2级和质量受限案例来自正式Agent；原始验收中没有3级最后时点，因此3级仅用形式化契约输入验证逻辑。合成案例不进入35品种通过率、事件指标或市场表现。</p><div class="cases">{_case_cards(cases)}</div></section>
<section><h2>固定查询：结果可由Python或命令行复核</h2><div class="cases"><article class="case-card"><h3>Python查询</h3><pre>{escape(python_example)}</pre></article><article class="case-card"><h3>命令行查询</h3><pre>{escape(cli_example)}</pre></article><article class="case-card"><h3>查询边界</h3><p>支持根证据、到预警路径、可能后果、质量限制、精确节点详情和指定异常的路径；不接受自由文本，不推断未注册关系。</p></article></div></section>
<section><h2>三项全局门禁均有执行次数与范围</h2><div class="checks">{_check_cards(evidence['checks'])}</div><p class="note">另外，35行合计包含{evidence['total_alert_paths']}条预警路径、{evidence['total_quality_paths']}条质量路径和{evidence['total_missing']}项缺失证据记录；解释置信度为normal的品种{evidence['normal_confidence']}个、limited的品种{evidence['limited_confidence']}个。</p></section>
<section><h2>完整35品种结果</h2><div class="table-wrap"><table><thead><tr><th>品种</th><th>所选时点</th><th>预警</th><th>节点</th><th>边</th><th>路径</th><th>预警路径</th><th>质量路径</th><th>置信度</th></tr></thead><tbody>{_product_rows(evidence['products'])}</tbody></table></div></section>
<section><h2>人工解释评分：不以程序冒充评审人</h2>{_review_panel(review)}<p class="note">正式口径是所有“评审人×案例×清晰性/证据充分性/逻辑完整性/措辞可信性/安全性”数值的算术平均，只有真实完整记录达到4.0/5.0才可标为通过。</p></section>
<section><h2>局限与安全边界直接约束解读</h2><ul class="limitations"><li><strong>直接数据根因：</strong>根节点是问题1的指标证据，不声称识别新闻、政策或宏观事件原因。</li><li><strong>质量置信度：</strong>质量路径只把解释置信度标为limited，不能提高市场风险等级。</li><li><strong>方向与建议：</strong>系统不预测标的涨跌方向，不提供交易建议或执行指令。</li><li><strong>价格代理：</strong>缺少独立期货行情时仍使用strike/moneyness重构标的代理；相关CVaR只能探索性解读。</li></ul></section>
<section><h2>复核与下一步</h2><p>评委可先运行02 Notebook，再用固定CLI复核任一品种/时间点。唯一尚未完成的正式硬门槛是真实人工解释评分；建议由3—5名独立评审人填写模板，运行汇总脚本后重新生成本报告。</p><h3>仍待回答的问题</h3><p>真实评审能否达到4.0/5.0，以及不同品种的解释清晰度是否存在系统性差异，必须等实际评分后回答；当前证据不作推断。</p></section>
</main><footer>证据源仅为 <code>outputs/knowledge_graph_acceptance_full.json</code>、<code>outputs/demo/knowledge_graph_snapshot.json</code> 与可选的真实人工评分汇总。报告为UTF-8自包含HTML，无脚本、CDN、网络链接或外部资源。</footer>
</div></body></html>"""


def _safe_html(html: str) -> None:
    lower = html.lower()
    if "<script" in lower or "http://" in lower or "https://" in lower:
        raise ValueError("Report contains a forbidden script or network reference")
    if re.search(r"<(?:link|iframe|object|embed)\b", lower):
        raise ValueError("Report contains a forbidden external-resource element")


def _atomic_write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return path


def build_report(
    acceptance_path: str | Path,
    snapshot_path: str | Path,
    output_path: str | Path,
    review_summary_path: str | Path | None = None,
) -> Path:
    """Reconcile formal evidence, then atomically publish a safe offline report."""

    acceptance_path = Path(acceptance_path)
    snapshot_path = Path(snapshot_path)
    acceptance = _load_json(acceptance_path)
    evidence = _reconcile_acceptance(acceptance)
    acceptance_sha = hashlib.sha256(acceptance_path.read_bytes()).hexdigest().upper()
    cases = _reconcile_snapshot(
        _load_json(snapshot_path),
        acceptance_sha256=acceptance_sha,
    )
    review = _load_review_summary(
        Path(review_summary_path) if review_summary_path is not None else None
    )
    html = _html_document(evidence=evidence, cases=cases, review=review)
    _safe_html(html)
    return _atomic_write(Path(output_path), html)


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build the Problem 2 offline report")
    parser.add_argument(
        "--acceptance",
        type=Path,
        default=project_root / "outputs" / "knowledge_graph_acceptance_full.json",
    )
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=project_root / "outputs" / "demo" / "knowledge_graph_snapshot.json",
    )
    parser.add_argument(
        "--review-summary",
        type=Path,
        default=project_root / "outputs" / "人工解释评分汇总.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "outputs" / "问题2-知识图谱验收报告.html",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    review_path = args.review_summary if args.review_summary.exists() else None
    output = build_report(args.acceptance, args.snapshot, args.output, review_path)
    print(f"Built self-contained report: {output}")
    if review_path is None:
        print("人工评分待完成")


if __name__ == "__main__":
    main()
````

</details>
