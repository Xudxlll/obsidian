---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/build_explanation_review.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/build_explanation_review.py>)

SHA-256：`c6f102e658d10368ae80301f5195e74db94bd34642598d2df9b786710d1b93a7`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import math
import os
from pathlib import Path
import tempfile
from typing import Any


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
    raise ValueError(f"JSON contains non-standard numeric constant: {value}")


def _load_snapshot(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    payload = json.loads(
        source.read_text(encoding="utf-8"),
        parse_constant=_reject_constant,
    )
    if type(payload) is not dict or type(payload.get("cases")) is not list:
        raise ValueError("Snapshot must contain a cases list")
    if not payload["cases"]:
        raise ValueError("Snapshot must contain at least one review case")
    return payload


def _atomic_write_csv(
    output_path: str | Path,
    *,
    fieldnames: tuple[str, ...],
    rows: list[dict[str, Any]],
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            prefix=f".{output.name}.",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(
                handle,
                fieldnames=fieldnames,
                extrasaction="raise",
                lineterminator="\n",
            )
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return output


def write_review_template(
    snapshot_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Create an unrated template; no reviewer identity or score is inferred."""

    snapshot = _load_snapshot(snapshot_path)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw_case in snapshot["cases"]:
        if type(raw_case) is not dict:
            raise ValueError("Each snapshot case must be an object")
        case_id = raw_case.get("case_id")
        product = raw_case.get("product")
        timestamp = raw_case.get("timestamp")
        alert_level = raw_case.get("alert_level")
        explanation = raw_case.get("explanation")
        if (
            type(case_id) is not str
            or not case_id.strip()
            or case_id in seen
            or type(product) is not str
            or not product.strip()
            or type(timestamp) is not str
            or not timestamp.strip()
            or type(alert_level) is not int
            or alert_level not in {0, 1, 2, 3}
            or type(explanation) is not dict
            or type(explanation.get("text")) is not str
            or not explanation["text"].strip()
        ):
            raise ValueError("Snapshot contains an invalid review case")
        seen.add(case_id)
        rows.append(
            {
                "case_id": case_id,
                "product": product,
                "timestamp": timestamp,
                "alert_level": alert_level,
                "explanation_text": explanation["text"],
                "reviewer_id": "",
                "clarity": "",
                "evidence": "",
                "logic": "",
                "wording": "",
                "safety": "",
                "comment": "",
                "reviewed_at": "",
            }
        )
    return _atomic_write_csv(output_path, fieldnames=REVIEW_COLUMNS, rows=rows)


def _required_text(row: dict[str, str], field: str, row_number: int) -> str:
    value = row.get(field, "")
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Row {row_number}: {field} is required")
    return value.strip()


def _score(row: dict[str, str], field: str, row_number: int) -> float:
    raw = row.get(field, "")
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"Row {row_number}: {field} score is blank")
    try:
        value = float(raw)
    except ValueError as error:
        raise ValueError(f"Row {row_number}: {field} score is not numeric") from error
    if not math.isfinite(value) or not 1.0 <= value <= 5.0:
        raise ValueError(f"Row {row_number}: {field} score must be finite and within 1-5")
    return value


def aggregate_reviews(
    ratings_path: str | Path,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate genuine completed rows and compute the exact hard-gate mean."""

    source = Path(ratings_path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != REVIEW_COLUMNS:
            raise ValueError("Ratings CSV columns must exactly match the review template")
        rows = list(reader)
    if not rows:
        raise ValueError("Ratings CSV contains no completed human ratings")

    seen_pairs: set[tuple[str, str]] = set()
    case_identity: dict[str, tuple[str, str, int, str]] = {}
    reviewers: set[str] = set()
    cases: set[str] = set()
    reviewed_times: list[str] = []
    values: list[float] = []
    dimension_values = {column: [] for column in SCORE_COLUMNS}

    for row_number, row in enumerate(rows, start=2):
        case_id = _required_text(row, "case_id", row_number)
        product = _required_text(row, "product", row_number)
        timestamp = _required_text(row, "timestamp", row_number)
        explanation = _required_text(row, "explanation_text", row_number)
        reviewer_id = _required_text(row, "reviewer_id", row_number)
        reviewed_at = _required_text(row, "reviewed_at", row_number)
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"Row {row_number}: timestamp fields must be ISO-8601") from error
        try:
            alert_level = int(_required_text(row, "alert_level", row_number))
        except ValueError as error:
            raise ValueError(f"Row {row_number}: alert_level must be 0-3") from error
        if str(alert_level) != row["alert_level"].strip() or alert_level not in {0, 1, 2, 3}:
            raise ValueError(f"Row {row_number}: alert_level must be 0-3")

        pair = (reviewer_id, case_id)
        if pair in seen_pairs:
            raise ValueError(f"Duplicate reviewer-case row: {reviewer_id}/{case_id}")
        seen_pairs.add(pair)
        identity = (product, timestamp, alert_level, explanation)
        if case_id in case_identity and case_identity[case_id] != identity:
            raise ValueError(f"Case identity drift detected for {case_id}")
        case_identity[case_id] = identity

        for column in SCORE_COLUMNS:
            value = _score(row, column, row_number)
            dimension_values[column].append(value)
            values.append(value)
        reviewers.add(reviewer_id)
        cases.add(case_id)
        reviewed_times.append(reviewed_at)

    overall = sum(values) / len(values)
    dimensions = {
        column: sum(column_values) / len(column_values)
        for column, column_values in dimension_values.items()
    }
    summary: dict[str, Any] = {
        "target_status": "passed" if overall >= 4.0 else "failed",
        "overall_mean": overall,
        "dimension_means": dimensions,
        "reviewer_count": len(reviewers),
        "case_count": len(cases),
        "value_count": len(values),
        "row_count": len(rows),
        "reviewed_at_min": min(reviewed_times),
        "reviewed_at_max": max(reviewed_times),
    }
    if output_path is not None:
        flat = {
            "target_status": summary["target_status"],
            "overall_mean": format(overall, ".12g"),
            **{
                f"{column}_mean": format(dimensions[column], ".12g")
                for column in SCORE_COLUMNS
            },
            "reviewer_count": len(reviewers),
            "case_count": len(cases),
            "value_count": len(values),
            "row_count": len(rows),
            "reviewed_at_min": min(reviewed_times),
            "reviewed_at_max": max(reviewed_times),
        }
        _atomic_write_csv(output_path, fieldnames=SUMMARY_COLUMNS, rows=[flat])
    return summary


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build honest explanation review assets")
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=project_root / "outputs" / "demo" / "knowledge_graph_snapshot.json",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=project_root / "outputs" / "人工解释评分模板.csv",
    )
    parser.add_argument("--ratings", type=Path)
    parser.add_argument("--summary", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    template = write_review_template(args.snapshot, args.template)
    print(f"Created blank review template: {template}")
    if args.ratings is None:
        if args.summary is not None:
            raise ValueError("--summary requires a genuine completed --ratings file")
        print("人工评分待完成；未生成评分汇总。")
        return
    if args.summary is None:
        raise ValueError("Completed --ratings requires an explicit --summary path")
    summary = aggregate_reviews(args.ratings, args.summary)
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False, sort_keys=True))


if __name__ == "__main__":
    main()

````

</details>
