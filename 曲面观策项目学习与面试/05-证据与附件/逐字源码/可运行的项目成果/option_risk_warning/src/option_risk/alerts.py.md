---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/alerts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/alerts.py>)

SHA-256：`bb7b4631d8f48c68a8318b71fc03b7b5068dc6ed1da3fd8266a1e3a49b1ee1e1`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score

from .config import PipelineConfig
from .decision import (
    DECISION_POLICY_VERSION,
    PRESSURE_SPECS,
    DecisionPolicy,
    apply_decision_policy,
    canonical_policy_diagnostics,
)
from .model import ModelBundle


PRESSURE_LABELS = {
    "pressure__atm_iv": "ATM隐含波动率处于历史高位",
    "pressure__atm_iv_chg_4": "ATM隐含波动率一小时内快速上升",
    "pressure__term_inversion": "近月与远月波动率期限结构倒挂",
    "pressure__convexity_violation_ratio": "执行价方向凸性违反增多",
    "pressure__max_local_iv_jump": "相邻行权价隐含波动率发生局部跳变",
    "pressure__put_call_parity_p95_error": "Put-Call平价偏离扩大",
    "pressure__calendar_variance_violation_ratio": "期限方向总方差一致性违反增多",
    "pressure__gamma_hhi": "Gamma风险集中在少数合约",
    "pressure__vega_hhi": "Vega风险集中在少数合约",
    "pressure__zero_volume_share": "零成交量合约占比上升",
    "pressure__iv_floor_share": "IV求解下限占比上升",
    "pressure__coverage_shortfall": "曲面节点覆盖缺口扩大",
}


def _explain_row(row: pd.Series) -> str:
    candidates: list[tuple[float, str]] = []
    for column, label in PRESSURE_LABELS.items():
        value = row.get(column, np.nan)
        if pd.notna(value):
            candidates.append((float(value), label))
    candidates.sort(reverse=True)
    triggered = [f"{label}（历史阈值倍数{value:.2f}）" for value, label in candidates[:3] if value >= 0.8]
    if not triggered:
        triggered = ["核心动态风险压力较低，未出现稳定的曲面恶化信号"]
    return "；".join(triggered)


def assign_alert_levels(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    bundle: ModelBundle,
    config: PipelineConfig | None = None,
    include_explanations: bool = True,
) -> pd.DataFrame:
    config = config or PipelineConfig()
    result = predictions.join(
        features[
            [
                "product",
                "atm_iv",
                "risk_pressure",
                "data_ready",
                "surface_coverage",
                *PRESSURE_LABELS.keys(),
            ]
        ],
        how="left",
    )
    probability = result["risk_probability"]
    attention_threshold = result.get("attention_threshold", bundle.attention_threshold)
    warning_threshold = result.get("warning_threshold", bundle.warning_threshold)
    danger_threshold = result.get("danger_threshold", bundle.danger_threshold)
    pressure_columns = [column for column in PRESSURE_LABELS if column in result]
    result["independent_pressure_signal_count"] = result[pressure_columns].ge(1.0).sum(axis=1)
    probability_warning = probability.ge(warning_threshold)
    composite_candidate = probability_warning & result[
        "independent_pressure_signal_count"
    ].ge(config.alert_policy_min_signals)
    persistence = max(1, config.alert_policy_persistence_bars)
    persistent_warning = (
        composite_candidate.astype("int8").rolling(persistence, min_periods=persistence).sum()
        >= persistence
    )
    result["alert_level"] = 0
    result.loc[probability.ge(attention_threshold), "alert_level"] = 1
    result.loc[persistent_warning, "alert_level"] = 2
    danger = (
        persistent_warning
        & probability.ge(danger_threshold)
        & result["independent_pressure_signal_count"].ge(
            max(3, config.alert_policy_min_signals + 1)
        )
        & result["risk_pressure"].ge(1.5)
    )
    result.loc[danger, "alert_level"] = 3
    result.loc[~result["data_ready"].fillna(False), "alert_level"] = 0

    # Keep the continuous 0-3 risk state intact and record the operational
    # notification pulse separately so cooldown never falsifies current risk.
    raw_warning = result["alert_level"].ge(2).to_numpy()
    emitted = np.zeros(len(result), dtype=bool)
    last_emitted = -10_000
    for position, active in enumerate(raw_warning):
        if active and position - last_emitted >= config.event_cooldown_bars:
            emitted[position] = True
            last_emitted = position
    result["alert_emitted"] = emitted
    result["alert_name"] = result["alert_level"].map(
        {0: "无预警", 1: "关注", 2: "警告", 3: "危险"}
    )
    if include_explanations:
        result["explanation"] = result.apply(_explain_row, axis=1)
    return result


def _policy_grid(config: PipelineConfig) -> list[PipelineConfig]:
    return [
        replace(
            config,
            alert_policy_min_signals=signals,
            alert_policy_persistence_bars=persistence,
            event_cooldown_bars=cooldown,
        )
        for signals in [1, 2, 3]
        for persistence in [1, 2, 3]
        for cooldown in [4, 6, 8, 10, 12, 16, 24]
    ]


def _tune_policy_for_month(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    bundle: ModelBundle,
    config: PipelineConfig,
    calibration_month: pd.Period,
) -> tuple[PipelineConfig, dict[str, object]]:
    periods = features.index.to_period("M")
    rows: list[tuple[bool, float, float, float, float, PipelineConfig, dict[str, object]]] = []
    for candidate_config in _policy_grid(config):
        candidate = assign_alert_levels(
            features,
            predictions,
            bundle,
            candidate_config,
            include_explanations=False,
        )
        candidate = candidate.copy()
        candidate["split"] = np.where(periods == calibration_month, "calibration", "other")
        metrics = evaluate_alerts(candidate, candidate_config, split="calibration")
        precision = float(metrics.get("event_precision", 0.0))
        recall = float(metrics.get("event_recall", 0.0))
        lead = float(metrics.get("average_lead_minutes") or 0.0)
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        feasible = precision >= 0.50 and recall >= 0.60 and lead >= 30.0
        rows.append((feasible, f1, precision, recall, lead, candidate_config, metrics))
    feasible_rows = [row for row in rows if row[0]]
    selected = max(
        feasible_rows or rows,
        key=lambda row: (row[1], row[2], row[3], -row[5].event_cooldown_bars),
    )
    selected_config = selected[5]
    diagnostics = {
        "calibration_month": str(calibration_month),
        "feasible_target_found": bool(feasible_rows),
        "selected_policy": {
            "minimum_independent_pressure_signals": selected_config.alert_policy_min_signals,
            "persistence_bars": selected_config.alert_policy_persistence_bars,
            "cooldown_bars": selected_config.event_cooldown_bars,
        },
        "calibration_metrics": selected[6],
    }
    return selected_config, diagnostics


def assign_walk_forward_alerts(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    bundle: ModelBundle,
    config: PipelineConfig,
) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Apply one validation-selected comparator policy to the untouched test."""

    validation_month = pd.Period(bundle.validation_end, freq="M")
    validation_policy, validation_diagnostics = _tune_policy_for_month(
        features, predictions, bundle, config, validation_month
    )
    result = assign_alert_levels(features, predictions, bundle, validation_policy)
    diagnostics = [
        {
            "applies_to": "validation_and_fixed_test",
            "test_protocol": "fixed_holdout_no_test_label_reuse",
            **validation_diagnostics,
        }
    ]
    return result, diagnostics


def assign_predictive_rule_alerts(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    config: PipelineConfig,
    lower: float,
    upper: float,
    cooldown: int,
    include_explanations: bool = True,
) -> pd.DataFrame:
    """Apply the same transparent state machine used by the runtime Agent."""

    feature_columns = [
        "product",
        "atm_iv",
        "risk_pressure",
        "core_risk_pressure",
        "data_ready",
        "history_ready",
        "surface_coverage",
        *[column for column in PRESSURE_LABELS if column in features],
    ]
    feature_columns = [column for column in feature_columns if column in features]
    result = predictions.join(
        features[feature_columns],
        how="left",
    )
    policy = DecisionPolicy(
        warning_pressure=float(lower),
        warning_upper_pressure=float(upper),
        cooldown_bars=int(cooldown),
    )
    state = apply_decision_policy(features, policy)
    for column in [
        "decision_score",
        "independent_pressure_signal_count",
        "alert_level",
        "alert_emitted",
        "alert_name",
        "policy_version",
        "policy_parameter_hash",
        "transition_reason",
    ]:
        result[column] = state[column]
    result["decision_source"] = DECISION_POLICY_VERSION
    if include_explanations:
        result["explanation"] = result.apply(_explain_row, axis=1)
    return result


def tune_predictive_rule(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    config: PipelineConfig,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Evaluate the fixed formal policy and retain grid search as sensitivity only."""

    canonical = DecisionPolicy()
    alerts = assign_predictive_rule_alerts(
        features,
        predictions,
        config,
        lower=canonical.warning_pressure,
        upper=canonical.warning_upper_pressure,
        cooldown=canonical.cooldown_bars,
    )
    canonical_metrics = evaluate_alerts(alerts, config, split="validation")

    candidates: list[tuple[bool, float, float, float, int, dict[str, object]]] = []
    for lower in np.arange(0.94, 0.991, 0.005):
        for upper in [1.0, 1.05, np.inf]:
            for cooldown in [4, 6, 8, 10, 12, 16]:
                candidate_alerts = assign_predictive_rule_alerts(
                    features,
                    predictions,
                    config,
                    lower=float(lower),
                    upper=float(upper),
                    cooldown=cooldown,
                    include_explanations=False,
                )
                metrics = evaluate_alerts(candidate_alerts, config, split="validation")
                precision = float(metrics["event_precision"])
                recall = float(metrics["event_recall"])
                lead = float(metrics["average_lead_minutes"] or 0.0)
                f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
                feasible = precision >= 0.50 and recall >= 0.60 and lead >= 30.0
                candidates.append(
                    (feasible, f1, float(lower), float(upper), cooldown, metrics)
                )
    feasible = [row for row in candidates if row[0]]
    selected = max(feasible or candidates, key=lambda row: (row[1], row[5]["event_precision"]))
    diagnostics = {
        **canonical_policy_diagnostics(),
        "feasible_target_found": bool(
            canonical_metrics.get("precision_target_met")
            and canonical_metrics.get("recall_target_met")
            and canonical_metrics.get("lead_target_met")
        ),
        "validation_metrics": canonical_metrics,
        "sensitivity_analysis": {
            "role": "validation-only diagnostic comparator; never selects the formal policy",
            "candidate_count": len(candidates),
            "feasible_candidate_found": bool(feasible),
            "best_candidate": {
                "lower_pressure": selected[2],
                "upper_pressure": selected[3],
                "cooldown_bars": selected[4],
                "validation_metrics": selected[5],
            },
        },
        "interpretation": "A level-2 warning is emitted as core pressure approaches its rolling threshold from below; level 3 is reserved for a new extreme multi-signal state.",
    }
    return alerts, diagnostics


def evaluate_alerts(
    alert_frame: pd.DataFrame, config: PipelineConfig, split: str = "test"
) -> dict[str, object]:
    frame = alert_frame.loc[
        alert_frame["split"].eq(split) & alert_frame["label_available"].fillna(False)
    ].copy()
    if frame.empty:
        return {"split": split, "rows": 0, "warning": "No evaluable rows"}

    predicted = frame["alert_emitted"].fillna(False).astype(bool)
    active_risk_state = frame["alert_level"].ge(2)
    point_precision = precision_score(frame["label"], predicted, zero_division=0)
    point_recall = recall_score(frame["label"], predicted, zero_division=0)

    # The source is a 15-minute bar sequence with night/lunch breaks.  Therefore
    # “2 bars ahead” must be evaluated by sequence position, not wall-clock time;
    # otherwise valid Friday/night-session warnings are incorrectly discarded.
    event_positions = set(np.flatnonzero(frame["event_start"].fillna(False).to_numpy()))
    alert_positions = np.flatnonzero(predicted.to_numpy())
    episode_starts: list[int] = []
    previous: int | None = None
    for position in alert_positions:
        if previous is None or position - previous > 2:
            episode_starts.append(int(position))
        previous = int(position)

    matched_alerts = 0
    immediate_alerts = 0
    for alert_position in episode_starts:
        future_events = [
            event
            for event in event_positions
            if alert_position <= event <= alert_position + config.horizon_bars
        ]
        if future_events:
            matched_alerts += 1
            if min(future_events) - alert_position < config.lead_bars:
                immediate_alerts += 1

    matched_events = 0
    lead_minutes: list[float] = []
    for event_position in sorted(event_positions):
        prior_alerts = [
            alert
            for alert in episode_starts
            if event_position - config.horizon_bars <= alert < event_position
        ]
        if prior_alerts:
            matched_events += 1
            latest_alert = max(prior_alerts)
            lead_minutes.append(float((event_position - latest_alert) * 15))

    event_precision = matched_alerts / len(episode_starts) if episode_starts else 0.0
    event_recall = matched_events / len(event_positions) if event_positions else 0.0
    return {
        "split": split,
        "rows": int(len(frame)),
        "positive_label_rows": int(frame["label"].sum()),
        "alert_rows_level_2_or_3": int(predicted.sum()),
        "alert_emission_rows": int(predicted.sum()),
        "risk_state_rows_level_2_or_3": int(active_risk_state.sum()),
        "point_precision": float(point_precision),
        "point_recall": float(point_recall),
        "event_count": len(event_positions),
        "alert_episode_count": len(episode_starts),
        "matched_events": matched_events,
        "correct_alerts_with_event_in_0_to_8_bars": matched_alerts,
        "correct_alerts_with_less_than_30m_lead": immediate_alerts,
        "event_precision": float(event_precision),
        "event_recall": float(event_recall),
        "average_lead_minutes": float(np.mean(lead_minutes)) if lead_minutes else None,
        "minimum_lead_minutes": float(np.min(lead_minutes)) if lead_minutes else None,
        "precision_target_met": bool(event_precision >= 0.50),
        "recall_target_met": bool(event_recall >= 0.60),
        "lead_target_met": bool(lead_minutes and np.mean(lead_minutes) >= 30.0),
    }
````

</details>
