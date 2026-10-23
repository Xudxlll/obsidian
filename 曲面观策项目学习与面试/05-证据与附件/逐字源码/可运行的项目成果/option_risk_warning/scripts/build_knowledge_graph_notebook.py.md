---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_knowledge_graph_notebook.py>)

SHA-256：`ac2827a7fcf48c51e6f23fe0e40892a4842dbb88dab09b53af4975dcea50d2df`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import asdict, replace
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
from typing import Any, Iterator

import nbformat as nbf
from nbclient import NotebookClient
import pandas as pd

from option_risk import AgentConfig, OptionRiskAgent
from option_risk.contracts import AgentResult, FeatureEvidence, KnowledgeGraphResult
from option_risk.decision import ALERT_NAMES, DecisionPolicy
from option_risk.graph_explanation import render_graph_explanation
from option_risk.graph_queries import GraphQueryService
from option_risk.graph_reasoner import build_graph_result, discover_risk_paths
from option_risk.knowledge_graph import build_knowledge_graph
from option_risk.knowledge_schema import FEATURE_RULES, KG_RULE_VERSION, KG_SCHEMA_VERSION


NOTEBOOK_CELL_IDS = (
    "overview",
    "runtime-contract",
    "catalog-selection",
    "real-event-analysis",
    "problem1-result",
    "schema-and-rules",
    "four-layer-graph",
    "preset-queries",
    "five-section-explanation",
    "traceability-check",
    "completion",
)
DEMO_PRODUCT = "ag"
DEMO_TIMESTAMP = "2025-04-07 10:15:00"
DEMO_CANDIDATES = {
    "level_0": ("ag", "2025-04-17 21:30:00"),
    "level_1": ("ag", "2025-04-30 15:00:00"),
    "level_2": ("ag", DEMO_TIMESTAMP),
    "quality_limited": ("ag", "2025-04-30 14:45:00"),
}


def _cell(cell: nbf.NotebookNode, cell_id: str) -> nbf.NotebookNode:
    cell["id"] = cell_id
    return cell


def build_notebook() -> nbf.NotebookNode:
    """Build the deterministic, single-Agent Problem 2 notebook source."""

    notebook = nbf.v4.new_notebook()
    notebook["metadata"]["kernelspec"] = {
        "display_name": "option-risk-warning",
        "language": "python",
        "name": "python3",
    }
    notebook["metadata"]["language_info"] = {"name": "python"}
    notebook["cells"] = [
        _cell(
            nbf.v4.new_markdown_cell(
                "# 问题2：单Agent风险知识图谱可复核演示\n\n"
                "本 Notebook 只实例化比赛系统原有的 `OptionRiskAgent`。用户入口仍是"
                "“品种 → 该品种有效时间点 → 确认”；知识图谱是同一结果中的可解释层，"
                "不创建第二个业务Agent，也不提供自由文本问答。演示事件是白银 `ag` 在"
                "2025-04-07 10:15:00（赛题官方极端事件区间内）的真实期权快照。"
            ),
            "overview",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "from pathlib import Path\n"
                "import os\n"
                "import sys\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "import networkx as nx\n"
                "from IPython.display import display\n"
                "from option_risk import AgentConfig, OptionRiskAgent\n"
                "from option_risk.graph_queries import GraphQueryService\n"
                "from option_risk.knowledge_graph import graph_from_node_link\n"
                "from option_risk.knowledge_schema import FEATURE_RULES, KG_SCHEMA_VERSION, KG_RULE_VERSION\n\n"
                "ROOT = Path.cwd()\n"
                "if not (ROOT / 'src' / 'option_risk').exists():\n"
                "    ROOT = ROOT.parent\n"
                "data_value = os.environ.get('OPTION_RISK_DATA_DIR')\n"
                "archive_value = os.environ.get('OPTION_RISK_ARCHIVE_PATH')\n"
                "fallback = ROOT / 'data' / 'demo'\n"
                "if data_value:\n"
                "    config = AgentConfig(data_source=Path(data_value), cache_dir=ROOT / 'data' / 'notebook_cache', output_dir=ROOT / 'outputs' / 'demo')\n"
                "elif archive_value:\n"
                "    config = AgentConfig(archive_path=Path(archive_value), cache_dir=ROOT / 'data' / 'notebook_cache', output_dir=ROOT / 'outputs' / 'demo')\n"
                "elif fallback.exists():\n"
                "    config = AgentConfig(data_source=fallback, cache_dir=ROOT / 'data' / 'notebook_cache', output_dir=ROOT / 'outputs' / 'demo')\n"
                "else:\n"
                "    raise FileNotFoundError('Set OPTION_RISK_DATA_DIR or OPTION_RISK_ARCHIVE_PATH')\n"
                "agent = OptionRiskAgent(config)\n"
                "print('PUBLIC_AGENT=OptionRiskAgent')\n"
            ),
            "runtime-contract",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "products = [item.code for item in agent.list_products()]\n"
                "selected_product = 'ag'\n"
                "assert selected_product in products\n"
                "available_times = agent.list_timestamps(selected_product)\n"
                "selected_time = pd.Timestamp('2025-04-07 10:15:00')\n"
                "assert selected_time in available_times\n"
                "pd.Series({'actual_product_count': len(products), 'selected_product': selected_product, "
                "'valid_timestamp_count': len(available_times), 'selected_timestamp': selected_time.isoformat()}, name='只读下拉选择')\n"
            ),
            "catalog-selection",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "result = agent.analyze(selected_product, selected_time)\n"
                "graph_result = result.knowledge_graph\n"
                "assert result.status == 'ready'\n"
                "assert graph_result is not None and graph_result.status == 'ready'\n"
                "assert result.product == graph_result.product == selected_product\n"
                "assert result.timestamp == graph_result.timestamp == selected_time\n"
                "print(f'REAL_EVENT={selected_product}/{selected_time.isoformat()}')\n"
            ),
            "real-event-analysis",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "problem1 = pd.Series({\n"
                "    'alert_level': result.alert_level, 'alert_name': result.alert_name,\n"
                "    'alert_emitted': result.alert_emitted, 'risk_score': result.risk_score,\n"
                "    'policy_version': result.policy_version, 'policy_parameter_hash': result.policy_parameter_hash,\n"
                "    'transition_reason': result.transition_reason, 'price_source': result.price_source,\n"
                "}, name='问题1正式结果')\n"
                "display(problem1)\n"
                "metrics = ['iv', 'delta', 'gamma', 'vega', 'theta']\n"
                "fig = plt.figure(figsize=(14, 7), constrained_layout=True)\n"
                "for position, metric in enumerate(metrics, start=1):\n"
                "    surface = result.surfaces[metric]\n"
                "    axis = fig.add_subplot(2, 3, position, projection='3d')\n"
                "    x, y = __import__('numpy').meshgrid(surface.log_moneyness, surface.time_to_expiry)\n"
                "    axis.plot_surface(x, y, surface.values, cmap='Blues', linewidth=0, antialiased=True)\n"
                "    axis.set_title(metric.upper())\n"
                "    axis.set_xlabel('ln(K/F)'); axis.set_ylabel('T'); axis.set_zlabel(metric)\n"
                "display(fig)\n"
                "plt.close(fig)\n"
            ),
            "problem1-result",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "assert graph_result.schema_version == KG_SCHEMA_VERSION\n"
                "assert graph_result.rule_version == KG_RULE_VERSION\n"
                "mapping = pd.DataFrame([{\n"
                "    'order': rule.order, 'feature': rule.feature_name, 'Evidence': rule.label,\n"
                "    'Anomaly': rule.anomaly, 'Mechanism': rule.mechanism,\n"
                "    'Conclusion': rule.conclusion, 'boundary': rule.boundary,\n"
                "} for rule in FEATURE_RULES])\n"
                "print(f'SCHEMA={graph_result.schema_version}; RULE={graph_result.rule_version}; MAPPINGS={len(mapping)}')\n"
                "display(mapping)\n"
            ),
            "schema-and-rules",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "selected_paths = list(graph_result.active_paths[:3])\n"
                "graph = graph_from_node_link(graph_result.graph_json)\n"
                "selected_nodes = []\n"
                "for path in selected_paths:\n"
                "    for node_id in (path.evidence_node_id, path.anomaly_node_id, path.mechanism_node_id, path.conclusion_node_id):\n"
                "        if node_id not in selected_nodes:\n"
                "            selected_nodes.append(node_id)\n"
                "selected_edges = [(u, v) for path in selected_paths for u, v in zip((path.evidence_node_id, path.anomaly_node_id, path.mechanism_node_id), (path.anomaly_node_id, path.mechanism_node_id, path.conclusion_node_id))]\n"
                "positions = {}\n"
                "for track, path in enumerate(selected_paths):\n"
                "    for layer, node_id in enumerate((path.evidence_node_id, path.anomaly_node_id, path.mechanism_node_id, path.conclusion_node_id)):\n"
                "        positions.setdefault(node_id, (layer, -track))\n"
                "fig_graph, axis_graph = plt.subplots(figsize=(13, 4), constrained_layout=True)\n"
                "if selected_nodes:\n"
                "    nx.draw_networkx_nodes(graph, positions, nodelist=selected_nodes, node_color='#dbeafe', edgecolors='#235a97', node_size=2400, ax=axis_graph)\n"
                "    nx.draw_networkx_edges(nx.DiGraph(selected_edges), positions, edge_color='#596776', arrows=True, arrowsize=16, ax=axis_graph)\n"
                "    labels = {node_id: f\"{graph.nodes[node_id]['node_type']}\\n{graph.nodes[node_id].get('feature_name', graph.nodes[node_id].get('rule_id', 'result'))}\" for node_id in selected_nodes}\n"
                "    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=7, ax=axis_graph)\n"
                "else:\n"
                "    axis_graph.text(0.5, 0.5, 'No active anomaly path', ha='center', va='center')\n"
                "axis_graph.set_title('Evidence -> Anomaly -> Mechanism -> Conclusion (top 3 paths)')\n"
                "axis_graph.axis('off')\n"
                "display(fig_graph)\n"
                "plt.close(fig_graph)\n"
                "assert len(selected_paths) <= 3\n"
                "print('FOUR_LAYERS=Evidence -> Anomaly -> Mechanism -> Conclusion')\n"
            ),
            "four-layer-graph",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "queries = GraphQueryService(graph_result)\n"
                "root_rows = queries.root_evidence(limit=3)\n"
                "alert_paths = queries.paths_to_alert()\n"
                "consequences = queries.possible_consequences()\n"
                "quality_paths = queries.quality_limitations()\n"
                "node_detail = queries.inspect_node(root_rows[0]['node_id']) if root_rows else queries.inspect_node(graph_result.graph_json['nodes'][0]['node_id'])\n"
                "anomaly_paths = queries.paths_from_anomaly(alert_paths[0]['anomaly_node_id']) if alert_paths else []\n"
                "pd.Series({'root_evidence': len(root_rows), 'paths_to_alert': len(alert_paths),\n"
                "'possible_consequences': len(consequences), 'quality_limitations': len(quality_paths),\n"
                "'inspect_node': node_detail['node_id'], 'paths_from_anomaly': len(anomaly_paths)}, name='固定预设查询')\n"
            ),
            "preset-queries",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "assert len(graph_result.explanation_sections) == 5\n"
                "for section in graph_result.explanation_sections:\n"
                "    print(f'## {section.title}\\n{section.content}\\n')\n"
            ),
            "five-section-explanation",
        ),
        _cell(
            nbf.v4.new_code_cell(
                "active_path_ids = {path.path_id for path in graph_result.active_paths}\n"
                "referenced_path_ids = {path_id for section in graph_result.explanation_sections for path_id in section.path_ids}\n"
                "assert referenced_path_ids <= active_path_ids\n"
                "assert all(path_id in graph_result.query_index['paths_from_anomaly'].get(path.anomaly_node_id, [])\n"
                "           for path in graph_result.active_paths for path_id in [path.path_id])\n"
                "print(f'TRACEABILITY_OK={len(referenced_path_ids)}/{len(active_path_ids)}')\n"
            ),
            "traceability-check",
        ),
        _cell(
            nbf.v4.new_markdown_cell(
                "## 完成\n\n该演示从真实数据选择项出发，保留问题1结论，随后构建和查询"
                "NetworkX四层图谱。所有解释路径均已回指活动路径；质量证据只降低解释置信度，"
                "不提高市场风险等级。系统不预测标的涨跌方向，也不提供交易建议。"
            ),
            "completion",
        ),
    ]
    return notebook


def execute_notebook(
    notebook: nbf.NotebookNode,
    output_path: str | Path,
    *,
    cwd: str | Path,
) -> nbf.NotebookNode:
    """Execute top-to-bottom with errors forbidden, then atomically publish."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    client = NotebookClient(
        notebook,
        timeout=600,
        kernel_name="python3",
        allow_errors=False,
        resources={"metadata": {"path": str(Path(cwd).resolve())}},
    )
    executed = client.execute()
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{output.name}.",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            nbf.write(executed, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return executed


def _strict_json(path: Path) -> dict[str, Any]:
    def reject(value: str) -> object:
        raise ValueError(f"Non-standard JSON constant: {value}")

    payload = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    if type(payload) is not dict:
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def _validate_acceptance(path: Path) -> dict[str, Any]:
    payload = _strict_json(path)
    products = payload.get("products")
    summary = payload.get("summary")
    checks = payload.get("global_checks")
    if type(products) is not list or len(products) != 35 or type(summary) is not dict:
        raise ValueError("Formal acceptance must contain exactly 35 product rows")
    passed = sum(type(row) is dict and row.get("status") == "passed" for row in products)
    failed = len(products) - passed
    if (
        summary.get("status") != "passed"
        or summary.get("product_count") != 35
        or summary.get("passed_products") != passed
        or summary.get("failed_products") != failed
        or passed != 35
        or failed != 0
    ):
        raise ValueError("Formal acceptance summary does not reconcile")
    if type(checks) is not dict:
        raise ValueError("Formal acceptance global checks are missing")
    for name in ("deterministic", "no_future", "content_safety"):
        check = checks.get(name)
        if (
            type(check) is not dict
            or check.get("passed") is not True
            or type(check.get("checked_count")) is not int
            or check["checked_count"] <= 0
            or type(check.get("scope")) is not str
            or not check["scope"].strip()
        ):
            raise ValueError(f"Formal acceptance check is not executed/passing: {name}")
    for row in products:
        graph = row.get("knowledge_graph")
        if (
            type(graph) is not dict
            or graph.get("status") != "ready"
            or graph.get("schema_version") != KG_SCHEMA_VERSION
            or graph.get("rule_version") != KG_RULE_VERSION
        ):
            raise ValueError("Formal acceptance contains an invalid graph row")
    return payload


def _case_queries(graph_result: KnowledgeGraphResult) -> dict[str, Any]:
    service = GraphQueryService(graph_result)
    roots = service.root_evidence(limit=3)
    nodes = sorted(
        (dict(row) for row in graph_result.graph_json["nodes"]),
        key=lambda row: str(row["node_id"]),
    )
    inspect_id = roots[0]["node_id"] if roots else nodes[0]["node_id"]
    active_paths = service.paths_to_alert() + service.quality_limitations()
    anomaly_id = active_paths[0]["anomaly_node_id"] if active_paths else None
    return {
        "root_evidence": roots,
        "paths_to_alert": service.paths_to_alert(),
        "possible_consequences": service.possible_consequences(),
        "quality_limitations": service.quality_limitations(),
        "inspect_node": {
            "node_id": inspect_id,
            "record": service.inspect_node(inspect_id),
        },
        "paths_from_anomaly": {
            "anomaly_id": anomaly_id,
            "records": service.paths_from_anomaly(anomaly_id) if anomaly_id else [],
        },
    }


def _result_summary(result: AgentResult) -> dict[str, Any]:
    payload = result.to_dict()
    return {
        "status": payload["status"],
        "alert_name": payload["alert_name"],
        "alert_emitted": payload["alert_emitted"],
        "risk_score": payload["risk_score"],
        "price_source": payload["price_source"],
        "policy_version": payload["policy_version"],
        "policy_parameter_hash": payload["policy_parameter_hash"],
        "transition_reason": payload["transition_reason"],
        "data_quality": _portable_value(payload["data_quality"]),
        "surface_metrics": sorted(payload["surfaces"]),
        "feature_evidence": payload["feature_evidence"],
        "trigger_reasons": payload["trigger_reasons"],
    }


def _portable_value(value: Any) -> Any:
    """Remove host-specific absolute paths while retaining relative provenance."""

    if isinstance(value, dict):
        return {str(key): _portable_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_portable_value(item) for item in value]
    if isinstance(value, tuple):
        return [_portable_value(item) for item in value]
    if isinstance(value, str):
        normalized = value.replace("\\", "/")
        if len(normalized) >= 3 and normalized[0].isalpha() and normalized[1:3] == ":/":
            parts = [part for part in normalized.split("/") if part]
            if "期权课题" in parts:
                return "/".join(parts[parts.index("期权课题") :])
            return Path(normalized).name
        if normalized.startswith(("/Users/", "/home/")):
            return Path(normalized).name
    return value


def _portable_real_graph(result: AgentResult) -> KnowledgeGraphResult:
    """Rebuild the same formal graph with portable data-quality provenance."""

    policy = DecisionPolicy()
    graph = build_knowledge_graph(
        product=result.product,
        timestamp=result.timestamp,
        evidence=result.feature_evidence,
        alert_level=result.alert_level,
        alert_name=result.alert_name,
        risk_score=result.risk_score,
        alert_emitted=result.alert_emitted,
        transition_reason=result.transition_reason,
        policy_version=result.policy_version,
        policy_parameter_hash=result.policy_parameter_hash,
        data_quality=_portable_value(result.data_quality),
        price_source=result.price_source,
        policy=policy,
    )
    paths = discover_risk_paths(graph)
    sections, text, confidence = render_graph_explanation(graph, paths)
    available = {
        row.feature_name
        for row in result.feature_evidence
        if row.current_value is not None and math.isfinite(float(row.current_value))
    }
    missing = tuple(
        rule.feature_name
        for rule in FEATURE_RULES
        if rule.feature_name not in available
    )
    return build_graph_result(
        graph,
        missing_evidence=missing,
        explanation_sections=sections,
        explanation_text=text,
        explanation_confidence=confidence,
    )


def _snapshot_case(
    *,
    case_id: str,
    scenario: str,
    origin: str,
    alert_level: int,
    graph_result: KnowledgeGraphResult,
    result_summary: dict[str, Any],
) -> dict[str, Any]:
    GraphQueryService(graph_result)
    active_ids = {path.path_id for path in graph_result.active_paths}
    referenced = {
        path_id
        for section in graph_result.explanation_sections
        for path_id in section.path_ids
    }
    if not referenced <= active_ids:
        raise ValueError("Explanation references a path absent from the graph")
    return {
        "case_id": case_id,
        "scenario": scenario,
        "product": graph_result.product,
        "timestamp": graph_result.timestamp.isoformat(),
        "alert_level": alert_level,
        "origin": origin,
        "result": result_summary,
        "graph": graph_result.to_dict(),
        "query": _case_queries(graph_result),
        "explanation": {
            "sections": [section.to_dict() for section in graph_result.explanation_sections],
            "text": graph_result.explanation_text,
            "confidence": graph_result.explanation_confidence,
            "path_ids": sorted(referenced),
            "traceability_passed": True,
        },
    }


def _real_case(scenario: str, result: AgentResult) -> dict[str, Any]:
    original = result.knowledge_graph
    if original is None or original.status != "ready":
        raise ValueError(f"Real case graph is unavailable: {scenario}")
    graph_result = _portable_real_graph(result)
    expected_level = int(scenario[-1]) if scenario.startswith("level_") else None
    if expected_level is not None and result.alert_level != expected_level:
        raise ValueError(f"Real case level mismatch: {scenario}")
    if scenario == "quality_limited" and graph_result.explanation_confidence != "limited":
        raise ValueError("Quality case must have limited explanation confidence")
    return _snapshot_case(
        case_id=f"{scenario}_real_{result.product}_{result.timestamp:%Y%m%dT%H%M%S}",
        scenario=scenario,
        origin="real",
        alert_level=result.alert_level,
        graph_result=graph_result,
        result_summary=_result_summary(result),
    )


def _contract_evidence(base: AgentResult) -> list[FeatureEvidence]:
    pressures = {"atm_iv": 1.70, "convexity_violation_ratio": 1.60, "gamma_hhi": 1.55}
    rows: list[FeatureEvidence] = []
    for row in base.feature_evidence:
        pressure = pressures.get(row.feature_name, 0.80)
        current = row.current_value
        if current is None or not math.isfinite(float(current)) or current == 0:
            current = 0.20
        rows.append(
            replace(
                row,
                current_value=float(current),
                reference_value=float(current) / pressure,
                pressure_ratio=pressure,
                status=ALERT_NAMES[3 if pressure >= 1.5 else 0],
            )
        )
    return rows


def _synthetic_level_three(base: AgentResult) -> dict[str, Any]:
    evidence = _contract_evidence(base)
    policy = DecisionPolicy()
    timestamp = base.timestamp
    graph = build_knowledge_graph(
        product="ag_contract",
        timestamp=timestamp,
        evidence=evidence,
        alert_level=3,
        alert_name=ALERT_NAMES[3],
        risk_score=1.70,
        alert_emitted=True,
        transition_reason="danger_emitted",
        policy_version=base.policy_version,
        policy_parameter_hash=policy.parameter_hash,
        data_quality={
            "synthetic_contract": True,
            "purpose": "Level-3 rule and explanation contract only",
        },
        price_source="reconstructed_proxy",
        policy=policy,
    )
    paths = discover_risk_paths(graph)
    sections, text, confidence = render_graph_explanation(graph, paths)
    graph_result = build_graph_result(
        graph,
        missing_evidence=(),
        explanation_sections=sections,
        explanation_text=text,
        explanation_confidence=confidence,
    )
    result_summary = {
        "status": "ready",
        "alert_name": ALERT_NAMES[3],
        "alert_emitted": True,
        "risk_score": 1.70,
        "price_source": "reconstructed_proxy",
        "policy_version": base.policy_version,
        "policy_parameter_hash": policy.parameter_hash,
        "transition_reason": "danger_emitted",
        "data_quality": {
            "synthetic_contract": True,
            "purpose": "Level-3 rule and explanation contract only",
        },
        "surface_metrics": [],
        "feature_evidence": [asdict(row) for row in evidence],
        "trigger_reasons": [],
        "synthetic_note": "形式化契约场景，不代表真实市场观测，不计入市场表现。",
    }
    return _snapshot_case(
        case_id=f"level_3_synthetic_contract_{timestamp:%Y%m%dT%H%M%S}",
        scenario="level_3",
        origin="synthetic_contract",
        alert_level=3,
        graph_result=graph_result,
        result_summary=result_summary,
    )


def _accepted_candidates(
    acceptance: dict[str, Any],
) -> dict[str, tuple[str, str]]:
    rows = acceptance["products"]
    candidates: dict[str, tuple[str, str]] = {}
    for level in (0, 1, 2):
        row = next(item for item in rows if item["analysis"]["alert_level"] == level)
        candidates[f"level_{level}"] = (row["product"], row["analysis"]["timestamp"])
    quality = next(
        item for item in rows if item["knowledge_graph"]["quality_path_count"] > 0
    )
    candidates["quality_limited"] = (
        quality["product"],
        quality["analysis"]["timestamp"],
    )
    return candidates


def _analyze_candidate(
    agent: OptionRiskAgent,
    products: set[str],
    candidate: tuple[str, str],
) -> AgentResult | None:
    product, timestamp_text = candidate
    if product not in products:
        return None
    timestamp = pd.Timestamp(timestamp_text)
    if timestamp not in agent.list_timestamps(product):
        return None
    return agent.analyze(product, timestamp)


def _atomic_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
        allow_nan=False,
    ) + "\n"
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
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return path


def build_snapshot(
    *,
    acceptance_path: str | Path,
    output_path: str | Path,
    data_dir: str | Path | None = None,
    archive_path: str | Path | None = None,
    cache_dir: str | Path,
    agent_output_dir: str | Path,
) -> dict[str, Any]:
    """Build real cases through OptionRiskAgent and one labelled contract case."""

    if data_dir is not None and archive_path is not None:
        raise ValueError("Choose either data_dir or archive_path, not both")
    acceptance_path = Path(acceptance_path)
    acceptance = _validate_acceptance(acceptance_path)
    config = AgentConfig(
        data_source=Path(data_dir) if data_dir is not None else None,
        archive_path=Path(archive_path) if archive_path is not None else None,
        cache_dir=Path(cache_dir),
        output_dir=Path(agent_output_dir),
    )
    agent = OptionRiskAgent(config)
    products = {item.code for item in agent.list_products()}
    accepted = _accepted_candidates(acceptance)
    real_cases: dict[str, AgentResult] = {}
    for scenario in ("level_0", "level_1", "level_2", "quality_limited"):
        result = _analyze_candidate(agent, products, accepted[scenario])
        if result is None:
            result = _analyze_candidate(agent, products, DEMO_CANDIDATES[scenario])
        if result is None:
            raise ValueError(f"Data source does not contain a real case for {scenario}")
        real_cases[scenario] = result

    cases = [
        _real_case("level_0", real_cases["level_0"]),
        _real_case("level_1", real_cases["level_1"]),
        _real_case("level_2", real_cases["level_2"]),
        _synthetic_level_three(real_cases["level_2"]),
        _real_case("quality_limited", real_cases["quality_limited"]),
    ]
    acceptance_sha = hashlib.sha256(acceptance_path.read_bytes()).hexdigest().upper()
    payload = {
        "format_version": "kg-snapshot-v1",
        "schema_version": KG_SCHEMA_VERSION,
        "rule_version": KG_RULE_VERSION,
        "generated_at": acceptance["generated_at"],
        "formal_acceptance_sha256": acceptance_sha,
        "case_count": len(cases),
        "real_case_count": sum(case["origin"] == "real" for case in cases),
        "synthetic_contract_case_count": sum(
            case["origin"] == "synthetic_contract" for case in cases
        ),
        "synthetic_contract_boundary": (
            "合成契约案例只验证3级规则、查询和解释链，不计入真实市场表现或35品种通过数。"
        ),
        "cases": cases,
    }
    _atomic_json(Path(output_path), payload)
    return payload


@contextmanager
def _source_environment(
    *, data_dir: Path | None, archive_path: Path | None
) -> Iterator[None]:
    previous = {
        "OPTION_RISK_DATA_DIR": os.environ.get("OPTION_RISK_DATA_DIR"),
        "OPTION_RISK_ARCHIVE_PATH": os.environ.get("OPTION_RISK_ARCHIVE_PATH"),
    }
    try:
        if data_dir is not None:
            os.environ["OPTION_RISK_DATA_DIR"] = str(data_dir)
            os.environ.pop("OPTION_RISK_ARCHIVE_PATH", None)
        elif archive_path is not None:
            os.environ["OPTION_RISK_ARCHIVE_PATH"] = str(archive_path)
            os.environ.pop("OPTION_RISK_DATA_DIR", None)
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build Problem 2 notebook and snapshots")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--data-dir", type=Path)
    source.add_argument("--archive-path", type=Path)
    parser.add_argument("--cache-dir", type=Path, default=project_root / "data" / "agent_cache")
    parser.add_argument("--agent-output-dir", type=Path, default=project_root / "outputs")
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
        "--notebook",
        type=Path,
        default=project_root / "notebooks" / "02_knowledge_graph_demo.ipynb",
    )
    parser.add_argument("--snapshot-only", action="store_true")
    parser.add_argument("--notebook-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.snapshot_only and args.notebook_only:
        raise ValueError("--snapshot-only and --notebook-only are mutually exclusive")
    project_root = Path(__file__).resolve().parents[1]
    data_dir = args.data_dir
    archive_path = args.archive_path
    if data_dir is None and archive_path is None:
        env_data = os.environ.get("OPTION_RISK_DATA_DIR")
        env_archive = os.environ.get("OPTION_RISK_ARCHIVE_PATH")
        if env_data:
            data_dir = Path(env_data)
        elif env_archive:
            archive_path = Path(env_archive)
        else:
            data_dir = project_root / "data" / "demo"
    if not args.notebook_only:
        payload = build_snapshot(
            acceptance_path=args.acceptance,
            output_path=args.snapshot,
            data_dir=data_dir,
            archive_path=archive_path,
            cache_dir=args.cache_dir,
            agent_output_dir=args.agent_output_dir,
        )
        print(f"Snapshot cases: {payload['case_count']} -> {args.snapshot}")
    if not args.snapshot_only:
        with _source_environment(data_dir=data_dir, archive_path=archive_path):
            execute_notebook(build_notebook(), args.notebook, cwd=project_root)
        print(f"Executed notebook: {args.notebook}")


if __name__ == "__main__":
    main()
````

</details>
