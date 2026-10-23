---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py>)

SHA-256：`52b8e3870395c1358c7549e12921a39806949d8b215481123957b02b605b3a22`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
"""Deterministic total-variance input preparation and fit selection.

The formal Agent reuses the timestamp fitting engine for its IV surface.  The
batch loaders, cache, plots, and artifact publishers remain diagnostic-only.
"""

from __future__ import annotations

import hashlib
import csv
import json
import math
import os
import re
import secrets
import shutil
import stat
import sys
import tempfile
import types
from collections import abc as collections_abc
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from itertools import combinations
from numbers import Real
from pathlib import Path
from typing import (
    Any,
    Callable,
    Literal,
    Mapping,
    Sequence,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from option_risk.config import PipelineConfig
from option_risk.io import (
    READ_COLUMNS,
    discover_parquet_files,
    partition_product,
    read_option_files,
)
from option_risk.quality import clean_and_profile
from option_risk.surfaces import build_surface_nodes

from option_risk.total_variance_fit import (
    CHECK_NAMES,
    SSVI_CHILD_FAILURE_CODES,
    AttemptScope,
    AttemptStatus,
    CalendarPairDiagnostic,
    CheckDiagnostic,
    CheckStatus,
    ExpiryFitResult,
    FinalMethod,
    ForwardSource,
    FitAttemptDiagnostic,
    FitMethod,
    FitPolicy,
    InputQuality,
    OptimizerStartSummary,
    OverallStatus,
    PerExpiryMetric,
    ResultStatus,
    SurfaceGridStatus,
    TimestampSurfaceDiagnostic,
    TimestampStatus,
    _LocalFitCandidate,
    _LocalExpiryInput,
    _LocalSsviBundle,
    _check_calendar_pair,
    _candidate_sampling_failure_checks,
    _fail_closed_local_checks,
    _failed_check_diagnostic,
    _indeterminate_check,
    _not_run_check,
    build_linear_local_candidate,
    build_pchip_local_candidate,
    evaluate_curve,
    fit_raw_svi_local,
    fit_ssvi_local,
    make_attempt_id,
    make_calendar_pair_id,
    to_json_compatible,
)


_REQUIRED_INPUT_COLUMNS = frozenset(
    {
        "product",
        "datetime",
        "dte",
        "time_to_expiry",
        "strike",
        "iv",
        "log_moneyness",
        "forward_price",
        "forward_source",
    }
)
_INPUT_FAILURE_CODES = (
    "invalid_strike",
    "invalid_forward",
    "invalid_iv",
    "invalid_time_to_expiry",
    "invalid_log_moneyness",
    "inconsistent_log_moneyness",
)


@dataclass(frozen=True, slots=True)
class EffectiveInputNode:
    """One canonical post-merge node used by the effective fingerprint."""

    maturity_id: str
    time_to_expiry: float
    merged_k: float
    total_variance: float
    duplicate_group_node_count: int
    forward_source: ForwardSource


@dataclass(frozen=True, slots=True)
class PreparedExpiryNodes:
    """Canonical merged nodes for one maturity and its local-fit input."""

    maturity_id: str
    time_to_expiry: float
    raw_node_count: int
    k: np.ndarray
    total_variance: np.ndarray
    implied_volatility: np.ndarray
    duplicate_group_node_count: tuple[int, ...]
    forward_source: ForwardSource
    local_input: _LocalExpiryInput = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        local_input = _LocalExpiryInput(
            maturity_id=self.maturity_id,
            time_to_expiry=self.time_to_expiry,
            raw_node_count=self.raw_node_count,
            k=self.k,
            total_variance=self.total_variance,
            implied_volatility=self.implied_volatility,
        )
        counts = tuple(self.duplicate_group_node_count)
        if len(counts) != local_input.node_count or any(
            isinstance(count, bool) or not isinstance(count, int) or count <= 0
            for count in counts
        ):
            raise ValueError("duplicate group counts must match merged nodes")
        if sum(counts) != self.raw_node_count:
            raise ValueError("duplicate group counts must reconcile raw nodes")
        if not isinstance(self.forward_source, ForwardSource):
            raise ValueError("forward_source must be ForwardSource")
        object.__setattr__(self, "k", local_input.k)
        object.__setattr__(self, "total_variance", local_input.total_variance)
        object.__setattr__(self, "implied_volatility", local_input.implied_volatility)
        object.__setattr__(self, "duplicate_group_node_count", counts)
        object.__setattr__(self, "local_input", local_input)

    @property
    def node_count(self) -> int:
        return self.local_input.node_count


@dataclass(frozen=True, slots=True)
class PreparedTimestampNodes:
    """Frozen result of the exact Task 4 timestamp input boundary."""

    product: str
    timestamp: str
    timestamp_status: TimestampStatus
    timestamp_failure_code: str | None
    timestamp_failure_reason: str | None
    forward_source: ForwardSource | None
    observed_forward_sources: tuple[ForwardSource, ...]
    input_quality: InputQuality
    expiries: tuple[PreparedExpiryNodes, ...]
    effective_nodes: tuple[EffectiveInputNode, ...]
    effective_input_fingerprint: str
    input_quality_fingerprint: str
    input_fingerprint: str


@dataclass(frozen=True, slots=True)
class _ValidInputRow:
    maturity_id: str
    time_to_expiry: float
    k: float
    total_variance: float
    implied_volatility: float
    forward_source: ForwardSource


@dataclass(frozen=True, slots=True)
class TimestampProfile:
    """Canonical sampling inputs for one observed surface-node timestamp."""

    timestamp: str
    timestamp_status: str
    input_fingerprint: str
    expiry_count: int
    node_total: int

    def __post_init__(self) -> None:
        timestamp = _canonical_timestamp(self.timestamp)
        status = (
            self.timestamp_status.value
            if isinstance(self.timestamp_status, TimestampStatus)
            else self.timestamp_status
        )
        if status not in {member.value for member in TimestampStatus}:
            raise ValueError("timestamp_status must be a closed TimestampStatus value")
        if re.fullmatch(r"sha256:[0-9a-f]{64}", self.input_fingerprint) is None:
            raise ValueError("input_fingerprint must be canonical sha256")
        for name, value in (
            ("expiry_count", self.expiry_count),
            ("node_total", self.node_total),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative int")
        object.__setattr__(self, "timestamp", timestamp)
        object.__setattr__(self, "timestamp_status", status)


@dataclass(frozen=True, slots=True)
class AgDiagnosticInput:
    """Read-only AG adapter result used by the Task 5 runner."""

    nodes: pd.DataFrame
    profiles: tuple[TimestampProfile, ...]
    source_fingerprint: str
    load_profile: tuple[dict[str, object], ...]


def _canonical_json_bytes(value: object) -> bytes:
    normalized = to_json_compatible(value)
    return (
        json.dumps(
            normalized,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _fingerprint(value: object) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _require_canonical_sha256(value: object, *, owner: str) -> str:
    if type(value) is not str or re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
        raise ValueError(f"{owner} must be canonical sha256")
    return value


def _require_nonnegative_json_int(
    value: object,
    *,
    owner: str,
    minimum: int = 0,
) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{owner} must be an exact integer >= {minimum}")
    return value


def _require_generated_at(value: object) -> str:
    if type(value) is not str or re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value
    ) is None:
        raise ValueError("generated_at must be UTC second-level RFC3339")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("generated_at must be a real UTC calendar timestamp") from exc
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("generated_at must round-trip as UTC second-level RFC3339")
    return value


def _canonical_product(product: object) -> str:
    if (
        not isinstance(product, str)
        or not product
        or product != product.lower()
        or re.fullmatch(r"[a-z0-9._-]+", product) is None
    ):
        raise ValueError("product must be a non-empty lowercase canonical value")
    return product


def _canonical_timestamp(value: object, *, owner: str = "timestamp") -> str:
    if value is None or isinstance(value, bool):
        raise ValueError(f"{owner} must be a local whole-second timestamp")
    try:
        timestamp = pd.Timestamp(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{owner} must be a local whole-second timestamp") from exc
    if pd.isna(timestamp):
        raise ValueError(f"{owner} must be a local whole-second timestamp")
    if timestamp.tzinfo is not None:
        raise ValueError(f"{owner} must not carry a timezone")
    if timestamp.microsecond != 0 or timestamp.nanosecond != 0:
        raise ValueError(f"{owner} must have whole-second precision")
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S")


def _is_null(value: object) -> bool:
    try:
        result = pd.isna(value)
    except (TypeError, ValueError):
        return False
    return bool(result) if isinstance(result, (bool, np.bool_)) else False


def _finite_float(value: object, *, positive: bool = False) -> float | None:
    if isinstance(value, bool) or not isinstance(value, Real):
        return None
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        return None
    return result


def _exact_maturity_id(value: object) -> str:
    number = _finite_float(value)
    if number is None or not number.is_integer():
        raise ValueError("dte schema requires a finite exact integer")
    return str(int(number))


def _source_token(value: object) -> ForwardSource:
    if isinstance(value, ForwardSource):
        return value
    if not isinstance(value, str):
        raise ValueError("forward_source schema token is outside the closed set")
    try:
        return ForwardSource(value)
    except ValueError as exc:
        raise ValueError(
            "forward_source schema token is outside the closed set"
        ) from exc


def _exp_is_finite(value: float) -> bool:
    try:
        return math.isfinite(math.exp(value))
    except OverflowError:
        return False


def _validate_call_schema(
    frame: pd.DataFrame,
    *,
    product: str,
    timestamp: str,
) -> tuple[tuple[str, ForwardSource], ...]:
    if not isinstance(frame, pd.DataFrame):
        raise ValueError("frame schema requires a pandas DataFrame")
    missing = sorted(_REQUIRED_INPUT_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError("frame schema is missing required columns: " + ",".join(missing))

    identities: list[tuple[str, ForwardSource]] = []
    for position, row in enumerate(frame.itertuples(index=False, name=None)):
        values = dict(zip(frame.columns, row, strict=True))
        row_product = values["product"]
        if not isinstance(row_product, str) or row_product != product:
            raise ValueError(f"row {position} product does not match explicit product")
        if _canonical_timestamp(values["datetime"], owner="row timestamp") != timestamp:
            raise ValueError(f"row {position} timestamp does not match explicit timestamp")
        maturity_id = _exact_maturity_id(values["dte"])
        source = _source_token(values["forward_source"])
        if source in {
            ForwardSource.UNDERLYING_PRICE_PROXY,
            ForwardSource.PRECOMPUTED_LOG_MONEYNESS_UNKNOWN,
        } and not _is_null(values["forward_price"]):
            raise ValueError(
                f"row {position} forward_source schema forbids forward_price"
            )
        identities.append((maturity_id, source))
    return tuple(identities)


def _input_quality_payload(quality: InputQuality) -> dict[str, object]:
    return {
        "input_row_count": quality.input_row_count,
        "valid_premerge_node_count": quality.valid_premerge_node_count,
        "merged_node_count": quality.merged_node_count,
        "excluded_counts": dict(quality.excluded_counts),
    }


def _effective_node_payload(node: EffectiveInputNode) -> dict[str, object]:
    return {
        "maturity_id": node.maturity_id,
        "time_to_expiry": node.time_to_expiry,
        "merged_k": node.merged_k,
        "total_variance": node.total_variance,
        "duplicate_group_node_count": node.duplicate_group_node_count,
        "forward_source": node.forward_source.value,
    }


def _build_fingerprints(
    *,
    product: str,
    timestamp: str,
    timestamp_status: TimestampStatus,
    timestamp_failure_code: str | None,
    observed_forward_sources: tuple[ForwardSource, ...],
    input_quality: InputQuality,
    effective_nodes: tuple[EffectiveInputNode, ...],
) -> tuple[str, str, str]:
    effective = _fingerprint(
        {
            "product": product,
            "timestamp": timestamp,
            "nodes": [_effective_node_payload(node) for node in effective_nodes],
        }
    )
    quality = _fingerprint(
        {
            "product": product,
            "timestamp": timestamp,
            "input_quality": _input_quality_payload(input_quality),
            "timestamp_status": timestamp_status.value,
            "timestamp_failure_code": timestamp_failure_code,
            "observed_forward_sources": [
                source.value for source in observed_forward_sources
            ],
        }
    )
    combined = _fingerprint(
        {
            "effective_input_fingerprint": effective,
            "input_quality_fingerprint": quality,
        }
    )
    return effective, quality, combined


def _schema_row_values(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        dict(zip(frame.columns, row, strict=True))
        for row in frame.itertuples(index=False, name=None)
    ]


def prepare_timestamp_nodes(
    frame: pd.DataFrame,
    *,
    product: str,
    timestamp: object,
    policy: FitPolicy,
) -> PreparedTimestampNodes:
    """Validate and canonically merge one timestamp without mutating ``frame``."""

    canonical_product = _canonical_product(product)
    canonical_timestamp = _canonical_timestamp(timestamp)
    if not isinstance(policy, FitPolicy):
        raise ValueError("policy must be FitPolicy")
    identities = _validate_call_schema(
        frame,
        product=canonical_product,
        timestamp=canonical_timestamp,
    )
    rows = _schema_row_values(frame)
    excluded_counts = {code: 0 for code in _INPUT_FAILURE_CODES}
    valid_rows: list[_ValidInputRow] = []

    for values, (maturity_id, source) in zip(rows, identities, strict=True):
        strike = _finite_float(values["strike"], positive=True)
        if strike is None:
            excluded_counts["invalid_strike"] += 1
            continue

        calculated_k: float | None = None
        if source is ForwardSource.TRUE_FUTURES_FORWARD:
            forward = _finite_float(values["forward_price"], positive=True)
            if forward is None:
                excluded_counts["invalid_forward"] += 1
                continue
            ratio = strike / forward
            calculated_k = (
                math.log(ratio)
                if math.isfinite(ratio) and ratio > 0.0
                else math.nan
            )

        implied_volatility = _finite_float(values["iv"], positive=True)
        if implied_volatility is None:
            excluded_counts["invalid_iv"] += 1
            continue
        time_to_expiry = _finite_float(values["time_to_expiry"], positive=True)
        if time_to_expiry is None:
            excluded_counts["invalid_time_to_expiry"] += 1
            continue

        input_k = (
            None
            if _is_null(values["log_moneyness"])
            else _finite_float(values["log_moneyness"])
        )
        if source is ForwardSource.TRUE_FUTURES_FORWARD:
            assert calculated_k is not None
            if not math.isfinite(calculated_k) or not _exp_is_finite(calculated_k):
                excluded_counts["invalid_log_moneyness"] += 1
                continue
            if not _is_null(values["log_moneyness"]):
                if input_k is None or not _exp_is_finite(input_k):
                    excluded_counts["invalid_log_moneyness"] += 1
                    continue
                if abs(input_k - calculated_k) > policy.k_consistency_tolerance:
                    excluded_counts["inconsistent_log_moneyness"] += 1
                    continue
            k = calculated_k
        else:
            if input_k is None or not _exp_is_finite(input_k):
                excluded_counts["invalid_log_moneyness"] += 1
                continue
            k = input_k

        total_variance = implied_volatility * implied_volatility * time_to_expiry
        if not math.isfinite(total_variance) or total_variance <= 0.0:
            excluded_counts["invalid_iv"] += 1
            continue
        valid_rows.append(
            _ValidInputRow(
                maturity_id=maturity_id,
                time_to_expiry=time_to_expiry,
                k=k,
                total_variance=total_variance,
                implied_volatility=implied_volatility,
                forward_source=source,
            )
        )

    observed_forward_sources = tuple(
        source
        for source in ForwardSource
        if any(row.forward_source is source for row in valid_rows)
    )
    if len(observed_forward_sources) > 1:
        input_quality = InputQuality(
            input_row_count=len(rows),
            valid_premerge_node_count=len(valid_rows),
            merged_node_count=0,
            excluded_counts=excluded_counts,
        )
        failure_reason = "mixed forward sources: " + ",".join(
            source.value for source in observed_forward_sources
        )
        fingerprints = _build_fingerprints(
            product=canonical_product,
            timestamp=canonical_timestamp,
            timestamp_status=TimestampStatus.FAILED_INPUT,
            timestamp_failure_code="mixed_forward_sources",
            observed_forward_sources=observed_forward_sources,
            input_quality=input_quality,
            effective_nodes=(),
        )
        return PreparedTimestampNodes(
            product=canonical_product,
            timestamp=canonical_timestamp,
            timestamp_status=TimestampStatus.FAILED_INPUT,
            timestamp_failure_code="mixed_forward_sources",
            timestamp_failure_reason=failure_reason,
            forward_source=None,
            observed_forward_sources=observed_forward_sources,
            input_quality=input_quality,
            expiries=(),
            effective_nodes=(),
            effective_input_fingerprint=fingerprints[0],
            input_quality_fingerprint=fingerprints[1],
            input_fingerprint=fingerprints[2],
        )

    maturity_to_times: dict[str, set[float]] = {}
    time_to_maturities: dict[float, set[str]] = {}
    for row in valid_rows:
        maturity_to_times.setdefault(row.maturity_id, set()).add(row.time_to_expiry)
        time_to_maturities.setdefault(row.time_to_expiry, set()).add(row.maturity_id)
    if any(len(times) != 1 for times in maturity_to_times.values()):
        raise ValueError("one maturity_id cannot map to multiple time_to_expiry values")
    if any(len(maturities) != 1 for maturities in time_to_maturities.values()):
        raise ValueError("different maturity_id values cannot share time_to_expiry")

    grouped: dict[tuple[str, float, float], list[float]] = {}
    for row in valid_rows:
        rounded = float(round(float(row.k), 10))
        merged_k = 0.0 if rounded == 0.0 else rounded
        grouped.setdefault(
            (row.maturity_id, row.time_to_expiry, merged_k), []
        ).append(row.total_variance)

    canonical_groups: list[tuple[str, float, float, float, int]] = []
    for (maturity_id, time_to_expiry, merged_k), values in grouped.items():
        total_variance = float(np.median(np.asarray(sorted(values), dtype=np.float64)))
        canonical_groups.append(
            (
                maturity_id,
                time_to_expiry,
                merged_k,
                total_variance,
                len(values),
            )
        )
    canonical_groups.sort(key=lambda item: (item[1], item[2], item[0]))

    forward_source = observed_forward_sources[0] if observed_forward_sources else None
    effective_nodes = tuple(
        EffectiveInputNode(
            maturity_id=maturity_id,
            time_to_expiry=time_to_expiry,
            merged_k=merged_k,
            total_variance=total_variance,
            duplicate_group_node_count=duplicate_count,
            forward_source=forward_source,
        )
        for (
            maturity_id,
            time_to_expiry,
            merged_k,
            total_variance,
            duplicate_count,
        ) in canonical_groups
        if forward_source is not None
    )

    expiry_groups: dict[tuple[str, float], list[EffectiveInputNode]] = {}
    for node in effective_nodes:
        expiry_groups.setdefault(
            (node.maturity_id, node.time_to_expiry), []
        ).append(node)
    expiries = tuple(
        PreparedExpiryNodes(
            maturity_id=maturity_id,
            time_to_expiry=time_to_expiry,
            raw_node_count=sum(node.duplicate_group_node_count for node in nodes),
            k=np.asarray([node.merged_k for node in nodes], dtype=np.float64),
            total_variance=np.asarray(
                [node.total_variance for node in nodes], dtype=np.float64
            ),
            implied_volatility=np.asarray(
                [
                    math.sqrt(node.total_variance / time_to_expiry)
                    for node in nodes
                ],
                dtype=np.float64,
            ),
            duplicate_group_node_count=tuple(
                node.duplicate_group_node_count for node in nodes
            ),
            forward_source=forward_source,
        )
        for (maturity_id, time_to_expiry), nodes in sorted(
            expiry_groups.items(), key=lambda item: (item[0][1], item[0][0])
        )
        if forward_source is not None
    )
    input_quality = InputQuality(
        input_row_count=len(rows),
        valid_premerge_node_count=len(valid_rows),
        merged_node_count=len(effective_nodes),
        excluded_counts=excluded_counts,
    )
    fingerprints = _build_fingerprints(
        product=canonical_product,
        timestamp=canonical_timestamp,
        timestamp_status=TimestampStatus.READY,
        timestamp_failure_code=None,
        observed_forward_sources=observed_forward_sources,
        input_quality=input_quality,
        effective_nodes=effective_nodes,
    )
    return PreparedTimestampNodes(
        product=canonical_product,
        timestamp=canonical_timestamp,
        timestamp_status=TimestampStatus.READY,
        timestamp_failure_code=None,
        timestamp_failure_reason=None,
        forward_source=forward_source,
        observed_forward_sources=observed_forward_sources,
        input_quality=input_quality,
        expiries=expiries,
        effective_nodes=effective_nodes,
        effective_input_fingerprint=fingerprints[0],
        input_quality_fingerprint=fingerprints[1],
        input_fingerprint=fingerprints[2],
    )


@dataclass(frozen=True, slots=True)
class _AttemptIdentity:
    attempt_id: str
    attempt_order: int
    scope: AttemptScope
    maturity_id: str | None
    participating_maturities: tuple[str, ...]
    time_to_expiry: float | None
    method: FitMethod
    parent_attempt_id: str | None


@dataclass(frozen=True, slots=True)
class _AttemptState:
    identity: _AttemptIdentity
    draft: _LocalFitCandidate
    attempt_status: AttemptStatus
    selection_eligible: bool
    blocked_by_parent: bool
    checks: Mapping[str, CheckDiagnostic]
    failure_code: str | None
    failure_reason: str | None


@dataclass(frozen=True, slots=True)
class _AcceptedExpiry:
    identity: _AttemptIdentity
    draft: _LocalFitCandidate
    expiry: PreparedExpiryNodes


def _all_not_run_checks() -> dict[str, CheckDiagnostic]:
    return {name: _not_run_check(name) for name in CHECK_NAMES}


def _no_prior_calendar_check() -> CheckDiagnostic:
    return CheckDiagnostic(
        name="calendar_consistent",
        status=CheckStatus.NOT_APPLICABLE,
        conclusion="not_applicable",
        reason_code="no_prior_maturity",
        primary_value=None,
        threshold=None,
        violation_count=None,
        grid_point_count=0,
        metrics={},
    )


def _no_overlap_calendar_check() -> CheckDiagnostic:
    return CheckDiagnostic(
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


def _aggregate_calendar_checks(
    pairs: tuple[CalendarPairDiagnostic, ...],
    *,
    no_prior: bool,
) -> CheckDiagnostic:
    if not pairs:
        return _no_prior_calendar_check() if no_prior else _not_run_check(
            "calendar_consistent"
        )
    for status in (
        CheckStatus.FAILED,
        CheckStatus.INDETERMINATE,
        CheckStatus.PASSED,
    ):
        match = next((pair.check for pair in pairs if pair.check.status is status), None)
        if match is not None:
            return match
    if all(pair.check.status is CheckStatus.NOT_TESTABLE for pair in pairs):
        return _no_overlap_calendar_check()
    raise ValueError("calendar pair statuses cannot be aggregated")


def _with_calendar_check(
    checks: Mapping[str, CheckDiagnostic],
    calendar: CheckDiagnostic,
) -> dict[str, CheckDiagnostic]:
    result = dict(checks)
    result["calendar_consistent"] = calendar
    return {name: result[name] for name in CHECK_NAMES}


def _not_run_parent_pair(
    *,
    pair_check_id: str,
    earlier_maturity_id: str,
    later_maturity_id: str,
    earlier_attempt_id: str | None,
    later_attempt_id: str | None,
    parent_attempt_id: str,
) -> CalendarPairDiagnostic:
    return CalendarPairDiagnostic(
        pair_check_id=pair_check_id,
        phase="ssvi_parent",
        earlier_maturity_id=earlier_maturity_id,
        later_maturity_id=later_maturity_id,
        earlier_attempt_id=earlier_attempt_id,
        later_attempt_id=later_attempt_id,
        parent_attempt_id=parent_attempt_id,
        common_k_min=None,
        common_k_max=None,
        check=_not_run_check("calendar_consistent"),
    )


def _safe_calendar_pair(
    *,
    pair_check_id: str,
    phase: Literal["ssvi_parent", "expiry_selection"],
    earlier_maturity_id: str,
    later_maturity_id: str,
    earlier_attempt_id: str | None,
    later_attempt_id: str | None,
    parent_attempt_id: str | None,
    earlier_curve: object,
    later_curve: object,
    earlier_raw_k: np.ndarray,
    later_raw_k: np.ndarray,
    policy: FitPolicy,
) -> CalendarPairDiagnostic:
    try:
        return _check_calendar_pair(
            pair_check_id=pair_check_id,
            phase=phase,
            earlier_maturity_id=earlier_maturity_id,
            later_maturity_id=later_maturity_id,
            earlier_attempt_id=earlier_attempt_id,
            later_attempt_id=later_attempt_id,
            parent_attempt_id=parent_attempt_id,
            earlier_curve=earlier_curve,
            later_curve=later_curve,
            earlier_raw_k=earlier_raw_k,
            later_raw_k=later_raw_k,
            policy=policy,
        )
    except Exception as exc:
        if earlier_curve is None or later_curve is None:
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
                check=_not_run_check("calendar_consistent"),
            )
        lo = max(float(earlier_curve.k_min), float(later_curve.k_min))
        hi = min(float(earlier_curve.k_max), float(later_curve.k_max))
        if lo >= hi:
            check = _no_overlap_calendar_check()
            common_k_min: float | None = None
            common_k_max: float | None = None
        else:
            check = _indeterminate_check(
                "calendar_consistent",
                primary_value=None,
                threshold=None,
                grid_point_count=0,
                metrics={"exception_type": type(exc).__name__},
            )
            common_k_min = lo
            common_k_max = hi
        return CalendarPairDiagnostic(
            pair_check_id=pair_check_id,
            phase=phase,
            earlier_maturity_id=earlier_maturity_id,
            later_maturity_id=later_maturity_id,
            earlier_attempt_id=earlier_attempt_id,
            later_attempt_id=later_attempt_id,
            parent_attempt_id=parent_attempt_id,
            common_k_min=common_k_min,
            common_k_max=common_k_max,
            check=check,
        )


def _per_expiry_not_run_metric(expiry: PreparedExpiryNodes) -> PerExpiryMetric:
    return PerExpiryMetric(
        maturity_id=expiry.maturity_id,
        time_to_expiry=expiry.time_to_expiry,
        raw_node_count=expiry.raw_node_count,
        node_count=expiry.node_count,
        k_min=float(expiry.k[0]),
        k_max=float(expiry.k[-1]),
        rmse_total_variance=None,
        nrmse_total_variance=None,
        rmse_iv=None,
        checks=_all_not_run_checks(),
    )


def _skipped_ssvi_parent(expiry: PreparedExpiryNodes) -> _LocalFitCandidate:
    checks = _all_not_run_checks()
    return _LocalFitCandidate(
        scope=AttemptScope.TIMESTAMP,
        maturity_id=None,
        participating_maturities=(expiry.maturity_id,),
        time_to_expiry=None,
        method=FitMethod.SSVI,
        optimizer_attempted=False,
        optimizer_success=None,
        optimizer_start_summary=None,
        local_success=False,
        parameters=None,
        per_expiry_metrics={
            expiry.maturity_id: _per_expiry_not_run_metric(expiry)
        },
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


def _ssvi_builder_exception_parent(
    expiries: tuple[PreparedExpiryNodes, ...],
    exc: Exception,
) -> _LocalFitCandidate:
    return _LocalFitCandidate(
        scope=AttemptScope.TIMESTAMP,
        maturity_id=None,
        participating_maturities=tuple(expiry.maturity_id for expiry in expiries),
        time_to_expiry=None,
        method=FitMethod.SSVI,
        optimizer_attempted=True,
        optimizer_success=False,
        optimizer_start_summary=OptimizerStartSummary(
            generated_count=0,
            precheck_discarded_count=0,
            duplicate_discarded_count=0,
            executed_count=0,
            optimizer_reported_success_count=0,
            evaluable_count=0,
            local_success_count=0,
            selected_start_index=None,
            selection_kind=None,
        ),
        local_success=False,
        parameters=None,
        per_expiry_metrics={
            expiry.maturity_id: _per_expiry_not_run_metric(expiry)
            for expiry in expiries
        },
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
        checks=_all_not_run_checks(),
        failure_code="optimizer_exception",
        failure_reason=f"SSVI builder exception: {type(exc).__name__}",
        curve=None,
    )


def _nonparametric_butterfly_check() -> CheckDiagnostic:
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


def _builder_exception_draft(
    expiry: PreparedExpiryNodes,
    method: FitMethod,
    exc: Exception,
) -> _LocalFitCandidate:
    if method is FitMethod.RAW_SVI:
        checks = _all_not_run_checks()
        optimizer_attempted = True
        optimizer_success: bool | None = False
        summary: OptimizerStartSummary | None = OptimizerStartSummary(
            generated_count=0,
            precheck_discarded_count=0,
            duplicate_discarded_count=0,
            executed_count=0,
            optimizer_reported_success_count=0,
            evaluable_count=0,
            local_success_count=0,
            selected_start_index=None,
            selection_kind=None,
        )
        failure_code = "optimizer_exception"
    else:
        checks = _all_not_run_checks()
        checks["positive_total_variance"] = _indeterminate_check(
            "positive_total_variance",
            primary_value=None,
            threshold=None,
            grid_point_count=0,
            metrics={"exception_type": type(exc).__name__},
        )
        checks["butterfly_g_nonnegative"] = _nonparametric_butterfly_check()
        optimizer_attempted = False
        optimizer_success = None
        summary = None
        failure_code = "check_resolution_limit"
    return _LocalFitCandidate(
        scope=AttemptScope.EXPIRY,
        maturity_id=expiry.maturity_id,
        participating_maturities=(),
        time_to_expiry=expiry.time_to_expiry,
        method=method,
        optimizer_attempted=optimizer_attempted,
        optimizer_success=optimizer_success,
        optimizer_start_summary=summary,
        local_success=False,
        parameters=None,
        per_expiry_metrics=None,
        rmse_total_variance=None,
        nrmse_total_variance=None,
        rmse_iv=None,
        raw_node_count=expiry.raw_node_count,
        node_count=expiry.node_count,
        k_min=float(expiry.k[0]),
        k_max=float(expiry.k[-1]),
        candidate_k=(),
        candidate_total_variance=(),
        candidate_iv=(),
        checks=checks,
        failure_code=failure_code,
        failure_reason=f"{method.value} builder exception: {type(exc).__name__}",
        curve=None,
    )


def _deep_plain_mapping(value: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        key: _deep_plain_mapping(item) if isinstance(item, Mapping) else item
        for key, item in value.items()
    }


def _materialize_attempt(
    state: _AttemptState,
    *,
    product: str,
    timestamp: str,
    policy: FitPolicy,
    forward_source: ForwardSource,
) -> FitAttemptDiagnostic:
    draft = state.draft
    identity = state.identity
    return FitAttemptDiagnostic(
        attempt_id=identity.attempt_id,
        parent_attempt_id=identity.parent_attempt_id,
        scope=identity.scope,
        product=product,
        timestamp=timestamp,
        maturity_id=identity.maturity_id,
        participating_maturities=list(identity.participating_maturities),
        time_to_expiry=identity.time_to_expiry,
        method=identity.method,
        attempt_order=identity.attempt_order,
        attempt_status=state.attempt_status,
        optimizer_attempted=draft.optimizer_attempted,
        optimizer_success=draft.optimizer_success,
        optimizer_start_summary=draft.optimizer_start_summary,
        selection_eligible=state.selection_eligible,
        blocked_by_parent=state.blocked_by_parent,
        local_success=draft.local_success,
        success=state.attempt_status is AttemptStatus.ACCEPTED,
        parameters=_deep_plain_mapping(draft.parameters),
        per_expiry_metrics=(
            None
            if draft.per_expiry_metrics is None
            else dict(draft.per_expiry_metrics)
        ),
        rmse_total_variance=draft.rmse_total_variance,
        nrmse_total_variance=draft.nrmse_total_variance,
        rmse_iv=draft.rmse_iv,
        raw_node_count=draft.raw_node_count,
        node_count=draft.node_count,
        k_min=draft.k_min,
        k_max=draft.k_max,
        candidate_k=list(draft.candidate_k),
        candidate_total_variance=list(draft.candidate_total_variance),
        candidate_iv=list(draft.candidate_iv),
        checks=dict(state.checks),
        failure_code=state.failure_code,
        failure_reason=state.failure_reason,
        policy_version=policy.policy_version,
        forward_source=forward_source,
    )


def _empty_method_counts() -> dict[FinalMethod, int]:
    return {method: 0 for method in FinalMethod}


def _failed_input_diagnostic(
    prepared: PreparedTimestampNodes,
    policy: FitPolicy,
) -> TimestampSurfaceDiagnostic:
    return TimestampSurfaceDiagnostic(
        product=prepared.product,
        timestamp=prepared.timestamp,
        diagnostic_only=True,
        timestamp_status=prepared.timestamp_status,
        timestamp_failure_code=prepared.timestamp_failure_code,
        timestamp_failure_reason=prepared.timestamp_failure_reason,
        forward_source=None,
        observed_forward_sources=list(prepared.observed_forward_sources),
        input_quality=prepared.input_quality,
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
        method_counts=_empty_method_counts(),
        overall_status=OverallStatus.NONE_USABLE,
        policy_version=policy.policy_version,
        effective_input_fingerprint=prepared.effective_input_fingerprint,
        input_quality_fingerprint=prepared.input_quality_fingerprint,
        input_fingerprint=prepared.input_fingerprint,
    )


def diagnose_timestamp(
    frame: pd.DataFrame,
    *,
    product: str,
    timestamp: object,
    policy: FitPolicy | None = None,
) -> TimestampSurfaceDiagnostic:
    """Run the deterministic two-phase calendar and lazy fallback state machine."""

    active_policy = FitPolicy() if policy is None else policy
    if not isinstance(active_policy, FitPolicy):
        raise ValueError("policy must be FitPolicy")
    prepared = prepare_timestamp_nodes(
        frame,
        product=product,
        timestamp=timestamp,
        policy=active_policy,
    )
    if prepared.timestamp_status is TimestampStatus.FAILED_INPUT:
        diagnostic = _failed_input_diagnostic(prepared, active_policy)
        validate_timestamp_diagnostic(diagnostic)
        return diagnostic

    identities: list[_AttemptIdentity] = []
    state_by_id: dict[str, _AttemptState] = {}
    draft_by_id: dict[str, _LocalFitCandidate] = {}
    histories: dict[str, list[_AttemptIdentity]] = {
        expiry.maturity_id: [] for expiry in prepared.expiries
    }
    pairs: list[CalendarPairDiagnostic] = []
    expiry_by_maturity = {
        expiry.maturity_id: expiry for expiry in prepared.expiries
    }

    def reserve(
        *,
        scope: AttemptScope,
        maturity_id: str | None,
        participating_maturities: tuple[str, ...],
        time_to_expiry: float | None,
        method: FitMethod,
        parent_attempt_id: str | None,
    ) -> _AttemptIdentity:
        order = len(identities)
        attempt_id = make_attempt_id(
            input_fingerprint=prepared.input_fingerprint,
            product=prepared.product,
            timestamp=prepared.timestamp,
            scope=scope,
            maturity_id=maturity_id,
            participating_maturities=participating_maturities,
            method=method,
            attempt_order=order,
            policy_version=active_policy.policy_version,
        )
        identity = _AttemptIdentity(
            attempt_id=attempt_id,
            attempt_order=order,
            scope=scope,
            maturity_id=maturity_id,
            participating_maturities=participating_maturities,
            time_to_expiry=time_to_expiry,
            method=method,
            parent_attempt_id=parent_attempt_id,
        )
        identities.append(identity)
        return identity

    eligible = tuple(
        expiry for expiry in prepared.expiries if expiry.node_count >= 4
    )
    parent_identity: _AttemptIdentity | None = None
    parent_draft: _LocalFitCandidate | None = None
    child_identity_by_maturity: dict[str, _AttemptIdentity] = {}
    child_draft_by_maturity: dict[str, _LocalFitCandidate] = {}

    if len(eligible) == 1:
        parent_draft = _skipped_ssvi_parent(eligible[0])
        parent_identity = reserve(
            scope=AttemptScope.TIMESTAMP,
            maturity_id=None,
            participating_maturities=parent_draft.participating_maturities,
            time_to_expiry=None,
            method=FitMethod.SSVI,
            parent_attempt_id=None,
        )
        draft_by_id[parent_identity.attempt_id] = parent_draft
    elif len(eligible) >= 2:
        try:
            bundle = fit_ssvi_local(
                tuple(expiry.local_input for expiry in eligible),
                policy=active_policy,
            )
            if not isinstance(bundle, _LocalSsviBundle):
                raise ValueError("SSVI builder returned an invalid bundle")
        except Exception as exc:
            parent_draft = _ssvi_builder_exception_parent(eligible, exc)
            bundle = _LocalSsviBundle(parent=parent_draft, children=())
        parent_draft = bundle.parent
        expected_maturities = tuple(expiry.maturity_id for expiry in eligible)
        if (
            parent_draft.scope is not AttemptScope.TIMESTAMP
            or parent_draft.method is not FitMethod.SSVI
            or parent_draft.participating_maturities != expected_maturities
        ):
            raise ValueError("SSVI parent draft identity does not match eligible expiries")
        parent_identity = reserve(
            scope=AttemptScope.TIMESTAMP,
            maturity_id=None,
            participating_maturities=expected_maturities,
            time_to_expiry=None,
            method=FitMethod.SSVI,
            parent_attempt_id=None,
        )
        draft_by_id[parent_identity.attempt_id] = parent_draft
        ordered_children = tuple(
            sorted(
                bundle.children,
                key=lambda child: (
                    expiry_by_maturity[child.maturity_id].time_to_expiry
                    if child.maturity_id in expiry_by_maturity
                    else math.inf,
                    child.maturity_id or "",
                ),
            )
        )
        if ordered_children and tuple(
            child.maturity_id for child in ordered_children
        ) != expected_maturities:
            raise ValueError("SSVI children must cover every participating maturity")
        for child in ordered_children:
            if (
                child.scope is not AttemptScope.EXPIRY
                or child.method is not FitMethod.SSVI
                or child.maturity_id is None
            ):
                raise ValueError("SSVI child draft has an invalid identity")
            expiry = expiry_by_maturity[child.maturity_id]
            identity = reserve(
                scope=AttemptScope.EXPIRY,
                maturity_id=child.maturity_id,
                participating_maturities=(),
                time_to_expiry=expiry.time_to_expiry,
                method=FitMethod.SSVI,
                parent_attempt_id=parent_identity.attempt_id,
            )
            child_identity_by_maturity[child.maturity_id] = identity
            child_draft_by_maturity[child.maturity_id] = child
            draft_by_id[identity.attempt_id] = child
            histories[child.maturity_id].append(identity)

    parent_accepted = False
    if parent_identity is not None and parent_draft is not None:
        if parent_draft.failure_code == "not_enough_maturities":
            parent_state = _AttemptState(
                identity=parent_identity,
                draft=parent_draft,
                attempt_status=AttemptStatus.SKIPPED,
                selection_eligible=False,
                blocked_by_parent=False,
                checks=dict(parent_draft.checks),
                failure_code=parent_draft.failure_code,
                failure_reason=parent_draft.failure_reason,
            )
        else:
            parent_pairs: list[CalendarPairDiagnostic] = []
            for earlier_maturity, later_maturity in combinations(
                parent_identity.participating_maturities, 2
            ):
                earlier_child = child_identity_by_maturity.get(earlier_maturity)
                later_child = child_identity_by_maturity.get(later_maturity)
                earlier_attempt_id = (
                    None if earlier_child is None else earlier_child.attempt_id
                )
                later_attempt_id = (
                    None if later_child is None else later_child.attempt_id
                )
                pair_check_id = make_calendar_pair_id(
                    input_fingerprint=prepared.input_fingerprint,
                    product=prepared.product,
                    timestamp=prepared.timestamp,
                    phase="ssvi_parent",
                    parent_attempt_id=parent_identity.attempt_id,
                    earlier_maturity_id=earlier_maturity,
                    later_maturity_id=later_maturity,
                    earlier_attempt_id=earlier_attempt_id,
                    later_attempt_id=later_attempt_id,
                    policy_version=active_policy.policy_version,
                )
                if (
                    not parent_draft.local_success
                    or earlier_child is None
                    or later_child is None
                ):
                    pair = _not_run_parent_pair(
                        pair_check_id=pair_check_id,
                        earlier_maturity_id=earlier_maturity,
                        later_maturity_id=later_maturity,
                        earlier_attempt_id=earlier_attempt_id,
                        later_attempt_id=later_attempt_id,
                        parent_attempt_id=parent_identity.attempt_id,
                    )
                else:
                    earlier_expiry = expiry_by_maturity[earlier_maturity]
                    later_expiry = expiry_by_maturity[later_maturity]
                    pair = _safe_calendar_pair(
                        pair_check_id=pair_check_id,
                        phase="ssvi_parent",
                        earlier_maturity_id=earlier_maturity,
                        later_maturity_id=later_maturity,
                        earlier_attempt_id=earlier_attempt_id,
                        later_attempt_id=later_attempt_id,
                        parent_attempt_id=parent_identity.attempt_id,
                        earlier_curve=child_draft_by_maturity[earlier_maturity].curve,
                        later_curve=child_draft_by_maturity[later_maturity].curve,
                        earlier_raw_k=earlier_expiry.k,
                        later_raw_k=later_expiry.k,
                        policy=active_policy,
                    )
                parent_pairs.append(pair)
                pairs.append(pair)
            if parent_draft.local_success:
                if not child_identity_by_maturity:
                    raise ValueError("locally successful SSVI parent requires children")
                calendar = _aggregate_calendar_checks(
                    tuple(parent_pairs), no_prior=False
                )
                parent_checks = _with_calendar_check(parent_draft.checks, calendar)
                if calendar.status is CheckStatus.FAILED:
                    parent_status = AttemptStatus.FAILED
                    parent_failure_code = "calendar_conflict"
                    parent_failure_reason = "SSVI parent calendar conflict"
                elif calendar.status is CheckStatus.INDETERMINATE:
                    parent_status = AttemptStatus.FAILED
                    parent_failure_code = "check_resolution_limit"
                    parent_failure_reason = "SSVI parent calendar check indeterminate"
                else:
                    parent_status = AttemptStatus.ACCEPTED
                    parent_failure_code = None
                    parent_failure_reason = None
                    parent_accepted = True
            else:
                parent_checks = dict(parent_draft.checks)
                parent_status = AttemptStatus.FAILED
                parent_failure_code = parent_draft.failure_code
                parent_failure_reason = parent_draft.failure_reason
            parent_state = _AttemptState(
                identity=parent_identity,
                draft=parent_draft,
                attempt_status=parent_status,
                selection_eligible=False,
                blocked_by_parent=False,
                checks=parent_checks,
                failure_code=parent_failure_code,
                failure_reason=parent_failure_reason,
            )
        state_by_id[parent_identity.attempt_id] = parent_state

        for maturity_id, child_identity in child_identity_by_maturity.items():
            if parent_accepted:
                continue
            child = child_draft_by_maturity[maturity_id]
            child_failure_code = (
                "parent_ssvi_rejected" if child.local_success else child.failure_code
            )
            child_failure_reason = (
                "SSVI parent rejected"
                if child.local_success
                else child.failure_reason
            )
            state_by_id[child_identity.attempt_id] = _AttemptState(
                identity=child_identity,
                draft=child,
                attempt_status=AttemptStatus.FAILED,
                selection_eligible=False,
                blocked_by_parent=True,
                checks=dict(child.checks),
                failure_code=child_failure_code,
                failure_reason=child_failure_reason,
            )

    accepted_earlier: list[_AcceptedExpiry] = []

    def process_candidate(
        identity: _AttemptIdentity,
        draft: _LocalFitCandidate,
        expiry: PreparedExpiryNodes,
    ) -> bool:
        if not draft.local_success:
            if draft.failure_code is None:
                raise ValueError("locally failed draft requires a failure code")
            state_by_id[identity.attempt_id] = _AttemptState(
                identity=identity,
                draft=draft,
                attempt_status=AttemptStatus.FAILED,
                selection_eligible=True,
                blocked_by_parent=False,
                checks=dict(draft.checks),
                failure_code=draft.failure_code,
                failure_reason=draft.failure_reason,
            )
            return False

        candidate_pairs: list[CalendarPairDiagnostic] = []
        for earlier in accepted_earlier:
            pair_check_id = make_calendar_pair_id(
                input_fingerprint=prepared.input_fingerprint,
                product=prepared.product,
                timestamp=prepared.timestamp,
                phase="expiry_selection",
                parent_attempt_id=None,
                earlier_maturity_id=earlier.expiry.maturity_id,
                later_maturity_id=expiry.maturity_id,
                earlier_attempt_id=earlier.identity.attempt_id,
                later_attempt_id=identity.attempt_id,
                policy_version=active_policy.policy_version,
            )
            pair = _safe_calendar_pair(
                pair_check_id=pair_check_id,
                phase="expiry_selection",
                earlier_maturity_id=earlier.expiry.maturity_id,
                later_maturity_id=expiry.maturity_id,
                earlier_attempt_id=earlier.identity.attempt_id,
                later_attempt_id=identity.attempt_id,
                parent_attempt_id=None,
                earlier_curve=earlier.draft.curve,
                later_curve=draft.curve,
                earlier_raw_k=earlier.expiry.k,
                later_raw_k=expiry.k,
                policy=active_policy,
            )
            candidate_pairs.append(pair)
            pairs.append(pair)
        calendar = _aggregate_calendar_checks(
            tuple(candidate_pairs), no_prior=not accepted_earlier
        )
        checks = _with_calendar_check(draft.checks, calendar)
        if calendar.status is CheckStatus.FAILED:
            status = AttemptStatus.FAILED
            failure_code = "calendar_conflict"
            failure_reason = "expiry calendar conflict"
        elif calendar.status is CheckStatus.INDETERMINATE:
            status = AttemptStatus.FAILED
            failure_code = "check_resolution_limit"
            failure_reason = "expiry calendar check indeterminate"
        else:
            status = AttemptStatus.ACCEPTED
            failure_code = None
            failure_reason = None
        state_by_id[identity.attempt_id] = _AttemptState(
            identity=identity,
            draft=draft,
            attempt_status=status,
            selection_eligible=True,
            blocked_by_parent=False,
            checks=checks,
            failure_code=failure_code,
            failure_reason=failure_reason,
        )
        if status is AttemptStatus.ACCEPTED:
            accepted_earlier.append(
                _AcceptedExpiry(identity=identity, draft=draft, expiry=expiry)
            )
            return True
        return False

    def build_fallback(
        expiry: PreparedExpiryNodes,
        method: FitMethod,
    ) -> tuple[_AttemptIdentity, _LocalFitCandidate]:
        identity = reserve(
            scope=AttemptScope.EXPIRY,
            maturity_id=expiry.maturity_id,
            participating_maturities=(),
            time_to_expiry=expiry.time_to_expiry,
            method=method,
            parent_attempt_id=None,
        )
        histories[expiry.maturity_id].append(identity)
        try:
            if method is FitMethod.RAW_SVI:
                candidate = fit_raw_svi_local(
                    expiry.local_input, policy=active_policy
                )
            elif method is FitMethod.PCHIP:
                candidate = build_pchip_local_candidate(
                    expiry.local_input, policy=active_policy
                )
            elif method is FitMethod.LINEAR:
                candidate = build_linear_local_candidate(
                    expiry.local_input, policy=active_policy
                )
            else:
                raise ValueError("SSVI children are supplied only by the parent bundle")
            if candidate is None:
                raise ValueError("eligible fallback builder returned no candidate")
            if (
                not isinstance(candidate, _LocalFitCandidate)
                or candidate.scope is not AttemptScope.EXPIRY
                or candidate.maturity_id != expiry.maturity_id
                or candidate.method is not method
            ):
                raise ValueError("fallback builder returned an invalid draft")
        except Exception as exc:
            candidate = _builder_exception_draft(expiry, method, exc)
        draft_by_id[identity.attempt_id] = candidate
        return identity, candidate

    for expiry in prepared.expiries:
        if expiry.node_count < 2:
            continue
        accepted = False
        child_identity = child_identity_by_maturity.get(expiry.maturity_id)
        if parent_accepted and child_identity is not None:
            child = child_draft_by_maturity[expiry.maturity_id]
            accepted = process_candidate(child_identity, child, expiry)
        if accepted:
            continue
        fallback_methods = (
            (FitMethod.RAW_SVI, FitMethod.PCHIP)
            if expiry.node_count >= 5
            else (FitMethod.PCHIP,)
            if expiry.node_count == 4
            else (FitMethod.LINEAR,)
        )
        for method in fallback_methods:
            identity, candidate = build_fallback(expiry, method)
            if process_candidate(identity, candidate, expiry):
                break

    if len(state_by_id) != len(identities):
        missing = [
            identity.attempt_id
            for identity in identities
            if identity.attempt_id not in state_by_id
        ]
        raise ValueError("attempt identities were not finalized: " + ",".join(missing))
    if identities and prepared.forward_source is None:
        raise ValueError("fit attempts require one canonical forward source")
    attempts = [
        _materialize_attempt(
            state_by_id[identity.attempt_id],
            product=prepared.product,
            timestamp=prepared.timestamp,
            policy=active_policy,
            forward_source=prepared.forward_source,
        )
        for identity in identities
    ]
    attempt_by_id = {attempt.attempt_id: attempt for attempt in attempts}

    expiry_results: list[ExpiryFitResult] = []
    for expiry in prepared.expiries:
        history = histories[expiry.maturity_id]
        history_attempts = [attempt_by_id[item.attempt_id] for item in history]
        selectable = [attempt for attempt in history_attempts if attempt.selection_eligible]
        terminal = selectable[-1] if selectable else None
        selected = (
            terminal
            if terminal is not None
            and terminal.attempt_status is AttemptStatus.ACCEPTED
            else None
        )
        candidate_attempts = [attempt for attempt in history_attempts if attempt.candidate_k]
        last_candidate = candidate_attempts[-1] if candidate_attempts else None
        if selected is not None:
            result = ExpiryFitResult(
                maturity_id=expiry.maturity_id,
                time_to_expiry=expiry.time_to_expiry,
                result_status=ResultStatus.USABLE,
                method=FinalMethod(selected.method.value),
                success=True,
                usable=True,
                raw_k=[float(value) for value in expiry.k],
                raw_total_variance=[
                    float(value) for value in expiry.total_variance
                ],
                raw_iv=[float(value) for value in expiry.implied_volatility],
                fit_k=list(selected.candidate_k),
                fit_total_variance=[
                    float(value)
                    for value in selected.candidate_total_variance
                    if value is not None
                ],
                fit_iv=[
                    float(value) for value in selected.candidate_iv if value is not None
                ],
                selected_attempt_id=selected.attempt_id,
                last_candidate_attempt_id=(
                    None if last_candidate is None else last_candidate.attempt_id
                ),
                terminal_attempt_id=selected.attempt_id,
                attempt_ids=[attempt.attempt_id for attempt in history_attempts],
                final_checks=dict(selected.checks),
                failure_code=None,
                failure_reason=None,
            )
        elif terminal is not None:
            result = ExpiryFitResult(
                maturity_id=expiry.maturity_id,
                time_to_expiry=expiry.time_to_expiry,
                result_status=ResultStatus.UNUSABLE,
                method=FinalMethod.UNUSABLE,
                success=False,
                usable=False,
                raw_k=[float(value) for value in expiry.k],
                raw_total_variance=[
                    float(value) for value in expiry.total_variance
                ],
                raw_iv=[float(value) for value in expiry.implied_volatility],
                fit_k=[],
                fit_total_variance=[],
                fit_iv=[],
                selected_attempt_id=None,
                last_candidate_attempt_id=(
                    None if last_candidate is None else last_candidate.attempt_id
                ),
                terminal_attempt_id=terminal.attempt_id,
                attempt_ids=[attempt.attempt_id for attempt in history_attempts],
                final_checks=dict(terminal.checks),
                failure_code=terminal.failure_code,
                failure_reason=terminal.failure_reason,
            )
        else:
            result = ExpiryFitResult(
                maturity_id=expiry.maturity_id,
                time_to_expiry=expiry.time_to_expiry,
                result_status=ResultStatus.UNUSABLE,
                method=FinalMethod.UNUSABLE,
                success=False,
                usable=False,
                raw_k=[float(value) for value in expiry.k],
                raw_total_variance=[
                    float(value) for value in expiry.total_variance
                ],
                raw_iv=[float(value) for value in expiry.implied_volatility],
                fit_k=[],
                fit_total_variance=[],
                fit_iv=[],
                selected_attempt_id=None,
                last_candidate_attempt_id=None,
                terminal_attempt_id=None,
                attempt_ids=[],
                final_checks=_all_not_run_checks(),
                failure_code="insufficient_nodes",
                failure_reason="fewer than two distinct merged k nodes",
            )
        expiry_results.append(result)

    supported_expiries = [
        expiry for expiry in prepared.expiries if expiry.node_count >= 2
    ]
    if supported_expiries:
        surface_k = [
            float(value)
            for value in np.linspace(
                min(float(expiry.k[0]) for expiry in supported_expiries),
                max(float(expiry.k[-1]) for expiry in supported_expiries),
                active_policy.surface_grid_size,
                endpoint=True,
                dtype=np.float64,
            )
        ]
        surface_status = SurfaceGridStatus.AVAILABLE
    else:
        surface_k = []
        surface_status = SurfaceGridStatus.UNAVAILABLE_NO_SUPPORT
    surface_w: list[list[float | None]] = []
    surface_iv: list[list[float | None]] = []
    for result in expiry_results:
        if not surface_k:
            surface_w.append([])
            surface_iv.append([])
            continue
        if not result.usable:
            surface_w.append([None] * len(surface_k))
            surface_iv.append([None] * len(surface_k))
            continue
        assert result.selected_attempt_id is not None
        selected_draft = draft_by_id[result.selected_attempt_id]
        if selected_draft.curve is None:
            raise ValueError("accepted attempt requires an evaluable curve")
        evaluated = evaluate_curve(selected_draft.curve, surface_k)
        w_row = [
            None if value is None else float(value)
            for value in evaluated.total_variance
        ]
        iv_row = [None if value is None else float(value) for value in evaluated.iv]
        surface_w.append(w_row)
        surface_iv.append(iv_row)

    attempt_order_by_id = {
        identity.attempt_id: identity.attempt_order for identity in identities
    }
    maturity_time = {
        expiry.maturity_id: expiry.time_to_expiry for expiry in prepared.expiries
    }
    pairs.sort(
        key=lambda pair: (
            0 if pair.phase == "ssvi_parent" else 1,
            maturity_time[pair.later_maturity_id],
            maturity_time[pair.earlier_maturity_id],
            pair.parent_attempt_id or "",
            attempt_order_by_id.get(pair.later_attempt_id, -1),
            pair.later_attempt_id or "",
            pair.earlier_attempt_id or "",
            pair.pair_check_id,
        )
    )
    method_counts = {
        method: sum(result.method is method for result in expiry_results)
        for method in FinalMethod
    }
    usable_count = sum(result.usable for result in expiry_results)
    unusable_count = len(expiry_results) - usable_count
    overall = (
        OverallStatus.NONE_USABLE
        if usable_count == 0
        else OverallStatus.ALL_USABLE
        if usable_count == len(expiry_results)
        else OverallStatus.PARTIALLY_USABLE
    )
    diagnostic = TimestampSurfaceDiagnostic(
        product=prepared.product,
        timestamp=prepared.timestamp,
        diagnostic_only=True,
        timestamp_status=TimestampStatus.READY,
        timestamp_failure_code=None,
        timestamp_failure_reason=None,
        forward_source=prepared.forward_source,
        observed_forward_sources=list(prepared.observed_forward_sources),
        input_quality=prepared.input_quality,
        ssvi_attempt=(
            None if parent_identity is None else parent_identity.attempt_id
        ),
        attempts=attempts,
        expiry_results=expiry_results,
        surface_grid_status=surface_status,
        surface_log_moneyness=surface_k,
        surface_time_to_expiry=[
            result.time_to_expiry for result in expiry_results
        ],
        surface_total_variance=surface_w,
        surface_iv=surface_iv,
        usable_expiry_count=usable_count,
        unusable_expiry_count=unusable_count,
        calendar_pair_checks=pairs,
        method_counts=method_counts,
        overall_status=overall,
        policy_version=active_policy.policy_version,
        effective_input_fingerprint=prepared.effective_input_fingerprint,
        input_quality_fingerprint=prepared.input_quality_fingerprint,
        input_fingerprint=prepared.input_fingerprint,
    )
    validate_timestamp_diagnostic(diagnostic)
    return diagnostic


def _pair_key(pair: CalendarPairDiagnostic) -> tuple[object, ...]:
    return (
        pair.phase,
        pair.parent_attempt_id,
        pair.earlier_maturity_id,
        pair.later_maturity_id,
        pair.earlier_attempt_id,
        pair.later_attempt_id,
    )


def validate_timestamp_diagnostic(
    diagnostic: TimestampSurfaceDiagnostic,
) -> None:
    """Strictly replay all references, pair universes, ordering, and masks."""

    if not isinstance(diagnostic, TimestampSurfaceDiagnostic):
        raise ValueError("diagnostic must be TimestampSurfaceDiagnostic")
    if diagnostic.timestamp_status is TimestampStatus.FAILED_INPUT:
        if diagnostic.calendar_pair_checks or diagnostic.attempts:
            raise ValueError("failed-input diagnostic cannot contain attempt or calendar state")
        return

    attempt_by_id = {
        attempt.attempt_id: attempt for attempt in diagnostic.attempts
    }
    result_by_maturity = {
        result.maturity_id: result for result in diagnostic.expiry_results
    }
    if len(result_by_maturity) != len(diagnostic.expiry_results):
        raise ValueError("expiry result maturity ids must be unique")
    maturity_time = {
        result.maturity_id: result.time_to_expiry
        for result in diagnostic.expiry_results
    }
    if diagnostic.input_quality.merged_node_count != sum(
        len(result.raw_k) for result in diagnostic.expiry_results
    ):
        raise ValueError("input quality merged node count does not match expiry results")
    for attempt in diagnostic.attempts:
        if attempt.forward_source is not diagnostic.forward_source:
            raise ValueError("attempt forward_source does not match its timestamp")

    raw_counts_by_maturity: dict[str, set[int]] = {
        maturity_id: set() for maturity_id in result_by_maturity
    }
    for result in diagnostic.expiry_results:
        expected_node_count = len(result.raw_k)
        expected_support = (
            (result.raw_k[0], result.raw_k[-1])
            if expected_node_count >= 2
            else (None, None)
        )
        expiry_attempts = [
            attempt
            for attempt in diagnostic.attempts
            if attempt.scope is AttemptScope.EXPIRY
            and attempt.maturity_id == result.maturity_id
        ]
        for attempt in expiry_attempts:
            if attempt.node_count != expected_node_count:
                raise ValueError("attempt node_count does not match its expiry nodes")
            if (attempt.k_min, attempt.k_max) != expected_support:
                raise ValueError("attempt k support does not match its expiry nodes")
            if attempt.raw_node_count is None:
                raise ValueError("expiry attempt raw_node_count cannot be null")
            raw_counts_by_maturity[result.maturity_id].add(attempt.raw_node_count)

    parents = [
        attempt
        for attempt in diagnostic.attempts
        if attempt.scope is AttemptScope.TIMESTAMP
    ]
    for parent in parents:
        assert parent.per_expiry_metrics is not None
        if set(parent.per_expiry_metrics) != set(parent.participating_maturities):
            raise ValueError(
                "SSVI metric keys must equal the parent participating maturities"
            )
        child_attempts = [
            attempt
            for attempt in diagnostic.attempts
            if attempt.parent_attempt_id == parent.attempt_id
        ]
        if parent.attempt_status is not AttemptStatus.SKIPPED:
            if parent.optimizer_start_summary is None:
                raise ValueError("active SSVI parent requires an optimizer summary")
            has_parent_evaluable_payload = bool(child_attempts) or any(
                value is not None
                for metric in parent.per_expiry_metrics.values()
                for value in (
                    metric.rmse_total_variance,
                    metric.nrmse_total_variance,
                    metric.rmse_iv,
                )
            ) or any(
                check.status is not CheckStatus.NOT_APPLICABLE
                or check.reason_code != "not_run"
                for metric in parent.per_expiry_metrics.values()
                for name, check in metric.checks.items()
                if name != "calendar_consistent"
            )
            if (parent.optimizer_start_summary.evaluable_count > 0) != (
                has_parent_evaluable_payload
            ):
                raise ValueError(
                    "SSVI parent evaluable starts must match retained local payload"
                )
        child_by_maturity = {
            attempt.maturity_id: attempt for attempt in child_attempts
        }
        if len(child_by_maturity) != len(child_attempts):
            raise ValueError("SSVI parent has duplicate child maturities")
        parent_evaluable = (
            parent.optimizer_start_summary is not None
            and parent.optimizer_start_summary.evaluable_count > 0
        )
        if parent_evaluable:
            if set(child_by_maturity) != set(parent.participating_maturities):
                raise ValueError(
                    "evaluable SSVI parent requires every participating child"
                )
        elif child_attempts:
            raise ValueError("non-evaluable SSVI parent cannot retain children")
        for child in child_attempts:
            if (
                child.failure_code is not None
                and child.failure_code not in SSVI_CHILD_FAILURE_CODES
            ):
                raise ValueError(
                    "SSVI child failure code is outside its closed expiry set"
                )
        if parent.parameters is None:
            if child_attempts:
                raise ValueError("SSVI children require parent representative parameters")
        else:
            theta_by_maturity = parent.parameters["theta_by_maturity"]
            if not isinstance(theta_by_maturity, Mapping) or set(
                theta_by_maturity
            ) != set(parent.participating_maturities):
                raise ValueError(
                    "SSVI parent theta keys must equal participating maturities"
                )
            for child in child_attempts:
                if child.maturity_id not in theta_by_maturity:
                    raise ValueError("SSVI child maturity has no parent theta parameter")
                expected_child_parameters = {
                    "rho": parent.parameters["rho"],
                    "eta": parent.parameters["eta"],
                    "gamma": parent.parameters["gamma"],
                    "theta": theta_by_maturity[child.maturity_id],
                }
                if child.parameters != expected_child_parameters:
                    raise ValueError(
                        "SSVI child parameters do not match its parent representative"
                    )
        canonical_incomplete_checks = _fail_closed_local_checks()
        marker_hole_checks = {
            name: _not_run_check(name) for name in CHECK_NAMES
        }
        marker_hole_checks["positive_total_variance"] = _indeterminate_check(
            "positive_total_variance",
            primary_value=None,
            threshold=None,
            grid_point_count=0,
            metrics={},
        )
        parent_has_incomplete_metrics_stage = parent_evaluable and any(
            all(
                value is None
                for value in (
                    metric.rmse_total_variance,
                    metric.nrmse_total_variance,
                    metric.rmse_iv,
                )
            )
            for metric in parent.per_expiry_metrics.values()
        )
        parent_incomplete_occurrences = tuple(
            (name, check.metrics["incomplete_stage"])
            for name, check in parent.checks.items()
            if "incomplete_stage" in check.metrics
        )
        parent_has_exact_incomplete_marker = (
            len(parent_incomplete_occurrences) == 1
            and parent_incomplete_occurrences[0][0]
            == "positive_total_variance"
            and type(parent_incomplete_occurrences[0][1]) is bool
            and parent_incomplete_occurrences[0][1] is True
        )
        for maturity_id in parent.participating_maturities:
            metric = parent.per_expiry_metrics[maturity_id]
            result = result_by_maturity.get(maturity_id)
            if result is None:
                raise ValueError("SSVI metric references an unknown maturity")
            if (
                metric.maturity_id != maturity_id
                or metric.time_to_expiry != result.time_to_expiry
                or metric.node_count != len(result.raw_k)
                or (metric.k_min, metric.k_max)
                != (result.raw_k[0], result.raw_k[-1])
            ):
                raise ValueError("SSVI metric node or support facts do not match its expiry")
            metric_calendar = metric.checks["calendar_consistent"]
            if not (
                metric_calendar.status is CheckStatus.NOT_APPLICABLE
                and metric_calendar.reason_code == "not_run"
            ):
                raise ValueError("SSVI metric calendar check must retain draft not_run state")
            child = child_by_maturity.get(maturity_id)
            metric_incomplete_occurrences = tuple(
                (name, check.metrics["incomplete_stage"])
                for name, check in metric.checks.items()
                if "incomplete_stage" in check.metrics
            )
            child_incomplete_occurrences = (
                ()
                if child is None
                else tuple(
                    (name, check.metrics["incomplete_stage"])
                    for name, check in child.checks.items()
                    if "incomplete_stage" in check.metrics
                )
            )
            metric_has_exact_incomplete_marker = (
                len(metric_incomplete_occurrences) == 1
                and metric_incomplete_occurrences[0][0]
                == "positive_total_variance"
                and type(metric_incomplete_occurrences[0][1]) is bool
                and metric_incomplete_occurrences[0][1] is True
            )
            child_has_exact_incomplete_marker = (
                len(child_incomplete_occurrences) == 1
                and child_incomplete_occurrences[0][0]
                == "positive_total_variance"
                and type(child_incomplete_occurrences[0][1]) is bool
                and child_incomplete_occurrences[0][1] is True
            )
            metric_has_marker_hole = metric.checks == marker_hole_checks
            child_has_marker_hole = (
                child is not None and child.checks == marker_hole_checks
            )
            if (
                parent_has_incomplete_metrics_stage
                or bool(metric_incomplete_occurrences)
                or bool(child_incomplete_occurrences)
                or metric_has_marker_hole
                or child_has_marker_hole
            ):
                if (
                    child is None
                    or not metric_has_exact_incomplete_marker
                    or not child_has_exact_incomplete_marker
                    or (
                        bool(parent_incomplete_occurrences)
                        and not parent_has_exact_incomplete_marker
                    )
                    or metric.checks != canonical_incomplete_checks
                    or child.checks != canonical_incomplete_checks
                ):
                    raise ValueError(
                        "SSVI incomplete-stage metric local checks and child draft "
                        "checks must be canonical fail-closed"
                    )
            if child is not None:
                if (
                    metric.rmse_total_variance,
                    metric.nrmse_total_variance,
                    metric.rmse_iv,
                ) != (
                    child.rmse_total_variance,
                    child.nrmse_total_variance,
                    child.rmse_iv,
                ):
                    raise ValueError("SSVI metric RMSE facts do not match its child draft")
                sampling_failure = (
                    child.failure_code == "check_resolution_limit"
                    and child.failure_reason == "diagnostic candidate sampling failed"
                    and not child.candidate_k
                    and not child.candidate_total_variance
                    and not child.candidate_iv
                    and child.checks
                    == _candidate_sampling_failure_checks(FitMethod.SSVI)
                )
                if not sampling_failure and any(
                    metric.checks[name] != child.checks[name]
                    for name in CHECK_NAMES
                    if name != "calendar_consistent"
                ):
                    raise ValueError("SSVI metric local checks do not match its child draft")
            if parent.attempt_status is AttemptStatus.SKIPPED and (
                any(
                    value is not None
                    for value in (
                        metric.rmse_total_variance,
                        metric.nrmse_total_variance,
                        metric.rmse_iv,
                    )
                )
                or any(
                    check.status is not CheckStatus.NOT_APPLICABLE
                    or check.reason_code != "not_run"
                    for check in metric.checks.values()
                )
            ):
                raise ValueError("skipped SSVI metric must retain null RMSE and not_run checks")
            raw_counts_by_maturity[maturity_id].add(metric.raw_node_count)
        parent_local_blocked = False
        for name in (
            "positive_total_variance",
            "call_price_monotonic",
            "call_price_convex",
            "butterfly_g_nonnegative",
            "jump_reliable",
        ):
            if parent_local_blocked:
                expected_parent_check = _not_run_check(name)
            else:
                candidates = [
                    parent.per_expiry_metrics[maturity_id].checks[name]
                    for maturity_id in parent.participating_maturities
                ]
                expected_parent_check = next(
                    (
                        check
                        for check in candidates
                        if check.status is CheckStatus.FAILED
                    ),
                    None,
                )
                if expected_parent_check is None:
                    expected_parent_check = next(
                        (
                            check
                            for check in candidates
                            if check.status is CheckStatus.INDETERMINATE
                        ),
                        candidates[0],
                    )
                if expected_parent_check.status in {
                    CheckStatus.FAILED,
                    CheckStatus.INDETERMINATE,
                }:
                    parent_local_blocked = True
            if parent.checks[name] != expected_parent_check:
                raise ValueError(
                    "SSVI parent local check does not aggregate its per-expiry metrics"
                )
    for maturity_id, raw_counts in raw_counts_by_maturity.items():
        if len(raw_counts) > 1:
            raise ValueError("raw_node_count is inconsistent within one expiry")
        if raw_counts and next(iter(raw_counts)) < len(result_by_maturity[maturity_id].raw_k):
            raise ValueError("raw_node_count cannot be smaller than merged node_count")
    known_raw_count = sum(
        next(iter(raw_counts))
        for raw_counts in raw_counts_by_maturity.values()
        if raw_counts
    )
    unknown_maturities = [
        maturity_id
        for maturity_id, raw_counts in raw_counts_by_maturity.items()
        if not raw_counts
    ]
    minimum_unknown_raw_count = sum(
        len(result_by_maturity[maturity_id].raw_k)
        for maturity_id in unknown_maturities
    )
    if diagnostic.input_quality.valid_premerge_node_count < (
        known_raw_count + minimum_unknown_raw_count
    ) or (
        not unknown_maturities
        and diagnostic.input_quality.valid_premerge_node_count != known_raw_count
    ):
        raise ValueError("input quality does not reconcile expiry raw_node_count facts")
    ssvi_eligible = [
        result.maturity_id
        for result in diagnostic.expiry_results
        if len(result.raw_k) >= 4
    ]
    if not ssvi_eligible:
        if parents or diagnostic.ssvi_attempt is not None:
            raise ValueError("zero SSVI-eligible expiries require no parent")
    else:
        if len(parents) != 1 or diagnostic.ssvi_attempt != parents[0].attempt_id:
            raise ValueError("SSVI-eligible expiries require one referenced parent")
        parent = parents[0]
        if parent.participating_maturities != ssvi_eligible:
            raise ValueError("SSVI parent must cover exactly the eligible expiries")
        if len(ssvi_eligible) == 1:
            if parent.attempt_status is not AttemptStatus.SKIPPED:
                raise ValueError("one SSVI-eligible expiry requires a skipped parent")
        elif parent.attempt_status is AttemptStatus.SKIPPED:
            raise ValueError("multiple SSVI-eligible expiries cannot skip the parent")
    for parent in parents:
        expected_participating = sorted(
            parent.participating_maturities,
            key=lambda maturity: (maturity_time.get(maturity, math.inf), maturity),
        )
        if parent.participating_maturities != expected_participating:
            raise ValueError("SSVI parent participating maturities are not in T order")
        if any(maturity not in result_by_maturity for maturity in parent.participating_maturities):
            raise ValueError("SSVI parent references an unknown maturity")

    parent_pairs = [
        pair for pair in diagnostic.calendar_pair_checks if pair.phase == "ssvi_parent"
    ]
    actual_parent_by_key: dict[tuple[object, ...], CalendarPairDiagnostic] = {}
    for pair in parent_pairs:
        key = _pair_key(pair)
        if key in actual_parent_by_key:
            raise ValueError("duplicate SSVI parent calendar pair key")
        actual_parent_by_key[key] = pair
    expected_parent_keys: set[tuple[object, ...]] = set()
    for parent in parents:
        children = {
            attempt.maturity_id: attempt
            for attempt in diagnostic.attempts
            if attempt.parent_attempt_id == parent.attempt_id
        }
        if children and set(children) != set(parent.participating_maturities):
            raise ValueError("SSVI children do not cover the parent maturity set")
        for child in children.values():
            if child.method is not FitMethod.SSVI or child.scope is not AttemptScope.EXPIRY:
                raise ValueError("parent attempt has a non-SSVI child")
            if parent.attempt_status is AttemptStatus.ACCEPTED:
                if child.blocked_by_parent or not child.selection_eligible:
                    raise ValueError("accepted SSVI parent must release every child")
            elif not child.blocked_by_parent or child.selection_eligible:
                raise ValueError("rejected SSVI parent must block every child")
            if child.blocked_by_parent and not (
                child.checks["calendar_consistent"].status
                is CheckStatus.NOT_APPLICABLE
                and child.checks["calendar_consistent"].reason_code == "not_run"
            ):
                raise ValueError("blocked SSVI child calendar check must be not_run")
        actual_for_parent: list[CalendarPairDiagnostic] = []
        for earlier, later in combinations(parent.participating_maturities, 2):
            earlier_child = children.get(earlier)
            later_child = children.get(later)
            key = (
                "ssvi_parent",
                parent.attempt_id,
                earlier,
                later,
                None if earlier_child is None else earlier_child.attempt_id,
                None if later_child is None else later_child.attempt_id,
            )
            expected_parent_keys.add(key)
            pair = actual_parent_by_key.get(key)
            if pair is None:
                raise ValueError("calendar pair universe is missing an SSVI parent pair")
            actual_for_parent.append(pair)
        if parent.local_success:
            if not children:
                raise ValueError("locally successful SSVI parent has no children")
            if any(
                pair.check.status is CheckStatus.NOT_APPLICABLE
                for pair in actual_for_parent
            ):
                raise ValueError("locally successful parent child pair cannot be not_run")
            aggregate = _aggregate_calendar_checks(
                tuple(actual_for_parent), no_prior=False
            )
            if parent.checks["calendar_consistent"] != aggregate:
                raise ValueError("SSVI parent calendar aggregate does not match its pairs")
        elif any(
            pair.check.status is not CheckStatus.NOT_APPLICABLE
            or pair.check.reason_code != "not_run"
            for pair in actual_for_parent
        ):
            raise ValueError("locally failed SSVI parent pairs must be not_run")
        elif not (
            parent.checks["calendar_consistent"].status
            is CheckStatus.NOT_APPLICABLE
            and parent.checks["calendar_consistent"].reason_code == "not_run"
        ):
            raise ValueError("locally failed SSVI parent calendar check must be not_run")
    if set(actual_parent_by_key) != expected_parent_keys:
        raise ValueError("SSVI parent calendar pair universe has extra records")

    selection_pairs = [
        pair
        for pair in diagnostic.calendar_pair_checks
        if pair.phase == "expiry_selection"
    ]
    actual_selection_by_key: dict[tuple[object, ...], CalendarPairDiagnostic] = {}
    for pair in selection_pairs:
        key = _pair_key(pair)
        if key in actual_selection_by_key:
            raise ValueError("duplicate expiry-selection calendar pair key")
        actual_selection_by_key[key] = pair
    expected_selection_keys: set[tuple[object, ...]] = set()
    accepted_earlier: list[FitAttemptDiagnostic] = []
    for result in diagnostic.expiry_results:
        result_attempts = [attempt_by_id[attempt_id] for attempt_id in result.attempt_ids]
        accepted_positions = [
            index
            for index, attempt in enumerate(result_attempts)
            if attempt.selection_eligible
            and attempt.attempt_status is AttemptStatus.ACCEPTED
        ]
        if len(accepted_positions) > 1:
            raise ValueError("an expiry cannot contain more than one accepted attempt")
        if accepted_positions and any(
            attempt.selection_eligible
            for attempt in result_attempts[accepted_positions[0] + 1 :]
        ):
            raise ValueError("eligible fallback attempt executed after acceptance")
        for attempt in result_attempts:
            if not attempt.selection_eligible:
                continue
            if attempt.local_success:
                candidate_pairs: list[CalendarPairDiagnostic] = []
                for earlier in accepted_earlier:
                    key = (
                        "expiry_selection",
                        None,
                        earlier.maturity_id,
                        attempt.maturity_id,
                        earlier.attempt_id,
                        attempt.attempt_id,
                    )
                    expected_selection_keys.add(key)
                    pair = actual_selection_by_key.get(key)
                    if pair is None:
                        raise ValueError(
                            "calendar pair universe is missing an expiry-selection pair"
                        )
                    candidate_pairs.append(pair)
                expected_calendar = _aggregate_calendar_checks(
                    tuple(candidate_pairs), no_prior=not accepted_earlier
                )
                if attempt.checks["calendar_consistent"] != expected_calendar:
                    raise ValueError(
                        "expiry attempt calendar aggregate does not match its pairs"
                    )
            elif any(
                pair.later_attempt_id == attempt.attempt_id for pair in selection_pairs
            ):
                raise ValueError("locally failed attempt cannot own selection pairs")
            elif not (
                attempt.checks["calendar_consistent"].status
                is CheckStatus.NOT_APPLICABLE
                and attempt.checks["calendar_consistent"].reason_code == "not_run"
            ):
                raise ValueError("local failure calendar check must be not_run")
            if attempt.attempt_status is AttemptStatus.ACCEPTED:
                accepted_earlier.append(attempt)
                break
    if set(actual_selection_by_key) != expected_selection_keys:
        raise ValueError("expiry-selection calendar pair universe has extra records")

    for pair in diagnostic.calendar_pair_checks:
        earlier_result = result_by_maturity.get(pair.earlier_maturity_id)
        later_result = result_by_maturity.get(pair.later_maturity_id)
        if earlier_result is None or later_result is None:
            raise ValueError("calendar pair references an unknown maturity")
        if earlier_result.time_to_expiry >= later_result.time_to_expiry:
            raise ValueError("calendar pair maturities are not ordered by T")
        if (
            pair.check.status is CheckStatus.NOT_APPLICABLE
            and pair.check.reason_code == "not_run"
        ):
            if (
                pair.common_k_min is not None
                or pair.common_k_max is not None
                or pair.check.grid_point_count != 0
            ):
                raise ValueError("not_run calendar pair must have null support and no grid")
            continue
        if not earlier_result.raw_k or not later_result.raw_k:
            raise ValueError("evaluated calendar pair requires both expiry supports")
        common_k_min = max(earlier_result.raw_k[0], later_result.raw_k[0])
        common_k_max = min(earlier_result.raw_k[-1], later_result.raw_k[-1])
        if common_k_min >= common_k_max:
            if not (
                pair.common_k_min is None
                and pair.common_k_max is None
                and pair.check.status is CheckStatus.NOT_TESTABLE
                and pair.check.reason_code == "no_overlap"
                and pair.check.primary_value is None
                and pair.check.threshold is None
                and pair.check.violation_count is None
                and pair.check.grid_point_count == 0
            ):
                raise ValueError("no-overlap calendar pair has invalid null/grid semantics")
        elif (
            pair.common_k_min != common_k_min
            or pair.common_k_max != common_k_max
            or pair.check.status
            in {CheckStatus.NOT_APPLICABLE, CheckStatus.NOT_TESTABLE}
            or (
                pair.check.status in {CheckStatus.PASSED, CheckStatus.FAILED}
                and pair.check.grid_point_count == 0
            )
        ):
            raise ValueError("calendar pair common support does not match expiry supports")

    attempt_order_by_id = {
        attempt.attempt_id: attempt.attempt_order for attempt in diagnostic.attempts
    }
    expected_pair_order = sorted(
        diagnostic.calendar_pair_checks,
        key=lambda pair: (
            0 if pair.phase == "ssvi_parent" else 1,
            maturity_time[pair.later_maturity_id],
            maturity_time[pair.earlier_maturity_id],
            pair.parent_attempt_id or "",
            attempt_order_by_id.get(pair.later_attempt_id, -1),
            pair.later_attempt_id or "",
            pair.earlier_attempt_id or "",
            pair.pair_check_id,
        ),
    )
    if diagnostic.calendar_pair_checks != expected_pair_order:
        raise ValueError("calendar pair records are not in canonical order")

    supports = [result for result in diagnostic.expiry_results if len(result.raw_k) >= 2]
    if supports:
        expected_k = [
            float(value)
            for value in np.linspace(
                min(result.raw_k[0] for result in supports),
                max(result.raw_k[-1] for result in supports),
                201,
                endpoint=True,
                dtype=np.float64,
            )
        ]
        if (
            diagnostic.surface_grid_status is not SurfaceGridStatus.AVAILABLE
            or diagnostic.surface_log_moneyness != expected_k
        ):
            raise ValueError("available surface grid is not the canonical 201-point grid")
    elif (
        diagnostic.surface_grid_status is not SurfaceGridStatus.UNAVAILABLE_NO_SUPPORT
        or diagnostic.surface_log_moneyness
    ):
        raise ValueError("no-support surface must have zero columns")
    for result, row in zip(
        diagnostic.expiry_results,
        diagnostic.surface_total_variance,
        strict=True,
    ):
        for k, value in zip(diagnostic.surface_log_moneyness, row, strict=True):
            expected_present = (
                result.usable
                and bool(result.raw_k)
                and result.raw_k[0] <= k <= result.raw_k[-1]
            )
            if (value is not None) != expected_present:
                raise ValueError("surface mask extends outside an expiry support")


# ---------------------------------------------------------------------------
# Task 5 isolated AG input/profile/sampling boundary
# ---------------------------------------------------------------------------


_AG_ADAPTER_COLUMNS = (
    "product",
    "datetime",
    "dte",
    "time_to_expiry",
    "strike",
    "iv",
    "log_moneyness",
    "forward_price",
    "forward_source",
)


def _option_file_has_read_schema(path: Path) -> bool:
    try:
        columns = set(pq.ParquetFile(path).schema_arrow.names)
    except Exception as exc:
        raise ValueError(f"cannot inspect parquet schema: {path}") from exc
    return set(READ_COLUMNS).issubset(columns)


def _month_route(data_root: Path, path: Path) -> tuple[int, int]:
    try:
        relative = path.resolve(strict=True).relative_to(data_root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ValueError(f"option file escapes data directory: {path}") from exc
    tokens: set[tuple[int, int]] = set()
    parts = relative.parts
    # The basename is excluded from directory YYYY/MM scanning.
    for index in range(max(len(parts) - 2, 0)):
        year_text, month_text = parts[index], parts[index + 1]
        if re.fullmatch(r"(?:19|20)\d{2}", year_text) and re.fullmatch(
            r"(?:0[1-9]|1[0-2])", month_text
        ):
            tokens.add((int(year_text), int(month_text)))
    match = re.fullmatch(
        r"options_((?:19|20)\d{2})(0[1-9]|1[0-2])\.parquet",
        relative.name,
        flags=re.IGNORECASE,
    )
    if match:
        tokens.add((int(match.group(1)), int(match.group(2))))
    if len(tokens) != 1:
        if not tokens:
            raise ValueError(f"month route cannot be parsed for option file: {relative}")
        raise ValueError(f"conflicting month routes for option file: {relative}")
    return next(iter(tokens))


def _business_values_equal(left: object, right: object) -> bool:
    if _is_null(left) and _is_null(right):
        return True
    if _is_null(left) or _is_null(right):
        return False
    if isinstance(left, pd.Timestamp) or isinstance(right, pd.Timestamp):
        try:
            return pd.Timestamp(left) == pd.Timestamp(right)
        except (TypeError, ValueError):
            return False
    try:
        value = left == right
        return bool(value) if not isinstance(value, np.ndarray) else False
    except (TypeError, ValueError):
        return False


def _deduplicate_raw_quotes(raw: pd.DataFrame) -> pd.DataFrame:
    """Reject ambiguous quote duplicates before quality.keep-first is reached."""

    frame = raw.copy(deep=True)
    business_columns = list(dict.fromkeys([*READ_COLUMNS, "product", "datetime"]))
    missing = [column for column in [*business_columns, "source_file"] if column not in frame]
    if missing:
        raise ValueError(f"duplicate conflict gate missing columns: {missing}")
    frame["source_file"] = frame["source_file"].astype("string")
    frame = frame.sort_values(
        ["datetime", "contract", "source_file"], kind="mergesort"
    ).reset_index(drop=True)
    keep: list[int] = []
    for _, group in frame.groupby(["datetime", "contract"], sort=True, dropna=False):
        reference = group.iloc[0]
        for row_index in range(1, len(group)):
            candidate = group.iloc[row_index]
            if any(
                not _business_values_equal(reference[column], candidate[column])
                for column in business_columns
            ):
                raise ValueError("conflicting duplicate quote for (datetime, contract)")
        keep.append(int(group.index[0]))
    return frame.loc[keep].sort_values(
        ["datetime", "contract", "source_file"], kind="mergesort"
    ).reset_index(drop=True)


def _adapt_surface_nodes(nodes: pd.DataFrame) -> pd.DataFrame:
    adapted = nodes.loc[
        :, ["product", "datetime", "dte", "time_to_expiry", "strike", "iv", "log_moneyness"]
    ].copy(deep=True)
    adapted["forward_price"] = np.nan
    adapted["forward_source"] = ForwardSource.UNDERLYING_PRICE_PROXY.value
    return adapted.loc[:, list(_AG_ADAPTER_COLUMNS)].sort_values(
        ["datetime", "dte", "log_moneyness", "strike"], kind="mergesort"
    ).reset_index(drop=True)


def _source_fingerprint(profiles: Sequence[TimestampProfile]) -> str:
    payload = [
        {
            "product": "ag",
            "timestamp": profile.timestamp,
            "input_fingerprint": profile.input_fingerprint,
        }
        for profile in sorted(profiles, key=lambda item: item.timestamp)
    ]
    return _fingerprint(payload)


def _load_ag_input(
    data_dir: str | Path,
    *,
    policy: FitPolicy,
    _reverse_discovery: bool = False,
) -> AgDiagnosticInput:
    """Load AG month-by-month using the production read/clean/node chain only."""

    root = Path(data_dir)
    if not root.exists() or not root.is_dir():
        raise ValueError("data_dir must be an existing directory")
    root = root.resolve(strict=True)
    discovered = discover_parquet_files(root)
    if _reverse_discovery:
        discovered = list(reversed(discovered))
    groups: dict[tuple[int, int], list[Path]] = {}
    for path in discovered:
        product = partition_product(path)
        if product is not None and product != "ag":
            continue
        if not _option_file_has_read_schema(path):
            continue
        route = _month_route(root, path)
        groups.setdefault(route, []).append(path)
    if not groups:
        raise ValueError("no AG option parquet files with the required schema")

    adapted_chunks: list[pd.DataFrame] = []
    load_profiles: list[dict[str, object]] = []
    config = PipelineConfig.from_paths("ag")
    for year_month in sorted(groups):
        files = sorted(groups[year_month], key=lambda value: os.path.normcase(str(value.resolve())))
        try:
            raw, ingest_profile = read_option_files(
                files, product="ag", start_date=None, end_date=None
            )
        except ValueError as exc:
            if str(exc) != "No rows for product='ag' after filtering":
                raise
            load_profiles.append(
                {
                    "year": year_month[0],
                    "month": year_month[1],
                    "file_count": len(files),
                    "clean_rows": 0,
                    "surface_node_rows": 0,
                    "status": "no_ag_rows",
                }
            )
            continue
        row_month = pd.to_datetime(raw["datetime"], errors="coerce").dt.to_period("M")
        expected_period = pd.Period(f"{year_month[0]:04d}-{year_month[1]:02d}", freq="M")
        if row_month.isna().any() or not row_month.eq(expected_period).all():
            raise ValueError("row month does not match the option-file month route")
        raw = _deduplicate_raw_quotes(raw)
        cleaned, quality_profile = clean_and_profile(raw, config, ingest_profile)
        chunk_profile: dict[str, object] = {
            "year": year_month[0],
            "month": year_month[1],
            "file_count": len(files),
            "clean_rows": int(len(cleaned)),
            "surface_node_rows": 0,
            "status": "loaded",
        }
        if not cleaned.empty:
            try:
                surface_nodes = build_surface_nodes(cleaned)
            except ValueError as exc:
                if "No surface-eligible rows" not in str(exc):
                    raise
            else:
                adapted = _adapt_surface_nodes(surface_nodes)
                chunk_profile["surface_node_rows"] = int(len(adapted))
                adapted_chunks.append(adapted)
        chunk_profile["quality_profile"] = quality_profile
        load_profiles.append(chunk_profile)
    if not adapted_chunks:
        raise ValueError("all AG month groups contain no surface-eligible nodes")

    nodes = pd.concat(adapted_chunks, ignore_index=True, sort=False).sort_values(
        ["datetime", "dte", "log_moneyness", "strike"], kind="mergesort"
    ).reset_index(drop=True)
    profiles: list[TimestampProfile] = []
    for timestamp in sorted(pd.Timestamp(value) for value in nodes["datetime"].unique()):
        timestamp_frame = nodes.loc[nodes["datetime"].eq(timestamp), :].copy(deep=True)
        prepared = prepare_timestamp_nodes(
            timestamp_frame,
            product="ag",
            timestamp=timestamp,
            policy=policy,
        )
        eligible_expiries = [expiry for expiry in prepared.expiries if expiry.node_count >= 2]
        profiles.append(
            TimestampProfile(
                timestamp=prepared.timestamp,
                timestamp_status=prepared.timestamp_status.value,
                input_fingerprint=prepared.input_fingerprint,
                expiry_count=len(eligible_expiries),
                node_total=sum(expiry.node_count for expiry in eligible_expiries),
            )
        )
    canonical_profiles = tuple(sorted(profiles, key=lambda item: item.timestamp))
    return AgDiagnosticInput(
        nodes=nodes.loc[:, list(_AG_ADAPTER_COLUMNS)].copy(deep=True),
        profiles=canonical_profiles,
        source_fingerprint=_source_fingerprint(canonical_profiles),
        load_profile=tuple(load_profiles),
    )


def _coerce_timestamp_profile(value: object) -> TimestampProfile:
    if isinstance(value, TimestampProfile):
        return value
    if isinstance(value, Mapping):
        expected = {
            "timestamp",
            "timestamp_status",
            "input_fingerprint",
            "expiry_count",
            "node_total",
        }
        if set(value) != expected:
            raise ValueError("profile must have the exact TimestampProfile key set")
        return TimestampProfile(**{key: value[key] for key in expected})
    try:
        return TimestampProfile(
            timestamp=getattr(value, "timestamp"),
            timestamp_status=getattr(value, "timestamp_status"),
            input_fingerprint=getattr(value, "input_fingerprint"),
            expiry_count=getattr(value, "expiry_count"),
            node_total=getattr(value, "node_total"),
        )
    except AttributeError as exc:
        raise ValueError("profile must expose TimestampProfile fields") from exc


def _eligible_sampling_profiles(
    profiles: Sequence[object], representative_timestamp: str
) -> list[TimestampProfile]:
    representative = _canonical_timestamp(representative_timestamp)
    by_timestamp: dict[str, TimestampProfile] = {}
    for value in profiles:
        profile = _coerce_timestamp_profile(value)
        existing = by_timestamp.get(profile.timestamp)
        if existing is not None and existing != profile:
            raise ValueError("conflicting duplicate timestamp profiles")
        by_timestamp[profile.timestamp] = profile
    return [
        profile
        for timestamp, profile in sorted(by_timestamp.items())
        if timestamp != representative
        and profile.timestamp_status == TimestampStatus.READY.value
        and profile.expiry_count >= 1
    ]


def select_stratified_timestamps(
    profiles: Sequence[object],
    *,
    representative_timestamp: str,
    sample_count: int = 20,
) -> list[str]:
    """Apply deterministic-stratified-20-v1 exactly, without randomness."""

    if isinstance(sample_count, bool) or sample_count != 20:
        raise ValueError("sample_count must equal 20")
    candidates = _eligible_sampling_profiles(profiles, representative_timestamp)
    count = len(candidates)
    if count <= sample_count:
        return [profile.timestamp for profile in candidates]

    expiries = np.asarray([profile.expiry_count for profile in candidates], dtype=np.float64)
    nodes = np.asarray([profile.node_total for profile in candidates], dtype=np.float64)
    expiry_median = float(np.median(expiries))
    node_median = float(np.median(nodes))
    expiry_range = max(float(np.max(expiries) - np.min(expiries)), 1.0)
    node_range = max(float(np.max(nodes) - np.min(nodes)), 1.0)
    time_denominator = float(max(count - 1, 1))
    strata: dict[tuple[int, str, str], list[int]] = {}
    for index, profile in enumerate(candidates):
        key = (
            min(4, math.floor(5 * index / count)),
            "low" if profile.expiry_count <= expiry_median else "high",
            "low" if profile.node_total <= node_median else "high",
        )
        strata.setdefault(key, []).append(index)

    selected: set[int] = set()
    for key in sorted(strata):
        indices = strata[key]
        centre_i = float(np.median(np.asarray(indices, dtype=np.float64)))
        centre_expiry = float(np.median(expiries[indices]))
        centre_nodes = float(np.median(nodes[indices]))
        winner = min(
            indices,
            key=lambda index: (
                float(
                    np.sqrt(
                        ((np.float64(index) - centre_i) / time_denominator) ** 2
                        + ((expiries[index] - centre_expiry) / expiry_range) ** 2
                        + ((nodes[index] - centre_nodes) / node_range) ** 2
                    )
                ),
                candidates[index].timestamp,
            ),
        )
        selected.add(winner)

    needed = sample_count - len(selected)
    if needed > 0:
        target_ranks = (
            [np.float64(count - 1) / np.float64(2)]
            if needed == 1
            else [
                np.float64(index) * np.float64(count - 1) / np.float64(needed - 1)
                for index in range(needed)
            ]
        )
        for target in target_ranks:
            target_index = int(math.floor(float(target) + 0.5))
            if target_index not in selected:
                selected.add(target_index)
                continue
            distance = 1
            while True:
                options = [
                    index
                    for index in (target_index - distance, target_index + distance)
                    if 0 <= index < count and index not in selected
                ]
                if options:
                    selected.add(min(options))
                    break
                distance += 1
    if len(selected) != sample_count:
        raise ValueError("deterministic sampling failed to select exactly 20 timestamps")
    return sorted(candidates[index].timestamp for index in selected)


def _nearest_profile_timestamp(
    profiles: Sequence[object], representative_timestamp: str
) -> str | None:
    representative = pd.Timestamp(_canonical_timestamp(representative_timestamp))
    values = sorted({_coerce_timestamp_profile(value).timestamp for value in profiles})
    if not values:
        return None
    return min(
        values,
        key=lambda value: (
            abs((pd.Timestamp(value) - representative).total_seconds()),
            pd.Timestamp(value),
        ),
    )


_CACHE_SCHEMA_VERSION = "ag-total-variance-fit-cache-v1"
_CACHE_RECORD_KEYS = frozenset(
    {
        "cache_schema_version",
        "source_fingerprint",
        "input_fingerprint",
        "policy_version",
        "policy",
        "diagnostic",
    }
)


def _validate_json_value(value: object, *, owner: str) -> object:
    if value is None or type(value) in {str, bool, int}:
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f"{owner} must contain finite JSON numbers")
        return value
    if isinstance(value, list):
        return [
            _validate_json_value(item, owner=f"{owner}[{index}]")
            for index, item in enumerate(value)
        ]
    if isinstance(value, dict):
        if any(type(key) is not str for key in value):
            raise ValueError(f"{owner} JSON object keys must be strings")
        return {
            key: _validate_json_value(item, owner=f"{owner}.{key}")
            for key, item in value.items()
        }
    raise ValueError(f"{owner} is not a closed JSON value")


def _decode_typed(value: object, annotation: object, *, owner: str) -> object:
    if annotation is Any:
        return _validate_json_value(value, owner=owner)
    if annotation is None or annotation is type(None):
        if value is not None:
            raise ValueError(f"{owner} must be null")
        return None
    origin = get_origin(annotation)
    arguments = get_args(annotation)
    if origin in {types.UnionType, Union}:
        failures: list[str] = []
        for member in arguments:
            try:
                return _decode_typed(value, member, owner=owner)
            except ValueError as exc:
                failures.append(str(exc))
        raise ValueError(f"{owner} has no valid union type: {'; '.join(failures)}")
    if origin is Literal:
        if not any(type(value) is type(option) and value == option for option in arguments):
            raise ValueError(f"{owner} violates its literal contract")
        return value
    if origin is list:
        if type(value) is not list:
            raise ValueError(f"{owner} must be a list")
        return [
            _decode_typed(item, arguments[0], owner=f"{owner}[{index}]")
            for index, item in enumerate(value)
        ]
    if origin is tuple:
        if type(value) is not list:
            raise ValueError(f"{owner} tuple must be encoded as a JSON list")
        if len(arguments) == 2 and arguments[1] is Ellipsis:
            return tuple(
                _decode_typed(item, arguments[0], owner=f"{owner}[{index}]")
                for index, item in enumerate(value)
            )
        if len(value) != len(arguments):
            raise ValueError(f"{owner} tuple has the wrong length")
        return tuple(
            _decode_typed(item, member, owner=f"{owner}[{index}]")
            for index, (item, member) in enumerate(zip(value, arguments, strict=True))
        )
    if origin in {dict, Mapping, collections_abc.Mapping}:
        if type(value) is not dict:
            raise ValueError(f"{owner} must be an object")
        key_type, value_type = arguments
        decoded: dict[object, object] = {}
        for key, item in value.items():
            decoded_key = _decode_typed(key, key_type, owner=f"{owner}.<key>")
            if decoded_key in decoded:
                raise ValueError(f"{owner} contains duplicate decoded keys")
            decoded[decoded_key] = _decode_typed(
                item, value_type, owner=f"{owner}.{key}"
            )
        return decoded
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        if type(value) is not str:
            raise ValueError(f"{owner} enum value must be a string")
        try:
            return annotation(value)
        except ValueError as exc:
            raise ValueError(f"{owner} has an unknown enum value") from exc
    if isinstance(annotation, type) and is_dataclass(annotation):
        if type(value) is not dict:
            raise ValueError(f"{owner} dataclass must be an object")
        init_fields = [item for item in fields(annotation) if item.init]
        expected = {item.name for item in init_fields}
        if set(value) != expected:
            raise ValueError(
                f"{owner} has an invalid key set; missing={sorted(expected-set(value))}, "
                f"extra={sorted(set(value)-expected)}"
            )
        hints = get_type_hints(annotation)
        decoded_values = {
            item.name: _decode_typed(
                value[item.name], hints[item.name], owner=f"{owner}.{item.name}"
            )
            for item in init_fields
        }
        try:
            return annotation(**decoded_values)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{owner} violates its dataclass contract: {exc}") from exc
    if annotation is str:
        if type(value) is not str:
            raise ValueError(f"{owner} must be a str")
        return value
    if annotation is bool:
        if type(value) is not bool:
            raise ValueError(f"{owner} must be a bool")
        return value
    if annotation is int:
        if type(value) is not int:
            raise ValueError(f"{owner} must be an int")
        return value
    if annotation is float:
        if type(value) is not float or not math.isfinite(value):
            raise ValueError(f"{owner} must be a finite float")
        return value
    raise ValueError(f"{owner} uses an unsupported closed type {annotation!r}")


def _validate_closed_attempt_parameters(attempt: FitAttemptDiagnostic) -> None:
    parameters = attempt.parameters
    if parameters is None:
        return
    if type(parameters) is not dict:
        raise ValueError("attempt parameters must be an exact JSON object or null")
    if attempt.method in {FitMethod.PCHIP, FitMethod.LINEAR}:
        raise ValueError("non-parametric attempt parameters must be null")

    def require_float(value: object, *, owner: str) -> None:
        if type(value) is not float or not math.isfinite(value):
            raise ValueError(f"{owner} must be a finite float")

    if attempt.method is FitMethod.RAW_SVI:
        scalar_names = {"a", "b", "rho", "m", "sigma"}
        if set(parameters) != scalar_names:
            raise ValueError("RAW_SVI parameters violate the closed schema")
        for name in scalar_names:
            require_float(parameters[name], owner=f"RAW_SVI parameters.{name}")
        return

    if attempt.scope is AttemptScope.EXPIRY:
        scalar_names = {"rho", "eta", "gamma", "theta"}
        if set(parameters) != scalar_names:
            raise ValueError("SSVI expiry parameters violate the closed schema")
        for name in scalar_names:
            require_float(parameters[name], owner=f"SSVI expiry parameters.{name}")
        return

    if set(parameters) != {"rho", "eta", "gamma", "theta_by_maturity"}:
        raise ValueError("SSVI parent parameters violate the closed schema")
    for name in ("rho", "eta", "gamma"):
        require_float(parameters[name], owner=f"SSVI parent parameters.{name}")
    theta = parameters["theta_by_maturity"]
    if type(theta) is not dict or set(theta) != set(attempt.participating_maturities):
        raise ValueError(
            "SSVI parent parameters.theta_by_maturity must exactly cover maturities"
        )
    for maturity_id, value in theta.items():
        if type(maturity_id) is not str or not maturity_id:
            raise ValueError(
                "SSVI parent parameters.theta_by_maturity keys must be strings"
            )
        require_float(
            value,
            owner=f"SSVI parent parameters.theta_by_maturity.{maturity_id}",
        )


def decode_timestamp_diagnostic(payload: object) -> TimestampSurfaceDiagnostic:
    """Strictly decode and independently validate the complete Task 4 object."""

    decoded = _decode_typed(
        payload, TimestampSurfaceDiagnostic, owner="TimestampSurfaceDiagnostic"
    )
    if not isinstance(decoded, TimestampSurfaceDiagnostic):
        raise ValueError("decoded payload is not TimestampSurfaceDiagnostic")
    for attempt in decoded.attempts:
        _validate_closed_attempt_parameters(attempt)
    validate_timestamp_diagnostic(decoded)
    return decoded


def _timestamp_cache_key(
    *,
    source_fingerprint: str,
    input_fingerprint: str,
    policy: FitPolicy,
) -> tuple[dict[str, object], str]:
    for name, value in (
        ("source_fingerprint", source_fingerprint),
        ("input_fingerprint", input_fingerprint),
    ):
        if re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
            raise ValueError(f"{name} must be canonical sha256")
    if not isinstance(policy, FitPolicy):
        raise ValueError("policy must be FitPolicy")
    payload: dict[str, object] = {
        "cache_schema_version": _CACHE_SCHEMA_VERSION,
        "input_fingerprint": input_fingerprint,
        "policy": to_json_compatible(policy),
        "source_fingerprint": source_fingerprint,
    }
    return payload, hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()


def _strict_json_bytes_load(data: bytes, *, owner: str) -> object:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{owner} is not UTF-8") from exc

    def reject_constant(value: str) -> object:
        raise ValueError(f"{owner} contains non-finite constant {value}")

    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        decoded: dict[str, object] = {}
        for key, value in pairs:
            if key in decoded:
                raise ValueError(f"{owner} contains duplicate JSON key {key!r}")
            decoded[key] = value
        return decoded

    try:
        payload = json.loads(
            text,
            parse_constant=reject_constant,
            object_pairs_hook=reject_duplicate_keys,
        )
        return _validate_json_value(payload, owner=owner)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{owner} is not strict JSON: {exc}") from exc


def _decode_cache_record(
    payload: object,
    *,
    source_fingerprint: str,
    input_fingerprint: str,
    policy: FitPolicy,
    product: str,
    timestamp: str,
) -> TimestampSurfaceDiagnostic:
    if type(payload) is not dict or set(payload) != _CACHE_RECORD_KEYS:
        raise ValueError("cache record has an invalid key set")
    if payload["cache_schema_version"] != _CACHE_SCHEMA_VERSION:
        raise ValueError("cache record schema is stale")
    if payload["source_fingerprint"] != source_fingerprint:
        raise ValueError("cache record source fingerprint mismatch")
    if payload["input_fingerprint"] != input_fingerprint:
        raise ValueError("cache record input fingerprint mismatch")
    if payload["policy_version"] != policy.policy_version:
        raise ValueError("cache record policy version mismatch")
    if _canonical_json_bytes(payload["policy"]) != _canonical_json_bytes(
        to_json_compatible(policy)
    ):
        raise ValueError("cache record policy mismatch")
    diagnostic = decode_timestamp_diagnostic(payload["diagnostic"])
    if diagnostic.product != product:
        raise ValueError("cached diagnostic product mismatch")
    if diagnostic.timestamp != _canonical_timestamp(timestamp):
        raise ValueError("cached diagnostic timestamp mismatch")
    if diagnostic.input_fingerprint != input_fingerprint:
        raise ValueError("cached diagnostic input fingerprint mismatch")
    if diagnostic.policy_version != policy.policy_version:
        raise ValueError("cached diagnostic policy mismatch")
    return diagnostic


def _cached_timestamp_diagnostic(
    cache_dir: str | Path,
    *,
    source_fingerprint: str,
    input_fingerprint: str,
    policy: FitPolicy,
    product: str,
    timestamp: str,
    builder: Callable[[], TimestampSurfaceDiagnostic],
    _output_dir: str | Path | None = None,
) -> tuple[TimestampSurfaceDiagnostic, bool]:
    """Return one strict cache record; corrupt records are misses and replaced."""

    product = _canonical_product(product)
    timestamp = _canonical_timestamp(timestamp)
    _, digest = _timestamp_cache_key(
        source_fingerprint=source_fingerprint,
        input_fingerprint=input_fingerprint,
        policy=policy,
    )
    requested_cache = _lexical_absolute_path(cache_dir)
    approved_cache = _resolve_path_safely(requested_cache)
    project = _project_root()
    _reject_write_root(
        approved_cache, role="cache", project=project, requested=requested_cache
    )
    requested_output = (
        _lexical_absolute_path(_output_dir) if _output_dir is not None else None
    )
    output = (
        _resolve_path_safely(requested_output) if requested_output is not None else None
    )
    if output is not None:
        _reject_write_root(
            output, role="output", project=project, requested=requested_output
        )
        if _paths_overlap(approved_cache, output):
            raise ValueError("cache_boundary_violation: cache and output overlap")
    capability = _create_cache_capability(
        requested_cache,
        output_dir=requested_output,
        expected_root=approved_cache,
        expected_output=output,
    )
    approved_root = capability.root
    timestamps_dir = capability.timestamps
    temporary: Path | None = None
    temporary_identity: tuple[int, int, int, int, int] | None = None
    try:
        _assert_cache_capability(capability)
        record_path = timestamps_dir / f"{digest}.json"
        safe_record = _validate_cache_internal_path(
            approved_root, record_path, output_dir=output
        )
        if safe_record.exists() and (
            not safe_record.is_file()
            or not stat.S_ISREG(safe_record.lstat().st_mode)
        ):
            raise ValueError(
                "cache_boundary_violation: cache record is not a regular file"
            )
        cache_hit: TimestampSurfaceDiagnostic | None = None
        if safe_record.is_file():
            try:
                raw_record = safe_record.read_bytes()
            except FileNotFoundError:
                raw_record = None
            if raw_record is not None:
                _assert_cache_capability(capability)
                try:
                    payload = _strict_json_bytes_load(raw_record, owner="cache record")
                    if raw_record != _canonical_json_bytes(payload):
                        raise ValueError("cache record is not canonical JSON")
                    cache_hit = _decode_cache_record(
                        payload,
                        source_fingerprint=source_fingerprint,
                        input_fingerprint=input_fingerprint,
                        policy=policy,
                        product=product,
                        timestamp=timestamp,
                    )
                except ValueError:
                    cache_hit = None
        if cache_hit is not None:
            return cache_hit, True

        _assert_cache_capability(capability)
        diagnostic = builder()
        if not isinstance(diagnostic, TimestampSurfaceDiagnostic):
            raise ValueError("cache builder must return TimestampSurfaceDiagnostic")
        validate_timestamp_diagnostic(diagnostic)
        diagnostic = decode_timestamp_diagnostic(to_json_compatible(diagnostic))
        if (
            diagnostic.product != product
            or diagnostic.timestamp != timestamp
            or diagnostic.input_fingerprint != input_fingerprint
            or diagnostic.policy_version != policy.policy_version
        ):
            raise ValueError(
                "cache builder returned a diagnostic with the wrong identity"
            )
        record = {
            "cache_schema_version": _CACHE_SCHEMA_VERSION,
            "source_fingerprint": source_fingerprint,
            "input_fingerprint": input_fingerprint,
            "policy_version": policy.policy_version,
            "policy": to_json_compatible(policy),
            "diagnostic": to_json_compatible(diagnostic),
        }
        data = _canonical_json_bytes(record)
        temporary = timestamps_dir / (
            f".{digest}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
        )
        _assert_cache_capability(capability)
        temporary = _validate_cache_internal_path(
            approved_root, temporary, output_dir=output
        )
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
        temporary_identity = _regular_file_identity(
            temporary, owner="temporary cache record"
        )
        _assert_cache_capability(capability)
        if (
            _regular_file_identity(temporary, owner="temporary cache record")
            != temporary_identity
        ):
            raise ValueError(
                "cache_boundary_violation: temporary cache record identity changed"
            )
        safe_record = _validate_cache_internal_path(
            approved_root, record_path, output_dir=output
        )
        if safe_record.exists() and (
            not safe_record.is_file()
            or not stat.S_ISREG(safe_record.lstat().st_mode)
        ):
            raise ValueError(
                "cache_boundary_violation: record target changed before replace"
            )
        _assert_cache_capability(capability)
        if (
            _regular_file_identity(temporary, owner="temporary cache record")
            != temporary_identity
        ):
            raise ValueError(
                "cache_boundary_violation: temporary cache record identity changed"
            )
        os.replace(temporary, safe_record)
        temporary_identity = None
        _assert_cache_capability(capability)
        return diagnostic, False
    finally:
        if temporary is not None and temporary_identity is not None:
            try:
                _assert_cache_capability(capability)
                if (
                    _regular_file_identity(temporary, owner="temporary cache record")
                    == temporary_identity
                ):
                    temporary.unlink()
            except (FileNotFoundError, ValueError):
                pass
        _finish_cache_capability(capability)


_DIAGNOSTICS_SCHEMA_VERSION = "ag-total-variance-fit-diagnostics-v1"
_SAMPLING_SCHEMA_VERSION = "ag-total-variance-fit-sampling-v1"
_SAMPLING_ALGORITHM_VERSION = "deterministic-stratified-20-v1"
_SUMMARY_SCHEMA_VERSION = "ag-total-variance-fit-summary-v1"
_REPRESENTATIVE_TIMESTAMP = "2025-04-07T10:15:00"
_REQUESTED_SAMPLE_COUNT = 20

ATTEMPTS_CSV_COLUMNS = (
    "diagnostic_only",
    "product",
    "timestamp",
    "attempt_order",
    "attempt_id",
    "parent_attempt_id",
    "scope",
    "maturity_id",
    "participating_maturities_json",
    "time_to_expiry",
    "method",
    "attempt_status",
    "optimizer_attempted",
    "optimizer_success",
    "optimizer_start_summary_json",
    "selection_eligible",
    "blocked_by_parent",
    "local_success",
    "success",
    "parameters_json",
    "per_expiry_metrics_json",
    "rmse_total_variance",
    "nrmse_total_variance",
    "rmse_iv",
    "raw_node_count",
    "node_count",
    "k_min",
    "k_max",
    "candidate_k_json",
    "candidate_total_variance_json",
    "candidate_iv_json",
    "positive_total_variance_status",
    "call_price_monotonic_status",
    "call_price_convex_status",
    "butterfly_g_nonnegative_status",
    "calendar_consistent_status",
    "jump_reliable_status",
    "checks_json",
    "failure_code",
    "failure_reason",
    "policy_version",
    "forward_source",
)


def _canonical_diagnostics(
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
) -> list[TimestampSurfaceDiagnostic]:
    values = list(diagnostics)
    if not values:
        raise ValueError("diagnostics must not be empty")
    for diagnostic in values:
        if not isinstance(diagnostic, TimestampSurfaceDiagnostic):
            raise ValueError("diagnostics must contain TimestampSurfaceDiagnostic")
        validate_timestamp_diagnostic(diagnostic)
    values.sort(key=lambda item: (item.product, item.timestamp))
    identities = [(item.product, item.timestamp) for item in values]
    if len(identities) != len(set(identities)):
        raise ValueError("diagnostics contain duplicate product/timestamp identities")
    if {item.product for item in values} != {"ag"}:
        raise ValueError("Task 5 diagnostics are AG-only")
    if len({item.policy_version for item in values}) != 1:
        raise ValueError("diagnostics must use one policy version")
    return values


def _batch_input_fingerprint(
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
) -> str:
    values = _canonical_diagnostics(diagnostics)
    return _fingerprint(
        [
            {
                "product": item.product,
                "timestamp": item.timestamp,
                "input_fingerprint": item.input_fingerprint,
            }
            for item in values
        ]
    )


def _write_canonical_json(payload: object, path: str | Path) -> None:
    Path(path).write_bytes(_canonical_json_bytes(payload))


def _build_diagnostics_payload(
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
    *,
    source_fingerprint: str,
    representative_timestamp: str,
    selected_additional_timestamps: Sequence[str],
) -> dict[str, object]:
    values = _canonical_diagnostics(diagnostics)
    representative = _canonical_timestamp(representative_timestamp)
    selected = sorted({_canonical_timestamp(item) for item in selected_additional_timestamps})
    if representative in selected or len(selected) != len(selected_additional_timestamps):
        raise ValueError("selected additional timestamps must be unique and exclude representative")
    expected = [representative, *selected]
    if [item.timestamp for item in values] != sorted(expected):
        raise ValueError("diagnostics timestamps do not match representative plus samples")
    if re.fullmatch(r"sha256:[0-9a-f]{64}", source_fingerprint) is None:
        raise ValueError("source_fingerprint must be canonical sha256")
    policy = FitPolicy()
    if values[0].policy_version != policy.policy_version:
        raise ValueError("diagnostics policy is not the Task 5 default policy")
    return {
        "schema_version": _DIAGNOSTICS_SCHEMA_VERSION,
        "diagnostic_only": True,
        "product": "ag",
        "display_label": "AG",
        "representative_timestamp": representative,
        "requested_sample_count": _REQUESTED_SAMPLE_COUNT,
        "actual_sample_count": len(selected),
        "source_fingerprint": source_fingerprint,
        "policy_version": policy.policy_version,
        "policy": to_json_compatible(policy),
        "batch_input_fingerprint": _batch_input_fingerprint(values),
        "timestamps": [to_json_compatible(item) for item in values],
    }


def _build_sampled_timestamps_payload(
    profiles: Sequence[object],
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
    *,
    representative_timestamp: str,
    selected_additional_timestamps: Sequence[str],
    source_fingerprint: str,
) -> dict[str, object]:
    values = _canonical_diagnostics(diagnostics)
    representative = _canonical_timestamp(representative_timestamp)
    selected = sorted(_canonical_timestamp(item) for item in selected_additional_timestamps)
    if len(selected) != len(set(selected)) or representative in selected:
        raise ValueError("selected additional timestamps must be unique")
    profile_values = sorted(
        (_coerce_timestamp_profile(item) for item in profiles),
        key=lambda item: item.timestamp,
    )
    if len({item.timestamp for item in profile_values}) != len(profile_values):
        raise ValueError("profiles contain duplicate timestamps")
    if source_fingerprint != _source_fingerprint(profile_values):
        raise ValueError("source_fingerprint does not match profiles")
    diagnostic_by_timestamp = {item.timestamp: item for item in values}
    if set(diagnostic_by_timestamp) != {representative, *selected}:
        raise ValueError("sampled diagnostics do not match representative plus selection")
    representative_diagnostic = diagnostic_by_timestamp[representative]
    profile_by_timestamp = {item.timestamp: item for item in profile_values}
    representative_profile = profile_by_timestamp.get(representative)
    if (
        representative_profile is None
        or representative_profile.timestamp_status
        != representative_diagnostic.timestamp_status.value
        or representative_profile.input_fingerprint
        != representative_diagnostic.input_fingerprint
    ):
        raise ValueError("representative profile does not match its diagnostic")
    eligible = _eligible_sampling_profiles(profile_values, representative)
    if select_stratified_timestamps(
        profile_values,
        representative_timestamp=representative,
        sample_count=_REQUESTED_SAMPLE_COUNT,
    ) != selected:
        raise ValueError("selected timestamps do not recompute from profiles")
    _validate_selected_profile_references(
        selected,
        eligible_profiles=eligible,
        diagnostics=diagnostic_by_timestamp,
    )
    eligible_payload = [
        {
            "timestamp": profile.timestamp,
            "input_fingerprint": profile.input_fingerprint,
            "expiry_count": profile.expiry_count,
            "node_total": profile.node_total,
        }
        for profile in eligible
    ]
    return {
        "schema_version": _SAMPLING_SCHEMA_VERSION,
        "sampling_algorithm_version": _SAMPLING_ALGORITHM_VERSION,
        "diagnostic_only": True,
        "product": "ag",
        "representative_timestamp": representative,
        "representative_status": representative_diagnostic.timestamp_status.value,
        "representative_input_fingerprint": representative_diagnostic.input_fingerprint,
        "requested_sample_count": _REQUESTED_SAMPLE_COUNT,
        "actual_sample_count": len(selected),
        "selected_additional_timestamps": selected,
        "eligible_candidate_count": len(eligible_payload),
        "eligible_candidate_profiles": eligible_payload,
        "profiled_timestamp_count": len(profile_values),
        "source_fingerprint": source_fingerprint,
        "batch_input_fingerprint": _batch_input_fingerprint(values),
    }


def _validate_selected_profile_references(
    selected: Sequence[str],
    *,
    eligible_profiles: Sequence[TimestampProfile],
    diagnostics: Mapping[str, TimestampSurfaceDiagnostic],
) -> None:
    eligible_by_timestamp = {item.timestamp: item for item in eligible_profiles}
    for timestamp in selected:
        profile = eligible_by_timestamp.get(timestamp)
        diagnostic = diagnostics.get(timestamp)
        if profile is None or diagnostic is None:
            raise ValueError("selected timestamp must reference a visible eligible profile")
        supported = [
            result for result in diagnostic.expiry_results if len(result.raw_k) >= 2
        ]
        expected_expiry_count = len(supported)
        expected_node_total = sum(len(result.raw_k) for result in supported)
        if (
            diagnostic.timestamp_status is not TimestampStatus.READY
            or profile.input_fingerprint != diagnostic.input_fingerprint
            or profile.expiry_count != expected_expiry_count
            or profile.node_total != expected_node_total
        ):
            raise ValueError(
                "selected profile fingerprint/expiry/node facts do not match diagnostic"
            )


_SAMPLED_KEYS = frozenset(
    {
        "schema_version",
        "sampling_algorithm_version",
        "diagnostic_only",
        "product",
        "representative_timestamp",
        "representative_status",
        "representative_input_fingerprint",
        "requested_sample_count",
        "actual_sample_count",
        "selected_additional_timestamps",
        "eligible_candidate_count",
        "eligible_candidate_profiles",
        "profiled_timestamp_count",
        "source_fingerprint",
        "batch_input_fingerprint",
    }
)


def write_sampled_timestamps(payload: object, path: str | Path) -> None:
    if type(payload) is not dict or set(payload) != _SAMPLED_KEYS:
        raise ValueError("sampled timestamps payload has an invalid key set")
    _validate_json_value(payload, owner="sampled_timestamps")
    if (
        payload["schema_version"] != _SAMPLING_SCHEMA_VERSION
        or payload["sampling_algorithm_version"] != _SAMPLING_ALGORITHM_VERSION
        or payload["diagnostic_only"] is not True
        or payload["product"] != "ag"
        or payload["requested_sample_count"] != _REQUESTED_SAMPLE_COUNT
    ):
        raise ValueError("sampled timestamps payload violates fixed constants")
    _write_canonical_json(payload, path)


def _compact_json_text(value: object) -> str:
    return json.dumps(
        to_json_compatible(value),
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )


def _csv_scalar(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, Enum):
        return str(value.value)
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("CSV scalar must be finite")
        return repr(value)
    if type(value) is str:
        return value
    raise ValueError(f"unsupported CSV scalar type: {type(value).__name__}")


def _attempt_csv_row(attempt: FitAttemptDiagnostic) -> dict[str, str]:
    checks = to_json_compatible(attempt.checks)
    return {
        "diagnostic_only": "true",
        "product": attempt.product,
        "timestamp": attempt.timestamp,
        "attempt_order": str(attempt.attempt_order),
        "attempt_id": attempt.attempt_id,
        "parent_attempt_id": _csv_scalar(attempt.parent_attempt_id),
        "scope": attempt.scope.value,
        "maturity_id": _csv_scalar(attempt.maturity_id),
        "participating_maturities_json": _compact_json_text(attempt.participating_maturities),
        "time_to_expiry": _csv_scalar(attempt.time_to_expiry),
        "method": attempt.method.value,
        "attempt_status": attempt.attempt_status.value,
        "optimizer_attempted": _csv_scalar(attempt.optimizer_attempted),
        "optimizer_success": _csv_scalar(attempt.optimizer_success),
        "optimizer_start_summary_json": _compact_json_text(attempt.optimizer_start_summary),
        "selection_eligible": _csv_scalar(attempt.selection_eligible),
        "blocked_by_parent": _csv_scalar(attempt.blocked_by_parent),
        "local_success": _csv_scalar(attempt.local_success),
        "success": _csv_scalar(attempt.success),
        "parameters_json": _compact_json_text(attempt.parameters),
        "per_expiry_metrics_json": _compact_json_text(attempt.per_expiry_metrics),
        "rmse_total_variance": _csv_scalar(attempt.rmse_total_variance),
        "nrmse_total_variance": _csv_scalar(attempt.nrmse_total_variance),
        "rmse_iv": _csv_scalar(attempt.rmse_iv),
        "raw_node_count": _csv_scalar(attempt.raw_node_count),
        "node_count": _csv_scalar(attempt.node_count),
        "k_min": _csv_scalar(attempt.k_min),
        "k_max": _csv_scalar(attempt.k_max),
        "candidate_k_json": _compact_json_text(attempt.candidate_k),
        "candidate_total_variance_json": _compact_json_text(
            attempt.candidate_total_variance
        ),
        "candidate_iv_json": _compact_json_text(attempt.candidate_iv),
        "positive_total_variance_status": checks["positive_total_variance"]["status"],
        "call_price_monotonic_status": checks["call_price_monotonic"]["status"],
        "call_price_convex_status": checks["call_price_convex"]["status"],
        "butterfly_g_nonnegative_status": checks[
            "butterfly_g_nonnegative"
        ]["status"],
        "calendar_consistent_status": checks["calendar_consistent"]["status"],
        "jump_reliable_status": checks["jump_reliable"]["status"],
        "checks_json": _compact_json_text(attempt.checks),
        "failure_code": _csv_scalar(attempt.failure_code),
        "failure_reason": _csv_scalar(attempt.failure_reason),
        "policy_version": attempt.policy_version,
        "forward_source": attempt.forward_source.value,
    }


def write_attempts_csv(
    diagnostics: Sequence[TimestampSurfaceDiagnostic], path: str | Path
) -> None:
    Path(path).write_bytes(_attempts_csv_bytes(diagnostics))


def _attempts_csv_bytes(
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
) -> bytes:
    values = _canonical_diagnostics(diagnostics)
    rows = [
        _attempt_csv_row(attempt)
        for diagnostic in values
        for attempt in sorted(
            diagnostic.attempts,
            key=lambda item: (item.attempt_order, item.attempt_id),
        )
    ]
    from io import StringIO

    buffer = StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=list(ATTEMPTS_CSV_COLUMNS),
        extrasaction="raise",
        lineterminator="\r\n",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8-sig")


def _empty_error_statistics() -> dict[str, object]:
    return {"count": 0, "min": None, "median": None, "p95": None, "max": None}


def _error_statistics(values: Sequence[float]) -> dict[str, object]:
    if not values:
        return _empty_error_statistics()
    array = np.asarray(values, dtype=np.float64)
    if not np.isfinite(array).all():
        raise ValueError("accepted error statistics must be finite")
    return {
        "count": int(array.size),
        "min": float(np.min(array)),
        "median": float(np.median(array)),
        "p95": float(np.quantile(array, 0.95, method="linear")),
        "max": float(np.max(array)),
    }


def build_summary(
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
    *,
    representative_timestamp: str,
    batch_input_fingerprint: str,
) -> dict[str, object]:
    """Independently recompute the closed Task 5 summary from diagnostics."""

    values = _canonical_diagnostics(diagnostics)
    representative = _canonical_timestamp(representative_timestamp)
    by_timestamp = {item.timestamp: item for item in values}
    if representative not in by_timestamp:
        raise ValueError("representative timestamp is absent from diagnostics")
    expected_batch = _batch_input_fingerprint(values)
    if batch_input_fingerprint != expected_batch:
        raise ValueError("batch_input_fingerprint mismatch")
    ready_count = sum(item.timestamp_status is TimestampStatus.READY for item in values)
    failed_count = sum(
        item.timestamp_status is TimestampStatus.FAILED_INPUT for item in values
    )
    expiry_results = [result for item in values for result in item.expiry_results]
    attempts = [attempt for item in values for attempt in item.attempts]
    selection_attempts = [
        attempt
        for attempt in attempts
        if attempt.scope is AttemptScope.EXPIRY and attempt.selection_eligible
    ]

    method_counts = {method.value: 0 for method in FinalMethod}
    for result in expiry_results:
        method_counts[result.method.value] += 1

    outcomes: dict[str, object] = {}
    for method in FitMethod:
        subset = [attempt for attempt in selection_attempts if attempt.method is method]
        accepted_count = sum(attempt.success for attempt in subset)
        denominator = len(subset)
        outcomes[method.value] = {
            "denominator": denominator,
            "local_success_count": sum(attempt.local_success for attempt in subset),
            "accepted_count": accepted_count,
            "calendar_failure_count": sum(
                attempt.local_success and attempt.failure_code == "calendar_conflict"
                for attempt in subset
            ),
            "calendar_indeterminate_count": sum(
                attempt.local_success and attempt.failure_code == "check_resolution_limit"
                for attempt in subset
            ),
            "success_rate": (
                float(accepted_count / denominator) if denominator else None
            ),
        }

    ssvi_parent = {status.value: 0 for status in AttemptStatus}
    for attempt in attempts:
        if attempt.scope is AttemptScope.TIMESTAMP and attempt.method is FitMethod.SSVI:
            ssvi_parent[attempt.attempt_status.value] += 1

    attempts_by_id = {attempt.attempt_id: attempt for attempt in attempts}
    accepted_errors: dict[FitMethod, dict[str, list[float]]] = {
        method: {"rmse_total_variance": [], "nrmse_total_variance": []}
        for method in FitMethod
    }
    for result in expiry_results:
        if not result.usable or result.selected_attempt_id is None:
            continue
        attempt = attempts_by_id[result.selected_attempt_id]
        for metric in ("rmse_total_variance", "nrmse_total_variance"):
            number = getattr(attempt, metric)
            if number is None:
                raise ValueError("selected usable attempt is missing accepted error metrics")
            accepted_errors[attempt.method][metric].append(number)
    accepted_statistics = {
        method.value: {
            metric: _error_statistics(metric_values)
            for metric, metric_values in accepted_errors[method].items()
        }
        for method in FitMethod
    }

    selection_check_counts = {
        name: {status.value: 0 for status in CheckStatus} for name in CHECK_NAMES
    }
    for attempt in selection_attempts:
        for name in CHECK_NAMES:
            selection_check_counts[name][attempt.checks[name].status.value] += 1
    calendar_counts = {status.value: 0 for status in CheckStatus}
    for diagnostic in values:
        for pair in diagnostic.calendar_pair_checks:
            calendar_counts[pair.check.status.value] += 1
    excluded_counts = {code: 0 for code in _INPUT_FAILURE_CODES}
    for diagnostic in values:
        for code in _INPUT_FAILURE_CODES:
            excluded_counts[code] += diagnostic.input_quality.excluded_counts[code]

    attempt_failure_counts: dict[str, int] = {}
    for attempt in attempts:
        if attempt.failure_code is not None:
            attempt_failure_counts[attempt.failure_code] = (
                attempt_failure_counts.get(attempt.failure_code, 0) + 1
            )
    final_failure_counts: dict[str, int] = {}
    for result in expiry_results:
        if not result.usable and result.failure_code is not None:
            final_failure_counts[result.failure_code] = (
                final_failure_counts.get(result.failure_code, 0) + 1
            )
    forward_counts = {source.value: 0 for source in ForwardSource}
    forward_counts["failed_input"] = 0
    for diagnostic in values:
        if diagnostic.timestamp_status is TimestampStatus.FAILED_INPUT:
            forward_counts["failed_input"] += 1
        elif diagnostic.forward_source is not None:
            forward_counts[diagnostic.forward_source.value] += 1

    return {
        "schema_version": _SUMMARY_SCHEMA_VERSION,
        "diagnostic_only": True,
        "product": "ag",
        "representative_timestamp": representative,
        "representative_timestamp_status": by_timestamp[
            representative
        ].timestamp_status.value,
        "policy_version": values[0].policy_version,
        "timestamp_input_fingerprints": [
            {
                "product": item.product,
                "timestamp": item.timestamp,
                "input_fingerprint": item.input_fingerprint,
            }
            for item in values
        ],
        "batch_input_fingerprint": expected_batch,
        "timestamp_counts": {
            "requested": len(values),
            "ready": ready_count,
            "failed_input": failed_count,
        },
        "expiry_counts": {
            "total": len(expiry_results),
            "usable": sum(result.usable for result in expiry_results),
            "unusable": sum(not result.usable for result in expiry_results),
        },
        "final_expiry_method_counts": method_counts,
        "selection_attempt_outcomes_by_method": outcomes,
        "ssvi_parent_outcomes": ssvi_parent,
        "accepted_fit_error_by_method": accepted_statistics,
        "selection_attempt_check_status_counts": selection_check_counts,
        "calendar_pair_status_counts": calendar_counts,
        "input_excluded_counts": excluded_counts,
        "attempt_failure_code_counts": dict(sorted(attempt_failure_counts.items())),
        "final_unusable_failure_code_counts": dict(
            sorted(final_failure_counts.items())
        ),
        "forward_source_counts": forward_counts,
    }


ARTIFACT_FILENAMES = (
    "diagnostics.json",
    "attempts.csv",
    "summary.json",
    "sampled_timestamps.json",
    "ag_20250407_101500_iv_fit_comparison.png",
    "artifact_manifest.json",
)
_MANIFEST_ARTIFACT_FILENAMES = ARTIFACT_FILENAMES[:-1]
_MANIFEST_SCHEMA_VERSION = "ag-total-variance-fit-artifact-manifest-v1"


@dataclass(frozen=True, slots=True)
class RuntimePaths:
    data_dir: Path
    cache_dir: Path
    output_dir: Path


@dataclass(slots=True)
class _StagingCapability:
    token: str
    staging: Path
    output_requested: Path
    output_resolved: Path
    parent: Path
    staging_identity: tuple[int, int, int, int, int]
    parent_identity: tuple[int, int, int, int, int]
    output_identity: tuple[int, int, int, int, int] | None
    state: Literal["active", "publishing", "published", "failed", "revoked"] = (
        "active"
    )


_STAGING_CAPABILITIES: dict[tuple[str, ...], _StagingCapability] = {}


@dataclass(slots=True)
class _CacheCapability:
    root_requested: Path
    root: Path
    output_requested: Path | None
    output: Path | None
    ancestor: Path
    ancestor_identity: tuple[int, int, int, int, int]
    parent: Path
    parent_identity: tuple[int, int, int, int, int]
    root_identity: tuple[int, int, int, int, int]
    timestamps: Path
    timestamps_identity: tuple[int, int, int, int, int]
    state: Literal["active", "revoked"] = "active"


def _project_root() -> Path:
    return Path(__file__).resolve(strict=True).parents[2]


def _resolve_path_safely(value: str | Path) -> Path:
    path = _lexical_absolute_path(value)
    tail: list[str] = []
    cursor = path
    while not os.path.lexists(cursor):
        if cursor.parent == cursor:
            raise ValueError("cache_boundary_violation: no existing path ancestor")
        tail.append(cursor.name)
        cursor = cursor.parent
    try:
        resolved = cursor.resolve(strict=True)
    except OSError as exc:
        raise ValueError("cache_boundary_violation: path cannot be resolved") from exc
    for component in reversed(tail):
        if component in {"", ".", ".."}:
            raise ValueError("cache_boundary_violation: unsafe path component")
        resolved = resolved / component
    return resolved


def _lexical_absolute_path(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = Path.cwd() / path
    return Path(os.path.abspath(path))


def _lexical_chain_has_reparse(path: Path, *, project: Path) -> bool:
    requested_parts = _casefold_parts(path)
    project_parts = _casefold_parts(project)
    if requested_parts[: len(project_parts)] != project_parts:
        return False
    cursor = _lexical_absolute_path(project)
    for component in _lexical_absolute_path(path).parts[len(project.parts) :]:
        cursor = cursor / component
        if os.path.lexists(cursor) and _is_link_or_junction(cursor):
            return True
    return False


def _casefold_parts(path: Path) -> tuple[str, ...]:
    absolute = Path(os.path.abspath(path))
    return tuple(part.casefold() for part in absolute.parts)


def _paths_overlap(left: Path, right: Path) -> bool:
    left_parts = _casefold_parts(left)
    right_parts = _casefold_parts(right)
    if not left_parts or not right_parts or left_parts[0] != right_parts[0]:
        return False
    shortest = min(len(left_parts), len(right_parts))
    return left_parts[:shortest] == right_parts[:shortest]


def _paths_equal(left: Path, right: Path) -> bool:
    return _casefold_parts(left) == _casefold_parts(right)


def _is_descendant(child: Path, parent: Path) -> bool:
    child_parts = _casefold_parts(child)
    parent_parts = _casefold_parts(parent)
    return (
        len(child_parts) > len(parent_parts)
        and child_parts[: len(parent_parts)] == parent_parts
    )


def _is_drive_root(path: Path) -> bool:
    return path.parent == path


def _protected_write_targets(project: Path) -> tuple[Path, ...]:
    return tuple(
        _resolve_path_safely(project / relative)
        for relative in (
            "src",
            "tests",
            "docs",
            "scripts",
            ".superpowers",
            "notebooks",
            ".agent_cache",
            "data",
            "outputs/demo",
            "option_risk_warning_submission.zip",
            "outputs",
        )
    )


def _reject_write_root(
    candidate: Path,
    *,
    role: Literal["cache", "output"],
    project: Path,
    requested: str | Path | None = None,
) -> None:
    requested_path = _lexical_absolute_path(candidate if requested is None else requested)
    default_cache = _lexical_absolute_path(
        project / "outputs" / ".ag_total_variance_fit_cache"
    )
    default_output = _lexical_absolute_path(
        project / "outputs" / "ag_total_variance_fit_diagnostics"
    )
    own_default = default_cache if role == "cache" else default_output
    other_default = default_output if role == "cache" else default_cache
    if _paths_equal(requested_path, other_default) or _paths_equal(
        candidate, other_default
    ):
        raise ValueError("cache_boundary_violation: default paths cannot swap roles")
    if _paths_equal(requested_path, own_default):
        if not _paths_equal(candidate, own_default) or _lexical_chain_has_reparse(
            requested_path, project=project
        ):
            raise ValueError(
                "cache_boundary_violation: default path cannot traverse an alias"
            )
        return
    if (
        _is_drive_root(candidate)
        or _is_drive_root(requested_path)
        or _paths_equal(candidate, project)
        or _paths_equal(requested_path, project)
        or _paths_equal(candidate, _resolve_path_safely(Path.home()))
        or _paths_equal(requested_path, _lexical_absolute_path(Path.home()))
    ):
        raise ValueError("cache_boundary_violation: unsafe writable root")
    for checked in (requested_path, candidate):
        if _paths_overlap(checked, default_cache) or _paths_overlap(
            checked, default_output
        ):
            raise ValueError("cache_boundary_violation: default allowlist does not propagate")
    protected_lexical = tuple(
        _lexical_absolute_path(project / relative)
        for relative in (
            "src",
            "tests",
            "docs",
            "scripts",
            ".superpowers",
            "notebooks",
            ".agent_cache",
            "data",
            "outputs/demo",
            "option_risk_warning_submission.zip",
            "outputs",
        )
    )
    for checked in (requested_path, candidate):
        for protected in (*protected_lexical, *_protected_write_targets(project)):
            if _paths_overlap(checked, protected):
                raise ValueError(
                    "cache_boundary_violation: writable path overlaps protected target"
                )


def _validate_runtime_paths(
    data_dir: str | Path,
    cache_dir: str | Path,
    output_dir: str | Path,
) -> RuntimePaths:
    """Resolve every path before discovery or mkdir and enforce the closed boundary."""

    data = _resolve_path_safely(data_dir)
    if not data.exists() or not data.is_dir():
        raise ValueError("cache_boundary_violation: data_dir must be an existing directory")
    cache_requested = _lexical_absolute_path(cache_dir)
    output_requested = _lexical_absolute_path(output_dir)
    cache = _resolve_path_safely(cache_requested)
    output = _resolve_path_safely(output_requested)
    project = _project_root()
    _reject_write_root(
        cache, role="cache", project=project, requested=cache_requested
    )
    _reject_write_root(
        output, role="output", project=project, requested=output_requested
    )
    if _paths_overlap(data, cache) or _paths_overlap(data, output):
        raise ValueError("cache_boundary_violation: data and writable paths overlap")
    if _paths_overlap(cache, output):
        raise ValueError("cache_boundary_violation: cache and output overlap")
    return RuntimePaths(data_dir=data, cache_dir=cache, output_dir=output)


def _is_link_or_junction(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        junction = getattr(path, "is_junction", None)
        if junction is not None and bool(junction()):
            return True
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        return bool(reparse_flag and attributes & reparse_flag)
    except OSError:
        return True


def _validate_cache_internal_path(
    cache_root: Path,
    candidate: Path,
    *,
    output_dir: Path | None,
) -> Path:
    resolved_root = _resolve_path_safely(cache_root)
    resolved_candidate = _resolve_path_safely(candidate)
    if not _is_descendant(resolved_candidate, resolved_root):
        raise ValueError("cache_boundary_violation: cache operation escaped cache root")
    if output_dir is not None and _paths_overlap(resolved_candidate, output_dir):
        raise ValueError("cache_boundary_violation: cache operation overlaps output")
    return resolved_candidate


def _nearest_existing_directory(path: Path) -> Path:
    cursor = _lexical_absolute_path(path)
    while not os.path.lexists(cursor):
        if cursor.parent == cursor:
            raise ValueError("cache_boundary_violation: no existing cache ancestor")
        cursor = cursor.parent
    _directory_identity(cursor, owner="cache ancestor")
    return cursor


def _create_cache_capability(
    cache_dir: str | Path,
    *,
    output_dir: str | Path | None,
    expected_root: Path | None = None,
    expected_output: Path | None = None,
) -> _CacheCapability:
    requested_root = _lexical_absolute_path(cache_dir)
    root = _resolve_path_safely(requested_root)
    project = _project_root()
    _reject_write_root(
        root, role="cache", project=project, requested=requested_root
    )
    if expected_root is not None and not _paths_equal(root, expected_root):
        raise ValueError("cache_boundary_violation: cache root changed before creation")

    requested_output = (
        _lexical_absolute_path(output_dir) if output_dir is not None else None
    )
    output = (
        _resolve_path_safely(requested_output)
        if requested_output is not None
        else None
    )
    if output is not None:
        _reject_write_root(
            output, role="output", project=project, requested=requested_output
        )
        if expected_output is not None and not _paths_equal(output, expected_output):
            raise ValueError("cache_boundary_violation: output changed before cache creation")
        if _paths_overlap(root, output):
            raise ValueError("cache_boundary_violation: cache and output overlap")

    ancestor = _nearest_existing_directory(requested_root)
    ancestor_identity = _directory_identity(ancestor, owner="cache ancestor")
    if not root.exists():
        root.mkdir(parents=True, exist_ok=False)
    if _directory_identity(ancestor, owner="cache ancestor") != ancestor_identity:
        raise ValueError("cache_boundary_violation: cache ancestor identity changed")
    if not _paths_equal(_resolve_path_safely(requested_root), root):
        raise ValueError("cache_boundary_violation: cache root changed during creation")
    _reject_write_root(
        root, role="cache", project=project, requested=requested_root
    )
    parent = root.parent
    parent_identity = _directory_identity(parent, owner="cache parent")
    root_identity = _directory_identity(root, owner="cache root")

    timestamps = _validate_cache_internal_path(
        root, root / "timestamps", output_dir=output
    )
    if not timestamps.exists():
        if (
            _directory_identity(ancestor, owner="cache ancestor")
            != ancestor_identity
            or _directory_identity(parent, owner="cache parent")
            != parent_identity
            or _directory_identity(root, owner="cache root") != root_identity
        ):
            raise ValueError(
                "cache_boundary_violation: cache identity changed before timestamps"
            )
        timestamps.mkdir(exist_ok=False)
    timestamps = timestamps.resolve(strict=True)
    timestamps_identity = _directory_identity(
        timestamps, owner="cache timestamps"
    )
    capability = _CacheCapability(
        root_requested=requested_root,
        root=root.resolve(strict=True),
        output_requested=requested_output,
        output=output,
        ancestor=ancestor,
        ancestor_identity=ancestor_identity,
        parent=parent,
        parent_identity=parent_identity,
        root_identity=root_identity,
        timestamps=timestamps,
        timestamps_identity=timestamps_identity,
    )
    _assert_cache_capability(capability)
    return capability


def _assert_cache_capability(capability: _CacheCapability) -> None:
    if not isinstance(capability, _CacheCapability) or capability.state != "active":
        raise ValueError("cache_boundary_violation: cache capability is expired")
    project = _project_root()
    current_root = _resolve_path_safely(capability.root_requested)
    _reject_write_root(
        current_root,
        role="cache",
        project=project,
        requested=capability.root_requested,
    )
    if not _paths_equal(current_root, capability.root):
        raise ValueError("cache_boundary_violation: cache root path changed")
    if capability.output_requested is not None:
        current_output = _resolve_path_safely(capability.output_requested)
        _reject_write_root(
            current_output,
            role="output",
            project=project,
            requested=capability.output_requested,
        )
        if capability.output is None or not _paths_equal(
            current_output, capability.output
        ):
            raise ValueError("cache_boundary_violation: output path changed")
        if _paths_overlap(current_root, current_output):
            raise ValueError("cache_boundary_violation: cache and output overlap")
    for path, expected, owner in (
        (capability.ancestor, capability.ancestor_identity, "cache ancestor"),
        (capability.parent, capability.parent_identity, "cache parent"),
        (capability.root, capability.root_identity, "cache root"),
        (
            capability.timestamps,
            capability.timestamps_identity,
            "cache timestamps",
        ),
    ):
        if _directory_identity(path, owner=owner) != expected:
            raise ValueError(f"cache_boundary_violation: {owner} identity changed")
    if not _is_descendant(capability.timestamps, capability.root):
        raise ValueError("cache_boundary_violation: timestamps escaped cache root")


def _finish_cache_capability(capability: _CacheCapability) -> None:
    capability.state = "revoked"


def _sha256_hex(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _runtime_versions() -> dict[str, str]:
    import matplotlib
    import scipy

    return {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__,
    }


def _write_artifact_manifest(
    directory: str | Path,
    *,
    source_fingerprint: str,
    batch_input_fingerprint: str,
    policy_version: str,
    generated_at: str,
) -> None:
    root = Path(directory)
    _require_generated_at(generated_at)
    for name, value in (
        ("source_fingerprint", source_fingerprint),
        ("batch_input_fingerprint", batch_input_fingerprint),
    ):
        _require_canonical_sha256(value, owner=name)
    artifacts: list[dict[str, object]] = []
    for name in _MANIFEST_ARTIFACT_FILENAMES:
        path = root / name
        if not path.is_file() or not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError(f"artifact missing or not regular: {name}")
        artifacts.append(
            {
                "relative_path": name,
                "byte_size": path.stat().st_size,
                "sha256": _sha256_hex(path),
            }
        )
    payload = {
        "schema_version": _MANIFEST_SCHEMA_VERSION,
        "diagnostic_only": True,
        "product": "ag",
        "generated_at": generated_at,
        "source_fingerprint": source_fingerprint,
        "policy_version": policy_version,
        "batch_input_fingerprint": batch_input_fingerprint,
        "runtime_versions": _runtime_versions(),
        "artifacts": artifacts,
    }
    _write_canonical_json(payload, root / "artifact_manifest.json")


def _read_canonical_json(path: Path, *, owner: str) -> object:
    data = path.read_bytes()
    payload = _strict_json_bytes_load(data, owner=owner)
    if data != _canonical_json_bytes(payload):
        raise ValueError(f"{owner} is not canonical JSON")
    return payload


_DIAGNOSTICS_KEYS = frozenset(
    {
        "schema_version",
        "diagnostic_only",
        "product",
        "display_label",
        "representative_timestamp",
        "requested_sample_count",
        "actual_sample_count",
        "source_fingerprint",
        "policy_version",
        "policy",
        "batch_input_fingerprint",
        "timestamps",
    }
)
_SUMMARY_KEYS = frozenset(
    {
        "schema_version",
        "diagnostic_only",
        "product",
        "representative_timestamp",
        "representative_timestamp_status",
        "policy_version",
        "timestamp_input_fingerprints",
        "batch_input_fingerprint",
        "timestamp_counts",
        "expiry_counts",
        "final_expiry_method_counts",
        "selection_attempt_outcomes_by_method",
        "ssvi_parent_outcomes",
        "accepted_fit_error_by_method",
        "selection_attempt_check_status_counts",
        "calendar_pair_status_counts",
        "input_excluded_counts",
        "attempt_failure_code_counts",
        "final_unusable_failure_code_counts",
        "forward_source_counts",
    }
)
_MANIFEST_KEYS = frozenset(
    {
        "schema_version",
        "diagnostic_only",
        "product",
        "generated_at",
        "source_fingerprint",
        "policy_version",
        "batch_input_fingerprint",
        "runtime_versions",
        "artifacts",
    }
)


def _require_exact_regular_artifacts(root: Path) -> None:
    if not root.exists() or not root.is_dir() or _is_link_or_junction(root):
        raise ValueError("artifact bundle must be a real directory")
    entries = list(root.iterdir())
    names = {entry.name for entry in entries}
    if names != set(ARTIFACT_FILENAMES) or len(entries) != len(ARTIFACT_FILENAMES):
        raise ValueError("artifact bundle must contain exact six approved files")
    for entry in entries:
        if not stat.S_ISREG(entry.lstat().st_mode):
            raise ValueError("artifact bundle entries must be regular files")


def validate_artifact_bundle(path: str | Path) -> dict[str, object]:
    """Strictly decode, cross-recompute and hash an exact-six artifact bundle."""

    root = Path(path)
    _require_exact_regular_artifacts(root)
    diagnostics_payload = _read_canonical_json(
        root / "diagnostics.json", owner="diagnostics.json"
    )
    if type(diagnostics_payload) is not dict or set(diagnostics_payload) != _DIAGNOSTICS_KEYS:
        raise ValueError("diagnostics.json has an invalid key set")
    requested_count = _require_nonnegative_json_int(
        diagnostics_payload["requested_sample_count"],
        owner="diagnostics requested_sample_count",
    )
    _require_nonnegative_json_int(
        diagnostics_payload["actual_sample_count"],
        owner="diagnostics actual_sample_count",
    )
    _require_canonical_sha256(
        diagnostics_payload["source_fingerprint"],
        owner="diagnostics source_fingerprint",
    )
    if (
        diagnostics_payload["schema_version"] != _DIAGNOSTICS_SCHEMA_VERSION
        or diagnostics_payload["diagnostic_only"] is not True
        or diagnostics_payload["product"] != "ag"
        or diagnostics_payload["display_label"] != "AG"
        or diagnostics_payload["representative_timestamp"] != _REPRESENTATIVE_TIMESTAMP
        or requested_count != _REQUESTED_SAMPLE_COUNT
        or _canonical_json_bytes(diagnostics_payload["policy"])
        != _canonical_json_bytes(to_json_compatible(FitPolicy()))
        or diagnostics_payload["policy_version"] != FitPolicy().policy_version
    ):
        raise ValueError("diagnostics.json violates fixed constants")
    if type(diagnostics_payload["timestamps"]) is not list:
        raise ValueError("diagnostics timestamps must be a list")
    diagnostics = [
        decode_timestamp_diagnostic(item) for item in diagnostics_payload["timestamps"]
    ]
    diagnostics = _canonical_diagnostics(diagnostics)
    if [to_json_compatible(item) for item in diagnostics] != diagnostics_payload["timestamps"]:
        raise ValueError("diagnostics timestamps are not canonically ordered")
    batch = _batch_input_fingerprint(diagnostics)
    if diagnostics_payload["batch_input_fingerprint"] != batch:
        raise ValueError("diagnostics batch fingerprint mismatch")

    sampled = _read_canonical_json(
        root / "sampled_timestamps.json", owner="sampled_timestamps.json"
    )
    if type(sampled) is not dict or set(sampled) != _SAMPLED_KEYS:
        raise ValueError("sampled_timestamps.json has an invalid key set")
    sampled_requested_count = _require_nonnegative_json_int(
        sampled["requested_sample_count"],
        owner="sampled requested_sample_count",
    )
    sampled_actual_count = _require_nonnegative_json_int(
        sampled["actual_sample_count"],
        owner="sampled actual_sample_count",
    )
    sampled_eligible_count = _require_nonnegative_json_int(
        sampled["eligible_candidate_count"],
        owner="sampled eligible_candidate_count",
    )
    profiled_count = _require_nonnegative_json_int(
        sampled["profiled_timestamp_count"],
        owner="sampled profiled_timestamp_count",
    )
    _require_canonical_sha256(
        sampled["source_fingerprint"], owner="sampled source_fingerprint"
    )
    if (
        sampled["schema_version"] != _SAMPLING_SCHEMA_VERSION
        or sampled["sampling_algorithm_version"] != _SAMPLING_ALGORITHM_VERSION
        or sampled["diagnostic_only"] is not True
        or sampled["product"] != "ag"
        or sampled["representative_timestamp"] != _REPRESENTATIVE_TIMESTAMP
        or sampled_requested_count != _REQUESTED_SAMPLE_COUNT
    ):
        raise ValueError("sampled_timestamps.json violates fixed constants")
    selected = sampled["selected_additional_timestamps"]
    if type(selected) is not list or any(type(item) is not str for item in selected):
        raise ValueError("selected timestamps must be a string list")
    if selected != sorted(set(selected)) or _REPRESENTATIVE_TIMESTAMP in selected:
        raise ValueError("selected timestamps are not canonical unique samples")
    if sampled_actual_count != len(selected):
        raise ValueError("sampled actual count mismatch")
    profile_payloads = sampled["eligible_candidate_profiles"]
    if type(profile_payloads) is not list:
        raise ValueError("eligible candidate profiles must be a list")
    eligible_profiles: list[TimestampProfile] = []
    expected_profile_keys = {"timestamp", "input_fingerprint", "expiry_count", "node_total"}
    for item in profile_payloads:
        if type(item) is not dict or set(item) != expected_profile_keys:
            raise ValueError("eligible candidate profile has an invalid key set")
        eligible_profiles.append(
            TimestampProfile(
                timestamp=item["timestamp"],
                timestamp_status=TimestampStatus.READY.value,
                input_fingerprint=item["input_fingerprint"],
                expiry_count=item["expiry_count"],
                node_total=item["node_total"],
            )
        )
    eligible_timestamps = [item.timestamp for item in eligible_profiles]
    if (
        len(eligible_timestamps) != len(set(eligible_timestamps))
        or _REPRESENTATIVE_TIMESTAMP in eligible_timestamps
        or any(
            item.expiry_count < 1 or item.node_total < 2 * item.expiry_count
            for item in eligible_profiles
        )
    ):
        raise ValueError("eligible candidate profiles are duplicated or ineligible")
    if profile_payloads != [
        {
            "timestamp": item.timestamp,
            "input_fingerprint": item.input_fingerprint,
            "expiry_count": item.expiry_count,
            "node_total": item.node_total,
        }
        for item in sorted(eligible_profiles, key=lambda value: value.timestamp)
    ]:
        raise ValueError("eligible candidate profiles are not canonically sorted")
    if sampled_eligible_count != len(eligible_profiles):
        raise ValueError("eligible candidate count mismatch")
    if profiled_count < max(len(diagnostics), 1 + len(eligible_profiles)):
        raise ValueError("profiled timestamp count does not cover diagnostics/profiles")
    if select_stratified_timestamps(
        eligible_profiles,
        representative_timestamp=_REPRESENTATIVE_TIMESTAMP,
        sample_count=_REQUESTED_SAMPLE_COUNT,
    ) != selected:
        raise ValueError("selected timestamps do not independently recompute")
    expected_timestamps = sorted([_REPRESENTATIVE_TIMESTAMP, *selected])
    if [item.timestamp for item in diagnostics] != expected_timestamps:
        raise ValueError("diagnostics and sampled timestamp references disagree")
    _validate_selected_profile_references(
        selected,
        eligible_profiles=eligible_profiles,
        diagnostics={item.timestamp: item for item in diagnostics},
    )
    representative = next(
        item for item in diagnostics if item.timestamp == _REPRESENTATIVE_TIMESTAMP
    )
    if (
        sampled["representative_status"] != representative.timestamp_status.value
        or sampled["representative_input_fingerprint"] != representative.input_fingerprint
        or sampled["batch_input_fingerprint"] != batch
        or sampled["source_fingerprint"] != diagnostics_payload["source_fingerprint"]
    ):
        raise ValueError("sampling references disagree with diagnostics")
    if diagnostics_payload["actual_sample_count"] != len(selected):
        raise ValueError("diagnostics actual sample count mismatch")

    summary = _read_canonical_json(root / "summary.json", owner="summary.json")
    if type(summary) is not dict or set(summary) != _SUMMARY_KEYS:
        raise ValueError("summary.json has an invalid key set")
    expected_summary = build_summary(
        diagnostics,
        representative_timestamp=_REPRESENTATIVE_TIMESTAMP,
        batch_input_fingerprint=batch,
    )
    if _canonical_json_bytes(summary) != _canonical_json_bytes(expected_summary):
        raise ValueError("summary.json does not independently recompute")
    attempts_bytes = (root / "attempts.csv").read_bytes()
    if attempts_bytes != _attempts_csv_bytes(diagnostics):
        raise ValueError("attempts.csv does not match diagnostics")
    png_bytes = (root / "ag_20250407_101500_iv_fit_comparison.png").read_bytes()
    if not png_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("comparison artifact is not a PNG")

    manifest = _read_canonical_json(
        root / "artifact_manifest.json", owner="artifact_manifest.json"
    )
    if type(manifest) is not dict or set(manifest) != _MANIFEST_KEYS:
        raise ValueError("artifact_manifest.json has an invalid key set")
    _require_canonical_sha256(
        manifest["source_fingerprint"], owner="manifest source_fingerprint"
    )
    _require_generated_at(manifest["generated_at"])
    if (
        manifest["schema_version"] != _MANIFEST_SCHEMA_VERSION
        or manifest["diagnostic_only"] is not True
        or manifest["product"] != "ag"
        or manifest["source_fingerprint"] != diagnostics_payload["source_fingerprint"]
        or manifest["policy_version"] != diagnostics_payload["policy_version"]
        or manifest["batch_input_fingerprint"] != batch
    ):
        raise ValueError("artifact manifest constants/references are invalid")
    versions = manifest["runtime_versions"]
    if (
        type(versions) is not dict
        or set(versions) != {"python", "numpy", "scipy", "matplotlib"}
        or any(type(value) is not str or not value for value in versions.values())
    ):
        raise ValueError("artifact manifest runtime_versions are invalid")
    artifacts = manifest["artifacts"]
    if type(artifacts) is not list or len(artifacts) != len(_MANIFEST_ARTIFACT_FILENAMES):
        raise ValueError("artifact manifest artifact list is invalid")
    for item, expected_name in zip(
        artifacts, _MANIFEST_ARTIFACT_FILENAMES, strict=True
    ):
        if type(item) is not dict or set(item) != {"relative_path", "byte_size", "sha256"}:
            raise ValueError("artifact manifest entry has an invalid key set")
        artifact_path = root / expected_name
        byte_size = _require_nonnegative_json_int(
            item["byte_size"], owner=f"manifest {expected_name} byte_size"
        )
        if (
            item["relative_path"] != expected_name
            or byte_size != artifact_path.stat().st_size
            or type(item["sha256"]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is None
            or item["sha256"] != _sha256_hex(artifact_path)
        ):
            raise ValueError("artifact manifest size/hash mismatch")
    return {
        "diagnostics": diagnostics_payload,
        "sampled_timestamps": sampled,
        "summary": summary,
        "manifest": manifest,
    }


def _validate_existing_output_names(output: Path) -> None:
    if not output.exists():
        return
    if not output.is_dir() or _is_link_or_junction(output):
        raise ValueError("artifact output must be a real directory")
    for entry in output.iterdir():
        if entry.name not in ARTIFACT_FILENAMES or not stat.S_ISREG(entry.lstat().st_mode):
            raise ValueError("artifact output contains unknown or non-regular entries")


def publish_artifact_bundle(
    staging_dir: str | Path,
    output_dir: str | Path,
    *,
    force: bool,
) -> None:
    """Publish a validated exact-six bundle, with the manifest replaced last."""

    capability, staging, output = _claim_staging_capability(
        staging_dir, output_dir
    )
    try:
        validate_artifact_bundle(staging)
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
        _validate_existing_output_names(output)
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
        if output.exists() and not force:
            raise ValueError("artifact output already exists; use force")
        if not output.exists():
            output.mkdir(exist_ok=False)
            if (
                _directory_identity(capability.parent, owner="staging parent")
                != capability.parent_identity
            ):
                raise ValueError(
                    "cache_boundary_violation: staging parent changed during output creation"
                )
            capability.output_identity = _directory_identity(
                output, owner="artifact output"
            )
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
        for name in _MANIFEST_ARTIFACT_FILENAMES:
            _assert_staging_capability_identity(
                capability, allowed_states=frozenset({"publishing"})
            )
            os.replace(staging / name, output / name)
            _assert_staging_capability_identity(
                capability, allowed_states=frozenset({"publishing"})
            )
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
        os.replace(
            staging / "artifact_manifest.json",
            output / "artifact_manifest.json",
        )
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
        validate_artifact_bundle(output)
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
    except Exception:
        _finish_staging_capability(capability, state="failed")
        raise
    else:
        _finish_staging_capability(capability, state="published")


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _plot_line_values(values: Sequence[float | None]) -> list[float]:
    plotted: list[float] = []
    for value in values:
        if value is None:
            plotted.append(float("nan"))
        elif type(value) is float and math.isfinite(value):
            plotted.append(value)
        else:
            raise ValueError("plot line values must be finite floats or null")
    return plotted


def _latest_rejected_parameter_candidate(
    diagnostic: TimestampSurfaceDiagnostic,
    maturity_id: str,
) -> FitAttemptDiagnostic | None:
    candidates = [
        attempt
        for attempt in diagnostic.attempts
        if attempt.maturity_id == maturity_id
        and attempt.attempt_status is AttemptStatus.FAILED
        and attempt.method in {FitMethod.SSVI, FitMethod.RAW_SVI}
        and bool(attempt.candidate_k)
    ]
    return (
        max(candidates, key=lambda item: (item.attempt_order, item.attempt_id))
        if candidates
        else None
    )


def plot_representative_comparison(
    diagnostic: TimestampSurfaceDiagnostic,
    path: str | Path,
) -> None:
    """Plot raw IV, the accepted curve, and at most one rejected candidate."""

    validate_timestamp_diagnostic(diagnostic)
    import matplotlib

    matplotlib.use("Agg", force=True)
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    expiry_count = len(diagnostic.expiry_results)
    rows = max(1, math.ceil(expiry_count / 3))
    with matplotlib.rc_context(
        {
            "font.family": "DejaVu Sans",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.unicode_minus": True,
        }
    ):
        figure = Figure(figsize=(15.0, 4.0 * rows), dpi=160, facecolor="white")
        FigureCanvasAgg(figure)
        axes = np.asarray(
            figure.subplots(rows, 3, squeeze=False), dtype=object
        ).reshape(rows, 3)
        by_attempt = {attempt.attempt_id: attempt for attempt in diagnostic.attempts}
        if expiry_count == 0:
            axis = axes[0, 0]
            reason = diagnostic.timestamp_failure_reason or (
                "No expiry passed the input/node eligibility boundary."
            )
            axis.text(
                0.5,
                0.5,
                f"No usable expiry curves\n{reason}",
                ha="center",
                va="center",
                transform=axis.transAxes,
                wrap=True,
            )
            axis.set_axis_off()
        for index, result in enumerate(diagnostic.expiry_results):
            axis = axes[index // 3, index % 3]
            if result.raw_k:
                axis.scatter(
                    result.raw_k,
                    result.raw_iv,
                    label="Raw IV nodes",
                    color="#202124",
                    marker="o",
                    s=24,
                    zorder=3,
                )
            if result.fit_k:
                axis.plot(
                    result.fit_k,
                    _plot_line_values(result.fit_iv),
                    label="Accepted fit",
                    color="#1565C0",
                    linestyle="-",
                    linewidth=1.8,
                    zorder=2,
                )
            rejected = _latest_rejected_parameter_candidate(
                diagnostic, result.maturity_id
            )
            if rejected is not None:
                axis.plot(
                    rejected.candidate_k,
                    _plot_line_values(rejected.candidate_iv),
                    label="Rejected parameter candidate",
                    color="#B0B0B0",
                    linestyle="--",
                    linewidth=1.3,
                    zorder=1,
                )
            selected = (
                by_attempt.get(result.selected_attempt_id)
                if result.selected_attempt_id is not None
                else None
            )
            rmse = (
                "n/a"
                if selected is None or selected.rmse_total_variance is None
                else format(selected.rmse_total_variance, ".6g")
            )
            axis.set_title(
                f"DTE={result.maturity_id} | method={result.method.value} | "
                f"nodes={len(result.raw_k)} | RMSE(w)={rmse}",
                fontsize=9,
            )
            axis.set_xlabel("k = ln(K/F)")
            axis.set_ylabel("Implied volatility")
            axis.grid(True, color="#E5E7EB", linewidth=0.6, linestyle=":")
            axis.margins(x=0.03, y=0.08)
            handles, labels = axis.get_legend_handles_labels()
            if handles:
                axis.legend(handles, labels, loc="upper right", fontsize=7, frameon=True)
            if not result.usable and result.failure_reason:
                axis.text(
                    0.02,
                    0.03,
                    f"UNUSABLE: {result.failure_reason}",
                    transform=axis.transAxes,
                    ha="left",
                    va="bottom",
                    fontsize=7,
                    color="#7F1D1D",
                    wrap=True,
                )
        for index in range(expiry_count, rows * 3):
            if expiry_count == 0 and index == 0:
                continue
            axes[index // 3, index % 3].set_visible(False)
        if diagnostic.forward_source is not None:
            forward_text = diagnostic.forward_source.value
        elif diagnostic.observed_forward_sources:
            forward_text = ",".join(
                source.value for source in diagnostic.observed_forward_sources
            )
        else:
            forward_text = "none"
        figure.suptitle(
            f"AG | {diagnostic.timestamp} | k=ln(K/F) | "
            f"forward_source={forward_text} | diagnostic-only; not used in formal warning",
            fontsize=12,
            y=0.965,
        )
        figure.subplots_adjust(
            left=0.06,
            right=0.98,
            bottom=0.10 if rows == 1 else 0.07,
            top=0.86 if rows == 1 else 0.89,
            wspace=0.26,
            hspace=0.34,
        )
        figure.savefig(
            Path(path),
            format="png",
            dpi=160,
            facecolor="white",
            edgecolor="white",
            metadata={"Software": "option-risk-total-variance-diagnostics-v1"},
        )
        figure.clear()


def _validate_created_staging(staging: Path, output: Path) -> Path:
    resolved_staging = staging.resolve(strict=True)
    resolved_parent = staging.parent.resolve(strict=True)
    output_parent = output.parent.resolve(strict=True)
    if (
        not stat.S_ISDIR(staging.lstat().st_mode)
        or _is_link_or_junction(staging)
        or not _paths_equal(resolved_parent, output_parent)
        or not _paths_equal(resolved_staging.parent, output_parent)
    ):
        raise ValueError("cache_boundary_violation: invalid staging directory")
    default_output = _lexical_absolute_path(
        _project_root() / "outputs" / "ag_total_variance_fit_diagnostics"
    )
    if _paths_equal(output, default_output):
        if re.fullmatch(
            r"\.ag_total_variance_fit_diagnostics\.staging-[a-z0-9_]+",
            staging.name,
        ) is None:
            raise ValueError("cache_boundary_violation: default staging name is invalid")
    else:
        _reject_write_root(resolved_staging, role="output", project=_project_root())
    return resolved_staging


def _directory_identity(path: Path, *, owner: str) -> tuple[int, int, int, int, int]:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise ValueError(f"cache_boundary_violation: {owner} is unavailable") from exc
    if not stat.S_ISDIR(metadata.st_mode) or _is_link_or_junction(path):
        raise ValueError(f"cache_boundary_violation: {owner} is not a real directory")
    return (
        int(metadata.st_dev),
        int(metadata.st_ino),
        int(metadata.st_mode),
        int(metadata.st_ctime_ns),
        int(getattr(metadata, "st_file_attributes", 0)),
    )


def _regular_file_identity(
    path: Path, *, owner: str
) -> tuple[int, int, int, int, int]:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise ValueError(f"cache_boundary_violation: {owner} is unavailable") from exc
    if not stat.S_ISREG(metadata.st_mode) or _is_link_or_junction(path):
        raise ValueError(f"cache_boundary_violation: {owner} is not a regular file")
    return (
        int(metadata.st_dev),
        int(metadata.st_ino),
        int(metadata.st_mode),
        int(metadata.st_ctime_ns),
        int(getattr(metadata, "st_file_attributes", 0)),
    )


def _staging_registry_key(path: str | Path) -> tuple[str, ...]:
    return _casefold_parts(_lexical_absolute_path(path))


def _create_staging_capability(output_dir: str | Path) -> _StagingCapability:
    requested_output = _lexical_absolute_path(output_dir)
    output = _resolve_path_safely(requested_output)
    project = _project_root()
    _reject_write_root(
        output,
        role="output",
        project=project,
        requested=requested_output,
    )
    parent = output.parent
    if not parent.exists() or not parent.is_dir() or _is_link_or_junction(parent):
        raise ValueError("cache_boundary_violation: staging parent must be a real directory")
    resolved_parent = parent.resolve(strict=True)
    if not _paths_equal(resolved_parent, parent):
        raise ValueError("cache_boundary_violation: staging parent changed before creation")
    parent_identity = _directory_identity(parent, owner="staging parent")
    output_identity = (
        _directory_identity(output, owner="artifact output")
        if output.exists()
        else None
    )
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=parent)
    )
    created_identity: tuple[int, int, int, int, int] | None = None
    try:
        if _directory_identity(parent, owner="staging parent") != parent_identity:
            raise ValueError(
                "cache_boundary_violation: staging parent identity changed during creation"
            )
        staging = _validate_created_staging(staging, output)
        created_identity = _directory_identity(staging, owner="staging directory")
        capability = _StagingCapability(
            token=secrets.token_hex(32),
            staging=staging,
            output_requested=requested_output,
            output_resolved=output,
            parent=parent,
            staging_identity=created_identity,
            parent_identity=parent_identity,
            output_identity=output_identity,
        )
        key = _staging_registry_key(staging)
        if key in _STAGING_CAPABILITIES:
            raise ValueError("cache_boundary_violation: duplicate staging capability")
        _STAGING_CAPABILITIES[key] = capability
        return capability
    except Exception:
        if created_identity is not None:
            try:
                if (
                    _directory_identity(parent, owner="staging parent")
                    == parent_identity
                    and _directory_identity(staging, owner="staging directory")
                    == created_identity
                ):
                    staging.rmdir()
            except (FileNotFoundError, OSError, ValueError):
                pass
        raise


def _assert_staging_capability_identity(
    capability: _StagingCapability,
    *,
    allowed_states: frozenset[str] = frozenset({"active", "publishing"}),
) -> None:
    if (
        not isinstance(capability, _StagingCapability)
        or capability.state not in allowed_states
    ):
        raise ValueError("cache_boundary_violation: staging capability is expired")
    current_output = _resolve_path_safely(capability.output_requested)
    _reject_write_root(
        current_output,
        role="output",
        project=_project_root(),
        requested=capability.output_requested,
    )
    if (
        not _paths_equal(current_output, capability.output_resolved)
        or _directory_identity(capability.parent, owner="staging parent")
        != capability.parent_identity
        or _directory_identity(capability.staging, owner="staging directory")
        != capability.staging_identity
    ):
        raise ValueError(
            "cache_boundary_violation: staging capability path/identity changed"
        )
    if capability.output_identity is None:
        if os.path.lexists(capability.output_resolved):
            raise ValueError(
                "cache_boundary_violation: artifact output appeared unexpectedly"
            )
    elif (
        _directory_identity(capability.output_resolved, owner="artifact output")
        != capability.output_identity
    ):
        raise ValueError("cache_boundary_violation: artifact output identity changed")


def _claim_staging_capability(
    staging_dir: str | Path,
    output_dir: str | Path,
) -> tuple[_StagingCapability, Path, Path]:
    staging_requested = _lexical_absolute_path(staging_dir)
    key = _staging_registry_key(staging_requested)
    capability = _STAGING_CAPABILITIES.get(key)
    if capability is None or capability.state != "active":
        raise ValueError("cache_boundary_violation: staging capability is absent or expired")
    capability.state = "publishing"
    try:
        requested_output = _lexical_absolute_path(output_dir)
        output = _resolve_path_safely(requested_output)
        if (
            requested_output != capability.output_requested
            or not _paths_equal(output, capability.output_resolved)
            or not _paths_equal(staging_requested, capability.staging)
        ):
            raise ValueError(
                "cache_boundary_violation: staging capability output/identity mismatch"
            )
        _assert_staging_capability_identity(
            capability, allowed_states=frozenset({"publishing"})
        )
        staging = _validate_created_staging(staging_requested, output)
        if not _paths_equal(staging, capability.staging):
            raise ValueError("cache_boundary_violation: staging capability path changed")
        return capability, staging, output
    except Exception:
        capability.state = "failed"
        if _STAGING_CAPABILITIES.get(key) is capability:
            del _STAGING_CAPABILITIES[key]
        raise


def _finish_staging_capability(
    capability: _StagingCapability,
    *,
    state: Literal["published", "failed"],
) -> None:
    capability.state = state
    key = _staging_registry_key(capability.staging)
    if _STAGING_CAPABILITIES.get(key) is capability:
        del _STAGING_CAPABILITIES[key]


def _cleanup_staging(capability: _StagingCapability) -> None:
    if not isinstance(capability, _StagingCapability):
        raise ValueError("cache_boundary_violation: cleanup requires staging capability")
    key = _staging_registry_key(capability.staging)
    if _STAGING_CAPABILITIES.get(key) is capability:
        del _STAGING_CAPABILITIES[key]
    prior_state = capability.state
    capability.state = "revoked"
    if prior_state not in {"active", "published", "failed"}:
        raise ValueError("cache_boundary_violation: staging capability cannot be reused")
    if not os.path.lexists(capability.staging):
        return
    if (
        _directory_identity(capability.parent, owner="staging parent")
        != capability.parent_identity
        or _directory_identity(capability.staging, owner="staging directory")
        != capability.staging_identity
    ):
        raise ValueError(
            "cache_boundary_violation: staging capability identity changed before cleanup"
        )
    verified = _validate_created_staging(
        capability.staging, capability.output_resolved
    )
    if not _paths_equal(verified, capability.staging):
        raise ValueError("cache_boundary_violation: staging changed before cleanup")
    shutil.rmtree(verified)


def _write_complete_staging_bundle(
    capability: _StagingCapability,
    *,
    diagnostics: Sequence[TimestampSurfaceDiagnostic],
    profiles: Sequence[TimestampProfile],
    source_fingerprint: str,
    representative_timestamp: str,
    selected_additional_timestamps: Sequence[str],
    generated_at: str,
) -> None:
    _assert_staging_capability_identity(capability)
    staging = capability.staging
    values = _canonical_diagnostics(diagnostics)
    diagnostics_payload = _build_diagnostics_payload(
        values,
        source_fingerprint=source_fingerprint,
        representative_timestamp=representative_timestamp,
        selected_additional_timestamps=selected_additional_timestamps,
    )
    sampled_payload = _build_sampled_timestamps_payload(
        profiles,
        values,
        representative_timestamp=representative_timestamp,
        selected_additional_timestamps=selected_additional_timestamps,
        source_fingerprint=source_fingerprint,
    )
    batch = diagnostics_payload["batch_input_fingerprint"]
    summary = build_summary(
        values,
        representative_timestamp=representative_timestamp,
        batch_input_fingerprint=batch,
    )
    _assert_staging_capability_identity(capability)
    _write_canonical_json(diagnostics_payload, staging / "diagnostics.json")
    _assert_staging_capability_identity(capability)
    write_attempts_csv(values, staging / "attempts.csv")
    _assert_staging_capability_identity(capability)
    _write_canonical_json(summary, staging / "summary.json")
    _assert_staging_capability_identity(capability)
    write_sampled_timestamps(sampled_payload, staging / "sampled_timestamps.json")
    representative = next(
        item
        for item in values
        if item.timestamp == _canonical_timestamp(representative_timestamp)
    )
    _assert_staging_capability_identity(capability)
    plot_representative_comparison(
        representative, staging / "ag_20250407_101500_iv_fit_comparison.png"
    )
    _assert_staging_capability_identity(capability)
    _write_artifact_manifest(
        staging,
        source_fingerprint=source_fingerprint,
        batch_input_fingerprint=batch,
        policy_version=values[0].policy_version,
        generated_at=generated_at,
    )
    _assert_staging_capability_identity(capability)


def run_ag_fit_diagnostics(
    *,
    data_dir: str | Path,
    cache_dir: str | Path,
    output_dir: str | Path,
    representative_timestamp: str,
    sample_count: int,
    force: bool = False,
) -> int:
    """Run the isolated AG diagnostic and apply the closed 0/1/2/3 matrix."""

    staging_capability: _StagingCapability | None = None
    output: Path | None = None
    try:
        if (
            _canonical_timestamp(representative_timestamp) != _REPRESENTATIVE_TIMESTAMP
            or isinstance(sample_count, bool)
            or sample_count != _REQUESTED_SAMPLE_COUNT
            or type(force) is not bool
        ):
            return 1
        paths = _validate_runtime_paths(data_dir, cache_dir, output_dir)
        output = paths.output_dir
        if output.exists():
            _validate_existing_output_names(output)
            if not force:
                return 1

        policy = FitPolicy()
        loaded = _load_ag_input(paths.data_dir, policy=policy)
        profile_by_timestamp = {profile.timestamp: profile for profile in loaded.profiles}
        if _REPRESENTATIVE_TIMESTAMP not in profile_by_timestamp:
            nearest = _nearest_profile_timestamp(
                loaded.profiles, _REPRESENTATIVE_TIMESTAMP
            )
            print(
                "representative_timestamp_missing: "
                f"requested={_REPRESENTATIVE_TIMESTAMP}, nearest={nearest}"
            )
            return 2
        selected = select_stratified_timestamps(
            loaded.profiles,
            representative_timestamp=_REPRESENTATIVE_TIMESTAMP,
            sample_count=_REQUESTED_SAMPLE_COUNT,
        )
        requested = sorted([_REPRESENTATIVE_TIMESTAMP, *selected])
        diagnostics: list[TimestampSurfaceDiagnostic] = []
        for timestamp in requested:
            profile = profile_by_timestamp[timestamp]
            timestamp_value = pd.Timestamp(timestamp)
            frame = loaded.nodes.loc[
                loaded.nodes["datetime"].eq(timestamp_value), list(_AG_ADAPTER_COLUMNS)
            ].copy(deep=True)

            def builder(
                frame: pd.DataFrame = frame,
                timestamp: str = timestamp,
            ) -> TimestampSurfaceDiagnostic:
                return diagnose_timestamp(
                    frame,
                    product="ag",
                    timestamp=timestamp,
                    policy=policy,
                )

            diagnostic, _ = _cached_timestamp_diagnostic(
                paths.cache_dir,
                source_fingerprint=loaded.source_fingerprint,
                input_fingerprint=profile.input_fingerprint,
                policy=policy,
                product="ag",
                timestamp=timestamp,
                builder=builder,
                _output_dir=paths.output_dir,
            )
            diagnostics.append(diagnostic)

        current_output = _resolve_path_safely(output)
        _reject_write_root(
            current_output,
            role="output",
            project=_project_root(),
            requested=output,
        )
        if not _paths_equal(current_output, output):
            raise ValueError("cache_boundary_violation: output path changed")
        output.parent.mkdir(parents=True, exist_ok=True)
        if not _paths_equal(output.parent.resolve(strict=True), output.parent):
            raise ValueError("cache_boundary_violation: output parent changed")
        staging_capability = _create_staging_capability(output)
        _write_complete_staging_bundle(
            staging_capability,
            diagnostics=diagnostics,
            profiles=loaded.profiles,
            source_fingerprint=loaded.source_fingerprint,
            representative_timestamp=_REPRESENTATIVE_TIMESTAMP,
            selected_additional_timestamps=selected,
            generated_at=_utc_now_text(),
        )
        _assert_staging_capability_identity(staging_capability)
        validate_artifact_bundle(staging_capability.staging)
        _assert_staging_capability_identity(staging_capability)
        publish_artifact_bundle(staging_capability.staging, output, force=force)
        validate_artifact_bundle(output)
        representative = next(
            item for item in diagnostics if item.timestamp == _REPRESENTATIVE_TIMESTAMP
        )
        if representative.timestamp_status is TimestampStatus.FAILED_INPUT:
            return 1
        if representative.usable_expiry_count == 0:
            return 3
        return 0
    except (OSError, ValueError, TypeError, KeyError):
        return 1
    finally:
        if staging_capability is not None:
            try:
                _cleanup_staging(staging_capability)
            except (OSError, ValueError):
                pass


__all__ = [
    "AgDiagnosticInput",
    "ARTIFACT_FILENAMES",
    "ATTEMPTS_CSV_COLUMNS",
    "EffectiveInputNode",
    "PreparedExpiryNodes",
    "PreparedTimestampNodes",
    "TimestampProfile",
    "build_summary",
    "decode_timestamp_diagnostic",
    "diagnose_timestamp",
    "plot_representative_comparison",
    "prepare_timestamp_nodes",
    "publish_artifact_bundle",
    "run_ag_fit_diagnostics",
    "select_stratified_timestamps",
    "write_attempts_csv",
    "write_sampled_timestamps",
    "validate_artifact_bundle",
    "validate_timestamp_diagnostic",
]
````

</details>
