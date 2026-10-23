---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/graph_explanation.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/graph_explanation.py>)

SHA-256：`ad3456f3e1d45e95a26ab32312c25b107ab082e7230c68688e033a1b6d206561`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

from collections.abc import Sequence
import math
import re
from typing import Any
import unicodedata

import networkx as nx

from .contracts import ExplanationSection, RiskPath
from .graph_reasoner import discover_risk_paths
from .knowledge_graph import KnowledgeGraphValidationError, validate_knowledge_graph
from .knowledge_schema import NodeType, RelationType


class UnsafeGraphExplanationError(ValueError):
    """Raised when an explanation contains unsupported causal or trading claims."""


_SECTION_SPECS = (
    ("conclusion", "当前结论"),
    ("root_evidence", "直接数据根因"),
    ("propagation", "风险传导过程"),
    ("consequences", "可能后果"),
    ("limitations", "可信度与限制"),
)
_RELATION_WORDING = {
    RelationType.NEAR_THRESHOLD.value: "已接近自身动态阈值",
    RelationType.EXCEEDS.value: "超过自身动态阈值",
    RelationType.VIOLATES.value: "当前数据出现相应约束违反",
    RelationType.SUPPORTS.value: "为该判断提供支持",
    RelationType.MAY_AMPLIFY.value: "可能放大",
    RelationType.MAY_LEAD_TO.value: "可能带来",
    RelationType.REDUCES_CONFIDENCE.value: "降低当前分析置信度",
}
_CHINESE_TRADE_ACTION = r"(?:买入|卖出|做多|做空|开多仓|开空仓|平多仓|平空仓)"
_CHINESE_TRADE_ACTION_RE = re.compile(_CHINESE_TRADE_ACTION)
_CHINESE_SINGLE_NEGATIVE = re.compile(
    rf"(?:不建议|不应当|不应|不要|无需|请勿){_CHINESE_TRADE_ACTION}"
)
_CHINESE_NO_RECOMMENDATION = re.compile(
    r"(?:本说明)?不提供(?:买入|卖出)"
    r"(?:(?:或|和|以及)(?:买入|卖出))*建议"
)
_CHINESE_DOUBLE_NEGATIVE = re.compile(r"(?:并非不|不是不|不得不|不能不|未尝不)")
_CHINESE_UNSAFE_PATTERNS = (
    re.compile(r"(?:一定|必定|保证|确保|肯定)(?:会)?(?:上涨|下跌|上升|下降)"),
    re.compile(r"(?:必然|一定|必定)(?:.{0,8})(?:导致|造成|引发)"),
)
_ENGLISH_TRIGGERED_ACTION_GRAMMAR = (
    r"(?:\b(?:buy|sell)\b|"
    r"\b(?:go|open|take|enter)\s+(?:an?\s+)?"
    r"(?:long|short)(?:\s+position)?\b)"
)
_ENGLISH_TRIGGERED_TRADE = re.compile(_ENGLISH_TRIGGERED_ACTION_GRAMMAR)
_ENGLISH_SINGLE_NEGATIVE = re.compile(
    rf"^(?:please\s+)?(?:do\s+not|never|not)\s+"
    rf"{_ENGLISH_TRIGGERED_ACTION_GRAMMAR}(?:\s+.*)?$"
)
_ENGLISH_NO_RECOMMENDATION = re.compile(
    r"^no\s+(?:buy|sell)(?:\s+(?:or|and)\s+(?:buy|sell))*\s+"
    r"recommendation(?:\s+is\s+provided)?$"
)
_ENGLISH_NOT_A_RECOMMENDATION = re.compile(
    r"^(?:this\s+is\s+)?not\s+(?:an?\s+)?(?:buy|sell)\s+"
    r"recommendation(?:\s+is\s+provided)?$"
)
_ENGLISH_DOUBLE_NEGATIVE = re.compile(
    r"\b(?:not|never|no)\s+(?:not|never|no)\b"
)
_ENGLISH_BARE_CONTINUATION = (
    r"(?:now\b|immediately\b|"
    r"(?:this|that|these|those)\s+"
    r"(?:futures?|contracts?|assets?|underlying|market)"
    r"(?:\s+(?:futures?|contracts?|assets?))?\b)"
)
_ENGLISH_BARE_ACTION = (
    rf"(?P<action>(?:long|short)\s+{_ENGLISH_BARE_CONTINUATION})"
)
_ENGLISH_BARE_BOUNDARY = r"(?:^|(?:\b(?:but|and|then)\b|但是|但|然后)\s*)"
_ENGLISH_BARE_SCANNER = re.compile(
    rf"{_ENGLISH_BARE_BOUNDARY}"
    rf"(?P<prefix>(?:(?:please|do\s+not|never|not)\s+)*)"
    rf"{_ENGLISH_BARE_ACTION}"
)
_ENGLISH_NEGATED_BARE_PREFIX = re.compile(
    r"^(?:please\s+)?(?:do\s+not|never|not)\s+$"
)
_ENGLISH_TRADE_LEXEMES = (
    "buy",
    "sell",
    "long",
    "short",
    "go",
    "open",
    "take",
    "enter",
)
_CLAUSE_SPLIT = re.compile(r"[\r\n.!?。！？;；,，]+")
_SENTENCE_SPLIT = re.compile(r"(?<=[。！？])\s*|\n+")
_LEADING_PATH_ID = re.compile(r"^\[(path:[^\]]+)\]")


def _normalize_language_clauses(text: str) -> tuple[str, ...]:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    normalized = "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Cf"
    )
    normalized = re.sub(r"\bdon['’]t\b", "do not", normalized)
    for word in _ENGLISH_TRADE_LEXEMES:
        letters = r"[\W_]*".join(re.escape(character) for character in word)
        normalized = re.sub(
            rf"(?<![a-z]){letters}(?![a-z])",
            word,
            normalized,
        )
    normalized = re.sub(
        r"\b(?:long|short)[\-‐-―]term\b",
        "durationadjective",
        normalized,
    )
    clauses: list[str] = []
    for raw_clause in _CLAUSE_SPLIT.split(normalized):
        clause = re.sub(r"[\W_]+", " ", raw_clause, flags=re.UNICODE).strip()
        clause = re.sub(r"\s+", " ", clause)
        if clause:
            clauses.append(clause)
    return tuple(clauses)


def _english_clause_is_safe(
    clause: str,
    *,
    triggered_action_count: int,
    bare_actions: Sequence[re.Match[str]],
) -> bool:
    action_count = triggered_action_count + len(bare_actions)
    if (
        action_count == 1
        and bare_actions
        and _ENGLISH_NEGATED_BARE_PREFIX.fullmatch(bare_actions[0].group("prefix"))
    ):
        return True
    if (
        action_count == 1
        and not bare_actions
        and _ENGLISH_SINGLE_NEGATIVE.fullmatch(clause)
    ):
        return True
    if _ENGLISH_NO_RECOMMENDATION.fullmatch(clause):
        return True
    return _ENGLISH_NOT_A_RECOMMENDATION.fullmatch(clause) is not None


def _chinese_clause_is_safe(compact: str, action_count: int) -> bool:
    if action_count == 1 and _CHINESE_SINGLE_NEGATIVE.search(compact):
        return True
    return _CHINESE_NO_RECOMMENDATION.fullmatch(compact) is not None


def validate_explanation_language(text: str) -> None:
    """Apply finite template-safety grammar to explanation text."""
    if not isinstance(text, str):
        raise TypeError("explanation text must be a string")
    for clause in _normalize_language_clauses(text):
        compact = re.sub(r"\s+", "", clause)
        for pattern in _CHINESE_UNSAFE_PATTERNS:
            match = pattern.search(compact)
            if match is not None:
                raise UnsafeGraphExplanationError(
                    f"Unsafe graph-explanation wording: {match.group(0)!r}"
                )

        triggered_actions = tuple(_ENGLISH_TRIGGERED_TRADE.finditer(clause))
        bare_actions = tuple(_ENGLISH_BARE_SCANNER.finditer(clause))
        chinese_actions = tuple(_CHINESE_TRADE_ACTION_RE.finditer(compact))
        total_action_count = (
            len(triggered_actions) + len(bare_actions) + len(chinese_actions)
        )
        if total_action_count == 0:
            continue
        if (
            _ENGLISH_DOUBLE_NEGATIVE.search(clause) is not None
            or _CHINESE_DOUBLE_NEGATIVE.search(compact) is not None
        ):
            raise UnsafeGraphExplanationError(
                "Unsafe graph-explanation wording: double negation"
            )

        if total_action_count > 1:
            english_no_recommendation = (
                not bare_actions
                and not chinese_actions
                and _ENGLISH_NO_RECOMMENDATION.fullmatch(clause) is not None
            )
            chinese_no_recommendation = (
                not triggered_actions
                and not bare_actions
                and _CHINESE_NO_RECOMMENDATION.fullmatch(compact) is not None
            )
            if not english_no_recommendation and not chinese_no_recommendation:
                raise UnsafeGraphExplanationError(
                    "Unsafe graph-explanation wording: uncovered multiple actions"
                )
            continue

        if (triggered_actions or bare_actions) and not _english_clause_is_safe(
            clause,
            triggered_action_count=len(triggered_actions),
            bare_actions=bare_actions,
        ):
            unsafe_action = (
                triggered_actions[0].group(0)
                if triggered_actions
                else bare_actions[0].group("action")
            )
            raise UnsafeGraphExplanationError(
                f"Unsafe graph-explanation wording: {unsafe_action!r}"
            )
        if chinese_actions and not _chinese_clause_is_safe(
            compact, len(chinese_actions)
        ):
            raise UnsafeGraphExplanationError(
                f"Unsafe graph-explanation wording: {chinese_actions[0].group(0)!r}"
            )


def _one_node(graph: nx.MultiDiGraph, node_type: NodeType) -> tuple[str, dict[str, Any]]:
    matches = [
        (str(node_id), data)
        for node_id, data in graph.nodes(data=True)
        if data["node_type"] == node_type.value
    ]
    if len(matches) != 1:
        raise KnowledgeGraphValidationError(
            f"Expected exactly one {node_type.value} node"
        )
    return matches[0]


def _stable_number(value: object) -> str:
    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    ):
        return format(float(value), ".6g")
    return "不可用"


def _timestamp_text(value: object) -> str:
    return str(value)


def _section(
    section_id: str,
    content: str,
    path_ids: Sequence[str] = (),
) -> ExplanationSection:
    title = dict(_SECTION_SPECS)[section_id]
    return ExplanationSection(
        section_id=section_id,
        title=title,
        content=content,
        path_ids=tuple(path_ids),
    )


def _conclusion_content(
    graph: nx.MultiDiGraph,
    *,
    active_paths: Sequence[RiskPath],
) -> str:
    _, product = _one_node(graph, NodeType.PRODUCT)
    _, snapshot = _one_node(graph, NodeType.RISK_SNAPSHOT)
    _, warning = _one_node(graph, NodeType.WARNING_STATE)
    content = (
        f"产品 {product['label']}，所选时间 { _timestamp_text(snapshot['timestamp']) }；"
        f"WarningState 为0—3：{warning['alert_name']}"
        f"（等级{warning['alert_level']}），风险分数 "
        f"{_stable_number(warning['risk_score'])}，状态转换原因 "
        f"{warning['transition_reason'] if warning['transition_reason'] is not None else '不可用'}。"
        "WarningState 由问题一直接复制，图谱不改变该状态。"
    )
    has_market_path = any(
        graph.nodes[path.conclusion_node_id]["node_type"]
        in {NodeType.WARNING_STATE.value, NodeType.RISK_CONSEQUENCE.value}
        for path in active_paths
    )
    if warning["transition_reason"] == "watch_held" and not has_market_path:
        content += "当前市场特征已回落，级别由问题一持续性机制暂时保留。"
    return content


def _root_section(
    graph: nx.MultiDiGraph,
    paths: Sequence[RiskPath],
) -> ExplanationSection:
    selected: list[RiskPath] = []
    seen_evidence: set[str] = set()
    for path in paths:
        if path.evidence_node_id in seen_evidence:
            continue
        seen_evidence.add(path.evidence_node_id)
        selected.append(path)
        if len(selected) == 3:
            break
    if not selected:
        return _section(
            "root_evidence",
            "所选事件图中没有达到活动路径条件的直接数据根因。",
        )

    sentences: list[str] = []
    for path in selected:
        evidence = graph.nodes[path.evidence_node_id]
        relation = _RELATION_WORDING[path.relation_semantics[0]]
        sentences.append(
            f"[{path.path_id}] {evidence['label']}：当前值 "
            f"{_stable_number(evidence['current_value'])}，动态历史参考/阈值 "
            f"{_stable_number(evidence['reference_value'])}，压力比 "
            f"{_stable_number(evidence['pressure_ratio'])}，方向 "
            f"{evidence['direction']}，{relation}。"
        )
    return _section(
        "root_evidence",
        "\n".join(sentences),
        [path.path_id for path in selected],
    )


def _propagation_section(
    graph: nx.MultiDiGraph,
    paths: Sequence[RiskPath],
) -> ExplanationSection:
    if not paths:
        return _section(
            "propagation",
            "当前没有活动风险路径，因此无可呈现的风险传导过程。",
        )
    sentences: list[str] = []
    for path in paths:
        nodes = (
            graph.nodes[path.evidence_node_id],
            graph.nodes[path.anomaly_node_id],
            graph.nodes[path.mechanism_node_id],
            graph.nodes[path.conclusion_node_id],
        )
        phrases = tuple(_RELATION_WORDING[value] for value in path.relation_semantics)
        sentences.append(
            f"[{path.path_id}] {nodes[0]['label']}{phrases[0]}{nodes[1]['label']}；"
            f"{nodes[1]['label']}{phrases[1]}{nodes[2]['label']}；"
            f"{nodes[2]['label']}{phrases[2]}{nodes[3]['label']}。"
        )
    return _section(
        "propagation",
        "\n".join(sentences),
        [path.path_id for path in paths],
    )


def _consequence_section(
    graph: nx.MultiDiGraph,
    paths: Sequence[RiskPath],
) -> ExplanationSection:
    consequence_paths = [
        path
        for path in paths
        if graph.nodes[path.conclusion_node_id]["node_type"]
        == NodeType.RISK_CONSEQUENCE.value
    ]
    if not consequence_paths:
        return _section(
            "consequences",
            "当前无已登记的非方向性市场风险后果；质量路径仅影响解释置信度。",
        )
    sentences = [
        f"[{path.path_id}] 图谱登记的可能后果为“"
        f"{graph.nodes[path.conclusion_node_id]['label']}”，仅表示非方向性风险。"
        for path in consequence_paths
    ]
    return _section(
        "consequences",
        "\n".join(sentences),
        [path.path_id for path in consequence_paths],
    )


def _limitations_content(graph: nx.MultiDiGraph) -> tuple[str, str]:
    _, snapshot = _one_node(graph, NodeType.RISK_SNAPSHOT)
    _, confidence = _one_node(graph, NodeType.CONFIDENCE_STATE)
    confidence_level = str(confidence["level"])
    lines = [
        "本说明不预测标的价格涨跌方向，也不提供交易建议。",
        "直接数据根因仅来自所选事件图，不是已证实的新闻、政策或行业原因。",
        f"所选证据时间戳为 {_timestamp_text(snapshot['timestamp'])}。",
    ]
    if confidence_level == "limited":
        labels_by_feature = {
            data["feature_name"]: data["label"]
            for _, data in graph.nodes(data=True)
            if data["node_type"] == NodeType.EVIDENCE.value
        }
        reasons = "、".join(
            labels_by_feature[feature_name]
            for feature_name in confidence["quality_reasons"]
        )
        lines.append(
            f"ConfidenceState 为 limited（解释置信度受限：{reasons}）；"
            "活动质量路径仅降低解释置信度，"
            "不代表0—3市场预警等级上调。"
        )
    else:
        lines.append("ConfidenceState 为 normal（解释置信度正常）。")
    if snapshot["price_source"] == "reconstructed_proxy":
        lines.append(
            "行权价/moneyness重构价格代理不是真实期货市场数据，"
            "正式使用时应替换为真实期货市场数据。"
        )
    return "".join(lines), "limited" if confidence_level == "limited" else "normal"


def _ordered_unique(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _validate_traceability(
    sections: Sequence[ExplanationSection],
    active_paths: Sequence[RiskPath],
) -> None:
    active_ids = {path.path_id for path in active_paths}
    for section in sections:
        if any(path_id not in active_ids for path_id in section.path_ids):
            raise KnowledgeGraphValidationError(
                "Explanation section references a path absent from active_paths"
            )
        if section.section_id not in {"root_evidence", "propagation", "consequences"}:
            continue
        sentences = [
            sentence.strip()
            for sentence in _SENTENCE_SPLIT.split(section.content)
            if sentence.strip()
        ]
        found: list[str] = []
        for sentence in sentences:
            match = _LEADING_PATH_ID.match(sentence)
            if match is None:
                if section.path_ids:
                    raise KnowledgeGraphValidationError(
                        "Every traced explanation sentence must begin with [path_id]"
                    )
                continue
            path_id = match.group(1)
            if path_id not in active_ids:
                raise KnowledgeGraphValidationError(
                    "Explanation sentence references a path absent from active_paths"
                )
            found.append(path_id)
        if section.path_ids != _ordered_unique(found):
            raise KnowledgeGraphValidationError(
                "Explanation section path_ids do not match its sentence prefixes"
            )


def render_graph_explanation(
    graph: nx.MultiDiGraph,
    paths: Sequence[RiskPath],
) -> tuple[list[ExplanationSection], str, str]:
    """Render five deterministic, graph-only, sentence-traceable sections."""
    validate_knowledge_graph(graph)
    canonical_paths = discover_risk_paths(graph)
    if isinstance(paths, (str, bytes)) or not isinstance(paths, Sequence):
        raise KnowledgeGraphValidationError("paths must be a sequence of RiskPath values")
    supplied_paths = list(paths)
    if supplied_paths != canonical_paths:
        raise KnowledgeGraphValidationError(
            "Supplied paths must equal the fresh canonical ranked paths exactly"
        )

    limitation_content, confidence_level = _limitations_content(graph)
    sections = [
        _section(
            "conclusion",
            _conclusion_content(graph, active_paths=canonical_paths),
        ),
        _root_section(graph, canonical_paths),
        _propagation_section(graph, canonical_paths),
        _consequence_section(graph, canonical_paths),
        _section("limitations", limitation_content),
    ]
    if tuple((section.section_id, section.title) for section in sections) != _SECTION_SPECS:
        raise KnowledgeGraphValidationError("Explanation sections do not match the contract")
    if any(not section.content.strip() for section in sections):
        raise KnowledgeGraphValidationError("Explanation sections must be non-empty")
    _validate_traceability(sections, canonical_paths)
    text = "\n\n".join(
        f"{section.title}\n{section.content}" for section in sections
    )
    validate_explanation_language(text)
    return sections, text, confidence_level


__all__ = [
    "UnsafeGraphExplanationError",
    "render_graph_explanation",
    "validate_explanation_language",
]
````

</details>
