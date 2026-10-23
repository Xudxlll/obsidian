---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/knowledge_schema.py>)

SHA-256：`22176876c5ac3c3391e491d836eb6f622f92b90f8aaa75594bfe03e6ad82cd34`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re
from typing import Iterable

from .decision import PRESSURE_SPECS


KG_SCHEMA_VERSION = "kg-schema-v1"
KG_RULE_VERSION = "kg-rule-v1"


class NodeType(StrEnum):
    PRODUCT = "Product"
    RISK_SNAPSHOT = "RiskSnapshot"
    EVIDENCE = "Evidence"
    ANOMALY = "Anomaly"
    MECHANISM = "Mechanism"
    RISK_CONSEQUENCE = "RiskConsequence"
    WARNING_STATE = "WarningState"
    CONFIDENCE_STATE = "ConfidenceState"


class RelationType(StrEnum):
    HAS_SNAPSHOT = "HAS_SNAPSHOT"
    HAS_EVIDENCE = "HAS_EVIDENCE"
    NEAR_THRESHOLD = "NEAR_THRESHOLD"
    EXCEEDS = "EXCEEDS"
    VIOLATES = "VIOLATES"
    SUPPORTS = "SUPPORTS"
    MAY_AMPLIFY = "MAY_AMPLIFY"
    MAY_LEAD_TO = "MAY_LEAD_TO"
    REDUCES_CONFIDENCE = "REDUCES_CONFIDENCE"


@dataclass(frozen=True, slots=True)
class FeatureRule:
    """Stable, non-causal mapping from one decision feature to graph layers."""

    order: int
    rule_id: str
    feature_name: str
    evidence_group: str
    label: str
    evidence_code: str
    anomaly_code: str
    anomaly: str
    mechanism_code: str
    mechanism: str
    conclusion_code: str
    conclusion: str
    conclusion_type: NodeType
    boundary: str
    evidence_relation_options: tuple[RelationType, ...]
    relation_types: tuple[RelationType, RelationType]


def _rule(
    order: int,
    feature_name: str,
    anomaly: str,
    mechanism: str,
    conclusion: str,
    conclusion_type: NodeType,
    boundary: str,
) -> FeatureRule:
    group, expected_feature, label = next(
        spec for spec in PRESSURE_SPECS.values() if spec[1] == feature_name
    )
    assert expected_feature == feature_name
    quality = group == "质量与流动性"
    violation_feature = feature_name in {
        "convexity_violation_ratio",
        "calendar_variance_violation_ratio",
    }
    may_amplify = feature_name in {"gamma_hhi", "vega_hhi"}
    return FeatureRule(
        order=order,
        rule_id=f"{KG_RULE_VERSION}:{feature_name}",
        feature_name=feature_name,
        evidence_group=group,
        label=label,
        evidence_code=f"evidence_{feature_name}",
        anomaly_code=f"anomaly_{feature_name}",
        anomaly=anomaly,
        mechanism_code=f"mechanism_{feature_name}",
        mechanism=mechanism,
        conclusion_code=(
            f"confidence_{feature_name}" if quality else f"risk_consequence_{feature_name}"
        ),
        conclusion=conclusion,
        conclusion_type=conclusion_type,
        boundary=boundary,
        evidence_relation_options=(
            RelationType.NEAR_THRESHOLD,
            RelationType.EXCEEDS,
            *((RelationType.VIOLATES,) if violation_feature else ()),
        ),
        relation_types=(
            RelationType.SUPPORTS,
            (
                RelationType.REDUCES_CONFIDENCE
                if quality
                else RelationType.MAY_AMPLIFY
                if may_amplify
                else RelationType.MAY_LEAD_TO
            ),
        ),
    )


FEATURE_RULES: tuple[FeatureRule, ...] = (
    _rule(1, "atm_iv", "ATM IV异常抬升", "波动率整体重定价", "短期波动风险上升", NodeType.RISK_CONSEQUENCE, "不预测标的涨跌"),
    _rule(2, "atm_iv_chg_4", "ATM IV短时变化异常", "波动率重定价加速", "短时波动敏感性上升", NodeType.RISK_CONSEQUENCE, "不断言外部事件原因"),
    _rule(3, "term_inversion", "期限结构倒挂", "近端风险压力集中", "短期波动风险上升", NodeType.RISK_CONSEQUENCE, "不等同于某条新闻导致"),
    _rule(4, "convexity_violation_ratio", "执行价凸性违反异常", "曲面定价一致性下降", "估值一致性风险", NodeType.RISK_CONSEQUENCE, "不声称存在可执行套利"),
    _rule(5, "max_local_iv_jump", "局部IV跳变", "曲面局部稳定性下降", "曲面估值稳定性风险", NodeType.RISK_CONSEQUENCE, "需结合覆盖和流动性理解"),
    _rule(6, "put_call_parity_p95_error", "Put-Call平价偏离异常", "相对定价一致性下降", "估值一致性风险", NodeType.RISK_CONSEQUENCE, "不声称存在可执行套利"),
    _rule(7, "calendar_variance_violation_ratio", "日历总方差约束违反", "期限方向定价一致性下降", "估值一致性风险", NodeType.RISK_CONSEQUENCE, "不等同于确定套利机会"),
    _rule(8, "gamma_hhi", "Gamma集中异常", "非线性敏感性集中", "Gamma敏感性风险增强", NodeType.RISK_CONSEQUENCE, "使用“可能放大”，不提仓位建议"),
    _rule(9, "vega_hhi", "Vega集中异常", "波动率敏感性集中", "Vega敏感性风险增强", NodeType.RISK_CONSEQUENCE, "使用“可能放大”，不提仓位建议"),
    _rule(10, "zero_volume_share", "零成交合约占比异常", "市场活跃度/可观测性受限", "解释置信度降低", NodeType.CONFIDENCE_STATE, "不支持市场风险等级上调"),
    _rule(11, "iv_floor_share", "IV求解下限占比异常", "IV反解可用性受限", "解释置信度降低", NodeType.CONFIDENCE_STATE, "不支持市场风险等级上调"),
    _rule(12, "coverage_shortfall", "曲面节点覆盖不足", "曲面分析可靠性受限", "解释置信度降低", NodeType.CONFIDENCE_STATE, "不支持市场风险等级上调"),
)


def _as_node_type(value: object) -> NodeType:
    try:
        return NodeType(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Unknown node type: {value!r}") from error


def _as_relation_type(value: object) -> RelationType:
    try:
        return RelationType(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Unknown relation type: {value!r}") from error


def validate_schema(rules: Iterable[FeatureRule] | None = None) -> None:
    """Reject schema drift before any graph-building task can consume the registry."""
    rows = tuple(FEATURE_RULES if rules is None else rules)
    expected = tuple(spec[1] for spec in PRESSURE_SPECS.values())
    feature_names = tuple(rule.feature_name for rule in rows)
    if feature_names != expected:
        raise ValueError("Feature rules must match PRESSURE_SPECS exactly and in canonical order")
    if len(set(feature_names)) != len(feature_names):
        raise ValueError("Feature rules contain duplicate features")
    if tuple(rule.order for rule in rows) != tuple(range(1, len(expected) + 1)):
        raise ValueError("Feature rule orders must be the unique canonical sequence")
    for rule in rows:
        expected_group, _, expected_label = next(
            spec for spec in PRESSURE_SPECS.values() if spec[1] == rule.feature_name
        )
        if rule.evidence_group != expected_group:
            raise ValueError("Feature rule evidence group must match PRESSURE_SPECS")
        if rule.label != expected_label:
            raise ValueError("Feature rule label must match PRESSURE_SPECS")
        if rule.rule_id != f"{KG_RULE_VERSION}:{rule.feature_name}":
            raise ValueError("Feature rule ID must be deterministic and versioned")
        expected_codes = (
            f"evidence_{rule.feature_name}",
            f"anomaly_{rule.feature_name}",
            f"mechanism_{rule.feature_name}",
            (
                f"confidence_{rule.feature_name}"
                if rule.conclusion_type == NodeType.CONFIDENCE_STATE
                else f"risk_consequence_{rule.feature_name}"
            ),
        )
        actual_codes = (
            rule.evidence_code,
            rule.anomaly_code,
            rule.mechanism_code,
            rule.conclusion_code,
        )
        if actual_codes != expected_codes:
            raise ValueError("Feature rule layer codes must be deterministic")
        if any(re.fullmatch(r"[a-z][a-z0-9_]*", code) is None for code in actual_codes):
            raise ValueError("Feature rule layer codes must be ASCII snake_case")
        conclusion_type = _as_node_type(rule.conclusion_type)
        evidence_options = tuple(
            _as_relation_type(value) for value in rule.evidence_relation_options
        )
        relation_types = tuple(_as_relation_type(value) for value in rule.relation_types)
        violation_feature = rule.feature_name in {
            "convexity_violation_ratio",
            "calendar_variance_violation_ratio",
        }
        expected_evidence_options = (
            RelationType.NEAR_THRESHOLD,
            RelationType.EXCEEDS,
            *((RelationType.VIOLATES,) if violation_feature else ()),
        )
        if evidence_options != expected_evidence_options:
            raise ValueError("Evidence relation options must support dynamic threshold selection")
        if len(relation_types) != 2 or relation_types[0] is not RelationType.SUPPORTS:
            raise ValueError("Feature rules must retain only static propagation relations")
        if rule.evidence_group == "质量与流动性":
            if conclusion_type is not NodeType.CONFIDENCE_STATE:
                raise ValueError("Quality rules may only end in ConfidenceState")
            if relation_types[-1] is not RelationType.REDUCES_CONFIDENCE:
                raise ValueError("Quality rules must reduce confidence")
        else:
            if conclusion_type is not NodeType.RISK_CONSEQUENCE:
                raise ValueError("Market rules must end in RiskConsequence")
            expected_terminal_relation = (
                RelationType.MAY_AMPLIFY
                if rule.feature_name in {"gamma_hhi", "vega_hhi"}
                else RelationType.MAY_LEAD_TO
            )
            if relation_types[-1] is not expected_terminal_relation:
                raise ValueError("Market propagation relation does not match the feature semantics")


validate_schema()
````

</details>
