---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/agent.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/agent.py>)

SHA-256：`ad35f6c5087a2dc9212231dd60c70f358f2dfec705eeef82ea4ce8374a84b773`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import asdict, replace
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

from .catalog import OptionDataCatalog
from .config import AgentConfig
from .contracts import (
    AgentResult,
    EvaluationResult,
    FeatureEvidence,
    KnowledgeGraphResult,
    ProductOption,
    SurfacePayload,
    TriggerReason,
)
from .decision import (
    ALERT_NAMES,
    DECISION_PRESSURE_COLUMNS,
    PRESSURE_SPECS,
    DecisionPolicy,
    _direction as _decision_direction,
    _severity as _decision_severity,
    apply_decision_policy,
    assess_features,
)
from .errors import InvalidTimestampError, SurfaceNotReadyError
from .features import extract_risk_features
from .graph_explanation import UnsafeGraphExplanationError, render_graph_explanation
from .graph_queries import GraphQueryService
from .graph_reasoner import build_graph_result, discover_risk_paths
from .io import read_option_files
from .knowledge_graph import (
    KnowledgeGraphError,
    KnowledgeGraphValidationError,
    build_knowledge_graph,
    graph_from_node_link,
    graph_to_node_link,
)
from .knowledge_schema import (
    FEATURE_RULES,
    KG_RULE_VERSION,
    KG_SCHEMA_VERSION,
    NodeType,
)
from .quality import clean_and_profile
from .surfaces import SURFACE_METRICS, build_surface_nodes, surface_grid


def _graph_cache_identity(policy: DecisionPolicy) -> dict[str, str]:
    """Return the patchable graph identities that materially affect cache trust."""

    return {
        "schema_version": KG_SCHEMA_VERSION,
        "rule_version": KG_RULE_VERSION,
        "decision_policy_parameter_hash": policy.parameter_hash,
    }


_CACHE_JSON_MAX_DEPTH = 64
_TIMELINE_COLUMNS = (
    "atm_iv",
    "risk_score",
    "core_risk_pressure",
    "dynamic_boundary",
    "danger_core_boundary",
    "alert_level",
    "alert_emitted",
    "alert_name",
    "policy_version",
    "policy_parameter_hash",
    "transition_reason",
)
_TRANSITION_AUDIT = {
    "not_ready": (0, False),
    "normal": (0, False),
    "watch_started": (1, False),
    "watch_held": (1, False),
    "watch_released": (0, False),
    "warning_emitted": (2, True),
    "warning_held": (2, False),
    "cooldown_suppressed": (2, False),
    "danger_emitted": (3, True),
    "danger_held": (3, False),
}
_TRANSITION_REASONS = frozenset(_TRANSITION_AUDIT)


def _is_finite_number(value: object) -> bool:
    if isinstance(value, (bool, np.bool_)) or not isinstance(
        value,
        (int, float, np.integer, np.floating),
    ):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError, OverflowError):
        return False


def _is_finite_number_or_none(value: object) -> bool:
    return value is None or _is_finite_number(value)


def _is_strict_json_value(value: object, *, depth: int = 0) -> bool:
    """Accept only bounded, standards-compliant JSON values.

    This deliberately uses exact builtin types.  Cached dictionaries are an
    untrusted persistence boundary; numpy scalars, tuples, sets, timestamps,
    non-string mapping keys and non-finite floats must be regenerated from the
    raw option data instead of silently normalized.
    """

    if depth > _CACHE_JSON_MAX_DEPTH:
        return False
    if value is None or type(value) in {bool, int, str}:
        return True
    if type(value) is float:
        return math.isfinite(value)
    if type(value) is list:
        return all(
            _is_strict_json_value(item, depth=depth + 1) for item in value
        )
    if type(value) is dict:
        return all(
            type(key) is str
            and _is_strict_json_value(item, depth=depth + 1)
            for key, item in value.items()
        )
    return False


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"Non-standard JSON constant is not allowed: {value}")


def _parse_finite_json_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("JSON floating-point value is not finite")
    return number


def _cache_payload_has_expected_shapes(payload: object) -> bool:
    """Preflight nested containers before permissive contract restoration."""

    if type(payload) is not dict or not _is_strict_json_value(payload):
        return False
    if type(payload.get("data_quality")) is not dict:
        return False
    surfaces = payload.get("surfaces")
    evidence = payload.get("feature_evidence")
    reasons = payload.get("trigger_reasons")
    timeline = payload.get("timeline")
    if (
        type(surfaces) is not dict
        or any(type(item) is not dict for item in surfaces.values())
        or type(evidence) is not list
        or any(type(item) is not dict for item in evidence)
        or type(reasons) is not list
        or any(type(item) is not dict for item in reasons)
        or type(timeline) is not list
        or any(type(item) is not dict for item in timeline)
    ):
        return False
    evaluation = payload.get("evaluation")
    if evaluation is not None and type(evaluation) is not dict:
        return False
    if type(evaluation) is dict and type(evaluation.get("metrics")) is not dict:
        return False
    graph = payload.get("knowledge_graph")
    if graph is None:
        return True
    if type(graph) is not dict:
        return False
    mapping_fields = ("graph_json", "query_index")
    sequence_fields = (
        "active_paths",
        "root_evidence",
        "possible_consequences",
        "explanation_sections",
        "missing_evidence",
    )
    return all(type(graph.get(field)) is dict for field in mapping_fields) and all(
        type(graph.get(field)) is list for field in sequence_fields
    )


def _allowed_directions_from_evidence(row: FeatureEvidence) -> frozenset[str]:
    current = row.current_value
    rate = row.change_rate
    if rate is None:
        if current is None or current == 0:
            return frozenset({"持平"})
        # A missing previous value produces "持平"; a zero previous value
        # produces the sign direction but intentionally has no finite rate.
        return frozenset({"持平", "上升" if current > 0 else "下降"})
    if current == 0 and rate == -1:
        return frozenset({"下降"})
    if current == 0 and rate == 1:
        return frozenset({"上升"})

    directions: set[str] = set()
    for denominator, expected_positive in ((1 + rate, True), (1 - rate, False)):
        if denominator == 0:
            continue
        previous = current / denominator if current is not None else None
        if (
            previous is None
            or bool(previous > 0) != expected_positive
            or previous == 0
        ):
            continue
        direction, recovered_rate = _decision_direction(current, previous)
        if recovered_rate is not None and math.isclose(
            recovered_rate,
            rate,
            rel_tol=1e-9,
            abs_tol=1e-12,
        ):
            directions.add(direction)
    if directions:
        return frozenset(directions)
    if rate == 0:
        return frozenset({"持平"})
    return frozenset({"上升" if rate > 0 else "下降"})


def _trigger_reasons_are_canonical(
    result: AgentResult,
    policy: DecisionPolicy,
) -> bool:
    ranked: list[tuple[float, int, FeatureEvidence]] = []
    for position, row in enumerate(result.feature_evidence):
        pressure = row.pressure_ratio
        if pressure is None or pressure < policy.attention_pressure:
            continue
        ranked.append((pressure, position, row))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    if ranked:
        expected_rows = [row for _, _, row in ranked[:3]]
        if len(result.trigger_reasons) != len(expected_rows):
            return False
        for reason, row in zip(result.trigger_reasons, expected_rows, strict=True):
            direction = reason.change_direction
            pressure = row.pressure_ratio
            assert pressure is not None
            expected_message = (
                f"{row.label}当前值{row.current_value:.6g}，"
                f"动态阈值{row.reference_value:.6g}，"
                f"历史阈值倍数{pressure:.3f}，较上一时点{direction}"
                if row.current_value is not None and row.reference_value is not None
                else f"{row.label}历史阈值倍数{pressure:.3f}，状态{direction}"
            )
            if (
                reason.feature_name != row.feature_name
                or reason.label != row.label
                or reason.current_value != row.current_value
                or reason.reference_value != row.reference_value
                or reason.pressure_ratio != pressure
                or direction not in _allowed_directions_from_evidence(row)
                or reason.severity != _decision_severity(pressure, policy)
                or reason.message != expected_message
            ):
                return False
        return True

    if result.timeline.empty:
        return False
    core = result.timeline.iloc[-1].get("core_risk_pressure")
    if not _is_finite_number(core):
        return False
    previous_core: float | None = None
    if len(result.timeline) > 1:
        previous = result.timeline.iloc[-2].get("core_risk_pressure")
        if _is_finite_number(previous):
            previous_core = float(previous)
    current_core = float(core)
    direction = _decision_direction(current_core, previous_core)[0]
    expected = [
        TriggerReason(
            feature_name="core_risk_pressure",
            label="综合核心风险压力",
            current_value=current_core,
            reference_value=1.0,
            pressure_ratio=current_core,
            change_direction=direction,
            severity=0,
            message=(
                f"综合核心风险压力{current_core:.3f}，"
                f"未达到关注阈值{policy.attention_pressure:.2f}"
            ),
        )
    ]
    return result.trigger_reasons == expected


def _is_valid_analytical_timeline_value(value: object) -> bool:
    if value is None or value is pd.NA:
        return True
    if isinstance(value, (bool, np.bool_)):
        return False
    if not isinstance(value, (int, float, np.integer, np.floating)):
        return False
    try:
        return not math.isinf(float(value))
    except (TypeError, ValueError, OverflowError):
        return False


def _current_cross_layer_facts_are_valid(
    timeline: pd.DataFrame,
    result: AgentResult,
    policy: DecisionPolicy,
) -> bool:
    if result.price_source != "reconstructed_proxy":
        return False
    evidence = {row.feature_name: row for row in result.feature_evidence}
    if set(evidence) != {rule.feature_name for rule in FEATURE_RULES}:
        return False
    finite_pressures = [
        float(row.pressure_ratio)
        for row in result.feature_evidence
        if _is_finite_number(row.pressure_ratio)
    ]
    core_pressures = [
        float(evidence[name].pressure_ratio)
        for name in ("atm_iv", "convexity_violation_ratio")
        if _is_finite_number(evidence[name].pressure_ratio)
    ]
    atm_value = evidence["atm_iv"].current_value
    if not finite_pressures or not core_pressures or not _is_finite_number(atm_value):
        return False
    latest = timeline.iloc[-1]
    expected_risk = max(finite_pressures)
    expected_core = max(core_pressures)
    danger_signal_count = sum(
        1
        for pressure_column in DECISION_PRESSURE_COLUMNS
        if _is_finite_number(
            evidence[PRESSURE_SPECS[pressure_column][1]].pressure_ratio
        )
        and float(evidence[PRESSURE_SPECS[pressure_column][1]].pressure_ratio)
        >= policy.danger_pressure
    )
    expected_danger = (
        expected_core >= policy.danger_core_pressure
        and danger_signal_count >= policy.multi_signal_count
    )
    return (
        float(result.risk_score) == expected_risk
        and _is_finite_number(latest["atm_iv"])
        and float(latest["atm_iv"]) == float(atm_value)
        and _is_finite_number(latest["risk_score"])
        and float(latest["risk_score"]) == expected_risk
        and _is_finite_number(latest["core_risk_pressure"])
        and float(latest["core_risk_pressure"]) == expected_core
        and (int(latest["alert_level"]) == 3) == expected_danger
    )


def _timeline_transition_sequence_is_valid(
    timeline: pd.DataFrame,
    policy: DecisionPolicy,
) -> bool:
    active_since: int | None = None
    active_since_is_before_window = False
    last_warning: int | None = None
    previous_level: int | None = None
    previous_reason: str | None = None

    for position, row in enumerate(timeline.itertuples(index=False)):
        reason = str(row.transition_reason)
        level = int(row.alert_level)
        score = float(row.risk_score) if _is_finite_number(row.risk_score) else None
        core = (
            float(row.core_risk_pressure)
            if _is_finite_number(row.core_risk_pressure)
            else None
        )
        if reason == "not_ready":
            if position == len(timeline) - 1:
                return False
            active_since = None
            active_since_is_before_window = False
            last_warning = None
            previous_level = 0
            previous_reason = reason
            continue
        if score is None or core is None:
            return False

        if reason in {"normal", "watch_started", "watch_held", "watch_released"}:
            if core >= policy.warning_pressure:
                return False
        elif reason == "warning_emitted":
            if core < policy.warning_pressure:
                return False
            if previous_level is not None and previous_level >= 2:
                if core >= policy.warning_upper_pressure:
                    return False
                if (
                    last_warning is not None
                    and position - last_warning < policy.cooldown_bars
                ):
                    return False
        elif reason == "warning_held":
            if core < policy.warning_upper_pressure:
                return False
            if previous_level is not None and previous_level < 2:
                return False
        elif reason == "cooldown_suppressed":
            if not (
                policy.warning_pressure
                <= core
                < policy.warning_upper_pressure
            ):
                return False
            if previous_level is not None and previous_level < 2:
                return False
            if last_warning is None:
                if position >= policy.cooldown_bars:
                    return False
            elif position - last_warning >= policy.cooldown_bars:
                return False
        elif reason == "danger_emitted":
            if core < policy.danger_core_pressure:
                return False
            if previous_reason in {"danger_emitted", "danger_held"}:
                return False
        elif reason == "danger_held":
            if core < policy.danger_core_pressure:
                return False
            if previous_reason is not None and previous_reason not in {
                "danger_emitted",
                "danger_held",
            }:
                return False

        if reason == "normal":
            if score >= policy.attention_pressure:
                return False
            if previous_level is not None and previous_level > 0:
                return False
            active_since = None
            active_since_is_before_window = False
        elif reason == "watch_started":
            if score < policy.attention_pressure:
                return False
            if previous_level is not None and previous_level > 0:
                return False
            active_since = position
            active_since_is_before_window = False
        elif reason in {"warning_emitted", "danger_emitted"}:
            active_since = position
            active_since_is_before_window = False
            last_warning = position
        elif reason in {"warning_held", "cooldown_suppressed", "danger_held"}:
            if active_since is None:
                if position == 0:
                    active_since_is_before_window = True
                else:
                    active_since = 0
        elif reason in {"watch_held", "watch_released"}:
            if reason == "watch_released" and position == 0:
                if score >= policy.attention_pressure:
                    return False
                active_since = None
                active_since_is_before_window = False
                previous_level = level
                previous_reason = reason
                continue
            if previous_level is not None and previous_level == 0:
                return False
            if active_since is None:
                if position == 0:
                    active_since_is_before_window = True
                elif not active_since_is_before_window:
                    active_since = 0
            duration = (
                None if active_since_is_before_window else position - int(active_since)
            )
            release_due = (
                duration is not None
                and duration >= policy.persistence_bars
                and score <= policy.attention_release_pressure
            ) or (
                duration is not None
                and duration >= policy.max_watch_bars
                and score < policy.attention_pressure
            )
            if reason == "watch_held" and release_due:
                return False
            if reason == "watch_released":
                if score >= policy.attention_pressure or (
                    duration is not None and not release_due
                ):
                    return False
                active_since = None
                active_since_is_before_window = False

        previous_level = level
        previous_reason = reason
    return True


def _timeline_replay_matches(
    timeline: pd.DataFrame,
    result: AgentResult,
    policy: DecisionPolicy,
) -> bool:
    features = pd.DataFrame(index=timeline.index)
    features["core_risk_pressure"] = pd.to_numeric(
        timeline["core_risk_pressure"],
        errors="coerce",
    )
    features["risk_pressure"] = pd.to_numeric(
        timeline["risk_score"],
        errors="coerce",
    )
    recorded_reasons = timeline["transition_reason"]
    finite_state = features["core_risk_pressure"].notna() & features[
        "risk_pressure"
    ].notna()
    inferred_ready = recorded_reasons.ne("not_ready") & finite_state
    features["data_ready"] = inferred_ready
    features["history_ready"] = inferred_ready
    for column in DECISION_PRESSURE_COLUMNS:
        features[column] = 0.0

    historical_danger = timeline["alert_level"].eq(3) & inferred_ready
    danger_columns = list(DECISION_PRESSURE_COLUMNS[: policy.multi_signal_count])
    features.loc[historical_danger, danger_columns] = policy.danger_pressure

    evidence = {row.feature_name: row for row in result.feature_evidence}
    latest_timestamp = timeline.index[-1]
    for pressure_column in DECISION_PRESSURE_COLUMNS:
        feature_name = PRESSURE_SPECS[pressure_column][1]
        pressure = evidence[feature_name].pressure_ratio
        features.loc[latest_timestamp, pressure_column] = (
            float(pressure) if _is_finite_number(pressure) else np.nan
        )
    features.loc[latest_timestamp, ["data_ready", "history_ready"]] = True

    features = features.reset_index(drop=True)
    expected_levels = timeline["alert_level"].astype(int).tolist()
    expected_pulses = timeline["alert_emitted"].astype(bool).tolist()
    expected_reasons = timeline["transition_reason"].astype(str).tolist()

    def seed_row(core: float, risk: float, *, danger: bool = False) -> dict[str, object]:
        row: dict[str, object] = {
            "core_risk_pressure": core,
            "risk_pressure": risk,
            "data_ready": True,
            "history_ready": True,
        }
        row.update({column: 0.0 for column in DECISION_PRESSURE_COLUMNS})
        if danger:
            for pressure_column in DECISION_PRESSURE_COLUMNS[: policy.multi_signal_count]:
                row[pressure_column] = policy.danger_pressure
        return row

    max_seed_age = max(
        1,
        policy.cooldown_bars,
        policy.persistence_bars,
        policy.max_watch_bars,
    )
    seed_prefixes = [pd.DataFrame(columns=features.columns)]
    for age in range(1, max_seed_age + 1):
        watch_rows = [
            seed_row(0.0, policy.attention_pressure) for _ in range(age)
        ]
        warning_rows = [seed_row(policy.warning_pressure, policy.warning_pressure)]
        warning_rows.extend(
            seed_row(policy.warning_upper_pressure, policy.warning_upper_pressure)
            for _ in range(age - 1)
        )
        danger_rows = [
            seed_row(
                policy.danger_core_pressure,
                policy.danger_core_pressure,
                danger=True,
            )
            for _ in range(age)
        ]
        for rows in (watch_rows, warning_rows, danger_rows):
            prefix = pd.DataFrame(rows, columns=features.columns)
            prefix.index = pd.RangeIndex(-len(prefix), 0)
            seed_prefixes.append(prefix)

    for prefix in seed_prefixes:
        candidate = pd.concat([prefix, features], axis=0)
        replayed = apply_decision_policy(candidate, policy).iloc[len(prefix) :]
        if (
            replayed["alert_level"].astype(int).tolist() == expected_levels
            and replayed["alert_emitted"].astype(bool).tolist() == expected_pulses
            and replayed["transition_reason"].astype(str).tolist() == expected_reasons
        ):
            return True
    return False


def _timeline_is_current(
    timeline: object,
    result: AgentResult,
    *,
    timestamp: pd.Timestamp,
    policy: DecisionPolicy,
) -> bool:
    if (
        not isinstance(timeline, pd.DataFrame)
        or timeline.empty
        or tuple(timeline.columns) != _TIMELINE_COLUMNS
        or not isinstance(timeline.index, pd.DatetimeIndex)
        or timeline.index.has_duplicates
        or timeline.index.hasnans
        or not timeline.index.is_monotonic_increasing
        or timeline.index.max() != timestamp
    ):
        return False
    for column in ("atm_iv", "risk_score", "core_risk_pressure"):
        if not all(
            _is_valid_analytical_timeline_value(value)
            for value in timeline[column].tolist()
        ):
            return False
    for value in timeline["dynamic_boundary"].tolist():
        if not _is_finite_number(value) or float(value) != policy.warning_pressure:
            return False
    for value in timeline["danger_core_boundary"].tolist():
        if not _is_finite_number(value) or float(value) != policy.danger_core_pressure:
            return False
    levels = timeline["alert_level"].tolist()
    emitted = timeline["alert_emitted"].tolist()
    names = timeline["alert_name"].tolist()
    transitions = timeline["transition_reason"].tolist()
    for level, pulse, name, transition in zip(
        levels,
        emitted,
        names,
        transitions,
        strict=True,
    ):
        if (
            isinstance(level, (bool, np.bool_))
            or not isinstance(level, (int, np.integer))
            or int(level) not in ALERT_NAMES
            or not isinstance(pulse, (bool, np.bool_))
            or name != ALERT_NAMES[int(level)]
            or type(transition) is not str
            or transition not in _TRANSITION_REASONS
            or (int(level), bool(pulse)) != _TRANSITION_AUDIT[transition]
        ):
            return False
    if (
        not timeline["policy_version"].eq(policy.policy_version).all()
        or not timeline["policy_parameter_hash"].eq(policy.parameter_hash).all()
    ):
        return False
    latest = timeline.iloc[-1]
    latest_atm_iv = latest["atm_iv"]
    latest_score = latest["risk_score"]
    latest_core = latest["core_risk_pressure"]
    return (
        _is_finite_number(latest_atm_iv)
        and _is_finite_number(latest_score)
        and _is_finite_number(latest_core)
        and float(latest_score) == float(result.risk_score)
        and int(latest["alert_level"]) == result.alert_level
        and bool(latest["alert_emitted"]) is result.alert_emitted
        and latest["alert_name"] == result.alert_name
        and latest["transition_reason"] == result.transition_reason
        and _current_cross_layer_facts_are_valid(timeline, result, policy)
        and _timeline_transition_sequence_is_valid(timeline, policy)
        and _timeline_replay_matches(timeline, result, policy)
    )


class OptionRiskAgent:
    """The sole public business Agent for competition problems 1 and 2."""

    RESULT_CACHE_VERSION = "result-v9-total-variance-surface"

    def __init__(self, config: AgentConfig):
        self.config = config
        self.config.ensure_directories()
        self.catalog = OptionDataCatalog(config)

    def list_products(self) -> list[ProductOption]:
        return self.catalog.list_products()

    def list_timestamps(self, product: str) -> pd.DatetimeIndex:
        return self.catalog.list_timestamps(product)

    def _validate_timestamp(self, product: str, timestamp: pd.Timestamp) -> None:
        available = self.list_timestamps(product)
        if timestamp not in available:
            raise InvalidTimestampError(f"时间点 {timestamp} 不属于品种 {product} 的有效选项")

    def _result_cache_path(
        self,
        product: str,
        timestamp: pd.Timestamp,
        policy: DecisionPolicy | None = None,
    ) -> Path:
        policy = policy or self._decision_policy(product)
        signature = {
            "source_fingerprint": self.catalog.source_fingerprint,
            "product": product,
            "timestamp": timestamp.isoformat(),
            "agent_config_version": self.config.config_version,
            "lookback_calendar_days": self.config.lookback_calendar_days,
            "pipeline_config": self.config.pipeline_config(product).to_dict(),
            "decision_policy": asdict(policy),
            "decision_policy_parameter_hash": policy.parameter_hash,
            "knowledge_graph": _graph_cache_identity(policy),
            "result_cache_version": self.RESULT_CACHE_VERSION,
        }
        key = json.dumps(signature, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
        path = self.config.cache_dir / "results" / self.catalog.source_fingerprint / product
        path.mkdir(parents=True, exist_ok=True)
        return path / f"{timestamp:%Y%m%dT%H%M%S}_{digest}.json.gz"

    @staticmethod
    def _timeline(features: pd.DataFrame, timestamp: pd.Timestamp, policy: DecisionPolicy) -> pd.DataFrame:
        full_view = features.loc[features.index <= timestamp].copy()
        full_state = apply_decision_policy(full_view, policy, timestamp=timestamp)
        view = full_view.tail(512)
        state = full_state.loc[view.index]
        timeline = pd.DataFrame(
            {
                "atm_iv": view.get("atm_iv"),
                "risk_score": state["decision_score"],
                "core_risk_pressure": view.get("core_risk_pressure"),
                "dynamic_boundary": policy.warning_pressure,
                "danger_core_boundary": policy.danger_core_pressure,
                "alert_level": state["alert_level"],
                "alert_emitted": state["alert_emitted"],
                "alert_name": state["alert_name"],
                "policy_version": state["policy_version"],
                "policy_parameter_hash": state["policy_parameter_hash"],
                "transition_reason": state["transition_reason"],
            },
            index=view.index,
        )
        timeline.index.name = "datetime"
        return timeline

    def _summary_payload(self, product: str) -> dict[str, object] | None:
        assert self.config.output_dir is not None
        candidates = [
            self.config.output_dir / product / "run_summary.json",
            self.config.output_dir / "run_summary.json",
        ]
        candidates.extend(sorted(self.config.output_dir.rglob("run_summary.json")))
        candidates = list(dict.fromkeys(candidates))
        for path in candidates:
            if not path.exists():
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            configured_product = str(payload.get("config", {}).get("product", "")).lower()
            if configured_product and configured_product != product:
                continue
            return payload
        return None

    def _decision_policy(self, product: str) -> DecisionPolicy:
        """Return the label-independent policy registered in application code."""

        del product
        return DecisionPolicy()

    def _load_evaluation(self, product: str) -> EvaluationResult | None:
        payload = self._summary_payload(product)
        if payload is not None:
            metrics = {
                "split": payload.get("split"),
                "config": payload.get("config"),
                "model": payload.get("model"),
                "artifact_identity": payload.get("run_identity")
                or payload.get("artifact_identity"),
                "test_metrics": payload.get("test_metrics"),
                "validation_metrics": payload.get("validation_metrics"),
                "cvar_backtest": payload.get("cvar_backtest"),
                "official_event_comparison": payload.get("official_event_comparison"),
                "primary_warning_policy": payload.get("primary_warning_policy"),
            }
            return EvaluationResult(available=True, status="ready", metrics=metrics)
        return None

    def get_evaluation(self, product: str) -> EvaluationResult:
        normalized = product.lower().strip()
        self.catalog._validate_product(normalized)
        evaluation = self._load_evaluation(normalized)
        if evaluation is None:
            return EvaluationResult(
                available=False,
                status="该品种尚未生成连续三个月离线回测",
                metrics={},
            )
        return evaluation

    @staticmethod
    def _missing_graph_evidence(graph) -> tuple[str, ...]:
        available: set[str] = set()
        for _, data in graph.nodes(data=True):
            if data.get("node_type") != NodeType.EVIDENCE.value:
                continue
            current = data.get("current_value")
            if (
                isinstance(current, (int, float, np.integer, np.floating))
                and not isinstance(current, (bool, np.bool_))
                and math.isfinite(float(current))
            ):
                available.add(str(data.get("feature_name")))
        return tuple(
            rule.feature_name
            for rule in FEATURE_RULES
            if rule.feature_name not in available
        )

    def _build_knowledge_graph_result(
        self,
        base_result: AgentResult,
        policy: DecisionPolicy,
    ) -> KnowledgeGraphResult:
        """Build and validate Problem 2 from the already-final Problem 1 result."""

        try:
            graph = self._graph_from_problem_one(base_result, policy)
            paths = discover_risk_paths(graph)
            sections, explanation_text, confidence = render_graph_explanation(
                graph,
                paths,
            )
            missing_evidence = self._missing_graph_evidence(graph)
            graph_result = build_graph_result(
                graph,
                missing_evidence=missing_evidence,
                explanation_sections=sections,
                explanation_text=explanation_text,
                explanation_confidence=confidence,
            )
            graph_result = replace(
                graph_result,
                missing_evidence=missing_evidence,
            )
            GraphQueryService(graph_result)
            return graph_result
        except (KnowledgeGraphError, UnsafeGraphExplanationError) as error:
            return KnowledgeGraphResult.unavailable(
                product=base_result.product,
                timestamp=base_result.timestamp,
                schema_version=KG_SCHEMA_VERSION,
                rule_version=KG_RULE_VERSION,
                error_type=type(error).__name__,
                error_message=str(error),
            )

    @staticmethod
    def _graph_from_problem_one(
        base_result: AgentResult,
        policy: DecisionPolicy,
    ):
        return build_knowledge_graph(
            product=base_result.product,
            timestamp=base_result.timestamp,
            evidence=base_result.feature_evidence,
            alert_level=base_result.alert_level,
            alert_name=base_result.alert_name,
            risk_score=base_result.risk_score,
            alert_emitted=base_result.alert_emitted,
            transition_reason=base_result.transition_reason,
            policy_version=base_result.policy_version,
            policy_parameter_hash=base_result.policy_parameter_hash,
            data_quality=base_result.data_quality,
            price_source=base_result.price_source,
            policy=policy,
        )

    def _attach_knowledge_graph(
        self,
        base_result: AgentResult,
        policy: DecisionPolicy,
    ) -> AgentResult:
        graph_result = self._build_knowledge_graph_result(base_result, policy)
        return replace(base_result, knowledge_graph=graph_result)

    @staticmethod
    def _is_current_problem_one_cache(
        result: object,
        *,
        product: str,
        timestamp: pd.Timestamp,
        policy: DecisionPolicy,
    ) -> bool:
        if not isinstance(result, AgentResult):
            return False
        if (
            result.product != product
            or result.timestamp != timestamp
            or result.status != "ready"
            or result.policy_version != policy.policy_version
            or result.policy_parameter_hash != policy.parameter_hash
        ):
            return False
        if type(result.alert_level) is not int or result.alert_level not in ALERT_NAMES:
            return False
        if result.alert_name != ALERT_NAMES[result.alert_level]:
            return False
        if type(result.alert_emitted) is not bool:
            return False
        if not _is_finite_number(result.risk_score):
            return False
        if type(result.price_source) is not str or not result.price_source:
            return False
        if type(result.data_quality) is not dict or not _is_strict_json_value(
            result.data_quality
        ):
            return False
        if type(result.feature_evidence) is not list or len(
            result.feature_evidence
        ) != len(FEATURE_RULES):
            return False
        for row, rule in zip(result.feature_evidence, FEATURE_RULES, strict=True):
            if (
                not isinstance(row, FeatureEvidence)
                or row.feature_name != rule.feature_name
                or row.group != rule.evidence_group
                or row.label != rule.label
            ):
                return False
            for value in (
                row.current_value,
                row.reference_value,
                row.pressure_ratio,
                row.change_rate,
            ):
                if not _is_finite_number_or_none(value):
                    return False
            if row.status != ALERT_NAMES[
                _decision_severity(row.pressure_ratio, policy)
            ]:
                return False
        if type(result.surfaces) is not dict or set(result.surfaces) != set(
            SURFACE_METRICS
        ):
            return False
        for metric, surface in result.surfaces.items():
            if (
                not isinstance(surface, SurfacePayload)
                or surface.timestamp != timestamp
                or surface.metric != metric
                or not isinstance(surface.log_moneyness, np.ndarray)
                or surface.log_moneyness.ndim != 1
                or surface.log_moneyness.size == 0
                or surface.log_moneyness.dtype.kind not in "fiu"
                or not isinstance(surface.time_to_expiry, np.ndarray)
                or surface.time_to_expiry.ndim != 1
                or surface.time_to_expiry.size == 0
                or surface.time_to_expiry.dtype.kind not in "fiu"
                or not isinstance(surface.values, np.ndarray)
                or surface.values.dtype.kind not in "fiu"
                or surface.values.shape
                != (len(surface.time_to_expiry), len(surface.log_moneyness))
            ):
                return False
            try:
                log_moneyness = surface.log_moneyness.astype(float, copy=False)
                time_to_expiry = surface.time_to_expiry.astype(float, copy=False)
                values = surface.values.astype(float, copy=False)
            except (TypeError, ValueError, OverflowError):
                return False
            if (
                not np.isfinite(log_moneyness).all()
                or not np.isfinite(time_to_expiry).all()
                or not (np.diff(log_moneyness) > 0).all()
                or not (np.diff(time_to_expiry) > 0).all()
                or not (time_to_expiry > 0).all()
                or np.isinf(values).any()
            ):
                return False
        if (
            type(result.transition_reason) is not str
            or result.transition_reason not in _TRANSITION_REASONS
            or not _timeline_is_current(
                result.timeline,
                result,
                timestamp=timestamp,
                policy=policy,
            )
        ):
            return False
        if type(result.trigger_reasons) is not list or not result.trigger_reasons:
            return False
        for reason in result.trigger_reasons:
            if (
                not isinstance(reason, TriggerReason)
                or type(reason.feature_name) is not str
                or type(reason.label) is not str
                or type(reason.change_direction) is not str
                or reason.change_direction not in {"上升", "下降", "持平"}
                or type(reason.severity) is not int
                or reason.severity not in ALERT_NAMES
                or type(reason.message) is not str
                or not reason.message
                or not _is_finite_number_or_none(reason.current_value)
                or not _is_finite_number_or_none(reason.reference_value)
                or not _is_finite_number_or_none(reason.pressure_ratio)
            ):
                return False
        if not _trigger_reasons_are_canonical(result, policy):
            return False
        return True

    def _validate_ready_graph_cache(
        self,
        result: AgentResult,
        policy: DecisionPolicy,
        *,
        compare_problem_one: bool = True,
    ) -> None:
        graph_result = result.knowledge_graph
        if graph_result is None or graph_result.status != "ready":
            raise KnowledgeGraphValidationError("Cached graph is not ready")
        if (
            graph_result.schema_version != KG_SCHEMA_VERSION
            or graph_result.rule_version != KG_RULE_VERSION
            or graph_result.product != result.product
            or graph_result.timestamp != result.timestamp
            or graph_result.error_type is not None
            or graph_result.error_message is not None
        ):
            raise KnowledgeGraphValidationError(
                "Cached graph outer event or version identity mismatch"
            )
        GraphQueryService(graph_result)
        graph = graph_from_node_link(graph_result.graph_json)
        if (
            graph.graph.get("policy_parameter_hash") != policy.parameter_hash
            or graph.graph.get("policy_parameters") != asdict(policy)
        ):
            raise KnowledgeGraphValidationError(
                "Cached graph decision policy identity mismatch"
            )
        if compare_problem_one:
            canonical_graph = self._graph_from_problem_one(result, policy)
            if graph_to_node_link(graph) != graph_to_node_link(canonical_graph):
                raise KnowledgeGraphValidationError(
                    "Cached graph does not match its current Problem 1 base"
                )
        paths = discover_risk_paths(graph)
        sections, explanation_text, confidence = render_graph_explanation(graph, paths)
        if (
            graph_result.explanation_sections != tuple(sections)
            or graph_result.explanation_text != explanation_text
            or graph_result.explanation_confidence != confidence
        ):
            raise KnowledgeGraphValidationError(
                "Cached graph explanation is not the fresh canonical rendering"
            )
        if graph_result.missing_evidence != self._missing_graph_evidence(graph):
            raise KnowledgeGraphValidationError(
                "Cached graph missing-evidence index is not canonical"
            )

    def _validate_publishable_result(
        self,
        result: AgentResult,
        *,
        product: str,
        timestamp: pd.Timestamp,
        policy: DecisionPolicy,
        compare_ready_to_problem_one: bool = True,
    ) -> None:
        if not self._is_current_problem_one_cache(
            result,
            product=product,
            timestamp=timestamp,
            policy=policy,
        ):
            raise ValueError("Published result does not contain the current Problem 1 identity")
        graph_result = result.knowledge_graph
        if graph_result is None:
            raise ValueError("Published current result must include a graph outcome")
        if graph_result.status == "ready":
            self._validate_ready_graph_cache(
                result,
                policy,
                compare_problem_one=compare_ready_to_problem_one,
            )
            return
        if (
            graph_result.status != "unavailable"
            or graph_result.schema_version != KG_SCHEMA_VERSION
            or graph_result.rule_version != KG_RULE_VERSION
            or graph_result.product != product
            or graph_result.timestamp != timestamp
            or not isinstance(graph_result.error_type, str)
            or not graph_result.error_type
            or not isinstance(graph_result.error_message, str)
        ):
            raise ValueError("Published unavailable graph outcome is malformed")

    @staticmethod
    def _load_cached_result(cache_path: Path) -> AgentResult | None:
        try:
            with gzip.open(cache_path, "rt", encoding="utf-8") as handle:
                payload = json.load(
                    handle,
                    parse_constant=_reject_json_constant,
                    parse_float=_parse_finite_json_float,
                )
            if not _cache_payload_has_expected_shapes(payload):
                return None
            return AgentResult.from_dict(payload)
        except (
            OSError,
            EOFError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
            AttributeError,
            OverflowError,
            RecursionError,
        ):
            return None

    def _publish_result(
        self,
        cache_path: Path,
        result: AgentResult,
        *,
        product: str,
        timestamp: pd.Timestamp,
        policy: DecisionPolicy,
    ) -> AgentResult:
        self._validate_publishable_result(
            result,
            product=product,
            timestamp=timestamp,
            policy=policy,
            compare_ready_to_problem_one=False,
        )
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{cache_path.name}-",
            suffix=".tmp",
            dir=cache_path.parent,
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            with gzip.open(temporary, "wt", encoding="utf-8") as handle:
                json.dump(result.to_dict(), handle, ensure_ascii=False, allow_nan=False)
            try:
                os.replace(temporary, cache_path)
            except PermissionError:
                published = self._load_cached_result(cache_path)
                if published is None:
                    raise
                self._validate_publishable_result(
                    published,
                    product=product,
                    timestamp=timestamp,
                    policy=policy,
                )
                return replace(
                    published,
                    evaluation=self._load_evaluation(product),
                )
        finally:
            temporary.unlink(missing_ok=True)
        return result

    def analyze(self, product: str, timestamp: pd.Timestamp | str) -> AgentResult:
        product = product.lower().strip()
        timestamp = pd.Timestamp(timestamp)
        self._validate_timestamp(product, timestamp)
        policy = self._decision_policy(product)
        cache_path = self._result_cache_path(product, timestamp, policy)
        if cache_path.exists():
            cached = self._load_cached_result(cache_path)
            if self._is_current_problem_one_cache(
                cached,
                product=product,
                timestamp=timestamp,
                policy=policy,
            ):
                # Offline evaluation can be generated after a point-in-time result
                # has already been cached. Keep the expensive surfaces/features in
                # cache while refreshing this lightweight, deployment-owned view.
                assert cached is not None
                refreshed = replace(cached, evaluation=self._load_evaluation(product))
                if cached.knowledge_graph is not None and cached.knowledge_graph.status == "ready":
                    try:
                        self._validate_ready_graph_cache(cached, policy)
                    except (KnowledgeGraphError, UnsafeGraphExplanationError):
                        pass
                    else:
                        return refreshed
                upgraded = self._attach_knowledge_graph(refreshed, policy)
                return self._publish_result(
                    cache_path,
                    upgraded,
                    product=product,
                    timestamp=timestamp,
                    policy=policy,
                )

        start = timestamp - pd.Timedelta(days=self.config.lookback_calendar_days)
        files = self.catalog.product_files(product, start=start, end=timestamp)
        pipeline_config = self.config.pipeline_config(
            product,
            start_date=str(start.date()),
            end_date=str(timestamp.date()),
        )
        raw, ingest_profile = read_option_files(
            files,
            product=product,
            start_date=pipeline_config.start_date,
            end_date=pipeline_config.end_date,
        )
        raw = raw.loc[raw["datetime"].le(timestamp)].copy()
        cleaned, quality_profile = clean_and_profile(raw, pipeline_config, ingest_profile)
        nodes = build_surface_nodes(cleaned)
        if timestamp not in set(nodes["datetime"]):
            raise SurfaceNotReadyError(f"时间点 {timestamp} 清洗后无法构建曲面")
        features = extract_risk_features(cleaned, nodes, pipeline_config)
        decision = assess_features(features, timestamp, policy, pipeline_config)

        surfaces: dict[str, SurfacePayload] = {}
        for metric in SURFACE_METRICS:
            grid = surface_grid(nodes, metric, timestamp=timestamp)
            if metric == "iv" and grid.fit_diagnostics is not None:
                quality_profile = dict(quality_profile)
                quality_profile["iv_surface_fit"] = grid.fit_diagnostics
            surfaces[metric] = SurfacePayload(
                metric=metric,
                timestamp=timestamp,
                log_moneyness=grid.log_moneyness,
                time_to_expiry=grid.dte / 365.0,
                values=grid.values,
            )

        result = AgentResult(
            product=product,
            timestamp=timestamp,
            status="ready",
            alert_level=decision.alert_level,
            alert_name=decision.alert_name,
            alert_emitted=decision.alert_emitted,
            risk_score=decision.risk_score,
            price_source="reconstructed_proxy",
            data_quality=quality_profile,
            surfaces=surfaces,
            feature_evidence=decision.feature_evidence,
            trigger_reasons=decision.trigger_reasons,
            timeline=self._timeline(features, timestamp, policy),
            evaluation=self._load_evaluation(product),
            policy_version=decision.policy_version,
            policy_parameter_hash=decision.policy_parameter_hash,
            transition_reason=decision.transition_reason,
        )
        result = self._attach_knowledge_graph(result, policy)
        return self._publish_result(
            cache_path,
            result,
            product=product,
            timestamp=timestamp,
            policy=policy,
        )
````

</details>
