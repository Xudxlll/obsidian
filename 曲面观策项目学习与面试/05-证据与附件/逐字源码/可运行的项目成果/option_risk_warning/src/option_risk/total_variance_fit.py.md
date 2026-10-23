---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py>)

SHA-256：`155f052b9ca8ca5042cdfa67eb7ed769b32ce082aa72a9f40ae6f7b3115f47a9`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
"""Total-variance contracts, curve math, and pure no-arbitrage checks."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from numbers import Integral, Real
from typing import Any, Literal, TypeAlias

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import minimize, shgo
from scipy.special import ndtr


class FitMethod(str, Enum):
    SSVI = "SSVI"
    RAW_SVI = "RAW_SVI"
    PCHIP = "PCHIP"
    LINEAR = "LINEAR"


class FinalMethod(str, Enum):
    SSVI = "SSVI"
    RAW_SVI = "RAW_SVI"
    PCHIP = "PCHIP"
    LINEAR = "LINEAR"
    UNUSABLE = "UNUSABLE"


class AttemptScope(str, Enum):
    TIMESTAMP = "timestamp"
    EXPIRY = "expiry"


class AttemptStatus(str, Enum):
    SKIPPED = "skipped"
    FAILED = "failed"
    ACCEPTED = "accepted"


class CheckStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    INDETERMINATE = "indeterminate"
    NOT_APPLICABLE = "not_applicable"
    NOT_TESTABLE = "not_testable"


class ResultStatus(str, Enum):
    USABLE = "usable"
    UNUSABLE = "unusable"


class OverallStatus(str, Enum):
    ALL_USABLE = "all_usable"
    PARTIALLY_USABLE = "partially_usable"
    NONE_USABLE = "none_usable"


class TimestampStatus(str, Enum):
    READY = "ready"
    FAILED_INPUT = "failed_input"


class SurfaceGridStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE_NO_SUPPORT = "unavailable_no_support"
    UNAVAILABLE_INPUT_FAILURE = "unavailable_input_failure"


class ForwardSource(str, Enum):
    TRUE_FUTURES_FORWARD = "true_futures_forward"
    UNDERLYING_PRICE_PROXY = "underlying_price_proxy"
    PRECOMPUTED_LOG_MONEYNESS_UNKNOWN = "precomputed_log_moneyness_unknown"


JSONScalar: TypeAlias = str | int | float | bool | None


class _FrozenDict(dict[str, Any]):
    """A deepcopy-safe immutable mapping used by the frozen policy object."""

    @staticmethod
    def _immutable(*args: object, **kwargs: object) -> None:
        raise TypeError("FitPolicy mappings are immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable
    __ior__ = _immutable

    def __deepcopy__(self, memo: dict[int, object]) -> _FrozenDict:
        return self

    def copy(self) -> _FrozenDict:
        return _FrozenDict(self)


CHECK_NAMES = (
    "positive_total_variance",
    "call_price_monotonic",
    "call_price_convex",
    "butterfly_g_nonnegative",
    "calendar_consistent",
    "jump_reliable",
)
CHECK_NAME_SET = frozenset(CHECK_NAMES)

INPUT_FAILURE_CODES = (
    "invalid_strike",
    "invalid_forward",
    "invalid_iv",
    "invalid_time_to_expiry",
    "invalid_log_moneyness",
    "inconsistent_log_moneyness",
)

FAILURE_CODES = frozenset(
    (
        *INPUT_FAILURE_CODES,
        "mixed_forward_sources",
        "degenerate_k_support",
        "insufficient_nodes",
        "not_enough_maturities",
        "optimizer_failed",
        "optimizer_exception",
        "non_finite_parameters",
        "parameter_constraint_failed",
        "parent_ssvi_rejected",
        "rmse_exceeded",
        "non_positive_total_variance",
        "call_price_monotonicity_failed",
        "call_price_convexity_failed",
        "butterfly_failed",
        "calendar_conflict",
        "abnormal_jump",
        "check_resolution_limit",
        "serialization_failed",
        "artifact_validation_failed",
        "cache_boundary_violation",
        "representative_timestamp_missing",
    )
)

ATTEMPT_FAILURE_CODES = frozenset(
    (
        "not_enough_maturities",
        "optimizer_failed",
        "optimizer_exception",
        "non_finite_parameters",
        "parameter_constraint_failed",
        "parent_ssvi_rejected",
        "rmse_exceeded",
        "non_positive_total_variance",
        "call_price_monotonicity_failed",
        "call_price_convexity_failed",
        "butterfly_failed",
        "calendar_conflict",
        "abnormal_jump",
        "check_resolution_limit",
    )
)

SSVI_CHILD_FAILURE_CODES = frozenset(
    (
        "rmse_exceeded",
        "non_positive_total_variance",
        "call_price_monotonicity_failed",
        "call_price_convexity_failed",
        "butterfly_failed",
        "abnormal_jump",
        "check_resolution_limit",
        "parent_ssvi_rejected",
        "calendar_conflict",
    )
)

METHOD_FAILURE_CODES = {
    FitMethod.SSVI: ATTEMPT_FAILURE_CODES,
    FitMethod.RAW_SVI: ATTEMPT_FAILURE_CODES
    - frozenset(("not_enough_maturities", "parent_ssvi_rejected")),
    FitMethod.PCHIP: frozenset(
        (
            "rmse_exceeded",
            "non_positive_total_variance",
            "call_price_monotonicity_failed",
            "call_price_convexity_failed",
            "calendar_conflict",
            "abnormal_jump",
            "check_resolution_limit",
        )
    ),
    FitMethod.LINEAR: frozenset(
        (
            "rmse_exceeded",
            "non_positive_total_variance",
            "call_price_monotonicity_failed",
            "call_price_convexity_failed",
            "calendar_conflict",
            "abnormal_jump",
            "check_resolution_limit",
        )
    ),
}

FAILURE_CODE_CHECK = {
    "non_positive_total_variance": "positive_total_variance",
    "call_price_monotonicity_failed": "call_price_monotonic",
    "call_price_convexity_failed": "call_price_convex",
    "butterfly_failed": "butterfly_g_nonnegative",
    "calendar_conflict": "calendar_consistent",
    "abnormal_jump": "jump_reliable",
}

HARD_GATE_CHECK_ORDER = (
    "positive_total_variance",
    "call_price_monotonic",
    "call_price_convex",
    "butterfly_g_nonnegative",
    "jump_reliable",
    "calendar_consistent",
)

CHECK_FAILURE_CODE = {
    check_name: failure_code
    for failure_code, check_name in FAILURE_CODE_CHECK.items()
}

REASON_CODES_BY_CHECK = {
    "positive_total_variance": frozenset(
        ("below_variance_floor", "non_finite_total_variance", "not_run", "resolution_limit")
    ),
    "call_price_monotonic": frozenset(
        ("call_price_increase", "not_run", "resolution_limit")
    ),
    "call_price_convex": frozenset(
        ("decreasing_secant_slope", "not_run", "resolution_limit")
    ),
    "butterfly_g_nonnegative": frozenset(
        ("negative_g", "method_has_no_analytic_g", "not_run", "resolution_limit")
    ),
    "calendar_consistent": frozenset(
        (
            "calendar_total_variance_decrease",
            "not_run",
            "no_prior_maturity",
            "no_overlap",
            "resolution_limit",
        )
    ),
    "jump_reliable": frozenset(
        (
            "absolute_iv_slope_exceeded",
            "robust_iv_slope_ratio_exceeded",
            "not_run",
            "resolution_limit",
        )
    ),
}

FAILED_REASON_CODES_BY_CHECK = {
    "positive_total_variance": frozenset(
        ("below_variance_floor", "non_finite_total_variance")
    ),
    "call_price_monotonic": frozenset(("call_price_increase",)),
    "call_price_convex": frozenset(("decreasing_secant_slope",)),
    "butterfly_g_nonnegative": frozenset(("negative_g",)),
    "calendar_consistent": frozenset(("calendar_total_variance_decrease",)),
    "jump_reliable": frozenset(
        ("absolute_iv_slope_exceeded", "robust_iv_slope_ratio_exceeded")
    ),
}

NOT_APPLICABLE_REASON_CODES_BY_CHECK = {
    name: frozenset(("not_run",)) for name in CHECK_NAMES
}
NOT_APPLICABLE_REASON_CODES_BY_CHECK["butterfly_g_nonnegative"] = frozenset(
    ("method_has_no_analytic_g", "not_run")
)
NOT_APPLICABLE_REASON_CODES_BY_CHECK["calendar_consistent"] = frozenset(
    ("no_prior_maturity", "not_run")
)


def _dict_ssvi_seeds() -> dict[str, tuple[float, ...]]:
    return {
        "rho": (-0.5, 0.0, 0.5),
        "gamma": (0.1, 0.3, 0.5),
        "eta": (0.1, 0.5, 1.0),
    }


def _dict_raw_svi_seeds() -> dict[str, tuple[float | str, ...]]:
    return {
        "rho": (-0.5, 0.0, 0.5),
        "b": (0.1, 0.5, 1.0),
        "m": ("k_at_min_w", "median_k"),
        "sigma": ("max_span_over_10_0.01", "max_span_over_2_0.05"),
    }


def _dict_slsqp_options() -> dict[str, float | int | bool]:
    return {"ftol": 1e-12, "maxiter": 2000, "eps": 1e-8, "disp": False}


def _dict_shgo_options() -> dict[str, int | str]:
    return {"n": 256, "iters": 3, "sampling_method": "simplicial", "workers": 1}


def _dict_shgo_minimizer_options() -> dict[str, float | int | bool | str]:
    return {"method": "SLSQP", "ftol": 1e-12, "maxiter": 500, "disp": False}


@dataclass(frozen=True, slots=True)
class FitPolicy:
    policy_version: str = "total-variance-fit-diagnostic-v1"
    base_grid_size: int = 201
    diagnostic_curve_base_size: int = 201
    surface_grid_size: int = 201
    max_refinement_depth: int = 8
    min_k_interval: float = 1e-6
    near_margin_factor: float = 10.0
    variance_floor: float = 1e-10
    constraint_margin: float = 1e-8
    nrmse_limit: float = 0.15
    price_monotonic_abs_tolerance: float = 1e-8
    price_convex_slope_tolerance: float = 1e-6
    butterfly_g_tolerance: float = 1e-8
    calendar_abs_tolerance: float = 1e-6
    calendar_rel_tolerance: float = 0.005
    max_abs_iv_slope: float = 5.0
    robust_iv_slope_floor: float = 0.05
    max_robust_slope_ratio: float = 10.0
    k_consistency_tolerance: float = 1e-10
    knot_neighbor_divisor: float = 100.0
    adaptive_refinement_checks: tuple[str, ...] = (
        "positive_total_variance",
        "butterfly_g_nonnegative",
        "calendar_consistent",
    )
    slsqp_method: str = "SLSQP"
    slsqp_options: dict[str, float | int | bool] = field(default_factory=_dict_slsqp_options)
    ssvi_variable_order: tuple[str, ...] = ("theta_by_maturity", "rho", "eta", "gamma")
    ssvi_theta_upper_cap: float = 100.0
    ssvi_theta_upper_floor: float = 1.0
    ssvi_theta_upper_observed_multiplier: float = 10.0
    ssvi_rho_bounds: tuple[float, float] = (-0.999, 0.999)
    ssvi_eta_upper: float = 100.0
    ssvi_gamma_bounds: tuple[float, float] = (0.0, 0.5)
    ssvi_start_seeds: dict[str, tuple[float, ...]] = field(default_factory=_dict_ssvi_seeds)
    ssvi_start_loop_order: tuple[str, ...] = ("rho", "gamma", "eta")
    ssvi_generated_start_count: int = 27
    ssvi_barrier_limit: float = 4.0
    ssvi_eta_cap_multiplier: float = 0.8
    raw_svi_variable_order: tuple[str, ...] = ("a", "b", "rho", "m", "sigma")
    raw_svi_w_scale_floor: float = 1e-4
    raw_svi_span_floor: float = 0.01
    raw_svi_a_bound_multiplier: float = 10.0
    raw_svi_b_upper: float = 2.0
    raw_svi_rho_bounds: tuple[float, float] = (-0.999, 0.999)
    raw_svi_m_span_multiplier: float = 2.0
    raw_svi_sigma_upper_floor: float = 2.0
    raw_svi_sigma_span_multiplier: float = 4.0
    raw_svi_a_initial_multiplier: float = 0.5
    raw_svi_b_clip_multiplier: float = 0.8
    raw_svi_start_seeds: dict[str, tuple[float | str, ...]] = field(
        default_factory=_dict_raw_svi_seeds
    )
    raw_svi_start_loop_order: tuple[str, ...] = ("rho", "b", "m", "sigma")
    raw_svi_generated_start_count: int = 36
    start_precheck_order: tuple[str, ...] = (
        "finite",
        "bounds",
        "analytic_constraints",
    )
    start_deduplication_rule: str = "float64_exact_keep_earliest_index"
    near_tie_relative_tolerance: float = 1e-12
    parameter_format: str = ".15g"
    success_selection_order: tuple[str, ...] = (
        "maximum_per_expiry_nrmse",
        "formatted_parameter_tuple",
        "start_index",
    )
    failure_representative_order: tuple[str, ...] = (
        "negative_stage_reached",
        "hard_failure_count",
        "primary_failure_priority",
        "finite_nrmse_or_positive_infinity",
        "finite_objective_or_positive_infinity",
        "finite_max_constraint_violation_or_positive_infinity",
        "formatted_parameter_tuple_or_high_sentinel",
        "start_index",
    )
    failure_stage_order: tuple[str, ...] = (
        "optimizer_exception",
        "optimizer_failed",
        "non_finite_parameters",
        "parameter_constraint_failed",
        "rmse_exceeded",
        "positive_total_variance",
        "call_price_monotonic",
        "call_price_convex",
        "butterfly_g_nonnegative",
        "jump_reliable",
    )
    failure_stage_reached_values: tuple[int, ...] = (0, 1, 2, 3, 4)
    failure_parameter_high_sentinel: tuple[str, ...] = ("\uffff",)
    shgo_options: dict[str, int | str] = field(default_factory=_dict_shgo_options)
    shgo_minimizer_options: dict[str, float | int | bool | str] = field(
        default_factory=_dict_shgo_minimizer_options
    )
    shgo_completeness_requirements: tuple[str, ...] = (
        "success_true",
        "finite_x_and_fun",
        "nonempty_finite_equal_length_xl_funl",
        "all_x_within_closed_support",
    )
    shgo_candidate_sources: tuple[str, ...] = (
        "k_min",
        "k_max",
        "result_x",
        "all_result_xl",
    )
    pchip_root_imag_tolerance: float = 1e-10
    pchip_root_interval_tolerance: float = 1e-12
    pchip_stationary_root_rules: tuple[str, ...] = (
        "w_prime_equals_zero",
        "two_w_w_second_minus_w_prime_squared_equals_zero",
        "strip_exact_zero_leading_coefficients",
        "float64_exact_deduplication",
    )

    def __post_init__(self) -> None:
        if not isinstance(self.policy_version, str) or not self.policy_version:
            raise ValueError("policy_version must be a non-empty string")
        if self.policy_version == "total-variance-fit-diagnostic-v1":
            for policy_field in dataclasses.fields(self):
                if policy_field.name == "policy_version":
                    continue
                if policy_field.default is not dataclasses.MISSING:
                    expected = policy_field.default
                else:
                    expected = policy_field.default_factory()
                if getattr(self, policy_field.name) != expected:
                    raise ValueError(
                        "v1 fixed strategy cannot change without a new policy_version"
                    )
        for policy_field in dataclasses.fields(self):
            value = getattr(self, policy_field.name)
            if isinstance(value, dict) and not isinstance(value, _FrozenDict):
                object.__setattr__(self, policy_field.name, _FrozenDict(value))


def _require_enum(value: object, enum_type: type[Enum], owner: str) -> None:
    if not isinstance(value, enum_type):
        raise ValueError(f"{owner} must be {enum_type.__name__}")


def _require_nonempty_string(value: object, owner: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{owner} must be a non-empty string")


def _require_count(value: object, owner: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 0:
        raise ValueError(f"{owner} must be a non-negative integer")


def _require_finite(
    value: object,
    owner: str,
    *,
    nullable: bool = False,
    positive: bool = False,
) -> None:
    if value is None and nullable:
        return
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(float(value)):
        raise ValueError(f"{owner} must be finite")
    if positive and float(value) <= 0.0:
        raise ValueError(f"{owner} must be positive")


def _require_local_timestamp(value: object, owner: str = "timestamp") -> None:
    _require_nonempty_string(value, owner)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", value) is None:
        raise ValueError(f"{owner} must be local ISO-8601 with whole seconds")


def _require_attempt_id(value: object, owner: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if not isinstance(value, str) or re.fullmatch(r"attempt:[0-9a-f]{64}", value) is None:
        raise ValueError(f"{owner} must be a full canonical attempt id")


def _require_pair_id(value: object) -> None:
    if not isinstance(value, str) or re.fullmatch(r"calendar-pair:[0-9a-f]{64}", value) is None:
        raise ValueError("pair_check_id must be a full canonical pair id")


def _require_fingerprint(value: object, owner: str) -> None:
    if not isinstance(value, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
        raise ValueError(f"{owner} must be a canonical SHA-256 fingerprint")


def _identity_digest(payload: dict[str, object], prefix: str) -> str:
    document = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ) + "\n"
    return prefix + hashlib.sha256(document.encode("utf-8")).hexdigest()


def make_attempt_id(
    *,
    input_fingerprint: str,
    product: str,
    timestamp: str,
    scope: AttemptScope,
    maturity_id: str | None,
    participating_maturities: Sequence[str],
    method: FitMethod,
    attempt_order: int,
    policy_version: str,
) -> str:
    """Build the complete deterministic section 12.5 attempt identity."""

    _require_fingerprint(input_fingerprint, "input_fingerprint")
    _require_nonempty_string(product, "product")
    _require_local_timestamp(timestamp)
    _require_enum(scope, AttemptScope, "scope")
    _require_enum(method, FitMethod, "method")
    _require_count(attempt_order, "attempt_order")
    _require_nonempty_string(policy_version, "policy_version")
    maturities = list(participating_maturities)
    if not all(isinstance(value, str) and value for value in maturities):
        raise ValueError("participating_maturities must contain non-empty strings")
    if scope is AttemptScope.TIMESTAMP:
        if maturity_id is not None or not maturities:
            raise ValueError("timestamp attempt identity requires participating maturities only")
    elif not isinstance(maturity_id, str) or not maturity_id or maturities:
        raise ValueError("expiry attempt identity requires one maturity_id only")
    return _identity_digest(
        {
            "input_fingerprint": input_fingerprint,
            "product": product,
            "timestamp": timestamp,
            "scope": scope.value,
            "maturity_id": maturity_id,
            "participating_maturities": maturities,
            "method": method.value,
            "attempt_order": attempt_order,
            "policy_version": policy_version,
        },
        "attempt:",
    )


def make_calendar_pair_id(
    *,
    input_fingerprint: str,
    product: str,
    timestamp: str,
    phase: Literal["ssvi_parent", "expiry_selection"],
    parent_attempt_id: str | None,
    earlier_maturity_id: str,
    later_maturity_id: str,
    earlier_attempt_id: str | None,
    later_attempt_id: str | None,
    policy_version: str,
) -> str:
    """Build the complete deterministic section 12.5 calendar-pair identity."""

    _require_fingerprint(input_fingerprint, "input_fingerprint")
    _require_nonempty_string(product, "product")
    _require_local_timestamp(timestamp)
    if phase not in {"ssvi_parent", "expiry_selection"}:
        raise ValueError("phase is outside the closed set")
    _require_attempt_id(parent_attempt_id, "parent_attempt_id", nullable=True)
    _require_nonempty_string(earlier_maturity_id, "earlier_maturity_id")
    _require_nonempty_string(later_maturity_id, "later_maturity_id")
    _require_attempt_id(earlier_attempt_id, "earlier_attempt_id", nullable=True)
    _require_attempt_id(later_attempt_id, "later_attempt_id", nullable=True)
    _require_nonempty_string(policy_version, "policy_version")
    return _identity_digest(
        {
            "input_fingerprint": input_fingerprint,
            "product": product,
            "timestamp": timestamp,
            "phase": phase,
            "parent_attempt_id": parent_attempt_id,
            "earlier_maturity_id": earlier_maturity_id,
            "later_maturity_id": later_maturity_id,
            "earlier_attempt_id": earlier_attempt_id,
            "later_attempt_id": later_attempt_id,
            "policy_version": policy_version,
        },
        "calendar-pair:",
    )


def _require_failure_code(value: object, *, nullable: bool) -> None:
    if value is None and nullable:
        return
    if value not in FAILURE_CODES:
        raise ValueError("failure_code is outside the closed v1 set")


def _require_checks(value: object, owner: str) -> None:
    if not isinstance(value, dict) or set(value) != CHECK_NAME_SET:
        raise ValueError(f"{owner} must contain exactly the six closed checks")
    for name, diagnostic in value.items():
        if not isinstance(diagnostic, CheckDiagnostic) or diagnostic.name != name:
            raise ValueError(f"{owner}[{name!r}] must be its matching CheckDiagnostic")


def _require_finite_sequence(
    values: object,
    owner: str,
    *,
    nullable_items: bool = False,
    strictly_increasing: bool = False,
) -> None:
    if not isinstance(values, list):
        raise ValueError(f"{owner} must be a list")
    previous: float | None = None
    for item in values:
        _require_finite(item, owner, nullable=nullable_items)
        if item is not None and strictly_increasing:
            current = float(item)
            if previous is not None and current <= previous:
                raise ValueError(f"{owner} must be strictly increasing")
            previous = current


def _require_parameter_scalars(value: Mapping[str, Any], owner: str) -> None:
    for key, item in value.items():
        if isinstance(item, Mapping):
            _require_parameter_scalars(item, f"{owner}.{key}")
        else:
            _require_finite(item, f"{owner}.{key}")


@dataclass(frozen=True, slots=True)
class CheckDiagnostic:
    name: str
    status: CheckStatus
    conclusion: str
    reason_code: str | None
    primary_value: float | None
    threshold: float | None
    violation_count: int | None
    grid_point_count: int
    metrics: dict[str, JSONScalar]

    def __post_init__(self) -> None:
        if self.name not in CHECK_NAME_SET:
            raise ValueError("name is outside the closed check set")
        _require_enum(self.status, CheckStatus, "status")
        _require_finite(self.primary_value, "primary_value", nullable=True)
        _require_finite(self.threshold, "threshold", nullable=True)
        _require_count(self.violation_count, "violation_count", nullable=True)
        _require_count(self.grid_point_count, "grid_point_count")
        if not isinstance(self.metrics, dict) or not all(
            isinstance(key, str) for key in self.metrics
        ):
            raise ValueError("metrics must be a string-keyed dictionary")
        for value in self.metrics.values():
            if isinstance(value, Enum):
                value = value.value
            if isinstance(value, np.generic):
                value = value.item()
            if value is not None and not isinstance(value, (str, bool, int, float)):
                raise ValueError("metrics values must be JSON scalars")
            if isinstance(value, (float, np.floating)) and not math.isfinite(float(value)):
                raise ValueError("metrics values must be finite")

        expected_conclusion = {
            CheckStatus.PASSED: "sampled_no_violation",
            CheckStatus.FAILED: "violation_found",
            CheckStatus.INDETERMINATE: "unreliable",
            CheckStatus.NOT_APPLICABLE: "not_applicable",
            CheckStatus.NOT_TESTABLE: "not_testable",
        }[self.status]
        if self.conclusion != expected_conclusion:
            raise ValueError("status and conclusion violate the closed truth table")
        if self.status is CheckStatus.PASSED:
            if self.reason_code is not None:
                raise ValueError("passed checks cannot have a reason_code")
        else:
            if self.reason_code not in REASON_CODES_BY_CHECK[self.name]:
                raise ValueError("reason_code is invalid for this check")
        if self.status is CheckStatus.FAILED:
            if self.reason_code not in FAILED_REASON_CODES_BY_CHECK[self.name]:
                raise ValueError("failed reason_code is invalid for this check")
            if self.primary_value is None or self.threshold is None:
                raise ValueError("failed checks require a value and threshold")
        if self.status is CheckStatus.INDETERMINATE and self.reason_code != "resolution_limit":
            raise ValueError("indeterminate checks require resolution_limit")
        if self.status is CheckStatus.NOT_APPLICABLE and self.reason_code not in (
            NOT_APPLICABLE_REASON_CODES_BY_CHECK[self.name]
        ):
            raise ValueError("not_applicable reason_code is invalid for this check")
        if self.status is CheckStatus.NOT_TESTABLE and self.reason_code != "no_overlap":
            raise ValueError("not_testable checks require no_overlap")


@dataclass(frozen=True, slots=True)
class OptimizerStartSummary:
    generated_count: int
    precheck_discarded_count: int
    duplicate_discarded_count: int
    executed_count: int
    optimizer_reported_success_count: int
    evaluable_count: int
    local_success_count: int
    selected_start_index: int | None
    selection_kind: Literal["local_success", "failure_representative"] | None

    def __post_init__(self) -> None:
        for field_name in (
            "generated_count",
            "precheck_discarded_count",
            "duplicate_discarded_count",
            "executed_count",
            "optimizer_reported_success_count",
            "evaluable_count",
            "local_success_count",
        ):
            _require_count(getattr(self, field_name), field_name)
        _require_count(self.selected_start_index, "selected_start_index", nullable=True)
        if self.generated_count != (
            self.precheck_discarded_count
            + self.duplicate_discarded_count
            + self.executed_count
        ):
            raise ValueError("optimizer start counts do not reconcile")
        if self.optimizer_reported_success_count > self.executed_count:
            raise ValueError("optimizer success count exceeds executed count")
        if self.evaluable_count > self.executed_count:
            raise ValueError("evaluable count exceeds executed count")
        if self.local_success_count > self.evaluable_count:
            raise ValueError("local success count exceeds evaluable count")
        if self.local_success_count > self.optimizer_reported_success_count:
            raise ValueError(
                "local success count exceeds optimizer-reported success count"
            )
        if self.executed_count == 0:
            if self.selected_start_index is not None or self.selection_kind is not None:
                raise ValueError("empty execution has no selected start")
        else:
            if self.selected_start_index is None or self.selection_kind not in {
                "local_success",
                "failure_representative",
            }:
                raise ValueError("executed starts require one representative")
            if self.selected_start_index >= self.generated_count:
                raise ValueError("selected_start_index is outside generated starts")
            if (self.selection_kind == "local_success") != (self.local_success_count > 0):
                raise ValueError("selection_kind contradicts local success count")


@dataclass(frozen=True, slots=True)
class PerExpiryMetric:
    maturity_id: str
    time_to_expiry: float
    raw_node_count: int
    node_count: int
    k_min: float
    k_max: float
    rmse_total_variance: float | None
    nrmse_total_variance: float | None
    rmse_iv: float | None
    checks: dict[str, CheckDiagnostic]

    def __post_init__(self) -> None:
        _require_nonempty_string(self.maturity_id, "maturity_id")
        _require_finite(self.time_to_expiry, "time_to_expiry", positive=True)
        _require_count(self.raw_node_count, "raw_node_count")
        _require_count(self.node_count, "node_count")
        if self.node_count > self.raw_node_count:
            raise ValueError("node_count cannot exceed raw_node_count")
        _require_finite(self.k_min, "k_min")
        _require_finite(self.k_max, "k_max")
        if self.k_min >= self.k_max:
            raise ValueError("k support must have positive width")
        for name in ("rmse_total_variance", "nrmse_total_variance", "rmse_iv"):
            _require_finite(getattr(self, name), name, nullable=True)
            if getattr(self, name) is not None and getattr(self, name) < 0:
                raise ValueError(f"{name} cannot be negative")
        _require_checks(self.checks, "checks")


@dataclass(frozen=True, slots=True)
class FitAttemptDiagnostic:
    attempt_id: str
    parent_attempt_id: str | None
    scope: AttemptScope
    product: str
    timestamp: str
    maturity_id: str | None
    participating_maturities: list[str]
    time_to_expiry: float | None
    method: FitMethod
    attempt_order: int
    attempt_status: AttemptStatus
    optimizer_attempted: bool
    optimizer_success: bool | None
    optimizer_start_summary: OptimizerStartSummary | None
    selection_eligible: bool
    blocked_by_parent: bool
    local_success: bool
    success: bool
    parameters: dict[str, Any] | None
    per_expiry_metrics: dict[str, PerExpiryMetric] | None
    rmse_total_variance: float | None
    nrmse_total_variance: float | None
    rmse_iv: float | None
    raw_node_count: int | None
    node_count: int | None
    k_min: float | None
    k_max: float | None
    candidate_k: list[float]
    candidate_total_variance: list[float | None]
    candidate_iv: list[float | None]
    checks: dict[str, CheckDiagnostic]
    failure_code: str | None
    failure_reason: str | None
    policy_version: str
    forward_source: ForwardSource

    def __post_init__(self) -> None:
        _require_attempt_id(self.attempt_id, "attempt_id")
        _require_attempt_id(self.parent_attempt_id, "parent_attempt_id", nullable=True)
        _require_enum(self.scope, AttemptScope, "scope")
        _require_nonempty_string(self.product, "product")
        _require_local_timestamp(self.timestamp)
        _require_enum(self.method, FitMethod, "method")
        _require_count(self.attempt_order, "attempt_order")
        _require_enum(self.attempt_status, AttemptStatus, "attempt_status")
        _require_enum(self.forward_source, ForwardSource, "forward_source")
        _require_nonempty_string(self.policy_version, "policy_version")
        for name in (
            "optimizer_attempted",
            "selection_eligible",
            "blocked_by_parent",
            "local_success",
            "success",
        ):
            if type(getattr(self, name)) is not bool:
                raise ValueError(f"{name} must be bool")
        if self.optimizer_success is not None and type(self.optimizer_success) is not bool:
            raise ValueError("optimizer_success must be bool or null")
        _require_failure_code(self.failure_code, nullable=True)
        if self.failure_code is not None and self.failure_code not in ATTEMPT_FAILURE_CODES:
            raise ValueError("failure_code is not valid for a fit attempt")
        if self.failure_code is not None and self.failure_code not in METHOD_FAILURE_CODES[
            self.method
        ]:
            raise ValueError("failure_code is not valid for this fit method")
        if self.failure_reason is not None:
            _require_nonempty_string(self.failure_reason, "failure_reason")
        _require_checks(self.checks, "checks")

        if self.scope is AttemptScope.TIMESTAMP:
            if self.method is not FitMethod.SSVI:
                raise ValueError("timestamp attempts are SSVI parents")
            if any(
                value is not None
                for value in (
                    self.maturity_id,
                    self.time_to_expiry,
                    self.rmse_total_variance,
                    self.nrmse_total_variance,
                    self.rmse_iv,
                    self.raw_node_count,
                    self.node_count,
                    self.k_min,
                    self.k_max,
                )
            ):
                raise ValueError("SSVI parent single-expiry fields must be null")
            if not self.participating_maturities or not all(
                isinstance(item, str) and item for item in self.participating_maturities
            ):
                raise ValueError("SSVI parent requires participating maturities")
            if not isinstance(self.per_expiry_metrics, dict):
                raise ValueError("SSVI parent requires per-expiry metrics")
            if self.parent_attempt_id is not None or self.blocked_by_parent:
                raise ValueError("SSVI parent cannot be parent-blocked")
            if self.selection_eligible:
                raise ValueError("SSVI parent is not an expiry selection candidate")
            if self.candidate_k or self.candidate_total_variance or self.candidate_iv:
                raise ValueError("SSVI parent cannot contain mixed-expiry arrays")
        else:
            _require_nonempty_string(self.maturity_id, "maturity_id")
            _require_finite(self.time_to_expiry, "time_to_expiry", positive=True)
            if self.participating_maturities:
                raise ValueError("expiry attempts cannot list participating maturities")
            if self.per_expiry_metrics is not None:
                raise ValueError("expiry attempts cannot contain per-expiry metrics")
            for name in ("raw_node_count", "node_count"):
                _require_count(getattr(self, name), name, nullable=True)
            for name in ("k_min", "k_max"):
                _require_finite(getattr(self, name), name, nullable=True)
            if (self.k_min is None) != (self.k_max is None):
                raise ValueError("k support bounds must be both present or both null")
            if self.k_min is not None and self.k_min >= self.k_max:
                raise ValueError("k support must have positive width")
            if self.method is FitMethod.SSVI:
                if self.parent_attempt_id is None:
                    raise ValueError("SSVI child must reference its parent")
                if (
                    self.failure_code is not None
                    and self.failure_code not in SSVI_CHILD_FAILURE_CODES
                ):
                    raise ValueError(
                        "SSVI child failure code is outside its closed expiry set"
                    )
            elif self.parent_attempt_id is not None:
                raise ValueError("only SSVI child attempts have a parent_attempt_id")

        for name in ("rmse_total_variance", "nrmse_total_variance", "rmse_iv"):
            _require_finite(getattr(self, name), name, nullable=True)
        _require_finite_sequence(self.candidate_k, "candidate_k", strictly_increasing=True)
        _require_finite_sequence(
            self.candidate_total_variance,
            "candidate_total_variance",
            nullable_items=True,
        )
        _require_finite_sequence(self.candidate_iv, "candidate_iv", nullable_items=True)
        if not (
            len(self.candidate_k)
            == len(self.candidate_total_variance)
            == len(self.candidate_iv)
        ):
            raise ValueError("candidate arrays must have equal lengths")

        if self.parameters is not None:
            if not isinstance(self.parameters, dict):
                raise ValueError("parameters must be an object or null")
            _require_parameter_scalars(self.parameters, "parameters")
        if self.method in {FitMethod.PCHIP, FitMethod.LINEAR}:
            if self.parameters is not None:
                raise ValueError("non-parametric methods have null parameters")
        elif self.parameters is not None:
            expected = (
                {"rho", "eta", "gamma", "theta_by_maturity"}
                if self.scope is AttemptScope.TIMESTAMP
                else {"rho", "eta", "gamma", "theta"}
                if self.method is FitMethod.SSVI
                else {"a", "b", "rho", "m", "sigma"}
            )
            if set(self.parameters) != expected:
                raise ValueError("parameters do not match the closed method schema")

        if self.optimizer_attempted:
            if self.optimizer_success is None or not isinstance(
                self.optimizer_start_summary, OptimizerStartSummary
            ):
                raise ValueError("optimizer attempts require success and start summary")
            if (
                self.optimizer_success
                and self.optimizer_start_summary.optimizer_reported_success_count
                == 0
            ):
                raise ValueError(
                    "selected optimizer success requires a reported successful start"
                )
            has_rmse_payload = any(
                value is not None
                for value in (
                    self.rmse_total_variance,
                    self.nrmse_total_variance,
                    self.rmse_iv,
                )
            )
            has_local_check_payload = any(
                check.status is not CheckStatus.NOT_APPLICABLE
                or check.reason_code != "not_run"
                for name, check in self.checks.items()
                if name != "calendar_consistent"
            )
            if self.scope is AttemptScope.TIMESTAMP:
                assert self.per_expiry_metrics is not None
                has_rmse_payload = any(
                    value is not None
                    for metric in self.per_expiry_metrics.values()
                    for value in (
                        metric.rmse_total_variance,
                        metric.nrmse_total_variance,
                        metric.rmse_iv,
                    )
                )
                has_local_check_payload = any(
                    check.status is not CheckStatus.NOT_APPLICABLE
                    or check.reason_code != "not_run"
                    for metric in self.per_expiry_metrics.values()
                    for name, check in metric.checks.items()
                    if name != "calendar_consistent"
                )
                if self.parameters is None:
                    if self.optimizer_start_summary.evaluable_count != 0:
                        raise ValueError(
                            "SSVI parent without a representative payload has zero "
                            "evaluable starts"
                        )
                    if has_rmse_payload or any(
                        check.status is not CheckStatus.NOT_APPLICABLE
                        or check.reason_code != "not_run"
                        for metric in self.per_expiry_metrics.values()
                        for check in metric.checks.values()
                    ):
                        raise ValueError(
                            "SSVI parent without parameters requires null RMSE and "
                            "not_run per-expiry checks"
                        )
                    if any(
                        check.status is not CheckStatus.NOT_APPLICABLE
                        or check.reason_code != "not_run"
                        for check in self.checks.values()
                    ):
                        raise ValueError(
                            "SSVI parent without parameters requires not_run parent checks"
                        )
            has_candidate_payload = bool(
                self.candidate_k
                or self.candidate_total_variance
                or self.candidate_iv
            )
            has_evaluable_payload = (
                has_rmse_payload
                or has_candidate_payload
                or has_local_check_payload
            )
            if has_evaluable_payload:
                if self.optimizer_start_summary.evaluable_count == 0:
                    raise ValueError(
                        "optimizer representative payload requires an evaluable start"
                    )
                if self.parameters is None:
                    raise ValueError(
                        "optimizer representative payload requires parameters"
                    )
            if (
                self.method is FitMethod.RAW_SVI
                and (self.optimizer_start_summary.evaluable_count > 0)
                != has_evaluable_payload
            ):
                raise ValueError(
                    "Raw-SVI evaluable starts must match its representative payload"
                )
            if self.failure_code == "non_finite_parameters" and (
                self.optimizer_start_summary.evaluable_count != 0
                or has_evaluable_payload
            ):
                raise ValueError(
                    "non_finite_parameters cannot retain evaluable payload"
                )
            if self.failure_code == "optimizer_exception" and (
                self.parameters is not None
                or self.optimizer_start_summary.evaluable_count != 0
            ):
                raise ValueError(
                    "optimizer exception requires null parameters and zero evaluable starts"
                )
            requires_evaluable_parameters = self.success or self.failure_code in {
                "parameter_constraint_failed",
                "rmse_exceeded",
                "non_positive_total_variance",
                "call_price_monotonicity_failed",
                "call_price_convexity_failed",
                "butterfly_failed",
                "abnormal_jump",
                "check_resolution_limit",
                "calendar_conflict",
            }
            if requires_evaluable_parameters and (
                self.parameters is None
                or self.optimizer_start_summary.evaluable_count == 0
            ):
                raise ValueError(
                    "late-stage optimizer result requires parameters and an "
                    "evaluable start"
                )
            selected_local = (
                self.optimizer_start_summary.selection_kind == "local_success"
            )
            sampling_failure_override = (
                self.scope is AttemptScope.EXPIRY
                and self.method is FitMethod.RAW_SVI
                and selected_local
                and self.optimizer_success is True
                and not self.local_success
                and self.attempt_status is AttemptStatus.FAILED
                and self.selection_eligible
                and not self.blocked_by_parent
                and self.parameters is not None
                and not self.candidate_k
                and not self.candidate_total_variance
                and not self.candidate_iv
                and self.failure_code == "check_resolution_limit"
                and self.failure_reason == "diagnostic candidate sampling failed"
                and self.checks["positive_total_variance"].status
                is CheckStatus.INDETERMINATE
                and self.checks["positive_total_variance"].reason_code
                == "resolution_limit"
                and all(
                    self.checks[name].status is CheckStatus.NOT_APPLICABLE
                    and self.checks[name].reason_code == "not_run"
                    for name in (
                        "call_price_monotonic",
                        "call_price_convex",
                        "butterfly_g_nonnegative",
                        "calendar_consistent",
                        "jump_reliable",
                    )
                )
            )
            if self.local_success != selected_local and not sampling_failure_override:
                raise ValueError("local_success contradicts selected optimizer start")
            if self.local_success and not self.optimizer_success:
                raise ValueError("a locally successful optimizer result must report success")
        elif self.optimizer_success is not None or self.optimizer_start_summary is not None:
            raise ValueError("non-optimizer attempts use null optimizer fields")

        if self.failure_code == "rmse_exceeded":
            has_nrmse_payload = (
                any(
                    metric.nrmse_total_variance is not None
                    for metric in self.per_expiry_metrics.values()
                )
                if self.scope is AttemptScope.TIMESTAMP
                else self.nrmse_total_variance is not None
            )
            if not has_nrmse_payload:
                raise ValueError("rmse_exceeded requires normalized RMSE payload")

        if self.method is FitMethod.RAW_SVI and not self.optimizer_attempted:
            raise ValueError("Raw-SVI always enters the multi-start optimizer")
        if self.method in {FitMethod.PCHIP, FitMethod.LINEAR} and self.optimizer_attempted:
            raise ValueError("non-parametric methods do not run the optimizer")
        if self.method is FitMethod.SSVI and self.scope is AttemptScope.EXPIRY:
            if self.optimizer_attempted:
                raise ValueError("SSVI child diagnostics do not run an optimizer")
        if (
            self.method is FitMethod.SSVI
            and self.scope is AttemptScope.TIMESTAMP
            and self.attempt_status is not AttemptStatus.SKIPPED
            and not self.optimizer_attempted
        ):
            raise ValueError("eligible SSVI parents enter the multi-start optimizer")

        if self.success != (self.attempt_status is AttemptStatus.ACCEPTED):
            raise ValueError("success is equivalent to accepted status")
        if self.success:
            if not self.local_success or self.failure_code is not None or self.failure_reason is not None:
                raise ValueError("accepted attempts must be locally successful without failure")
        elif self.failure_code is None:
            raise ValueError("unsuccessful attempts require failure_code")
        if self.blocked_by_parent:
            if (
                self.method is not FitMethod.SSVI
                or self.scope is not AttemptScope.EXPIRY
                or self.selection_eligible
                or self.attempt_status is not AttemptStatus.FAILED
            ):
                raise ValueError("blocked_by_parent is only valid for failed SSVI children")
        elif not self.selection_eligible and self.scope is not AttemptScope.TIMESTAMP:
            raise ValueError("non-parent expiry candidates are selection eligible")
        if self.attempt_status is AttemptStatus.SKIPPED:
            if not (
                self.scope is AttemptScope.TIMESTAMP
                and self.method is FitMethod.SSVI
                and not self.optimizer_attempted
                and self.optimizer_success is None
                and self.optimizer_start_summary is None
                and not self.selection_eligible
                and not self.blocked_by_parent
                and not self.local_success
                and not self.success
                and self.failure_code == "not_enough_maturities"
                and self.parameters is None
                and all(
                    check.status is CheckStatus.NOT_APPLICABLE
                    and check.reason_code == "not_run"
                    for check in self.checks.values()
                )
            ):
                raise ValueError("only an ineligible SSVI timestamp parent can be skipped")
        elif self.failure_code == "not_enough_maturities":
            raise ValueError("not_enough_maturities requires skipped SSVI parent status")
        if self.optimizer_attempted:
            if self.optimizer_success is False and self.failure_code not in {
                "optimizer_failed",
                "optimizer_exception",
            }:
                raise ValueError("optimizer failure must be the primary failure code")
            if self.optimizer_success is True and self.failure_code in {
                "optimizer_failed",
                "optimizer_exception",
            }:
                raise ValueError("successful optimizer representative cannot use optimizer failure")
        elif self.failure_code in {"optimizer_failed", "optimizer_exception"}:
            raise ValueError("non-optimizer attempts cannot use optimizer failure codes")
        if self.failure_code == "calendar_conflict" and not self.local_success:
            raise ValueError("calendar-stage failures preserve local_success")
        if self.failure_code == "parent_ssvi_rejected" and not (
            self.blocked_by_parent and self.local_success
        ):
            raise ValueError("parent_ssvi_rejected requires a locally successful blocked child")
        if self.blocked_by_parent and self.local_success and (
            self.failure_code != "parent_ssvi_rejected"
        ):
            raise ValueError("locally successful blocked child uses parent_ssvi_rejected")
        if self.local_success and not self.success and self.failure_code not in {
            "parent_ssvi_rejected",
            "calendar_conflict",
            "check_resolution_limit",
        }:
            raise ValueError("locally successful failure must occur at parent or calendar stage")
        expected_failed_check = FAILURE_CODE_CHECK.get(self.failure_code)
        if expected_failed_check is not None and (
            self.checks[expected_failed_check].status is not CheckStatus.FAILED
        ):
            raise ValueError("failure_code requires its corresponding failed check")
        if self.failure_code == "check_resolution_limit":
            resolution_checks = (
                ("calendar_consistent",)
                if self.local_success
                else (
                    "positive_total_variance",
                    "call_price_monotonic",
                    "call_price_convex",
                    "butterfly_g_nonnegative",
                    "jump_reliable",
                )
                if self.method in {FitMethod.SSVI, FitMethod.RAW_SVI}
                else (
                    "positive_total_variance",
                    "call_price_monotonic",
                    "call_price_convex",
                    "jump_reliable",
                )
            )
            if not any(
                self.checks[name].status is CheckStatus.INDETERMINATE
                and self.checks[name].reason_code == "resolution_limit"
                for name in resolution_checks
            ):
                raise ValueError("check_resolution_limit requires an applicable unreliable check")
        butterfly = self.checks["butterfly_g_nonnegative"]
        if self.method in {FitMethod.PCHIP, FitMethod.LINEAR}:
            if not (
                butterfly.status is CheckStatus.NOT_APPLICABLE
                and butterfly.reason_code == "method_has_no_analytic_g"
            ):
                raise ValueError(
                    "non-parametric butterfly check must report method_has_no_analytic_g"
                )
        elif (
            butterfly.status is CheckStatus.NOT_APPLICABLE
            and butterfly.reason_code == "method_has_no_analytic_g"
        ):
            raise ValueError("parameter methods have an analytic butterfly check")

        applicable_local_checks = [
            "positive_total_variance",
            "call_price_monotonic",
            "call_price_convex",
            "jump_reliable",
        ]
        if self.method in {FitMethod.SSVI, FitMethod.RAW_SVI}:
            applicable_local_checks.append("butterfly_g_nonnegative")
        if self.local_success and any(
            self.checks[name].status is not CheckStatus.PASSED
            for name in applicable_local_checks
        ):
            raise ValueError("local_success requires every applicable local hard check to pass")

        if self.success:
            calendar = self.checks["calendar_consistent"]
            valid_calendar_state = (
                calendar.status is CheckStatus.PASSED
                or (
                    calendar.status is CheckStatus.NOT_APPLICABLE
                    and calendar.reason_code == "no_prior_maturity"
                )
                or (
                    calendar.status is CheckStatus.NOT_TESTABLE
                    and calendar.reason_code == "no_overlap"
                )
            )
            if not valid_calendar_state:
                raise ValueError("accepted attempt has an invalid calendar check state")

        first_check_failure_code = None
        for check_name in HARD_GATE_CHECK_ORDER:
            if (
                check_name == "butterfly_g_nonnegative"
                and self.method in {FitMethod.PCHIP, FitMethod.LINEAR}
            ):
                continue
            status = self.checks[check_name].status
            if status is CheckStatus.FAILED:
                first_check_failure_code = CHECK_FAILURE_CODE[check_name]
                break
            if status is CheckStatus.INDETERMINATE:
                first_check_failure_code = "check_resolution_limit"
                break
        check_gate_failure_codes = frozenset(CHECK_FAILURE_CODE.values()) | {
            "check_resolution_limit"
        }
        if (
            self.failure_code in check_gate_failure_codes
            and self.failure_code != first_check_failure_code
        ):
            raise ValueError(
                "failure_code must identify the first failed or indeterminate hard gate"
            )


@dataclass(frozen=True, slots=True)
class ExpiryFitResult:
    maturity_id: str
    time_to_expiry: float
    result_status: ResultStatus
    method: FinalMethod
    success: bool
    usable: bool
    raw_k: list[float]
    raw_total_variance: list[float]
    raw_iv: list[float]
    fit_k: list[float]
    fit_total_variance: list[float]
    fit_iv: list[float]
    selected_attempt_id: str | None
    last_candidate_attempt_id: str | None
    terminal_attempt_id: str | None
    attempt_ids: list[str]
    final_checks: dict[str, CheckDiagnostic]
    failure_code: str | None
    failure_reason: str | None

    def __post_init__(self) -> None:
        _require_nonempty_string(self.maturity_id, "maturity_id")
        _require_finite(self.time_to_expiry, "time_to_expiry", positive=True)
        _require_enum(self.result_status, ResultStatus, "result_status")
        _require_enum(self.method, FinalMethod, "method")
        if type(self.success) is not bool or type(self.usable) is not bool:
            raise ValueError("success and usable must be bool")
        if self.success != self.usable:
            raise ValueError("success and usable must be equal")
        _require_finite_sequence(self.raw_k, "raw_k", strictly_increasing=True)
        _require_finite_sequence(self.raw_total_variance, "raw_total_variance")
        _require_finite_sequence(self.raw_iv, "raw_iv")
        _require_finite_sequence(self.fit_k, "fit_k", strictly_increasing=True)
        _require_finite_sequence(self.fit_total_variance, "fit_total_variance")
        _require_finite_sequence(self.fit_iv, "fit_iv")
        if not (len(self.raw_k) == len(self.raw_total_variance) == len(self.raw_iv)):
            raise ValueError("raw arrays must have equal lengths")
        if not (len(self.fit_k) == len(self.fit_total_variance) == len(self.fit_iv)):
            raise ValueError("fit arrays must have equal lengths")
        for owner, value in (
            ("selected_attempt_id", self.selected_attempt_id),
            ("last_candidate_attempt_id", self.last_candidate_attempt_id),
            ("terminal_attempt_id", self.terminal_attempt_id),
        ):
            _require_attempt_id(value, owner, nullable=True)
        if not isinstance(self.attempt_ids, list) or len(set(self.attempt_ids)) != len(
            self.attempt_ids
        ):
            raise ValueError("attempt_ids must be a unique ordered list")
        for attempt_id in self.attempt_ids:
            _require_attempt_id(attempt_id, "attempt_ids item")
        for reference in (
            self.selected_attempt_id,
            self.last_candidate_attempt_id,
            self.terminal_attempt_id,
        ):
            if reference is not None and reference not in self.attempt_ids:
                raise ValueError("attempt reference is not present in attempt_ids")
        _require_checks(self.final_checks, "final_checks")
        _require_failure_code(self.failure_code, nullable=True)
        if self.failure_reason is not None:
            _require_nonempty_string(self.failure_reason, "failure_reason")

        if self.usable:
            if (
                self.result_status is not ResultStatus.USABLE
                or self.method is FinalMethod.UNUSABLE
                or self.selected_attempt_id is None
                or self.terminal_attempt_id != self.selected_attempt_id
                or self.failure_code is not None
                or self.failure_reason is not None
                or not self.fit_k
            ):
                raise ValueError("usable result violates its closed truth table")
        elif (
            self.result_status is not ResultStatus.UNUSABLE
            or self.method is not FinalMethod.UNUSABLE
            or self.selected_attempt_id is not None
            or self.failure_code is None
            or self.fit_k
            or self.fit_total_variance
            or self.fit_iv
        ):
            raise ValueError("unusable result violates its closed truth table")
        if self.terminal_attempt_id is None and self.failure_code != "insufficient_nodes":
            raise ValueError("only insufficient nodes can have no terminal attempt")
        if self.failure_code == "insufficient_nodes" and self.terminal_attempt_id is not None:
            raise ValueError("insufficient nodes has no terminal attempt")
        if self.failure_code == "insufficient_nodes":
            if (
                len(self.raw_k) >= 2
                or self.selected_attempt_id is not None
                or self.last_candidate_attempt_id is not None
                or self.terminal_attempt_id is not None
                or self.attempt_ids
                or any(
                    check.status is not CheckStatus.NOT_APPLICABLE
                    or check.reason_code != "not_run"
                    for check in self.final_checks.values()
                )
            ):
                raise ValueError("insufficient nodes requires an empty candidate history")


@dataclass(frozen=True, slots=True)
class InputQuality:
    input_row_count: int
    valid_premerge_node_count: int
    merged_node_count: int
    excluded_counts: dict[str, int]

    def __post_init__(self) -> None:
        for name in (
            "input_row_count",
            "valid_premerge_node_count",
            "merged_node_count",
        ):
            _require_count(getattr(self, name), name)
        if not isinstance(self.excluded_counts, dict) or set(self.excluded_counts) != set(
            INPUT_FAILURE_CODES
        ):
            raise ValueError("excluded_counts must contain the six closed input codes")
        for code, count in self.excluded_counts.items():
            _require_count(count, f"excluded_counts[{code}]")
        if self.input_row_count != self.valid_premerge_node_count + sum(
            self.excluded_counts.values()
        ):
            raise ValueError("input quality counts do not reconcile")
        if self.merged_node_count > self.valid_premerge_node_count:
            raise ValueError("merged_node_count exceeds valid pre-merge nodes")


@dataclass(frozen=True, slots=True)
class CalendarPairDiagnostic:
    pair_check_id: str
    phase: Literal["ssvi_parent", "expiry_selection"]
    earlier_maturity_id: str
    later_maturity_id: str
    earlier_attempt_id: str | None
    later_attempt_id: str | None
    parent_attempt_id: str | None
    common_k_min: float | None
    common_k_max: float | None
    check: CheckDiagnostic

    def __post_init__(self) -> None:
        _require_pair_id(self.pair_check_id)
        if self.phase not in {"ssvi_parent", "expiry_selection"}:
            raise ValueError("phase is outside the closed set")
        _require_nonempty_string(self.earlier_maturity_id, "earlier_maturity_id")
        _require_nonempty_string(self.later_maturity_id, "later_maturity_id")
        if self.earlier_maturity_id == self.later_maturity_id:
            raise ValueError("calendar pair maturities must differ")
        for owner, value in (
            ("earlier_attempt_id", self.earlier_attempt_id),
            ("later_attempt_id", self.later_attempt_id),
            ("parent_attempt_id", self.parent_attempt_id),
        ):
            _require_attempt_id(value, owner, nullable=True)
        if not isinstance(self.check, CheckDiagnostic) or self.check.name != "calendar_consistent":
            raise ValueError("calendar pair requires calendar_consistent check")
        _require_finite(self.common_k_min, "common_k_min", nullable=True)
        _require_finite(self.common_k_max, "common_k_max", nullable=True)
        if (self.common_k_min is None) != (self.common_k_max is None):
            raise ValueError("common support bounds must be both present or both null")
        if self.common_k_min is not None and self.common_k_min >= self.common_k_max:
            raise ValueError("common support must have positive width")
        if self.check.status in {CheckStatus.NOT_APPLICABLE, CheckStatus.NOT_TESTABLE}:
            if self.common_k_min is not None:
                raise ValueError("unevaluated pair has null common support")
        elif self.common_k_min is None:
            raise ValueError("evaluated calendar pair requires common support bounds")
        if self.phase == "ssvi_parent":
            if self.parent_attempt_id is None:
                raise ValueError("SSVI parent pairs reference their parent")
            if (self.earlier_attempt_id is None) != (self.later_attempt_id is None):
                raise ValueError("SSVI pair child references are both present or both null")
            if self.earlier_attempt_id is None and not (
                self.check.status is CheckStatus.NOT_APPLICABLE
                and self.check.reason_code == "not_run"
            ):
                raise ValueError("missing SSVI children require not_run")
            if (
                self.earlier_attempt_id is not None
                and self.check.status is CheckStatus.NOT_APPLICABLE
                and self.check.reason_code != "not_run"
            ):
                raise ValueError("unevaluated SSVI child pairs require not_run")
        else:
            if (
                self.parent_attempt_id is not None
                or self.earlier_attempt_id is None
                or self.later_attempt_id is None
            ):
                raise ValueError("expiry-selection pairs require both expiry attempts only")
            if self.check.status is CheckStatus.NOT_APPLICABLE:
                raise ValueError("expiry-selection pairs cannot be not_applicable")


@dataclass(frozen=True, slots=True)
class TimestampSurfaceDiagnostic:
    product: str
    timestamp: str
    diagnostic_only: Literal[True]
    timestamp_status: TimestampStatus
    timestamp_failure_code: str | None
    timestamp_failure_reason: str | None
    forward_source: ForwardSource | None
    observed_forward_sources: list[ForwardSource]
    input_quality: InputQuality
    ssvi_attempt: str | None
    attempts: list[FitAttemptDiagnostic]
    expiry_results: list[ExpiryFitResult]
    surface_grid_status: SurfaceGridStatus
    surface_log_moneyness: list[float]
    surface_time_to_expiry: list[float]
    surface_total_variance: list[list[float | None]]
    surface_iv: list[list[float | None]]
    usable_expiry_count: int
    unusable_expiry_count: int
    calendar_pair_checks: list[CalendarPairDiagnostic]
    method_counts: dict[FinalMethod, int]
    overall_status: OverallStatus
    policy_version: str
    effective_input_fingerprint: str
    input_quality_fingerprint: str
    input_fingerprint: str

    def __post_init__(self) -> None:
        _require_nonempty_string(self.product, "product")
        _require_local_timestamp(self.timestamp)
        if self.diagnostic_only is not True:
            raise ValueError("diagnostic_only must be literal true")
        _require_enum(self.timestamp_status, TimestampStatus, "timestamp_status")
        _require_enum(self.surface_grid_status, SurfaceGridStatus, "surface_grid_status")
        _require_enum(self.overall_status, OverallStatus, "overall_status")
        _require_nonempty_string(self.policy_version, "policy_version")
        for owner, value in (
            ("effective_input_fingerprint", self.effective_input_fingerprint),
            ("input_quality_fingerprint", self.input_quality_fingerprint),
            ("input_fingerprint", self.input_fingerprint),
        ):
            _require_fingerprint(value, owner)
        if not isinstance(self.input_quality, InputQuality):
            raise ValueError("input_quality must be InputQuality")
        if self.forward_source is not None:
            _require_enum(self.forward_source, ForwardSource, "forward_source")
        if not isinstance(self.observed_forward_sources, list) or any(
            not isinstance(item, ForwardSource) for item in self.observed_forward_sources
        ):
            raise ValueError("observed_forward_sources must contain ForwardSource values")
        expected_observed = [
            source for source in ForwardSource if source in self.observed_forward_sources
        ]
        if self.observed_forward_sources != expected_observed:
            raise ValueError("observed forward sources must be unique enum order")
        _require_attempt_id(self.ssvi_attempt, "ssvi_attempt", nullable=True)
        _require_count(self.usable_expiry_count, "usable_expiry_count")
        _require_count(self.unusable_expiry_count, "unusable_expiry_count")
        if set(self.method_counts) != set(FinalMethod):
            raise ValueError("method_counts must contain all five final methods")
        for method, count in self.method_counts.items():
            _require_enum(method, FinalMethod, "method_counts key")
            _require_count(count, f"method_counts[{method.value}]")

        if self.timestamp_status is TimestampStatus.FAILED_INPUT:
            if (
                self.timestamp_failure_code != "mixed_forward_sources"
                or self.forward_source is not None
                or len(self.observed_forward_sources) < 2
                or self.input_quality.valid_premerge_node_count == 0
                or self.input_quality.merged_node_count != 0
                or self.attempts
                or self.expiry_results
                or self.calendar_pair_checks
                or self.surface_grid_status is not SurfaceGridStatus.UNAVAILABLE_INPUT_FAILURE
                or self.surface_log_moneyness
                or self.surface_time_to_expiry
                or self.surface_total_variance
                or self.surface_iv
                or self.usable_expiry_count
                or self.unusable_expiry_count
            ):
                raise ValueError("failed_input state violates its closed truth table")
            expected_reason = "mixed forward sources: " + ",".join(
                source.value for source in self.observed_forward_sources
            )
            if self.timestamp_failure_reason != expected_reason:
                raise ValueError("mixed source failure reason is not canonical")
        elif (
            self.timestamp_failure_code is not None
            or self.timestamp_failure_reason is not None
            or self.surface_grid_status is SurfaceGridStatus.UNAVAILABLE_INPUT_FAILURE
        ):
            raise ValueError("ready timestamps have no timestamp failure")
        elif self.input_quality.valid_premerge_node_count == 0:
            if (
                self.input_quality.merged_node_count != 0
                or self.forward_source is not None
                or self.observed_forward_sources
            ):
                raise ValueError("ready timestamp without valid nodes has no forward source")
        elif (
            self.input_quality.merged_node_count == 0
            or len(self.observed_forward_sources) != 1
            or self.forward_source is not self.observed_forward_sources[0]
        ):
            raise ValueError("ready valid nodes require one matching forward source")

        if not isinstance(self.attempts, list) or any(
            not isinstance(item, FitAttemptDiagnostic) for item in self.attempts
        ):
            raise ValueError("attempts must contain FitAttemptDiagnostic values")
        if [item.attempt_order for item in self.attempts] != list(range(len(self.attempts))):
            raise ValueError("attempt_order must be unique, continuous, and ordered")
        attempt_by_id = {item.attempt_id: item for item in self.attempts}
        if len(attempt_by_id) != len(self.attempts):
            raise ValueError("attempt_id values must be unique")
        for attempt in self.attempts:
            if (
                attempt.product != self.product
                or attempt.timestamp != self.timestamp
                or attempt.policy_version != self.policy_version
            ):
                raise ValueError("attempt identity context must match its timestamp")
            expected_attempt_id = make_attempt_id(
                input_fingerprint=self.input_fingerprint,
                product=self.product,
                timestamp=self.timestamp,
                scope=attempt.scope,
                maturity_id=attempt.maturity_id,
                participating_maturities=attempt.participating_maturities,
                method=attempt.method,
                attempt_order=attempt.attempt_order,
                policy_version=self.policy_version,
            )
            if attempt.attempt_id != expected_attempt_id:
                raise ValueError("attempt_id does not match its canonical identity payload")
        if self.ssvi_attempt is not None:
            parent = attempt_by_id.get(self.ssvi_attempt)
            if parent is None or parent.scope is not AttemptScope.TIMESTAMP:
                raise ValueError("ssvi_attempt must reference the SSVI parent")

        if not isinstance(self.expiry_results, list) or any(
            not isinstance(item, ExpiryFitResult) for item in self.expiry_results
        ):
            raise ValueError("expiry_results must contain ExpiryFitResult values")
        expiry_times = [item.time_to_expiry for item in self.expiry_results]
        if any(later <= earlier for earlier, later in zip(expiry_times, expiry_times[1:])):
            raise ValueError("expiry results must be strictly increasing in T")
        for result in self.expiry_results:
            if not set(result.attempt_ids).issubset(attempt_by_id):
                raise ValueError("expiry result references an unknown attempt")
            expected_attempts = [
                attempt
                for attempt in self.attempts
                if attempt.scope is AttemptScope.EXPIRY
                and attempt.maturity_id == result.maturity_id
            ]
            if result.attempt_ids != [attempt.attempt_id for attempt in expected_attempts]:
                raise ValueError("expiry result must reference every same-expiry attempt in order")
            for attempt in expected_attempts:
                if attempt.time_to_expiry != result.time_to_expiry:
                    raise ValueError("expiry attempt T must match its result")
            candidate_attempts = [
                attempt for attempt in expected_attempts if attempt.candidate_k
            ]
            expected_last_candidate = (
                candidate_attempts[-1].attempt_id if candidate_attempts else None
            )
            if result.last_candidate_attempt_id != expected_last_candidate:
                raise ValueError("last_candidate_attempt_id does not reference the last curve")
            if result.usable:
                selected = attempt_by_id[result.selected_attempt_id]
                selectable_attempts = [
                    attempt for attempt in expected_attempts if attempt.selection_eligible
                ]
                if (
                    selected.attempt_status is not AttemptStatus.ACCEPTED
                    or not selected.success
                    or not selectable_attempts
                    or selected is not selectable_attempts[-1]
                    or selected.method.value != result.method.value
                    or selected.maturity_id != result.maturity_id
                    or selected.time_to_expiry != result.time_to_expiry
                ):
                    raise ValueError(
                        "selected attempt must be the final accepted selection candidate"
                    )
                if result.final_checks != selected.checks:
                    raise ValueError("usable final_checks must copy the selected attempt")
                if (
                    result.fit_k != selected.candidate_k
                    or result.fit_total_variance != selected.candidate_total_variance
                    or result.fit_iv != selected.candidate_iv
                ):
                    raise ValueError("usable fit arrays must copy the selected candidate")
            elif result.terminal_attempt_id is not None:
                terminal = attempt_by_id[result.terminal_attempt_id]
                selectable_attempts = [
                    attempt for attempt in expected_attempts if attempt.selection_eligible
                ]
                if (
                    not selectable_attempts
                    or terminal is not selectable_attempts[-1]
                    or terminal.maturity_id != result.maturity_id
                    or terminal.time_to_expiry != result.time_to_expiry
                ):
                    raise ValueError("terminal attempt is not the last executed expiry candidate")
                if (
                    result.final_checks != terminal.checks
                    or result.failure_code != terminal.failure_code
                    or result.failure_reason != terminal.failure_reason
                ):
                    raise ValueError("unusable result must copy the terminal attempt failure")
        usable_count = sum(item.usable for item in self.expiry_results)
        unusable_count = len(self.expiry_results) - usable_count
        if (self.usable_expiry_count, self.unusable_expiry_count) != (
            usable_count,
            unusable_count,
        ):
            raise ValueError("expiry usability counts do not reconcile")
        if sum(self.method_counts.values()) != len(self.expiry_results):
            raise ValueError("method counts do not reconcile")
        expected_method_counts = {
            method: sum(result.method is method for result in self.expiry_results)
            for method in FinalMethod
        }
        if self.method_counts != expected_method_counts:
            raise ValueError("method_counts must be recomputed from expiry_results")
        expected_overall = (
            OverallStatus.NONE_USABLE
            if usable_count == 0
            else OverallStatus.ALL_USABLE
            if usable_count == len(self.expiry_results)
            else OverallStatus.PARTIALLY_USABLE
        )
        if self.overall_status is not expected_overall:
            raise ValueError("overall_status does not match usable expiry count")

        if not isinstance(self.calendar_pair_checks, list) or any(
            not isinstance(item, CalendarPairDiagnostic)
            for item in self.calendar_pair_checks
        ):
            raise ValueError("calendar_pair_checks contains an invalid item")
        pair_ids = [item.pair_check_id for item in self.calendar_pair_checks]
        if len(pair_ids) != len(set(pair_ids)):
            raise ValueError("pair_check_id values must be unique")
        for pair in self.calendar_pair_checks:
            expected_pair_id = make_calendar_pair_id(
                input_fingerprint=self.input_fingerprint,
                product=self.product,
                timestamp=self.timestamp,
                phase=pair.phase,
                parent_attempt_id=pair.parent_attempt_id,
                earlier_maturity_id=pair.earlier_maturity_id,
                later_maturity_id=pair.later_maturity_id,
                earlier_attempt_id=pair.earlier_attempt_id,
                later_attempt_id=pair.later_attempt_id,
                policy_version=self.policy_version,
            )
            if pair.pair_check_id != expected_pair_id:
                raise ValueError("pair_check_id does not match its canonical identity payload")

        _require_finite_sequence(
            self.surface_log_moneyness,
            "surface_log_moneyness",
            strictly_increasing=True,
        )
        _require_finite_sequence(
            self.surface_time_to_expiry,
            "surface_time_to_expiry",
            strictly_increasing=True,
        )
        if self.surface_time_to_expiry != expiry_times:
            raise ValueError("surface maturities must match expiry results")
        row_count = len(self.surface_time_to_expiry)
        column_count = len(self.surface_log_moneyness)
        if not isinstance(self.surface_total_variance, list) or not isinstance(
            self.surface_iv, list
        ):
            raise ValueError("surface matrices must be lists")
        if len(self.surface_total_variance) != row_count or len(self.surface_iv) != row_count:
            raise ValueError("surface matrix row count is invalid")
        for result, w_row, iv_row in zip(
            self.expiry_results,
            self.surface_total_variance,
            self.surface_iv,
            strict=True,
        ):
            _require_finite_sequence(w_row, "surface_total_variance row", nullable_items=True)
            _require_finite_sequence(iv_row, "surface_iv row", nullable_items=True)
            if len(w_row) != column_count or len(iv_row) != column_count:
                raise ValueError("surface matrix column count is invalid")
            for w_value, iv_value in zip(w_row, iv_row):
                if (w_value is None) != (iv_value is None):
                    raise ValueError("surface w and IV masks must match")
                if w_value is not None:
                    if w_value <= 0.0 or iv_value != math.sqrt(
                        w_value / result.time_to_expiry
                    ):
                        raise ValueError("surface IV must equal sqrt(w/T) for positive w")
            if not result.usable and any(value is not None for value in w_row):
                raise ValueError("unusable expiry surface row must be null")
        if self.surface_grid_status is SurfaceGridStatus.AVAILABLE:
            if column_count != 201:
                raise ValueError("available surface grid has exactly 201 points")
        elif column_count != 0:
            raise ValueError("unavailable surface grid has zero columns")


def to_total_variance(implied_volatility: float, time_to_expiry: float) -> float:
    """Convert one finite non-negative IV to total variance."""

    _require_finite(implied_volatility, "implied_volatility")
    _require_finite(time_to_expiry, "time_to_expiry", positive=True)
    if float(implied_volatility) < 0.0:
        raise ValueError("implied_volatility cannot be negative")
    return float(implied_volatility) ** 2 * float(time_to_expiry)


def to_implied_volatility(total_variance: float, time_to_expiry: float) -> float:
    """Convert one finite positive total variance to display IV."""

    _require_finite(total_variance, "total_variance", positive=True)
    _require_finite(time_to_expiry, "time_to_expiry", positive=True)
    return math.sqrt(float(total_variance) / float(time_to_expiry))


def _readonly_array(values: object, *, dtype: Any) -> np.ndarray:
    result = np.array(values, dtype=dtype, copy=True)
    result.setflags(write=False)
    return result


def diagnostic_curve_grid(
    k_min: float,
    k_max: float,
    merged_raw_k: Sequence[float] | np.ndarray,
    policy: FitPolicy | None = None,
) -> np.ndarray:
    """Return the exact float64 unique union used by diagnostics and plots."""

    active_policy = FitPolicy() if policy is None else policy
    if not isinstance(active_policy, FitPolicy):
        raise ValueError("policy must be FitPolicy")
    _require_finite(k_min, "k_min")
    _require_finite(k_max, "k_max")
    if float(k_min) >= float(k_max):
        raise ValueError("diagnostic curve support must have positive width")
    raw = np.asarray(merged_raw_k, dtype=np.float64)
    if raw.ndim != 1 or raw.size == 0 or not np.isfinite(raw).all():
        raise ValueError("merged_raw_k must be a non-empty finite vector")
    if np.any(raw < float(k_min)) or np.any(raw > float(k_max)):
        raise ValueError("merged_raw_k must lie within closed support")
    base = np.linspace(
        float(k_min),
        float(k_max),
        active_policy.diagnostic_curve_base_size,
        endpoint=True,
        dtype=np.float64,
    )
    return _readonly_array(np.unique(np.concatenate((base, raw))), dtype=np.float64)


_CURVE_MODEL_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class CurveModel:
    method: FitMethod
    time_to_expiry: float
    k_min: float
    k_max: float
    knots: np.ndarray
    _evaluator: Callable[[np.ndarray], object]
    _first_derivative: Callable[[np.ndarray], object] | None
    _second_derivative: Callable[[np.ndarray], object] | None
    _piecewise: object | None

    def __init__(
        self,
        token: object,
        *,
        method: FitMethod,
        time_to_expiry: float,
        k_min: float,
        k_max: float,
        evaluator: Callable[[np.ndarray], object],
        knots: Sequence[float] | np.ndarray,
        first_derivative: Callable[[np.ndarray], object] | None = None,
        second_derivative: Callable[[np.ndarray], object] | None = None,
        piecewise: object | None = None,
    ) -> None:
        if token is not _CURVE_MODEL_TOKEN:
            raise TypeError("CurveModel has private construction semantics")
        _require_enum(method, FitMethod, "method")
        _require_finite(time_to_expiry, "time_to_expiry", positive=True)
        _require_finite(k_min, "k_min")
        _require_finite(k_max, "k_max")
        if float(k_min) >= float(k_max):
            raise ValueError("curve support must have positive width")
        if not callable(evaluator):
            raise ValueError("evaluator must be callable")
        knot_values = np.asarray(knots, dtype=np.float64)
        if (
            knot_values.ndim != 1
            or knot_values.size == 0
            or not np.isfinite(knot_values).all()
            or np.any(np.diff(knot_values) <= 0.0)
            or knot_values[0] < float(k_min)
            or knot_values[-1] > float(k_max)
        ):
            raise ValueError("knots must be a finite, increasing in-domain vector")
        object.__setattr__(self, "method", method)
        object.__setattr__(self, "time_to_expiry", float(time_to_expiry))
        object.__setattr__(self, "k_min", float(k_min))
        object.__setattr__(self, "k_max", float(k_max))
        object.__setattr__(self, "knots", _readonly_array(knot_values, dtype=np.float64))
        object.__setattr__(self, "_evaluator", evaluator)
        object.__setattr__(self, "_first_derivative", first_derivative)
        object.__setattr__(self, "_second_derivative", second_derivative)
        object.__setattr__(self, "_piecewise", piecewise)


def _create_curve_model(
    *,
    method: FitMethod,
    time_to_expiry: float,
    k_min: float,
    k_max: float,
    evaluator: Callable[[np.ndarray], object],
    knots: Sequence[float] | np.ndarray,
    first_derivative: Callable[[np.ndarray], object] | None = None,
    second_derivative: Callable[[np.ndarray], object] | None = None,
    piecewise: object | None = None,
) -> CurveModel:
    """Private bridge for later fitters and contract tests; never bypass evaluation."""

    return CurveModel(
        _CURVE_MODEL_TOKEN,
        method=method,
        time_to_expiry=time_to_expiry,
        k_min=k_min,
        k_max=k_max,
        evaluator=evaluator,
        knots=knots,
        first_derivative=first_derivative,
        second_derivative=second_derivative,
        piecewise=piecewise,
    )


@dataclass(frozen=True, slots=True)
class CurveEvaluation:
    k: np.ndarray
    supported: np.ndarray
    total_variance: np.ndarray
    iv: np.ndarray

    def __post_init__(self) -> None:
        arrays = (
            _readonly_array(self.k, dtype=np.float64),
            _readonly_array(self.supported, dtype=np.bool_),
            _readonly_array(self.total_variance, dtype=object),
            _readonly_array(self.iv, dtype=object),
        )
        if len({array.shape for array in arrays}) != 1:
            raise ValueError("curve evaluation arrays must have equal shapes")
        for name, value in zip(
            ("k", "supported", "total_variance", "iv"), arrays, strict=True
        ):
            object.__setattr__(self, name, value)


def evaluate_curve(
    curve: CurveModel,
    k_query: Sequence[float] | np.ndarray | float,
) -> CurveEvaluation:
    """Evaluate a curve only on its closed raw-node support; never extrapolate."""

    if not isinstance(curve, CurveModel):
        raise ValueError("curve must be CurveModel")
    query = np.asarray(k_query, dtype=np.float64)
    if query.ndim == 0:
        query = query.reshape(1)
    if query.ndim != 1 or not np.isfinite(query).all():
        raise ValueError("k_query must be a finite scalar or one-dimensional vector")
    supported = (query >= curve.k_min) & (query <= curve.k_max)
    total_variance = np.full(query.shape, None, dtype=object)
    iv = np.full(query.shape, None, dtype=object)
    if np.any(supported):
        evaluated = np.asarray(curve._evaluator(query[supported]), dtype=np.float64)
        if evaluated.ndim == 0:
            evaluated = evaluated.reshape(1)
        else:
            evaluated = evaluated.reshape(-1)
        if evaluated.size != int(np.count_nonzero(supported)):
            raise ValueError("curve evaluator returned an incompatible shape")
        supported_indices = np.flatnonzero(supported)
        for index, value in zip(supported_indices, evaluated, strict=True):
            if math.isfinite(float(value)):
                total_variance[index] = float(value)
                if float(value) > 0.0:
                    iv[index] = to_implied_volatility(value, curve.time_to_expiry)
    return CurveEvaluation(
        k=query,
        supported=supported,
        total_variance=total_variance,
        iv=iv,
    )


def _ssvi_value_derivatives(
    k: Sequence[float] | np.ndarray,
    *,
    theta: float,
    rho: float,
    eta: float,
    gamma: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = np.asarray(k, dtype=np.float64)
    theta64 = np.float64(theta)
    rho64 = np.float64(rho)
    phi = np.float64(eta) * theta64 ** (-np.float64(gamma))
    shifted = phi * values + rho64
    q = shifted * shifted + 1.0 - rho64 * rho64
    root = np.sqrt(q)
    total_variance = theta64 / 2.0 * (1.0 + rho64 * phi * values + root)
    first = theta64 / 2.0 * (rho64 * phi + phi * shifted / root)
    second = (
        theta64
        / 2.0
        * phi**2
        * (1.0 - rho64**2)
        / q ** np.float64(1.5)
    )
    return total_variance, first, second


def _raw_svi_value_derivatives(
    k: Sequence[float] | np.ndarray,
    parameters: Sequence[float] | np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = np.asarray(k, dtype=np.float64)
    parameter_values = np.asarray(parameters, dtype=np.float64)
    if parameter_values.shape != (5,):
        raise ValueError("Raw-SVI parameters must be [a,b,rho,m,sigma]")
    a, b, rho, m, sigma = parameter_values
    shifted = values - m
    squared = shifted * shifted + sigma * sigma
    root = np.sqrt(squared)
    total_variance = a + b * (rho * shifted + root)
    first = b * (rho + shifted / root)
    second = b * sigma * sigma / squared ** np.float64(1.5)
    return total_variance, first, second


def _ssvi_constraint_slacks(
    theta_by_maturity: Sequence[float] | np.ndarray,
    *,
    rho: float,
    eta: float,
    gamma: float,
    policy: FitPolicy,
) -> dict[str, float]:
    theta = np.asarray(theta_by_maturity, dtype=np.float64)
    if theta.ndim != 1 or theta.size == 0:
        raise ValueError("theta_by_maturity must be a non-empty vector")
    phi = float(eta) * theta ** (-float(gamma))
    monotonic = float(np.min(np.diff(theta))) if theta.size > 1 else 0.0
    return {
        "theta_floor": float(np.min(theta - policy.variance_floor)),
        "theta_monotonic": monotonic,
        "rho_lower": float(rho) - policy.ssvi_rho_bounds[0],
        "rho_upper": policy.ssvi_rho_bounds[1] - float(rho),
        "eta_lower": float(eta) - policy.constraint_margin,
        "eta_upper": policy.ssvi_eta_upper - float(eta),
        "gamma_lower": float(gamma) - policy.ssvi_gamma_bounds[0],
        "gamma_upper": policy.ssvi_gamma_bounds[1] - float(gamma),
        "barrier_one": float(
            np.min(
                policy.ssvi_barrier_limit
                - policy.constraint_margin
                - theta * phi * (1.0 + abs(float(rho)))
            )
        ),
        "barrier_two": float(
            np.min(
                policy.ssvi_barrier_limit
                - policy.constraint_margin
                - theta * phi * phi * (1.0 + abs(float(rho)))
            )
        ),
    }


def _raw_svi_constraint_slacks(
    parameters: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> dict[str, float]:
    values = np.asarray(parameters, dtype=np.float64)
    if values.shape != (5,):
        raise ValueError("Raw-SVI parameters must be [a,b,rho,m,sigma]")
    a, b, rho, _m, sigma = (float(value) for value in values)
    return {
        "b_lower": b - policy.constraint_margin,
        "rho_lower": rho - policy.raw_svi_rho_bounds[0],
        "rho_upper": policy.raw_svi_rho_bounds[1] - rho,
        "sigma_lower": sigma - policy.constraint_margin,
        "global_minimum": (
            a
            + b * sigma * math.sqrt(1.0 - rho * rho)
            - policy.constraint_margin
        ),
        "right_wing": 2.0 - policy.constraint_margin - b * (1.0 + rho),
        "left_wing": 2.0 - policy.constraint_margin - b * (1.0 - rho),
    }


def _ssvi_objective(
    parameters: Sequence[float] | np.ndarray,
    k_by_maturity: Sequence[Sequence[float] | np.ndarray],
    w_by_maturity: Sequence[Sequence[float] | np.ndarray],
    policy: FitPolicy,
) -> float:
    parameter_values = np.asarray(parameters, dtype=np.float64)
    maturity_count = len(k_by_maturity)
    if maturity_count == 0 or maturity_count != len(w_by_maturity):
        raise ValueError("SSVI objective requires matching non-empty maturities")
    if parameter_values.shape != (maturity_count + 3,):
        raise ValueError("SSVI parameter vector has incompatible length")
    rho, eta, gamma = parameter_values[-3:]
    objective = np.float64(0.0)
    for theta, k_values, observed_values in zip(
        parameter_values[:maturity_count],
        k_by_maturity,
        w_by_maturity,
        strict=True,
    ):
        k_array = np.asarray(k_values, dtype=np.float64)
        observed = np.asarray(observed_values, dtype=np.float64)
        if k_array.ndim != 1 or observed.shape != k_array.shape or k_array.size == 0:
            raise ValueError("SSVI maturity nodes must be matching non-empty vectors")
        fitted = _ssvi_value_derivatives(
            k_array,
            theta=float(theta),
            rho=float(rho),
            eta=float(eta),
            gamma=float(gamma),
        )[0]
        scale = np.float64(
            max(float(np.median(np.abs(observed))), policy.variance_floor)
        )
        residual = (fitted - observed) / scale / np.sqrt(np.float64(k_array.size))
        objective += np.sum(residual * residual, dtype=np.float64)
    return float(objective)


def _raw_svi_objective(
    parameters: Sequence[float] | np.ndarray,
    k: Sequence[float] | np.ndarray,
    observed_total_variance: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> float:
    k_values = np.asarray(k, dtype=np.float64)
    observed = np.asarray(observed_total_variance, dtype=np.float64)
    if k_values.ndim != 1 or observed.shape != k_values.shape or k_values.size == 0:
        raise ValueError("Raw-SVI objective nodes must be matching non-empty vectors")
    fitted = _raw_svi_value_derivatives(k_values, parameters)[0]
    scale = np.float64(max(float(np.median(np.abs(observed))), policy.variance_floor))
    residual = (fitted - observed) / scale
    return float(np.mean(residual * residual, dtype=np.float64))


def _fit_error_metrics(
    observed_total_variance: Sequence[float] | np.ndarray,
    fitted_total_variance: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> dict[str, float]:
    observed = np.asarray(observed_total_variance, dtype=np.float64)
    fitted = np.asarray(fitted_total_variance, dtype=np.float64)
    if observed.ndim != 1 or fitted.shape != observed.shape or observed.size == 0:
        raise ValueError("fit error vectors must be matching and non-empty")
    rmse = float(np.sqrt(np.mean((fitted - observed) ** 2, dtype=np.float64)))
    scale = max(float(np.median(np.abs(observed))), policy.variance_floor)
    return {"rmse_total_variance": rmse, "nrmse_total_variance": rmse / scale}


def _validated_curve_nodes(
    k_nodes: Sequence[float] | np.ndarray,
    total_variance_nodes: Sequence[float] | np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    k_values = np.asarray(k_nodes, dtype=np.float64)
    w_values = np.asarray(total_variance_nodes, dtype=np.float64)
    if (
        k_values.ndim != 1
        or w_values.shape != k_values.shape
        or k_values.size < 2
        or not np.isfinite(k_values).all()
        or not np.isfinite(w_values).all()
        or np.any(np.diff(k_values) <= 0.0)
    ):
        raise ValueError("curve nodes must be matching finite vectors with increasing k")
    return k_values, w_values


def _create_ssvi_curve(
    *,
    time_to_expiry: float,
    k_min: float,
    k_max: float,
    raw_k: Sequence[float] | np.ndarray,
    theta: float,
    rho: float,
    eta: float,
    gamma: float,
) -> CurveModel:
    raw_values = np.asarray(raw_k, dtype=np.float64)
    if (
        raw_values.ndim != 1
        or raw_values.size < 4
        or not np.isfinite(raw_values).all()
        or np.any(np.diff(raw_values) <= 0.0)
        or raw_values[0] != float(k_min)
        or raw_values[-1] != float(k_max)
    ):
        raise ValueError("SSVI curve requires at least four increasing support nodes")

    def values(k: np.ndarray) -> np.ndarray:
        return _ssvi_value_derivatives(
            k, theta=theta, rho=rho, eta=eta, gamma=gamma
        )[0]

    def first(k: np.ndarray) -> np.ndarray:
        return _ssvi_value_derivatives(
            k, theta=theta, rho=rho, eta=eta, gamma=gamma
        )[1]

    def second(k: np.ndarray) -> np.ndarray:
        return _ssvi_value_derivatives(
            k, theta=theta, rho=rho, eta=eta, gamma=gamma
        )[2]

    return _create_curve_model(
        method=FitMethod.SSVI,
        time_to_expiry=time_to_expiry,
        k_min=k_min,
        k_max=k_max,
        evaluator=values,
        knots=raw_values,
        first_derivative=first,
        second_derivative=second,
    )


def _create_raw_svi_curve(
    *,
    time_to_expiry: float,
    k_min: float,
    k_max: float,
    raw_k: Sequence[float] | np.ndarray,
    parameters: Sequence[float] | np.ndarray,
) -> CurveModel:
    parameter_values = np.asarray(parameters, dtype=np.float64).copy()
    raw_values = np.asarray(raw_k, dtype=np.float64)
    if (
        raw_values.ndim != 1
        or raw_values.size < 5
        or not np.isfinite(raw_values).all()
        or np.any(np.diff(raw_values) <= 0.0)
        or raw_values[0] != float(k_min)
        or raw_values[-1] != float(k_max)
    ):
        raise ValueError("Raw-SVI curve requires at least five increasing support nodes")

    def values(k: np.ndarray) -> np.ndarray:
        return _raw_svi_value_derivatives(k, parameter_values)[0]

    def first(k: np.ndarray) -> np.ndarray:
        return _raw_svi_value_derivatives(k, parameter_values)[1]

    def second(k: np.ndarray) -> np.ndarray:
        return _raw_svi_value_derivatives(k, parameter_values)[2]

    return _create_curve_model(
        method=FitMethod.RAW_SVI,
        time_to_expiry=time_to_expiry,
        k_min=k_min,
        k_max=k_max,
        evaluator=values,
        knots=raw_values,
        first_derivative=first,
        second_derivative=second,
    )


def _create_pchip_curve(
    *,
    time_to_expiry: float,
    k_nodes: Sequence[float] | np.ndarray,
    total_variance_nodes: Sequence[float] | np.ndarray,
) -> CurveModel:
    k_values, w_values = _validated_curve_nodes(k_nodes, total_variance_nodes)
    if k_values.size < 4:
        raise ValueError("PCHIP requires at least four nodes")
    interpolator = PchipInterpolator(k_values, w_values, extrapolate=False)
    first = interpolator.derivative(1)
    second = interpolator.derivative(2)
    return _create_curve_model(
        method=FitMethod.PCHIP,
        time_to_expiry=time_to_expiry,
        k_min=float(k_values[0]),
        k_max=float(k_values[-1]),
        evaluator=interpolator,
        knots=k_values,
        first_derivative=first,
        second_derivative=second,
        piecewise=interpolator,
    )


def _create_linear_curve(
    *,
    time_to_expiry: float,
    k_nodes: Sequence[float] | np.ndarray,
    total_variance_nodes: Sequence[float] | np.ndarray,
) -> CurveModel:
    k_values, w_values = _validated_curve_nodes(k_nodes, total_variance_nodes)
    if k_values.size not in {2, 3}:
        raise ValueError("LINEAR requires exactly two or three nodes")
    slopes = np.diff(w_values) / np.diff(k_values)

    def values(query: np.ndarray) -> np.ndarray:
        return np.interp(query, k_values, w_values)

    def first(query: np.ndarray) -> np.ndarray:
        indices = np.searchsorted(k_values, query, side="right") - 1
        indices = np.clip(indices, 0, slopes.size - 1)
        return slopes[indices]

    def second(query: np.ndarray) -> np.ndarray:
        return np.zeros(np.asarray(query).shape, dtype=np.float64)

    return _create_curve_model(
        method=FitMethod.LINEAR,
        time_to_expiry=time_to_expiry,
        k_min=float(k_values[0]),
        k_max=float(k_values[-1]),
        evaluator=values,
        knots=k_values,
        first_derivative=first,
        second_derivative=second,
        piecewise=(k_values.copy(), w_values.copy()),
    )


def _curve_values(curve: CurveModel, k: Sequence[float] | np.ndarray) -> np.ndarray:
    evaluation = evaluate_curve(curve, k)
    if not bool(np.all(evaluation.supported)):
        raise ValueError("check grid must stay within closed curve support")
    return np.array(
        [np.nan if value is None else float(value) for value in evaluation.total_variance],
        dtype=np.float64,
    )


def _knot_neighbor_points(curve: CurveModel, policy: FitPolicy) -> np.ndarray:
    if curve.method not in {FitMethod.PCHIP, FitMethod.LINEAR} or curve.knots.size < 3:
        return np.empty(0, dtype=np.float64)
    points: list[float] = []
    for index in range(1, curve.knots.size - 1):
        knot = float(curve.knots[index])
        delta = min(
            knot - float(curve.knots[index - 1]),
            float(curve.knots[index + 1]) - knot,
        ) / policy.knot_neighbor_divisor
        for point in (knot - delta, knot + delta):
            if curve.k_min <= point <= curve.k_max:
                points.append(point)
    return np.asarray(points, dtype=np.float64)


def _composite_check_grid(
    curve: CurveModel,
    merged_raw_k: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> np.ndarray:
    raw = np.asarray(merged_raw_k, dtype=np.float64)
    if raw.ndim != 1 or not np.isfinite(raw).all():
        raise ValueError("merged_raw_k must be a finite vector")
    if np.any(raw < curve.k_min) or np.any(raw > curve.k_max):
        raise ValueError("merged_raw_k lies outside curve support")
    base = np.linspace(
        curve.k_min,
        curve.k_max,
        policy.base_grid_size,
        endpoint=True,
        dtype=np.float64,
    )
    return _readonly_array(
        np.unique(
            np.concatenate((base, raw, curve.knots, _knot_neighbor_points(curve, policy)))
        ),
        dtype=np.float64,
    )


@dataclass(frozen=True, slots=True)
class _RefinementResult:
    grid: np.ndarray
    resolution_limited: bool
    max_depth_triggered: bool
    minimum_interval: float
    refinement_depth: int
    non_finite_probe: bool


def _adaptive_margin_grid(
    initial_grid: Sequence[float] | np.ndarray,
    margin_evaluator: Callable[[np.ndarray], np.ndarray],
    *,
    tolerance: float,
    policy: FitPolicy,
) -> _RefinementResult:
    grid = np.unique(np.asarray(initial_grid, dtype=np.float64))
    near_band = policy.near_margin_factor * float(tolerance)
    max_depth_triggered = False
    refinement_depth = 0
    non_finite_probe = False
    while True:
        margins = np.asarray(margin_evaluator(grid), dtype=np.float64)
        if margins.shape != grid.shape or not np.isfinite(margins).all():
            non_finite_probe = True
            break
        if np.any(margins < 0.0):
            break
        widths = np.diff(grid)
        eligible = widths > policy.min_k_interval
        if not np.any(eligible):
            break
        if refinement_depth >= policy.max_refinement_depth:
            max_depth_triggered = bool(
                np.any(
                    (
                        (np.abs(margins[:-1]) <= near_band)
                        | (np.abs(margins[1:]) <= near_band)
                    )
                    & eligible
                )
            )
            break
        midpoints = (grid[:-1] + grid[1:]) / 2.0
        midpoint_margins = np.asarray(
            margin_evaluator(midpoints[eligible]), dtype=np.float64
        )
        if midpoint_margins.shape != midpoints[eligible].shape or not np.isfinite(
            midpoint_margins
        ).all():
            grid = np.unique(np.concatenate((grid, midpoints[eligible])))
            refinement_depth += 1
            non_finite_probe = True
            break
        endpoint_near = (
            (np.abs(margins[:-1]) <= near_band)
            | (np.abs(margins[1:]) <= near_band)
        ) & eligible
        probe_near_or_violation = np.zeros(widths.shape, dtype=bool)
        probe_near_or_violation[eligible] = (
            (np.abs(midpoint_margins) <= near_band) | (midpoint_margins < 0.0)
        )
        refine = endpoint_near | probe_near_or_violation
        if not np.any(refine):
            break
        grid = np.unique(np.concatenate((grid, midpoints[refine])))
        refinement_depth += 1
        if np.any(midpoint_margins < 0.0):
            break
    final_margins = np.asarray(margin_evaluator(grid), dtype=np.float64)
    finite = final_margins.shape == grid.shape and np.isfinite(final_margins).all()
    final_near = bool(finite and np.any(np.abs(final_margins) <= near_band))
    final_eligible = bool(
        grid.size > 1 and np.any(np.diff(grid) > policy.min_k_interval)
    )
    resolution_limited = bool(
        finite
        and not np.any(final_margins < 0.0)
        and final_near
        and (
            max_depth_triggered
            or refinement_depth >= policy.max_refinement_depth
            or not final_eligible
        )
    )
    minimum_interval = float(np.min(np.diff(grid))) if grid.size > 1 else 0.0
    return _RefinementResult(
        grid=_readonly_array(grid, dtype=np.float64),
        resolution_limited=resolution_limited,
        max_depth_triggered=max_depth_triggered,
        minimum_interval=minimum_interval,
        refinement_depth=refinement_depth,
        non_finite_probe=non_finite_probe,
    )


def _not_run_check(name: str) -> CheckDiagnostic:
    return CheckDiagnostic(
        name=name,
        status=CheckStatus.NOT_APPLICABLE,
        conclusion="not_applicable",
        reason_code="not_run",
        primary_value=None,
        threshold=None,
        violation_count=None,
        grid_point_count=0,
        metrics={},
    )


def _passed_check(
    name: str,
    *,
    primary_value: float,
    threshold: float,
    grid_point_count: int,
    metrics: dict[str, JSONScalar],
) -> CheckDiagnostic:
    return CheckDiagnostic(
        name=name,
        status=CheckStatus.PASSED,
        conclusion="sampled_no_violation",
        reason_code=None,
        primary_value=float(primary_value),
        threshold=float(threshold),
        violation_count=0,
        grid_point_count=grid_point_count,
        metrics=metrics,
    )


def _indeterminate_check(
    name: str,
    *,
    primary_value: float | None,
    threshold: float | None,
    grid_point_count: int,
    metrics: dict[str, JSONScalar],
) -> CheckDiagnostic:
    return CheckDiagnostic(
        name=name,
        status=CheckStatus.INDETERMINATE,
        conclusion="unreliable",
        reason_code="resolution_limit",
        primary_value=primary_value,
        threshold=threshold,
        violation_count=None,
        grid_point_count=grid_point_count,
        metrics=metrics,
    )


def _failed_check_diagnostic(
    name: str,
    *,
    reason_code: str,
    primary_value: float,
    threshold: float,
    violation_count: int,
    grid_point_count: int,
    metrics: dict[str, JSONScalar],
) -> CheckDiagnostic:
    return CheckDiagnostic(
        name=name,
        status=CheckStatus.FAILED,
        conclusion="violation_found",
        reason_code=reason_code,
        primary_value=float(primary_value),
        threshold=float(threshold),
        violation_count=violation_count,
        grid_point_count=grid_point_count,
        metrics=metrics,
    )


def _check_positive_total_variance(
    curve: CurveModel,
    merged_raw_k: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> CheckDiagnostic:
    initial = _composite_check_grid(curve, merged_raw_k, policy)

    def margin(points: np.ndarray) -> np.ndarray:
        return _curve_values(curve, points) - policy.variance_floor

    refined = _adaptive_margin_grid(
        initial, margin, tolerance=policy.variance_floor, policy=policy
    )
    values = _curve_values(curve, refined.grid)
    finite = np.isfinite(values)
    if not finite.all():
        return _failed_check_diagnostic(
            "positive_total_variance",
            reason_code="non_finite_total_variance",
            primary_value=float(np.min(values[finite])) if finite.any() else 0.0,
            threshold=policy.variance_floor,
            violation_count=int(np.count_nonzero(~finite)),
            grid_point_count=refined.grid.size,
            metrics={
                "non_finite_count": int(np.count_nonzero(~finite)),
                "refinement_depth": refined.refinement_depth,
                "non_finite_probe": refined.non_finite_probe,
            },
        )
    minimum = float(np.min(values))
    violations = values <= policy.variance_floor
    metrics: dict[str, JSONScalar] = {
        "minimum_margin": minimum - policy.variance_floor,
        "minimum_interval": refined.minimum_interval,
        "max_depth_triggered": refined.max_depth_triggered,
        "refinement_depth": refined.refinement_depth,
        "non_finite_probe": refined.non_finite_probe,
    }
    if np.any(violations):
        return _failed_check_diagnostic(
            "positive_total_variance",
            reason_code="below_variance_floor",
            primary_value=minimum,
            threshold=policy.variance_floor,
            violation_count=int(np.count_nonzero(violations)),
            grid_point_count=refined.grid.size,
            metrics=metrics,
        )
    if refined.resolution_limited:
        return _indeterminate_check(
            "positive_total_variance",
            primary_value=minimum,
            threshold=policy.variance_floor,
            grid_point_count=refined.grid.size,
            metrics=metrics,
        )
    return _passed_check(
        "positive_total_variance",
        primary_value=minimum,
        threshold=policy.variance_floor,
        grid_point_count=refined.grid.size,
        metrics=metrics,
    )


def _normalized_black_call(
    k: Sequence[float] | np.ndarray,
    total_variance: Sequence[float] | np.ndarray,
) -> np.ndarray:
    k_values = np.asarray(k, dtype=np.float64)
    w_values = np.asarray(total_variance, dtype=np.float64)
    if k_values.shape != w_values.shape or np.any(w_values <= 0.0):
        raise ValueError("Black call requires matching k and positive total variance")
    root = np.sqrt(w_values)
    d1 = -k_values / root + 0.5 * root
    d2 = d1 - root
    return ndtr(d1) - np.exp(k_values) * ndtr(d2)


def _cancellation_prone_intervals(points: np.ndarray) -> np.ndarray:
    point_differences = np.diff(points)
    resolution_scale = np.maximum(
        1.0, np.maximum(np.abs(points[:-1]), np.abs(points[1:]))
    )
    return (
        point_differences
        <= 16.0 * np.finfo(np.float64).eps * resolution_scale
    )


def _black_call_limiting_strike_slope(
    k: np.ndarray,
    total_variance: np.ndarray,
    total_variance_derivative: np.ndarray,
) -> np.ndarray:
    roots = np.sqrt(total_variance)
    d2 = -k / roots - 0.5 * roots
    density = np.exp(-0.5 * d2 * d2) / math.sqrt(2.0 * math.pi)
    return density * total_variance_derivative / (2.0 * roots) - ndtr(d2)


def _check_call_price_monotonic(
    curve: CurveModel,
    grid: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> CheckDiagnostic:
    points = np.unique(np.asarray(grid, dtype=np.float64))
    values = _curve_values(curve, points)
    if not np.isfinite(values).all() or np.any(values <= 0.0):
        return _not_run_check("call_price_monotonic")
    changes = np.diff(_normalized_black_call(points, values))
    cancellation_prone = _cancellation_prone_intervals(points)
    if np.any(cancellation_prone):
        if curve._first_derivative is None:
            return _not_run_check("call_price_monotonic")
        left_points = points[:-1][cancellation_prone]
        left_derivatives = np.asarray(
            curve._first_derivative(left_points), dtype=np.float64
        )
        limiting_slopes = _black_call_limiting_strike_slope(
            left_points,
            values[:-1][cancellation_prone],
            left_derivatives,
        )
        stable_strike_differences = (
            np.exp(left_points)
            * np.expm1(np.diff(points)[cancellation_prone])
        )
        changes[cancellation_prone] = limiting_slopes * stable_strike_differences
    maximum = float(np.max(changes)) if changes.size else 0.0
    violations = changes > policy.price_monotonic_abs_tolerance
    metrics = {"maximum_positive_change": max(maximum, 0.0)}
    if np.any(violations):
        return _failed_check_diagnostic(
            "call_price_monotonic",
            reason_code="call_price_increase",
            primary_value=maximum,
            threshold=policy.price_monotonic_abs_tolerance,
            violation_count=int(np.count_nonzero(violations)),
            grid_point_count=points.size,
            metrics=metrics,
        )
    return _passed_check(
        "call_price_monotonic",
        primary_value=maximum,
        threshold=policy.price_monotonic_abs_tolerance,
        grid_point_count=points.size,
        metrics=metrics,
    )


def _check_call_price_convex(
    curve: CurveModel,
    grid: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> CheckDiagnostic:
    points = np.unique(np.asarray(grid, dtype=np.float64))
    values = _curve_values(curve, points)
    if not np.isfinite(values).all() or np.any(values <= 0.0):
        return _not_run_check("call_price_convex")
    calls = _normalized_black_call(points, values)
    point_differences = np.diff(points)
    strike_differences = np.exp(points[:-1]) * np.expm1(point_differences)
    slopes = np.diff(calls) / strike_differences
    cancellation_prone = _cancellation_prone_intervals(points)
    if np.any(cancellation_prone):
        if curve._first_derivative is None:
            return _not_run_check("call_price_convex")
        left_points = points[:-1][cancellation_prone]
        left_derivatives = np.asarray(
            curve._first_derivative(left_points), dtype=np.float64
        )
        slopes[cancellation_prone] = _black_call_limiting_strike_slope(
            left_points,
            values[:-1][cancellation_prone],
            left_derivatives,
        )
    slope_changes = np.diff(slopes)
    minimum = float(np.min(slope_changes)) if slope_changes.size else 0.0
    violations = slope_changes < -policy.price_convex_slope_tolerance
    metrics = {"minimum_secant_slope_change": minimum}
    if np.any(violations):
        return _failed_check_diagnostic(
            "call_price_convex",
            reason_code="decreasing_secant_slope",
            primary_value=minimum,
            threshold=-policy.price_convex_slope_tolerance,
            violation_count=int(np.count_nonzero(violations)),
            grid_point_count=points.size,
            metrics=metrics,
        )
    return _passed_check(
        "call_price_convex",
        primary_value=minimum,
        threshold=-policy.price_convex_slope_tolerance,
        grid_point_count=points.size,
        metrics=metrics,
    )


def _butterfly_g_values(curve: CurveModel, points: np.ndarray) -> np.ndarray:
    if curve._first_derivative is None or curve._second_derivative is None:
        raise ValueError("analytic derivatives are unavailable")
    w = _curve_values(curve, points)
    first = np.asarray(curve._first_derivative(points), dtype=np.float64)
    second = np.asarray(curve._second_derivative(points), dtype=np.float64)
    return (
        (1.0 - points * first / (2.0 * w)) ** 2
        - first**2 / 4.0 * (1.0 / w + 0.25)
        + second / 2.0
    )


def _check_butterfly_g_nonnegative(
    curve: CurveModel,
    merged_raw_k: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> CheckDiagnostic:
    if curve.method in {FitMethod.PCHIP, FitMethod.LINEAR}:
        return CheckDiagnostic(
            name="butterfly_g_nonnegative",
            status=CheckStatus.NOT_APPLICABLE,
            conclusion="not_applicable",
            reason_code="method_has_no_analytic_g",
            primary_value=None,
            threshold=None,
            violation_count=None,
            grid_point_count=0,
            metrics={},
        )
    initial = _composite_check_grid(curve, merged_raw_k, policy)

    def margin(points: np.ndarray) -> np.ndarray:
        return _butterfly_g_values(curve, points) + policy.butterfly_g_tolerance

    refined = _adaptive_margin_grid(
        initial, margin, tolerance=policy.butterfly_g_tolerance, policy=policy
    )
    g_values = _butterfly_g_values(curve, refined.grid)
    if not np.isfinite(g_values).all():
        return _indeterminate_check(
            "butterfly_g_nonnegative",
            primary_value=None,
            threshold=-policy.butterfly_g_tolerance,
            grid_point_count=refined.grid.size,
            metrics={
                "non_finite_count": int(np.count_nonzero(~np.isfinite(g_values))),
                "minimum_interval": refined.minimum_interval,
                "max_depth_triggered": refined.max_depth_triggered,
                "refinement_depth": refined.refinement_depth,
                "non_finite_probe": refined.non_finite_probe,
            },
        )
    minimum = float(np.min(g_values))
    violations = g_values < -policy.butterfly_g_tolerance
    metrics = {
        "minimum_g_margin": minimum + policy.butterfly_g_tolerance,
        "minimum_interval": refined.minimum_interval,
        "max_depth_triggered": refined.max_depth_triggered,
        "refinement_depth": refined.refinement_depth,
        "non_finite_probe": refined.non_finite_probe,
    }
    if np.any(violations):
        return _failed_check_diagnostic(
            "butterfly_g_nonnegative",
            reason_code="negative_g",
            primary_value=minimum,
            threshold=-policy.butterfly_g_tolerance,
            violation_count=int(np.count_nonzero(violations)),
            grid_point_count=refined.grid.size,
            metrics=metrics,
        )
    if refined.resolution_limited:
        return _indeterminate_check(
            "butterfly_g_nonnegative",
            primary_value=minimum,
            threshold=-policy.butterfly_g_tolerance,
            grid_point_count=refined.grid.size,
            metrics=metrics,
        )
    return _passed_check(
        "butterfly_g_nonnegative",
        primary_value=minimum,
        threshold=-policy.butterfly_g_tolerance,
        grid_point_count=refined.grid.size,
        metrics=metrics,
    )


def _common_calendar_grid(
    earlier_curve: CurveModel,
    later_curve: CurveModel,
    earlier_raw_k: Sequence[float] | np.ndarray,
    later_raw_k: Sequence[float] | np.ndarray,
    lo: float,
    hi: float,
    policy: FitPolicy,
) -> np.ndarray:
    base = np.linspace(lo, hi, policy.base_grid_size, endpoint=True, dtype=np.float64)
    collections = [base]
    for curve, raw in (
        (earlier_curve, np.asarray(earlier_raw_k, dtype=np.float64)),
        (later_curve, np.asarray(later_raw_k, dtype=np.float64)),
    ):
        for values in (raw, curve.knots, _knot_neighbor_points(curve, policy)):
            collections.append(values[(values >= lo) & (values <= hi)])
    return np.unique(np.concatenate(collections))


def _check_calendar_pair(
    *,
    pair_check_id: str,
    phase: Literal["ssvi_parent", "expiry_selection"],
    earlier_maturity_id: str,
    later_maturity_id: str,
    earlier_attempt_id: str | None,
    later_attempt_id: str | None,
    parent_attempt_id: str | None,
    earlier_curve: CurveModel,
    later_curve: CurveModel,
    earlier_raw_k: Sequence[float] | np.ndarray,
    later_raw_k: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> CalendarPairDiagnostic:
    lo = max(earlier_curve.k_min, later_curve.k_min)
    hi = min(earlier_curve.k_max, later_curve.k_max)
    if lo >= hi:
        check = CheckDiagnostic(
            name="calendar_consistent",
            status=CheckStatus.NOT_TESTABLE,
            conclusion="not_testable",
            reason_code="no_overlap",
            primary_value=None,
            threshold=None,
            violation_count=None,
            grid_point_count=0,
            metrics={},
        )
        return CalendarPairDiagnostic(
            pair_check_id=pair_check_id,
            phase=phase,
            earlier_maturity_id=earlier_maturity_id,
            later_maturity_id=later_maturity_id,
            earlier_attempt_id=earlier_attempt_id,
            later_attempt_id=later_attempt_id,
            parent_attempt_id=parent_attempt_id,
            common_k_min=None,
            common_k_max=None,
            check=check,
        )
    initial = _common_calendar_grid(
        earlier_curve,
        later_curve,
        earlier_raw_k,
        later_raw_k,
        lo,
        hi,
        policy,
    )

    def margin(points: np.ndarray) -> np.ndarray:
        earlier = _curve_values(earlier_curve, points)
        later = _curve_values(later_curve, points)
        return (
            later
            - earlier
            + policy.calendar_abs_tolerance
            + policy.calendar_rel_tolerance * np.maximum(earlier, later)
        )

    refined = _adaptive_margin_grid(
        initial, margin, tolerance=policy.calendar_abs_tolerance, policy=policy
    )
    earlier = _curve_values(earlier_curve, refined.grid)
    later = _curve_values(later_curve, refined.grid)
    difference = later - earlier
    safety_margin = margin(refined.grid)
    if not np.isfinite(safety_margin).all():
        check = _indeterminate_check(
            "calendar_consistent",
            primary_value=None,
            threshold=None,
            grid_point_count=refined.grid.size,
            metrics={
                "non_finite_count": int(np.count_nonzero(~np.isfinite(safety_margin))),
                "minimum_interval": refined.minimum_interval,
                "max_depth_triggered": refined.max_depth_triggered,
                "refinement_depth": refined.refinement_depth,
                "non_finite_probe": refined.non_finite_probe,
            },
        )
    else:
        minimum_difference = float(np.min(difference))
        minimum_margin = float(np.min(safety_margin))
        thresholds = -(
            policy.calendar_abs_tolerance
            + policy.calendar_rel_tolerance * np.maximum(earlier, later)
        )
        metrics = {
            "minimum_calendar_margin": minimum_margin,
            "minimum_interval": refined.minimum_interval,
            "max_depth_triggered": refined.max_depth_triggered,
            "refinement_depth": refined.refinement_depth,
            "non_finite_probe": refined.non_finite_probe,
        }
        violations = safety_margin < 0.0
        if np.any(violations):
            check = _failed_check_diagnostic(
                "calendar_consistent",
                reason_code="calendar_total_variance_decrease",
                primary_value=minimum_difference,
                threshold=float(np.max(thresholds[violations])),
                violation_count=int(np.count_nonzero(violations)),
                grid_point_count=refined.grid.size,
                metrics=metrics,
            )
        elif refined.resolution_limited:
            check = _indeterminate_check(
                "calendar_consistent",
                primary_value=minimum_difference,
                threshold=float(np.max(thresholds)),
                grid_point_count=refined.grid.size,
                metrics=metrics,
            )
        else:
            check = _passed_check(
                "calendar_consistent",
                primary_value=minimum_difference,
                threshold=float(np.max(thresholds)),
                grid_point_count=refined.grid.size,
                metrics=metrics,
            )
    return CalendarPairDiagnostic(
        pair_check_id=pair_check_id,
        phase=phase,
        earlier_maturity_id=earlier_maturity_id,
        later_maturity_id=later_maturity_id,
        earlier_attempt_id=earlier_attempt_id,
        later_attempt_id=later_attempt_id,
        parent_attempt_id=parent_attempt_id,
        common_k_min=float(lo),
        common_k_max=float(hi),
        check=check,
    )


class _ResolutionLimit(RuntimeError):
    pass


def _parameter_max_abs_iv_slope(
    curve: CurveModel,
    policy: FitPolicy,
) -> tuple[float, float]:
    if curve.method not in {FitMethod.SSVI, FitMethod.RAW_SVI}:
        raise ValueError("SHGO slope search is only for parameter curves")
    if curve._first_derivative is None:
        raise _ResolutionLimit("analytic first derivative is unavailable")

    def objective(argument: np.ndarray) -> float:
        point = np.asarray(argument, dtype=np.float64).reshape(-1)
        if point.size != 1:
            return float("nan")
        w = _curve_values(curve, point)
        first = np.asarray(curve._first_derivative(point), dtype=np.float64)
        squared = first * first / (4.0 * curve.time_to_expiry * w)
        return -float(squared[0])

    try:
        result = shgo(
            objective,
            bounds=[(curve.k_min, curve.k_max)],
            n=policy.shgo_options["n"],
            iters=policy.shgo_options["iters"],
            sampling_method=policy.shgo_options["sampling_method"],
            workers=policy.shgo_options["workers"],
            minimizer_kwargs={
                "method": policy.shgo_minimizer_options["method"],
                "options": {
                    "ftol": policy.shgo_minimizer_options["ftol"],
                    "maxiter": policy.shgo_minimizer_options["maxiter"],
                    "disp": policy.shgo_minimizer_options["disp"],
                },
            },
        )
    except Exception as exc:
        raise _ResolutionLimit("SHGO raised an exception") from exc
    if not bool(getattr(result, "success", False)):
        raise _ResolutionLimit("SHGO did not report success")
    x = np.asarray(getattr(result, "x", []), dtype=np.float64).reshape(-1)
    fun = np.asarray(getattr(result, "fun", np.nan), dtype=np.float64).reshape(-1)
    xl = np.asarray(getattr(result, "xl", []), dtype=np.float64)
    funl = np.asarray(getattr(result, "funl", []), dtype=np.float64).reshape(-1)
    if (
        x.size != 1
        or fun.size != 1
        or not np.isfinite(x).all()
        or not np.isfinite(fun).all()
        or xl.size == 0
        or funl.size == 0
    ):
        raise _ResolutionLimit("SHGO primary or local result is incomplete")
    xl_points = xl.reshape(-1)
    if xl_points.size != funl.size or not np.isfinite(xl_points).all() or not np.isfinite(
        funl
    ).all():
        raise _ResolutionLimit("SHGO local result set is incomplete")
    candidates = np.unique(
        np.concatenate(
            (
                np.array([curve.k_min, curve.k_max], dtype=np.float64),
                x,
                xl_points,
            )
        )
    )
    if np.any(candidates < curve.k_min) or np.any(candidates > curve.k_max):
        raise _ResolutionLimit("SHGO returned an out-of-domain point")
    w = _curve_values(curve, candidates)
    first = np.asarray(curve._first_derivative(candidates), dtype=np.float64)
    slopes = np.abs(first) / (2.0 * np.sqrt(curve.time_to_expiry * w))
    if not np.isfinite(slopes).all():
        raise _ResolutionLimit("SHGO candidates have non-finite slopes")
    index = int(np.argmax(slopes))
    return float(slopes[index]), float(candidates[index])


def _real_polynomial_roots(
    ascending_coefficients: np.ndarray,
    *,
    lower: float,
    upper: float,
    policy: FitPolicy,
) -> list[float]:
    coefficients = np.asarray(ascending_coefficients, dtype=np.float64)
    while coefficients.size and coefficients[-1] == 0.0:
        coefficients = coefficients[:-1]
    if coefficients.size <= 1:
        return []
    try:
        roots = np.roots(coefficients[::-1])
    except (FloatingPointError, np.linalg.LinAlgError, ValueError) as exc:
        raise _ResolutionLimit("PCHIP polynomial roots failed") from exc
    result: list[float] = []
    for root in roots:
        if abs(float(root.imag)) > policy.pchip_root_imag_tolerance:
            continue
        value = float(root.real)
        if (
            value < lower - policy.pchip_root_interval_tolerance
            or value > upper + policy.pchip_root_interval_tolerance
        ):
            continue
        result.append(float(np.clip(value, lower, upper)))
    return result


def _pchip_stationary_points(curve: CurveModel, policy: FitPolicy) -> np.ndarray:
    if curve.method is not FitMethod.PCHIP or not isinstance(
        curve._piecewise, PchipInterpolator
    ):
        raise ValueError("PCHIP stationary roots require a PCHIP curve")
    interpolator = curve._piecewise
    candidates: list[float] = [float(value) for value in curve.knots]
    for index in range(curve.knots.size - 1):
        width = float(curve.knots[index + 1] - curve.knots[index])
        c3, c2, c1, c0 = (
            np.float64(value) for value in interpolator.c[:, index]
        )
        w = np.array([c0, c1, c2, c3], dtype=np.float64)
        first = np.array([c1, 2.0 * c2, 3.0 * c3], dtype=np.float64)
        second = np.array([2.0 * c2, 6.0 * c3], dtype=np.float64)
        stationary_factor = 2.0 * np.polynomial.polynomial.polymul(w, second)
        first_squared = np.polynomial.polynomial.polymul(first, first)
        if stationary_factor.size < first_squared.size:
            stationary_factor = np.pad(
                stationary_factor, (0, first_squared.size - stationary_factor.size)
            )
        elif first_squared.size < stationary_factor.size:
            first_squared = np.pad(
                first_squared, (0, stationary_factor.size - first_squared.size)
            )
        stationary_factor = stationary_factor - first_squared
        local_roots = _real_polynomial_roots(
            first, lower=0.0, upper=width, policy=policy
        ) + _real_polynomial_roots(
            stationary_factor, lower=0.0, upper=width, policy=policy
        )
        candidates.extend(float(curve.knots[index]) + root for root in local_roots)
    return _readonly_array(np.unique(np.asarray(candidates, dtype=np.float64)), dtype=np.float64)


def _pchip_max_abs_iv_slope(
    curve: CurveModel, policy: FitPolicy
) -> tuple[float, float]:
    candidates = _pchip_stationary_points(curve, policy)
    if curve._first_derivative is None:
        raise _ResolutionLimit("PCHIP derivative is unavailable")
    w = _curve_values(curve, candidates)
    first = np.asarray(curve._first_derivative(candidates), dtype=np.float64)
    slopes = np.abs(first) / (2.0 * np.sqrt(curve.time_to_expiry * w))
    if not np.isfinite(slopes).all():
        raise _ResolutionLimit("PCHIP stationary evaluation is non-finite")
    index = int(np.argmax(slopes))
    return float(slopes[index]), float(candidates[index])


def _linear_max_abs_iv_slope(curve: CurveModel) -> tuple[float, float]:
    if curve.method is not FitMethod.LINEAR:
        raise ValueError("linear endpoint maximum requires a LINEAR curve")
    w = _curve_values(curve, curve.knots)
    candidates: list[tuple[float, float]] = []
    for index in range(curve.knots.size - 1):
        slope = (w[index + 1] - w[index]) / (
            curve.knots[index + 1] - curve.knots[index]
        )
        endpoint_index = index if w[index] <= w[index + 1] else index + 1
        value = abs(float(slope)) / (
            2.0 * math.sqrt(curve.time_to_expiry * float(w[endpoint_index]))
        )
        candidates.append((value, float(curve.knots[endpoint_index])))
    return max(candidates, key=lambda item: (item[0], -item[1]))


def _check_jump_reliable(
    curve: CurveModel,
    merged_raw_k: Sequence[float] | np.ndarray,
    raw_iv: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> CheckDiagnostic:
    raw_k = np.asarray(merged_raw_k, dtype=np.float64)
    observed_iv = np.asarray(raw_iv, dtype=np.float64)
    if (
        raw_k.ndim != 1
        or observed_iv.shape != raw_k.shape
        or raw_k.size < 2
        or not np.isfinite(raw_k).all()
        or not np.isfinite(observed_iv).all()
        or np.any(np.diff(raw_k) <= 0.0)
    ):
        return _indeterminate_check(
            "jump_reliable",
            primary_value=None,
            threshold=None,
            grid_point_count=0,
            metrics={},
        )
    fitted = evaluate_curve(curve, raw_k)
    fitted_iv = np.array(
        [np.nan if value is None else float(value) for value in fitted.iv],
        dtype=np.float64,
    )
    if not np.isfinite(fitted_iv).all():
        return _indeterminate_check(
            "jump_reliable",
            primary_value=None,
            threshold=None,
            grid_point_count=0,
            metrics={},
        )
    node_interval_jump = float(np.max(np.abs(np.diff(fitted_iv))))
    raw_slopes = np.abs(np.diff(observed_iv)) / np.maximum(
        np.abs(np.diff(raw_k)), policy.min_k_interval
    )
    raw_scale = float(np.median(raw_slopes))
    try:
        if curve.method in {FitMethod.SSVI, FitMethod.RAW_SVI}:
            maximum, location = _parameter_max_abs_iv_slope(curve, policy)
        elif curve.method is FitMethod.PCHIP:
            maximum, location = _pchip_max_abs_iv_slope(curve, policy)
        else:
            maximum, location = _linear_max_abs_iv_slope(curve)
    except (ValueError, FloatingPointError, _ResolutionLimit):
        return _indeterminate_check(
            "jump_reliable",
            primary_value=None,
            threshold=None,
            grid_point_count=0,
            metrics={
                "node_interval_jump": node_interval_jump,
                "raw_slope_median": raw_scale,
                "optimizer_complete": False,
            },
        )
    robust_ratio = maximum / max(raw_scale, policy.robust_iv_slope_floor)
    metrics = {
        "node_interval_jump": node_interval_jump,
        "raw_slope_median": raw_scale,
        "max_abs_iv_slope": maximum,
        "robust_slope_ratio": robust_ratio,
        "max_abs_iv_slope_k": location,
        "optimizer_complete": True,
    }
    if maximum > policy.max_abs_iv_slope:
        return _failed_check_diagnostic(
            "jump_reliable",
            reason_code="absolute_iv_slope_exceeded",
            primary_value=maximum,
            threshold=policy.max_abs_iv_slope,
            violation_count=1,
            grid_point_count=0,
            metrics=metrics,
        )
    if robust_ratio > policy.max_robust_slope_ratio:
        return _failed_check_diagnostic(
            "jump_reliable",
            reason_code="robust_iv_slope_ratio_exceeded",
            primary_value=robust_ratio,
            threshold=policy.max_robust_slope_ratio,
            violation_count=1,
            grid_point_count=0,
            metrics=metrics,
        )
    return _passed_check(
        "jump_reliable",
        primary_value=maximum,
        threshold=policy.max_abs_iv_slope,
        grid_point_count=0,
        metrics=metrics,
    )


def _run_local_checks(
    curve: CurveModel,
    merged_raw_k: Sequence[float] | np.ndarray,
    raw_iv: Sequence[float] | np.ndarray,
    policy: FitPolicy,
) -> dict[str, CheckDiagnostic]:
    checks: dict[str, CheckDiagnostic] = {}
    grid: np.ndarray | None = None
    gate_order = (
        "positive_total_variance",
        "call_price_monotonic",
        "call_price_convex",
        "butterfly_g_nonnegative",
        "jump_reliable",
    )
    blocked = False
    for name in gate_order:
        if blocked:
            checks[name] = _not_run_check(name)
            continue
        try:
            if name == "positive_total_variance":
                check = _check_positive_total_variance(
                    curve, merged_raw_k, policy
                )
            elif name == "call_price_monotonic":
                grid = _composite_check_grid(curve, merged_raw_k, policy)
                check = _check_call_price_monotonic(curve, grid, policy)
            elif name == "call_price_convex":
                if grid is None:
                    raise RuntimeError("local check grid is unavailable")
                check = _check_call_price_convex(curve, grid, policy)
            elif name == "butterfly_g_nonnegative":
                check = _check_butterfly_g_nonnegative(
                    curve, merged_raw_k, policy
                )
            else:
                check = _check_jump_reliable(
                    curve, merged_raw_k, raw_iv, policy
                )
        except Exception as exc:
            check = _indeterminate_check(
                name,
                primary_value=None,
                threshold=None,
                grid_point_count=0,
                metrics={"exception_type": type(exc).__name__},
            )
        checks[name] = check
        if check.status in {CheckStatus.FAILED, CheckStatus.INDETERMINATE}:
            blocked = True
    if curve.method in {FitMethod.PCHIP, FitMethod.LINEAR}:
        checks["butterfly_g_nonnegative"] = _check_butterfly_g_nonnegative(
            curve,
            merged_raw_k,
            policy,
        )
    checks["calendar_consistent"] = _not_run_check("calendar_consistent")
    return {name: checks[name] for name in CHECK_NAMES}


@dataclass(frozen=True, slots=True)
class _LocalExpiryInput:
    """Validated merged nodes consumed only by the local fitting stage."""

    maturity_id: str
    time_to_expiry: float
    raw_node_count: int
    k: np.ndarray
    total_variance: np.ndarray
    implied_volatility: np.ndarray

    def __post_init__(self) -> None:
        _require_nonempty_string(self.maturity_id, "maturity_id")
        _require_finite(self.time_to_expiry, "time_to_expiry", positive=True)
        _require_count(self.raw_node_count, "raw_node_count")
        arrays = tuple(
            _readonly_array(value, dtype=np.float64)
            for value in (self.k, self.total_variance, self.implied_volatility)
        )
        if len({array.shape for array in arrays}) != 1 or arrays[0].ndim != 1:
            raise ValueError("local expiry node arrays must be matching vectors")
        if self.raw_node_count < arrays[0].size:
            raise ValueError("raw_node_count cannot be smaller than merged nodes")
        if any(not np.isfinite(array).all() for array in arrays):
            raise ValueError("local expiry nodes must be finite")
        if arrays[0].size > 1 and np.any(np.diff(arrays[0]) <= 0.0):
            raise ValueError("local expiry k nodes must be strictly increasing")
        if np.any(arrays[1] <= 0.0) or np.any(arrays[2] <= 0.0):
            raise ValueError("observed variance and IV nodes must be positive")
        for name, value in zip(
            ("k", "total_variance", "implied_volatility"), arrays, strict=True
        ):
            object.__setattr__(self, name, value)

    @property
    def node_count(self) -> int:
        return int(self.k.size)


@dataclass(frozen=True, slots=True)
class _IndexedStart:
    start_index: int
    parameters: np.ndarray

    def __post_init__(self) -> None:
        _require_count(self.start_index, "start_index")
        values = _readonly_array(self.parameters, dtype=np.float64)
        if values.ndim != 1:
            raise ValueError("start parameters must be a vector")
        object.__setattr__(self, "parameters", values)


@dataclass(frozen=True, slots=True)
class _PreparedStarts:
    generated_count: int
    precheck_discarded_count: int
    duplicate_discarded_count: int
    starts: tuple[_IndexedStart, ...]
    bounds: tuple[tuple[float, float], ...]
    theta_upper: float | None = None
    theta_initial: np.ndarray | None = None
    w_scale: float | None = None
    span: float | None = None

    def __post_init__(self) -> None:
        if self.theta_initial is not None:
            object.__setattr__(
                self,
                "theta_initial",
                _readonly_array(self.theta_initial, dtype=np.float64),
            )


@dataclass(frozen=True, slots=True)
class _StartPayload:
    curves: tuple[CurveModel, ...]
    metrics: tuple[dict[str, float | None] | None, ...]
    checks: tuple[dict[str, CheckDiagnostic] | None, ...]


@dataclass(frozen=True, slots=True)
class _StartOutcome:
    start_index: int
    optimizer_success: bool
    parameters: tuple[float, ...] | None
    objective: float | None
    stage_reached: int
    max_nrmse: float | None
    max_constraint_violation: float | None
    hard_failures: tuple[tuple[int, str], ...]
    payload: _StartPayload | None
    optimizer_message: str | None

    def __post_init__(self) -> None:
        _require_count(self.start_index, "start_index")
        if type(self.optimizer_success) is not bool:
            raise ValueError("optimizer_success must be bool")
        if self.stage_reached not in {0, 1, 2, 3, 4}:
            raise ValueError("stage_reached is outside the closed set")
        if self.parameters is not None:
            values = tuple(float(value) for value in self.parameters)
            object.__setattr__(self, "parameters", values)
        for name in ("objective", "max_nrmse", "max_constraint_violation"):
            value = getattr(self, name)
            if value is not None and not math.isfinite(float(value)):
                raise ValueError(f"{name} must be finite or null")
        previous = -1
        for priority, code in self.hard_failures:
            if priority < previous or priority not in range(10):
                raise ValueError("hard failures must follow the closed gate order")
            if code not in ATTEMPT_FAILURE_CODES:
                raise ValueError("hard failure code is outside the closed set")
            previous = priority

    @property
    def local_success(self) -> bool:
        return (
            self.optimizer_success
            and self.stage_reached == 4
            and not self.hard_failures
        )

    @property
    def primary_failure_code(self) -> str | None:
        return self.hard_failures[0][1] if self.hard_failures else None


@dataclass(frozen=True, slots=True)
class _LocalFitCandidate:
    """Immutable local draft; Task 4 alone adds final attempt state and calendar."""

    scope: AttemptScope
    maturity_id: str | None
    participating_maturities: tuple[str, ...]
    time_to_expiry: float | None
    method: FitMethod
    optimizer_attempted: bool
    optimizer_success: bool | None
    optimizer_start_summary: OptimizerStartSummary | None
    local_success: bool
    parameters: Mapping[str, Any] | None
    per_expiry_metrics: Mapping[str, PerExpiryMetric] | None
    rmse_total_variance: float | None
    nrmse_total_variance: float | None
    rmse_iv: float | None
    raw_node_count: int | None
    node_count: int | None
    k_min: float | None
    k_max: float | None
    candidate_k: tuple[float, ...]
    candidate_total_variance: tuple[float | None, ...]
    candidate_iv: tuple[float | None, ...]
    checks: Mapping[str, CheckDiagnostic]
    failure_code: str | None
    failure_reason: str | None
    curve: CurveModel | None

    def __post_init__(self) -> None:
        if self.parameters is not None and not isinstance(self.parameters, _FrozenDict):
            object.__setattr__(self, "parameters", _freeze_mapping(self.parameters))
        if self.per_expiry_metrics is not None and not isinstance(
            self.per_expiry_metrics, _FrozenDict
        ):
            object.__setattr__(
                self, "per_expiry_metrics", _FrozenDict(self.per_expiry_metrics)
            )
        if not isinstance(self.checks, _FrozenDict):
            object.__setattr__(self, "checks", _FrozenDict(self.checks))
        if not self.optimizer_attempted and self.failure_code in {
            "optimizer_failed",
            "optimizer_exception",
        }:
            raise ValueError("non-optimizer draft cannot use optimizer failure codes")


@dataclass(frozen=True, slots=True)
class _LocalSsviBundle:
    parent: _LocalFitCandidate
    children: tuple[_LocalFitCandidate, ...]

    def __post_init__(self) -> None:
        summary = self.parent.optimizer_start_summary
        parent_evaluable = summary is not None and summary.evaluable_count > 0
        child_maturities = tuple(child.maturity_id for child in self.children)
        if parent_evaluable:
            if child_maturities != self.parent.participating_maturities:
                raise ValueError(
                    "evaluable SSVI parent requires one ordered child per maturity"
                )
        elif self.children:
            raise ValueError("non-evaluable SSVI parent cannot retain children")


def _freeze_mapping(value: Mapping[str, Any]) -> _FrozenDict:
    return _FrozenDict(
        {
            key: _freeze_mapping(item) if isinstance(item, Mapping) else item
            for key, item in value.items()
        }
    )


def _precheck_and_deduplicate_starts(
    generated: Sequence[_IndexedStart],
    precheck: Callable[[np.ndarray], bool],
) -> tuple[tuple[_IndexedStart, ...], int, int]:
    precheck_discarded = 0
    duplicate_discarded = 0
    kept: list[_IndexedStart] = []
    exact_keys: set[tuple[float, ...]] = set()
    for item in generated:
        if not precheck(item.parameters):
            precheck_discarded += 1
            continue
        key = tuple(float(value) for value in item.parameters)
        if key in exact_keys:
            duplicate_discarded += 1
            continue
        exact_keys.add(key)
        kept.append(item)
    return tuple(kept), precheck_discarded, duplicate_discarded


def _bound_slacks(
    parameters: Sequence[float] | np.ndarray,
    bounds: Sequence[tuple[float, float]],
) -> tuple[float, ...]:
    values = np.asarray(parameters, dtype=np.float64)
    if values.shape != (len(bounds),):
        raise ValueError("parameter vector and bounds do not match")
    slacks: list[float] = []
    for value, (lower, upper) in zip(values, bounds, strict=True):
        slacks.extend((float(value - lower), float(upper - value)))
    return tuple(slacks)


def _all_nonnegative_finite(values: Sequence[float]) -> bool:
    array = np.asarray(values, dtype=np.float64)
    return bool(np.isfinite(array).all() and np.all(array >= 0.0))


def _prepare_ssvi_starts(
    expiries: Sequence[_LocalExpiryInput],
    policy: FitPolicy,
) -> _PreparedStarts:
    ordered = tuple(sorted(expiries, key=lambda item: (item.time_to_expiry, item.maturity_id)))
    if not ordered or any(item.node_count < 4 for item in ordered):
        raise ValueError("SSVI starts require one or more four-node maturities")
    maximum_observed = max(float(np.max(item.total_variance)) for item in ordered)
    theta_upper = min(
        policy.ssvi_theta_upper_cap,
        max(
            policy.ssvi_theta_upper_floor,
            policy.ssvi_theta_upper_observed_multiplier * maximum_observed,
        ),
    )
    theta_seed: list[float] = []
    for expiry in ordered:
        if expiry.k[0] <= 0.0 <= expiry.k[-1]:
            value = float(np.interp(np.float64(0.0), expiry.k, expiry.total_variance))
        else:
            value = float(expiry.total_variance[int(np.argmin(np.abs(expiry.k)))])
        theta_seed.append(value)
    theta_initial = np.clip(
        np.maximum.accumulate(np.asarray(theta_seed, dtype=np.float64)),
        policy.variance_floor,
        theta_upper,
    )
    bounds = tuple(
        [(policy.variance_floor, theta_upper)] * len(ordered)
        + [
            policy.ssvi_rho_bounds,
            (policy.constraint_margin, policy.ssvi_eta_upper),
            policy.ssvi_gamma_bounds,
        ]
    )
    generated: list[_IndexedStart] = []
    for rho in policy.ssvi_start_seeds["rho"]:
        for gamma in policy.ssvi_start_seeds["gamma"]:
            theta = theta_initial
            cap_one = (
                policy.ssvi_barrier_limit - policy.constraint_margin
            ) / (theta ** (1.0 - float(gamma)) * (1.0 + abs(float(rho))))
            cap_two = np.sqrt(
                (policy.ssvi_barrier_limit - policy.constraint_margin)
                / (theta ** (1.0 - 2.0 * float(gamma)) * (1.0 + abs(float(rho))))
            )
            eta_cap = float(min(float(np.min(cap_one)), float(np.min(cap_two))))
            for eta_seed in policy.ssvi_start_seeds["eta"]:
                eta = min(float(eta_seed), policy.ssvi_eta_cap_multiplier * eta_cap)
                parameters = np.asarray(
                    [*theta_initial, float(rho), eta, float(gamma)], dtype=np.float64
                )
                generated.append(_IndexedStart(len(generated), parameters))

    def precheck(parameters: np.ndarray) -> bool:
        if not np.isfinite(parameters).all():
            return False
        if not _all_nonnegative_finite(_bound_slacks(parameters, bounds)):
            return False
        theta = parameters[: len(ordered)]
        rho, eta, gamma = parameters[-3:]
        if eta < policy.constraint_margin:
            return False
        return _all_nonnegative_finite(
            tuple(
                _ssvi_constraint_slacks(
                    theta,
                    rho=float(rho),
                    eta=float(eta),
                    gamma=float(gamma),
                    policy=policy,
                ).values()
            )
        )

    kept, precheck_count, duplicate_count = _precheck_and_deduplicate_starts(
        generated, precheck
    )
    return _PreparedStarts(
        generated_count=policy.ssvi_generated_start_count,
        precheck_discarded_count=precheck_count,
        duplicate_discarded_count=duplicate_count,
        starts=kept,
        bounds=bounds,
        theta_upper=float(theta_upper),
        theta_initial=theta_initial,
    )


def _prepare_raw_svi_starts(
    expiry: _LocalExpiryInput,
    policy: FitPolicy,
) -> _PreparedStarts:
    if expiry.node_count < 5:
        raise ValueError("Raw-SVI starts require at least five nodes")
    w_scale = max(float(np.median(expiry.total_variance)), policy.raw_svi_w_scale_floor)
    span = max(float(expiry.k[-1] - expiry.k[0]), policy.raw_svi_span_floor)
    bounds = (
        (-policy.raw_svi_a_bound_multiplier * w_scale, policy.raw_svi_a_bound_multiplier * w_scale),
        (policy.constraint_margin, policy.raw_svi_b_upper - policy.constraint_margin),
        policy.raw_svi_rho_bounds,
        (
            float(expiry.k[0] - policy.raw_svi_m_span_multiplier * span),
            float(expiry.k[-1] + policy.raw_svi_m_span_multiplier * span),
        ),
        (
            policy.constraint_margin,
            max(policy.raw_svi_sigma_upper_floor, policy.raw_svi_sigma_span_multiplier * span),
        ),
    )
    a_initial = max(
        policy.constraint_margin,
        policy.raw_svi_a_initial_multiplier * float(np.min(expiry.total_variance)),
    )
    minimum_mask = expiry.total_variance == np.min(expiry.total_variance)
    k_at_minimum = float(np.min(expiry.k[minimum_mask]))
    median_k = float(np.median(expiry.k))
    sigma_seeds = (
        max(span / 10.0, 0.01),
        max(span / 2.0, 0.05),
    )
    generated: list[_IndexedStart] = []
    for rho in policy.raw_svi_start_seeds["rho"]:
        b_cap = (
            policy.raw_svi_b_clip_multiplier
            * (policy.raw_svi_b_upper - policy.constraint_margin)
            / (1.0 + abs(float(rho)))
        )
        for b_seed in policy.raw_svi_start_seeds["b"]:
            b = float(
                np.clip(
                    min(float(b_seed), b_cap),
                    bounds[1][0],
                    bounds[1][1],
                )
            )
            for m_seed in (k_at_minimum, median_k):
                for sigma_seed in sigma_seeds:
                    generated.append(
                        _IndexedStart(
                            len(generated),
                            np.asarray(
                                [a_initial, b, float(rho), m_seed, sigma_seed],
                                dtype=np.float64,
                            ),
                        )
                    )

    def precheck(parameters: np.ndarray) -> bool:
        if not np.isfinite(parameters).all():
            return False
        if not _all_nonnegative_finite(_bound_slacks(parameters, bounds)):
            return False
        return _all_nonnegative_finite(
            tuple(_raw_svi_constraint_slacks(parameters, policy).values())
        )

    kept, precheck_count, duplicate_count = _precheck_and_deduplicate_starts(
        generated, precheck
    )
    return _PreparedStarts(
        generated_count=policy.raw_svi_generated_start_count,
        precheck_discarded_count=precheck_count,
        duplicate_discarded_count=duplicate_count,
        starts=kept,
        bounds=bounds,
        w_scale=float(w_scale),
        span=float(span),
    )


def _formatted_parameter_key(
    outcome: _StartOutcome,
    policy: FitPolicy,
) -> tuple[str, ...]:
    if outcome.parameters is None or not all(
        math.isfinite(float(value)) for value in outcome.parameters
    ):
        return policy.failure_parameter_high_sentinel
    return tuple(format(float(value), policy.parameter_format) for value in outcome.parameters)


def _finite_or_infinity(value: float | None) -> float:
    if value is None or not math.isfinite(float(value)):
        return float("inf")
    return float(value)


def _failure_sort_key(
    outcome: _StartOutcome,
    policy: FitPolicy,
) -> tuple[object, ...]:
    primary_priority = outcome.hard_failures[0][0] if outcome.hard_failures else 10
    return (
        -outcome.stage_reached,
        len(outcome.hard_failures),
        primary_priority,
        _finite_or_infinity(outcome.max_nrmse),
        _finite_or_infinity(outcome.objective),
        _finite_or_infinity(outcome.max_constraint_violation),
        _formatted_parameter_key(outcome, policy),
        outcome.start_index,
    )


def _select_start_outcome(
    outcomes: Sequence[_StartOutcome],
    policy: FitPolicy,
) -> tuple[_StartOutcome, Literal["local_success", "failure_representative"]]:
    if not outcomes:
        raise ValueError("cannot select from an empty outcome set")
    successful = [
        outcome
        for outcome in outcomes
        if outcome.local_success
        and outcome.objective is not None
        and outcome.max_nrmse is not None
    ]
    if successful:
        minimum_objective = min(float(outcome.objective) for outcome in successful)
        tolerance = policy.near_tie_relative_tolerance * max(
            1.0, abs(minimum_objective)
        )
        near = [
            outcome
            for outcome in successful
            if float(outcome.objective) <= minimum_objective + tolerance
        ]
        return (
            min(
                near,
                key=lambda outcome: (
                    float(outcome.max_nrmse),
                    _formatted_parameter_key(outcome, policy),
                    outcome.start_index,
                ),
            ),
            "local_success",
        )
    return min(outcomes, key=lambda outcome: _failure_sort_key(outcome, policy)), "failure_representative"


def _fit_metrics_for_curve(
    curve: CurveModel,
    expiry: _LocalExpiryInput,
    fitted_total_variance: np.ndarray,
    policy: FitPolicy,
) -> dict[str, float | None]:
    metrics: dict[str, float | None] = _fit_error_metrics(
        expiry.total_variance, fitted_total_variance, policy
    )
    if np.all(fitted_total_variance > 0.0):
        fitted_iv = np.sqrt(fitted_total_variance / expiry.time_to_expiry)
        metrics["rmse_iv"] = float(
            np.sqrt(np.mean((fitted_iv - expiry.implied_volatility) ** 2, dtype=np.float64))
        )
    else:
        metrics["rmse_iv"] = None
    return metrics


def _check_gate_failures(
    checks_by_expiry: Sequence[Mapping[str, CheckDiagnostic]],
    *,
    include_butterfly: bool,
) -> tuple[tuple[int, str], ...]:
    gates: tuple[tuple[int, str, str], ...] = (
        (5, "positive_total_variance", "non_positive_total_variance"),
        (6, "call_price_monotonic", "call_price_monotonicity_failed"),
        (7, "call_price_convex", "call_price_convexity_failed"),
        (8, "butterfly_g_nonnegative", "butterfly_failed"),
        (9, "jump_reliable", "abnormal_jump"),
    )
    failures: list[tuple[int, str]] = []
    for priority, check_name, failure_code in gates:
        if priority == 8 and not include_butterfly:
            continue
        statuses = [checks[check_name].status for checks in checks_by_expiry]
        if CheckStatus.FAILED in statuses:
            failures.append((priority, failure_code))
        elif CheckStatus.INDETERMINATE in statuses:
            failures.append((priority, "check_resolution_limit"))
    return tuple(failures)


def _maximum_constraint_violation(slacks: Sequence[float]) -> float | None:
    values = np.asarray(slacks, dtype=np.float64)
    if values.ndim != 1 or not np.isfinite(values).all():
        return None
    return float(max(0.0, -float(np.min(values))))


def _optimizer_message(result: object | None) -> str | None:
    if result is None:
        return None
    try:
        value = getattr(result, "message", None)
        return None if value is None else str(value)
    except Exception:
        return None


def _exception_message(error: BaseException) -> str:
    try:
        return str(error)
    except Exception:
        return type(error).__name__


def _evaluate_raw_start_outcome(
    *,
    start_index: int,
    optimizer_result: object | None,
    optimizer_exception: BaseException | None,
    expiry: _LocalExpiryInput,
    bounds: Sequence[tuple[float, float]],
    policy: FitPolicy,
) -> _StartOutcome:
    if optimizer_exception is not None:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=False,
            parameters=None,
            objective=None,
            stage_reached=0,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=((0, "optimizer_exception"),),
            payload=None,
            optimizer_message=_exception_message(optimizer_exception),
        )
    try:
        optimizer_success = bool(getattr(optimizer_result, "success", False))
    except Exception:
        optimizer_success = False
    hard_failures: list[tuple[int, str]] = []
    if not optimizer_success:
        hard_failures.append((1, "optimizer_failed"))
    try:
        values = np.asarray(getattr(optimizer_result, "x", []), dtype=np.float64)
    except Exception:
        values = np.asarray([], dtype=np.float64)
    if values.shape != (5,) or not np.isfinite(values).all():
        hard_failures.append((2, "non_finite_parameters"))
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=None,
            objective=None,
            stage_reached=0,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(hard_failures),
            payload=None,
            optimizer_message=_optimizer_message(optimizer_result),
        )
    parameter_tuple = tuple(float(value) for value in values)
    objective: float | None = None
    try:
        candidate_objective = _raw_svi_objective(
            values, expiry.k, expiry.total_variance, policy
        )
        if math.isfinite(candidate_objective):
            objective = float(candidate_objective)
    except Exception:
        objective = None
    try:
        curve = _create_raw_svi_curve(
            time_to_expiry=expiry.time_to_expiry,
            k_min=float(expiry.k[0]),
            k_max=float(expiry.k[-1]),
            raw_k=expiry.k,
            parameters=values,
        )
        fitted = _curve_values(curve, expiry.k)
        if not np.isfinite(fitted).all():
            raise ValueError("non-finite fitted node")
    except Exception:
        hard_failures.append((2, "non_finite_parameters"))
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=1,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(sorted(hard_failures)),
            payload=None,
            optimizer_message=_optimizer_message(optimizer_result),
        )
    payload = _StartPayload(curves=(curve,), metrics=(None,), checks=(None,))
    try:
        slacks = (
            *_bound_slacks(values, bounds),
            *_raw_svi_constraint_slacks(values, policy).values(),
        )
        max_violation = _maximum_constraint_violation(slacks)
    except Exception as exc:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=2,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(sorted(hard_failures)),
            payload=payload,
            optimizer_message=_exception_message(exc),
        )
    if max_violation is None:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=2,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(sorted(hard_failures)),
            payload=payload,
            optimizer_message="constraint evaluation was non-finite",
        )
    if max_violation > 0.0:
        hard_failures.append((3, "parameter_constraint_failed"))
    try:
        metrics = _fit_metrics_for_curve(curve, expiry, fitted, policy)
        maximum_nrmse = float(metrics["nrmse_total_variance"])
        if not math.isfinite(maximum_nrmse):
            raise ValueError("non-finite normalized fit error")
        if maximum_nrmse > policy.nrmse_limit:
            hard_failures.append((4, "rmse_exceeded"))
    except Exception as exc:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=3,
            max_nrmse=None,
            max_constraint_violation=max_violation,
            hard_failures=tuple(sorted(hard_failures)),
            payload=payload,
            optimizer_message=_exception_message(exc),
        )
    payload = _StartPayload(curves=(curve,), metrics=(metrics,), checks=(None,))
    try:
        checks = _run_local_checks(
            curve, expiry.k, expiry.implied_volatility, policy
        )
        hard_failures.extend(
            _check_gate_failures((checks,), include_butterfly=True)
        )
    except Exception as exc:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=3,
            max_nrmse=maximum_nrmse,
            max_constraint_violation=max_violation,
            hard_failures=tuple(sorted(hard_failures)),
            payload=payload,
            optimizer_message=_exception_message(exc),
        )
    payload = _StartPayload(curves=(curve,), metrics=(metrics,), checks=(checks,))
    return _StartOutcome(
        start_index=start_index,
        optimizer_success=optimizer_success,
        parameters=parameter_tuple,
        objective=objective,
        stage_reached=4,
        max_nrmse=maximum_nrmse,
        max_constraint_violation=max_violation,
        hard_failures=tuple(sorted(hard_failures)),
        payload=payload,
        optimizer_message=_optimizer_message(optimizer_result),
    )


def _evaluate_ssvi_start_outcome(
    *,
    start_index: int,
    optimizer_result: object | None,
    optimizer_exception: BaseException | None,
    expiries: Sequence[_LocalExpiryInput],
    bounds: Sequence[tuple[float, float]],
    policy: FitPolicy,
) -> _StartOutcome:
    if optimizer_exception is not None:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=False,
            parameters=None,
            objective=None,
            stage_reached=0,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=((0, "optimizer_exception"),),
            payload=None,
            optimizer_message=_exception_message(optimizer_exception),
        )
    try:
        optimizer_success = bool(getattr(optimizer_result, "success", False))
    except Exception:
        optimizer_success = False
    hard_failures: list[tuple[int, str]] = []
    if not optimizer_success:
        hard_failures.append((1, "optimizer_failed"))
    expected_size = len(expiries) + 3
    try:
        values = np.asarray(getattr(optimizer_result, "x", []), dtype=np.float64)
    except Exception:
        values = np.asarray([], dtype=np.float64)
    if values.shape != (expected_size,) or not np.isfinite(values).all():
        hard_failures.append((2, "non_finite_parameters"))
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=None,
            objective=None,
            stage_reached=0,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(hard_failures),
            payload=None,
            optimizer_message=_optimizer_message(optimizer_result),
        )
    parameter_tuple = tuple(float(value) for value in values)
    theta_values = values[: len(expiries)]
    rho, eta, gamma = (float(value) for value in values[-3:])
    objective: float | None = None
    try:
        candidate_objective = _ssvi_objective(
            values,
            tuple(expiry.k for expiry in expiries),
            tuple(expiry.total_variance for expiry in expiries),
            policy,
        )
        if math.isfinite(candidate_objective):
            objective = float(candidate_objective)
    except Exception:
        objective = None
    try:
        curves = tuple(
            _create_ssvi_curve(
                time_to_expiry=expiry.time_to_expiry,
                k_min=float(expiry.k[0]),
                k_max=float(expiry.k[-1]),
                raw_k=expiry.k,
                theta=float(theta),
                rho=rho,
                eta=eta,
                gamma=gamma,
            )
            for expiry, theta in zip(expiries, theta_values, strict=True)
        )
        fitted_values = tuple(
            _curve_values(curve, expiry.k)
            for curve, expiry in zip(curves, expiries, strict=True)
        )
        if any(not np.isfinite(values_at_nodes).all() for values_at_nodes in fitted_values):
            raise ValueError("non-finite fitted node")
    except Exception:
        hard_failures.append((2, "non_finite_parameters"))
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=1,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(sorted(hard_failures)),
            payload=None,
            optimizer_message=_optimizer_message(optimizer_result),
        )
    empty_metrics: tuple[dict[str, float | None] | None, ...] = tuple(
        None for _ in expiries
    )
    empty_checks: tuple[dict[str, CheckDiagnostic] | None, ...] = tuple(
        None for _ in expiries
    )
    payload = _StartPayload(
        curves=curves, metrics=empty_metrics, checks=empty_checks
    )
    try:
        slacks = (
            *_bound_slacks(values, bounds),
            *_ssvi_constraint_slacks(
                theta_values,
                rho=rho,
                eta=eta,
                gamma=gamma,
                policy=policy,
            ).values(),
        )
        max_violation = _maximum_constraint_violation(slacks)
    except Exception as exc:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=2,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(sorted(hard_failures)),
            payload=payload,
            optimizer_message=_exception_message(exc),
        )
    if max_violation is None:
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=2,
            max_nrmse=None,
            max_constraint_violation=None,
            hard_failures=tuple(sorted(hard_failures)),
            payload=payload,
            optimizer_message="constraint evaluation was non-finite",
        )
    if max_violation > 0.0:
        hard_failures.append((3, "parameter_constraint_failed"))
    metrics_progress: list[dict[str, float | None] | None] = [
        None for _ in expiries
    ]
    try:
        for index, (curve, expiry, fitted) in enumerate(
            zip(curves, expiries, fitted_values, strict=True)
        ):
            metrics_progress[index] = _fit_metrics_for_curve(
                curve, expiry, fitted, policy
            )
        maximum_nrmse = max(
            float(item["nrmse_total_variance"])
            for item in metrics_progress
            if item is not None
        )
        if not math.isfinite(maximum_nrmse):
            raise ValueError("non-finite normalized fit error")
        if maximum_nrmse > policy.nrmse_limit:
            hard_failures.append((4, "rmse_exceeded"))
    except Exception as exc:
        known_nrmse_values: list[float] = []
        for item in metrics_progress:
            if item is None:
                continue
            try:
                known_nrmse = float(item["nrmse_total_variance"])
            except (KeyError, TypeError, ValueError):
                continue
            if math.isfinite(known_nrmse):
                known_nrmse_values.append(known_nrmse)
        known_maximum_nrmse = (
            max(known_nrmse_values) if known_nrmse_values else None
        )
        if (
            known_maximum_nrmse is not None
            and known_maximum_nrmse > policy.nrmse_limit
        ):
            hard_failures.append((4, "rmse_exceeded"))
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=3,
            max_nrmse=known_maximum_nrmse,
            max_constraint_violation=max_violation,
            hard_failures=tuple(sorted(hard_failures)),
            payload=_StartPayload(
                curves=curves,
                metrics=tuple(metrics_progress),
                checks=empty_checks,
            ),
            optimizer_message=_exception_message(exc),
        )
    metrics = tuple(metrics_progress)
    checks_progress: list[dict[str, CheckDiagnostic] | None] = [
        None for _ in expiries
    ]
    try:
        for index, (curve, expiry) in enumerate(
            zip(curves, expiries, strict=True)
        ):
            checks_progress[index] = _run_local_checks(
                curve, expiry.k, expiry.implied_volatility, policy
            )
        completed_checks = tuple(
            item for item in checks_progress if item is not None
        )
        if len(completed_checks) != len(expiries):
            raise ValueError("not all local checks completed")
        hard_failures.extend(
            _check_gate_failures(completed_checks, include_butterfly=True)
        )
    except Exception as exc:
        resolved_checks = tuple(
            _fail_closed_local_checks() if item is None else item
            for item in checks_progress
        )
        hard_failures.extend(
            _check_gate_failures(resolved_checks, include_butterfly=True)
        )
        return _StartOutcome(
            start_index=start_index,
            optimizer_success=optimizer_success,
            parameters=parameter_tuple,
            objective=objective,
            stage_reached=3,
            max_nrmse=maximum_nrmse,
            max_constraint_violation=max_violation,
            hard_failures=tuple(sorted(hard_failures)),
            payload=_StartPayload(
                curves=curves,
                metrics=metrics,
                checks=tuple(checks_progress),
            ),
            optimizer_message=_exception_message(exc),
        )
    checks = tuple(checks_progress)
    return _StartOutcome(
        start_index=start_index,
        optimizer_success=optimizer_success,
        parameters=parameter_tuple,
        objective=objective,
        stage_reached=4,
        max_nrmse=maximum_nrmse,
        max_constraint_violation=max_violation,
        hard_failures=tuple(sorted(hard_failures)),
        payload=_StartPayload(curves=curves, metrics=metrics, checks=checks),
        optimizer_message=_optimizer_message(optimizer_result),
    )


def _optimizer_summary(
    plan: _PreparedStarts,
    outcomes: Sequence[_StartOutcome],
    selected: _StartOutcome | None,
    selection_kind: Literal["local_success", "failure_representative"] | None,
) -> OptimizerStartSummary:
    return OptimizerStartSummary(
        generated_count=plan.generated_count,
        precheck_discarded_count=plan.precheck_discarded_count,
        duplicate_discarded_count=plan.duplicate_discarded_count,
        executed_count=len(outcomes),
        optimizer_reported_success_count=sum(
            outcome.optimizer_success for outcome in outcomes
        ),
        evaluable_count=sum(outcome.stage_reached >= 2 for outcome in outcomes),
        local_success_count=sum(outcome.local_success for outcome in outcomes),
        selected_start_index=None if selected is None else selected.start_index,
        selection_kind=selection_kind,
    )


def _candidate_arrays(
    curve: CurveModel,
    expiry: _LocalExpiryInput,
    policy: FitPolicy,
) -> tuple[tuple[float, ...], tuple[float | None, ...], tuple[float | None, ...]]:
    grid = diagnostic_curve_grid(
        float(expiry.k[0]), float(expiry.k[-1]), expiry.k, policy
    )
    evaluated = evaluate_curve(curve, grid)
    return (
        tuple(float(value) for value in grid),
        tuple(
            None if value is None else float(value)
            for value in evaluated.total_variance
        ),
        tuple(None if value is None else float(value) for value in evaluated.iv),
    )


def _null_fit_metrics() -> dict[str, float | None]:
    return {
        "rmse_total_variance": None,
        "nrmse_total_variance": None,
        "rmse_iv": None,
    }


def _all_not_run_checks() -> _FrozenDict:
    return _FrozenDict({name: _not_run_check(name) for name in CHECK_NAMES})


def _fail_closed_local_checks(
    check_name: str = "positive_total_variance",
) -> _FrozenDict:
    checks = {name: _not_run_check(name) for name in CHECK_NAMES}
    checks[check_name] = _indeterminate_check(
        check_name,
        primary_value=None,
        threshold=None,
        grid_point_count=0,
        metrics={"incomplete_stage": True},
    )
    return _FrozenDict(checks)


def _candidate_sampling_failure_checks(method: FitMethod) -> _FrozenDict:
    checks = {name: _not_run_check(name) for name in CHECK_NAMES}
    checks["positive_total_variance"] = _indeterminate_check(
        "positive_total_variance",
        primary_value=None,
        threshold=None,
        grid_point_count=0,
        metrics={"candidate_sampling_failed": True},
    )
    if method in {FitMethod.PCHIP, FitMethod.LINEAR}:
        checks["butterfly_g_nonnegative"] = CheckDiagnostic(
            name="butterfly_g_nonnegative",
            status=CheckStatus.NOT_APPLICABLE,
            conclusion="not_applicable",
            reason_code="method_has_no_analytic_g",
            primary_value=None,
            threshold=None,
            violation_count=None,
            grid_point_count=0,
            metrics={},
        )
    return _FrozenDict(checks)


def _resolved_draft_checks(
    checks: Mapping[str, CheckDiagnostic] | None,
    failure_code: str | None,
) -> _FrozenDict:
    if checks is not None:
        return _FrozenDict(checks)
    if failure_code == "check_resolution_limit":
        return _fail_closed_local_checks()
    return _all_not_run_checks()


def _selected_draft_failure_code(
    selected: _StartOutcome | None,
) -> str | None:
    if selected is None:
        return "optimizer_failed"
    if selected.primary_failure_code is not None:
        return selected.primary_failure_code
    if not selected.local_success:
        return "check_resolution_limit"
    return None


def _per_expiry_metric(
    expiry: _LocalExpiryInput,
    metrics: Mapping[str, float | None] | None,
    checks: Mapping[str, CheckDiagnostic] | None,
) -> PerExpiryMetric:
    resolved_metrics = _null_fit_metrics() if metrics is None else metrics
    resolved_checks = _all_not_run_checks() if checks is None else checks
    return PerExpiryMetric(
        maturity_id=expiry.maturity_id,
        time_to_expiry=expiry.time_to_expiry,
        raw_node_count=expiry.raw_node_count,
        node_count=expiry.node_count,
        k_min=float(expiry.k[0]),
        k_max=float(expiry.k[-1]),
        rmse_total_variance=resolved_metrics["rmse_total_variance"],
        nrmse_total_variance=resolved_metrics["nrmse_total_variance"],
        rmse_iv=resolved_metrics["rmse_iv"],
        checks=_FrozenDict(resolved_checks),
    )


def _local_failure_from_metrics_and_checks(
    metrics: Mapping[str, float | None],
    checks: Mapping[str, CheckDiagnostic],
    method: FitMethod,
    policy: FitPolicy,
) -> str | None:
    nrmse = metrics["nrmse_total_variance"]
    if nrmse is None or float(nrmse) > policy.nrmse_limit:
        return "rmse_exceeded"
    failures = _check_gate_failures(
        (checks,), include_butterfly=method in {FitMethod.SSVI, FitMethod.RAW_SVI}
    )
    return failures[0][1] if failures else None


def _expiry_candidate_from_curve(
    *,
    expiry: _LocalExpiryInput,
    method: FitMethod,
    curve: CurveModel | None,
    metrics: Mapping[str, float | None] | None,
    checks: Mapping[str, CheckDiagnostic] | None,
    optimizer_attempted: bool,
    optimizer_success: bool | None,
    optimizer_start_summary: OptimizerStartSummary | None,
    parameters: Mapping[str, Any] | None,
    local_success: bool,
    failure_code: str | None,
    failure_reason: str | None,
    policy: FitPolicy,
) -> _LocalFitCandidate:
    resolved_metrics = _null_fit_metrics() if metrics is None else metrics
    resolved_checks = _resolved_draft_checks(checks, failure_code)
    if curve is None:
        candidate_k: tuple[float, ...] = ()
        candidate_w: tuple[float | None, ...] = ()
        candidate_iv: tuple[float | None, ...] = ()
    else:
        sampling_failed = False
        try:
            candidate_k, candidate_w, candidate_iv = _candidate_arrays(
                curve, expiry, policy
            )
        except Exception:
            candidate_k, candidate_w, candidate_iv = (), (), ()
            sampling_failed = local_success
        if sampling_failed:
            resolved_checks = _candidate_sampling_failure_checks(method)
            local_success = False
            failure_code = "check_resolution_limit"
            failure_reason = "diagnostic candidate sampling failed"
    return _LocalFitCandidate(
        scope=AttemptScope.EXPIRY,
        maturity_id=expiry.maturity_id,
        participating_maturities=(),
        time_to_expiry=expiry.time_to_expiry,
        method=method,
        optimizer_attempted=optimizer_attempted,
        optimizer_success=optimizer_success,
        optimizer_start_summary=optimizer_start_summary,
        local_success=local_success,
        parameters=parameters,
        per_expiry_metrics=None,
        rmse_total_variance=resolved_metrics["rmse_total_variance"],
        nrmse_total_variance=resolved_metrics["nrmse_total_variance"],
        rmse_iv=resolved_metrics["rmse_iv"],
        raw_node_count=expiry.raw_node_count,
        node_count=expiry.node_count,
        k_min=float(expiry.k[0]),
        k_max=float(expiry.k[-1]),
        candidate_k=candidate_k,
        candidate_total_variance=candidate_w,
        candidate_iv=candidate_iv,
        checks=resolved_checks,
        failure_code=failure_code,
        failure_reason=failure_reason,
        curve=curve,
    )


def fit_raw_svi_local(
    expiry: _LocalExpiryInput,
    *,
    policy: FitPolicy | None = None,
) -> _LocalFitCandidate | None:
    """Run the deterministic Raw-SVI local stage without calendar selection."""

    active_policy = FitPolicy() if policy is None else policy
    if not isinstance(expiry, _LocalExpiryInput):
        raise ValueError("expiry must be _LocalExpiryInput")
    if expiry.node_count < 5:
        return None
    plan = _prepare_raw_svi_starts(expiry, active_policy)
    outcomes: list[_StartOutcome] = []

    def analytic_constraints(parameters: np.ndarray) -> np.ndarray:
        return np.asarray(
            tuple(_raw_svi_constraint_slacks(parameters, active_policy).values()),
            dtype=np.float64,
        )

    for start in plan.starts:
        result: object | None = None
        error: BaseException | None = None
        try:
            result = minimize(
                lambda parameters: _raw_svi_objective(
                    np.asarray(parameters, dtype=np.float64),
                    expiry.k,
                    expiry.total_variance,
                    active_policy,
                ),
                np.asarray(start.parameters, dtype=np.float64),
                method=active_policy.slsqp_method,
                bounds=plan.bounds,
                constraints=({"type": "ineq", "fun": analytic_constraints},),
                options=dict(active_policy.slsqp_options),
            )
        except Exception as exc:
            error = exc
        outcomes.append(
            _evaluate_raw_start_outcome(
                start_index=start.start_index,
                optimizer_result=result,
                optimizer_exception=error,
                expiry=expiry,
                bounds=plan.bounds,
                policy=active_policy,
            )
        )
    if outcomes:
        selected, selection_kind = _select_start_outcome(outcomes, active_policy)
    else:
        selected, selection_kind = None, None
    summary = _optimizer_summary(plan, outcomes, selected, selection_kind)
    parameters = (
        None
        if selected is None or selected.parameters is None
        else {
            name: float(value)
            for name, value in zip(
                active_policy.raw_svi_variable_order,
                selected.parameters,
                strict=True,
            )
        }
    )
    payload = None if selected is None else selected.payload
    curve = None if payload is None or not payload.curves else payload.curves[0]
    metrics = None if payload is None or not payload.metrics else payload.metrics[0]
    checks = None if payload is None or not payload.checks else payload.checks[0]
    local_success = selected is not None and selected.local_success
    failure_code = _selected_draft_failure_code(selected)
    return _expiry_candidate_from_curve(
        expiry=expiry,
        method=FitMethod.RAW_SVI,
        curve=curve,
        metrics=metrics,
        checks=checks,
        optimizer_attempted=True,
        optimizer_success=False if selected is None else selected.optimizer_success,
        optimizer_start_summary=summary,
        parameters=parameters,
        local_success=local_success,
        failure_code=failure_code,
        failure_reason=(
            None
            if local_success
            else "no executable optimizer start"
            if selected is None
            else selected.optimizer_message or failure_code
        ),
        policy=active_policy,
    )


def _aggregate_ssvi_parent_checks(
    checks_by_expiry: Sequence[Mapping[str, CheckDiagnostic]],
) -> _FrozenDict:
    aggregated: dict[str, CheckDiagnostic] = {
        "calendar_consistent": _not_run_check("calendar_consistent")
    }
    blocked = False
    for name in HARD_GATE_CHECK_ORDER:
        if blocked:
            aggregated[name] = _not_run_check(name)
            continue
        candidates = [checks[name] for checks in checks_by_expiry]
        chosen = next(
            (item for item in candidates if item.status is CheckStatus.FAILED),
            None,
        )
        if chosen is None:
            chosen = next(
                (
                    item
                    for item in candidates
                    if item.status is CheckStatus.INDETERMINATE
                ),
                candidates[0],
            )
        aggregated[name] = chosen
        if chosen.status in {CheckStatus.FAILED, CheckStatus.INDETERMINATE}:
            blocked = True
    return _FrozenDict({name: aggregated[name] for name in CHECK_NAMES})


def _not_enough_maturities_bundle(
    expiries: Sequence[_LocalExpiryInput],
) -> _LocalSsviBundle:
    ordered = tuple(sorted(expiries, key=lambda item: (item.time_to_expiry, item.maturity_id)))
    checks = _FrozenDict({name: _not_run_check(name) for name in CHECK_NAMES})
    parent = _LocalFitCandidate(
        scope=AttemptScope.TIMESTAMP,
        maturity_id=None,
        participating_maturities=tuple(item.maturity_id for item in ordered),
        time_to_expiry=None,
        method=FitMethod.SSVI,
        optimizer_attempted=False,
        optimizer_success=None,
        optimizer_start_summary=None,
        local_success=False,
        parameters=None,
        per_expiry_metrics=_FrozenDict(
            {
                item.maturity_id: PerExpiryMetric(
                    maturity_id=item.maturity_id,
                    time_to_expiry=item.time_to_expiry,
                    raw_node_count=item.raw_node_count,
                    node_count=item.node_count,
                    k_min=float(item.k[0]),
                    k_max=float(item.k[-1]),
                    rmse_total_variance=None,
                    nrmse_total_variance=None,
                    rmse_iv=None,
                    checks=checks,
                )
                for item in ordered
            }
        )
        if ordered
        else _FrozenDict(),
        rmse_total_variance=None,
        nrmse_total_variance=None,
        rmse_iv=None,
        raw_node_count=None,
        node_count=None,
        k_min=None,
        k_max=None,
        candidate_k=(),
        candidate_total_variance=(),
        candidate_iv=(),
        checks=checks,
        failure_code="not_enough_maturities",
        failure_reason="SSVI requires at least two maturities with four nodes",
        curve=None,
    )
    return _LocalSsviBundle(parent=parent, children=())


def fit_ssvi_local(
    expiries: Sequence[_LocalExpiryInput],
    *,
    policy: FitPolicy | None = None,
) -> _LocalSsviBundle:
    """Run the deterministic SSVI parent stage and retain evaluable child drafts."""

    active_policy = FitPolicy() if policy is None else policy
    eligible = tuple(
        sorted(
            (
                expiry
                for expiry in expiries
                if isinstance(expiry, _LocalExpiryInput) and expiry.node_count >= 4
            ),
            key=lambda item: (item.time_to_expiry, item.maturity_id),
        )
    )
    if len(eligible) < 2:
        return _not_enough_maturities_bundle(eligible)
    plan = _prepare_ssvi_starts(eligible, active_policy)
    outcomes: list[_StartOutcome] = []

    def analytic_constraints(parameters: np.ndarray) -> np.ndarray:
        values = np.asarray(parameters, dtype=np.float64)
        return np.asarray(
            tuple(
                _ssvi_constraint_slacks(
                    values[: len(eligible)],
                    rho=float(values[-3]),
                    eta=float(values[-2]),
                    gamma=float(values[-1]),
                    policy=active_policy,
                ).values()
            ),
            dtype=np.float64,
        )

    for start in plan.starts:
        result: object | None = None
        error: BaseException | None = None
        try:
            result = minimize(
                lambda parameters: _ssvi_objective(
                    np.asarray(parameters, dtype=np.float64),
                    tuple(expiry.k for expiry in eligible),
                    tuple(expiry.total_variance for expiry in eligible),
                    active_policy,
                ),
                np.asarray(start.parameters, dtype=np.float64),
                method=active_policy.slsqp_method,
                bounds=plan.bounds,
                constraints=({"type": "ineq", "fun": analytic_constraints},),
                options=dict(active_policy.slsqp_options),
            )
        except Exception as exc:
            error = exc
        outcomes.append(
            _evaluate_ssvi_start_outcome(
                start_index=start.start_index,
                optimizer_result=result,
                optimizer_exception=error,
                expiries=eligible,
                bounds=plan.bounds,
                policy=active_policy,
            )
        )
    if outcomes:
        selected, selection_kind = _select_start_outcome(outcomes, active_policy)
    else:
        selected, selection_kind = None, None
    summary = _optimizer_summary(plan, outcomes, selected, selection_kind)
    parameter_values = (
        None
        if selected is None or selected.parameters is None
        else selected.parameters
    )
    theta_values = () if parameter_values is None else parameter_values[: len(eligible)]
    rho, eta, gamma = (
        (None, None, None)
        if parameter_values is None
        else parameter_values[-3:]
    )
    payload = None if selected is None else selected.payload
    curves = () if payload is None else payload.curves
    metrics_by_expiry = (
        tuple(None for _ in eligible)
        if payload is None or len(payload.metrics) != len(eligible)
        else payload.metrics
    )
    checks_by_expiry = (
        tuple(None for _ in eligible)
        if payload is None or len(payload.checks) != len(eligible)
        else payload.checks
    )
    local_success = selected is not None and selected.local_success
    failure_code = _selected_draft_failure_code(selected)
    has_complete_child_payload = (
        parameter_values is not None and len(curves) == len(eligible)
    )
    resolved_checks_by_expiry = tuple(
        (
            _fail_closed_local_checks()
            if has_complete_child_payload
            else _all_not_run_checks()
        )
        if checks is None
        else _FrozenDict(checks)
        for checks in checks_by_expiry
    )
    per_expiry_metrics = _FrozenDict(
        {
            expiry.maturity_id: _per_expiry_metric(expiry, metrics, checks)
            for expiry, metrics, checks in zip(
                eligible,
                metrics_by_expiry,
                resolved_checks_by_expiry,
                strict=True,
            )
        }
    )
    parent_parameters = (
        None
        if parameter_values is None
        else _FrozenDict(
            {
                "rho": rho,
                "eta": eta,
                "gamma": gamma,
                "theta_by_maturity": _FrozenDict(
                    {
                        expiry.maturity_id: theta
                        for expiry, theta in zip(
                            eligible, theta_values, strict=True
                        )
                    }
                ),
            }
        )
    )
    parent_checks = _aggregate_ssvi_parent_checks(resolved_checks_by_expiry)
    parent = _LocalFitCandidate(
        scope=AttemptScope.TIMESTAMP,
        maturity_id=None,
        participating_maturities=tuple(item.maturity_id for item in eligible),
        time_to_expiry=None,
        method=FitMethod.SSVI,
        optimizer_attempted=True,
        optimizer_success=False if selected is None else selected.optimizer_success,
        optimizer_start_summary=summary,
        local_success=local_success,
        parameters=parent_parameters,
        per_expiry_metrics=per_expiry_metrics,
        rmse_total_variance=None,
        nrmse_total_variance=None,
        rmse_iv=None,
        raw_node_count=None,
        node_count=None,
        k_min=None,
        k_max=None,
        candidate_k=(),
        candidate_total_variance=(),
        candidate_iv=(),
        checks=parent_checks,
        failure_code=failure_code,
        failure_reason=(
            None
            if local_success
            else "no executable optimizer start"
            if selected is None
            else selected.optimizer_message or failure_code
        ),
        curve=None,
    )
    children: list[_LocalFitCandidate] = []
    if has_complete_child_payload:
        for expiry, theta, curve, metrics, resolved_checks in zip(
            eligible,
            theta_values,
            curves,
            metrics_by_expiry,
            resolved_checks_by_expiry,
            strict=True,
        ):
            child_failure = (
                "check_resolution_limit"
                if metrics is None
                else _local_failure_from_metrics_and_checks(
                    metrics, resolved_checks, FitMethod.SSVI, active_policy
                )
            )
            children.append(
                _expiry_candidate_from_curve(
                    expiry=expiry,
                    method=FitMethod.SSVI,
                    curve=curve,
                    metrics=metrics,
                    checks=resolved_checks,
                    optimizer_attempted=False,
                    optimizer_success=None,
                    optimizer_start_summary=None,
                    parameters={
                        "rho": rho,
                        "eta": eta,
                        "gamma": gamma,
                        "theta": theta,
                    },
                    local_success=child_failure is None,
                    failure_code=child_failure,
                    failure_reason=child_failure,
                    policy=active_policy,
                )
            )
    return _LocalSsviBundle(parent=parent, children=tuple(children))


def _build_nonparametric_local_candidate(
    expiry: _LocalExpiryInput,
    *,
    method: FitMethod,
    policy: FitPolicy,
) -> _LocalFitCandidate:
    curve = (
        _create_pchip_curve(
            time_to_expiry=expiry.time_to_expiry,
            k_nodes=expiry.k,
            total_variance_nodes=expiry.total_variance,
        )
        if method is FitMethod.PCHIP
        else _create_linear_curve(
            time_to_expiry=expiry.time_to_expiry,
            k_nodes=expiry.k,
            total_variance_nodes=expiry.total_variance,
        )
    )
    fitted = _curve_values(curve, expiry.k)
    metrics = _fit_metrics_for_curve(curve, expiry, fitted, policy)
    checks = _run_local_checks(curve, expiry.k, expiry.implied_volatility, policy)
    failure_code = _local_failure_from_metrics_and_checks(
        metrics, checks, method, policy
    )
    return _expiry_candidate_from_curve(
        expiry=expiry,
        method=method,
        curve=curve,
        metrics=metrics,
        checks=checks,
        optimizer_attempted=False,
        optimizer_success=None,
        optimizer_start_summary=None,
        parameters=None,
        local_success=failure_code is None,
        failure_code=failure_code,
        failure_reason=failure_code,
        policy=policy,
    )


def build_pchip_local_candidate(
    expiry: _LocalExpiryInput,
    *,
    policy: FitPolicy | None = None,
) -> _LocalFitCandidate | None:
    active_policy = FitPolicy() if policy is None else policy
    if not isinstance(expiry, _LocalExpiryInput):
        raise ValueError("expiry must be _LocalExpiryInput")
    if expiry.node_count < 4:
        return None
    return _build_nonparametric_local_candidate(
        expiry, method=FitMethod.PCHIP, policy=active_policy
    )


def build_linear_local_candidate(
    expiry: _LocalExpiryInput,
    *,
    policy: FitPolicy | None = None,
) -> _LocalFitCandidate | None:
    active_policy = FitPolicy() if policy is None else policy
    if not isinstance(expiry, _LocalExpiryInput):
        raise ValueError("expiry must be _LocalExpiryInput")
    if expiry.node_count not in {2, 3}:
        return None
    return _build_nonparametric_local_candidate(
        expiry, method=FitMethod.LINEAR, policy=active_policy
    )


def to_json_compatible(value: object) -> object:
    """Recursively normalize strict JSON data and reject all non-finite numbers."""

    if isinstance(value, Enum):
        return to_json_compatible(value.value)
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {
            item.name: to_json_compatible(getattr(value, item.name))
            for item in dataclasses.fields(value)
        }
    if isinstance(value, np.ndarray):
        return to_json_compatible(value.tolist())
    if isinstance(value, np.generic):
        return to_json_compatible(value.item())
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, Integral):
        return int(value)
    if isinstance(value, Real):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError("strict JSON does not permit NaN or Infinity")
        return result
    if isinstance(value, Mapping):
        normalized: dict[str, object] = {}
        for key, item in value.items():
            if isinstance(key, Enum):
                key = key.value
            if not isinstance(key, str):
                raise ValueError("strict JSON object keys must be strings")
            normalized[key] = to_json_compatible(item)
        return normalized
    if isinstance(value, (list, tuple)):
        return [to_json_compatible(item) for item in value]
    raise ValueError(f"unsupported strict JSON value: {type(value).__name__}")
````

</details>
