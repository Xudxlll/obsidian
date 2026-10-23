---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py>)

SHA-256：`9a56e5bde12f9eb7fe62fff195594dcceb84fc9c04b0b8e56126df0588b0ad5a`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from dataclasses import replace
import re

import pytest

from graph_fixtures import graph_context, make_feature_evidence
from option_risk.decision import DecisionPolicy
from option_risk.graph_explanation import (
    UnsafeGraphExplanationError,
    render_graph_explanation,
    validate_explanation_language,
)
from option_risk.graph_reasoner import discover_risk_paths
from option_risk.knowledge_graph import (
    KnowledgeGraphValidationError,
    build_knowledge_graph,
    graph_from_node_link,
    graph_to_node_link,
)


SECTION_IDS = (
    "conclusion",
    "root_evidence",
    "propagation",
    "consequences",
    "limitations",
)
SECTION_TITLES = (
    "当前结论",
    "直接数据根因",
    "风险传导过程",
    "可能后果",
    "可信度与限制",
)


def _scenario(
    evidence,
    *,
    alert_level=2,
    alert_name="警告",
    transition_reason="normal",
    price_source="real_futures",
):
    context = graph_context(alert_level=alert_level, alert_name=alert_name)
    context.update(
        transition_reason=transition_reason,
        price_source=price_source,
    )
    graph = build_knowledge_graph(
        **context,
        evidence=evidence,
        policy=DecisionPolicy(),
    )
    return graph, discover_risk_paths(graph)


def _assert_five_sections(sections, text):
    assert isinstance(sections, list)
    assert tuple(section.section_id for section in sections) == SECTION_IDS
    assert tuple(section.title for section in sections) == SECTION_TITLES
    assert all(section.content.strip() for section in sections)
    assert all(section.content in text for section in sections)


def _assert_sentence_traceability(section):
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[。！？])\s*|\n+", section.content)
        if sentence.strip()
    ]
    found = []
    for sentence in sentences:
        match = re.match(r"^\[(path:[^\]]+)\]", sentence)
        assert match is not None, sentence
        if match.group(1) not in found:
            found.append(match.group(1))
    assert section.path_ids == tuple(found)


def test_level_zero_without_active_paths_keeps_all_sections_nonempty_and_untraced():
    graph, paths = _scenario(
        [make_feature_evidence("atm_iv", 0.5)],
        alert_level=0,
        alert_name="无预警",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    assert paths == []
    assert all(section.path_ids == () for section in sections)
    assert "AG" in sections[0].content
    assert "2025-04-07 10:15:00" in sections[0].content
    assert "0—3：无预警" in sections[0].content
    assert "0.5" in sections[0].content
    assert "normal" in sections[0].content
    assert "WarningState" in sections[0].content and "问题一" in sections[0].content
    assert confidence == "normal"


def test_near_threshold_watch_uses_dynamic_threshold_wording_and_values():
    graph, paths = _scenario(
        [make_feature_evidence("atm_iv", 0.95)],
        alert_level=1,
        alert_name="关注",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    root = sections[1]
    assert root.path_ids == (paths[0].path_id,)
    assert root.content.startswith(f"[{paths[0].path_id}]")
    assert "ATM隐含波动率" in root.content
    assert "当前值 0.2" in root.content
    assert "动态历史参考/阈值 0.210526" in root.content
    assert "压力比 0.95" in root.content
    assert "上升" in root.content
    assert "已接近自身动态阈值" in root.content
    assert "为该判断提供支持" in sections[2].content
    assert confidence == "normal"


def test_watch_held_without_active_path_describes_persistence_not_current_anomaly():
    graph, paths = _scenario(
        [make_feature_evidence("atm_iv", 0.5)],
        alert_level=1,
        alert_name="关注",
        transition_reason="watch_held",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    assert paths == []
    assert all(section.path_ids == () for section in sections)
    assert "当前市场特征已回落" in text
    assert "问题一持续性机制暂时保留" in text
    assert "当前异常" not in text
    assert confidence == "normal"


def test_watch_held_with_quality_only_path_still_describes_market_feature_fallback():
    graph, paths = _scenario(
        [make_feature_evidence("coverage_shortfall", 1.4)],
        alert_level=1,
        alert_name="关注",
        transition_reason="watch_held",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    assert paths
    assert all(path.conclusion_node_id.startswith("confidence:") for path in paths)
    assert "当前市场特征已回落" in sections[0].content
    assert "问题一持续性机制暂时保留" in sections[0].content
    assert "当前市场异常" not in text
    assert "质量路径仅降低解释置信度" in sections[4].content
    assert confidence == "limited"


def test_level_two_renders_three_unique_roots_and_relation_wording():
    graph, paths = _scenario(
        [
            make_feature_evidence("atm_iv", 1.15),
            make_feature_evidence("term_inversion", 1.33),
            make_feature_evidence("gamma_hhi", 1.29),
        ]
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    assert len(sections[1].path_ids) == 3
    assert len(set(sections[1].path_ids)) == 3
    assert text.count("当前值 0.2") == 3
    assert "超过自身动态阈值" in text
    assert "可能放大" in text
    assert "可能带来" in text
    assert confidence == "normal"


def test_level_three_core_plus_multiple_signals_preserves_formal_warning_state():
    graph, paths = _scenario(
        [
            make_feature_evidence("atm_iv", 1.6),
            make_feature_evidence("term_inversion", 1.2),
            make_feature_evidence("gamma_hhi", 1.2),
        ],
        alert_level=3,
        alert_name="危险",
        transition_reason="danger_core_plus_multiple",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    assert "0—3：危险" in sections[0].content
    assert "danger_core_plus_multiple" in sections[0].content
    assert "WarningState" in sections[0].content
    assert "图谱不改变" in sections[0].content
    assert confidence == "normal"


def test_quality_only_path_lowers_confidence_without_raising_market_alert():
    graph, paths = _scenario(
        [make_feature_evidence("coverage_shortfall", 1.4)],
        alert_level=0,
        alert_name="无预警",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    assert "0—3：无预警" in sections[0].content
    assert "降低当前分析置信度" in sections[2].content
    assert "仅降低解释置信度" in sections[4].content
    assert "不代表0—3市场预警等级上调" in sections[4].content
    assert confidence == "limited"


def test_reconstructed_price_is_explicitly_limited_as_a_non_market_proxy():
    graph, paths = _scenario(
        [make_feature_evidence("atm_iv", 1.15)],
        price_source="reconstructed_proxy",
    )

    sections, text, confidence = render_graph_explanation(graph, paths)

    _assert_five_sections(sections, text)
    limitation = sections[4].content
    assert "行权价/moneyness重构价格代理" in limitation
    assert "不是真实期货市场数据" in limitation
    assert "正式使用时应替换" in limitation
    assert confidence == "normal"


def test_root_propagation_and_consequence_sentences_are_exactly_traceable():
    graph, paths = _scenario(
        [
            make_feature_evidence("term_inversion", 1.2),
            make_feature_evidence("gamma_hhi", 1.3),
            make_feature_evidence("coverage_shortfall", 1.4),
        ]
    )

    sections, _, _ = render_graph_explanation(graph, paths)

    for section in sections[1:4]:
        _assert_sentence_traceability(section)
        assert set(section.path_ids).issubset({path.path_id for path in paths})


@pytest.mark.parametrize(
    "mutation",
    ["unknown", "duplicate", "reordered", "truncated", "field_tampered"],
)
def test_renderer_rejects_any_noncanonical_path_sequence(mutation):
    graph, paths = _scenario(
        [make_feature_evidence("atm_iv", 1.15), make_feature_evidence("gamma_hhi", 1.3)]
    )
    supplied = list(paths)
    if mutation == "unknown":
        supplied[0] = replace(supplied[0], path_id="path:unknown")
    elif mutation == "duplicate":
        supplied.insert(1, supplied[0])
    elif mutation == "reordered":
        supplied[0], supplied[1] = supplied[1], supplied[0]
    elif mutation == "truncated":
        supplied.pop()
    else:
        supplied[0] = replace(supplied[0], pressure_ratio=99.0)

    with pytest.raises(KnowledgeGraphValidationError):
        render_graph_explanation(graph, supplied)


def test_renderer_validates_graph_before_rendering():
    graph, paths = _scenario([make_feature_evidence("atm_iv", 1.15)])
    graph.nodes[paths[0].evidence_node_id]["label"] = "未注册标签"

    with pytest.raises(KnowledgeGraphValidationError):
        render_graph_explanation(graph, paths)


def test_renderer_is_deterministic_and_does_not_mutate_inputs():
    graph, paths = _scenario(
        [make_feature_evidence("atm_iv", 1.15), make_feature_evidence("gamma_hhi", 1.3)]
    )
    before_nodes = list(graph.nodes(data=True))
    before_paths = list(paths)

    first = render_graph_explanation(graph, paths)
    second = render_graph_explanation(graph, paths)

    assert first == second
    assert list(graph.nodes(data=True)) == before_nodes
    assert paths == before_paths


def test_multi_quality_reason_order_survives_node_link_round_trip():
    graph, paths = _scenario(
        [
            make_feature_evidence("coverage_shortfall", 1.4),
            make_feature_evidence("iv_floor_share", 1.3),
        ],
        alert_level=0,
        alert_name="无预警",
    )
    restored = graph_from_node_link(graph_to_node_link(graph))
    restored_paths = discover_risk_paths(restored)

    original = render_graph_explanation(graph, paths)
    round_tripped = render_graph_explanation(restored, restored_paths)

    assert original == round_tripped
    limitations = original[0][4].content
    assert limitations.index("IV求解下限占比") < limitations.index("曲面节点覆盖缺口")


@pytest.mark.parametrize(
    "phrase",
    [
        "建议买入",
        "建议卖出",
        "建议做多",
        "建议做空",
        "一定上涨",
        "一定下跌",
        "必然导致",
        "可以买入",
        "应当做空",
        "确保上涨",
        "建议做 多",
        "建议开多仓",
        "建议平空仓",
        "BUY now",
        "Go LONG",
        "sell-now",
        "go_short",
        "B\u200bUY now",
        "B.U.Y now",
        "Open a LONG position",
        "Take a short position",
        "not not BUY",
        "并非不建议买入",
        "Do not BUY or SELL",
        "Do not BUY now; SELL now",
        "不建议买入但建议卖出",
        "不提供买入建议但建议卖出",
        "g.o LONG now",
        "o.p.e.n a LONG position",
        "t-a-k-e a SHORT position",
        "e_n_t_e_r a SHORT position",
        "SHORT this futures contract",
        "Do not BUY now; g.o LONG now",
        "不建议买入；o.p.e.n a SHORT position",
        "not not SHORT this futures contract",
        "not not LONG now",
        "Please SHORT this futures contract",
        "Do not BUY now; not not SHORT this futures contract",
        "This is not a BUY recommendation; please LONG this futures contract",
        "Do not BUY now but SHORT this futures contract",
        "Never SELL and LONG now",
        "不建议买入但 SHORT this futures contract",
        "Do not g.o LONG now but SHORT this futures contract",
    ],
)
def test_language_validator_rejects_unsupported_or_trading_language(phrase):
    with pytest.raises(UnsafeGraphExplanationError):
        validate_explanation_language(phrase)


@pytest.mark.parametrize(
    "text",
    [
        "不提供交易建议。",
        "不建议买入。",
        "不要卖出。",
        "不建议开多仓。",
        "Do not BUY now.",
        "Never go SHORT based on this explanation.",
        "Don't BUY based on this explanation",
        "不提供买入或卖出建议",
        "No BUY or SELL recommendation is provided",
        "This is not a BUY recommendation",
        "long-term risk is discussed",
        "a short-term window",
        "long-term market risk is discussed",
        "long-term futures volatility is discussed",
        "short-term contract risk is monitored",
        "short-term underlying trend is discussed",
        "long market history is analyzed",
        "short contract maturities are observed",
        "Do not SHORT this futures contract",
        "Never LONG now",
        "Do not BUY now but long-term futures volatility is discussed",
        "Never SELL and a short-term window is monitored",
        "不建议买入但 long market history is analyzed",
        "不建议买入然后 short contract maturities are observed",
        "不预测标的价格涨跌方向。",
        "这不是已证实的新闻或政策原因。",
        "Gamma敏感性集中可能放大相关风险。",
    ],
)
def test_language_validator_allows_approved_cautious_or_negative_wording(text):
    assert validate_explanation_language(text) is None


@pytest.mark.parametrize("value", [None, 3, b"text"])
def test_language_validator_requires_a_string(value):
    with pytest.raises(TypeError):
        validate_explanation_language(value)


@pytest.mark.parametrize("trigger", ["go", "open", "take", "enter"])
@pytest.mark.parametrize("side", ["long", "short"])
@pytest.mark.parametrize("separator", [".", "_", "\u200b"])
def test_language_validator_rejects_uniformly_obfuscated_position_grammar(
    trigger, side, separator
):
    obfuscated_trigger = separator.join(trigger)
    obfuscated_side = separator.join(side)
    phrase = f"{obfuscated_trigger} {obfuscated_side} position"

    with pytest.raises(UnsafeGraphExplanationError):
        validate_explanation_language(phrase)


@pytest.mark.parametrize("conjunction", ["but", "and", "then"])
@pytest.mark.parametrize(
    "bare_action", ["LONG now", "SHORT this futures contract"]
)
def test_language_validator_rejects_positive_bare_action_after_english_negative(
    conjunction, bare_action
):
    phrase = f"Do not BUY now {conjunction} {bare_action}"

    with pytest.raises(UnsafeGraphExplanationError):
        validate_explanation_language(phrase)


@pytest.mark.parametrize("conjunction", ["但", "但是", "然后"])
@pytest.mark.parametrize(
    "bare_action", ["LONG now", "SHORT this futures contract"]
)
def test_language_validator_rejects_positive_bare_action_after_chinese_negative(
    conjunction, bare_action
):
    phrase = f"不建议买入{conjunction}{bare_action}"

    with pytest.raises(UnsafeGraphExplanationError):
        validate_explanation_language(phrase)
````

</details>
