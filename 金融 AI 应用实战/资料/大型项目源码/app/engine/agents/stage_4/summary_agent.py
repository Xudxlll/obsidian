import json
import logging
from app.engine.orchestrator.invoker import run_agent_turn

logger = logging.getLogger("default")

from app.engine.prompts.parts import SUMMARY_SYSTEM_PROMPT as SYSTEM_PROMPT

_DEFAULT_STRUCTURED_DATA = {
    "key_indicators": {"entry_price": "N/A", "target_price": "N/A", "stop_loss": "N/A", "support_level": "N/A", "resistance_level": "N/A"},
    "model_confidence": 0,
    "risk_assessment": {"level": "Low", "score": 0.0, "description": "生成失败"},
    "analysis_summary": "系统错误：无法生成分析摘要",
    "investment_recommendation": "暂无建议",
    "analysis_reference": [],
    "final_signal": "Hold",
}

_PLACEHOLDER_PREFIX = "⚠️"
_FAILURE_KEYWORDS = ("数据获取失败", "获取数据失败", "工具调用失败")
_INVALID_REPORT_MAX_LEN = 200
_MISSING_PLACEHOLDER = "（该项数据缺失）"

def _is_invalid_report(text: str) -> bool:

    if not text or not isinstance(text, str):
        return True
    if text.startswith(_PLACEHOLDER_PREFIX):
        return True
    if len(text) < _INVALID_REPORT_MAX_LEN and any(k in text for k in _FAILURE_KEYWORDS):
        return True
    return False

def _ensure_required_fields(data: dict) -> dict:
    for key, default_val in _DEFAULT_STRUCTURED_DATA.items():
        if key not in data:
            data[key] = default_val
    return data

def _truncate(text: str, limit: int) -> str:
    if not text or not isinstance(text, str):
        return ""
    return text[:limit]

def _build_user_message(
    company_name: str,
    trader_plan: str,
    final_decision: str,
    market_report: str,
    news_report: str,
    fundamentals_report: str,
    sentiment_report: str,
    risk_debate_history: str,
    other_reports: dict,
    missing_labels: list[str] | None = None,
) -> str:

    parts = [f"请为以下公司生成结构化总结数据：{company_name}\n"]
    if missing_labels:
        parts.append(
            f"注：以下输入数据缺失：{'、'.join(missing_labels)}。"
            "请基于现有有效数据正常生成总结，缺失项对应字段填 \"N/A\"，"
            "并在 risk_assessment.description 中简要注明数据缺失。"
        )
    parts.append(f"<trader_plan>{_truncate(trader_plan, 1500)}</trader_plan>")
    parts.append(f"<final_decision>{_truncate(final_decision, 1500)}</final_decision>")
    parts.append(f"<market_report>{_truncate(market_report, 500)}</market_report>")
    parts.append(f"<news_report>{_truncate(news_report, 500)}</news_report>")
    parts.append(
        f"<fundamentals_report>{_truncate(fundamentals_report, 500)}</fundamentals_report>"
    )
    parts.append(f"<sentiment_report>{_truncate(sentiment_report, 500)}</sentiment_report>")
    parts.append(f"<risk_debate>{_truncate(risk_debate_history, 1500)}</risk_debate>")
    if other_reports:
        extra_lines = []
        for k, v in other_reports.items():
            extra_lines.append(f"- {k}: {_truncate(v, 300)}")
        parts.append(f"<other_reports>{chr(10).join(extra_lines)}</other_reports>")
    return "\n".join(parts)

def create_summary_agent(llm):
    async def summary_node(state):
        logger.info("📊 [Summary Agent] 开始生成结构化总结数据...")

        company_name = state.get("company_of_interest", "Unknown")

        all_reports = {}
        for key in state.keys():
            if key.endswith("_report") and state[key]:
                all_reports[key] = state[key]

        market_report = state.get("market_report", "")
        news_report = state.get("news_report", "")
        fundamentals_report = state.get("fundamentals_report", "")
        sentiment_report = state.get("sentiment_report", "")

        trader_plan = state.get("trader_investment_plan", "")
        final_decision = state.get("final_trade_decision", "")

        from app.engine.orchestrator.state import risk_history

        risk_debate_history = risk_history(state.get("risk_debate_state"))

        other_reports = {
            k: v for k, v in all_reports.items()
            if k not in (
                "market_report",
                "news_report",
                "fundamentals_report",
                "sentiment_report",
            )
        }

        def _sanitize(label: str, text: str) -> str:
            if _is_invalid_report(text):
                missing_labels.append(label)
                return _MISSING_PLACEHOLDER
            return text

        missing_labels: list[str] = []
        trader_plan_s = _sanitize("交易计划", trader_plan)
        final_decision_s = _sanitize("最终决策", final_decision)
        market_report_s = _sanitize("市场报告", market_report)
        news_report_s = _sanitize("新闻报告", news_report)
        fundamentals_report_s = _sanitize("基本面报告", fundamentals_report)
        sentiment_report_s = _sanitize("情绪报告", sentiment_report)
        risk_debate_s = _sanitize("风险辩论", risk_debate_history or "")

        other_reports_s: dict = {}
        for k, v in other_reports.items():
            other_reports_s[k] = _sanitize(k, v)

        non_empty_inputs = [
            t for t in (
                trader_plan, final_decision, market_report, news_report,
                fundamentals_report, sentiment_report, risk_debate_history or "",
                *other_reports.values(),
            ) if t
        ]
        if non_empty_inputs and all(_is_invalid_report(t) for t in non_empty_inputs):
            logger.warning(
                f"⚠️ [Summary Agent] 全部输入无效（{missing_labels}），"
                "跳过 LLM 调用，直接返回失败结构"
            )
            return {
                "structured_summary": {
                    **_DEFAULT_STRUCTURED_DATA,
                    "analysis_summary": "数据获取失败，无法生成报告",
                    "investment_recommendation": "无建议",
                    "risk_assessment": {
                        "level": "High",
                        "score": 10.0,
                        "description": "数据获取失败，无法生成报告",
                    },
                }
            }

        user_prompt = _build_user_message(
            company_name=company_name,
            trader_plan=trader_plan_s,
            final_decision=final_decision_s,
            market_report=market_report_s,
            news_report=news_report_s,
            fundamentals_report=fundamentals_report_s,
            sentiment_report=sentiment_report_s,
            risk_debate_history=risk_debate_s,
            other_reports=other_reports_s,
            missing_labels=missing_labels,
        )

        try:
            content = (
                await run_agent_turn(
                    llm,
                    [],
                    user_prompt,
                    system=SYSTEM_PROMPT,
                    task_id=state.get("task_id") or "",
                    agent_key="summary",
                    phase="summary",
                    user_id=state.get("user_id") or "",
                    event_sink=state.get("_event_sink"),
                )
            ).strip()
            
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            structured_data = json.loads(content)

            required_keys = {
                "key_indicators", "model_confidence", "risk_assessment",
                "analysis_summary", "investment_recommendation", "final_signal",
            }
            missing = required_keys - set(structured_data.keys())
            if missing:
                logger.warning(
                    f"⚠️ [Summary Agent] LLM 返回 JSON 缺少必需字段: {missing}，"
                    "使用兜底值补齐"
                )
                structured_data = _ensure_required_fields(structured_data)

            logger.info(f"✅ [Summary Agent] 成功生成结构化数据: {list(structured_data.keys())}")
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ [Summary Agent] JSON 解析失败: {e}")
            logger.error(f"   原始内容: {content}")
            structured_data = {
                "key_indicators": {"entry_price": "N/A", "target_price": "N/A", "stop_loss": "N/A", "support_level": "N/A", "resistance_level": "N/A"},
                "model_confidence": 50,
                "risk_assessment": {"level": "Medium", "score": 5.0, "description": "解析失败，使用默认值"},
                "analysis_summary": "JSON解析失败，无法生成分析摘要",
                "investment_recommendation": "暂无建议",
                "analysis_reference": [],
                "final_signal": "Hold"
            }
        except Exception as e:
            logger.error(f"❌ [Summary Agent] 生成失败: {e}", exc_info=True)
            structured_data = {
                "key_indicators": {"entry_price": "N/A", "target_price": "N/A", "stop_loss": "N/A", "support_level": "N/A", "resistance_level": "N/A"},
                "model_confidence": 0,
                "risk_assessment": {"level": "Low", "score": 0.0, "description": "生成失败"},
                "analysis_summary": "系统错误：无法生成分析摘要",
                "investment_recommendation": "暂无建议",
                "analysis_reference": [],
                "final_signal": "Hold"
            }

        return {"structured_summary": structured_data}

    return summary_node
