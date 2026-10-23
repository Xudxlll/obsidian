---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/pipeline.py>)

SHA-256：`a860807429a70b8db7299b33f245b5a4486f2acf43ef8e2b702564943ad5d5a7`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .alerts import assign_walk_forward_alerts, evaluate_alerts, tune_predictive_rule
from .backtest import cvar_warning_backtest
from .config import PipelineConfig, PipelinePaths
from .decision import DecisionPolicy
from .features import extract_risk_features
from .io import discover_parquet_files, read_option_files
from .labels import build_forward_labels, event_table
from .model import fit_warning_model
from .official_events import (
    evaluate_official_events,
    find_official_event_file,
    load_official_events,
)
from .quality import clean_and_profile
from .provenance import build_run_identity, fixed_holdout_checks
from .surfaces import build_surface_nodes, choose_latest_complete_snapshot, surface_grid
from .visualization import (
    plot_alert_timeline,
    plot_greeks_heatmaps,
    plot_surface_3d,
    save_snapshot_grids,
)


def _json_default(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, (pd.Timestamp, pd.Period, Path)):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(f"Cannot serialize {type(value)!r}")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8"
    )


def _identity_input_files(
    parquet_files: list[Path], official_event_file: Path | None
) -> list[Path]:
    """Return every input actually consulted by the offline run."""

    result = list(parquet_files)
    if official_event_file is not None:
        resolved = {path.resolve() for path in result}
        if official_event_file.resolve() not in resolved:
            result.append(official_event_file)
    return result


def _attach_run_identity(
    summary: dict[str, object],
    *,
    features: pd.DataFrame,
    config: PipelineConfig,
    input_files: list[Path],
    input_root: str | Path,
    bundle: object,
    source_root: str | Path | None = None,
) -> dict[str, object]:
    """Bind an offline summary to the exact code, data, config, and policy used."""

    diagnostics = summary.get("primary_warning_policy")
    if not isinstance(diagnostics, dict):
        raise ValueError("primary_warning_policy diagnostics are required for run identity")
    policy = DecisionPolicy.from_diagnostics(diagnostics)
    if diagnostics.get("policy_parameter_hash") != policy.parameter_hash:
        raise ValueError("primary_warning_policy must contain the canonical policy parameter hash")

    summary["run_identity"] = build_run_identity(
        features=features,
        config=config,
        input_files=input_files,
        input_root=input_root,
        policy=policy,
        source_root=source_root,
        calibration_end=str(getattr(bundle, "validation_end")),
        test_start=str(getattr(bundle, "test_start")),
        test_end=str(getattr(bundle, "test_end")),
        fixed_holdout_no_test_label_reuse=True,
    )
    holdout = fixed_holdout_checks(summary, bundle)
    if not all(holdout.values()):
        summary.pop("run_identity", None)
        failed = sorted(name for name, passed in holdout.items() if not passed)
        raise ValueError(f"Cannot attest fixed holdout protocol; failed checks: {failed}")
    return summary


def _rule_baseline(
    features: pd.DataFrame, model_predictions: pd.DataFrame
) -> pd.DataFrame:
    rule = model_predictions[["split", "label", "event_start", "label_available"]].copy()
    pressure = features["risk_pressure"].replace([np.inf, -np.inf], np.nan)
    rule["risk_probability"] = (1.0 - np.exp(-(pressure - 0.5).clip(lower=0))).clip(0, 1)
    rule["alert_level"] = 0
    rule.loc[pressure.ge(0.80), "alert_level"] = 1
    rule.loc[pressure.ge(1.00), "alert_level"] = 2
    rule.loc[pressure.ge(1.50), "alert_level"] = 3
    rule.loc[~features["data_ready"].fillna(False), "alert_level"] = 0
    rule["alert_emitted"] = rule["alert_level"].ge(2)
    return rule


def _effective_labels_for_output(
    labels: pd.DataFrame, predictions: pd.DataFrame
) -> pd.DataFrame:
    """Use the model's split-purged label availability in the formal label artifact."""

    missing = [column for column in labels.columns if column not in predictions]
    if missing:
        raise ValueError(f"Predictions are missing label output columns: {missing}")
    if not labels.index.equals(predictions.index):
        raise ValueError("Labels and predictions must have the same ordered index")
    return predictions.loc[:, labels.columns].copy()


def run_pipeline(
    data_dir: str | Path,
    output_dir: str | Path,
    config: PipelineConfig | None = None,
) -> dict[str, object]:
    config = config or PipelineConfig()
    paths = PipelinePaths(Path(data_dir), Path(output_dir))
    paths.ensure()

    files = discover_parquet_files(paths.data_dir)
    raw, ingest_profile = read_option_files(
        files,
        product=config.product,
        start_date=config.start_date,
        end_date=config.end_date,
    )
    cleaned, quality_profile = clean_and_profile(raw, config, ingest_profile)
    nodes = build_surface_nodes(cleaned)
    features = extract_risk_features(cleaned, nodes, config)
    labels = build_forward_labels(features, config)
    bundle, predictions, model_diagnostics = fit_warning_model(
        features, labels, config, include_label_derived=False
    )
    ml_alerts, alert_policy_diagnostics = assign_walk_forward_alerts(
        features, predictions, bundle, config
    )
    alerts, predictive_rule_diagnostics = tune_predictive_rule(
        features, predictions, config
    )
    alerts["reference_underlying_price"] = features["reference_underlying_price"]
    derived_bundle, derived_predictions, derived_diagnostics = fit_warning_model(
        features, labels, config, include_label_derived=True
    )
    derived_alerts, derived_alert_policy_diagnostics = assign_walk_forward_alerts(
        features, derived_predictions, derived_bundle, config
    )
    rule = _rule_baseline(features, predictions)
    effective_labels = _effective_labels_for_output(labels, predictions)

    validation_metrics = evaluate_alerts(alerts, config, split="validation")
    test_metrics = evaluate_alerts(alerts, config, split="test")
    ml_test_metrics = evaluate_alerts(ml_alerts, config, split="test")
    rule_test_metrics = evaluate_alerts(rule, config, split="test")
    derived_test_metrics = evaluate_alerts(derived_alerts, config, split="test")
    cvar_metrics, cvar_detail, random_cvar = cvar_warning_backtest(
        alerts, random_state=config.random_state
    )

    official_event_file = find_official_event_file(paths.data_dir)
    if official_event_file is not None:
        official_events = load_official_events(official_event_file)
        official_event_metrics, official_event_detail = evaluate_official_events(
            official_events, alerts, config
        )
    else:
        official_event_metrics = {"available": False, "reason": "extreme_event.csv not found"}
        official_event_detail = pd.DataFrame()

    features.reset_index(names="datetime").to_parquet(paths.output_dir / "risk_features.parquet")
    effective_labels.reset_index(names="datetime").to_parquet(
        paths.output_dir / "risk_labels.parquet"
    )
    alerts.reset_index(names="datetime").to_parquet(paths.output_dir / "warning_predictions.parquet")
    derived_alerts.reset_index(names="datetime").to_parquet(
        paths.output_dir / "ablation_predictions_with_label_derived.parquet"
    )
    ml_alerts.reset_index(names="datetime").to_parquet(
        paths.output_dir / "ml_predictions_raw_only.parquet"
    )
    # Event starts remain an objective full-sequence chronology.  They are not
    # label rows used by fitting/calibration; availability is governed by the
    # split-purged risk_labels artifact above.
    event_table(labels).to_csv(paths.output_dir / "detected_events.csv", index=False, encoding="utf-8-sig")
    cvar_detail.reset_index(names="date").to_parquet(paths.output_dir / "cvar_backtest_daily.parquet")
    random_cvar.to_parquet(paths.output_dir / "cvar_random_warning_baseline.parquet", index=False)
    official_event_detail.to_csv(
        paths.output_dir / "official_event_comparison.csv", index=False, encoding="utf-8-sig"
    )
    bundle.save(str(paths.output_dir / "warning_model.joblib"))

    latest = choose_latest_complete_snapshot(
        nodes,
        min_expiries=config.min_expiries_per_snapshot,
        min_nodes=config.min_quotes_per_snapshot,
    )
    figures = paths.output_dir / "figures"
    plot_surface_3d(surface_grid(nodes, "iv", latest), figures / "latest_iv_surface.png")
    plot_greeks_heatmaps(nodes, latest, figures / "latest_greeks_surfaces.png")
    plot_alert_timeline(alerts, figures / "test_alert_timeline.png")
    save_snapshot_grids(nodes, latest, paths.output_dir / "latest_surface_grids.npz")

    summary: dict[str, object] = {
        "project": "Commodity option volatility-surface risk warning prototype",
        "config": config.to_dict(),
        "quality": quality_profile,
        "surface": {
            "surface_node_rows": int(len(nodes)),
            "snapshot_count": int(nodes["datetime"].nunique()),
            "latest_complete_snapshot": latest,
            "latest_expiry_count": int(nodes.loc[nodes["datetime"].eq(latest), "dte"].nunique()),
        },
        "model": model_diagnostics,
        "primary_warning_policy": predictive_rule_diagnostics,
        "alert_policy_walk_forward": alert_policy_diagnostics,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
        "rule_baseline_test_metrics": rule_test_metrics,
        "feature_leakage_ablation": {
            "raw_only_ml_model": ml_test_metrics,
            "with_label_derived_features": derived_test_metrics,
            "with_label_derived_model_diagnostics": derived_diagnostics,
            "with_label_derived_alert_policy": derived_alert_policy_diagnostics,
            "interpretation": "The ML ablation is separate from the primary transparent dynamic-rule warning policy. The raw-only ML model excludes pressure__, history_q95__, risk_pressure and core_risk_pressure; the second ML model retains them only as a comparator.",
        },
        "cvar_backtest": cvar_metrics,
        "official_event_comparison": official_event_metrics,
        "outputs": {
            "features": "risk_features.parquet",
            "labels": "risk_labels.parquet",
            "predictions": "warning_predictions.parquet",
            "events": "detected_events.csv",
            "model": "warning_model.joblib",
            "cvar_daily": "cvar_backtest_daily.parquet",
            "cvar_random_baseline": "cvar_random_warning_baseline.parquet",
            "official_events": "official_event_comparison.csv",
            "ablation_predictions": "ablation_predictions_with_label_derived.parquet",
            "raw_only_ml_predictions": "ml_predictions_raw_only.parquet",
            "iv_surface": "figures/latest_iv_surface.png",
            "greeks_surfaces": "figures/latest_greeks_surfaces.png",
            "alert_timeline": "figures/test_alert_timeline.png",
        },
    }
    _attach_run_identity(
        summary,
        features=features,
        config=config,
        input_files=_identity_input_files(files, official_event_file),
        input_root=paths.data_dir,
        bundle=bundle,
    )
    _write_json(paths.output_dir / "run_summary.json", summary)
    return summary
````

</details>
