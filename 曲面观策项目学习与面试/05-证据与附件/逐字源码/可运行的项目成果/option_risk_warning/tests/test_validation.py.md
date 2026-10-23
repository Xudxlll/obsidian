---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_validation.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py>)

SHA-256：`847c0ae0166cb75fb1d7acf844f35ad90cbf91f3127ca6d6937a522eb550236a`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import replace
import inspect

import numpy as np
import pandas as pd
import pytest

from option_risk.contracts import (
    AgentResult,
    FeatureEvidence,
    ProductOption,
    SurfacePayload,
    TriggerReason,
)
from option_risk.validation import (
    validate_agent_result,
    validate_deployment,
    validate_public_agent_surface,
)


GROUPS = {
    "曲面水平与形态",
    "期限结构",
    "无套利风险",
    "Greeks集中风险",
    "质量与流动性",
}
POLICY_VERSION = "validated-dynamic-state-v2"
POLICY_HASH = "df74c842c88bc54a54d0f57a40aa704cfcb7177bcd39297525de45dee69dd5d3"


def _result(groups: set[str] = GROUPS) -> AgentResult:
    timestamp = pd.Timestamp("2025-04-30 15:00")
    surfaces = {
        metric: SurfacePayload(
            metric=metric,
            timestamp=timestamp,
            log_moneyness=np.array([-0.1, 0.0, 0.1]),
            time_to_expiry=np.array([20 / 365, 50 / 365]),
            values=np.ones((2, 3)),
        )
        for metric in ["iv", "delta", "gamma", "vega", "theta"]
    }
    evidence = [
        FeatureEvidence(
            group=group,
            feature_name=f"feature_{number}",
            label=group,
            current_value=0.2,
            reference_value=0.3,
            pressure_ratio=2 / 3,
            change_rate=0.01,
            status="无预警",
        )
        for number, group in enumerate(sorted(groups))
    ]
    return AgentResult(
        product="ag",
        timestamp=timestamp,
        status="ready",
        alert_level=0,
        alert_name="无预警",
        alert_emitted=False,
        risk_score=0.5,
        price_source="reconstructed_proxy",
        data_quality={"clean_rate": 0.9},
        surfaces=surfaces,
        feature_evidence=evidence,
        trigger_reasons=[
            TriggerReason(
                feature_name="core_risk_pressure",
                label="综合核心风险压力",
                current_value=0.5,
                reference_value=1.0,
                pressure_ratio=0.5,
                change_direction="持平",
                severity=0,
                message="未达到关注阈值",
            )
        ],
        timeline=pd.DataFrame(
            {
                "alert_level": [0, 0],
                "alert_emitted": [False, False],
                "policy_version": [POLICY_VERSION, POLICY_VERSION],
                "policy_parameter_hash": [POLICY_HASH, POLICY_HASH],
                "transition_reason": ["normal", "normal"],
            },
            index=pd.to_datetime(["2025-04-30 14:45", "2025-04-30 15:00"]),
        ),
        evaluation=None,
        policy_version=POLICY_VERSION,
        policy_parameter_hash=POLICY_HASH,
        transition_reason="normal",
    )


def test_public_surface_exposes_exactly_one_business_agent() -> None:
    summary = validate_public_agent_surface()

    assert summary["agent_classes"] == ["OptionRiskAgent"]
    assert summary["passed"] is True


def test_result_validator_enforces_all_problem_one_outputs() -> None:
    summary = validate_agent_result(_result(), "ag", pd.Timestamp("2025-04-30 15:00"))

    assert summary["surface_metrics"] == ["delta", "gamma", "iv", "theta", "vega"]
    assert set(summary["feature_groups"]) == GROUPS
    assert summary["alert_level"] == 0
    assert summary["alert_emitted"] is False
    assert summary["policy_version"] == POLICY_VERSION
    assert summary["policy_parameter_hash"] == POLICY_HASH
    assert summary["transition_reason"] == "normal"


def test_result_validator_rejects_missing_fifth_feature_group() -> None:
    with pytest.raises(AssertionError, match="质量与流动性"):
        validate_agent_result(
            _result(GROUPS - {"质量与流动性"}),
            "ag",
            pd.Timestamp("2025-04-30 15:00"),
        )


def test_result_validator_rejects_timeline_level_different_from_current_alert() -> None:
    result = _result()
    timeline = result.timeline.copy()
    timeline.iloc[-1, timeline.columns.get_loc("alert_level")] = 2

    with pytest.raises(AssertionError, match="时间轴末行预警等级"):
        validate_agent_result(
            replace(result, timeline=timeline),
            "ag",
            pd.Timestamp("2025-04-30 15:00"),
        )


def test_result_validator_rejects_timeline_emission_different_from_current_result() -> None:
    result = _result()
    timeline = result.timeline.copy()
    timeline.loc[timeline.index[-1], "alert_emitted"] = True

    with pytest.raises(AssertionError, match="新发通知"):
        validate_agent_result(
            replace(result, timeline=timeline),
            "ag",
            pd.Timestamp("2025-04-30 15:00"),
        )


@pytest.mark.parametrize(
    ("column", "value", "message"),
    [
        ("policy_version", "legacy-policy-v0", "策略版本"),
        ("policy_parameter_hash", "different-hash", "策略参数哈希"),
        ("transition_reason", "watch_started", "迁移原因"),
    ],
)
def test_result_validator_rejects_timeline_identity_different_from_current(
    column: str,
    value: str,
    message: str,
) -> None:
    result = _result()
    timeline = result.timeline.copy()
    timeline.loc[timeline.index[-1], column] = value

    with pytest.raises(AssertionError, match=message):
        validate_agent_result(
            replace(result, timeline=timeline),
            "ag",
            pd.Timestamp("2025-04-30 15:00"),
        )


def _expected_problem_one_summary() -> dict:
    return {
        "product": "ag",
        "timestamp": "2025-04-30T15:00:00",
        "status": "ready",
        "alert_level": 0,
        "alert_name": "无预警",
        "alert_emitted": False,
        "surface_metrics": ["delta", "gamma", "iv", "theta", "vega"],
        "feature_groups": [
            "Greeks集中风险",
            "无套利风险",
            "曲面水平与形态",
            "期限结构",
            "质量与流动性",
        ],
        "evidence_count": 5,
        "reason_count": 1,
        "timeline_rows": 2,
        "price_source": "reconstructed_proxy",
        "evaluation_available": False,
        "policy_version": POLICY_VERSION,
        "policy_parameter_hash": POLICY_HASH,
        "transition_reason": "normal",
    }


def test_problem_one_validation_public_signatures_remain_exact() -> None:
    """Catches Problem 2 weakening or renaming the existing Problem 1 API."""
    assert str(inspect.signature(validate_agent_result)) == (
        "(result: 'AgentResult', requested_product: 'str', "
        "requested_timestamp: 'pd.Timestamp') -> 'dict[str, Any]'"
    )
    assert str(inspect.signature(validate_deployment)) == (
        "(agent: 'OptionRiskAgent', *, analyze: 'bool' = True, "
        "product_codes: 'list[str] | None' = None, "
        "progress: 'Callable[[str], None] | None' = None) -> 'dict[str, Any]'"
    )


def test_problem_one_result_summary_keys_and_values_remain_exact() -> None:
    """Catches Problem 2 changing any established Problem 1 summary field."""
    assert validate_agent_result(
        _result(),
        "ag",
        pd.Timestamp("2025-04-30 15:00"),
    ) == _expected_problem_one_summary()


def test_problem_one_result_identity_error_message_remains_exact() -> None:
    """Catches Problem 2 changing the established identity failure semantics."""
    with pytest.raises(AssertionError) as captured:
        validate_agent_result(
            _result(),
            "cu",
            pd.Timestamp("2025-04-30 15:00"),
        )

    assert str(captured.value) == "返回品种'ag'与请求'cu'不一致"


class _ProblemOneValidationAgent:
    def __init__(self) -> None:
        self.timestamp_calls: list[str] = []
        self.analyze_calls: list[tuple[str, pd.Timestamp]] = []

    def list_products(self):
        return [ProductOption(code="ag", label="AG")]

    def list_timestamps(self, product: str):
        self.timestamp_calls.append(product)
        return pd.DatetimeIndex(["2025-04-30 14:45", "2025-04-30 15:00"])

    def analyze(self, product: str, timestamp: pd.Timestamp):
        self.analyze_calls.append((product, pd.Timestamp(timestamp)))
        return _result()


def test_problem_one_deployment_report_contract_remains_exact() -> None:
    """Catches the new deployment validator mutating the old report contract."""
    agent = _ProblemOneValidationAgent()
    progress: list[str] = []

    report = validate_deployment(agent, progress=progress.append)

    assert set(report) == {
        "generated_at",
        "mode",
        "public_agent_surface",
        "summary",
        "products",
    }
    assert pd.Timestamp(report["generated_at"]).tzinfo is not None
    assert report["mode"] == "full"
    assert report["public_agent_surface"] == {
        "agent_classes": ["OptionRiskAgent"],
        "passed": True,
    }
    assert report["summary"] == {
        "status": "passed",
        "product_count": 1,
        "passed_products": 1,
        "failed_products": 0,
    }
    assert report["products"] == [
        {
            "product": "ag",
            "status": "passed",
            "timestamp_count": 2,
            "first_timestamp": "2025-04-30T14:45:00",
            "last_timestamp": "2025-04-30T15:00:00",
            "analysis": _expected_problem_one_summary(),
        }
    ]
    assert agent.timestamp_calls == ["ag"]
    assert agent.analyze_calls == [("ag", pd.Timestamp("2025-04-30 15:00"))]
    assert progress == ["[1/1] ag: passed"]


def test_problem_one_deployment_unknown_product_error_remains_exact() -> None:
    """Catches Problem 2 changing old continuation rows or progress errors."""
    agent = _ProblemOneValidationAgent()
    progress: list[str] = []

    report = validate_deployment(
        agent,
        product_codes=["xx"],
        progress=progress.append,
    )

    assert report["products"] == [
        {
            "product": "xx",
            "status": "failed",
            "error_type": "AssertionError",
            "error": "数据目录不存在品种：xx",
        }
    ]
    assert report["summary"] == {
        "status": "failed",
        "product_count": 1,
        "passed_products": 0,
        "failed_products": 1,
    }
    assert agent.timestamp_calls == []
    assert agent.analyze_calls == []
    assert progress == ["[1/1] xx: failed - 数据目录不存在品种：xx"]
````

</details>
