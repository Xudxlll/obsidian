---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py>)

SHA-256：`a4bd188bcc9dd1ed4217f767dae305766b80c9e8adedced7e6b2759eafd23730`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess

import nbformat
import pytest

from option_risk.contracts import KnowledgeGraphResult
from option_risk.graph_queries import GraphQueryService
from option_risk.knowledge_schema import FEATURE_RULES, KG_RULE_VERSION, KG_SCHEMA_VERSION


ROOT = Path(__file__).parents[1]
ACCEPTANCE = ROOT / "outputs" / "knowledge_graph_acceptance_full.json"
SNAPSHOT = ROOT / "outputs" / "demo" / "knowledge_graph_snapshot.json"
REVIEW_TEMPLATE = ROOT / "outputs" / "人工解释评分模板.csv"
REVIEW_SUMMARY = ROOT / "outputs" / "人工解释评分汇总.csv"
REPORT = ROOT / "outputs" / "问题2-知识图谱验收报告.html"
NOTEBOOK = ROOT / "notebooks" / "02_knowledge_graph_demo.ipynb"
GUIDE = ROOT / "docs" / "问题2-知识图谱设计与运行说明.md"

EXPECTED_ACCEPTANCE_SHA256 = (
    "E1C54F628792FD7D26CFDE606EB57F9D319739DD1BDD82FFF320CDEC4A85585B"
)
EXPECTED_NOTEBOOK_CELL_IDS = (
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
EXPECTED_SCENARIOS = {
    "level_0",
    "level_1",
    "level_2",
    "level_3",
    "quality_limited",
}
REVIEW_COLUMNS = (
    "case_id",
    "product",
    "timestamp",
    "alert_level",
    "explanation_text",
    "reviewer_id",
    "clarity",
    "evidence",
    "logic",
    "wording",
    "safety",
    "comment",
    "reviewed_at",
)
SCORE_COLUMNS = ("clarity", "evidence", "logic", "wording", "safety")


def _load_script(filename: str):
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_strict_json(path: Path) -> dict[str, object]:
    def reject_constant(value: str) -> object:
        raise ValueError(f"non-standard JSON constant: {value}")

    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_task8_deliverables_exist_and_formal_acceptance_is_unchanged() -> None:
    required = (
        ROOT / "scripts" / "build_explanation_review.py",
        ROOT / "scripts" / "build_knowledge_graph_notebook.py",
        ROOT / "scripts" / "build_knowledge_graph_report.py",
        NOTEBOOK,
        GUIDE,
        SNAPSHOT,
        REVIEW_TEMPLATE,
        REPORT,
    )
    assert all(path.is_file() for path in required)
    assert not REVIEW_SUMMARY.exists(), "不得从空白或合成评分生成汇总"
    assert hashlib.sha256(ACCEPTANCE.read_bytes()).hexdigest().upper() == (
        EXPECTED_ACCEPTANCE_SHA256
    )


def test_notebook_builder_is_deterministic_and_executes_without_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_script("build_knowledge_graph_notebook.py")
    notebook = module.build_notebook()
    assert tuple(cell["id"] for cell in notebook.cells) == EXPECTED_NOTEBOOK_CELL_IDS
    assert notebook.metadata.kernelspec.name == "python3"

    source = "\n".join(str(cell.get("source", "")) for cell in notebook.cells)
    assert "OptionRiskAgent" in source
    assert "OPTION_RISK_DATA_DIR" in source
    assert "OPTION_RISK_ARCHIVE_PATH" in source
    assert "2025-04-07 10:15:00" in source
    assert not re.search(r"(?i)pip\s+install|requests\.|urlopen|download", source)
    assert "http://" not in source and "https://" not in source
    assert not re.search(r"(?i)(?:[a-z]:[\\/]|/Users/|/home/)", source)

    monkeypatch.setenv("OPTION_RISK_DATA_DIR", str(ROOT / "data" / "demo"))
    monkeypatch.delenv("OPTION_RISK_ARCHIVE_PATH", raising=False)
    executed_path = tmp_path / "02_knowledge_graph_demo.ipynb"
    module.execute_notebook(notebook, executed_path, cwd=ROOT)

    executed = nbformat.read(executed_path, as_version=4)
    code_cells = [cell for cell in executed.cells if cell.cell_type == "code"]
    assert code_cells
    assert all(cell.execution_count is not None for cell in code_cells)
    assert not [
        output
        for cell in code_cells
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    rendered = json.dumps(executed, ensure_ascii=False)
    assert "2025-04-07T10:15:00" in rendered
    assert "kg-schema-v1" in rendered and "kg-rule-v1" in rendered
    assert "TRACEABILITY_OK" in rendered


def test_delivered_notebook_is_fully_executed_and_matches_builder() -> None:
    module = _load_script("build_knowledge_graph_notebook.py")
    delivered = nbformat.read(NOTEBOOK, as_version=4)
    template = module.build_notebook()
    assert tuple(cell["id"] for cell in delivered.cells) == EXPECTED_NOTEBOOK_CELL_IDS
    assert [cell.source for cell in delivered.cells] == [cell.source for cell in template.cells]
    code_cells = [cell for cell in delivered.cells if cell.cell_type == "code"]
    assert all(cell.execution_count is not None for cell in code_cells)
    assert not any(
        output.get("output_type") == "error"
        for cell in code_cells
        for output in cell.get("outputs", [])
    )


def test_snapshot_is_strict_versioned_traceable_and_covers_five_scenarios() -> None:
    payload = _load_strict_json(SNAPSHOT)
    assert payload["format_version"] == "kg-snapshot-v1"
    assert payload["schema_version"] == KG_SCHEMA_VERSION
    assert payload["rule_version"] == KG_RULE_VERSION
    assert payload["formal_acceptance_sha256"] == EXPECTED_ACCEPTANCE_SHA256

    cases = payload["cases"]
    assert isinstance(cases, list) and len(cases) == 5
    assert {case["scenario"] for case in cases} == EXPECTED_SCENARIOS
    assert len({case["case_id"] for case in cases}) == len(cases)
    assert all(
        set(case) >= {
            "case_id",
            "scenario",
            "product",
            "timestamp",
            "alert_level",
            "origin",
            "result",
            "graph",
            "query",
            "explanation",
        }
        for case in cases
    )
    assert all(case["origin"] in {"real", "synthetic_contract"} for case in cases)
    assert next(case for case in cases if case["scenario"] == "level_3")["origin"] == (
        "synthetic_contract"
    )
    assert all(
        case["origin"] == "real"
        for case in cases
        if case["scenario"] in {"level_0", "level_1", "level_2", "quality_limited"}
    )

    for case in cases:
        assert type(case["alert_level"]) is int
        assert case["alert_level"] in {0, 1, 2, 3}
        graph_result = KnowledgeGraphResult.from_dict(case["graph"])
        assert graph_result.status == "ready"
        assert graph_result.product == case["product"]
        assert graph_result.timestamp.isoformat() == case["timestamp"]
        assert graph_result.schema_version == KG_SCHEMA_VERSION
        assert graph_result.rule_version == KG_RULE_VERSION

        service = GraphQueryService(graph_result)
        query = case["query"]
        assert query["root_evidence"] == service.root_evidence(limit=3)
        assert query["paths_to_alert"] == service.paths_to_alert()
        assert query["possible_consequences"] == service.possible_consequences()
        assert query["quality_limitations"] == service.quality_limitations()
        assert query["inspect_node"]["record"] == service.inspect_node(
            query["inspect_node"]["node_id"]
        )
        anomaly_id = query["paths_from_anomaly"]["anomaly_id"]
        if anomaly_id is None:
            assert query["paths_from_anomaly"]["records"] == []
        else:
            assert query["paths_from_anomaly"]["records"] == (
                service.paths_from_anomaly(anomaly_id)
            )

        explanation = case["explanation"]
        assert explanation["text"] == graph_result.explanation_text
        assert explanation["confidence"] == graph_result.explanation_confidence
        assert explanation["sections"] == [
            section.to_dict() for section in graph_result.explanation_sections
        ]
        active_ids = {path.path_id for path in graph_result.active_paths}
        referenced_ids = {
            path_id
            for section in explanation["sections"]
            for path_id in section["path_ids"]
        }
        assert referenced_ids <= active_ids
        assert explanation["traceability_passed"] is True

    assert next(case for case in cases if case["scenario"] == "level_0")[
        "alert_level"
    ] == 0
    assert next(case for case in cases if case["scenario"] == "level_1")[
        "alert_level"
    ] == 1
    assert next(case for case in cases if case["scenario"] == "level_2")[
        "alert_level"
    ] == 2
    assert next(case for case in cases if case["scenario"] == "level_3")[
        "alert_level"
    ] == 3
    assert next(case for case in cases if case["scenario"] == "quality_limited")[
        "graph"
    ]["explanation_confidence"] == "limited"


def test_review_template_is_blank_and_aggregation_math_is_exact(tmp_path: Path) -> None:
    module = _load_script("build_explanation_review.py")
    template = tmp_path / "review-template.csv"
    module.write_review_template(SNAPSHOT, template)

    with template.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        assert tuple(handle.seek(0) or next(csv.reader(handle))) == REVIEW_COLUMNS
    assert len(rows) == 5
    assert all(
        row[column] == ""
        for row in rows
        for column in (*SCORE_COLUMNS, "reviewer_id", "comment", "reviewed_at")
    )

    completed: list[dict[str, object]] = []
    for reviewer_id, score in (("reviewer-a", 4), ("reviewer-b", 5)):
        for row in rows:
            rated: dict[str, object] = dict(row)
            rated.update(
                reviewer_id=reviewer_id,
                clarity=score,
                evidence=score,
                logic=score,
                wording=score,
                safety=score,
                comment="独立人工评分",
                reviewed_at="2026-08-29T13:30:00+08:00",
            )
            completed.append(rated)
    ratings = tmp_path / "ratings.csv"
    summary_path = tmp_path / "summary.csv"
    _write_csv(ratings, completed)
    summary = module.aggregate_reviews(ratings, summary_path)
    assert summary["overall_mean"] == 4.5
    assert summary["reviewer_count"] == 2
    assert summary["case_count"] == 5
    assert summary["value_count"] == 50
    assert summary["target_status"] == "passed"
    assert all(summary["dimension_means"][column] == 4.5 for column in SCORE_COLUMNS)
    assert summary_path.is_file()


def test_review_aggregation_rejects_incomplete_invalid_and_duplicate_rows(
    tmp_path: Path,
) -> None:
    module = _load_script("build_explanation_review.py")
    with REVIEW_TEMPLATE.open("r", encoding="utf-8-sig", newline="") as handle:
        base = next(csv.DictReader(handle))
    valid: dict[str, object] = dict(base)
    valid.update(
        reviewer_id="reviewer-a",
        clarity=4,
        evidence=4,
        logic=4,
        wording=4,
        safety=4,
        comment="人工检查",
        reviewed_at="2026-08-29T13:30:00+08:00",
    )
    attacks: list[list[dict[str, object]]] = []
    for column, value in (
        ("clarity", ""),
        ("evidence", "NaN"),
        ("logic", 0),
        ("wording", 6),
        ("reviewer_id", ""),
        ("reviewed_at", ""),
    ):
        row = dict(valid)
        row[column] = value
        attacks.append([row])
    attacks.append([dict(valid), dict(valid)])

    for index, rows in enumerate(attacks):
        ratings = tmp_path / f"invalid-{index}.csv"
        summary = tmp_path / f"invalid-{index}-summary.csv"
        _write_csv(ratings, rows)
        with pytest.raises(ValueError):
            module.aggregate_reviews(ratings, summary)
        assert not summary.exists()


def test_report_reconciles_all_formal_evidence_and_is_offline_safe(tmp_path: Path) -> None:
    module = _load_script("build_knowledge_graph_report.py")
    output = tmp_path / "report.html"
    module.build_report(ACCEPTANCE, SNAPSHOT, output)
    html = output.read_text(encoding="utf-8")
    lower = html.lower()

    acceptance = _load_strict_json(ACCEPTANCE)
    products = acceptance["products"]
    total_nodes = sum(row["knowledge_graph"]["node_count"] for row in products)
    total_edges = sum(row["knowledge_graph"]["edge_count"] for row in products)
    total_paths = sum(row["knowledge_graph"]["active_path_count"] for row in products)
    assert f'data-total-nodes="{total_nodes}"' in html
    assert f'data-total-edges="{total_edges}"' in html
    assert f'data-total-paths="{total_paths}"' in html
    assert "35/35" in html
    assert html.count("<tr data-product=") == 35
    assert all(rule.feature_name in html and rule.label in html for rule in FEATURE_RULES)
    assert all(name in html for name in ("deterministic", "no_future", "content_safety"))
    assert all(scenario in html for scenario in EXPECTED_SCENARIOS)
    assert "人工评分待完成" in html
    assert "2026-08-22" not in html
    assert "<svg" in lower and "viewbox=" in lower
    assert "@media (max-width: 430px)" in html
    assert "overflow-wrap" in html
    assert "<script" not in lower
    assert "http://" not in lower and "https://" not in lower
    assert not re.search(r"<(?:link|iframe|object|embed)\b", lower)


def test_report_escapes_external_text_and_rejects_inconsistent_acceptance(
    tmp_path: Path,
) -> None:
    module = _load_script("build_knowledge_graph_report.py")
    acceptance = _load_strict_json(ACCEPTANCE)
    acceptance["global_checks"]["deterministic"]["scope"] = (
        '<img src=x onerror="alert(1)">'
    )
    escaped_source = tmp_path / "escaped-acceptance.json"
    escaped_source.write_text(
        json.dumps(acceptance, ensure_ascii=False, allow_nan=False), encoding="utf-8"
    )
    snapshot = _load_strict_json(SNAPSHOT)
    snapshot["formal_acceptance_sha256"] = hashlib.sha256(
        escaped_source.read_bytes()
    ).hexdigest().upper()
    escaped_snapshot = tmp_path / "escaped-snapshot.json"
    escaped_snapshot.write_text(
        json.dumps(snapshot, ensure_ascii=False, allow_nan=False), encoding="utf-8"
    )
    escaped_report = tmp_path / "escaped.html"
    module.build_report(escaped_source, escaped_snapshot, escaped_report)
    html = escaped_report.read_text(encoding="utf-8")
    assert '<img src=x onerror="alert(1)">' not in html
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;" in html

    acceptance["summary"]["passed_products"] = 34
    inconsistent = tmp_path / "inconsistent.json"
    inconsistent.write_text(
        json.dumps(acceptance, ensure_ascii=False, allow_nan=False), encoding="utf-8"
    )
    blocked_output = tmp_path / "blocked.html"
    with pytest.raises(ValueError):
        module.build_report(inconsistent, SNAPSHOT, blocked_output)
    assert not blocked_output.exists()


def test_readme_and_problem2_guide_cover_cross_platform_operation_and_boundaries() -> None:
    combined = (ROOT / "README.md").read_text(encoding="utf-8")
    combined += "\n" + GUIDE.read_text(encoding="utf-8")
    required_phrases = (
        "Python >=3.12",
        "Windows PowerShell",
        "macOS zsh",
        "RAR",
        "ZIP",
        "Parquet",
        "tar/bsdtar",
        "手动解压",
        "品种 → 可选时间点 → 确认",
        "六个结果页签",
        "固定预设查询",
        "不提供自由文本",
        "35/35",
        "schema_version",
        "rule_version",
        "policy_version",
        "policy_parameter_hash",
        "source_timestamp",
        "未来数据",
        "不预测涨跌方向",
        "不提供交易建议",
        "人工评分待完成",
        "约7.2GB",
        "约104MB",
        "首次安装通常需要网络",
        "后续分析、Notebook 与报告可离线运行",
        "macOS 支持但尚未完成真实 Mac 机器正式认证",
    )
    assert all(phrase in combined for phrase in required_phrases)
    assert "python==3.12" not in combined.lower()
    assert not re.search(r"(?i)(?:[a-z]:[\\/]|/Users/|/home/)", combined)


def test_package_manifest_is_explicit_clean_and_contains_problem2_delivery() -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    assert shell is not None
    completed = subprocess.run(
        [
            shell,
            "-NoProfile",
            "-File",
            str(ROOT / "scripts" / "package_submission.ps1"),
            "-ManifestOnly",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    manifest = json.loads(completed.stdout)
    assert manifest["audit"]["absolute_path_scan_passed"] is True
    assert manifest["audit"]["raw_data_scan_passed"] is True
    files = set(manifest["files"])
    required = {
        "README.md",
        "pyproject.toml",
        "src/option_risk/agent.py",
        "src/option_risk/knowledge_graph.py",
        "scripts/query_knowledge_graph.py",
        "scripts/validate_knowledge_graph.py",
        "scripts/build_explanation_review.py",
        "scripts/build_knowledge_graph_notebook.py",
        "scripts/build_knowledge_graph_report.py",
        "docs/问题2-知识图谱设计与运行说明.md",
        "notebooks/02_knowledge_graph_demo.ipynb",
        "outputs/knowledge_graph_acceptance_full.json",
        "outputs/demo/knowledge_graph_snapshot.json",
        "outputs/人工解释评分模板.csv",
        "outputs/问题2-知识图谱验收报告.html",
    }
    assert required <= files
    assert not {
        "整改说明-问题1.md",
        "docs/问题1-Agent运行说明.md",
        "notebooks/01_end_to_end_demo.ipynb",
        "outputs/人工解释评分汇总.csv",
    } & files
    forbidden_parts = {
        "data",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".superpowers",
        ".git",
    }
    assert all(not (set(Path(name).parts) & forbidden_parts) for name in files)
    assert all(not name.endswith((".rar", ".zip", ".parquet", ".pyc", ".pyo")) for name in files)
    assert all(".egg-info/" not in name for name in files)
````

</details>
