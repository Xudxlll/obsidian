---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/scripts/validate_outputs.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/scripts/validate_outputs.py>)

SHA-256：`4d4a032234977c59fa9ec19760c6c5b0e3f6f88eb8b1407441030b6c9ff9c9e0`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd
import joblib

from option_risk.alerts import evaluate_alerts
from option_risk.config import PipelineConfig
from option_risk.decision import (
    DECISION_POLICY_VERSION,
    PRIMARY_POLICY_SELECTION_DATA,
    DecisionPolicy,
)
from option_risk.io import discover_parquet_files
from option_risk.official_events import find_official_event_file
from option_risk.provenance import (
    fixed_holdout_checks,
    replay_decision_policy_checks,
    run_identity_checks,
)


EXPECTED_SURFACES = {"iv", "delta", "gamma", "vega", "theta"}
EXPECTED_FEATURE_GROUPS = {
    "曲面水平与形态",
    "期限结构",
    "无套利风险",
    "Greeks集中风险",
    "质量与流动性",
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _html_artifact_checks(
    html_path: str | Path,
    artifact: dict[str, object],
) -> dict[str, bool]:
    """Require the delivered HTML to be the exact deterministic artifact render."""

    path = Path(html_path)
    checks = {
        "html_report_exists": path.is_file(),
        "html_report_exactly_matches_current_artifact": False,
        "html_report_is_self_contained": False,
    }
    if not checks["html_report_exists"]:
        return checks
    try:
        renderer_path = PROJECT_ROOT / "scripts" / "render_acceptance_html.py"
        spec = importlib.util.spec_from_file_location(
            "option_risk_acceptance_html_renderer",
            renderer_path,
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load renderer: {renderer_path}")
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)
        expected = renderer.render_html(artifact)
        observed = path.read_text(encoding="utf-8")
    except Exception:
        return checks
    checks["html_report_exactly_matches_current_artifact"] = observed == expected
    lowered = observed.lower()
    checks["html_report_is_self_contained"] = bool(
        "default-src 'none'" in lowered
        and "connect-src 'none'" in lowered
        and "http://" not in lowered
        and "https://" not in lowered
        and "<script" not in lowered
        and "<link" not in lowered
    )
    return checks


def _notebook_artifact_checks(
    notebook_path: str | Path,
    summary: dict[str, object],
) -> dict[str, bool]:
    """Reject missing, unexecuted, errored, or stale companion notebooks."""

    path = Path(notebook_path)
    checks = {
        "notebook_exists": path.is_file(),
        "notebook_is_parseable": False,
        "notebook_all_code_cells_executed": False,
        "notebook_has_no_error_outputs": False,
        "notebook_contains_current_policy_identity": False,
        "notebook_contains_current_test_metrics": False,
    }
    if not checks["notebook_exists"]:
        return checks
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        cells = notebook.get("cells")
        if not isinstance(cells, list):
            return checks
        code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
        outputs = [
            output
            for cell in code_cells
            for output in cell.get("outputs", [])
            if isinstance(output, dict)
        ]
        serialized = json.dumps(notebook, ensure_ascii=False)
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError, TypeError):
        return checks
    checks["notebook_is_parseable"] = True
    checks["notebook_all_code_cells_executed"] = bool(
        code_cells
        and all(isinstance(cell.get("execution_count"), int) for cell in code_cells)
    )
    checks["notebook_has_no_error_outputs"] = not any(
        output.get("output_type") == "error" for output in outputs
    )
    identity = summary.get("run_identity")
    identity = identity if isinstance(identity, dict) else {}
    policy = identity.get("decision_policy")
    policy = policy if isinstance(policy, dict) else {}
    policy_hash = policy.get("parameter_sha256")
    selection_data = policy.get("selection_data")
    checks["notebook_contains_current_policy_identity"] = bool(
        isinstance(policy_hash, str)
        and policy_hash in serialized
        and isinstance(selection_data, str)
        and selection_data in serialized
        and "预注册固定动态状态机（正式主策略）" in serialized
        and "验证集定参" not in serialized
    )
    test_metrics = summary.get("test_metrics")
    test_metrics = test_metrics if isinstance(test_metrics, dict) else {}
    try:
        metric_tokens = [
            f"{float(test_metrics[field]):.6f}"
            for field in ["event_precision", "event_recall", "average_lead_minutes"]
        ]
    except (KeyError, TypeError, ValueError):
        metric_tokens = []
    checks["notebook_contains_current_test_metrics"] = bool(
        metric_tokens and all(token in serialized for token in metric_tokens)
    )
    return checks


def _close(left: Any, right: Any) -> bool:
    if left is None or right is None:
        return left is right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return bool(np.isclose(float(left), float(right), rtol=1e-10, atol=1e-12))
    return left == right


def _cvar95(returns: pd.Series) -> float:
    values = returns.dropna().astype(float)
    cutoff = values.quantile(0.05)
    return float(-values.loc[values.le(cutoff)].mean())


def _discover_identity_inputs(input_root: str | Path) -> list[Path]:
    root = Path(input_root)
    files = discover_parquet_files(root)
    official_event_file = find_official_event_file(root)
    if official_event_file is not None:
        resolved = {path.resolve() for path in files}
        if official_event_file.resolve() not in resolved:
            files.append(official_event_file)
    return files


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recompute and validate the complete Problem 1 delivery outputs."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Explicit input-data root; overrides project and legacy identity locations.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Offline output directory; defaults to <project>/outputs/demo.",
    )
    return parser


def _usable_validation_data_root(path: Path) -> bool:
    try:
        return bool(_discover_identity_inputs(path))
    except (FileNotFoundError, OSError):
        return False


def _select_validation_data_root(
    explicit_data_dir: str | Path | None,
    project_root: str | Path,
    identity: dict[str, object],
) -> Path | None:
    """Choose portable input data before considering a legacy absolute path."""

    if explicit_data_dir is not None:
        return Path(explicit_data_dir).expanduser().resolve()

    project_demo = Path(project_root).resolve() / "data" / "demo"
    if _usable_validation_data_root(project_demo):
        return project_demo

    if identity.get("version") != "option-risk-run-identity-v1":
        return None
    input_identity = identity.get("input_files")
    input_identity = input_identity if isinstance(input_identity, dict) else {}
    recorded_root = input_identity.get("root")
    if not isinstance(recorded_root, str) or not recorded_root.strip():
        return None
    legacy_root = Path(recorded_root).expanduser()
    if not legacy_root.is_absolute() or not _usable_validation_data_root(legacy_root):
        return None
    return legacy_root.resolve()


def _agent_policy_identity_complete(products: list[object]) -> bool:
    canonical_hash = DecisionPolicy().parameter_hash
    for row in products:
        if not isinstance(row, dict) or not isinstance(row.get("analysis"), dict):
            return False
        analysis = row["analysis"]
        policy_hash = analysis.get("policy_parameter_hash")
        if analysis.get("policy_version") != DECISION_POLICY_VERSION:
            return False
        if (
            not isinstance(policy_hash, str)
            or len(policy_hash) != 64
            or policy_hash != canonical_hash
        ):
            return False
        try:
            int(policy_hash, 16)
        except ValueError:
            return False
        transition_reason = analysis.get("transition_reason")
        if not isinstance(transition_reason, str) or not transition_reason.strip():
            return False
    return bool(products)


def _provenance_checks(
    *,
    summary: dict[str, object],
    features: pd.DataFrame,
    warnings: pd.DataFrame,
    bundle: object,
    input_files: list[Path],
    input_root: str | Path,
    source_root: str | Path | None = None,
) -> dict[str, bool]:
    """Recompute the offline identity and replay the only canonical policy."""

    config_payload = summary.get("config")
    try:
        if not isinstance(config_payload, dict):
            raise TypeError("run_summary.config must be an object")
        config = PipelineConfig(**config_payload)
    except (TypeError, ValueError):
        config = PipelineConfig()
        config_valid = False
    else:
        config_valid = True

    policy_payload = summary.get("primary_warning_policy")
    try:
        if not isinstance(policy_payload, dict):
            raise TypeError("run_summary.primary_warning_policy must be an object")
        if "policy_version" not in policy_payload or "policy_parameter_hash" not in policy_payload:
            raise ValueError("policy identity fields are required")
        policy = DecisionPolicy.from_diagnostics(policy_payload)
        if policy_payload["policy_parameter_hash"] != policy.parameter_hash:
            raise ValueError("policy parameter hash mismatch")
    except (TypeError, ValueError):
        policy = DecisionPolicy()
        policy_valid = False
    else:
        policy_valid = True

    identity = summary.get("run_identity")
    identity_payload = identity if isinstance(identity, dict) else {}
    checks: dict[str, bool] = {
        "validator_pipeline_config_valid": config_valid,
        "validator_primary_policy_identity_valid": policy_valid,
        "decision_source_matches_current_policy_version": bool(
            len(warnings)
            and "decision_source" in warnings
            and warnings["decision_source"].eq(DECISION_POLICY_VERSION).all()
        ),
        "decision_source_matches_warning_policy_version": bool(
            len(warnings)
            and "decision_source" in warnings
            and "policy_version" in warnings
            and warnings["decision_source"].astype("string").equals(
                warnings["policy_version"].astype("string")
            )
        ),
    }
    checks.update(
        run_identity_checks(
            identity_payload,
            features=features,
            config=config,
            input_files=input_files,
            input_root=input_root,
            policy=policy,
            source_root=source_root,
        )
    )
    if policy_valid:
        checks.update(replay_decision_policy_checks(features, warnings, policy))
    else:
        checks.update(
            {
                "decision_policy_replay_index_matches": False,
                "decision_policy_alert_levels_replay_exactly": False,
                "decision_policy_alert_emissions_replay_exactly": False,
                "decision_policy_version_matches_exactly": False,
                "decision_policy_parameter_hash_matches_exactly": False,
            }
        )
    checks.update(fixed_holdout_checks(summary, bundle))
    return checks


def main(argv: Sequence[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)
    output = (
        args.output_dir.expanduser().resolve()
        if args.output_dir is not None
        else PROJECT_ROOT / "outputs" / "demo"
    )
    required = [
        "run_summary.json",
        "risk_features.parquet",
        "risk_labels.parquet",
        "warning_predictions.parquet",
        "detected_events.csv",
        "warning_model.joblib",
        "cvar_backtest_daily.parquet",
        "latest_surface_grids.npz",
        "cvar_random_warning_baseline.parquet",
        "official_event_comparison.csv",
        "ablation_predictions_with_label_derived.parquet",
        "ml_predictions_raw_only.parquet",
        "figures/latest_iv_surface.png",
        "figures/latest_greeks_surfaces.png",
        "figures/test_alert_timeline.png",
    ]
    checks: dict[str, object] = {}
    checks["all_required_outputs_exist"] = all((output / name).is_file() for name in required)

    features = pd.read_parquet(output / "risk_features.parquet").set_index("datetime")
    warnings = pd.read_parquet(output / "warning_predictions.parquet").set_index("datetime")
    summary = json.loads((output / "run_summary.json").read_text(encoding="utf-8"))
    grids = np.load(output / "latest_surface_grids.npz")
    model = joblib.load(output / "warning_model.joblib")

    identity = summary.get("run_identity")
    identity = identity if isinstance(identity, dict) else {}
    selected_data_root = _select_validation_data_root(args.data_dir, PROJECT_ROOT, identity)
    if selected_data_root is not None:
        try:
            input_files = _discover_identity_inputs(selected_data_root)
        except (FileNotFoundError, OSError):
            input_files = []
        input_root = selected_data_root
    else:
        input_files = []
        input_root = PROJECT_ROOT / "data" / "demo"
    checks.update(
        _provenance_checks(
            summary=summary,
            features=features,
            warnings=warnings,
            bundle=model,
            input_files=input_files,
            input_root=input_root,
        )
    )

    checks["feature_index_unique"] = bool(features.index.is_unique)
    checks["feature_index_sorted"] = bool(features.index.is_monotonic_increasing)
    checks["warning_index_matches_features"] = bool(warnings.index.equals(features.index))
    checks["alert_levels_valid"] = bool(warnings["alert_level"].isin([0, 1, 2, 3]).all())
    checks["warning_explanations_complete"] = bool(
        warnings.loc[warnings["alert_level"].ge(2), "explanation"].astype("string").str.len().gt(0).all()
    )
    prohibited = "买入|卖出|开仓|交易建议"
    checks["no_trading_instruction_in_explanations"] = bool(
        ~warnings["explanation"].astype("string").str.contains(prohibited, regex=True).any()
    )
    test_months = sorted(
        warnings.index[warnings["split"].eq("test")].to_period("M").unique().astype(str).tolist()
    )
    checks["test_months"] = test_months
    checks["test_has_three_consecutive_months"] = test_months == ["2025-02", "2025-03", "2025-04"]
    checks["surface_grids_have_finite_values"] = all(
        bool(np.isfinite(grids[f"{metric}_values"]).any())
        for metric in ["iv", "delta", "gamma", "vega", "theta"]
    )
    checks["summary_test_rows_match"] = (
        int(warnings["split"].eq("test").sum()) >= summary["test_metrics"]["rows"]
    )
    checks["primary_model_excludes_label_derived_features"] = not any(
        column.startswith("pressure__")
        or column.startswith("history_q95__")
        or column in {"risk_pressure", "core_risk_pressure"}
        for column in model.feature_columns
    )
    checks["threshold_feasibility_is_explicit"] = "feasible_target_found" in summary[
        "model"
    ]["threshold_tuning"]
    checks["cvar_has_random_baseline"] = (
        summary["cvar_backtest"]["random_warning_date_baseline"].get("simulations") == 1000
    )
    checks["official_event_file_was_evaluated"] = (
        summary["official_event_comparison"].get("official_row_count") == 17
    )
    checks["primary_policy_is_pre_registered_fixed"] = bool(
        summary["primary_warning_policy"].get("selection_data")
        == PRIMARY_POLICY_SELECTION_DATA
    )
    checks["primary_predictions_identify_decision_source"] = bool(
        checks["decision_source_matches_current_policy_version"]
        and checks["decision_source_matches_warning_policy_version"]
    )
    recomputed_metrics = evaluate_alerts(
        warnings,
        PipelineConfig(**summary["config"]),
        split="test",
    )
    metric_fields = [
        "rows",
        "positive_label_rows",
        "alert_rows_level_2_or_3",
        "event_count",
        "alert_episode_count",
        "matched_events",
        "correct_alerts_with_event_in_0_to_8_bars",
        "event_precision",
        "event_recall",
        "average_lead_minutes",
        "minimum_lead_minutes",
    ]
    checks["recomputed_test_metrics_match_summary"] = all(
        _close(recomputed_metrics[field], summary["test_metrics"][field])
        for field in metric_fields
    )
    quality = summary["quality"]
    checks["quality_clean_rate_reconciles"] = _close(
        quality["clean_rate"],
        quality["clean_rows"] / quality["rows_after_product_filter"],
    )
    checks["no_duplicate_primary_key_rows"] = quality["duplicate_primary_key_rows_removed"] == 0
    checks["surface_snapshot_count_matches_features"] = (
        len(features) == summary["surface"]["snapshot_count"]
    )
    test_frame = warnings.loc[warnings["split"].eq("test")]
    checks["test_range_is_three_consecutive_months"] = bool(
        test_frame.index.min() == pd.Timestamp("2025-02-05 09:15:00")
        and test_frame.index.max() == pd.Timestamp("2025-04-30 15:00:00")
    )

    daily = pd.read_parquet(output / "cvar_backtest_daily.parquet")
    cvar_summary = summary["cvar_backtest"]
    cvar_checks: list[bool] = []
    for side in ["long", "short"]:
        baseline = _cvar95(daily[f"{side}_baseline_return"])
        warning = _cvar95(daily[f"{side}_warning_return"])
        improvement = (baseline - warning) / baseline
        cvar_checks.extend(
            [
                _close(baseline, cvar_summary[side]["baseline_cvar95"]),
                _close(warning, cvar_summary[side]["warning_cvar95"]),
                _close(improvement, cvar_summary[side]["improvement_rate"]),
            ]
        )
    checks["recomputed_long_short_cvar_matches_summary"] = all(cvar_checks)

    acceptance_path = output.parent / "agent_acceptance_full.json"
    artifact_path = output.parent / "问题1-Agent离线验收报告.artifact.json"
    checks["delivery_artifacts_exist"] = acceptance_path.is_file() and artifact_path.is_file()
    if checks["delivery_artifacts_exist"]:
        acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        products = acceptance["products"]
        checks["all_35_products_pass_full_agent_query"] = bool(
            acceptance["summary"] == {
                "status": "passed",
                "product_count": 35,
                "passed_products": 35,
                "failed_products": 0,
            }
            and len(products) == 35
            and all(row["status"] == "passed" for row in products)
        )
        checks["all_products_have_complete_problem_one_payload"] = all(
            set(row["analysis"]["surface_metrics"]) == EXPECTED_SURFACES
            and set(row["analysis"]["feature_groups"]) == EXPECTED_FEATURE_GROUPS
            and row["analysis"]["alert_level"] in {0, 1, 2, 3}
            and row["analysis"]["reason_count"] > 0
            and row["analysis"]["timeline_rows"] > 0
            and row["timestamp_count"] > 0
            for row in products
        ) and _agent_policy_identity_complete(products)
        snapshot = artifact["snapshot"]["datasets"]
        report_metrics = snapshot["backtest_summary"][0]
        checks["report_metrics_match_run_summary"] = all(
            [
                _close(report_metrics["event_precision"], summary["test_metrics"]["event_precision"]),
                _close(report_metrics["event_recall"], summary["test_metrics"]["event_recall"]),
                _close(
                    report_metrics["average_lead_minutes"],
                    summary["test_metrics"]["average_lead_minutes"],
                ),
                _close(
                    report_metrics["cvar_improvement"],
                    summary["cvar_backtest"]["average_improvement_rate"],
                ),
                _close(
                    report_metrics["random_cvar_median"],
                    summary["cvar_backtest"]["random_warning_date_baseline"]["median"],
                ),
            ]
        )
        coverage = {row["product"]: row for row in snapshot["product_coverage"]}
        checks["report_product_coverage_matches_acceptance"] = bool(
            len(coverage) == 35
            and all(
                coverage[row["product"]]["timestamp_count"] == row["timestamp_count"]
                and coverage[row["product"]]["latest_alert_level"]
                == row["analysis"]["alert_level"]
                for row in products
            )
        )
        checks.update(
            _html_artifact_checks(
                output.parent / "问题1-Agent离线验收报告.html",
                artifact,
            )
        )
        checks.update(
            _notebook_artifact_checks(
                PROJECT_ROOT / "notebooks" / "01_end_to_end_demo.ipynb",
                summary,
            )
        )
    checks["all_boolean_checks_pass"] = all(
        value for value in checks.values() if isinstance(value, bool)
    )
    (output / "validation_report.json").write_text(
        json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    if not checks["all_boolean_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
````

</details>
