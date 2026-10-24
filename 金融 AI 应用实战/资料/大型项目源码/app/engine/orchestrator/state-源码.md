---
type: 原始源码副本
---

来源：`app/engine/orchestrator/state.py`。原始完整文件，未修改代码。

```python
from typing import Any, Dict, List, Optional, TypedDict

import logging

logger = logging.getLogger("orchestrator.state")

class BullBearRound(TypedDict, total=False):

    bull: str
    bear: str

class RiskRound(TypedDict, total=False):

    risky: str
    safe: str
    neutral: str

class InvestmentDebateState(TypedDict, total=False):

    rounds: List[BullBearRound]
    count: int
    max_rounds: int
    judge_decision: str

class RiskDebateState(TypedDict, total=False):

    rounds: List[RiskRound]
    count: int
    max_rounds: int
    latest_speaker: str
    judge_decision: str

class NodeError(TypedDict):

    node: str
    phase: str
    error: str
    ts: float
    duration_ms: int
    retried: bool

class PipelineState(TypedDict, total=False):
    messages: List[Any]
    company_of_interest: str
    trade_date: str
    task_id: Optional[str]
    user_id: str
    investment_debate_state: InvestmentDebateState
    risk_debate_state: RiskDebateState
    reports: Dict[str, str]
    trader_investment_plan: str
    investment_plan: str
    final_trade_decision: str
    node_timings: Dict[str, float]
    errors: List[NodeError]

_INV_SIDE_ARGS = {
    "bull": ("多头分析师", "bull_history", "bull_report_content"),
    "bear": ("空头分析师", "bear_history", "bear_report_content"),
}
_INV_SIDE_ORDER = ("bull", "bear")
_INV_SECTION_TITLES = {
    "bull": ("## 初始报告：核心投资论点", "## 第 {round} 轮辩论报告：针对空方观点的反驳与辩护"),
    "bear": ("## 初始报告：核心风险警示", "## 第 {round} 轮辩论报告：针对多方观点的质疑与反驳"),
}

_RISK_SIDE_ARGS = {
    "risky": ("激进派", "risky_history", "risky_report_content", "current_risky_response"),
    "safe": ("保守派", "safe_history", "safe_report_content", "current_safe_response"),
    "neutral": ("中性派", "neutral_history", "neutral_report_content", "current_neutral_response"),
}
_RISK_SIDE_ORDER = ("risky", "safe", "neutral")
_RISK_SECTION_TITLES = {
    "risky": ("## 初始观点：激进策略", "## 第 {round} 轮辩论：激进派反驳"),
    "safe": ("## 初始观点：保守策略", "## 第 {round} 轮辩论：保守派反驳"),
    "neutral": ("## 初始观点：中性策略", "## 第 {round} 轮辩论：中性派观点"),
}

def current_round_index(ds: Dict[str, Any], per_turn: int) -> int:

    return ds.get("count", 0) // per_turn

def append_round(ds: Dict[str, Any], side_key: str, content: str, per_turn: int) -> None:

    rounds: List[Dict[str, Any]] = ds.setdefault("rounds", [])
    idx = current_round_index(ds, per_turn)
    while idx >= len(rounds):
        rounds.append({})
    rounds[idx][side_key] = content
    ds["count"] = ds.get("count", 0) + 1

def _argument(side_key: str, arg_tag: str, round_idx: int, content: str) -> str:
    prefix = (
        f"# 【{arg_tag} - 初始报告】"
        if round_idx == 0
        else f"# 【{arg_tag} - 第 {round_idx} 轮辩论】"
    )
    return f"{prefix}\n{content}"

def _iter_rounds(ds: Dict[str, Any]) -> List[Dict[str, Any]]:
    return ds.get("rounds") or []

def _side_contents(ds: Dict[str, Any], side_key: str) -> List[str]:
    return [r.get(side_key) for r in _iter_rounds(ds) if r.get(side_key)]

def _side_argument(side_args: Dict, side_key: str, ds: Dict[str, Any]) -> List[str]:
    arg_tag = side_args[side_key][0]
    out = []
    for i, r in enumerate(_iter_rounds(ds)):
        content = r.get(side_key)
        if content:
            out.append(_argument(side_key, arg_tag, i, content))
    return out

def _history_from(ds: Dict[str, Any], side_order, side_args) -> str:
    parts: List[str] = []
    for side_key in side_order:
        parts.extend(_side_argument(side_args, side_key, ds))
    return "".join(("\n" + p if parts else p) for p in parts) if parts else ""

def _report_content_from(section_titles: Dict, side_key: str, ds: Dict[str, Any]) -> str:
    initial_title, debate_title = section_titles[side_key]
    parts: List[str] = []
    for i, content in enumerate(_side_contents(ds, side_key)):
        title = initial_title if i == 0 else debate_title.format(round=i)
        parts.append(f"\n\n{title}\n\n{content}")
    return "".join(parts)

def _latest_content(ds: Dict[str, Any], side_key: str) -> str:
    contents = _side_contents(ds, side_key)
    return contents[-1] if contents else ""

def investment_history(ds: Optional[Dict[str, Any]]) -> str:
    if not ds:
        return ""
    legacy = ds.get("history")
    if legacy is not None and not ds.get("rounds"):
        return legacy
    return _history_from(ds, _INV_SIDE_ORDER, _INV_SIDE_ARGS)

def investment_side_history(ds: Optional[Dict[str, Any]], side: str) -> str:
    if not ds:
        return ""
    legacy = ds.get(_INV_SIDE_ARGS[side][1])
    if legacy is not None and not ds.get("rounds"):
        return legacy
    parts = _side_argument(_INV_SIDE_ARGS, side, ds)
    return "".join(("\n" + p if i else p) for i, p in enumerate(parts))

def investment_report_content(ds: Optional[Dict[str, Any]], side: str) -> str:
    if not ds:
        return ""
    legacy = ds.get(_INV_SIDE_ARGS[side][2])
    if legacy is not None and not ds.get("rounds"):
        return legacy
    return _report_content_from(_INV_SECTION_TITLES, side, ds)

def investment_current_response(ds: Optional[Dict[str, Any]]) -> str:
    if not ds:
        return ""
    if not ds.get("rounds"):
        return ds.get("current_response", "")
    for side in reversed(_INV_SIDE_ORDER):
        c = _latest_content(ds, side)
        if c:
            return c
    return ds.get("judge_decision", "")

def risk_history(ds: Optional[Dict[str, Any]]) -> str:
    if not ds:
        return ""
    legacy = ds.get("history")
    if legacy is not None and not ds.get("rounds"):
        return legacy
    return _history_from(ds, _RISK_SIDE_ORDER, _RISK_SIDE_ARGS)

def risk_side_history(ds: Optional[Dict[str, Any]], side: str) -> str:
    if not ds:
        return ""
    legacy = ds.get(_RISK_SIDE_ARGS[side][1])
    if legacy is not None and not ds.get("rounds"):
        return legacy
    parts = _side_argument(_RISK_SIDE_ARGS, side, ds)
    return "".join(("\n" + p if i else p) for i, p in enumerate(parts))

def risk_report_content(ds: Optional[Dict[str, Any]], side: str) -> str:
    if not ds:
        return ""
    legacy = ds.get(_RISK_SIDE_ARGS[side][2])
    if legacy is not None and not ds.get("rounds"):
        return legacy
    return _report_content_from(_RISK_SECTION_TITLES, side, ds)

def risk_current_response(ds: Optional[Dict[str, Any]], side: str) -> str:
    if not ds:
        return ""
    if not ds.get("rounds"):
        return ds.get(_RISK_SIDE_ARGS[side][3], "")
    return _latest_content(ds, side)

def create_initial_state(
    company_name: str,
    trade_date: str,
    task_id: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    from app.llm.core.types import Message, Role

    task_description = f"请对股票 {company_name} 进行全面分析，交易日期：{trade_date}"

    state: Dict[str, Any] = {
        "messages": [Message(role=Role.USER, content=task_description)],
        "company_of_interest": company_name,
        "trade_date": str(trade_date),
        "task_id": task_id,
        "user_id": user_id or "",
        "investment_debate_state": InvestmentDebateState(
            rounds=[], count=0, max_rounds=2, judge_decision=""
        ),
        "risk_debate_state": RiskDebateState(
            rounds=[], count=0, max_rounds=3, latest_speaker="", judge_decision=""
        ),
        "reports": {},
        "errors": [],
        "trader_investment_plan": "",
        "investment_plan": "",
        "final_trade_decision": "",
    }

    try:
        from app.engine.agents.analysts.dynamic_analyst import DynamicAnalystFactory

        for agent in DynamicAnalystFactory.get_all_agents():
            slug = agent.get("slug", "")
            if not slug:
                continue
            internal_key = slug.replace("-analyst", "").replace("-", "_")
            report_key = f"{internal_key}_report"
            if report_key not in state:
                state[report_key] = ""
    except Exception as e:
        logger.warning(f"⚠️ 动态初始化智能体字段失败: {e}")

    return state

def export_legacy_state(state: Dict[str, Any]) -> Dict[str, Any]:

    out = dict(state)

    ids = state.get("investment_debate_state") or {}
    if isinstance(ids, dict):
        legacy_ids = dict(ids)
        if ids.get("rounds"):
            legacy_ids.update({
                "history": investment_history(ids),
                "current_response": investment_current_response(ids),
                "current_round_index": current_round_index(ids, 2),
                "bull_history": investment_side_history(ids, "bull"),
                "bear_history": investment_side_history(ids, "bear"),
                "bull_report_content": investment_report_content(ids, "bull"),
                "bear_report_content": investment_report_content(ids, "bear"),
            })
        else:
            legacy_ids.setdefault("history", "")
            legacy_ids.setdefault("current_response", "")
            legacy_ids.setdefault("current_round_index", 0)
            legacy_ids.setdefault("bull_history", "")
            legacy_ids.setdefault("bear_history", "")
            legacy_ids.setdefault("bull_report_content", "")
            legacy_ids.setdefault("bear_report_content", "")
        legacy_ids.setdefault("count", 0)
        legacy_ids.setdefault("max_rounds", 2)
        legacy_ids.setdefault("judge_decision", "")
        legacy_ids.setdefault("rounds", [])
        out["investment_debate_state"] = legacy_ids

    rds = state.get("risk_debate_state") or {}
    if isinstance(rds, dict):
        legacy_rds = dict(rds)
        if rds.get("rounds"):
            legacy_rds.update({
                "history": risk_history(rds),
                "current_round_index": current_round_index(rds, 3),
                **{
                    _RISK_SIDE_ARGS[s][3]: risk_current_response(rds, s)
                    for s in _RISK_SIDE_ORDER
                },
                **{
                    _RISK_SIDE_ARGS[s][1]: risk_side_history(rds, s)
                    for s in _RISK_SIDE_ORDER
                },
                **{
                    _RISK_SIDE_ARGS[s][2]: risk_report_content(rds, s)
                    for s in _RISK_SIDE_ORDER
                },
            })
        else:
            for side in _RISK_SIDE_ORDER:
                _, hk, rk, ck = _RISK_SIDE_ARGS[side]
                legacy_rds.setdefault(hk, "")
                legacy_rds.setdefault(rk, "")
                legacy_rds.setdefault(ck, "")
            legacy_rds.setdefault("history", "")
            legacy_rds.setdefault("current_round_index", 0)
        legacy_rds.setdefault("count", 0)
        legacy_rds.setdefault("max_rounds", 3)
        legacy_rds.setdefault("latest_speaker", "")
        legacy_rds.setdefault("judge_decision", "")
        legacy_rds.setdefault("rounds", [])
        out["risk_debate_state"] = legacy_rds

    return out

```
