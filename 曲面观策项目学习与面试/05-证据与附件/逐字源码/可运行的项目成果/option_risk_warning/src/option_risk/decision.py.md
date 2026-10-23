---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/decision.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/decision.py>)

SHA-256：`180caf76feffaa3c6c1c91556c116109912b85dd9aa4db01310c61d2fffc635d`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

import numpy as np
import pandas as pd

from .config import PipelineConfig
from .contracts import FeatureEvidence, TriggerReason, _json_ready
from .errors import InsufficientHistoryError, InvalidTimestampError, SurfaceNotReadyError


ALERT_NAMES = {0: "无预警", 1: "关注", 2: "警告", 3: "危险"}
DECISION_POLICY_VERSION = "validated-dynamic-state-v2"
PRIMARY_POLICY_SELECTION_DATA = "pre-registered fixed canonical policy"

PRESSURE_SPECS = {
    "pressure__atm_iv": ("曲面水平与形态", "atm_iv", "ATM隐含波动率"),
    "pressure__atm_iv_chg_4": ("曲面水平与形态", "atm_iv_chg_4", "ATM隐含波动率一小时变化"),
    "pressure__term_inversion": ("期限结构", "term_inversion", "期限结构倒挂程度"),
    "pressure__convexity_violation_ratio": (
        "无套利风险",
        "convexity_violation_ratio",
        "曲面凸性违反率",
    ),
    "pressure__max_local_iv_jump": ("曲面水平与形态", "max_local_iv_jump", "局部IV跳变"),
    "pressure__put_call_parity_p95_error": (
        "无套利风险",
        "put_call_parity_p95_error",
        "Put-Call平价95%偏离",
    ),
    "pressure__calendar_variance_violation_ratio": (
        "无套利风险",
        "calendar_variance_violation_ratio",
        "日历总方差违反率",
    ),
    "pressure__gamma_hhi": ("Greeks集中风险", "gamma_hhi", "Gamma持仓加权集中度"),
    "pressure__vega_hhi": ("Greeks集中风险", "vega_hhi", "Vega持仓加权集中度"),
    "pressure__zero_volume_share": (
        "质量与流动性",
        "zero_volume_share",
        "零成交量合约占比",
    ),
    "pressure__iv_floor_share": (
        "质量与流动性",
        "iv_floor_share",
        "IV求解下限占比",
    ),
    "pressure__coverage_shortfall": (
        "质量与流动性",
        "coverage_shortfall",
        "曲面节点覆盖缺口",
    ),
}

# Quality/liquidity pressures are displayed as evidence and contribute to the
# overall watch score, but formal escalation uses market-risk signals only.
# This keeps data-quality degradation from being mistaken for a market event.
DECISION_PRESSURE_COLUMNS = tuple(
    column for column, (group, _, _) in PRESSURE_SPECS.items() if group != "质量与流动性"
)


@dataclass(frozen=True, slots=True)
class DecisionPolicy:
    attention_pressure: float = 0.90
    attention_release_pressure: float = 0.85
    warning_pressure: float = 0.98
    warning_upper_pressure: float = 1.00
    danger_pressure: float = 1.00
    danger_core_pressure: float = 1.50
    multi_signal_count: int = 3
    cooldown_bars: int = 6
    persistence_bars: int = 2
    max_watch_bars: int = 6
    policy_version: str = DECISION_POLICY_VERSION

    @classmethod
    def from_diagnostics(cls, payload: dict[str, object] | None) -> "DecisionPolicy":
        """Validate and restore the pre-registered canonical policy identity."""

        if payload is None:
            raise ValueError("policy_version is required in policy diagnostics")
        policy_version = payload.get("policy_version")
        if policy_version != DECISION_POLICY_VERSION:
            raise ValueError(
                "Unsupported policy_version "
                f"{policy_version!r}; expected {DECISION_POLICY_VERSION!r}"
            )
        if payload.get("selection_data") != PRIMARY_POLICY_SELECTION_DATA:
            raise ValueError(
                "selection_data must identify the pre-registered fixed canonical policy"
            )
        policy = cls(policy_version=DECISION_POLICY_VERSION)
        selected_fields = {
            "selected_lower_pressure": policy.warning_pressure,
            "selected_upper_pressure": policy.warning_upper_pressure,
            "selected_cooldown_bars": policy.cooldown_bars,
        }
        for field, expected in selected_fields.items():
            observed = payload.get(field)
            try:
                matches = float(observed) == float(expected)
            except (TypeError, ValueError):
                matches = False
            if not matches:
                raise ValueError(
                    f"{field} must match the pre-registered canonical policy value {expected}"
                )
        parameter_hash = payload.get("policy_parameter_hash")
        if parameter_hash != policy.parameter_hash:
            raise ValueError(
                "policy_parameter_hash is missing or does not match the selected policy parameters"
            )
        return policy

    @property
    def parameter_hash(self) -> str:
        parameters = asdict(self)
        parameters.pop("policy_version")
        encoded = json.dumps(
            parameters,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def canonical_policy_diagnostics() -> dict[str, object]:
    """Return the stable, label-independent identity of the formal policy."""

    policy = DecisionPolicy()
    return {
        "selection_data": PRIMARY_POLICY_SELECTION_DATA,
        "policy_version": policy.policy_version,
        "policy_parameter_hash": policy.parameter_hash,
        "selected_lower_pressure": policy.warning_pressure,
        "selected_upper_pressure": policy.warning_upper_pressure,
        "selected_cooldown_bars": policy.cooldown_bars,
    }


@dataclass(frozen=True, slots=True)
class DecisionResult:
    timestamp: pd.Timestamp
    alert_level: int
    alert_name: str
    alert_emitted: bool
    risk_score: float
    policy_version: str
    policy_parameter_hash: str
    transition_reason: str
    trigger_reasons: list[TriggerReason]
    feature_evidence: list[FeatureEvidence]

    def to_dict(self) -> dict[str, object]:
        return _json_ready(asdict(self))


def _number(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None


def _direction(current: float | None, previous: float | None) -> tuple[str, float | None]:
    if current is None or previous is None:
        return "持平", None
    difference = current - previous
    tolerance = max(abs(previous), 1.0) * 1e-10
    label = "上升" if difference > tolerance else "下降" if difference < -tolerance else "持平"
    rate = difference / abs(previous) if abs(previous) > 1e-12 else None
    return label, rate


def _severity(pressure: float | None, policy: DecisionPolicy) -> int:
    if pressure is None:
        return 0
    if pressure >= policy.danger_core_pressure:
        return 3
    if pressure >= policy.warning_pressure:
        return 2
    if pressure >= policy.attention_pressure:
        return 1
    return 0


def apply_decision_policy(
    features: pd.DataFrame,
    policy: DecisionPolicy | None = None,
    *,
    timestamp: pd.Timestamp | str | None = None,
) -> pd.DataFrame:
    """Replay the one canonical, past-only warning state machine.

    ``alert_level`` is the continuous current risk state. ``alert_emitted`` is
    the sparse operational-notification pulse. Downgrade uses a lower release
    boundary and a minimum persistence period to avoid adjacent-bar flicker.
    """

    policy = policy or DecisionPolicy()
    view = features.sort_index()
    if timestamp is not None:
        view = view.loc[view.index <= pd.Timestamp(timestamp)]
    if view.empty:
        return pd.DataFrame(
            columns=[
                "decision_score",
                "independent_pressure_signal_count",
                "alert_level",
                "alert_emitted",
                "alert_name",
                "policy_version",
                "policy_parameter_hash",
                "transition_reason",
            ],
            index=view.index,
        )

    core = pd.to_numeric(view.get("core_risk_pressure"), errors="coerce")
    overall = pd.to_numeric(view.get("risk_pressure"), errors="coerce")
    score = pd.concat([core.rename("core"), overall.rename("overall")], axis=1).max(axis=1)
    data_ready = view.get("data_ready", False)
    if not isinstance(data_ready, pd.Series):
        data_ready = pd.Series(bool(data_ready), index=view.index)
    history_ready = view.get("history_ready", False)
    if not isinstance(history_ready, pd.Series):
        history_ready = pd.Series(bool(history_ready), index=view.index)
    ready = data_ready.fillna(False) & history_ready.fillna(False) & core.notna()
    pressure_columns = [column for column in DECISION_PRESSURE_COLUMNS if column in view]
    independent = (
        view[pressure_columns].ge(policy.danger_pressure).sum(axis=1)
        if pressure_columns
        else pd.Series(0, index=view.index)
    )

    levels = np.zeros(len(view), dtype="int8")
    alert_emitted = np.zeros(len(view), dtype=bool)
    transition_reasons = np.full(len(view), "not_ready", dtype=object)
    watch_active = False
    watch_started = -10_000
    last_warning = -10_000
    previous_danger = False
    previous_formal_state = False
    for position in range(len(view)):
        if not bool(ready.iloc[position]):
            watch_active = False
            previous_danger = False
            previous_formal_state = False
            continue
        core_value = float(core.iloc[position])
        score_value = float(score.iloc[position])
        danger_candidate = bool(
            core_value >= policy.danger_core_pressure
            and int(independent.iloc[position]) >= policy.multi_signal_count
        )
        warning_candidate = bool(
            core_value >= policy.warning_pressure
            and core_value < policy.warning_upper_pressure
        )
        formal_state = danger_candidate or core_value >= policy.warning_pressure

        if danger_candidate:
            levels[position] = 3
            if not previous_danger:
                alert_emitted[position] = True
                transition_reasons[position] = "danger_emitted"
                watch_started = position
                last_warning = position
            else:
                transition_reasons[position] = "danger_held"
            watch_active = True
        elif core_value >= policy.warning_pressure:
            levels[position] = 2
            if not watch_active:
                watch_started = position
            watch_active = True
            if not previous_formal_state:
                # A direct jump over the calibrated frontier must still notify
                # the user when the formal warning state is first entered.
                alert_emitted[position] = True
                transition_reasons[position] = "warning_emitted"
                last_warning = position
                watch_started = position
            elif warning_candidate and position - last_warning >= policy.cooldown_bars:
                alert_emitted[position] = True
                transition_reasons[position] = "warning_emitted"
                last_warning = position
                watch_started = position
            elif warning_candidate:
                transition_reasons[position] = "cooldown_suppressed"
            else:
                transition_reasons[position] = "warning_held"
        else:
            if score_value >= policy.attention_pressure:
                if not watch_active:
                    watch_started = position
                    transition_reasons[position] = "watch_started"
                else:
                    transition_reasons[position] = "watch_held"
                watch_active = True
            elif (
                watch_active
                and position - watch_started >= policy.persistence_bars
                and score_value <= policy.attention_release_pressure
            ):
                watch_active = False
                transition_reasons[position] = "watch_released"
            elif (
                watch_active
                and position - watch_started >= policy.max_watch_bars
                and score_value < policy.attention_pressure
            ):
                watch_active = False
                transition_reasons[position] = "watch_released"
            elif watch_active:
                transition_reasons[position] = "watch_held"
            else:
                transition_reasons[position] = "normal"
            levels[position] = 1 if watch_active else 0
        previous_danger = danger_candidate
        previous_formal_state = formal_state

    result = pd.DataFrame(
        {
            "decision_score": score,
            "independent_pressure_signal_count": independent.astype("int16"),
            "alert_level": levels,
            "alert_emitted": alert_emitted,
            "transition_reason": transition_reasons,
        },
        index=view.index,
    )
    result["alert_name"] = result["alert_level"].map(ALERT_NAMES)
    result["policy_version"] = policy.policy_version
    result["policy_parameter_hash"] = policy.parameter_hash
    return result


def _evidence(
    history: pd.DataFrame,
    row: pd.Series,
    policy: DecisionPolicy,
) -> tuple[list[FeatureEvidence], list[TriggerReason]]:
    previous = history.iloc[-2] if len(history) > 1 else pd.Series(dtype=object)
    evidence: list[FeatureEvidence] = []
    ranked: list[tuple[float, TriggerReason]] = []
    for pressure_column, (group, feature_name, label) in PRESSURE_SPECS.items():
        if pressure_column not in row.index:
            continue
        current = _number(row.get(feature_name))
        reference = _number(row.get(f"history_q95__{feature_name}"))
        pressure = _number(row.get(pressure_column))
        previous_value = _number(previous.get(feature_name)) if len(previous) else None
        direction, change_rate = _direction(current, previous_value)
        severity = _severity(pressure, policy)
        status = ALERT_NAMES[severity]
        evidence.append(
            FeatureEvidence(
                group=group,
                feature_name=feature_name,
                label=label,
                current_value=current,
                reference_value=reference,
                pressure_ratio=pressure,
                change_rate=change_rate,
                status=status,
            )
        )
        if pressure is not None and pressure >= policy.attention_pressure:
            message = (
                f"{label}当前值{current:.6g}，动态阈值{reference:.6g}，"
                f"历史阈值倍数{pressure:.3f}，较上一时点{direction}"
                if current is not None and reference is not None
                else f"{label}历史阈值倍数{pressure:.3f}，状态{direction}"
            )
            reason = TriggerReason(
                feature_name=feature_name,
                label=label,
                current_value=current,
                reference_value=reference,
                pressure_ratio=pressure,
                change_direction=direction,
                severity=severity,
                message=message,
            )
            ranked.append((pressure, reason))
    ranked.sort(key=lambda item: item[0], reverse=True)
    reasons = [reason for _, reason in ranked[:3]]
    return evidence, reasons


def assess_features(
    features: pd.DataFrame,
    timestamp: pd.Timestamp | str,
    policy: DecisionPolicy | None = None,
    config: PipelineConfig | None = None,
) -> DecisionResult:
    """Assess one timestamp using only rows available at or before it."""

    policy = policy or DecisionPolicy()
    config = config or PipelineConfig()
    timestamp = pd.Timestamp(timestamp)
    if timestamp not in features.index:
        raise InvalidTimestampError(f"风险特征中不存在时间点：{timestamp}")
    history = features.loc[features.index <= timestamp].sort_index()
    row = history.loc[timestamp]
    if isinstance(row, pd.DataFrame):
        row = row.iloc[-1]
    if not bool(row.get("data_ready", False)):
        raise SurfaceNotReadyError(f"时间点 {timestamp} 的曲面数据质量不足")
    if not bool(row.get("history_ready", False)):
        raise InsufficientHistoryError(f"时间点 {timestamp} 之前的动态阈值历史不足")

    core = _number(row.get("core_risk_pressure"))
    overall = _number(row.get("risk_pressure"))
    if core is None:
        raise InsufficientHistoryError(f"时间点 {timestamp} 缺少核心历史压力")
    risk_score = max(core, overall if overall is not None else core)
    previous_core = _number(history.iloc[-2].get("core_risk_pressure")) if len(history) > 1 else None
    state = apply_decision_policy(history, policy, timestamp=timestamp)
    level = int(state.iloc[-1]["alert_level"])
    alert_emitted = bool(state.iloc[-1]["alert_emitted"])
    transition_reason = str(state.iloc[-1]["transition_reason"])

    evidence, reasons = _evidence(history, row, policy)
    if not reasons:
        reasons = [
            TriggerReason(
                feature_name="core_risk_pressure",
                label="综合核心风险压力",
                current_value=core,
                reference_value=1.0,
                pressure_ratio=core,
                change_direction="持平" if previous_core is None else _direction(core, previous_core)[0],
                severity=0,
                message=f"综合核心风险压力{core:.3f}，未达到关注阈值{policy.attention_pressure:.2f}",
            )
        ]
    return DecisionResult(
        timestamp=timestamp,
        alert_level=level,
        alert_name=ALERT_NAMES[level],
        alert_emitted=alert_emitted,
        risk_score=float(risk_score),
        policy_version=policy.policy_version,
        policy_parameter_hash=policy.parameter_hash,
        transition_reason=transition_reason,
        trigger_reasons=reasons,
        feature_evidence=evidence,
    )
````

</details>
