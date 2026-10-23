---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py>)

SHA-256：`3fa33aaa7b4587a3ca94a08bd159fe0ca8b06a8cceeee0d83a4caad8d1f4aa88`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import dataclasses
import copy
import inspect
import json
from dataclasses import FrozenInstanceError
from enum import Enum
from types import SimpleNamespace
from typing import Literal, get_args, get_type_hints

import numpy as np
import pytest

import option_risk.total_variance_fit as fit
from option_risk.total_variance_fit import (
    AttemptScope,
    AttemptStatus,
    CalendarPairDiagnostic,
    CheckDiagnostic,
    CheckStatus,
    ExpiryFitResult,
    FinalMethod,
    FitAttemptDiagnostic,
    FitMethod,
    FitPolicy,
    ForwardSource,
    InputQuality,
    OptimizerStartSummary,
    OverallStatus,
    PerExpiryMetric,
    ResultStatus,
    SurfaceGridStatus,
    TimestampStatus,
    TimestampSurfaceDiagnostic,
    diagnostic_curve_grid,
    evaluate_curve,
    to_implied_volatility,
    to_json_compatible,
    to_total_variance,
)


ATTEMPT_A = "attempt:" + "a" * 64
ATTEMPT_B = "attempt:" + "b" * 64
PAIR_A = "calendar-pair:" + "c" * 64
POLICY_VERSION = "total-variance-fit-diagnostic-v1"
TIMESTAMP = "2025-04-07T10:15:00"


def _assert_frozen_dataclass(instance: object) -> None:
    assert dataclasses.is_dataclass(instance)
    assert instance.__dataclass_params__.frozen is True
    with pytest.raises(FrozenInstanceError):
        setattr(instance, dataclasses.fields(instance)[0].name, None)


def test_nonparametric_butterfly_status_survives_an_earlier_failed_gate() -> None:
    time_to_expiry = 42.0 / 365.0
    k = np.array(
        [
            -0.212405517697334,
            -0.207183524966240,
            -0.201988711953163,
            -0.196820706129074,
        ],
        dtype=float,
    )
    iv = np.array(
        [
            0.222629219293594,
            0.289819121360779,
            0.293033242225647,
            0.292192995548248,
        ],
        dtype=float,
    )
    expiry = fit._LocalExpiryInput(
        maturity_id="42",
        time_to_expiry=time_to_expiry,
        raw_node_count=4,
        k=k,
        total_variance=iv * iv * time_to_expiry,
        implied_volatility=iv,
    )

    candidate = fit.build_pchip_local_candidate(expiry, policy=FitPolicy())

    assert candidate is not None
    assert candidate.failure_code == "call_price_convexity_failed"
    butterfly = candidate.checks["butterfly_g_nonnegative"]
    assert butterfly.status is CheckStatus.NOT_APPLICABLE
    assert butterfly.reason_code == "method_has_no_analytic_g"


def _check(
    name: str,
    status: CheckStatus = CheckStatus.PASSED,
) -> CheckDiagnostic:
    if status is CheckStatus.PASSED:
        return CheckDiagnostic(
            name=name,
            status=status,
            conclusion="sampled_no_violation",
            reason_code=None,
            primary_value=0.1,
            threshold=0.0,
            violation_count=0,
            grid_point_count=201,
            metrics={"minimum_margin": np.float64(0.1)},
        )
    if status is CheckStatus.NOT_APPLICABLE:
        reason = (
            "method_has_no_analytic_g"
            if name == "butterfly_g_nonnegative"
            else "no_prior_maturity"
            if name == "calendar_consistent"
            else "not_run"
        )
        return CheckDiagnostic(
            name=name,
            status=status,
            conclusion="not_applicable",
            reason_code=reason,
            primary_value=None,
            threshold=None,
            violation_count=None,
            grid_point_count=0,
            metrics={},
        )
    raise AssertionError("unsupported test fixture")


def _six_checks(method: FitMethod = FitMethod.PCHIP) -> dict[str, CheckDiagnostic]:
    checks = {
        name: _check(name)
        for name in (
            "positive_total_variance",
            "call_price_monotonic",
            "call_price_convex",
            "jump_reliable",
        )
    }
    checks["butterfly_g_nonnegative"] = (
        _check("butterfly_g_nonnegative")
        if method in {FitMethod.SSVI, FitMethod.RAW_SVI}
        else _check("butterfly_g_nonnegative", CheckStatus.NOT_APPLICABLE)
    )
    checks["calendar_consistent"] = _check(
        "calendar_consistent", CheckStatus.NOT_APPLICABLE
    )
    return checks


def _failed_check(name: str, reason_code: str) -> CheckDiagnostic:
    return CheckDiagnostic(
        name=name,
        status=CheckStatus.FAILED,
        conclusion="violation_found",
        reason_code=reason_code,
        primary_value=-0.01,
        threshold=0.0,
        violation_count=1,
        grid_point_count=201,
        metrics={"minimum_margin": -0.01},
    )


def _resolution_check(name: str) -> CheckDiagnostic:
    return CheckDiagnostic(
        name=name,
        status=CheckStatus.INDETERMINATE,
        conclusion="unreliable",
        reason_code="resolution_limit",
        primary_value=0.0,
        threshold=1e-8,
        violation_count=0,
        grid_point_count=257,
        metrics={"minimum_margin": 0.0},
    )


def _not_run_checks() -> dict[str, CheckDiagnostic]:
    return {
        name: CheckDiagnostic(
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
        for name in fit.CHECK_NAMES
    }


def _summary(kind: str, *, optimizer_success: bool) -> OptimizerStartSummary:
    return OptimizerStartSummary(
        generated_count=1,
        precheck_discarded_count=0,
        duplicate_discarded_count=0,
        executed_count=1,
        optimizer_reported_success_count=int(optimizer_success),
        evaluable_count=1,
        local_success_count=int(kind == "local_success"),
        selected_start_index=0,
        selection_kind=kind,
    )


def _per_expiry_metric() -> PerExpiryMetric:
    return PerExpiryMetric(
        maturity_id="ag2505",
        time_to_expiry=30.0 / 365.0,
        raw_node_count=5,
        node_count=5,
        k_min=-0.2,
        k_max=0.2,
        rmse_total_variance=0.001,
        nrmse_total_variance=0.02,
        rmse_iv=0.003,
        checks=_six_checks(FitMethod.SSVI),
    )


def _attempt(
    *,
    method: FitMethod = FitMethod.PCHIP,
    scope: AttemptScope = AttemptScope.EXPIRY,
    attempt_status: AttemptStatus = AttemptStatus.ACCEPTED,
    optimizer_success: bool | None = None,
    optimizer_start_summary: OptimizerStartSummary | None = None,
    selection_eligible: bool = True,
    blocked_by_parent: bool = False,
    local_success: bool = True,
    success: bool = True,
    failure_code: str | None = None,
) -> FitAttemptDiagnostic:
    is_parent = scope is AttemptScope.TIMESTAMP
    is_child = method is FitMethod.SSVI and not is_parent
    if method is FitMethod.SSVI:
        parameters = (
            {
                "rho": -0.2,
                "eta": 0.5,
                "gamma": 0.3,
                "theta_by_maturity": {"ag2505": 0.04},
            }
            if is_parent
            else {"rho": -0.2, "eta": 0.5, "gamma": 0.3, "theta": 0.04}
        )
    elif method is FitMethod.RAW_SVI:
        parameters = {"a": 0.01, "b": 0.2, "rho": -0.2, "m": 0.0, "sigma": 0.1}
    else:
        parameters = None
    if attempt_status is AttemptStatus.SKIPPED:
        parameters = None
    attempt_checks = (
        _not_run_checks()
        if attempt_status is AttemptStatus.SKIPPED
        else _six_checks(method)
    )
    failure_check = {
        "non_positive_total_variance": (
            "positive_total_variance",
            "below_variance_floor",
        ),
        "call_price_monotonicity_failed": (
            "call_price_monotonic",
            "call_price_increase",
        ),
        "call_price_convexity_failed": (
            "call_price_convex",
            "decreasing_secant_slope",
        ),
        "butterfly_failed": ("butterfly_g_nonnegative", "negative_g"),
        "calendar_conflict": (
            "calendar_consistent",
            "calendar_total_variance_decrease",
        ),
        "abnormal_jump": ("jump_reliable", "absolute_iv_slope_exceeded"),
    }.get(failure_code)
    if failure_check is not None and not (
        failure_code == "butterfly_failed"
        and method in {FitMethod.PCHIP, FitMethod.LINEAR}
    ):
        name, reason = failure_check
        attempt_checks[name] = _failed_check(name, reason)
    if failure_code == "check_resolution_limit":
        resolution_name = "calendar_consistent" if local_success else "jump_reliable"
        attempt_checks[resolution_name] = _resolution_check(resolution_name)
    return FitAttemptDiagnostic(
        attempt_id=ATTEMPT_A,
        parent_attempt_id=ATTEMPT_B if is_child else None,
        scope=scope,
        product="ag",
        timestamp=TIMESTAMP,
        maturity_id=None if is_parent else "ag2505",
        participating_maturities=["ag2505"] if is_parent else [],
        time_to_expiry=None if is_parent else 30.0 / 365.0,
        method=method,
        attempt_order=0,
        attempt_status=attempt_status,
        optimizer_attempted=optimizer_start_summary is not None,
        optimizer_success=optimizer_success,
        optimizer_start_summary=optimizer_start_summary,
        selection_eligible=selection_eligible,
        blocked_by_parent=blocked_by_parent,
        local_success=local_success,
        success=success,
        parameters=parameters,
        per_expiry_metrics={"ag2505": _per_expiry_metric()} if is_parent else None,
        rmse_total_variance=None if is_parent else 0.001,
        nrmse_total_variance=None if is_parent else 0.02,
        rmse_iv=None if is_parent else 0.003,
        raw_node_count=None if is_parent else 5,
        node_count=None if is_parent else 5,
        k_min=None if is_parent else -0.2,
        k_max=None if is_parent else 0.2,
        candidate_k=[] if is_parent else [-0.2, 0.0, 0.2],
        candidate_total_variance=[] if is_parent else [0.04, 0.041, 0.042],
        candidate_iv=[]
        if is_parent
        else [
            np.sqrt(0.04 / (30.0 / 365.0)),
            np.sqrt(0.041 / (30.0 / 365.0)),
            np.sqrt(0.042 / (30.0 / 365.0)),
        ],
        checks=attempt_checks,
        failure_code=failure_code,
        failure_reason=None if failure_code is None else "expected test failure",
        policy_version=POLICY_VERSION,
        forward_source=ForwardSource.UNDERLYING_PRICE_PROXY,
    )


def _expiry_result(*, usable: bool) -> ExpiryFitResult:
    time_to_expiry = 30.0 / 365.0
    fitted_w = [0.04, 0.041, 0.042]
    fitted_iv = [np.sqrt(value / time_to_expiry) for value in fitted_w]
    return ExpiryFitResult(
        maturity_id="ag2505",
        time_to_expiry=time_to_expiry,
        result_status=ResultStatus.USABLE if usable else ResultStatus.UNUSABLE,
        method=FinalMethod.PCHIP if usable else FinalMethod.UNUSABLE,
        success=usable,
        usable=usable,
        raw_k=[-0.2, 0.0, 0.2],
        raw_total_variance=fitted_w,
        raw_iv=fitted_iv,
        fit_k=[-0.2, 0.0, 0.2] if usable else [],
        fit_total_variance=fitted_w if usable else [],
        fit_iv=fitted_iv if usable else [],
        selected_attempt_id=ATTEMPT_A if usable else None,
        last_candidate_attempt_id=ATTEMPT_A,
        terminal_attempt_id=ATTEMPT_A,
        attempt_ids=[ATTEMPT_A],
        final_checks=_six_checks(),
        failure_code=None if usable else "rmse_exceeded",
        failure_reason=None if usable else "terminal candidate failed",
    )


def _accepted_attempt_and_result(
    maturity_id: str,
    time_to_expiry: float,
    attempt_order: int,
    input_fingerprint: str,
) -> tuple[FitAttemptDiagnostic, ExpiryFitResult]:
    attempt_id = fit.make_attempt_id(
        input_fingerprint=input_fingerprint,
        product="ag",
        timestamp=TIMESTAMP,
        scope=AttemptScope.EXPIRY,
        maturity_id=maturity_id,
        participating_maturities=[],
        method=FitMethod.PCHIP,
        attempt_order=attempt_order,
        policy_version=POLICY_VERSION,
    )
    attempt = dataclasses.replace(
        _attempt(),
        attempt_id=attempt_id,
        maturity_id=maturity_id,
        time_to_expiry=time_to_expiry,
        attempt_order=attempt_order,
    )
    result = dataclasses.replace(
        _expiry_result(usable=True),
        maturity_id=maturity_id,
        time_to_expiry=time_to_expiry,
        selected_attempt_id=attempt_id,
        last_candidate_attempt_id=attempt_id,
        terminal_attempt_id=attempt_id,
        attempt_ids=[attempt_id],
        fit_k=attempt.candidate_k,
        fit_total_variance=[float(value) for value in attempt.candidate_total_variance],
        fit_iv=[float(value) for value in attempt.candidate_iv],
        final_checks=attempt.checks,
    )
    return attempt, result


def _ready_timestamp(
    pairs: list[tuple[FitAttemptDiagnostic, ExpiryFitResult]],
    *,
    input_fingerprint: str,
    calendar_pair_checks: list[CalendarPairDiagnostic] | None = None,
) -> TimestampSurfaceDiagnostic:
    grid = np.linspace(-0.2, 0.2, 201).tolist()
    expiry_results = [result for _, result in pairs]
    surface_w = [[0.04 + 0.01 * index] * 201 for index in range(len(pairs))]
    surface_iv = [
        [np.sqrt(w_row[0] / result.time_to_expiry)] * 201
        for w_row, result in zip(surface_w, expiry_results, strict=True)
    ]
    zeros = {code: 0 for code in fit.INPUT_FAILURE_CODES}
    return TimestampSurfaceDiagnostic(
        product="ag",
        timestamp=TIMESTAMP,
        diagnostic_only=True,
        timestamp_status=TimestampStatus.READY,
        timestamp_failure_code=None,
        timestamp_failure_reason=None,
        forward_source=ForwardSource.UNDERLYING_PRICE_PROXY,
        observed_forward_sources=[ForwardSource.UNDERLYING_PRICE_PROXY],
        input_quality=InputQuality(
            input_row_count=5 * len(pairs),
            valid_premerge_node_count=5 * len(pairs),
            merged_node_count=5 * len(pairs),
            excluded_counts=zeros,
        ),
        ssvi_attempt=None,
        attempts=[attempt for attempt, _ in pairs],
        expiry_results=expiry_results,
        surface_grid_status=SurfaceGridStatus.AVAILABLE,
        surface_log_moneyness=grid,
        surface_time_to_expiry=[result.time_to_expiry for result in expiry_results],
        surface_total_variance=surface_w,
        surface_iv=surface_iv,
        usable_expiry_count=len(pairs),
        unusable_expiry_count=0,
        calendar_pair_checks=calendar_pair_checks or [],
        method_counts={
            FinalMethod.SSVI: 0,
            FinalMethod.RAW_SVI: 0,
            FinalMethod.PCHIP: len(pairs),
            FinalMethod.LINEAR: 0,
            FinalMethod.UNUSABLE: 0,
        },
        overall_status=OverallStatus.ALL_USABLE,
        policy_version=POLICY_VERSION,
        effective_input_fingerprint="sha256:" + "2" * 64,
        input_quality_fingerprint="sha256:" + "3" * 64,
        input_fingerprint=input_fingerprint,
    )


def _failed_input_timestamp() -> TimestampSurfaceDiagnostic:
    zeros = {code: 0 for code in fit.INPUT_FAILURE_CODES}
    observed = [
        ForwardSource.TRUE_FUTURES_FORWARD,
        ForwardSource.UNDERLYING_PRICE_PROXY,
    ]
    return TimestampSurfaceDiagnostic(
        product="ag",
        timestamp=TIMESTAMP,
        diagnostic_only=True,
        timestamp_status=TimestampStatus.FAILED_INPUT,
        timestamp_failure_code="mixed_forward_sources",
        timestamp_failure_reason=(
            "mixed forward sources: " + ",".join(item.value for item in observed)
        ),
        forward_source=None,
        observed_forward_sources=observed,
        input_quality=InputQuality(
            input_row_count=2,
            valid_premerge_node_count=2,
            merged_node_count=0,
            excluded_counts=zeros,
        ),
        ssvi_attempt=None,
        attempts=[],
        expiry_results=[],
        surface_grid_status=SurfaceGridStatus.UNAVAILABLE_INPUT_FAILURE,
        surface_log_moneyness=[],
        surface_time_to_expiry=[],
        surface_total_variance=[],
        surface_iv=[],
        usable_expiry_count=0,
        unusable_expiry_count=0,
        calendar_pair_checks=[],
        method_counts={method: 0 for method in FinalMethod},
        overall_status=OverallStatus.NONE_USABLE,
        policy_version=POLICY_VERSION,
        effective_input_fingerprint="sha256:" + "7" * 64,
        input_quality_fingerprint="sha256:" + "8" * 64,
        input_fingerprint="sha256:" + "9" * 64,
    )


def _insufficient_timestamp(input_fingerprint: str) -> TimestampSurfaceDiagnostic:
    zeros = {code: 0 for code in fit.INPUT_FAILURE_CODES}
    result = ExpiryFitResult(
        maturity_id="ag2505",
        time_to_expiry=30.0 / 365.0,
        result_status=ResultStatus.UNUSABLE,
        method=FinalMethod.UNUSABLE,
        success=False,
        usable=False,
        raw_k=[0.0],
        raw_total_variance=[0.04],
        raw_iv=[np.sqrt(0.04 / (30.0 / 365.0))],
        fit_k=[],
        fit_total_variance=[],
        fit_iv=[],
        selected_attempt_id=None,
        last_candidate_attempt_id=None,
        terminal_attempt_id=None,
        attempt_ids=[],
        final_checks=_not_run_checks(),
        failure_code="insufficient_nodes",
        failure_reason="fewer than two unique nodes",
    )
    return TimestampSurfaceDiagnostic(
        product="ag",
        timestamp=TIMESTAMP,
        diagnostic_only=True,
        timestamp_status=TimestampStatus.READY,
        timestamp_failure_code=None,
        timestamp_failure_reason=None,
        forward_source=ForwardSource.UNDERLYING_PRICE_PROXY,
        observed_forward_sources=[ForwardSource.UNDERLYING_PRICE_PROXY],
        input_quality=InputQuality(
            input_row_count=1,
            valid_premerge_node_count=1,
            merged_node_count=1,
            excluded_counts=zeros,
        ),
        ssvi_attempt=None,
        attempts=[],
        expiry_results=[result],
        surface_grid_status=SurfaceGridStatus.UNAVAILABLE_NO_SUPPORT,
        surface_log_moneyness=[],
        surface_time_to_expiry=[result.time_to_expiry],
        surface_total_variance=[[]],
        surface_iv=[[]],
        usable_expiry_count=0,
        unusable_expiry_count=1,
        calendar_pair_checks=[],
        method_counts={
            FinalMethod.SSVI: 0,
            FinalMethod.RAW_SVI: 0,
            FinalMethod.PCHIP: 0,
            FinalMethod.LINEAR: 0,
            FinalMethod.UNUSABLE: 1,
        },
        overall_status=OverallStatus.NONE_USABLE,
        policy_version=POLICY_VERSION,
        effective_input_fingerprint="sha256:" + "d" * 64,
        input_quality_fingerprint="sha256:" + "e" * 64,
        input_fingerprint=input_fingerprint,
    )


def test_fit_policy_is_frozen_exact_and_serializes_all_fixed_solver_rules() -> None:
    policy = FitPolicy()

    _assert_frozen_dataclass(policy)
    expected_core = {
        "policy_version": POLICY_VERSION,
        "base_grid_size": 201,
        "diagnostic_curve_base_size": 201,
        "surface_grid_size": 201,
        "max_refinement_depth": 8,
        "min_k_interval": 1e-6,
        "near_margin_factor": 10.0,
        "variance_floor": 1e-10,
        "constraint_margin": 1e-8,
        "nrmse_limit": 0.15,
        "price_monotonic_abs_tolerance": 1e-8,
        "price_convex_slope_tolerance": 1e-6,
        "butterfly_g_tolerance": 1e-8,
        "calendar_abs_tolerance": 1e-6,
        "calendar_rel_tolerance": 0.005,
        "max_abs_iv_slope": 5.0,
        "robust_iv_slope_floor": 0.05,
        "max_robust_slope_ratio": 10.0,
        "k_consistency_tolerance": 1e-10,
    }
    actual = dataclasses.asdict(policy)
    assert {key: actual[key] for key in expected_core} == expected_core
    assert actual["slsqp_options"] == {
        "ftol": 1e-12,
        "maxiter": 2000,
        "eps": 1e-8,
        "disp": False,
    }
    assert actual["ssvi_start_seeds"] == {
        "rho": (-0.5, 0.0, 0.5),
        "gamma": (0.1, 0.3, 0.5),
        "eta": (0.1, 0.5, 1.0),
    }
    assert actual["ssvi_generated_start_count"] == 27
    assert actual["raw_svi_start_seeds"] == {
        "rho": (-0.5, 0.0, 0.5),
        "b": (0.1, 0.5, 1.0),
        "m": ("k_at_min_w", "median_k"),
        "sigma": ("max_span_over_10_0.01", "max_span_over_2_0.05"),
    }
    assert actual["raw_svi_generated_start_count"] == 36
    assert actual["knot_neighbor_divisor"] == 100.0
    assert actual["adaptive_refinement_checks"] == (
        "positive_total_variance",
        "butterfly_g_nonnegative",
        "calendar_consistent",
    )
    assert actual["ssvi_start_loop_order"] == ("rho", "gamma", "eta")
    assert actual["raw_svi_start_loop_order"] == ("rho", "b", "m", "sigma")
    assert actual["start_precheck_order"] == (
        "finite",
        "bounds",
        "analytic_constraints",
    )
    assert actual["start_deduplication_rule"] == "float64_exact_keep_earliest_index"
    assert actual["near_tie_relative_tolerance"] == 1e-12
    assert actual["success_selection_order"] == (
        "maximum_per_expiry_nrmse",
        "formatted_parameter_tuple",
        "start_index",
    )
    assert actual["failure_representative_order"] == (
        "negative_stage_reached",
        "hard_failure_count",
        "primary_failure_priority",
        "finite_nrmse_or_positive_infinity",
        "finite_objective_or_positive_infinity",
        "finite_max_constraint_violation_or_positive_infinity",
        "formatted_parameter_tuple_or_high_sentinel",
        "start_index",
    )
    assert actual["failure_stage_order"] == (
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
    assert actual["shgo_options"] == {
        "n": 256,
        "iters": 3,
        "sampling_method": "simplicial",
        "workers": 1,
    }
    assert actual["shgo_minimizer_options"] == {
        "method": "SLSQP",
        "ftol": 1e-12,
        "maxiter": 500,
        "disp": False,
    }
    assert actual["shgo_completeness_requirements"] == (
        "success_true",
        "finite_x_and_fun",
        "nonempty_finite_equal_length_xl_funl",
        "all_x_within_closed_support",
    )
    assert actual["shgo_candidate_sources"] == (
        "k_min",
        "k_max",
        "result_x",
        "all_result_xl",
    )
    assert actual["pchip_stationary_root_rules"] == (
        "w_prime_equals_zero",
        "two_w_w_second_minus_w_prime_squared_equals_zero",
        "strip_exact_zero_leading_coefficients",
        "float64_exact_deduplication",
    )
    json.dumps(to_json_compatible(actual), allow_nan=False)


def test_v1_fit_policy_rejects_strategy_overrides_without_a_new_version() -> None:
    with pytest.raises(ValueError):
        FitPolicy(base_grid_size=101)
    with pytest.raises(ValueError):
        FitPolicy(slsqp_options={"ftol": 1e-6})

    revised = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-test",
        base_grid_size=101,
    )
    assert revised.base_grid_size == 101


@pytest.mark.parametrize(
    "mapping_name",
    [
        "slsqp_options",
        "ssvi_start_seeds",
        "raw_svi_start_seeds",
        "shgo_options",
        "shgo_minimizer_options",
    ],
)
def test_fit_policy_nested_strategy_mappings_are_immutable(mapping_name: str) -> None:
    mapping = getattr(FitPolicy(), mapping_name)
    with pytest.raises(TypeError):
        mapping["tampered"] = 1
    with pytest.raises(TypeError):
        mapping.update({"tampered": 1})


def test_attempt_id_uses_the_full_canonical_identity_payload() -> None:
    identity = fit.make_attempt_id(
        input_fingerprint="sha256:" + "1" * 64,
        product="ag",
        timestamp=TIMESTAMP,
        scope=AttemptScope.EXPIRY,
        maturity_id="ag2505",
        participating_maturities=[],
        method=FitMethod.PCHIP,
        attempt_order=7,
        policy_version=POLICY_VERSION,
    )
    assert identity == (
        "attempt:025bd49310c0af77a04803e0cd0624fa"
        "58381ec0ea54062117f5dbaf6f910e5b"
    )
    changed = fit.make_attempt_id(
        input_fingerprint="sha256:" + "1" * 64,
        product="ag",
        timestamp=TIMESTAMP,
        scope=AttemptScope.EXPIRY,
        maturity_id="ag2505",
        participating_maturities=[],
        method=FitMethod.PCHIP,
        attempt_order=8,
        policy_version=POLICY_VERSION,
    )
    assert changed != identity


def test_calendar_pair_id_uses_the_full_canonical_identity_payload() -> None:
    identity = fit.make_calendar_pair_id(
        input_fingerprint="sha256:" + "1" * 64,
        product="ag",
        timestamp=TIMESTAMP,
        phase="expiry_selection",
        parent_attempt_id=None,
        earlier_maturity_id="ag2504",
        later_maturity_id="ag2505",
        earlier_attempt_id=ATTEMPT_A,
        later_attempt_id=ATTEMPT_B,
        policy_version=POLICY_VERSION,
    )
    assert identity == (
        "calendar-pair:4f5c38d8174f95d2d14c9e5bcfd5f210"
        "1f90b213cfd30c03044a84e87386dd4f"
    )
    changed = fit.make_calendar_pair_id(
        input_fingerprint="sha256:" + "1" * 64,
        product="ag",
        timestamp=TIMESTAMP,
        phase="expiry_selection",
        parent_attempt_id=None,
        earlier_maturity_id="ag2504",
        later_maturity_id="ag2506",
        earlier_attempt_id=ATTEMPT_A,
        later_attempt_id=ATTEMPT_B,
        policy_version=POLICY_VERSION,
    )
    assert changed != identity


def test_timestamp_rejects_forged_attempt_and_pair_ids() -> None:
    input_fingerprint = "sha256:" + "1" * 64
    earlier = _accepted_attempt_and_result(
        "ag2504", 20.0 / 365.0, 0, input_fingerprint
    )
    later = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 1, input_fingerprint
    )
    pair_id = fit.make_calendar_pair_id(
        input_fingerprint=input_fingerprint,
        product="ag",
        timestamp=TIMESTAMP,
        phase="expiry_selection",
        parent_attempt_id=None,
        earlier_maturity_id="ag2504",
        later_maturity_id="ag2505",
        earlier_attempt_id=earlier[0].attempt_id,
        later_attempt_id=later[0].attempt_id,
        policy_version=POLICY_VERSION,
    )
    pair = CalendarPairDiagnostic(
        pair_check_id=pair_id,
        phase="expiry_selection",
        earlier_maturity_id="ag2504",
        later_maturity_id="ag2505",
        earlier_attempt_id=earlier[0].attempt_id,
        later_attempt_id=later[0].attempt_id,
        parent_attempt_id=None,
        common_k_min=-0.2,
        common_k_max=0.2,
        check=_check("calendar_consistent"),
    )
    diagnostic = _ready_timestamp(
        [earlier, later],
        input_fingerprint=input_fingerprint,
        calendar_pair_checks=[pair],
    )
    assert diagnostic.attempts[0].attempt_id == earlier[0].attempt_id

    forged_attempt = dataclasses.replace(earlier[0], attempt_id=ATTEMPT_A)
    forged_result = dataclasses.replace(
        earlier[1],
        selected_attempt_id=ATTEMPT_A,
        last_candidate_attempt_id=ATTEMPT_A,
        terminal_attempt_id=ATTEMPT_A,
        attempt_ids=[ATTEMPT_A],
    )
    with pytest.raises(ValueError):
        _ready_timestamp(
            [(forged_attempt, forged_result), later],
            input_fingerprint=input_fingerprint,
        )

    with pytest.raises(ValueError):
        _ready_timestamp(
            [earlier, later],
            input_fingerprint=input_fingerprint,
            calendar_pair_checks=[dataclasses.replace(pair, pair_check_id=PAIR_A)],
        )


@pytest.mark.parametrize(
    ("enum_type", "expected"),
    [
        (FitMethod, ["SSVI", "RAW_SVI", "PCHIP", "LINEAR"]),
        (FinalMethod, ["SSVI", "RAW_SVI", "PCHIP", "LINEAR", "UNUSABLE"]),
        (AttemptScope, ["timestamp", "expiry"]),
        (AttemptStatus, ["skipped", "failed", "accepted"]),
        (
            CheckStatus,
            ["passed", "failed", "indeterminate", "not_applicable", "not_testable"],
        ),
        (ResultStatus, ["usable", "unusable"]),
        (OverallStatus, ["all_usable", "partially_usable", "none_usable"]),
        (TimestampStatus, ["ready", "failed_input"]),
        (
            SurfaceGridStatus,
            [
                "available",
                "unavailable_no_support",
                "unavailable_input_failure",
            ],
        ),
        (
            ForwardSource,
            [
                "true_futures_forward",
                "underlying_price_proxy",
                "precomputed_log_moneyness_unknown",
            ],
        ),
    ],
)
def test_closed_enumerations_preserve_exact_values_and_order(
    enum_type: type[Enum], expected: list[str]
) -> None:
    assert [item.value for item in enum_type] == expected


def test_unusable_is_a_final_method_not_a_fit_attempt_method() -> None:
    assert "UNUSABLE" not in FitMethod.__members__
    assert FinalMethod.UNUSABLE.value == "UNUSABLE"


@pytest.mark.parametrize(
    ("data_type", "expected_fields"),
    [
        (
            CheckDiagnostic,
            [
                "name",
                "status",
                "conclusion",
                "reason_code",
                "primary_value",
                "threshold",
                "violation_count",
                "grid_point_count",
                "metrics",
            ],
        ),
        (
            OptimizerStartSummary,
            [
                "generated_count",
                "precheck_discarded_count",
                "duplicate_discarded_count",
                "executed_count",
                "optimizer_reported_success_count",
                "evaluable_count",
                "local_success_count",
                "selected_start_index",
                "selection_kind",
            ],
        ),
        (
            PerExpiryMetric,
            [
                "maturity_id",
                "time_to_expiry",
                "raw_node_count",
                "node_count",
                "k_min",
                "k_max",
                "rmse_total_variance",
                "nrmse_total_variance",
                "rmse_iv",
                "checks",
            ],
        ),
        (
            FitAttemptDiagnostic,
            [
                "attempt_id",
                "parent_attempt_id",
                "scope",
                "product",
                "timestamp",
                "maturity_id",
                "participating_maturities",
                "time_to_expiry",
                "method",
                "attempt_order",
                "attempt_status",
                "optimizer_attempted",
                "optimizer_success",
                "optimizer_start_summary",
                "selection_eligible",
                "blocked_by_parent",
                "local_success",
                "success",
                "parameters",
                "per_expiry_metrics",
                "rmse_total_variance",
                "nrmse_total_variance",
                "rmse_iv",
                "raw_node_count",
                "node_count",
                "k_min",
                "k_max",
                "candidate_k",
                "candidate_total_variance",
                "candidate_iv",
                "checks",
                "failure_code",
                "failure_reason",
                "policy_version",
                "forward_source",
            ],
        ),
        (
            ExpiryFitResult,
            [
                "maturity_id",
                "time_to_expiry",
                "result_status",
                "method",
                "success",
                "usable",
                "raw_k",
                "raw_total_variance",
                "raw_iv",
                "fit_k",
                "fit_total_variance",
                "fit_iv",
                "selected_attempt_id",
                "last_candidate_attempt_id",
                "terminal_attempt_id",
                "attempt_ids",
                "final_checks",
                "failure_code",
                "failure_reason",
            ],
        ),
        (
            InputQuality,
            [
                "input_row_count",
                "valid_premerge_node_count",
                "merged_node_count",
                "excluded_counts",
            ],
        ),
        (
            CalendarPairDiagnostic,
            [
                "pair_check_id",
                "phase",
                "earlier_maturity_id",
                "later_maturity_id",
                "earlier_attempt_id",
                "later_attempt_id",
                "parent_attempt_id",
                "common_k_min",
                "common_k_max",
                "check",
            ],
        ),
        (
            TimestampSurfaceDiagnostic,
            [
                "product",
                "timestamp",
                "diagnostic_only",
                "timestamp_status",
                "timestamp_failure_code",
                "timestamp_failure_reason",
                "forward_source",
                "observed_forward_sources",
                "input_quality",
                "ssvi_attempt",
                "attempts",
                "expiry_results",
                "surface_grid_status",
                "surface_log_moneyness",
                "surface_time_to_expiry",
                "surface_total_variance",
                "surface_iv",
                "usable_expiry_count",
                "unusable_expiry_count",
                "calendar_pair_checks",
                "method_counts",
                "overall_status",
                "policy_version",
                "effective_input_fingerprint",
                "input_quality_fingerprint",
                "input_fingerprint",
            ],
        ),
    ],
)
def test_closed_dataclasses_have_exact_required_fields(
    data_type: type[object], expected_fields: list[str]
) -> None:
    fields = dataclasses.fields(data_type)
    assert [field.name for field in fields] == expected_fields
    assert all(
        field.default is dataclasses.MISSING
        and field.default_factory is dataclasses.MISSING
        for field in fields
    )


def test_contract_annotations_keep_required_and_nullable_fields_distinct() -> None:
    attempt_hints = get_type_hints(FitAttemptDiagnostic)
    assert type(None) in get_args(attempt_hints["parent_attempt_id"])
    assert type(None) in get_args(attempt_hints["optimizer_success"])
    assert type(None) not in get_args(attempt_hints["success"])
    assert type(None) not in get_args(attempt_hints["attempt_order"])
    result_hints = get_type_hints(ExpiryFitResult)
    assert type(None) in get_args(result_hints["selected_attempt_id"])
    assert type(None) not in get_args(result_hints["usable"])
    summary_hints = get_type_hints(OptimizerStartSummary)
    assert summary_hints["selection_kind"] == (
        Literal["local_success", "failure_representative"] | None
    )
    pair_hints = get_type_hints(CalendarPairDiagnostic)
    assert pair_hints["phase"] == Literal["ssvi_parent", "expiry_selection"]
    timestamp_hints = get_type_hints(TimestampSurfaceDiagnostic)
    assert timestamp_hints["diagnostic_only"] == Literal[True]


def test_optimizer_start_summary_enforces_reconciliation_and_upper_bounds() -> None:
    summary = _summary("local_success", optimizer_success=True)
    _assert_frozen_dataclass(summary)
    assert summary.local_success_count == 1

    base = dataclasses.asdict(summary)
    for override in (
        {"generated_count": 2},
        {"optimizer_reported_success_count": 2},
        {"optimizer_reported_success_count": 0},
        {"evaluable_count": 2},
        {"local_success_count": 2},
        {"selected_start_index": 1},
    ):
        with pytest.raises(ValueError):
            OptimizerStartSummary(**(base | override))


@pytest.mark.parametrize(
    (
        "method",
        "scope",
        "status",
        "optimizer_success",
        "selection_eligible",
        "blocked",
        "local_success",
        "success",
        "failure_code",
        "selection_kind",
    ),
    [
        (FitMethod.SSVI, AttemptScope.TIMESTAMP, AttemptStatus.SKIPPED, None, False, False, False, False, "not_enough_maturities", None),
        (FitMethod.SSVI, AttemptScope.TIMESTAMP, AttemptStatus.FAILED, False, False, False, False, False, "optimizer_failed", "failure_representative"),
        (FitMethod.SSVI, AttemptScope.TIMESTAMP, AttemptStatus.FAILED, True, False, False, False, False, "rmse_exceeded", "failure_representative"),
        (FitMethod.SSVI, AttemptScope.TIMESTAMP, AttemptStatus.FAILED, True, False, False, True, False, "calendar_conflict", "local_success"),
        (FitMethod.SSVI, AttemptScope.TIMESTAMP, AttemptStatus.FAILED, True, False, False, True, False, "check_resolution_limit", "local_success"),
        (FitMethod.RAW_SVI, AttemptScope.EXPIRY, AttemptStatus.FAILED, False, True, False, False, False, "optimizer_failed", "failure_representative"),
        (FitMethod.RAW_SVI, AttemptScope.EXPIRY, AttemptStatus.FAILED, True, True, False, False, False, "rmse_exceeded", "failure_representative"),
        (FitMethod.PCHIP, AttemptScope.EXPIRY, AttemptStatus.FAILED, None, True, False, False, False, "rmse_exceeded", None),
        (FitMethod.PCHIP, AttemptScope.EXPIRY, AttemptStatus.FAILED, None, True, False, False, False, "check_resolution_limit", None),
        (FitMethod.SSVI, AttemptScope.EXPIRY, AttemptStatus.FAILED, None, False, True, True, False, "parent_ssvi_rejected", None),
        (FitMethod.SSVI, AttemptScope.EXPIRY, AttemptStatus.FAILED, None, False, True, False, False, "rmse_exceeded", None),
        (FitMethod.PCHIP, AttemptScope.EXPIRY, AttemptStatus.FAILED, None, True, False, True, False, "calendar_conflict", None),
        (FitMethod.PCHIP, AttemptScope.EXPIRY, AttemptStatus.FAILED, None, True, False, True, False, "check_resolution_limit", None),
        (FitMethod.PCHIP, AttemptScope.EXPIRY, AttemptStatus.ACCEPTED, None, True, False, True, True, None, None),
        (FitMethod.SSVI, AttemptScope.TIMESTAMP, AttemptStatus.ACCEPTED, True, False, False, True, True, None, "local_success"),
    ],
)
def test_attempt_truth_table_accepts_every_closed_row(
    method: FitMethod,
    scope: AttemptScope,
    status: AttemptStatus,
    optimizer_success: bool | None,
    selection_eligible: bool,
    blocked: bool,
    local_success: bool,
    success: bool,
    failure_code: str | None,
    selection_kind: str | None,
) -> None:
    summary = (
        None
        if selection_kind is None
        else _summary(selection_kind, optimizer_success=bool(optimizer_success))
    )
    attempt = _attempt(
        method=method,
        scope=scope,
        attempt_status=status,
        optimizer_success=optimizer_success,
        optimizer_start_summary=summary,
        selection_eligible=selection_eligible,
        blocked_by_parent=blocked,
        local_success=local_success,
        success=success,
        failure_code=failure_code,
    )
    _assert_frozen_dataclass(attempt)


@pytest.mark.parametrize(
    "override",
    [
        {"attempt_status": AttemptStatus.ACCEPTED, "success": False},
        {"attempt_status": AttemptStatus.FAILED, "success": True},
        {"attempt_status": AttemptStatus.ACCEPTED, "local_success": False},
        {"attempt_status": AttemptStatus.ACCEPTED, "failure_code": "rmse_exceeded"},
        {"optimizer_success": False},
        {"blocked_by_parent": True},
    ],
)
def test_attempt_truth_table_rejects_contradictory_rows(override: dict[str, object]) -> None:
    attempt = _attempt()
    with pytest.raises(ValueError):
        FitAttemptDiagnostic(**(dataclasses.asdict(attempt) | override))


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "method": FitMethod.PCHIP,
            "scope": AttemptScope.EXPIRY,
            "attempt_status": AttemptStatus.SKIPPED,
            "local_success": False,
            "success": False,
            "failure_code": "not_enough_maturities",
        },
        {
            "method": FitMethod.SSVI,
            "scope": AttemptScope.EXPIRY,
            "attempt_status": AttemptStatus.SKIPPED,
            "selection_eligible": True,
            "local_success": False,
            "success": False,
            "failure_code": "not_enough_maturities",
        },
        {
            "method": FitMethod.SSVI,
            "scope": AttemptScope.TIMESTAMP,
            "attempt_status": AttemptStatus.FAILED,
            "selection_eligible": False,
            "local_success": False,
            "success": False,
            "failure_code": "not_enough_maturities",
        },
        {
            "method": FitMethod.RAW_SVI,
            "attempt_status": AttemptStatus.FAILED,
            "optimizer_success": False,
            "optimizer_start_summary": _summary(
                "failure_representative", optimizer_success=False
            ),
            "local_success": False,
            "success": False,
            "failure_code": "rmse_exceeded",
        },
        {
            "method": FitMethod.RAW_SVI,
            "attempt_status": AttemptStatus.FAILED,
            "optimizer_success": True,
            "optimizer_start_summary": _summary(
                "failure_representative", optimizer_success=True
            ),
            "local_success": False,
            "success": False,
            "failure_code": "optimizer_failed",
        },
        {
            "method": FitMethod.PCHIP,
            "attempt_status": AttemptStatus.FAILED,
            "local_success": False,
            "success": False,
            "failure_code": "optimizer_failed",
        },
        {
            "method": FitMethod.PCHIP,
            "attempt_status": AttemptStatus.FAILED,
            "local_success": False,
            "success": False,
            "failure_code": "parent_ssvi_rejected",
        },
    ],
)
def test_attempt_truth_table_rejects_method_and_stage_failure_code_mismatches(
    kwargs: dict[str, object],
) -> None:
    with pytest.raises(ValueError):
        _attempt(**kwargs)


def test_skipped_ssvi_parent_has_no_parameters_or_executed_checks() -> None:
    skipped = _attempt(
        method=FitMethod.SSVI,
        scope=AttemptScope.TIMESTAMP,
        attempt_status=AttemptStatus.SKIPPED,
        selection_eligible=False,
        local_success=False,
        success=False,
        failure_code="not_enough_maturities",
    )
    with pytest.raises(ValueError):
        dataclasses.replace(
            skipped,
            parameters={
                "rho": -0.2,
                "eta": 0.5,
                "gamma": 0.3,
                "theta_by_maturity": {"ag2505": 0.04},
            },
        )
    with pytest.raises(ValueError):
        dataclasses.replace(skipped, checks=_six_checks())


@pytest.mark.parametrize("method", [FitMethod.PCHIP, FitMethod.LINEAR])
@pytest.mark.parametrize(
    "failure_code",
    ["non_finite_parameters", "parameter_constraint_failed", "butterfly_failed"],
)
def test_non_parametric_methods_reject_parameter_and_butterfly_failure_codes(
    method: FitMethod,
    failure_code: str,
) -> None:
    with pytest.raises(ValueError):
        _attempt(
            method=method,
            attempt_status=AttemptStatus.FAILED,
            local_success=False,
            success=False,
            failure_code=failure_code,
        )


@pytest.mark.parametrize(
    ("method", "failure_code", "replacement_checks"),
    [
        (
            FitMethod.PCHIP,
            "call_price_monotonicity_failed",
            _six_checks(FitMethod.PCHIP),
        ),
        (
            FitMethod.LINEAR,
            "check_resolution_limit",
            _six_checks(FitMethod.LINEAR),
        ),
        (
            FitMethod.SSVI,
            "butterfly_failed",
            _six_checks(FitMethod.PCHIP),
        ),
    ],
)
def test_failure_code_requires_its_corresponding_method_check_state(
    method: FitMethod,
    failure_code: str,
    replacement_checks: dict[str, CheckDiagnostic],
) -> None:
    kwargs: dict[str, object] = {
        "method": method,
        "attempt_status": AttemptStatus.FAILED,
        "local_success": False,
        "success": False,
        "failure_code": failure_code,
    }
    if method is FitMethod.SSVI:
        kwargs.update(
            scope=AttemptScope.EXPIRY,
            selection_eligible=True,
            blocked_by_parent=False,
        )
    attempt = _attempt(**kwargs)
    with pytest.raises(ValueError):
        dataclasses.replace(attempt, checks=replacement_checks)


def _accepted_attempt_for_method(method: FitMethod) -> FitAttemptDiagnostic:
    kwargs: dict[str, object] = {"method": method}
    if method is FitMethod.RAW_SVI:
        kwargs.update(
            optimizer_success=True,
            optimizer_start_summary=_summary("local_success", optimizer_success=True),
        )
    return _attempt(**kwargs)


@pytest.mark.parametrize(
    "method",
    [FitMethod.SSVI, FitMethod.RAW_SVI, FitMethod.PCHIP, FitMethod.LINEAR],
)
def test_accepted_attempt_requires_every_applicable_local_hard_check_to_pass(
    method: FitMethod,
) -> None:
    attempt = _accepted_attempt_for_method(method)
    checks = dict(attempt.checks)
    checks["positive_total_variance"] = _failed_check(
        "positive_total_variance", "below_variance_floor"
    )
    with pytest.raises(ValueError):
        dataclasses.replace(attempt, checks=checks)


def test_calendar_stage_local_success_rejects_an_earlier_failed_local_gate() -> None:
    attempt = _attempt(
        attempt_status=AttemptStatus.FAILED,
        local_success=True,
        success=False,
        failure_code="calendar_conflict",
    )
    checks = dict(attempt.checks)
    checks["call_price_convex"] = _failed_check(
        "call_price_convex", "decreasing_secant_slope"
    )
    with pytest.raises(ValueError):
        dataclasses.replace(attempt, checks=checks)


@pytest.mark.parametrize(
    ("attempt", "earlier_check", "earlier_reason"),
    [
        (
            _attempt(
                method=FitMethod.PCHIP,
                attempt_status=AttemptStatus.FAILED,
                local_success=False,
                success=False,
                failure_code="call_price_monotonicity_failed",
            ),
            "positive_total_variance",
            "below_variance_floor",
        ),
        (
            _attempt(
                method=FitMethod.RAW_SVI,
                attempt_status=AttemptStatus.FAILED,
                optimizer_success=True,
                optimizer_start_summary=_summary(
                    "failure_representative", optimizer_success=True
                ),
                local_success=False,
                success=False,
                failure_code="butterfly_failed",
            ),
            "call_price_convex",
            "decreasing_secant_slope",
        ),
        (
            _attempt(
                method=FitMethod.SSVI,
                attempt_status=AttemptStatus.FAILED,
                local_success=False,
                success=False,
                failure_code="abnormal_jump",
            ),
            "butterfly_g_nonnegative",
            "negative_g",
        ),
    ],
)
def test_primary_failure_code_is_the_first_actual_failed_hard_gate(
    attempt: FitAttemptDiagnostic,
    earlier_check: str,
    earlier_reason: str,
) -> None:
    checks = dict(attempt.checks)
    checks[earlier_check] = _failed_check(earlier_check, earlier_reason)
    with pytest.raises(ValueError):
        dataclasses.replace(attempt, checks=checks)


@pytest.mark.parametrize("method", [FitMethod.PCHIP, FitMethod.LINEAR])
def test_non_parametric_butterfly_check_is_never_generic_not_run(
    method: FitMethod,
) -> None:
    attempt = _accepted_attempt_for_method(method)
    checks = dict(attempt.checks)
    checks["butterfly_g_nonnegative"] = _not_run_checks()[
        "butterfly_g_nonnegative"
    ]
    with pytest.raises(ValueError):
        dataclasses.replace(attempt, checks=checks)


@pytest.mark.parametrize("method", [FitMethod.SSVI, FitMethod.RAW_SVI])
def test_parameter_method_accepted_attempt_must_execute_analytic_butterfly_gate(
    method: FitMethod,
) -> None:
    attempt = _accepted_attempt_for_method(method)
    checks = dict(attempt.checks)
    checks["butterfly_g_nonnegative"] = _not_run_checks()[
        "butterfly_g_nonnegative"
    ]
    with pytest.raises(ValueError):
        dataclasses.replace(attempt, checks=checks)


def test_expiry_result_enforces_usable_and_unusable_reference_rules() -> None:
    usable = _expiry_result(usable=True)
    unusable = _expiry_result(usable=False)
    _assert_frozen_dataclass(usable)
    _assert_frozen_dataclass(unusable)

    with pytest.raises(ValueError):
        ExpiryFitResult(
            **(dataclasses.asdict(usable) | {"selected_attempt_id": None})
        )
    with pytest.raises(ValueError):
        ExpiryFitResult(
            **(dataclasses.asdict(unusable) | {"method": FinalMethod.PCHIP})
        )
    with pytest.raises(ValueError):
        ExpiryFitResult(
            **(dataclasses.asdict(unusable) | {"terminal_attempt_id": ATTEMPT_B})
        )


def test_insufficient_nodes_result_requires_null_terminal_reference() -> None:
    unusable = _expiry_result(usable=False)
    with pytest.raises(ValueError):
        dataclasses.replace(
            unusable,
            failure_code="insufficient_nodes",
            failure_reason="fewer than two nodes",
            terminal_attempt_id=ATTEMPT_A,
        )


def test_timestamp_cross_validates_selected_attempt_status_method_and_expiry() -> None:
    input_fingerprint = "sha256:" + "4" * 64
    accepted, result = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )

    failed = dataclasses.replace(
        accepted,
        attempt_status=AttemptStatus.FAILED,
        local_success=False,
        success=False,
        failure_code="rmse_exceeded",
        failure_reason="fit error exceeded",
    )
    with pytest.raises(ValueError):
        _ready_timestamp([(failed, result)], input_fingerprint=input_fingerprint)

    with pytest.raises(ValueError):
        _ready_timestamp(
            [(accepted, dataclasses.replace(result, method=FinalMethod.LINEAR))],
            input_fingerprint=input_fingerprint,
        )

    other_maturity = _accepted_attempt_and_result(
        "ag2506", 30.0 / 365.0, 0, input_fingerprint
    )[0]
    mismatched_result = dataclasses.replace(
        result,
        selected_attempt_id=other_maturity.attempt_id,
        last_candidate_attempt_id=other_maturity.attempt_id,
        terminal_attempt_id=other_maturity.attempt_id,
        attempt_ids=[other_maturity.attempt_id],
    )
    with pytest.raises(ValueError):
        _ready_timestamp(
            [(other_maturity, mismatched_result)],
            input_fingerprint=input_fingerprint,
        )


def test_timestamp_requires_final_checks_and_arrays_to_copy_selected_attempt() -> None:
    input_fingerprint = "sha256:" + "5" * 64
    accepted, result = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )
    mismatched_checks = dict(result.final_checks)
    mismatched_checks["calendar_consistent"] = _check("calendar_consistent")
    with pytest.raises(ValueError):
        _ready_timestamp(
            [(accepted, dataclasses.replace(result, final_checks=mismatched_checks))],
            input_fingerprint=input_fingerprint,
        )
    with pytest.raises(ValueError):
        _ready_timestamp(
            [(accepted, dataclasses.replace(result, fit_total_variance=[0.05] * 3))],
            input_fingerprint=input_fingerprint,
        )


def test_timestamp_requires_unusable_failure_to_copy_terminal_attempt() -> None:
    input_fingerprint = "sha256:" + "6" * 64
    accepted, accepted_result = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )
    failed = dataclasses.replace(
        accepted,
        attempt_status=AttemptStatus.FAILED,
        local_success=False,
        success=False,
        failure_code="rmse_exceeded",
        failure_reason="terminal fit error exceeded",
    )
    unusable = dataclasses.replace(
        _expiry_result(usable=False),
        maturity_id=failed.maturity_id,
        time_to_expiry=failed.time_to_expiry,
        selected_attempt_id=None,
        last_candidate_attempt_id=failed.attempt_id,
        terminal_attempt_id=failed.attempt_id,
        attempt_ids=[failed.attempt_id],
        final_checks=failed.checks,
        failure_code=failed.failure_code,
        failure_reason=failed.failure_reason,
    )
    ready = _ready_timestamp(
        [(accepted, accepted_result)], input_fingerprint=input_fingerprint
    )
    bad_checks = dict(unusable.final_checks)
    bad_checks["calendar_consistent"] = _check("calendar_consistent")
    with pytest.raises(ValueError):
        dataclasses.replace(
            ready,
            attempts=[failed],
            expiry_results=[dataclasses.replace(unusable, final_checks=bad_checks)],
            surface_total_variance=[[None] * 201],
            surface_iv=[[None] * 201],
            usable_expiry_count=0,
            unusable_expiry_count=1,
            method_counts={
                FinalMethod.SSVI: 0,
                FinalMethod.RAW_SVI: 0,
                FinalMethod.PCHIP: 0,
                FinalMethod.LINEAR: 0,
                FinalMethod.UNUSABLE: 1,
            },
            overall_status=OverallStatus.NONE_USABLE,
        )


def test_usable_result_rejects_selection_candidates_after_the_accepted_attempt() -> None:
    input_fingerprint = "sha256:" + "f" * 64
    accepted, result = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )
    later, _ = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 1, input_fingerprint
    )
    later_failed = dataclasses.replace(
        later,
        attempt_status=AttemptStatus.FAILED,
        local_success=False,
        success=False,
        failure_code="rmse_exceeded",
        failure_reason="later candidate should never execute",
    )
    result_with_later = dataclasses.replace(
        result,
        attempt_ids=[accepted.attempt_id, later_failed.attempt_id],
        last_candidate_attempt_id=later_failed.attempt_id,
    )
    diagnostic = _ready_timestamp(
        [(accepted, result)], input_fingerprint=input_fingerprint
    )
    with pytest.raises(ValueError):
        dataclasses.replace(
            diagnostic,
            attempts=[accepted, later_failed],
            expiry_results=[result_with_later],
        )


def test_insufficient_nodes_rejects_attempts_candidates_and_non_not_run_checks() -> None:
    input_fingerprint = "sha256:" + "0" * 64
    diagnostic = _insufficient_timestamp(input_fingerprint)
    result = diagnostic.expiry_results[0]
    candidate, _ = _accepted_attempt_and_result(
        result.maturity_id,
        result.time_to_expiry,
        0,
        input_fingerprint,
    )
    failed_candidate = dataclasses.replace(
        candidate,
        attempt_status=AttemptStatus.FAILED,
        local_success=False,
        success=False,
        failure_code="rmse_exceeded",
        failure_reason="candidate unexpectedly exists",
    )
    with pytest.raises(ValueError):
        bad_result = dataclasses.replace(
            result,
            attempt_ids=[failed_candidate.attempt_id],
            last_candidate_attempt_id=failed_candidate.attempt_id,
        )
        dataclasses.replace(
            diagnostic,
            attempts=[failed_candidate],
            expiry_results=[bad_result],
        )

    with pytest.raises(ValueError):
        dataclasses.replace(result, final_checks=_six_checks(FitMethod.PCHIP))


def test_timestamp_recomputes_method_counts_from_expiry_results() -> None:
    input_fingerprint = "sha256:" + "a" * 64
    pair = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )
    diagnostic = _ready_timestamp([pair], input_fingerprint=input_fingerprint)
    with pytest.raises(ValueError):
        dataclasses.replace(
            diagnostic,
            method_counts={
                FinalMethod.SSVI: 0,
                FinalMethod.RAW_SVI: 0,
                FinalMethod.PCHIP: 0,
                FinalMethod.LINEAR: 1,
                FinalMethod.UNUSABLE: 0,
            },
        )


def test_timestamp_validates_every_finite_surface_iv_cell_from_w_and_t() -> None:
    input_fingerprint = "sha256:" + "b" * 64
    pair = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )
    diagnostic = _ready_timestamp([pair], input_fingerprint=input_fingerprint)
    wrong_iv = [list(diagnostic.surface_iv[0])]
    wrong_iv[0][17] += 1e-12
    with pytest.raises(ValueError):
        dataclasses.replace(diagnostic, surface_iv=wrong_iv)


def test_failed_input_requires_zero_merged_nodes_and_multiple_sources() -> None:
    diagnostic = _failed_input_timestamp()
    with pytest.raises(ValueError):
        dataclasses.replace(
            diagnostic,
            input_quality=dataclasses.replace(
                diagnostic.input_quality,
                merged_node_count=1,
            ),
        )

    one_source = [ForwardSource.UNDERLYING_PRICE_PROXY]
    with pytest.raises(ValueError):
        dataclasses.replace(
            diagnostic,
            observed_forward_sources=one_source,
            timestamp_failure_reason=(
                "mixed forward sources: " + ",".join(item.value for item in one_source)
            ),
        )


@pytest.mark.parametrize(
    "override",
    [
        {"forward_source": ForwardSource.TRUE_FUTURES_FORWARD},
        {"forward_source": None, "observed_forward_sources": []},
        {
            "observed_forward_sources": [
                ForwardSource.TRUE_FUTURES_FORWARD,
                ForwardSource.UNDERLYING_PRICE_PROXY,
            ]
        },
    ],
)
def test_ready_timestamp_requires_one_matching_source_when_valid_nodes_exist(
    override: dict[str, object],
) -> None:
    input_fingerprint = "sha256:" + "c" * 64
    pair = _accepted_attempt_and_result(
        "ag2505", 30.0 / 365.0, 0, input_fingerprint
    )
    diagnostic = _ready_timestamp([pair], input_fingerprint=input_fingerprint)
    with pytest.raises(ValueError):
        dataclasses.replace(diagnostic, **override)


@pytest.mark.parametrize(
    "check",
    [
        _check("calendar_consistent"),
        CheckDiagnostic(
            name="calendar_consistent",
            status=CheckStatus.FAILED,
            conclusion="violation_found",
            reason_code="calendar_total_variance_decrease",
            primary_value=-0.01,
            threshold=-0.001,
            violation_count=1,
            grid_point_count=201,
            metrics={"minimum_margin": -0.009},
        ),
        CheckDiagnostic(
            name="calendar_consistent",
            status=CheckStatus.INDETERMINATE,
            conclusion="unreliable",
            reason_code="resolution_limit",
            primary_value=0.0,
            threshold=1e-6,
            violation_count=0,
            grid_point_count=257,
            metrics={"minimum_margin": 0.0},
        ),
    ],
)
def test_evaluated_calendar_pair_requires_positive_width_common_bounds(
    check: CheckDiagnostic,
) -> None:
    with pytest.raises(ValueError):
        CalendarPairDiagnostic(
            pair_check_id=PAIR_A,
            phase="expiry_selection",
            earlier_maturity_id="ag2504",
            later_maturity_id="ag2505",
            earlier_attempt_id=ATTEMPT_A,
            later_attempt_id=ATTEMPT_B,
            parent_attempt_id=None,
            common_k_min=None,
            common_k_max=None,
            check=check,
        )


def test_expiry_selection_pair_rejects_not_applicable_no_prior_maturity() -> None:
    with pytest.raises(ValueError):
        CalendarPairDiagnostic(
            pair_check_id=PAIR_A,
            phase="expiry_selection",
            earlier_maturity_id="ag2504",
            later_maturity_id="ag2505",
            earlier_attempt_id=ATTEMPT_A,
            later_attempt_id=ATTEMPT_B,
            parent_attempt_id=None,
            common_k_min=None,
            common_k_max=None,
            check=_check("calendar_consistent", CheckStatus.NOT_APPLICABLE),
        )


def test_ssvi_parent_local_failure_pair_retains_child_references_as_not_run() -> None:
    pair = CalendarPairDiagnostic(
        pair_check_id=PAIR_A,
        phase="ssvi_parent",
        earlier_maturity_id="ag2504",
        later_maturity_id="ag2505",
        earlier_attempt_id=ATTEMPT_A,
        later_attempt_id=ATTEMPT_B,
        parent_attempt_id="attempt:" + "d" * 64,
        common_k_min=None,
        common_k_max=None,
        check=CheckDiagnostic(
            name="calendar_consistent",
            status=CheckStatus.NOT_APPLICABLE,
            conclusion="not_applicable",
            reason_code="not_run",
            primary_value=None,
            threshold=None,
            violation_count=None,
            grid_point_count=0,
            metrics={},
        ),
    )

    assert pair.earlier_attempt_id == ATTEMPT_A
    assert pair.later_attempt_id == ATTEMPT_B
    assert pair.check.status is CheckStatus.NOT_APPLICABLE
    assert pair.check.reason_code == "not_run"


def test_total_variance_and_display_iv_round_trip() -> None:
    iv = 0.325
    time_to_expiry = 45.0 / 365.0
    total_variance = to_total_variance(iv, time_to_expiry)
    assert total_variance == pytest.approx(iv**2 * time_to_expiry)
    assert to_implied_volatility(total_variance, time_to_expiry) == pytest.approx(iv)
    assert to_total_variance(0.0, time_to_expiry) == 0.0


@pytest.mark.parametrize(
    ("function", "first", "time_to_expiry"),
    [
        (to_total_variance, -0.1, 1.0),
        (to_total_variance, np.nan, 1.0),
        (to_total_variance, np.inf, 1.0),
        (to_total_variance, 0.2, 0.0),
        (to_total_variance, 0.2, -1.0),
        (to_implied_volatility, 0.0, 1.0),
        (to_implied_volatility, -0.1, 1.0),
        (to_implied_volatility, np.nan, 1.0),
        (to_implied_volatility, np.inf, 1.0),
        (to_implied_volatility, 0.1, 0.0),
    ],
)
def test_variance_conversions_reject_invalid_inputs(
    function: object, first: float, time_to_expiry: float
) -> None:
    with pytest.raises(ValueError):
        function(first, time_to_expiry)


def test_diagnostic_curve_grid_is_exact_numpy_unique_union() -> None:
    raw_k = np.array([-0.3, -0.1234567890123, 0.0, 0.3], dtype=np.float64)
    expected = np.unique(
        np.concatenate(
            (
                np.linspace(-0.3, 0.3, 201, endpoint=True, dtype=np.float64),
                raw_k,
            )
        )
    )
    actual = diagnostic_curve_grid(-0.3, 0.3, raw_k)

    np.testing.assert_array_equal(actual, expected)
    assert actual.flags.writeable is False
    assert actual.tolist().count(-0.1234567890123) == 1


@pytest.mark.parametrize("method", list(FitMethod))
def test_every_curve_method_uses_one_closed_domain_evaluator(method: FitMethod) -> None:
    knots = np.array([-0.2, 0.0, 0.2], dtype=np.float64)
    curve = fit._create_curve_model(
        method=method,
        time_to_expiry=0.25,
        k_min=-0.2,
        k_max=0.2,
        evaluator=lambda k: 0.04 + 0.01 * np.asarray(k, dtype=np.float64) ** 2,
        knots=knots,
    )
    knots[0] = -999.0
    assert curve.k_min == -0.2
    assert curve.k_max == 0.2
    assert curve.knots.flags.writeable is False
    assert curve.knots.tolist() == [-0.2, 0.0, 0.2]
    with pytest.raises(ValueError):
        curve.knots[0] = -0.1
    assert not callable(curve)
    assert not hasattr(curve, "evaluate")

    left_outside = np.nextafter(curve.k_min, -np.inf)
    right_outside = np.nextafter(curve.k_max, np.inf)
    result = evaluate_curve(
        curve,
        np.array([left_outside, curve.k_min, 0.0, curve.k_max, right_outside]),
    )

    assert result.supported.tolist() == [False, True, True, True, False]
    assert result.total_variance.tolist()[0] is None
    assert result.total_variance.tolist()[-1] is None
    assert result.iv.tolist()[0] is None
    assert result.iv.tolist()[-1] is None
    assert result.total_variance.tolist()[1:4] == pytest.approx([0.0404, 0.04, 0.0404])
    assert result.iv.tolist()[1:4] == pytest.approx(
        [np.sqrt(0.0404 / 0.25), np.sqrt(0.04 / 0.25), np.sqrt(0.0404 / 0.25)]
    )
    for array in (result.k, result.supported, result.total_variance, result.iv):
        assert array.flags.writeable is False


def test_curve_model_construction_is_private_and_public_api_cannot_enable_extrapolation() -> None:
    assert dataclasses.is_dataclass(fit.CurveModel)
    with pytest.raises(TypeError):
        fit.CurveModel()
    assert "extrapolate" not in inspect.signature(evaluate_curve).parameters
    public_names = {name for name in vars(fit) if not name.startswith("_")}
    assert not {
        "ssvi_total_variance",
        "raw_svi_total_variance",
        "pchip_evaluate",
        "linear_evaluate",
    } & public_names
    assert not any("extrapolat" in name.lower() for name in public_names)


def test_evaluate_curve_preserves_supported_bad_w_as_null_safe_diagnostics() -> None:
    curve = fit._create_curve_model(
        method=FitMethod.LINEAR,
        time_to_expiry=0.5,
        k_min=-1.0,
        k_max=1.0,
        evaluator=lambda k: np.array([0.04, 0.0, -0.01, np.nan]),
        knots=np.array([-1.0, 1.0]),
    )
    result = evaluate_curve(curve, [-1.0, -0.5, 0.5, 1.0])
    assert result.supported.tolist() == [True, True, True, True]
    assert result.total_variance.tolist() == [0.04, 0.0, -0.01, None]
    assert result.iv.tolist()[0] == pytest.approx(np.sqrt(0.04 / 0.5))
    assert result.iv.tolist()[1:] == [None, None, None]


def test_recursive_json_adapter_normalizes_numpy_scalars_and_preserves_null() -> None:
    value = {
        "float": np.float64(1.25),
        "integer": np.int64(3),
        "boolean": np.bool_(True),
        "null": None,
        "nested": [ForwardSource.UNDERLYING_PRICE_PROXY, (np.float32(0.5),)],
    }
    converted = to_json_compatible(value)
    assert converted == {
        "float": 1.25,
        "integer": 3,
        "boolean": True,
        "null": None,
        "nested": ["underlying_price_proxy", [0.5]],
    }
    assert type(converted["float"]) is float
    assert type(converted["integer"]) is int
    assert type(converted["boolean"]) is bool
    json.dumps(converted, allow_nan=False)


@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf, {"x": [np.float64(np.nan)]}])
def test_recursive_json_adapter_rejects_non_finite_values(bad: object) -> None:
    with pytest.raises(ValueError):
        to_json_compatible(bad)


def test_check_metrics_allow_only_finite_json_scalars_not_arrays() -> None:
    valid = _check("positive_total_variance")
    assert valid.metrics == {"minimum_margin": np.float64(0.1)}
    for bad_metrics in (
        {"array": [1.0]},
        {"nan": np.nan},
        {"infinity": np.inf},
        {"nested": {"x": 1.0}},
    ):
        with pytest.raises(ValueError):
            CheckDiagnostic(
                **(dataclasses.asdict(valid) | {"metrics": bad_metrics})
            )


@pytest.mark.parametrize(
    "override",
    [
        {
            "status": CheckStatus.FAILED,
            "conclusion": "violation_found",
            "reason_code": "not_run",
        },
        {
            "status": CheckStatus.NOT_APPLICABLE,
            "conclusion": "not_applicable",
            "reason_code": "below_variance_floor",
        },
    ],
)
def test_check_truth_table_rejects_reason_codes_from_the_wrong_status(
    override: dict[str, object],
) -> None:
    valid = _check("positive_total_variance")
    with pytest.raises(ValueError):
        CheckDiagnostic(**(dataclasses.asdict(valid) | override))


def test_ssvi_formula_and_analytic_derivatives_match_hand_values_and_differences() -> None:
    k = np.array([-0.2, 0.05, 0.3], dtype=np.float64)
    w, first, second = fit._ssvi_value_derivatives(
        k, theta=0.04, rho=-0.3, eta=0.7, gamma=0.25
    )
    np.testing.assert_allclose(
        w,
        [0.04455718340629552, 0.039117845896585395, 0.03656043281669686],
        rtol=2e-15,
        atol=2e-16,
    )
    h = 1e-5
    plus = fit._ssvi_value_derivatives(
        k + h, theta=0.04, rho=-0.3, eta=0.7, gamma=0.25
    )[0]
    minus = fit._ssvi_value_derivatives(
        k - h, theta=0.04, rho=-0.3, eta=0.7, gamma=0.25
    )[0]
    np.testing.assert_allclose(first, (plus - minus) / (2.0 * h), rtol=2e-9, atol=1e-11)
    np.testing.assert_allclose(
        second, (plus - 2.0 * w + minus) / h**2, rtol=3e-6, atol=2e-7
    )


def test_raw_svi_formula_and_analytic_derivatives_match_hand_values_and_differences() -> None:
    k = np.array([-0.2, 0.05, 0.3], dtype=np.float64)
    parameters = np.array([0.01, 0.2, -0.4, 0.03, 0.15], dtype=np.float64)
    w, first, second = fit._raw_svi_value_derivatives(k, parameters)
    np.testing.assert_allclose(
        w,
        [0.08331812087098392, 0.03866549190084311, 0.050173780845922],
        rtol=2e-15,
        atol=2e-16,
    )
    h = 1e-5
    plus = fit._raw_svi_value_derivatives(k + h, parameters)[0]
    minus = fit._raw_svi_value_derivatives(k - h, parameters)[0]
    np.testing.assert_allclose(first, (plus - minus) / (2.0 * h), rtol=2e-9, atol=1e-11)
    np.testing.assert_allclose(
        second, (plus - 2.0 * w + minus) / h**2, rtol=3e-6, atol=2e-7
    )


def test_ssvi_and_raw_analytic_constraint_slacks_enforce_every_barrier() -> None:
    policy = FitPolicy()
    ssvi_ok = fit._ssvi_constraint_slacks(
        np.array([0.03, 0.04]), rho=-0.2, eta=0.5, gamma=0.3, policy=policy
    )
    assert min(ssvi_ok.values()) >= 0.0
    assert fit._ssvi_constraint_slacks(
        np.array([0.04, 0.03]), rho=-0.2, eta=0.5, gamma=0.3, policy=policy
    )["theta_monotonic"] < 0.0
    assert min(
        fit._ssvi_constraint_slacks(
            np.array([0.03, 0.04]), rho=-0.2, eta=100.0, gamma=0.0, policy=policy
        )[name]
        for name in ("barrier_one", "barrier_two")
    ) < 0.0

    raw_ok = fit._raw_svi_constraint_slacks(
        np.array([0.01, 0.2, -0.4, 0.03, 0.15]), policy
    )
    assert min(raw_ok.values()) >= 0.0
    assert raw_ok["global_minimum"] == pytest.approx(
        0.01 + 0.2 * 0.15 * np.sqrt(1.0 - 0.4**2) - policy.constraint_margin
    )
    assert fit._raw_svi_constraint_slacks(
        np.array([-0.04, 0.2, 0.0, 0.03, 0.15]), policy
    )["global_minimum"] < 0.0
    assert fit._raw_svi_constraint_slacks(
        np.array([0.01, 1.5, 0.5, 0.03, 0.15]), policy
    )["right_wing"] < 0.0


def test_golden_ssvi_and_raw_objectives_and_nrmse_scale_are_exact() -> None:
    policy = FitPolicy()
    k_by_maturity = (
        np.array([-0.2, 0.05, 0.3]),
        np.array([-0.15, 0.1, 0.25, 0.4]),
    )
    w_by_maturity = (
        np.array([0.035, 0.04, 0.052]),
        np.array([0.052, 0.055, 0.06, 0.07]),
    )
    ssvi_parameters = np.array([0.04, 0.055, -0.3, 0.7, 0.25])
    assert fit._ssvi_objective(
        ssvi_parameters, k_by_maturity, w_by_maturity, policy
    ) == pytest.approx(0.10949762428614794, rel=2e-15, abs=2e-16)

    raw_parameters = np.array([0.01, 0.2, -0.4, 0.03, 0.15])
    raw_objective = fit._raw_svi_objective(
        raw_parameters, k_by_maturity[0], w_by_maturity[0], policy
    )
    assert raw_objective == pytest.approx(
        0.48744933182676004, rel=1e-14, abs=1e-16
    )

    metrics = fit._fit_error_metrics(
        np.array([0.01, 0.02, 0.09]), np.array([0.02, 0.01, 0.08]), policy
    )
    assert metrics["rmse_total_variance"] == pytest.approx(0.01)
    assert metrics["nrmse_total_variance"] == pytest.approx(0.5)


@pytest.mark.parametrize(
    ("builder_name", "method"),
    [("_create_pchip_curve", FitMethod.PCHIP), ("_create_linear_curve", FitMethod.LINEAR)],
)
def test_interpolators_hit_nodes_and_never_extrapolate(
    builder_name: str, method: FitMethod
) -> None:
    k = np.array([-0.3, -0.1, 0.2, 0.4])
    w = np.array([0.05, 0.035, 0.04, 0.06])
    if method is FitMethod.LINEAR:
        k = k[:3]
        w = w[:3]
    builder = getattr(fit, builder_name)
    curve = builder(time_to_expiry=0.25, k_nodes=k, total_variance_nodes=w)
    result = evaluate_curve(
        curve,
        np.r_[np.nextafter(k[0], -np.inf), k, np.nextafter(k[-1], np.inf)],
    )
    assert curve.method is method
    assert result.supported.tolist() == [False, *([True] * k.size), False]
    assert result.total_variance.tolist()[0] is None
    assert result.total_variance.tolist()[-1] is None
    np.testing.assert_allclose(result.total_variance.tolist()[1:-1], w, rtol=0.0, atol=2e-16)


def test_curve_builders_reject_method_ineligible_node_counts() -> None:
    with pytest.raises(ValueError):
        fit._create_ssvi_curve(
            time_to_expiry=0.25,
            k_min=-0.2,
            k_max=0.2,
            raw_k=np.array([-0.2, 0.0, 0.2]),
            theta=0.04,
            rho=-0.3,
            eta=0.7,
            gamma=0.25,
        )
    with pytest.raises(ValueError):
        fit._create_raw_svi_curve(
            time_to_expiry=0.25,
            k_min=-0.2,
            k_max=0.2,
            raw_k=np.array([-0.2, -0.1, 0.1, 0.2]),
            parameters=np.array([0.04, 0.2, -0.3, 0.0, 0.25]),
        )
    with pytest.raises(ValueError):
        fit._create_pchip_curve(
            time_to_expiry=0.25,
            k_nodes=np.array([-0.2, 0.0, 0.2]),
            total_variance_nodes=np.array([0.04, 0.03, 0.05]),
        )
    with pytest.raises(ValueError):
        fit._create_linear_curve(
            time_to_expiry=0.25,
            k_nodes=np.array([-0.3, -0.1, 0.1, 0.3]),
            total_variance_nodes=np.array([0.04, 0.03, 0.05, 0.06]),
        )


def test_normalized_black_checks_use_nonuniform_strike_ratio_monotonicity_and_secants() -> None:
    k = np.array([-0.3, -0.1, 0.05, 0.3])
    call = fit._normalized_black_call(k, np.full(k.shape, 0.04))
    assert np.all(np.diff(call) < 0.0)
    curve = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=k,
        total_variance_nodes=np.full(k.shape, 0.04),
    )
    assert fit._check_call_price_monotonic(curve, k, FitPolicy()).status is CheckStatus.PASSED
    assert fit._check_call_price_convex(curve, k, FitPolicy()).status is CheckStatus.PASSED

    increasing_call_curve = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=k,
        total_variance_nodes=np.array([0.01, 1.0, 0.01, 1.0]),
    )
    nonconvex_curve = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=k,
        total_variance_nodes=np.array([0.04, 0.3, 0.01, 0.4]),
    )
    assert fit._check_call_price_monotonic(
        increasing_call_curve, k, FitPolicy()
    ).reason_code == "call_price_increase"
    convex = fit._check_call_price_convex(nonconvex_curve, k, FitPolicy())
    assert convex.status is CheckStatus.FAILED
    assert convex.reason_code == "decreasing_secant_slope"
    assert convex.status is not CheckStatus.INDETERMINATE


def test_composite_grid_contains_raw_knots_and_both_knot_neighbors() -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-test", base_grid_size=11
    )
    curve = fit._create_linear_curve(
        time_to_expiry=0.25,
        k_nodes=np.array([-1.0, 0.0, 1.0]),
        total_variance_nodes=np.array([0.04, 0.05, 0.06]),
    )
    grid = fit._composite_check_grid(curve, np.array([-1.0, -0.123456789, 1.0]), policy)
    for required in (-1.0, -0.123456789, -0.01, 0.0, 0.01, 1.0):
        assert required in grid


def test_positive_refinement_can_be_resolution_limited_but_price_shape_never_is() -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-test",
        base_grid_size=5,
        max_refinement_depth=2,
    )
    curve = fit._create_curve_model(
        method=FitMethod.RAW_SVI,
        time_to_expiry=0.25,
        k_min=-0.1,
        k_max=0.1,
        evaluator=lambda k: np.full(np.asarray(k).shape, policy.variance_floor * 6.0),
        knots=np.array([-0.1, 0.1]),
    )
    positive = fit._check_positive_total_variance(curve, curve.knots, policy)
    assert positive.status is CheckStatus.INDETERMINATE
    assert positive.conclusion == "unreliable"
    assert positive.reason_code == "resolution_limit"
    for check in (
        fit._check_call_price_monotonic(curve, fit._composite_check_grid(curve, curve.knots, policy), policy),
        fit._check_call_price_convex(curve, fit._composite_check_grid(curve, curve.knots, policy), policy),
    ):
        assert check.status is not CheckStatus.INDETERMINATE
        assert check.reason_code != "resolution_limit"


def test_ssvi_and_raw_use_analytic_g_and_interpolators_close_the_gate() -> None:
    policy = FitPolicy()
    ssvi = fit._create_ssvi_curve(
        time_to_expiry=0.25,
        k_min=-0.5,
        k_max=0.5,
        raw_k=np.array([-0.5, -0.15, 0.15, 0.5]),
        theta=0.04,
        rho=-0.3,
        eta=0.7,
        gamma=0.25,
    )
    raw_good = fit._create_raw_svi_curve(
        time_to_expiry=0.25,
        k_min=-0.5,
        k_max=0.5,
        raw_k=np.array([-0.5, -0.25, 0.0, 0.25, 0.5]),
        parameters=np.array([0.04, 0.2, -0.3, 0.0, 0.25]),
    )
    raw_narrow_violation = fit._create_raw_svi_curve(
        time_to_expiry=0.25,
        k_min=-0.5,
        k_max=0.5,
        raw_k=np.array([-0.5, -0.35, -0.1, 0.2, 0.5]),
        parameters=np.array(
            [
                0.054139377646245455,
                0.6128125548585291,
                0.6266249154210204,
                -0.2425133644203067,
                2.17840440110165e-05,
            ]
        ),
    )
    assert fit._check_butterfly_g_nonnegative(ssvi, ssvi.knots, policy).status is CheckStatus.PASSED
    assert fit._check_butterfly_g_nonnegative(raw_good, raw_good.knots, policy).status is CheckStatus.PASSED
    base_only = np.linspace(-0.5, 0.5, policy.base_grid_size)
    assert np.min(fit._butterfly_g_values(raw_narrow_violation, base_only)) == pytest.approx(
        0.0008088493175652616, rel=2e-12, abs=2e-15
    )
    bad = fit._check_butterfly_g_nonnegative(
        raw_narrow_violation, raw_narrow_violation.knots, policy
    )
    assert bad.status is CheckStatus.FAILED
    assert bad.reason_code == "negative_g"
    assert bad.primary_value < -policy.butterfly_g_tolerance

    pchip = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=np.array([-0.2, -0.05, 0.1, 0.2]),
        total_variance_nodes=np.array([0.04, 0.035, 0.04, 0.05]),
    )
    interpolation_check = fit._check_butterfly_g_nonnegative(pchip, pchip.knots, policy)
    assert interpolation_check.status is CheckStatus.NOT_APPLICABLE
    assert interpolation_check.reason_code == "method_has_no_analytic_g"


@pytest.mark.parametrize(
    ("later_level", "expected_status", "expected_reason"),
    [
        (0.05, CheckStatus.PASSED, None),
        (0.03, CheckStatus.FAILED, "calendar_total_variance_decrease"),
        (0.039799, CheckStatus.INDETERMINATE, "resolution_limit"),
    ],
)
def test_calendar_pair_uses_one_common_adaptive_grid_and_closed_outcomes(
    later_level: float, expected_status: CheckStatus, expected_reason: str | None
) -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-test",
        base_grid_size=9,
        max_refinement_depth=2,
    )
    earlier = fit._create_linear_curve(
        time_to_expiry=0.2,
        k_nodes=np.array([-0.3, 0.0, 0.3]),
        total_variance_nodes=np.full(3, 0.04),
    )
    later = fit._create_linear_curve(
        time_to_expiry=0.4,
        k_nodes=np.array([-0.2, 0.05, 0.4]),
        total_variance_nodes=np.full(3, later_level),
    )
    pair = fit._check_calendar_pair(
        pair_check_id=PAIR_A,
        phase="expiry_selection",
        earlier_maturity_id="ag2505",
        later_maturity_id="ag2506",
        earlier_attempt_id=ATTEMPT_A,
        later_attempt_id=ATTEMPT_B,
        parent_attempt_id=None,
        earlier_curve=earlier,
        later_curve=later,
        earlier_raw_k=earlier.knots,
        later_raw_k=later.knots,
        policy=policy,
    )
    assert pair.common_k_min == -0.2
    assert pair.common_k_max == 0.3
    assert pair.check.status is expected_status
    assert pair.check.reason_code == expected_reason
    assert pair.check.grid_point_count >= policy.base_grid_size


def test_calendar_pair_without_public_domain_is_not_testable_no_overlap() -> None:
    earlier = fit._create_linear_curve(
        time_to_expiry=0.2,
        k_nodes=np.array([-0.4, -0.3]),
        total_variance_nodes=np.array([0.04, 0.04]),
    )
    later = fit._create_linear_curve(
        time_to_expiry=0.4,
        k_nodes=np.array([-0.3, -0.2]),
        total_variance_nodes=np.array([0.05, 0.05]),
    )
    pair = fit._check_calendar_pair(
        pair_check_id=PAIR_A,
        phase="expiry_selection",
        earlier_maturity_id="ag2505",
        later_maturity_id="ag2506",
        earlier_attempt_id=ATTEMPT_A,
        later_attempt_id=ATTEMPT_B,
        parent_attempt_id=None,
        earlier_curve=earlier,
        later_curve=later,
        earlier_raw_k=earlier.knots,
        later_raw_k=later.knots,
        policy=FitPolicy(),
    )
    assert pair.common_k_min is None and pair.common_k_max is None
    assert pair.check.status is CheckStatus.NOT_TESTABLE
    assert pair.check.conclusion == "not_testable"
    assert pair.check.reason_code == "no_overlap"


def test_jump_check_passes_constant_curve_rejects_spike_and_closes_later_gates() -> None:
    policy = FitPolicy()
    k = np.array([-0.3, -0.1, 0.1, 0.3])
    smooth = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=k,
        total_variance_nodes=np.full(4, 0.25 * 0.2**2),
    )
    smooth_jump = fit._check_jump_reliable(smooth, k, np.full(4, 0.2), policy)
    assert smooth_jump.status is CheckStatus.PASSED
    spike_iv = np.array([0.2, 0.2, 1.5, 0.2])
    spike = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=k,
        total_variance_nodes=spike_iv**2 * 0.25,
    )
    spike_jump = fit._check_jump_reliable(spike, k, spike_iv, policy)
    assert spike_jump.status is CheckStatus.FAILED
    assert spike_jump.reason_code in {
        "absolute_iv_slope_exceeded",
        "robust_iv_slope_ratio_exceeded",
    }

    invalid = fit._create_curve_model(
        method=FitMethod.LINEAR,
        time_to_expiry=0.25,
        k_min=-0.3,
        k_max=0.3,
        evaluator=lambda values: np.full(np.asarray(values).shape, -0.01),
        knots=np.array([-0.3, 0.3]),
    )
    checks = fit._run_local_checks(invalid, invalid.knots, np.array([0.2, 0.2]), policy)
    assert checks["positive_total_variance"].status is CheckStatus.FAILED
    for name in (
        "call_price_monotonic",
        "call_price_convex",
        "jump_reliable",
        "calendar_consistent",
    ):
        assert checks[name].status is CheckStatus.NOT_APPLICABLE
        assert checks[name].reason_code == "not_run"
    butterfly = checks["butterfly_g_nonnegative"]
    assert butterfly.status is CheckStatus.NOT_APPLICABLE
    assert butterfly.reason_code == "method_has_no_analytic_g"


def test_pchip_enumerates_all_stationary_roots_and_matches_dense_reference() -> None:
    policy = FitPolicy()
    k = np.array([-0.4, -0.2, 0.0, 0.15, 0.4])
    iv = np.array([0.25, 0.55, 0.18, 0.7, 0.22])
    curve = fit._create_pchip_curve(
        time_to_expiry=0.3,
        k_nodes=k,
        total_variance_nodes=iv**2 * 0.3,
    )
    stationary = fit._pchip_stationary_points(curve, policy)
    assert stationary.size > curve.knots.size
    analytic_value, analytic_k = fit._pchip_max_abs_iv_slope(curve, policy)
    dense_k = np.linspace(k[0], k[-1], 500_001)
    dense_w = np.asarray(curve._evaluator(dense_k), dtype=np.float64)
    dense_first = np.asarray(curve._first_derivative(dense_k), dtype=np.float64)
    dense_abs = np.abs(dense_first) / (2.0 * np.sqrt(curve.time_to_expiry * dense_w))
    assert analytic_value == pytest.approx(float(np.max(dense_abs)), rel=2e-7, abs=2e-7)
    assert abs(analytic_k - dense_k[int(np.argmax(dense_abs))]) <= 3e-6


def test_linear_jump_maximum_uses_each_segment_minimum_w_endpoint() -> None:
    curve = fit._create_linear_curve(
        time_to_expiry=0.5,
        k_nodes=np.array([-0.3, 0.0, 0.4]),
        total_variance_nodes=np.array([0.02, 0.08, 0.04]),
    )
    value, location = fit._linear_max_abs_iv_slope(curve)
    expected = (0.08 - 0.02) / 0.3 / (2.0 * np.sqrt(0.5 * 0.02))
    assert value == pytest.approx(expected)
    assert location == -0.3


@pytest.mark.parametrize(
    "bad_result",
    [
        SimpleNamespace(success=False),
        SimpleNamespace(success=True, x=np.array([0.0]), fun=-1.0),
        SimpleNamespace(
            success=True,
            x=np.array([0.0]),
            fun=-1.0,
            xl=np.array([[0.0]]),
            funl=np.array([np.nan]),
        ),
    ],
)
def test_parameter_jump_requires_complete_finite_successful_shgo_result(
    monkeypatch: pytest.MonkeyPatch, bad_result: object
) -> None:
    curve = fit._create_raw_svi_curve(
        time_to_expiry=0.25,
        k_min=-0.3,
        k_max=0.3,
        raw_k=np.array([-0.3, -0.15, 0.0, 0.15, 0.3]),
        parameters=np.array([0.04, 0.2, -0.3, 0.0, 0.25]),
    )
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: bad_result)
    check = fit._check_jump_reliable(
        curve, curve.knots, np.array([0.45, 0.425, 0.4, 0.375, 0.35]), FitPolicy()
    )
    assert check.status is CheckStatus.INDETERMINATE
    assert check.conclusion == "unreliable"
    assert check.reason_code == "resolution_limit"


def test_jump_root_or_shgo_exception_is_closed_as_resolution_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = fit._create_raw_svi_curve(
        time_to_expiry=0.25,
        k_min=-0.3,
        k_max=0.3,
        raw_k=np.array([-0.3, -0.15, 0.0, 0.15, 0.3]),
        parameters=np.array([0.04, 0.2, -0.3, 0.0, 0.25]),
    )

    def raise_solver(*args: object, **kwargs: object) -> object:
        raise RuntimeError("solver failed")

    monkeypatch.setattr(fit, "shgo", raise_solver)
    raw_check = fit._check_jump_reliable(
        raw, raw.knots, np.array([0.45, 0.425, 0.4, 0.375, 0.35]), FitPolicy()
    )
    assert raw_check.status is CheckStatus.INDETERMINATE
    assert raw_check.reason_code == "resolution_limit"

    pchip = fit._create_pchip_curve(
        time_to_expiry=0.25,
        k_nodes=np.array([-0.3, -0.1, 0.1, 0.3]),
        total_variance_nodes=np.array([0.02, 0.06, 0.03, 0.05]),
    )

    def raise_roots(*args: object, **kwargs: object) -> np.ndarray:
        raise np.linalg.LinAlgError("root solver failed")

    monkeypatch.setattr(fit.np, "roots", raise_roots)
    pchip_check = fit._check_jump_reliable(
        pchip, pchip.knots, np.array([0.3, 0.49, 0.35, 0.45]), FitPolicy()
    )
    assert pchip_check.status is CheckStatus.INDETERMINATE
    assert pchip_check.reason_code == "resolution_limit"


def test_parameter_jump_calls_fixed_shgo_and_matches_dense_reference(monkeypatch: pytest.MonkeyPatch) -> None:
    curve = fit._create_raw_svi_curve(
        time_to_expiry=0.25,
        k_min=-0.3,
        k_max=0.3,
        raw_k=np.array([-0.3, -0.15, 0.0, 0.15, 0.3]),
        parameters=np.array([0.04, 0.2, -0.3, 0.0, 0.25]),
    )
    real_shgo = fit.shgo
    calls: list[dict[str, object]] = []

    def recording_shgo(*args: object, **kwargs: object) -> object:
        calls.append(copy.deepcopy(kwargs))
        return real_shgo(*args, **kwargs)

    monkeypatch.setattr(fit, "shgo", recording_shgo)
    value, location = fit._parameter_max_abs_iv_slope(curve, FitPolicy())
    assert calls == [
        {
            "bounds": [(-0.3, 0.3)],
            "n": 256,
            "iters": 3,
            "sampling_method": "simplicial",
            "workers": 1,
            "minimizer_kwargs": {
                "method": "SLSQP",
                "options": {"ftol": 1e-12, "maxiter": 500, "disp": False},
            },
        }
    ]
    dense_k = np.linspace(-0.3, 0.3, 500_001)
    dense_w = np.asarray(curve._evaluator(dense_k), dtype=np.float64)
    dense_first = np.asarray(curve._first_derivative(dense_k), dtype=np.float64)
    dense_abs = np.abs(dense_first) / (2.0 * np.sqrt(0.25 * dense_w))
    assert value == pytest.approx(float(np.max(dense_abs)), rel=2e-7, abs=2e-7)
    assert -0.3 <= location <= 0.3


def test_jump_conclusion_is_independent_of_base_grid_size() -> None:
    k = np.array([-0.4, -0.2, 0.0, 0.15, 0.4])
    iv = np.array([0.25, 0.55, 0.18, 0.7, 0.22])
    curve = fit._create_pchip_curve(
        time_to_expiry=0.3,
        k_nodes=k,
        total_variance_nodes=iv**2 * 0.3,
    )
    small = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-small-grid", base_grid_size=51
    )
    large = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-large-grid", base_grid_size=401
    )
    first = fit._check_jump_reliable(curve, k, iv, small)
    second = fit._check_jump_reliable(curve, k, iv, large)
    assert dataclasses.asdict(first) == dataclasses.asdict(second)


def test_adaptive_refinement_stops_after_exactly_max_depth_rounds() -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-depth-audit",
        base_grid_size=3,
        max_refinement_depth=2,
    )
    result = fit._adaptive_margin_grid(
        np.array([0.0, 0.5, 1.0]),
        lambda points: np.full(points.shape, 0.5),
        tolerance=1.0,
        policy=policy,
    )
    np.testing.assert_array_equal(result.grid, np.linspace(0.0, 1.0, 9))
    assert result.refinement_depth == 2
    assert result.max_depth_triggered is True
    assert result.resolution_limited is True
    assert result.minimum_interval == 0.125


def test_violation_only_on_forbidden_extra_round_remains_resolution_limited() -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-depth-counterexample",
        base_grid_size=3,
        max_refinement_depth=2,
    )

    def total_variance(points: np.ndarray) -> np.ndarray:
        values = np.full(points.shape, policy.variance_floor * 1.5)
        values[points == 0.0625] = policy.variance_floor * 0.5
        return values

    curve = fit._create_curve_model(
        method=FitMethod.RAW_SVI,
        time_to_expiry=0.25,
        k_min=0.0,
        k_max=1.0,
        evaluator=total_variance,
        knots=np.array([0.0, 1.0]),
    )
    check = fit._check_positive_total_variance(curve, curve.knots, policy)
    assert check.status is CheckStatus.INDETERMINATE
    assert check.conclusion == "unreliable"
    assert check.reason_code == "resolution_limit"
    assert check.grid_point_count == 9
    assert check.metrics["refinement_depth"] == 2
    assert check.metrics["minimum_interval"] == 0.125


def test_nonfinite_midpoint_probe_is_retained_and_positive_check_fails_closed() -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-nonfinite-positive",
        base_grid_size=3,
        max_refinement_depth=2,
    )

    def total_variance(points: np.ndarray) -> np.ndarray:
        values = np.full(points.shape, 0.04)
        values[points == 0.25] = np.nan
        return values

    curve = fit._create_curve_model(
        method=FitMethod.RAW_SVI,
        time_to_expiry=0.25,
        k_min=0.0,
        k_max=1.0,
        evaluator=total_variance,
        knots=np.array([0.0, 1.0]),
    )
    check = fit._check_positive_total_variance(curve, curve.knots, policy)
    assert check.status is CheckStatus.FAILED
    assert check.reason_code == "non_finite_total_variance"
    assert check.grid_point_count == 5
    assert check.metrics == {
        "non_finite_count": 1,
        "refinement_depth": 1,
        "non_finite_probe": True,
    }


def test_nonfinite_midpoint_probe_makes_g_and_calendar_indeterminate() -> None:
    policy = FitPolicy(
        policy_version="total-variance-fit-diagnostic-v2-nonfinite-margins",
        base_grid_size=3,
        max_refinement_depth=2,
    )

    def first_derivative(points: np.ndarray) -> np.ndarray:
        values = np.zeros(points.shape)
        values[points == 0.25] = np.nan
        return values

    g_curve = fit._create_curve_model(
        method=FitMethod.RAW_SVI,
        time_to_expiry=0.25,
        k_min=0.0,
        k_max=1.0,
        evaluator=lambda points: np.full(points.shape, 0.04),
        knots=np.array([0.0, 1.0]),
        first_derivative=first_derivative,
        second_derivative=lambda points: np.zeros(points.shape),
    )
    g_check = fit._check_butterfly_g_nonnegative(g_curve, g_curve.knots, policy)
    assert g_check.status is CheckStatus.INDETERMINATE
    assert g_check.conclusion == "unreliable"
    assert g_check.reason_code == "resolution_limit"
    assert g_check.grid_point_count == 5
    assert g_check.metrics["refinement_depth"] == 1
    assert g_check.metrics["non_finite_probe"] is True

    earlier = fit._create_curve_model(
        method=FitMethod.LINEAR,
        time_to_expiry=0.2,
        k_min=0.0,
        k_max=1.0,
        evaluator=lambda points: np.full(points.shape, 0.04),
        knots=np.array([0.0, 1.0]),
    )

    def later_variance(points: np.ndarray) -> np.ndarray:
        values = np.full(points.shape, 0.05)
        values[points == 0.25] = np.nan
        return values

    later = fit._create_curve_model(
        method=FitMethod.LINEAR,
        time_to_expiry=0.4,
        k_min=0.0,
        k_max=1.0,
        evaluator=later_variance,
        knots=np.array([0.0, 1.0]),
    )
    pair = fit._check_calendar_pair(
        pair_check_id=PAIR_A,
        phase="expiry_selection",
        earlier_maturity_id="ag2505",
        later_maturity_id="ag2506",
        earlier_attempt_id=ATTEMPT_A,
        later_attempt_id=ATTEMPT_B,
        parent_attempt_id=None,
        earlier_curve=earlier,
        later_curve=later,
        earlier_raw_k=earlier.knots,
        later_raw_k=later.knots,
        policy=policy,
    )
    assert pair.check.status is CheckStatus.INDETERMINATE
    assert pair.check.conclusion == "unreliable"
    assert pair.check.reason_code == "resolution_limit"
    assert pair.check.grid_point_count == 5
    assert pair.check.metrics["refinement_depth"] == 1
    assert pair.check.metrics["non_finite_probe"] is True


@pytest.mark.parametrize("method", [FitMethod.SSVI, FitMethod.RAW_SVI])
def test_parameter_curve_builders_obey_closed_domain_at_nextafter(method: FitMethod) -> None:
    if method is FitMethod.SSVI:
        curve = fit._create_ssvi_curve(
            time_to_expiry=0.25,
            k_min=-0.4,
            k_max=0.4,
            raw_k=np.array([-0.4, -0.1, 0.1, 0.4]),
            theta=0.04,
            rho=-0.3,
            eta=0.7,
            gamma=0.25,
        )
    else:
        curve = fit._create_raw_svi_curve(
            time_to_expiry=0.25,
            k_min=-0.4,
            k_max=0.4,
            raw_k=np.array([-0.4, -0.2, 0.0, 0.2, 0.4]),
            parameters=np.array([0.04, 0.2, -0.3, 0.0, 0.25]),
        )
    evaluated = evaluate_curve(
        curve,
        [
            np.nextafter(curve.k_min, -np.inf),
            curve.k_min,
            curve.k_max,
            np.nextafter(curve.k_max, np.inf),
        ],
    )
    assert evaluated.supported.tolist() == [False, True, True, False]
    assert evaluated.total_variance.tolist()[0] is None
    assert evaluated.total_variance.tolist()[-1] is None
    assert all(value is not None for value in evaluated.total_variance.tolist()[1:3])


def test_raw_left_and_right_wing_constraints_fail_independently() -> None:
    policy = FitPolicy()
    right = fit._raw_svi_constraint_slacks(
        np.array([0.01, 1.5, 0.5, 0.03, 0.15]), policy
    )
    left = fit._raw_svi_constraint_slacks(
        np.array([0.01, 1.5, -0.5, 0.03, 0.15]), policy
    )
    assert right["right_wing"] < 0.0 < right["left_wing"]
    assert left["left_wing"] < 0.0 < left["right_wing"]


def test_pchip_stationary_candidate_set_is_complete_and_locked() -> None:
    k = np.array([-0.4, -0.2, 0.0, 0.15, 0.4])
    iv = np.array([0.25, 0.55, 0.18, 0.7, 0.22])
    curve = fit._create_pchip_curve(
        time_to_expiry=0.3,
        k_nodes=k,
        total_variance_nodes=iv**2 * 0.3,
    )
    actual = fit._pchip_stationary_points(curve, FitPolicy())
    expected = np.array(
        [
            -0.4,
            -0.20000000000000007,
            -0.2,
            -0.060616225492318904,
            0.0,
            0.040052600460255335,
            0.15,
            0.4,
        ]
    )
    assert actual.size == expected.size
    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=5e-15)


def _local_expiry(
    maturity_id: str,
    time_to_expiry: float,
    k: list[float],
    total_variance: list[float],
    *,
    raw_node_count: int | None = None,
) -> object:
    return fit._LocalExpiryInput(
        maturity_id=maturity_id,
        time_to_expiry=time_to_expiry,
        raw_node_count=len(k) if raw_node_count is None else raw_node_count,
        k=np.asarray(k, dtype=np.float64),
        total_variance=np.asarray(total_variance, dtype=np.float64),
        implied_volatility=np.sqrt(
            np.asarray(total_variance, dtype=np.float64) / np.float64(time_to_expiry)
        ),
    )


def _complete_shgo_result(x: float = 0.0) -> SimpleNamespace:
    return SimpleNamespace(
        success=True,
        x=np.asarray([x], dtype=np.float64),
        fun=0.0,
        xl=np.asarray([[x]], dtype=np.float64),
        funl=np.asarray([0.0], dtype=np.float64),
    )


def test_ssvi_start_plan_locks_theta_initialization_bounds_and_all_27_indices() -> None:
    policy = FitPolicy()
    expiries = (
        _local_expiry(
            "30", 0.1, [-0.2, -0.1, 0.1, 0.3], [0.02, 0.04, 0.08, 0.1]
        ),
        _local_expiry(
            "60", 0.2, [0.1, 0.2, 0.3, 0.4], [0.03, 0.04, 0.05, 0.06]
        ),
    )

    plan = fit._prepare_ssvi_starts(expiries, policy)

    assert plan.generated_count == 27
    assert plan.precheck_discarded_count == 0
    assert plan.duplicate_discarded_count == 0
    assert plan.theta_upper == 1.0
    np.testing.assert_array_equal(plan.theta_initial, np.asarray([0.06, 0.06]))
    assert plan.bounds == (
        (1e-10, 1.0),
        (1e-10, 1.0),
        (-0.999, 0.999),
        (1e-8, 100.0),
        (0.0, 0.5),
    )
    assert [item.start_index for item in plan.starts] == list(range(27))
    expected = {
        0: (0.06, 0.06, -0.5, 0.1, 0.1),
        1: (0.06, 0.06, -0.5, 0.5, 0.1),
        2: (0.06, 0.06, -0.5, 1.0, 0.1),
        3: (0.06, 0.06, -0.5, 0.1, 0.3),
        8: (0.06, 0.06, -0.5, 1.0, 0.5),
        9: (0.06, 0.06, 0.0, 0.1, 0.1),
        26: (0.06, 0.06, 0.5, 1.0, 0.5),
    }
    for index, values in expected.items():
        np.testing.assert_array_equal(plan.starts[index].parameters, np.asarray(values))


def test_raw_start_plan_locks_scale_bounds_loop_order_and_all_36_indices() -> None:
    expiry = _local_expiry(
        "90",
        0.25,
        [-0.3, -0.1, 0.2, 0.4, 0.6],
        [0.05, 0.04, 0.06, 0.07, 0.08],
    )

    plan = fit._prepare_raw_svi_starts(expiry, FitPolicy())

    assert plan.generated_count == 36
    assert plan.precheck_discarded_count == 0
    assert plan.duplicate_discarded_count == 0
    assert plan.w_scale == pytest.approx(0.06)
    assert plan.span == pytest.approx(0.9)
    assert plan.bounds == (
        (-0.6, 0.6),
        (1e-8, 1.99999999),
        (-0.999, 0.999),
        (-2.0999999999999996, 2.4),
        (1e-8, 3.5999999999999996),
    )
    assert [item.start_index for item in plan.starts] == list(range(36))
    expected = {
        0: (0.02, 0.1, -0.5, -0.1, 0.09),
        1: (0.02, 0.1, -0.5, -0.1, 0.45),
        2: (0.02, 0.1, -0.5, 0.2, 0.09),
        4: (0.02, 0.5, -0.5, -0.1, 0.09),
        12: (0.02, 0.1, 0.0, -0.1, 0.09),
        35: (0.02, 1.0, 0.5, 0.2, 0.45),
    }
    by_index = {item.start_index: item.parameters for item in plan.starts}
    for index, values in expected.items():
        np.testing.assert_allclose(by_index[index], np.asarray(values), rtol=0, atol=1e-16)


def test_start_precheck_then_float64_exact_dedup_keeps_earliest_original_index() -> None:
    next_float = np.nextafter(np.float64(0.0), np.float64(1.0))
    generated = tuple(
        fit._IndexedStart(index, np.asarray(values, dtype=np.float64))
        for index, values in enumerate(
            (
                (0.0, 0.0),
                (0.0, -0.0),
                (next_float, 0.0),
                (np.nan, 0.0),
                (2.0, 0.0),
            )
        )
    )

    kept, precheck_count, duplicate_count = fit._precheck_and_deduplicate_starts(
        generated,
        lambda values: bool(np.isfinite(values).all() and np.all(np.abs(values) <= 1.0)),
    )

    assert precheck_count == 2
    assert duplicate_count == 1
    assert [item.start_index for item in kept] == [0, 2]
    assert kept[1].parameters[0] == next_float


def _outcome(
    *,
    start_index: int,
    objective: float | None,
    max_nrmse: float | None,
    parameters: tuple[float, ...] | None,
    stage_reached: int = 4,
    optimizer_success: bool = True,
    hard_failures: tuple[tuple[int, str], ...] = (),
    max_constraint_violation: float | None = 0.0,
) -> object:
    return fit._StartOutcome(
        start_index=start_index,
        optimizer_success=optimizer_success,
        parameters=parameters,
        objective=objective,
        stage_reached=stage_reached,
        max_nrmse=max_nrmse,
        max_constraint_violation=max_constraint_violation,
        hard_failures=hard_failures,
        payload=None,
        optimizer_message=None,
    )


def test_near_tie_success_selection_uses_nrmse_formatted_parameters_then_index() -> None:
    outcomes = (
        _outcome(start_index=0, objective=1.0, max_nrmse=0.10, parameters=(1.0,)),
        _outcome(start_index=1, objective=1.0 + 5e-13, max_nrmse=0.09, parameters=(3.0,)),
        _outcome(start_index=2, objective=1.0 + 2e-12, max_nrmse=0.01, parameters=(0.0,)),
        _outcome(start_index=3, objective=1.0 + 5e-13, max_nrmse=0.09, parameters=(2.0,)),
        _outcome(start_index=4, objective=1.0 + 5e-13, max_nrmse=0.09, parameters=(2.0,)),
    )

    selected, kind = fit._select_start_outcome(outcomes, FitPolicy())

    assert kind == "local_success"
    assert selected.start_index == 3


def test_failure_representative_uses_the_complete_fixed_tuple_and_15g_key() -> None:
    lower_stage = _outcome(
        start_index=0,
        objective=0.01,
        max_nrmse=0.01,
        parameters=(0.1,),
        stage_reached=3,
        hard_failures=((3, "parameter_constraint_failed"),),
    )
    more_failures_but_deeper = _outcome(
        start_index=1,
        objective=0.2,
        max_nrmse=0.2,
        parameters=(0.1234567890123456,),
        stage_reached=4,
        optimizer_success=False,
        hard_failures=((1, "optimizer_failed"), (4, "rmse_exceeded")),
    )
    same_depth_fewer_failures = _outcome(
        start_index=2,
        objective=0.3,
        max_nrmse=0.3,
        parameters=(9.0,),
        stage_reached=4,
        hard_failures=((4, "rmse_exceeded"),),
    )
    better_primary = _outcome(
        start_index=3,
        objective=0.4,
        max_nrmse=0.4,
        parameters=(8.0,),
        stage_reached=4,
        hard_failures=((3, "parameter_constraint_failed"),),
    )

    selected, kind = fit._select_start_outcome(
        (lower_stage, more_failures_but_deeper, same_depth_fewer_failures, better_primary),
        FitPolicy(),
    )

    assert kind == "failure_representative"
    assert selected.start_index == 3
    assert fit._failure_sort_key(more_failures_but_deeper, FitPolicy()) == (
        -4,
        2,
        1,
        0.2,
        0.2,
        0.0,
        ("0.123456789012346",),
        1,
    )
    missing = _outcome(
        start_index=9,
        objective=None,
        max_nrmse=None,
        parameters=None,
        stage_reached=0,
        optimizer_success=False,
        hard_failures=((2, "non_finite_parameters"),),
        max_constraint_violation=None,
    )
    missing_key = fit._failure_sort_key(missing, FitPolicy())
    assert np.isinf(missing_key[3:6]).all()
    assert missing_key[6] == ("\uffff",)


def test_raw_start_continues_to_stage_four_after_optimizer_reports_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiry = _local_expiry(
        "90",
        0.5,
        [-0.4, -0.2, 0.0, 0.2, 0.4],
        [0.0912, 0.07672135955, 0.07, 0.07272135955, 0.0832],
    )
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3], dtype=np.float64)
    result = SimpleNamespace(success=False, x=parameters, fun=0.0, message="iteration limit")
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: _complete_shgo_result())

    outcome = fit._evaluate_raw_start_outcome(
        start_index=7,
        optimizer_result=result,
        optimizer_exception=None,
        expiry=expiry,
        bounds=fit._prepare_raw_svi_starts(expiry, FitPolicy()).bounds,
        policy=FitPolicy(),
    )

    assert outcome.stage_reached == 4
    assert outcome.optimizer_success is False
    assert outcome.payload is not None
    assert outcome.max_nrmse is not None
    assert outcome.hard_failures[0] == (1, "optimizer_failed")


def test_convex_check_keeps_near_equal_float64_k_strike_intervals_finite() -> None:
    curve = fit._create_linear_curve(
        time_to_expiry=0.25,
        k_nodes=np.asarray([-0.1, 0.0, 0.1]),
        total_variance_nodes=np.asarray([0.04, 0.04, 0.04]),
    )
    grid = np.asarray([-0.1, 0.0, np.nextafter(0.0, 1.0), 0.1])

    check = fit._check_call_price_convex(curve, grid, FitPolicy())

    assert check.status is CheckStatus.PASSED
    assert check.grid_point_count == 4
    assert check.primary_value is not None
    assert check.primary_value == pytest.approx(0.09720123129227104, abs=1e-15)
    assert check.metrics["minimum_secant_slope_change"] == pytest.approx(
        0.09720123129227104, abs=1e-15
    )


@pytest.mark.parametrize(
    ("grid", "expected_minimum"),
    [
        (
            [-0.1, np.nextafter(0.1, -np.inf), 0.1, 0.2],
            0.18106302941363073,
        ),
        (
            [-0.1, 0.1, np.nextafter(0.1, np.inf), 0.2],
            0.021466248752266825,
        ),
    ],
    ids=["left_neighbor_uses_left_segment", "right_neighbor_uses_right_segment"],
)
def test_convex_cancellation_limit_uses_linear_interval_left_endpoint_segment(
    grid: list[float], expected_minimum: float
) -> None:
    curve = fit._create_linear_curve(
        time_to_expiry=0.25,
        k_nodes=np.asarray([-0.1, 0.1, 0.2]),
        total_variance_nodes=np.asarray([0.04, 0.04, 0.06]),
    )

    check = fit._check_call_price_convex(curve, np.asarray(grid), FitPolicy())

    assert check.status is CheckStatus.PASSED
    assert check.grid_point_count == 4
    assert check.primary_value == pytest.approx(expected_minimum, abs=1e-15)
    assert check.metrics["minimum_secant_slope_change"] == pytest.approx(
        expected_minimum, abs=1e-15
    )


def test_monotonic_cancellation_interval_uses_limiting_slope_price_change() -> None:
    curve = fit._create_linear_curve(
        time_to_expiry=0.25,
        k_nodes=np.asarray([-0.1, 0.1, 0.2]),
        total_variance_nodes=np.asarray([0.04, 0.04, 0.1]),
    )
    grid = np.asarray([0.1, np.nextafter(0.1, np.inf)])

    check = fit._check_call_price_monotonic(curve, grid, FitPolicy())

    assert check.status is CheckStatus.PASSED
    assert check.grid_point_count == 2
    assert check.primary_value == pytest.approx(3.4598524118749008e-18, abs=1e-30)
    assert check.metrics["maximum_positive_change"] == pytest.approx(
        3.4598524118749008e-18, abs=1e-30
    )


def test_raw_local_fit_uses_only_fixed_slsqp_and_one_draft_for_all_starts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3], dtype=np.float64)
    k = np.asarray([-0.4, -0.2, 0.0, 0.2, 0.4], dtype=np.float64)
    w = fit._raw_svi_value_derivatives(k, parameters)[0]
    expiry = _local_expiry("90", 0.5, k.tolist(), w.tolist())
    calls: list[dict[str, object]] = []

    def fake_minimize(objective: object, x0: object, **kwargs: object) -> SimpleNamespace:
        calls.append({"x0": np.asarray(x0).copy(), **kwargs})
        return SimpleNamespace(
            success=True,
            x=parameters.copy(),
            fun=fit._raw_svi_objective(parameters, k, w, FitPolicy()),
            message="ok",
        )

    monkeypatch.setattr(fit, "minimize", fake_minimize)
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: _complete_shgo_result())

    candidate = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert candidate is not None
    assert type(candidate) is fit._LocalFitCandidate
    assert len(calls) == 18
    assert all(call["method"] == "SLSQP" for call in calls)
    assert all(
        call["options"]
        == {"ftol": 1e-12, "maxiter": 2000, "eps": 1e-8, "disp": False}
        for call in calls
    )
    assert candidate.optimizer_start_summary == OptimizerStartSummary(
        generated_count=36,
        precheck_discarded_count=0,
        duplicate_discarded_count=18,
        executed_count=18,
        optimizer_reported_success_count=18,
        evaluable_count=18,
        local_success_count=18,
        selected_start_index=0,
        selection_kind="local_success",
    )
    assert candidate.local_success is True
    assert candidate.failure_code is None
    assert candidate.parameters == {
        "a": 0.04,
        "b": 0.1,
        "rho": -0.2,
        "m": 0.0,
        "sigma": 0.3,
    }
    np.testing.assert_array_equal(
        np.asarray(candidate.candidate_k),
        diagnostic_curve_grid(float(k[0]), float(k[-1]), k),
    )


def test_optimizer_success_with_failed_rmse_is_a_failure_representative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    k = np.asarray([-0.4, -0.2, 0.0, 0.2, 0.4], dtype=np.float64)
    observed_parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3])
    observed = fit._raw_svi_value_derivatives(k, observed_parameters)[0]
    expiry = _local_expiry("90", 0.5, k.tolist(), observed.tolist())
    poor_parameters = np.asarray([0.4, 0.01, 0.0, 0.0, 0.3], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True, x=poor_parameters.copy(), fun=9.0, message="ok"
        ),
    )
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: _complete_shgo_result())

    candidate = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert candidate is not None
    assert candidate.optimizer_success is True
    assert candidate.local_success is False
    assert candidate.failure_code == "rmse_exceeded"
    assert candidate.optimizer_start_summary is not None
    assert candidate.optimizer_start_summary.local_success_count == 0
    assert candidate.optimizer_start_summary.selection_kind == "failure_representative"


def test_ssvi_failure_representative_builds_one_parent_and_evaluable_child_drafts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    k = np.asarray([-0.3, -0.1, 0.1, 0.3], dtype=np.float64)
    rho, eta, gamma = -0.2, 0.3, 0.2
    theta_values = (0.04, 0.06)
    expiries = tuple(
        _local_expiry(
            maturity_id,
            time_to_expiry,
            k.tolist(),
            fit._ssvi_value_derivatives(
                k, theta=theta, rho=rho, eta=eta, gamma=gamma
            )[0].tolist(),
        )
        for maturity_id, time_to_expiry, theta in (
            ("30", 0.1, theta_values[0]),
            ("60", 0.2, theta_values[1]),
        )
    )
    parameters = np.asarray([*theta_values, rho, eta, gamma], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=False, x=parameters.copy(), fun=0.0, message="iteration limit"
        ),
    )
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: _complete_shgo_result())

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    assert type(bundle) is fit._LocalSsviBundle
    assert bundle.parent.local_success is False
    assert bundle.parent.failure_code == "optimizer_failed"
    assert bundle.parent.per_expiry_metrics is not None
    assert tuple(bundle.parent.per_expiry_metrics) == ("30", "60")
    assert len(bundle.children) == 2
    assert tuple(child.maturity_id for child in bundle.children) == ("30", "60")
    assert all(child.curve is not None for child in bundle.children)
    assert all(child.local_success for child in bundle.children)
    assert all(child.failure_code is None for child in bundle.children)
    assert all(
        child.checks["calendar_consistent"].reason_code == "not_run"
        for child in bundle.children
    )
    prohibited = {
        "attempt_id",
        "attempt_order",
        "attempt_status",
        "selection_eligible",
        "blocked_by_parent",
        "success",
    }
    assert prohibited.isdisjoint(field.name for field in dataclasses.fields(bundle.parent))


def test_local_candidate_builders_enforce_method_node_eligibility(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: _complete_shgo_result())

    def constant(count: int) -> object:
        return _local_expiry(
            str(count),
            0.25,
            np.linspace(-0.3, 0.3, count).tolist(),
            np.full(count, 0.04).tolist(),
        )

    assert fit.fit_raw_svi_local(constant(4)) is None
    assert fit.build_pchip_local_candidate(constant(3)) is None
    assert fit.build_pchip_local_candidate(constant(4)) is not None
    assert fit.build_linear_local_candidate(constant(1)) is None
    assert fit.build_linear_local_candidate(constant(2)) is not None
    assert fit.build_linear_local_candidate(constant(3)) is not None
    assert fit.build_linear_local_candidate(constant(4)) is None


def test_local_failure_representative_is_bitwise_deterministic_across_two_runs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    k = np.asarray([-0.4, -0.2, 0.0, 0.2, 0.4], dtype=np.float64)
    observed_parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3])
    observed = fit._raw_svi_value_derivatives(k, observed_parameters)[0]
    expiry = _local_expiry("90", 0.5, k.tolist(), observed.tolist())
    poor_parameters = np.asarray([0.4, 0.01, 0.0, 0.0, 0.3], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True, x=poor_parameters.copy(), fun=9.0, message="ok"
        ),
    )
    monkeypatch.setattr(fit, "shgo", lambda *args, **kwargs: _complete_shgo_result())

    first = fit.fit_raw_svi_local(expiry, policy=FitPolicy())
    second = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert first is not None and second is not None
    assert first.parameters == second.parameters
    assert first.optimizer_start_summary == second.optimizer_start_summary
    assert first.candidate_k == second.candidate_k
    assert first.candidate_total_variance == second.candidate_total_variance
    assert first.candidate_iv == second.candidate_iv
    assert first.failure_code == second.failure_code


def _raw_stage_expiry() -> object:
    return _local_expiry(
        "90",
        0.5,
        [-0.4, -0.2, 0.0, 0.2, 0.4],
        [0.08, 0.04, 0.06, 0.07, 0.09],
    )


def _raw_stage_outcome(
    expiry: object,
    parameters: np.ndarray,
) -> object:
    return fit._evaluate_raw_start_outcome(
        start_index=7,
        optimizer_result=SimpleNamespace(
            success=True, x=parameters, fun=0.0, message="ok"
        ),
        optimizer_exception=None,
        expiry=expiry,
        bounds=fit._prepare_raw_svi_starts(expiry, FitPolicy()).bounds,
        policy=FitPolicy(),
    )


def test_start_outcome_stage_zero_requires_no_finite_parameter_vector() -> None:
    outcome = _raw_stage_outcome(
        _raw_stage_expiry(),
        np.asarray([0.04, 0.1, np.nan, 0.0, 0.3]),
    )

    assert outcome.stage_reached == 0
    assert outcome.parameters is None
    assert outcome.payload is None
    assert outcome.primary_failure_code == "non_finite_parameters"


def test_start_outcome_stage_one_keeps_finite_parameters_after_node_evaluation_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiry = _raw_stage_expiry()
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3])
    monkeypatch.setattr(
        fit,
        "_curve_values",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("node evaluation")),
    )

    outcome = _raw_stage_outcome(expiry, parameters)

    assert outcome.stage_reached == 1
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is None
    assert outcome.primary_failure_code == "non_finite_parameters"


def test_start_outcome_stage_two_keeps_curve_when_constraint_evaluation_raises() -> None:
    expiry = _raw_stage_expiry()
    parameters = np.asarray([0.04, 0.1, 2.0, 0.0, 0.3])

    outcome = _raw_stage_outcome(expiry, parameters)

    assert outcome.stage_reached == 2
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is not None
    assert len(outcome.payload.curves) == 1
    assert outcome.payload.metrics == (None,)
    assert outcome.payload.checks == (None,)
    assert outcome.max_constraint_violation is None
    assert outcome.hard_failures == ()
    assert outcome.primary_failure_code is None


def test_start_outcome_stage_three_keeps_curve_when_metric_evaluation_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiry = _raw_stage_expiry()
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3])
    monkeypatch.setattr(
        fit,
        "_fit_metrics_for_curve",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("metric evaluation")),
    )

    outcome = _raw_stage_outcome(expiry, parameters)

    assert outcome.stage_reached == 3
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is not None
    assert len(outcome.payload.curves) == 1
    assert outcome.payload.metrics == (None,)
    assert outcome.payload.checks == (None,)
    assert outcome.hard_failures == ()
    assert outcome.primary_failure_code is None


def test_start_outcome_stage_three_keeps_metrics_when_local_check_evaluation_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3])
    k = np.asarray([-0.4, -0.2, 0.0, 0.2, 0.4])
    total_variance = fit._raw_svi_value_derivatives(k, parameters)[0]
    expiry = _local_expiry("90", 0.5, k.tolist(), total_variance.tolist())
    monkeypatch.setattr(
        fit,
        "_run_local_checks",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("check evaluation")),
    )

    outcome = _raw_stage_outcome(expiry, parameters)

    assert outcome.stage_reached == 3
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is not None
    assert len(outcome.payload.curves) == 1
    assert outcome.payload.metrics[0] is not None
    assert outcome.payload.checks == (None,)
    assert outcome.hard_failures == ()
    assert outcome.primary_failure_code is None


def test_raw_constraint_postprocess_exception_continues_all_36_starts_and_keeps_curve(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiry = _raw_stage_expiry()
    parameters = np.asarray([0.04, 0.1, 2.0, 0.0, 0.3])
    calls = 0

    def finite_result(*args: object, **kwargs: object) -> SimpleNamespace:
        nonlocal calls
        calls += 1
        return SimpleNamespace(
            success=True, x=parameters.copy(), fun=0.0, message="ok"
        )

    monkeypatch.setattr(fit, "minimize", finite_result)

    candidate = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert candidate is not None
    assert calls == 36
    assert candidate.optimizer_start_summary == OptimizerStartSummary(
        generated_count=36,
        precheck_discarded_count=0,
        duplicate_discarded_count=0,
        executed_count=36,
        optimizer_reported_success_count=36,
        evaluable_count=36,
        local_success_count=0,
        selected_start_index=0,
        selection_kind="failure_representative",
    )
    assert candidate.optimizer_success is True
    assert candidate.local_success is False
    assert candidate.failure_code == "check_resolution_limit"
    assert candidate.parameters == {
        "a": 0.04,
        "b": 0.1,
        "rho": 2.0,
        "m": 0.0,
        "sigma": 0.3,
    }
    assert candidate.curve is not None
    assert candidate.candidate_k
    assert len(candidate.candidate_k) == len(candidate.candidate_total_variance)
    assert candidate.rmse_total_variance is None
    assert all(
        check.status is CheckStatus.NOT_APPLICABLE and check.reason_code == "not_run"
        for name, check in candidate.checks.items()
        if name != "positive_total_variance"
    )
    assert candidate.checks["positive_total_variance"].status is CheckStatus.INDETERMINATE
    assert candidate.checks["positive_total_variance"].reason_code == "resolution_limit"


def _ssvi_stage_expiries() -> tuple[object, object]:
    k = np.asarray([-0.3, -0.1, 0.1, 0.3], dtype=np.float64)
    rho, eta, gamma = -0.2, 0.3, 0.2
    return tuple(
        _local_expiry(
            maturity_id,
            time_to_expiry,
            k.tolist(),
            fit._ssvi_value_derivatives(
                k, theta=theta, rho=rho, eta=eta, gamma=gamma
            )[0].tolist(),
        )
        for maturity_id, time_to_expiry, theta in (
            ("30", 0.1, 0.04),
            ("60", 0.2, 0.06),
        )
    )


def _assert_canonical_fail_closed_local_checks(
    checks: object,
) -> None:
    positive = checks["positive_total_variance"]
    assert positive.status is CheckStatus.INDETERMINATE
    assert positive.conclusion == "unreliable"
    assert positive.reason_code == "resolution_limit"
    assert positive.primary_value is None
    assert positive.threshold is None
    assert positive.violation_count is None
    assert positive.grid_point_count == 0
    assert positive.metrics == {"incomplete_stage": True}
    assert all(
        check.status is CheckStatus.NOT_APPLICABLE
        and check.conclusion == "not_applicable"
        and check.reason_code == "not_run"
        and check.primary_value is None
        and check.threshold is None
        and check.violation_count is None
        and check.grid_point_count == 0
        and check.metrics == {}
        for name, check in checks.items()
        if name != "positive_total_variance"
    )


def test_ssvi_constraint_postprocess_exception_reaches_stage_two_with_all_curves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2])
    bounds = fit._prepare_ssvi_starts(expiries, FitPolicy()).bounds
    monkeypatch.setattr(
        fit,
        "_ssvi_constraint_slacks",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("constraints")),
    )

    outcome = fit._evaluate_ssvi_start_outcome(
        start_index=3,
        optimizer_result=SimpleNamespace(
            success=True, x=parameters, fun=0.0, message="ok"
        ),
        optimizer_exception=None,
        expiries=expiries,
        bounds=bounds,
        policy=FitPolicy(),
    )

    assert outcome.stage_reached == 2
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is not None
    assert len(outcome.payload.curves) == 2
    assert outcome.payload.metrics == (None, None)
    assert outcome.payload.checks == (None, None)
    assert outcome.hard_failures == ()
    assert outcome.primary_failure_code is None


def test_ssvi_metric_exception_reaches_stage_three_and_keeps_all_curves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2])
    bounds = fit._prepare_ssvi_starts(expiries, FitPolicy()).bounds
    monkeypatch.setattr(
        fit,
        "_fit_metrics_for_curve",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("metrics")),
    )

    outcome = fit._evaluate_ssvi_start_outcome(
        start_index=3,
        optimizer_result=SimpleNamespace(
            success=True, x=parameters, fun=0.0, message="ok"
        ),
        optimizer_exception=None,
        expiries=expiries,
        bounds=bounds,
        policy=FitPolicy(),
    )

    assert outcome.stage_reached == 3
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is not None
    assert len(outcome.payload.curves) == 2
    assert outcome.payload.metrics == (None, None)
    assert outcome.payload.checks == (None, None)
    assert outcome.hard_failures == ()
    assert outcome.primary_failure_code is None


def test_ssvi_check_exception_reaches_stage_three_and_keeps_all_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2])
    bounds = fit._prepare_ssvi_starts(expiries, FitPolicy()).bounds
    monkeypatch.setattr(
        fit,
        "_run_local_checks",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("checks")),
    )

    outcome = fit._evaluate_ssvi_start_outcome(
        start_index=3,
        optimizer_result=SimpleNamespace(
            success=True, x=parameters, fun=0.0, message="ok"
        ),
        optimizer_exception=None,
        expiries=expiries,
        bounds=bounds,
        policy=FitPolicy(),
    )

    assert outcome.stage_reached == 3
    assert outcome.parameters == tuple(parameters)
    assert outcome.payload is not None
    assert len(outcome.payload.curves) == 2
    assert all(metric is not None for metric in outcome.payload.metrics)
    assert outcome.payload.checks == (None, None)
    assert outcome.hard_failures == ((5, "check_resolution_limit"),)
    assert outcome.primary_failure_code == "check_resolution_limit"


def test_ssvi_selected_finite_parameters_and_curves_survive_constraint_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2])
    plan = fit._prepare_ssvi_starts(expiries, FitPolicy())
    calls = 0

    def finite_result(*args: object, **kwargs: object) -> SimpleNamespace:
        nonlocal calls
        calls += 1
        return SimpleNamespace(
            success=True, x=parameters.copy(), fun=0.0, message="ok"
        )

    monkeypatch.setattr(fit, "_prepare_ssvi_starts", lambda *args: plan)
    monkeypatch.setattr(fit, "minimize", finite_result)
    monkeypatch.setattr(
        fit,
        "_ssvi_constraint_slacks",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("constraints")),
    )

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    assert calls == 27
    assert bundle.parent.optimizer_start_summary == OptimizerStartSummary(
        generated_count=27,
        precheck_discarded_count=0,
        duplicate_discarded_count=0,
        executed_count=27,
        optimizer_reported_success_count=27,
        evaluable_count=27,
        local_success_count=0,
        selected_start_index=0,
        selection_kind="failure_representative",
    )
    assert bundle.parent.failure_code == "check_resolution_limit"
    assert bundle.parent.parameters == {
        "rho": -0.2,
        "eta": 0.3,
        "gamma": 0.2,
        "theta_by_maturity": {"30": 0.04, "60": 0.06},
    }
    assert bundle.parent.per_expiry_metrics is not None
    assert tuple(bundle.parent.per_expiry_metrics) == ("30", "60")
    assert all(
        metric.rmse_total_variance is None
        and metric.nrmse_total_variance is None
        and metric.rmse_iv is None
        for metric in bundle.parent.per_expiry_metrics.values()
    )
    assert len(bundle.children) == 2
    assert all(child.curve is not None and child.candidate_k for child in bundle.children)
    assert all(child.parameters is not None for child in bundle.children)
    assert all(child.local_success is False for child in bundle.children)
    assert all(
        child.failure_code == "check_resolution_limit"
        for child in bundle.children
    )


def test_ssvi_stage_two_optimizer_failure_maps_children_to_resolution_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2])

    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=False,
            x=parameters.copy(),
            fun=0.0,
            message="synthetic optimizer failure",
        ),
    )
    monkeypatch.setattr(
        fit,
        "_maximum_constraint_violation",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("synthetic constraint postprocess failure")
        ),
    )

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    assert bundle.parent.failure_code == "optimizer_failed"
    assert bundle.parent.optimizer_start_summary.evaluable_count == 27
    assert bundle.parent.parameters is not None
    assert len(bundle.children) == 2
    for child in bundle.children:
        assert child.optimizer_attempted is False
        assert child.optimizer_success is None
        assert child.optimizer_start_summary is None
        assert child.parameters is not None
        assert child.curve is not None
        assert child.candidate_k
        assert child.local_success is False
        assert child.failure_code == "check_resolution_limit"
        assert child.failure_reason == "check_resolution_limit"
        positive = child.checks["positive_total_variance"]
        assert positive.status is CheckStatus.INDETERMINATE
        assert positive.reason_code == "resolution_limit"
        assert all(
            check.status is CheckStatus.NOT_APPLICABLE
            and check.reason_code == "not_run"
            for name, check in child.checks.items()
            if name != "positive_total_variance"
        )

    with pytest.raises(ValueError, match="non-optimizer|optimizer failure"):
        dataclasses.replace(
            bundle.children[0],
            failure_code="optimizer_failed",
            failure_reason="forged inherited optimizer failure",
        )
    with pytest.raises(ValueError, match="children|maturit|evaluable"):
        dataclasses.replace(bundle, children=())


def test_ssvi_stage_three_constraint_failure_keeps_fail_closed_children(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.6])

    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True,
            x=parameters.copy(),
            fun=0.0,
            message="synthetic parameter constraint failure",
        ),
    )
    monkeypatch.setattr(
        fit,
        "_run_local_checks",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("synthetic local check failure")
        ),
    )

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    assert bundle.parent.failure_code == "parameter_constraint_failed"
    assert bundle.parent.optimizer_start_summary.evaluable_count == 27
    assert bundle.parent.parameters is not None
    assert all(
        metric.rmse_total_variance is not None
        and metric.nrmse_total_variance is not None
        and metric.rmse_iv is not None
        for metric in bundle.parent.per_expiry_metrics.values()
    )
    assert len(bundle.children) == 2
    for child in bundle.children:
        assert child.parameters is not None
        assert child.curve is not None
        assert child.candidate_k
        assert child.local_success is False
        assert child.failure_code == "check_resolution_limit"
        assert child.failure_reason == "check_resolution_limit"
        assert child.checks == fit._fail_closed_local_checks()


def test_ssvi_rmse_failure_precedes_later_check_exception_for_every_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.05, 0.07, -0.2, 0.3, 0.2])
    policy = FitPolicy(
        policy_version="test-ssvi-rmse-before-check-resolution-v1",
        nrmse_limit=1.0e-12,
    )

    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True,
            x=parameters.copy(),
            fun=0.0,
            message="synthetic RMSE failure before check exception",
        ),
    )
    monkeypatch.setattr(
        fit,
        "_run_local_checks",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("synthetic later local check failure")
        ),
    )

    bundle = fit.fit_ssvi_local(expiries, policy=policy)

    assert bundle.parent.failure_code == "rmse_exceeded"
    assert len(bundle.children) == 2
    for child in bundle.children:
        parent_metric = bundle.parent.per_expiry_metrics[child.maturity_id]
        assert parent_metric.nrmse_total_variance is not None
        assert parent_metric.nrmse_total_variance > policy.nrmse_limit
        assert child.nrmse_total_variance == parent_metric.nrmse_total_variance
        assert child.parameters is not None
        assert child.candidate_k
        assert child.local_success is False
        assert child.failure_code == "rmse_exceeded"
        assert child.failure_reason == "rmse_exceeded"
        _assert_canonical_fail_closed_local_checks(child.checks)
        assert parent_metric.checks == child.checks


@pytest.mark.parametrize(
    ("optimizer_success", "expected_parent_failure"),
    [(False, "optimizer_failed"), (True, "rmse_exceeded")],
)
def test_ssvi_partial_metrics_classify_each_child_at_earliest_known_gate(
    monkeypatch: pytest.MonkeyPatch,
    optimizer_success: bool,
    expected_parent_failure: str,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.05, 0.07, -0.2, 0.3, 0.2])
    policy = FitPolicy(
        policy_version="test-ssvi-partial-metrics-gate-order-v1",
        nrmse_limit=1.0e-12,
    )
    real_fit_metrics = fit._fit_metrics_for_curve
    metric_calls = 0

    def first_metric_then_fail(*args: object, **kwargs: object) -> object:
        nonlocal metric_calls
        metric_calls += 1
        if metric_calls % 2 == 0:
            raise RuntimeError("synthetic second-expiry metric failure")
        return real_fit_metrics(*args, **kwargs)

    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=optimizer_success,
            x=parameters.copy(),
            fun=0.0,
            message="synthetic partial metrics representative",
        ),
    )
    monkeypatch.setattr(fit, "_fit_metrics_for_curve", first_metric_then_fail)

    bundle = fit.fit_ssvi_local(expiries, policy=policy)

    assert bundle.parent.failure_code == expected_parent_failure
    first, second = bundle.children
    assert first.maturity_id == "30"
    assert first.nrmse_total_variance is not None
    assert first.nrmse_total_variance > policy.nrmse_limit
    assert first.failure_code == "rmse_exceeded"
    _assert_canonical_fail_closed_local_checks(first.checks)
    assert bundle.parent.per_expiry_metrics["30"].checks == first.checks
    assert second.maturity_id == "60"
    assert second.nrmse_total_variance is None
    assert second.failure_code == "check_resolution_limit"
    _assert_canonical_fail_closed_local_checks(second.checks)
    assert bundle.parent.per_expiry_metrics["60"].checks == second.checks


@pytest.mark.parametrize(
    ("first_check_failed", "expected_parent_failure", "expected_child_failure"),
    [
        (False, "check_resolution_limit", None),
        (True, "non_positive_total_variance", "non_positive_total_variance"),
    ],
)
def test_ssvi_partial_checks_preserve_completed_child_gate_before_exception(
    monkeypatch: pytest.MonkeyPatch,
    first_check_failed: bool,
    expected_parent_failure: str,
    expected_child_failure: str | None,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2])
    policy = FitPolicy()
    real_local_checks = fit._run_local_checks
    check_calls = 0

    def first_checks_then_fail(*args: object, **kwargs: object) -> object:
        nonlocal check_calls
        check_calls += 1
        if check_calls % 2 == 0:
            raise RuntimeError("synthetic second-expiry check failure")
        checks = dict(real_local_checks(*args, **kwargs))
        assert all(
            check.status is CheckStatus.PASSED
            for name, check in checks.items()
            if name != "calendar_consistent"
        )
        assert checks["calendar_consistent"].status is CheckStatus.NOT_APPLICABLE
        assert checks["calendar_consistent"].reason_code == "not_run"
        if first_check_failed:
            checks["positive_total_variance"] = fit._failed_check_diagnostic(
                "positive_total_variance",
                reason_code="below_variance_floor",
                primary_value=-1.0,
                threshold=policy.variance_floor,
                violation_count=1,
                grid_point_count=1,
                metrics={},
            )
        return checks

    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True,
            x=parameters.copy(),
            fun=0.0,
            message="synthetic partial checks representative",
        ),
    )
    monkeypatch.setattr(fit, "_run_local_checks", first_checks_then_fail)

    bundle = fit.fit_ssvi_local(expiries, policy=policy)

    assert bundle.parent.failure_code == expected_parent_failure
    first, second = bundle.children
    assert first.maturity_id == "30"
    assert first.failure_code == expected_child_failure
    assert first.local_success is (expected_child_failure is None)
    assert bundle.parent.per_expiry_metrics["30"].checks == first.checks
    if first_check_failed:
        positive = first.checks["positive_total_variance"]
        assert positive.status is CheckStatus.FAILED
        assert positive.reason_code == "below_variance_floor"
    else:
        assert all(
            check.status is CheckStatus.PASSED
            for name, check in first.checks.items()
            if name != "calendar_consistent"
        )
    assert second.maturity_id == "60"
    assert second.failure_code == "check_resolution_limit"
    _assert_canonical_fail_closed_local_checks(second.checks)
    assert bundle.parent.per_expiry_metrics["60"].checks == second.checks


def test_ssvi_all_27_optimizer_exceptions_reconcile_and_keep_parent_metric_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiries = _ssvi_stage_expiries()
    calls = 0

    def raises(*args: object, **kwargs: object) -> object:
        nonlocal calls
        calls += 1
        raise RuntimeError("optimizer exploded")

    monkeypatch.setattr(fit, "minimize", raises)

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    assert calls == 27
    assert bundle.parent.optimizer_start_summary == OptimizerStartSummary(
        generated_count=27,
        precheck_discarded_count=0,
        duplicate_discarded_count=0,
        executed_count=27,
        optimizer_reported_success_count=0,
        evaluable_count=0,
        local_success_count=0,
        selected_start_index=0,
        selection_kind="failure_representative",
    )
    assert bundle.parent.failure_code == "optimizer_exception"
    assert bundle.parent.parameters is None
    assert bundle.children == ()
    assert bundle.parent.per_expiry_metrics is not None
    assert tuple(bundle.parent.per_expiry_metrics) == ("30", "60")
    for expiry, metric in zip(
        expiries, bundle.parent.per_expiry_metrics.values(), strict=True
    ):
        assert metric.time_to_expiry == expiry.time_to_expiry
        assert metric.raw_node_count == expiry.raw_node_count
        assert metric.node_count == expiry.node_count
        assert metric.k_min == expiry.k[0]
        assert metric.k_max == expiry.k[-1]
        assert metric.rmse_total_variance is None
        assert metric.nrmse_total_variance is None
        assert metric.rmse_iv is None
        assert all(
            check.status is CheckStatus.NOT_APPLICABLE
            and check.reason_code == "not_run"
            for check in metric.checks.values()
        )


def test_all_precheck_discarded_starts_reconcile_with_zero_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expiry = _raw_stage_expiry()
    original = fit._prepare_raw_svi_starts(expiry, FitPolicy())
    discarded = dataclasses.replace(
        original,
        precheck_discarded_count=36,
        duplicate_discarded_count=0,
        starts=(),
    )
    monkeypatch.setattr(fit, "_prepare_raw_svi_starts", lambda *args: discarded)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: pytest.fail("discarded starts must not execute"),
    )

    candidate = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert candidate is not None
    assert candidate.optimizer_start_summary == OptimizerStartSummary(
        generated_count=36,
        precheck_discarded_count=36,
        duplicate_discarded_count=0,
        executed_count=0,
        optimizer_reported_success_count=0,
        evaluable_count=0,
        local_success_count=0,
        selected_start_index=None,
        selection_kind=None,
    )
    assert candidate.optimizer_success is False
    assert candidate.parameters is None
    assert candidate.curve is None
    assert candidate.candidate_k == ()
    assert candidate.failure_code == "optimizer_failed"


def _exact_raw_stage_expiry() -> object:
    k = np.asarray([-0.4, -0.2, 0.0, 0.2, 0.4], dtype=np.float64)
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3], dtype=np.float64)
    total_variance = fit._raw_svi_value_derivatives(k, parameters)[0]
    return _local_expiry("90", 0.5, k.tolist(), total_variance.tolist())


def _materialize_failed_local_draft(candidate: object) -> FitAttemptDiagnostic:
    is_parent = candidate.scope is AttemptScope.TIMESTAMP
    is_ssvi_child = (
        candidate.method is FitMethod.SSVI
        and candidate.scope is AttemptScope.EXPIRY
    )
    return FitAttemptDiagnostic(
        attempt_id=ATTEMPT_A,
        parent_attempt_id=ATTEMPT_B if is_ssvi_child else None,
        scope=candidate.scope,
        product="ag",
        timestamp=TIMESTAMP,
        maturity_id=candidate.maturity_id,
        participating_maturities=list(candidate.participating_maturities),
        time_to_expiry=candidate.time_to_expiry,
        method=candidate.method,
        attempt_order=0,
        attempt_status=AttemptStatus.FAILED,
        optimizer_attempted=candidate.optimizer_attempted,
        optimizer_success=candidate.optimizer_success,
        optimizer_start_summary=candidate.optimizer_start_summary,
        selection_eligible=not is_parent,
        blocked_by_parent=False,
        local_success=candidate.local_success,
        success=False,
        parameters=None
        if candidate.parameters is None
        else dict(candidate.parameters),
        per_expiry_metrics=None
        if candidate.per_expiry_metrics is None
        else dict(candidate.per_expiry_metrics),
        rmse_total_variance=candidate.rmse_total_variance,
        nrmse_total_variance=candidate.nrmse_total_variance,
        rmse_iv=candidate.rmse_iv,
        raw_node_count=candidate.raw_node_count,
        node_count=candidate.node_count,
        k_min=candidate.k_min,
        k_max=candidate.k_max,
        candidate_k=list(candidate.candidate_k),
        candidate_total_variance=list(candidate.candidate_total_variance),
        candidate_iv=list(candidate.candidate_iv),
        checks=dict(candidate.checks),
        failure_code=candidate.failure_code,
        failure_reason=candidate.failure_reason or candidate.failure_code,
        policy_version=POLICY_VERSION,
        forward_source=ForwardSource.UNDERLYING_PRICE_PROXY,
    )


@pytest.mark.parametrize(
    ("check_function", "check_name"),
    [
        ("_check_call_price_monotonic", "call_price_monotonic"),
        ("_check_jump_reliable", "jump_reliable"),
    ],
)
def test_raw_check_exception_draft_round_trips_to_fit_attempt_diagnostic(
    monkeypatch: pytest.MonkeyPatch,
    check_function: str,
    check_name: str,
) -> None:
    expiry = _exact_raw_stage_expiry()
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True, x=parameters.copy(), fun=0.0, message="ok"
        ),
    )
    monkeypatch.setattr(
        fit,
        check_function,
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("local check")),
    )

    candidate = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert candidate is not None
    assert candidate.failure_code == "check_resolution_limit"
    assert candidate.checks[check_name].status is CheckStatus.INDETERMINATE
    assert candidate.checks[check_name].reason_code == "resolution_limit"
    attempt = _materialize_failed_local_draft(candidate)
    assert attempt.failure_code == "check_resolution_limit"


@pytest.mark.parametrize(
    ("check_function", "check_name"),
    [
        ("_check_call_price_monotonic", "call_price_monotonic"),
        ("_check_jump_reliable", "jump_reliable"),
    ],
)
def test_ssvi_check_exception_parent_and_children_round_trip_to_fit_attempts(
    monkeypatch: pytest.MonkeyPatch,
    check_function: str,
    check_name: str,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True, x=parameters.copy(), fun=0.0, message="ok"
        ),
    )
    monkeypatch.setattr(
        fit,
        check_function,
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("local check")),
    )

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    drafts = (bundle.parent, *bundle.children)
    assert len(drafts) == 3
    for draft in drafts:
        assert draft.failure_code == "check_resolution_limit"
        assert draft.checks[check_name].status is CheckStatus.INDETERMINATE
        assert draft.checks[check_name].reason_code == "resolution_limit"
        attempt = _materialize_failed_local_draft(draft)
        assert attempt.failure_code == "check_resolution_limit"


@pytest.mark.parametrize("failure_point", ["diagnostic_curve_grid", "evaluate_curve"])
def test_raw_candidate_array_exception_becomes_materializable_local_failure(
    monkeypatch: pytest.MonkeyPatch,
    failure_point: str,
) -> None:
    expiry = _exact_raw_stage_expiry()
    parameters = np.asarray([0.04, 0.1, -0.2, 0.0, 0.3], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True, x=parameters.copy(), fun=0.0, message="ok"
        ),
    )
    monkeypatch.setattr(
        fit, "_run_local_checks", lambda *args, **kwargs: _six_checks(FitMethod.RAW_SVI)
    )
    if failure_point == "evaluate_curve":
        original_evaluate = fit.evaluate_curve

        def fail_on_diagnostic_grid(curve: object, k: object) -> object:
            if np.asarray(k).size > expiry.node_count:
                raise RuntimeError("arrays")
            return original_evaluate(curve, k)

        monkeypatch.setattr(fit, "evaluate_curve", fail_on_diagnostic_grid)
    else:
        monkeypatch.setattr(
            fit,
            failure_point,
            lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("arrays")),
        )

    candidate = fit.fit_raw_svi_local(expiry, policy=FitPolicy())

    assert candidate is not None
    assert candidate.local_success is False
    assert candidate.parameters is not None
    assert candidate.curve is not None
    assert candidate.candidate_k == ()
    assert candidate.candidate_total_variance == ()
    assert candidate.candidate_iv == ()
    assert candidate.failure_code == "check_resolution_limit"
    assert candidate.failure_reason == "diagnostic candidate sampling failed"
    assert candidate.checks["positive_total_variance"].status is CheckStatus.INDETERMINATE
    assert candidate.optimizer_start_summary is not None
    assert candidate.optimizer_start_summary.selection_kind == "local_success"
    attempt = _materialize_failed_local_draft(candidate)
    assert attempt.local_success is False
    assert attempt.failure_code == "check_resolution_limit"
    with pytest.raises(ValueError, match="local_success|sampling|parameters"):
        dataclasses.replace(attempt, parameters=None)


@pytest.mark.parametrize("failure_point", ["diagnostic_curve_grid", "evaluate_curve"])
def test_ssvi_candidate_array_exception_becomes_materializable_child_failure(
    monkeypatch: pytest.MonkeyPatch,
    failure_point: str,
) -> None:
    expiries = _ssvi_stage_expiries()
    parameters = np.asarray([0.04, 0.06, -0.2, 0.3, 0.2], dtype=np.float64)
    monkeypatch.setattr(
        fit,
        "minimize",
        lambda *args, **kwargs: SimpleNamespace(
            success=True, x=parameters.copy(), fun=0.0, message="ok"
        ),
    )
    monkeypatch.setattr(
        fit, "_run_local_checks", lambda *args, **kwargs: _six_checks(FitMethod.SSVI)
    )
    if failure_point == "evaluate_curve":
        original_evaluate = fit.evaluate_curve

        def fail_on_diagnostic_grid(curve: object, k: object) -> object:
            if np.asarray(k).size > expiries[0].node_count:
                raise RuntimeError("arrays")
            return original_evaluate(curve, k)

        monkeypatch.setattr(fit, "evaluate_curve", fail_on_diagnostic_grid)
    else:
        monkeypatch.setattr(
            fit,
            failure_point,
            lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("arrays")),
        )

    bundle = fit.fit_ssvi_local(expiries, policy=FitPolicy())

    assert bundle.parent.local_success is True
    assert len(bundle.children) == 2
    for child in bundle.children:
        assert child.local_success is False
        assert child.parameters is not None
        assert child.curve is not None
        assert child.candidate_k == ()
        assert child.candidate_total_variance == ()
        assert child.candidate_iv == ()
        assert child.failure_code == "check_resolution_limit"
        assert child.failure_reason == "diagnostic candidate sampling failed"
        assert child.checks["positive_total_variance"].status is CheckStatus.INDETERMINATE
        assert child.optimizer_start_summary is None
        attempt = _materialize_failed_local_draft(child)
        assert attempt.local_success is False
        assert attempt.failure_code == "check_resolution_limit"


@pytest.mark.parametrize(
    ("method", "node_count"),
    [(FitMethod.PCHIP, 4), (FitMethod.LINEAR, 3)],
)
def test_nonparametric_candidate_array_exception_preserves_structural_butterfly_and_materializes(
    monkeypatch: pytest.MonkeyPatch,
    method: FitMethod,
    node_count: int,
) -> None:
    expiry = _local_expiry(
        str(node_count),
        0.25,
        np.linspace(-0.3, 0.3, node_count).tolist(),
        np.full(node_count, 0.04).tolist(),
    )
    monkeypatch.setattr(
        fit,
        "diagnostic_curve_grid",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("arrays")),
    )

    candidate = (
        fit.build_pchip_local_candidate(expiry, policy=FitPolicy())
        if method is FitMethod.PCHIP
        else fit.build_linear_local_candidate(expiry, policy=FitPolicy())
    )

    assert candidate is not None
    assert candidate.local_success is False
    assert candidate.curve is not None
    assert candidate.candidate_k == ()
    assert candidate.failure_code == "check_resolution_limit"
    assert candidate.failure_reason == "diagnostic candidate sampling failed"
    assert candidate.checks["positive_total_variance"].status is CheckStatus.INDETERMINATE
    butterfly = candidate.checks["butterfly_g_nonnegative"]
    assert butterfly.status is CheckStatus.NOT_APPLICABLE
    assert butterfly.reason_code == "method_has_no_analytic_g"
    attempt = _materialize_failed_local_draft(candidate)
    assert attempt.local_success is False
    assert attempt.failure_code == "check_resolution_limit"
````

</details>
