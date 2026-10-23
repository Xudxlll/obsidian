---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/model.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/model.py>)

SHA-256：`7b5d19e7401d12808b88d3c040b021308c72a4886edaad8851b2a6c53fbbadde`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import dataclass

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler

from .config import PipelineConfig
from .labels import purge_split_boundary_labels


@dataclass
class ModelBundle:
    estimator: object
    feature_columns: list[str]
    attention_threshold: float
    warning_threshold: float
    danger_threshold: float
    train_end: str
    validation_end: str
    test_start: str
    test_end: str
    feature_policy: str

    def save(self, path: str) -> None:
        joblib.dump(self, path)


def chronological_month_split(
    index: pd.DatetimeIndex, config: PipelineConfig
) -> tuple[pd.Period, pd.Period, pd.Period, pd.Period]:
    months = sorted(pd.Series(index.to_period("M").unique()).dropna().tolist())
    required = config.validation_months + config.test_months + 2
    if len(months) < required:
        raise ValueError(
            f"Need at least {required} distinct months for train/validation/test; found {len(months)}"
        )
    test_start = months[-config.test_months]
    validation_start = months[-(config.test_months + config.validation_months)]
    train_end = months[-(config.test_months + config.validation_months + 1)]
    return train_end, validation_start, test_start, months[-1]


def _candidate_columns(
    features: pd.DataFrame, include_label_derived: bool = False
) -> list[str]:
    numeric = features.select_dtypes(include=[np.number, "bool"]).columns.tolist()
    excluded = {"data_ready", "history_ready"}
    if not include_label_derived:
        excluded.update({"risk_pressure", "core_risk_pressure"})
        excluded.update(
            column
            for column in numeric
            if column.startswith("pressure__") or column.startswith("history_q95__")
        )
    return [column for column in numeric if column not in excluded]


def _tune_warning_threshold(
    y_true: pd.Series, probability: np.ndarray
) -> tuple[float, dict[str, object]]:
    grid = np.unique(
        np.concatenate(
            [
                np.geomspace(0.001, 0.05, 16),
                np.linspace(0.05, 0.95, 73),
                1.0 - np.geomspace(0.001, 0.05, 16),
            ]
        )
    )
    candidates: list[tuple[bool, float, float, float, float]] = []
    for threshold in grid:
        predicted = probability >= threshold
        precision = precision_score(y_true, predicted, zero_division=0)
        recall = recall_score(y_true, predicted, zero_division=0)
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        candidates.append((precision >= 0.50 and recall >= 0.60, f1, recall, precision, threshold))
    feasible = [row for row in candidates if row[0]]
    selected = max(feasible or candidates, key=lambda row: (row[1], row[2], row[3]))
    threshold = float(selected[-1])
    diagnostics = {
        "feasible_target_found": bool(feasible),
        "selected_threshold": threshold,
        "selected_f1": float(selected[1]),
        "selected_recall": float(selected[2]),
        "selected_precision": float(selected[3]),
        "grid_min": float(grid.min()),
        "grid_max": float(grid.max()),
        "selected_at_grid_boundary": bool(
            np.isclose(threshold, grid.min()) or np.isclose(threshold, grid.max())
        ),
    }
    return threshold, diagnostics


def _fit_estimator(X_train: pd.DataFrame, y_train: pd.Series, config: PipelineConfig) -> object:
    if y_train.nunique() < 2:
        estimator: object = DummyClassifier(strategy="prior")
        estimator.fit(X_train.fillna(0), y_train)
        return estimator
    estimator = make_pipeline(
        SimpleImputer(strategy="median", add_indicator=True),
        RobustScaler(),
        LogisticRegression(
            C=0.25,
            max_iter=2000,
            class_weight="balanced",
            random_state=config.random_state,
        ),
    )
    estimator.fit(X_train, y_train)
    return estimator


def _positive_probability(estimator: object, X: pd.DataFrame) -> np.ndarray:
    if isinstance(estimator, DummyClassifier):
        probability = estimator.predict_proba(X.fillna(0))
        classes = list(estimator.classes_)
    else:
        probability = estimator.predict_proba(X)
        classes = list(estimator.classes_)
    if 1 not in classes:
        return np.zeros(len(X), dtype=float)
    return probability[:, classes.index(1)]


def fit_warning_model(
    features: pd.DataFrame,
    labels: pd.DataFrame,
    config: PipelineConfig,
    include_label_derived: bool = False,
) -> tuple[ModelBundle, pd.DataFrame, dict[str, object]]:
    train_end, validation_start, test_start, test_end = chronological_month_split(
        pd.DatetimeIndex(features.index), config
    )
    periods = features.index.to_period("M")
    splits = pd.Series(
        np.select(
            [periods <= train_end, periods == validation_start, periods >= test_start],
            ["train", "validation", "test"],
            default="gap",
        ),
        index=features.index,
        dtype="string",
    )
    effective_labels, boundary_purge = purge_split_boundary_labels(
        labels, splits, horizon_bars=config.horizon_bars
    )
    available = effective_labels["label_available"].fillna(False)
    train_mask = available & (periods <= train_end)
    validation_mask = available & (periods == validation_start)
    test_mask = available & (periods >= test_start)

    feature_columns = _candidate_columns(features, include_label_derived=include_label_derived)
    X = features[feature_columns].replace([np.inf, -np.inf], np.nan)
    y = effective_labels["label"].astype("int8")
    X_train, y_train = X.loc[train_mask], y.loc[train_mask]
    X_validation, y_validation = X.loc[validation_mask], y.loc[validation_mask]
    if X_train.empty or X_validation.empty:
        raise ValueError("Chronological split produced an empty train or validation set")

    # Fixed holdout: train through train_end and use the next month only for
    # threshold calibration.  The final consecutive test months never alter
    # the estimator, thresholds, or alert policy.
    estimator = _fit_estimator(X_train, y_train, config)
    probability_all = _positive_probability(estimator, X)
    probability_validation = _positive_probability(estimator, X_validation)

    warning_threshold, threshold_diagnostics = _tune_warning_threshold(
        y_validation, probability_validation
    )
    attention_threshold = max(0.0001, warning_threshold * 0.60)
    high_quantile = float(np.nanquantile(probability_validation, 0.90))
    danger_threshold = min(0.98, max(warning_threshold + 0.15, high_quantile))

    bundle = ModelBundle(
        estimator=estimator,
        feature_columns=feature_columns,
        attention_threshold=attention_threshold,
        warning_threshold=warning_threshold,
        danger_threshold=danger_threshold,
        train_end=str(train_end),
        validation_end=str(validation_start),
        test_start=str(test_start),
        test_end=str(test_end),
        feature_policy="with_label_derived" if include_label_derived else "raw_only",
    )
    predictions = pd.DataFrame(index=features.index)
    predictions["risk_probability"] = probability_all
    predictions["split"] = splits
    predictions = predictions.join(effective_labels)
    predictions["attention_threshold"] = attention_threshold
    predictions["warning_threshold"] = warning_threshold
    predictions["danger_threshold"] = danger_threshold

    diagnostics = {
        "test_protocol": "fixed_holdout_no_test_label_reuse",
        "forward_label_boundary_purge": boundary_purge,
        "train_end": str(train_end),
        "validation_end": str(validation_start),
        "test_start": str(test_start),
        "test_end": str(test_end),
        "feature_count": len(feature_columns),
        "train_rows": int(train_mask.sum()),
        "validation_rows": int(validation_mask.sum()),
        "test_rows": int(test_mask.sum()),
        "train_positive_rate": float(y_train.mean()),
        "validation_positive_rate": float(y_validation.mean()),
        "test_positive_rate": float(y.loc[test_mask].mean()) if test_mask.any() else None,
        "attention_threshold": attention_threshold,
        "warning_threshold": warning_threshold,
        "danger_threshold": danger_threshold,
        "feature_policy": "with_label_derived" if include_label_derived else "raw_only",
        "excluded_label_derived_feature_count": int(
            len(_candidate_columns(features, include_label_derived=True)) - len(feature_columns)
        ),
        "threshold_tuning": threshold_diagnostics,
        "walk_forward_folds": [],
    }
    return bundle, predictions, diagnostics
````

</details>
