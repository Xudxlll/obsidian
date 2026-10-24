---
type: 原始源码副本
---

来源：`app/engine/orchestrator/pipeline.py`。原始完整文件，未修改代码。

```python
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import logging

from .state import create_initial_state, export_legacy_state

_NODE_SLUG_MAP: Dict[str, str] = {
    "Bull Researcher": "bull-researcher",
    "Bear Researcher": "bear-researcher",
    "Research Manager": "research-manager",
    "Trader": "trader",
    "Risky Analyst": "risky-analyst",
    "Safe Analyst": "safe-analyst",
    "Neutral Analyst": "neutral-analyst",
    "Risk Judge": "risk-manager",
}
_NODE_DISPLAY_FALLBACK: Dict[str, str] = {
    "Summary Agent": "报告总结",
}
_NODE_EVENT_KEYS: Dict[str, str] = {
    "Bull Researcher": "researcher_bull",
    "Bear Researcher": "researcher_bear",
    "Research Manager": "research_manager",
    "Trader": "trader",
    "Risky Analyst": "risk_debater_risky",
    "Safe Analyst": "risk_debater_safe",
    "Neutral Analyst": "risk_debater_neutral",
    "Risk Judge": "risk_manager",
    "Summary Agent": "summary",
}
_NODE_DISPLAY_NAMES: Optional[Dict[str, str]] = None

def _resolve_display_names() -> Dict[str, str]:
    global _NODE_DISPLAY_NAMES
    if _NODE_DISPLAY_NAMES is None:
        from app.engine.agents.utils.agent_config import load_agent_display_name
        names = {}
        for node_name, slug in _NODE_SLUG_MAP.items():
            name = load_agent_display_name(slug)
            if name:
                names[node_name] = name
        names.update(_NODE_DISPLAY_FALLBACK)
        _NODE_DISPLAY_NAMES = names
    return _NODE_DISPLAY_NAMES

logger = logging.getLogger("orchestrator.pipeline")

MAX_ROUNDS = 10

@dataclass
class PipelineDeps:

    analyst_client: Any
    debate_client: Any
    toolkit: Any
    bull_memory: Any = None
    bear_memory: Any = None
    trader_memory: Any = None
    invest_judge_memory: Any = None
    risk_manager_memory: Any = None
    config: Dict[str, Any] = field(default_factory=dict)
    analyst_limit: Optional[int] = None
    analyst_limit_key: Optional[str] = None
    debate_limit: Optional[int] = None
    debate_limit_key: Optional[str] = None

def _format_analyst_node(internal_key: str) -> str:
    return internal_key.replace("_", " ").title().replace(" ", "_") + " Analyst"

def _merge_state_update(target: Dict[str, Any], update: Dict[str, Any]) -> None:
    if not update:
        return
    if "reports" in update and isinstance(update["reports"], dict):
        target["reports"] = {**(target.get("reports") or {}), **update["reports"]}
    if "messages" in update and isinstance(update["messages"], list):
        target.setdefault("messages", [])
        target["messages"].extend(update["messages"])
    for k, v in update.items():
        if k in ("reports", "messages"):
            continue
        target[k] = v

def _report_display_title(report_key: str, display_name: str = "") -> str:

    base = report_key[: -len("_report")] if report_key.endswith("_report") else report_key
    _SLUG_ALIAS = {
        "trader_investment_plan": "trader",
        "investment_plan": "trader",
        "final_trade_decision": "trader",
        "research_team_decision": "research-manager",
        "risk_management_decision": "risk-manager",
        "risk_manager_decision": "risk-manager",
    }
    title = ""
    try:
        from app.engine.agents.utils.agent_config import load_agent_display_name

        slug = _SLUG_ALIAS.get(base, base.replace("_", "-"))
        for candidate in (slug, f"{slug}-analyst"):
            title = load_agent_display_name(candidate)
            if title:
                break
    except Exception:
        title = ""
    return title or display_name or report_key

async def _emit_report_ready(
    event_sink: Optional[Any],
    update: Dict[str, Any],
    *,
    agent_key: str,
    phase: str,
    before_reports: Dict[str, Any],
    display_name: str = "",
) -> None:

    if event_sink is None:
        return
    try:
        from app.llm.events import REPORT_CONTENT_MAX_CHARS

        reports_update = (update or {}).get("reports")
        if not isinstance(reports_update, dict) or not reports_update:
            return
        for report_key, content in reports_update.items():
            if before_reports.get(report_key) == content:
                continue
            text = content if isinstance(content, str) else str(content)
            await event_sink.emit(
                "report_ready",
                agent_key=agent_key,
                phase=phase,
                report_key=report_key,
                title=_report_display_title(report_key, display_name),
                content=text[:REPORT_CONTENT_MAX_CHARS],
            )
    except Exception as e:
        logger.warning(f"⚠️ [orchestrator] report_ready 发射失败: {e}")

def _merge_debate_updates(
    st: Dict[str, Any],
    updates: List[Dict[str, Any]],
    *,
    state_key: str,
    side_keys: List[str],
    has_latest_speaker: bool = False,
) -> List[str]:

    from .state import current_round_index

    ds = st.setdefault(state_key, {})
    snapshot_count = int(ds.get("count", 0) or 0)
    snapshot_idx = current_round_index(ds, len(side_keys))
    succeeded: List[str] = []
    last_written: Optional[str] = None
    for side_key, update in zip(side_keys, updates):
        new_ds = (update or {}).get(state_key)
        content = None
        if isinstance(new_ds, dict):
            new_rounds = new_ds.get("rounds") or []
            if snapshot_idx < len(new_rounds):
                content = new_rounds[snapshot_idx].get(side_key)
        if content:
            rounds: List[Dict[str, Any]] = ds.setdefault("rounds", [])
            while snapshot_idx >= len(rounds):
                rounds.append({})
            rounds[snapshot_idx][side_key] = content
            succeeded.append(side_key)
            last_written = side_key
        _merge_state_update(st, {k: v for k, v in (update or {}).items() if k != state_key})
    ds["count"] = snapshot_count + len(succeeded)
    if has_latest_speaker and last_written is not None:
        ds["latest_speaker"] = last_written
    return succeeded

def _record_error(st: Dict[str, Any], node_name: str, error: str, start: float, *, retried: bool) -> None:
    st.setdefault("errors", []).append({
        "node": node_name,
        "phase": st.get("_phase", ""),
        "error": error,
        "ts": time.time(),
        "duration_ms": int((time.time() - start) * 1000),
        "retried": retried,
    })

def compute_total_units(
    num_analysts: int,
    *,
    phase2_enabled: bool,
    phase2_rounds: int,
    phase3_enabled: bool,
    phase3_rounds: int,
) -> int:
    units = max(num_analysts, 0)
    if phase2_enabled:
        units += 2 * (max(phase2_rounds, 0) + 1) + 1
    units += 1
    if phase3_enabled:
        units += 3 * (max(phase3_rounds, 0) + 1) + 1
    units += 1
    return units

def interpolate_percent(completed: int, total: int, lo: int, hi: int) -> int:
    if total <= 0 or completed <= 0:
        return lo
    if completed >= total:
        return hi
    return lo + round(completed / total * (hi - lo))

async def run_pipeline(
    deps: PipelineDeps,
    company_name: str,
    trade_date: str,
    selected_analysts: List[str],
    *,
    task_id: Optional[str] = None,
    progress_callback: Optional[Callable[[Any], None]] = None,
    event_sink: Optional[Any] = None,
    user_id: Optional[str] = None,
    progress_range: tuple = (0, 100),
) -> Dict[str, Any]:
    config = deps.config or {}
    phase2_enabled = bool(config.get("phase2_enabled", False))
    phase3_enabled = bool(config.get("phase3_enabled", False))
    debate_parallel = bool(config.get("debate_parallel", True))

    max_debate_rounds = config.get("phase2_debate_rounds")
    if max_debate_rounds is None:
        max_debate_rounds = config.get("max_debate_rounds", 1)
    max_debate_rounds = max(0, min(int(max_debate_rounds), MAX_ROUNDS))
    if not phase2_enabled:
        max_debate_rounds = 0

    max_risk_rounds = config.get("phase3_debate_rounds")
    if max_risk_rounds is None:
        max_risk_rounds = config.get("max_risk_discuss_rounds", 1)
    max_risk_rounds = max(0, min(int(max_risk_rounds), MAX_ROUNDS))
    if not phase3_enabled:
        max_risk_rounds = 0

    mcp_manager = None
    mcp_tools: List = []
    enable_mcp = bool(getattr(deps.toolkit, "enable_mcp", False))
    if enable_mcp:
        try:
            from app.llm.mcp.client import MCPManager
            from app.llm.mcp.tools import discover_mcp_tools

            mcp_manager = MCPManager()
            mcp_tools = await discover_mcp_tools(mcp_manager)
            selected_ids = config.get("mcp_tool_ids")
            if selected_ids:
                selected_set = set(selected_ids)
                mcp_tools = [t for t in mcp_tools if t.name in selected_set]
                logger.info(
                    f"🔧 [orchestrator] MCP 工具按选择过滤: {len(mcp_tools)}/{len(selected_set)} 个"
                )
            logger.info(f"🔧 [orchestrator] MCP 工具发现: {len(mcp_tools)} 个")
        except Exception as e:
            logger.warning(f"⚠️ [orchestrator] MCP 工具发现失败，跳过: {e}")
            if mcp_manager is not None:
                try:
                    await mcp_manager.close_all()
                except Exception as close_err:
                    logger.warning(f"⚠️ [orchestrator] MCP 会话关闭失败: {close_err}")
            mcp_manager = None
            mcp_tools = []

    node_timings: Dict[str, float] = {}

    completed_box = [0]
    total_units_box = [0]
    progress_lo, progress_hi = progress_range

    if event_sink is None and progress_callback is not None:
        from app.llm.events import EventSink

        event_sink = EventSink(task_id=task_id or "", on_progress=progress_callback)

    def _progress_text(node_name: str) -> str:
        try:
            from app.engine.agents.analysts.dynamic_analyst import DynamicAnalystFactory

            mapping = DynamicAnalystFactory.build_node_mapping()
            message = mapping.get(node_name)
            if message is None:
                return f"🔍 {node_name}"
            return message or f"🔍 {node_name}"
        except Exception as e:
            logger.warning(f"⚠️ [orchestrator] 进度文案解析失败: {e}")
            return f"🔍 {node_name}"

    async def _emit_unit_done(node_name: str, phase: str, agent_key: str) -> None:
        if event_sink is None:
            return
        completed_box[0] += 1
        total = total_units_box[0]
        percent = interpolate_percent(completed_box[0], total, progress_lo, progress_hi)
        try:
            await event_sink.emit(
                "progress", agent_key=agent_key or node_name, phase=phase,
                completed=completed_box[0], total=total,
                percent=percent, step_text=_progress_text(node_name),
            )
        except Exception as e:
            logger.warning(f"⚠️ [orchestrator] 进度事件发射失败: {e}")

    async def _execute_node(
        node_name: str, node_fn, st: Dict[str, Any], event_key: str = "", display_name: str = "",
        critical: bool = False, limit_key: Optional[str] = None, limit: Optional[int] = None,
    ) -> Dict[str, Any]:

        from app.llm.limiter import alimit

        key = event_key or _NODE_EVENT_KEYS.get(node_name, node_name)
        start = time.time()
        if event_sink is not None:
            event_sink.mark_running(key)
            await event_sink.emit(
                "agent_start", agent_key=key, phase=st.get("_phase", ""),
                name=display_name or _resolve_display_names().get(node_name) or node_name,
            )
        try:
            try:
                async with alimit(limit_key, limit):
                    update = await node_fn(st)
            except Exception as e:
                logger.error(f"❌ [orchestrator] 节点 {node_name} 异常: {e}", exc_info=True)
                if not critical:
                    _record_error(st, node_name, str(e), start, retried=False)
                    update = {}
                else:
                    logger.warning(f"🔁 [orchestrator] 关键节点 {node_name} 失败，重试 1 次")
                    try:
                        async with alimit(limit_key, limit):
                            update = await node_fn(st)
                    except Exception as e2:
                        _record_error(st, node_name, str(e2), start, retried=True)
                        raise
        finally:
            elapsed = time.time() - start
            node_timings[node_name] = elapsed
            logger.info(f"⏱️ [{node_name}] 耗时: {elapsed:.2f}秒")
            if event_sink is not None:
                event_sink.mark_completed(key)
                await event_sink.emit(
                    "agent_end", agent_key=key, duration_ms=int(elapsed * 1000)
                )
                await _emit_unit_done(node_name, phase=st.get("_phase", ""), agent_key=key)
        return update or {}

    async def _run_node(
        node_name: str, node_fn, st: Dict[str, Any], event_key: str = "", display_name: str = "",
        critical: bool = False, limit_key: Optional[str] = None, limit: Optional[int] = None,
    ) -> None:
        key = event_key or _NODE_EVENT_KEYS.get(node_name, node_name)
        update = await _execute_node(
            node_name, node_fn, st, event_key=event_key, display_name=display_name,
            critical=critical, limit_key=limit_key, limit=limit,
        )
        _before_reports = dict(st.get("reports") or {})
        _merge_state_update(st, update or {})
        await _emit_report_ready(
            event_sink,
            update or {},
            agent_key=key,
            phase=st.get("_phase", ""),
            before_reports=_before_reports,
            display_name=display_name or _resolve_display_names().get(node_name) or "",
        )

    async def _run_debate_round(
        side_nodes: List[tuple],
        st: Dict[str, Any],
        *,
        state_key: str,
        side_keys: List[str],
        report_keys: List[str],
        report_view: Callable[[Dict[str, Any], str], str],
        has_latest_speaker: bool = False,
    ) -> None:

        updates = await asyncio.gather(*[
            _execute_node(
                node_name, node_fn, st,
                critical=False,
                limit_key=deps.debate_limit_key, limit=deps.debate_limit,
            )
            for node_name, node_fn in side_nodes
        ])

        _before_reports = dict(st.get("reports") or {})
        _merge_debate_updates(
            st, updates, state_key=state_key, side_keys=side_keys,
            has_latest_speaker=has_latest_speaker,
        )

        ds = st.get(state_key) or {}
        for (node_name, _fn), side_key, report_key in zip(side_nodes, side_keys, report_keys):
            content = report_view(ds, side_key)
            if not content:
                continue
            st.setdefault("reports", {})[report_key] = content
            await _emit_report_ready(
                event_sink, {"reports": {report_key: content}},
                agent_key=_NODE_EVENT_KEYS.get(node_name, node_name),
                phase=st.get("_phase", ""),
                before_reports=_before_reports,
                display_name=_resolve_display_names().get(node_name) or node_name,
            )

    state = create_initial_state(company_name, trade_date, task_id=task_id, user_id=user_id)
    state["_event_sink"] = event_sink

    try:
        try:
            state["_phase"] = "analysts"
            from .agents import build_analyst_specs, run_analyst

            specs = await build_analyst_specs(
                selected_analysts,
                deps.toolkit,
                max_tool_calls=int(config.get("max_tool_calls", 12)),
                mcp_tools=mcp_tools,
                enable_subagent=bool(config.get("enable_subagent", False)),
            )
            concurrency = max(1, int(config.get("analyst_concurrency", 5) or 1))
            if deps.analyst_limit:
                concurrency = min(concurrency, int(deps.analyst_limit))
            semaphore = asyncio.Semaphore(concurrency)
            total_units_box[0] = compute_total_units(
                len(specs),
                phase2_enabled=phase2_enabled, phase2_rounds=max_debate_rounds,
                phase3_enabled=phase3_enabled, phase3_rounds=max_risk_rounds,
            )

            async def _run_analyst(internal_key: str, spec) -> Dict[str, Any]:
                node_name = _format_analyst_node(internal_key)
                start = time.time()
                if event_sink is not None:
                    event_sink.mark_running(internal_key)
                    await event_sink.emit(
                        "agent_start", agent_key=internal_key, phase="analysts",
                        name=spec.name,
                    )
                try:
                    from app.llm.limiter import alimit

                    async with semaphore, alimit(deps.analyst_limit_key, deps.analyst_limit):
                        return await run_analyst(
                            spec, deps.analyst_client, state, event_sink=event_sink
                        )
                except Exception as e:
                    logger.error(f"❌ [orchestrator] 分析师 {spec.name} 异常: {e}", exc_info=True)
                    _record_error(state, node_name, str(e), start, retried=False)
                    return {}
                finally:
                    elapsed = time.time() - start
                    node_timings[node_name] = elapsed
                    logger.info(f"⏱️ [{node_name}] 耗时: {elapsed:.2f}秒")
                    if event_sink is not None:
                        event_sink.mark_completed(internal_key)
                        await event_sink.emit(
                            "agent_end", agent_key=internal_key,
                            duration_ms=int(elapsed * 1000),
                        )
                        await _emit_unit_done(node_name, "analysts", internal_key)

            analyst_results = await asyncio.gather(
                *[_run_analyst(k, s) for k, s in specs.items()]
            )
            for (_internal_key, _spec), update in zip(specs.items(), analyst_results):
                _before = dict(state.get("reports") or {})
                _merge_state_update(state, update or {})
                await _emit_report_ready(
                    event_sink, update or {},
                    agent_key=_internal_key, phase="analysts", before_reports=_before,
                )

            if phase2_enabled:
                state["_phase"] = "research"
                state["investment_debate_state"]["max_rounds"] = max_debate_rounds + 1
                from app.engine.agents.stage_2.research_manager import create_research_manager
                from app.engine.agents.stage_2.researcher_factory import create_researcher

                bull_node = create_researcher(deps.debate_client, deps.bull_memory, side="bull")
                bear_node = create_researcher(deps.debate_client, deps.bear_memory, side="bear")
                research_manager = create_research_manager(deps.debate_client, deps.invest_judge_memory)

                from .state import investment_report_content

                side_nodes_p2 = [("Bull Researcher", bull_node), ("Bear Researcher", bear_node)]
                side_keys_p2 = ["bull", "bear"]
                report_keys_p2 = ["bull_researcher", "bear_researcher"]
                for _round in range(max_debate_rounds + 1):
                    if debate_parallel:
                        await _run_debate_round(
                            side_nodes_p2, state,
                            state_key="investment_debate_state",
                            side_keys=side_keys_p2,
                            report_keys=report_keys_p2,
                            report_view=investment_report_content,
                        )
                    else:
                        for node_name, node_fn in side_nodes_p2:
                            await _run_node(
                                node_name, node_fn, state,
                                limit_key=deps.debate_limit_key, limit=deps.debate_limit,
                            )
                await _run_node(
                    "Research Manager", research_manager, state, critical=True,
                    limit_key=deps.debate_limit_key, limit=deps.debate_limit,
                )

            state["_phase"] = "trader"
            from app.engine.agents.stage_2.trader import create_trader

            trader_node = create_trader(deps.debate_client, deps.trader_memory)
            await _run_node(
                "Trader", trader_node, state, critical=True,
                limit_key=deps.debate_limit_key, limit=deps.debate_limit,
            )

            if phase3_enabled:
                state["_phase"] = "risk"
                state["risk_debate_state"]["max_rounds"] = max_risk_rounds + 1
                from app.engine.agents.stage_3.debator_factory import create_debator
                from app.engine.agents.stage_3.risk_manager import create_risk_manager

                debators = {
                    "Risky Analyst": create_debator(deps.debate_client, side="risky"),
                    "Safe Analyst": create_debator(deps.debate_client, side="safe"),
                    "Neutral Analyst": create_debator(deps.debate_client, side="neutral"),
                }
                risk_manager = create_risk_manager(deps.debate_client, deps.risk_manager_memory)

                from .state import risk_report_content

                side_nodes_p3 = [
                    ("Risky Analyst", debators["Risky Analyst"]),
                    ("Safe Analyst", debators["Safe Analyst"]),
                    ("Neutral Analyst", debators["Neutral Analyst"]),
                ]
                side_keys_p3 = ["risky", "safe", "neutral"]
                report_keys_p3 = ["risky_analyst", "safe_analyst", "neutral_analyst"]
                for _round in range(max_risk_rounds + 1):
                    if debate_parallel:
                        await _run_debate_round(
                            side_nodes_p3, state,
                            state_key="risk_debate_state",
                            side_keys=side_keys_p3,
                            report_keys=report_keys_p3,
                            report_view=risk_report_content,
                            has_latest_speaker=True,
                        )
                    else:
                        for node_name, node_fn in side_nodes_p3:
                            await _run_node(
                                node_name, node_fn, state,
                                limit_key=deps.debate_limit_key, limit=deps.debate_limit,
                            )
                await _run_node(
                    "Risk Judge", risk_manager, state, critical=True,
                    limit_key=deps.debate_limit_key, limit=deps.debate_limit,
                )

            state["_phase"] = "summary"
            from app.engine.agents.stage_4.summary_agent import create_summary_agent

            summary_node = create_summary_agent(deps.debate_client)
            await _run_node(
                "Summary Agent", summary_node, state, critical=True,
                limit_key=deps.debate_limit_key, limit=deps.debate_limit,
            )

            for report_key, report_content in (state.get("reports") or {}).items():
                if report_key.endswith("_report") and report_content and not state.get(report_key):
                    state[report_key] = report_content

            state.pop("_phase", None)
            state.pop("_event_sink", None)
            state["node_timings"] = dict(node_timings)
            return export_legacy_state(state)
        except Exception as e:
            state.pop("_phase", None)
            state.pop("_event_sink", None)
            state["node_timings"] = dict(node_timings)
            e.partial_state = export_legacy_state(state)
            raise
    finally:
        if mcp_manager is not None:
            try:
                await mcp_manager.close_all()
            except Exception as e:
                logger.warning(f"⚠️ [orchestrator] 关闭 MCP 连接失败: {e}")

```
