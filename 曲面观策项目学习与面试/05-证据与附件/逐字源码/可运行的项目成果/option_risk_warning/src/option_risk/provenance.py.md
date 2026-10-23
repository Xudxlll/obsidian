---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/provenance.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/provenance.py>)

SHA-256：`a950cfb4ceead2d63ce574c31f5ec2036a43bb09c613fcbb04f0a28a44dd5d31`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

import numpy as np
import pandas as pd

from .config import PipelineConfig
from .decision import (
    PRIMARY_POLICY_SELECTION_DATA,
    DecisionPolicy,
    PRESSURE_SPECS,
    apply_decision_policy,
)
from .features import FEATURE_SCHEMA_VERSION


RUN_IDENTITY_VERSION = "option-risk-run-identity-v3"
FIXED_HOLDOUT_PROTOCOL = "fixed_holdout_no_test_label_reuse"
INPUT_FINGERPRINT_ALGORITHM = "sha256(relative-path,size,sha256-content)-v3"
SOURCE_TREE_HASH_ALGORITHM = "sha256(relative-path,sha256-content)-v1"
FORWARD_LABEL_BOUNDARY_PURGE_POLICY = "forward_label_window_must_remain_within_split"

PRESSURE_COLUMNS = tuple(PRESSURE_SPECS)
HISTORY_COLUMNS = tuple(
    f"history_q95__{feature_name}" for _, feature_name, _ in PRESSURE_SPECS.values()
)
EXCLUDED_LABEL_DERIVED_COLUMNS = (
    *PRESSURE_COLUMNS,
    *HISTORY_COLUMNS,
    "risk_pressure",
    "core_risk_pressure",
)


def _json_value(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _json_value(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_json_value(item) for item in value), key=repr)
    if isinstance(value, (Path, pd.Timestamp, pd.Period, pd.Timedelta)):
        return str(value)
    if isinstance(value, np.ndarray):
        return [_json_value(item) for item in value.tolist()]
    if isinstance(value, np.generic):
        return _json_value(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return {"__float__": "Infinity" if value > 0 else "-Infinity" if value < 0 else "NaN"}
    return value


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        _json_value(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256_json(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _content_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _relative_name(path: Path, root: Path) -> str:
    resolved_path = path.resolve()
    resolved_root = root.resolve()
    if resolved_root.is_file():
        if resolved_path != resolved_root:
            raise ValueError(f"Input file {resolved_path} is outside input root {resolved_root}")
        return resolved_path.name
    try:
        return resolved_path.relative_to(resolved_root).as_posix()
    except ValueError as exc:
        raise ValueError(
            f"Input file {resolved_path} is outside input root {resolved_root}"
        ) from exc


def _input_file_identity(input_files: Iterable[str | Path], input_root: str | Path) -> dict[str, object]:
    root = Path(input_root)
    entries: list[dict[str, object]] = []
    for file_path in input_files:
        path = Path(file_path)
        entries.append(
            {
                "relative_path": _relative_name(path, root),
                "size": path.stat().st_size,
                "content_sha256": _content_sha256(path),
            }
        )
    entries.sort(key=lambda item: str(item["relative_path"]))
    return {
        "root_hint": ".",
        "file_count": len(entries),
        "algorithm": INPUT_FINGERPRINT_ALGORITHM,
        "fingerprint_sha256": _sha256_json(entries),
        "files": entries,
    }


def _source_tree_identity(source_root: str | Path | None = None) -> dict[str, object]:
    root = Path(source_root) if source_root is not None else Path(__file__).resolve().parent
    entries = [
        {
            "relative_path": path.relative_to(root).as_posix(),
            "content_sha256": _content_sha256(path),
        }
        for path in sorted(root.rglob("*.py"), key=lambda item: item.as_posix())
        if path.is_file()
    ]
    return {
        "root_hint": ".",
        "python_file_count": len(entries),
        "algorithm": SOURCE_TREE_HASH_ALGORITHM,
        "sha256": _sha256_json(entries),
    }


def _package_version() -> str:
    try:
        return version("option-risk-warning")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        if pyproject.is_file():
            for line in pyproject.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("version") and "=" in line:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        return "unknown"


def _feature_schema(features: pd.DataFrame) -> dict[str, object]:
    ordered_columns = [str(column) for column in features.columns]
    return {
        "version": FEATURE_SCHEMA_VERSION,
        "ordered_feature_column_count": len(ordered_columns),
        "ordered_feature_columns": ordered_columns,
        "ordered_feature_columns_sha256": _sha256_json(ordered_columns),
        "pressure_columns": list(PRESSURE_COLUMNS),
        "pressure_column_count": len(PRESSURE_COLUMNS),
        "history_columns": list(HISTORY_COLUMNS),
        "history_column_count": len(HISTORY_COLUMNS),
        "excluded_label_derived_columns": list(EXCLUDED_LABEL_DERIVED_COLUMNS),
        "excluded_label_derived_column_count": len(EXCLUDED_LABEL_DERIVED_COLUMNS),
    }


def _feature_contract_status(features: pd.DataFrame) -> tuple[bool, bool, bool]:
    ordered_columns = [str(column) for column in features.columns]
    observed_pressure = [column for column in ordered_columns if column.startswith("pressure__")]
    observed_history = [column for column in ordered_columns if column.startswith("history_q95__")]
    pressure_ok = len(observed_pressure) == 12 and set(observed_pressure) == set(PRESSURE_COLUMNS)
    history_ok = len(observed_history) == 12 and set(observed_history) == set(HISTORY_COLUMNS)
    exclusions_ok = bool(
        len(EXCLUDED_LABEL_DERIVED_COLUMNS) == 26
        and all(ordered_columns.count(column) == 1 for column in EXCLUDED_LABEL_DERIVED_COLUMNS)
    )
    return pressure_ok, history_ok, exclusions_ok


def decision_policy_parameter_sha256(policy: DecisionPolicy) -> str:
    canonical_hash = getattr(policy, "parameter_hash", None)
    if canonical_hash is not None:
        return str(canonical_hash)
    parameters = asdict(policy)
    parameters.pop("policy_version", None)
    return _sha256_json(parameters)


def _decision_policy_identity(policy: DecisionPolicy) -> dict[str, object]:
    parameters = asdict(policy)
    parameters.pop("policy_version", None)
    parameters.pop("policy_hash", None)
    return {
        "selection_data": PRIMARY_POLICY_SELECTION_DATA,
        "version": policy.policy_version,
        "parameters": _json_value(parameters),
        "parameter_sha256": decision_policy_parameter_sha256(policy),
        "policy_parameter_hash": decision_policy_parameter_sha256(policy),
    }


def pipeline_config_sha256(config: PipelineConfig) -> str:
    return _sha256_json({"type": "PipelineConfig", "parameters": config.to_dict()})


def _forward_label_boundary_purge_contract(horizon_bars: int) -> dict[str, object]:
    return {
        "policy": FORWARD_LABEL_BOUNDARY_PURGE_POLICY,
        "horizon_bars": horizon_bars,
        "train_to_validation_rows": horizon_bars,
        "validation_to_test_rows": horizon_bars,
        "total_rows": 2 * horizon_bars,
    }


def build_run_identity(
    *,
    features: pd.DataFrame,
    config: PipelineConfig,
    input_files: Iterable[str | Path],
    input_root: str | Path,
    policy: DecisionPolicy,
    calibration_end: str,
    test_start: str,
    test_end: str,
    fixed_holdout_no_test_label_reuse: bool,
    source_root: str | Path | None = None,
) -> dict[str, object]:
    """Build the reproducible identity embedded in every offline run summary."""

    pressure_ok, history_ok, exclusions_ok = _feature_contract_status(features)
    if not pressure_ok:
        raise ValueError("Feature schema must contain exactly the canonical 12 pressure columns")
    if not history_ok:
        raise ValueError("Feature schema must contain exactly the canonical 12 history columns")
    if not exclusions_ok:
        raise ValueError("Feature schema must contain exactly the 26 label-derived exclusions")
    if policy != DecisionPolicy():
        raise ValueError("Run identity requires the pre-registered canonical DecisionPolicy")

    return {
        "version": RUN_IDENTITY_VERSION,
        "feature_schema": _feature_schema(features),
        "decision_policy": _decision_policy_identity(policy),
        "pipeline_config_sha256": pipeline_config_sha256(config),
        "input_files": _input_file_identity(input_files, input_root),
        "source_tree": _source_tree_identity(source_root),
        "package_version": _package_version(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evaluation_protocol": {
            "name": FIXED_HOLDOUT_PROTOCOL,
            "fixed_holdout_no_test_label_reuse": bool(fixed_holdout_no_test_label_reuse),
            "calibration_end": str(calibration_end),
            "test_start": str(test_start),
            "test_end": str(test_end),
            "forward_label_boundary_purge": _forward_label_boundary_purge_contract(
                config.horizon_bars
            ),
        },
    }


def _is_utc_timestamp(value: object) -> bool:
    try:
        parsed = datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def run_identity_checks(
    identity: Mapping[str, object] | None,
    *,
    features: pd.DataFrame,
    config: PipelineConfig,
    input_files: Iterable[str | Path],
    input_root: str | Path,
    policy: DecisionPolicy,
    source_root: str | Path | None = None,
) -> dict[str, bool]:
    """Recompute every material identity component and reject stale artifacts."""

    payload = dict(identity or {})
    saved_schema = payload.get("feature_schema")
    saved_policy = payload.get("decision_policy")
    saved_inputs = payload.get("input_files")
    saved_source = payload.get("source_tree")
    saved_protocol = payload.get("evaluation_protocol")
    saved_schema = saved_schema if isinstance(saved_schema, Mapping) else {}
    saved_policy = saved_policy if isinstance(saved_policy, Mapping) else {}
    saved_inputs = saved_inputs if isinstance(saved_inputs, Mapping) else {}
    saved_source = saved_source if isinstance(saved_source, Mapping) else {}
    saved_protocol = saved_protocol if isinstance(saved_protocol, Mapping) else {}

    current_schema = _feature_schema(features)
    current_policy = _decision_policy_identity(policy)
    try:
        current_inputs = _input_file_identity(input_files, input_root)
    except (FileNotFoundError, OSError, ValueError):
        current_inputs = {}
    try:
        current_source = _source_tree_identity(source_root)
    except (FileNotFoundError, OSError):
        current_source = {}

    exact_pressure_columns, exact_history_columns, exact_exclusions = _feature_contract_status(
        features
    )

    return {
        "identity_present": bool(payload),
        "identity_version_matches": payload.get("version") == RUN_IDENTITY_VERSION,
        "identity_generated_at_is_utc": _is_utc_timestamp(payload.get("generated_at")),
        "identity_package_version_matches": payload.get("package_version") == _package_version(),
        "identity_feature_schema_version_matches": saved_schema.get("version")
        == FEATURE_SCHEMA_VERSION,
        "identity_ordered_feature_columns_match": saved_schema.get(
            "ordered_feature_columns_sha256"
        )
        == current_schema["ordered_feature_columns_sha256"],
        "identity_pressure_column_contract_matches": bool(
            exact_pressure_columns
            and saved_schema.get("pressure_columns") == current_schema["pressure_columns"]
            and saved_schema.get("pressure_column_count") == 12
        ),
        "identity_history_column_contract_matches": bool(
            exact_history_columns
            and saved_schema.get("history_columns") == current_schema["history_columns"]
            and saved_schema.get("history_column_count") == 12
        ),
        "identity_26_column_exclusion_contract_matches": bool(
            saved_schema.get("excluded_label_derived_columns")
            == current_schema["excluded_label_derived_columns"]
            and saved_schema.get("excluded_label_derived_column_count") == 26
            and exact_exclusions
        ),
        "identity_decision_policy_version_matches": saved_policy.get("version")
        == current_policy["version"],
        "identity_decision_policy_is_pre_registered_fixed": saved_policy.get(
            "selection_data"
        )
        == PRIMARY_POLICY_SELECTION_DATA,
        "identity_decision_policy_parameters_match": bool(
            saved_policy.get("parameter_sha256") == current_policy["parameter_sha256"]
            and saved_policy.get("policy_parameter_hash")
            == current_policy["policy_parameter_hash"]
        ),
        "identity_pipeline_config_matches": payload.get("pipeline_config_sha256")
        == pipeline_config_sha256(config),
        "identity_forward_label_boundary_purge_matches_config": saved_protocol.get(
            "forward_label_boundary_purge"
        )
        == _forward_label_boundary_purge_contract(config.horizon_bars),
        "identity_input_files_match": bool(
            current_inputs
            and saved_inputs.get("algorithm") == INPUT_FINGERPRINT_ALGORITHM
            and saved_inputs.get("file_count") == current_inputs.get("file_count")
            and saved_inputs.get("fingerprint_sha256")
            == current_inputs.get("fingerprint_sha256")
        ),
        "identity_source_tree_matches": bool(
            current_source
            and saved_source.get("algorithm") == SOURCE_TREE_HASH_ALGORITHM
            and saved_source.get("python_file_count") == current_source.get("python_file_count")
            and saved_source.get("sha256") == current_source.get("sha256")
        ),
    }


def replay_decision_policy_checks(
    features: pd.DataFrame,
    warnings: pd.DataFrame,
    policy: DecisionPolicy,
) -> dict[str, bool]:
    """Replay the canonical state machine and require byte-for-byte policy identity."""

    canonical = apply_decision_policy(features, policy)
    indices_match = warnings.index.equals(canonical.index)
    levels_match = False
    if indices_match and "alert_level" in warnings and "alert_level" in canonical:
        left = pd.to_numeric(warnings["alert_level"], errors="coerce")
        right = pd.to_numeric(canonical["alert_level"], errors="coerce")
        levels_match = bool(left.equals(right))
    emissions_match = bool(
        indices_match
        and "alert_emitted" in warnings
        and "alert_emitted" in canonical
        and warnings["alert_emitted"].fillna(False).astype(bool).equals(
            canonical["alert_emitted"].fillna(False).astype(bool)
        )
    )
    versions_match = bool(
        indices_match
        and "policy_version" in warnings
        and "policy_version" in canonical
        and warnings["policy_version"].astype("string").equals(
            canonical["policy_version"].astype("string")
        )
    )
    canonical_has_hash = "policy_parameter_hash" in canonical
    hashes_match = bool(
        not canonical_has_hash
        or (
            indices_match
            and "policy_parameter_hash" in warnings
            and warnings["policy_parameter_hash"].astype("string").equals(
                canonical["policy_parameter_hash"].astype("string")
            )
        )
    )
    return {
        "decision_policy_replay_index_matches": indices_match,
        "decision_policy_alert_levels_replay_exactly": levels_match,
        "decision_policy_alert_emissions_replay_exactly": emissions_match,
        "decision_policy_version_matches_exactly": versions_match,
        "decision_policy_parameter_hash_matches_exactly": hashes_match,
    }


def _month(value: object) -> pd.Period | None:
    if value in (None, ""):
        return None
    try:
        return pd.Period(value, freq="M")
    except (TypeError, ValueError):
        return None


def _diagnostic_protocol_checks(diagnostics: object, test_start: pd.Period | None) -> tuple[bool, bool]:
    if not isinstance(diagnostics, list) or not diagnostics:
        return False, False
    protocol_ok = True
    calibration_ok = test_start is not None
    for diagnostic in diagnostics:
        if not isinstance(diagnostic, Mapping):
            return False, False
        protocol_ok = protocol_ok and diagnostic.get("test_protocol") == FIXED_HOLDOUT_PROTOCOL
        calibration = _month(diagnostic.get("calibration_month"))
        calibration_ok = calibration_ok and calibration is not None and calibration < test_start
    return protocol_ok, calibration_ok


def _boundary_purge_matches_horizon(diagnostics: Mapping[str, object], horizon: int) -> bool:
    purge = diagnostics.get("forward_label_boundary_purge")
    if not isinstance(purge, Mapping):
        return False
    return bool(
        purge.get("policy") == FORWARD_LABEL_BOUNDARY_PURGE_POLICY
        and purge.get("horizon_bars") == horizon
        and purge.get("train_to_validation_rows") == horizon
        and purge.get("validation_to_test_rows") == horizon
        and purge.get("total_rows") == 2 * horizon
    )


def fixed_holdout_checks(summary: Mapping[str, object], bundle: object) -> dict[str, bool]:
    """Verify that all calibration ends before the untouched fixed test period."""

    model = summary.get("model")
    model = model if isinstance(model, Mapping) else {}
    ablation = summary.get("feature_leakage_ablation")
    ablation = ablation if isinstance(ablation, Mapping) else {}
    derived_model = ablation.get("with_label_derived_model_diagnostics")
    derived_model = derived_model if isinstance(derived_model, Mapping) else {}
    primary_policy = summary.get("primary_warning_policy")
    primary_policy = primary_policy if isinstance(primary_policy, Mapping) else {}
    run_identity = summary.get("run_identity")
    run_identity = run_identity if isinstance(run_identity, Mapping) else {}
    protocol = run_identity.get("evaluation_protocol")
    protocol = protocol if isinstance(protocol, Mapping) else {}
    config = summary.get("config")
    config = config if isinstance(config, Mapping) else {}
    try:
        horizon_bars = int(config.get("horizon_bars"))
    except (TypeError, ValueError):
        horizon_bars = -1
    split_boundary_purge_ok = bool(
        horizon_bars >= 0
        and _boundary_purge_matches_horizon(model, horizon_bars)
        and _boundary_purge_matches_horizon(derived_model, horizon_bars)
        and _boundary_purge_matches_horizon(protocol, horizon_bars)
    )

    bundle_calibration = _month(getattr(bundle, "validation_end", None))
    bundle_test_start = _month(getattr(bundle, "test_start", None))
    bundle_test_end = _month(getattr(bundle, "test_end", None))
    identity_calibration = _month(protocol.get("calibration_end"))
    identity_test_start = _month(protocol.get("test_start"))
    identity_test_end = _month(protocol.get("test_end"))
    calibration_precedes_test = bool(
        bundle_calibration is not None
        and bundle_test_start is not None
        and bundle_calibration < bundle_test_start
        and identity_calibration is not None
        and identity_calibration < bundle_test_start
    )

    alert_protocol_ok, alert_calibration_ok = _diagnostic_protocol_checks(
        summary.get("alert_policy_walk_forward"), bundle_test_start
    )
    derived_protocol_ok, derived_calibration_ok = _diagnostic_protocol_checks(
        ablation.get("with_label_derived_alert_policy"), bundle_test_start
    )
    model_fixed = bool(
        model.get("test_protocol") == FIXED_HOLDOUT_PROTOCOL
        and model.get("walk_forward_folds") == []
        and _boundary_purge_matches_horizon(model, horizon_bars)
    )
    derived_model_fixed = bool(
        derived_model.get("test_protocol") == FIXED_HOLDOUT_PROTOCOL
        and derived_model.get("walk_forward_folds") == []
        and _boundary_purge_matches_horizon(derived_model, horizon_bars)
    )
    identity_matches_bundle = bool(
        protocol.get("name") == FIXED_HOLDOUT_PROTOCOL
        and protocol.get("fixed_holdout_no_test_label_reuse") is True
        and identity_calibration == bundle_calibration
        and identity_test_start == bundle_test_start
        and identity_test_end == bundle_test_end
        and _boundary_purge_matches_horizon(protocol, horizon_bars)
    )
    try:
        selected_policy = DecisionPolicy.from_diagnostics(dict(primary_policy))
    except (TypeError, ValueError):
        primary_policy_identity_current = False
    else:
        primary_policy_identity_current = bool(
            primary_policy.get("policy_version") == selected_policy.policy_version
            and primary_policy.get("policy_parameter_hash") == selected_policy.parameter_hash
        )
    all_calibration_precedes = bool(
        calibration_precedes_test and alert_calibration_ok and derived_calibration_ok
    )
    no_reuse = bool(
        identity_matches_bundle
        and primary_policy.get("selection_data") == PRIMARY_POLICY_SELECTION_DATA
        and primary_policy_identity_current
        and model_fixed
        and derived_model_fixed
        and alert_protocol_ok
        and derived_protocol_ok
        and all_calibration_precedes
        and split_boundary_purge_ok
    )
    return {
        "fixed_holdout_protocol_identity_matches_model_bundle": identity_matches_bundle,
        "fixed_holdout_primary_policy_is_pre_registered_fixed": primary_policy.get(
            "selection_data"
        )
        == PRIMARY_POLICY_SELECTION_DATA,
        "fixed_holdout_primary_policy_identity_is_current": primary_policy_identity_current,
        "fixed_holdout_model_has_no_test_label_reuse": model_fixed,
        "fixed_holdout_ablation_model_has_no_test_label_reuse": derived_model_fixed,
        "fixed_holdout_split_boundary_labels_are_purged": split_boundary_purge_ok,
        "fixed_holdout_alert_policies_have_no_test_label_reuse": bool(
            alert_protocol_ok and derived_protocol_ok
        ),
        "fixed_holdout_all_calibration_precedes_test_start": all_calibration_precedes,
        "fixed_holdout_no_test_label_reuse": no_reuse,
    }
````

</details>
