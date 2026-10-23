---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_knowledge_schema.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_schema.py>)

SHA-256：`1a561db133032c7ec334e876f26ce3a948cf0b36a5bcbce20fc5c84a0ece8e6a`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import replace

import pytest

from option_risk.decision import PRESSURE_SPECS
from option_risk.knowledge_schema import (
    FEATURE_RULES,
    KG_RULE_VERSION,
    RelationType,
    validate_schema,
)


def test_schema_maps_exactly_the_canonical_twelve_features() -> None:
    """Catches a missing, added, or incorrectly mapped decision pressure feature."""
    assert {rule.feature_name for rule in FEATURE_RULES} == {
        spec[1] for spec in PRESSURE_SPECS.values()
    }
    assert len(FEATURE_RULES) == 12
    validate_schema()


def test_feature_rules_preserve_the_canonical_order_and_semantics() -> None:
    """Catches a graph rule that changes a prescribed anomaly-to-conclusion path."""
    expected = [
        ("atm_iv", "ATM IV异常抬升", "波动率整体重定价", "短期波动风险上升", "RiskConsequence", "不预测标的涨跌"),
        ("atm_iv_chg_4", "ATM IV短时变化异常", "波动率重定价加速", "短时波动敏感性上升", "RiskConsequence", "不断言外部事件原因"),
        ("term_inversion", "期限结构倒挂", "近端风险压力集中", "短期波动风险上升", "RiskConsequence", "不等同于某条新闻导致"),
        ("convexity_violation_ratio", "执行价凸性违反异常", "曲面定价一致性下降", "估值一致性风险", "RiskConsequence", "不声称存在可执行套利"),
        ("max_local_iv_jump", "局部IV跳变", "曲面局部稳定性下降", "曲面估值稳定性风险", "RiskConsequence", "需结合覆盖和流动性理解"),
        ("put_call_parity_p95_error", "Put-Call平价偏离异常", "相对定价一致性下降", "估值一致性风险", "RiskConsequence", "不声称存在可执行套利"),
        ("calendar_variance_violation_ratio", "日历总方差约束违反", "期限方向定价一致性下降", "估值一致性风险", "RiskConsequence", "不等同于确定套利机会"),
        ("gamma_hhi", "Gamma集中异常", "非线性敏感性集中", "Gamma敏感性风险增强", "RiskConsequence", "使用“可能放大”，不提仓位建议"),
        ("vega_hhi", "Vega集中异常", "波动率敏感性集中", "Vega敏感性风险增强", "RiskConsequence", "使用“可能放大”，不提仓位建议"),
        ("zero_volume_share", "零成交合约占比异常", "市场活跃度/可观测性受限", "解释置信度降低", "ConfidenceState", "不支持市场风险等级上调"),
        ("iv_floor_share", "IV求解下限占比异常", "IV反解可用性受限", "解释置信度降低", "ConfidenceState", "不支持市场风险等级上调"),
        ("coverage_shortfall", "曲面节点覆盖不足", "曲面分析可靠性受限", "解释置信度降低", "ConfidenceState", "不支持市场风险等级上调"),
    ]
    actual = [
        (
            rule.feature_name,
            rule.anomaly,
            rule.mechanism,
            rule.conclusion,
            rule.conclusion_type.value,
            rule.boundary,
        )
        for rule in FEATURE_RULES
    ]
    assert actual == expected
    assert all(rule.rule_id.startswith(f"{KG_RULE_VERSION}:") for rule in FEATURE_RULES)


def test_feature_rules_expose_the_explicit_canonical_order() -> None:
    """Catches a registry reordering that changes the canonical feature sequence."""
    assert [rule.order for rule in FEATURE_RULES] == list(range(1, 13))

    duplicate_order = replace(FEATURE_RULES[0], order=2)

    with pytest.raises(ValueError, match="orders"):
        validate_schema((duplicate_order, *FEATURE_RULES[1:]))


def test_first_edge_remains_dynamic_while_rules_define_allowed_relations() -> None:
    """Catches a rule hard-coding a threshold relation before Task 2 sees pressure."""
    violation_features = {
        "convexity_violation_ratio",
        "calendar_variance_violation_ratio",
    }
    for rule in FEATURE_RULES:
        assert rule.relation_types[0] is RelationType.SUPPORTS
        assert rule.evidence_relation_options[:2] == (
            RelationType.NEAR_THRESHOLD,
            RelationType.EXCEEDS,
        )
        assert (RelationType.VIOLATES in rule.evidence_relation_options) == (
            rule.feature_name in violation_features
        )

    assert next(
        rule for rule in FEATURE_RULES if rule.feature_name == "gamma_hhi"
    ).relation_types[-1] is RelationType.MAY_AMPLIFY
    assert next(
        rule for rule in FEATURE_RULES if rule.feature_name == "zero_volume_share"
    ).relation_types[-1] is RelationType.REDUCES_CONFIDENCE


@pytest.mark.parametrize(
    ("changed_field", "changed_value", "message"),
    [
        ("evidence_group", "错误分组", "evidence group"),
        ("label", "错误标签", "label"),
        ("rule_id", f"{KG_RULE_VERSION}:not_atm_iv", "deterministic"),
        ("evidence_code", "evidence_renamed", "deterministic"),
        ("anomaly_code", "anomaly_renamed", "deterministic"),
        ("mechanism_code", "mechanism_renamed", "deterministic"),
        ("conclusion_code", "conclusion_renamed", "deterministic"),
    ],
)
def test_schema_rejects_noncanonical_rule_identity_and_pressure_metadata(
    changed_field: str,
    changed_value: str,
    message: str,
) -> None:
    """Catches schema records that drift from the canonical decision contract."""
    changed = replace(FEATURE_RULES[0], **{changed_field: changed_value})

    with pytest.raises(ValueError, match=message):
        validate_schema((changed, *FEATURE_RULES[1:]))


def test_quality_rules_can_only_reduce_confidence() -> None:
    """Catches quality evidence being incorrectly promoted to market risk."""
    quality = [rule for rule in FEATURE_RULES if rule.evidence_group == "质量与流动性"]
    assert len(quality) == 3
    assert {rule.conclusion_type.value for rule in quality} == {"ConfidenceState"}
````

</details>
