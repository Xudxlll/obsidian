import re
import time
from typing import Literal

from app.llm.core.types import Message, Role
import logging
from app.engine.agents.utils.agent_config import load_agent_config, resolve_company_name
from app.engine.orchestrator.invoker import run_agent_turn

logger = logging.getLogger("default")

_STAGE2_REPORT_KEYS = frozenset({"bull_researcher", "bear_researcher"})

_SIDE_CONFIG = {
    "bull": {
        "slug": "bull-researcher",
        "emoji": "🐂",
        "label": "多头",
        "counterpart": "bear",
        "counterpart_label": "看跌分析师",
        "self_role_label": "核心论点",
        "counterpart_role_label": "对手（看跌分析师）",
        "round_key": "bull",
        "report_state_key": "bull_report_content",
        "history_key": "bull_history",
        "report_file_title": "看涨投资分析报告",
        "report_file_prefix": "看涨分析报告",
        "report_key": "bull_researcher",
        "speaker": "Bull Researcher",
        "argument_tag": "多头分析师",
        "section_initial": "## 初始报告：核心投资论点",
        "section_debate": "## 第 {round} 轮辩论报告：针对空方观点的反驳与辩护",
        "trigger_initial": (
            "请基于提供的基础报告，撰写你的【初始分析报告】。"
            "重点阐述核心投资论点，构建完整的逻辑框架。"
            "本阶段暂不需要反驳对手（因为辩论尚未开始）。"
        ),
        "file_header": "# {company_name} ({ticker}) 看涨投资分析报告",
    },
    "bear": {
        "slug": "bear-researcher",
        "emoji": "🐻",
        "label": "空头",
        "counterpart": "bull",
        "counterpart_label": "看涨分析师",
        "self_role_label": "风险警示",
        "counterpart_role_label": "对手（看涨分析师）",
        "round_key": "bear",
        "report_state_key": "bear_report_content",
        "history_key": "bear_history",
        "report_file_title": "看跌投资风险报告",
        "report_file_prefix": "看跌分析报告",
        "report_key": "bear_researcher",
        "speaker": "Bear Researcher",
        "argument_tag": "空头分析师",
        "section_initial": "## 初始报告：核心风险警示",
        "section_debate": "## 第 {round} 轮辩论报告：针对多方观点的质疑与反驳",
        "trigger_initial": (
            "请基于提供的基础报告，撰写你的【初始分析报告】。"
            "重点阐述核心风险警示，构建完整的逻辑框架。"
            "本阶段暂不需要反驳对手（因为辩论尚未开始）。"
        ),
        "file_header": "# {company_name} ({ticker}) 看跌投资风险报告",
    },
}

def create_researcher(llm, memory, side: Literal["bull", "bear"] = "bull"):

    if side not in _SIDE_CONFIG:
        raise ValueError(f"未知的辩手方向: {side!r}，期望 'bull' 或 'bear'")

    cfg = _SIDE_CONFIG[side]
    counter_cfg = _SIDE_CONFIG[cfg["counterpart"]]
    emoji = cfg["emoji"]
    label = cfg["label"]

    async def researcher_node(state) -> dict:
        logger.debug(f"{emoji} [DEBUG] ===== {label}研究员节点开始 =====")

        investment_debate_state = state.get("investment_debate_state", {})

        try:
            from app.engine.orchestrator.state import (
                current_round_index as calc_round_index,
                investment_report_content as view_report,
            )

            current_round_index = calc_round_index(investment_debate_state, 2)
            max_rounds = investment_debate_state.get("max_rounds", 2)
            rounds = investment_debate_state.get("rounds", [])

            from app.engine.prompts.builder import collect_reports, report_display_names

            all_reports = collect_reports(state, exclude_ids=_STAGE2_REPORT_KEYS)

            display_names = report_display_names()

            ticker = state.get("company_of_interest", "Unknown")
            from app.utils.stock_utils import StockUtils
            market_info = StockUtils.get_market_info(ticker)

            company_name = await resolve_company_name(ticker, market_info)
            currency = market_info["currency_name"]
            currency_symbol = market_info["currency_symbol"]

            logger.info(
                f"{emoji} [{label}研究员] 当前轮次: "
                f"{current_round_index}/{max_rounds}, 股票: {company_name}"
            )

            base_prompt = load_agent_config(cfg["slug"])
            if not base_prompt:
                error_msg = (
                    f"❌ 未找到 {cfg['slug']} 智能体配置，"
                    "请检查 phase2_agents_config.yaml 文件。"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            from app.engine.prompts.builder import (
                build_recall_rounds,
                build_researcher_trigger,
                context_prefix as build_context_prefix,
                inject_report_messages,
            )

            system = build_context_prefix(ticker, company_name, currency, currency_symbol) + "\n\n" + base_prompt
            messages = []

            messages.extend(
                inject_report_messages(
                    all_reports, display_names,
                    header_template="这是【{name}】：",
                )
            )

            from app.engine.agents.utils.memory import fetch_memory_brief

            memory_brief = await fetch_memory_brief(
                memory, "\n\n".join(r for r in all_reports.values() if r)
            )
            if memory_brief and not memory_brief.startswith("暂无"):
                messages.append(
                    Message(role=Role.USER, content=f"=== 历史交易反思（类似情景） ===\n{memory_brief}")
                )

            if current_round_index > 0:
                logger.info(
                    f"{emoji} [{label}研究员] 注入历史辩论上下文 "
                    f"(Rounds 0 to {current_round_index - 1})"
                )
                messages.extend(
                    build_recall_rounds(
                        rounds, current_round_index,
                        self_key=cfg["round_key"],
                        self_prefix_fmt=f"【回顾】这是我在【{{phase}}】建立的{cfg['self_role_label']}：",
                        opponents=[(
                            counter_cfg["round_key"],
                            f"【回顾】这是{cfg['counterpart_role_label']}在【{{phase}}】提出的观点：",
                        )],
                    )
                )

            has_counter_latest = bool(
                current_round_index > 0
                and current_round_index - 1 < len(rounds)
                and counter_cfg["round_key"] in rounds[current_round_index - 1]
            )
            trigger_msg = build_researcher_trigger(
                cfg["trigger_initial"], current_round_index, max_rounds,
                counter_latest=has_counter_latest,
            )

            content = await run_agent_turn(
                llm, messages, trigger_msg,
                system=system,
                task_id=state.get("task_id") or "",
                agent_key=f"researcher_{side}",
                phase="research",
                user_id=state.get("user_id") or "",
                event_sink=state.get("_event_sink"),
            )

            if not content.strip():
                content = f"⚠️ {label}研究员本轮未能生成有效内容（LLM 返回空响应）。"
                logger.warning(f"{emoji} [{label}研究员] LLM 返回空响应，使用占位文本")

            lines = content.strip().split("\n")
            cleaned_lines = [
                line for line in lines
                if not (
                    line.strip().startswith("# ")
                    or (line.strip().startswith("## ") and "分析报告" in line)
                )
            ]
            content = "\n".join(cleaned_lines).strip()

            from app.engine.orchestrator.state import append_round

            new_investment_debate_state = dict(investment_debate_state)
            append_round(new_investment_debate_state, cfg["round_key"], content, 2)
            report_content = view_report(new_investment_debate_state, side)

            try:
                from app.core.config import settings
                import os
                report_dir = os.path.join(settings.runtime_dir, "results")
                os.makedirs(report_dir, exist_ok=True)
                safe_name = re.sub(r'[\\/:*?"<>|]', "_", company_name or "unknown")
                filename = os.path.join(
                    report_dir, f"{cfg['report_file_prefix']}_{safe_name}.md"
                )
                tmp_filename = filename + ".tmp"
                with open(tmp_filename, "w", encoding="utf-8") as f:
                    f.write(
                        cfg["file_header"].format(
                            company_name=company_name, ticker=ticker
                        )
                        + "\n\n"
                    )
                    f.write(f"> 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"> 货币单位：{currency}\n\n")
                    f.write(report_content)
                os.replace(tmp_filename, filename)
                logger.info(f"{emoji} [{label}研究员] 已更新报告文件: {filename}")
            except Exception as e:
                logger.error(f"{emoji} [ERROR] 保存报告文件失败: {e}")

            return {
                "investment_debate_state": new_investment_debate_state,
                "reports": {cfg["report_key"]: report_content},
            }

        except Exception as e:
            logger.error(
                f"{emoji} ❌ [{label}研究员] 节点执行异常: {e}", exc_info=True
            )
            error_content = f"❌ {label}研究员节点执行失败：{e}"
            new_investment_debate_state = dict(investment_debate_state)
            new_investment_debate_state.update({
                "current_response": error_content,
                "latest_speaker": cfg["speaker"],
            })
            return {
                "investment_debate_state": new_investment_debate_state,
                "reports": {cfg["report_key"]: error_content},
            }

    return researcher_node
