---
type: 原始源码副本
---

来源：`app/llm/runner.py`。原始完整文件，未修改代码。

```python
import inspect
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import logging

from .compact.auto_compactor import AutoCompactor, CompactConfig
from .compact.token_counter import TokenCounter
from .core.base import BaseLLMClient
from .core.errors import ContextWindowExceededError
from .core.types import ChatResponse, Message, Role, ToolResultBlock, ToolUseBlock
from .limits import resolve_output_limits
from .orchestration.concurrency import partition_tool_calls, run_batches
from .events import (
    TOOL_RESULT_MAX_CHARS,
    messages_event_payload,
    unwrap_system_reminder,
)
from .retry import DEFAULT_MAX_RETRIES, FallbackTriggeredError, with_retry

logger = logging.getLogger("app.llm.runner")

DEFAULT_MAX_TURNS = 16
MAX_OUTPUT_TOKENS_RECOVERY_LIMIT = 3
RECOVERY_INSTRUCTION = (
    "Output token limit hit. Resume directly from where you stopped — no apology, "
    "no repetition, continue the unfinished content."
)

def _extract_thinking_text(resp: ChatResponse) -> str:

    parts: List[str] = []
    try:
        raw = getattr(resp, "raw", None)
        content = getattr(raw, "content", None)
        if isinstance(content, list):
            for b in content:
                if getattr(b, "type", "") in ("thinking", "reasoning"):
                    t = getattr(b, "thinking", None) or getattr(b, "text", None) or getattr(b, "reasoning", None)
                    if t:
                        parts.append(str(t))
        if not parts:
            choices = getattr(raw, "choices", None)
            if choices:
                msg = getattr(choices[0], "message", None)
                if msg is not None:
                    t = getattr(msg, "reasoning_content", None) or getattr(msg, "reasoning", None)
                    if t:
                        parts.append(str(t))
    except Exception as e:
        logger.debug(f"[runner] thinking 块抽取失败: {e}")
    return "\n".join(parts)

@dataclass
class RunResult:

    messages: List[Message] = field(default_factory=list)
    final_text: str = ""
    turns: int = 0
    tool_calls_executed: int = 0
    total_tokens: int = 0
    compacted: bool = False
    stop_reason: str = ""
    user_messages_injected: int = 0

async def run_conversation(
    client: BaseLLMClient,
    user_message: str,
    *,
    system: Optional[str] = None,
    tools: Optional[List[Any]] = None,
    registry: Optional[Any] = None,
    max_turns: int = DEFAULT_MAX_TURNS,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    thinking_budget: Optional[int] = None,
    thinking_effort: Optional[str] = None,
    fallback_client: Optional[BaseLLMClient] = None,
    retry_times: Optional[int] = None,
    history: Optional[List[Message]] = None,
    on_text_delta: Optional[Callable[[str], None]] = None,
    compact_config: Optional[CompactConfig] = None,
    enable_skill_listing: bool = False,
    skill_dirs: Optional[List[str]] = None,
    task_id: str = "",
    agent_key: str = "",
    phase: str = "",
    user_id: str = "",
    event_sink: Optional[Any] = None,
    inbox: Optional[Any] = None,
) -> RunResult:

    from .tools.registry import ToolRegistry, tool_registry as default_registry

    reg: ToolRegistry = registry or default_registry
    tool_defs = tools if tools is not None else reg.defs()

    extra_defs = {t.name: t for t in tool_defs if reg.get(t.name) is None}

    async def emit(event_type: str, **payload: Any) -> None:
        if event_sink is not None:
            await event_sink.emit(event_type, agent_key=agent_key, phase=phase, **payload)

    def record_usage(c: BaseLLMClient, resp: ChatResponse) -> None:
        from app.services.token_usage_recorder import token_usage_recorder

        token_usage_recorder.record(
            provider=getattr(c, "protocol", "unknown"),
            model_name=getattr(resp, "model", "") or getattr(c, "model", ""),
            usage=resp.usage,
            task_id=task_id,
            user_id=user_id,
            agent_key=agent_key,
            phase=phase,
        )

    messages = history if history is not None else []
    messages.append(Message(role=Role.USER, content=user_message))

    if enable_skill_listing:
        listing = _build_skill_listing(skill_dirs)
        if listing:
            system = (system + "\n\n" if system else "") + listing

    counter = TokenCounter()
    compactor = AutoCompactor(client, counter, compact_config)

    result = RunResult(messages=messages)
    turns = 0
    output_recovery_count = 0
    empty_response_retried = False
    truncated_text_parts: List[str] = []
    escalated_max_tokens: Optional[int] = None
    reacted_too_long = False
    active_client = client
    used_fallback = False

    safe_map = {t.name: bool(t.is_concurrency_safe) for t in tool_defs}

    while True:
        turns += 1
        if turns > max_turns:
            logger.warning(f"⚠️ [runner] 达到最大轮数 {max_turns}，强制停止")
            result.stop_reason = "max_turns"
            break

        need_compact = (
            compactor.should_compact(messages)
            or compactor.should_compact_predictive(messages)
            or compactor.is_blocking(messages)
        )
        if need_compact:
            messages, llm_compacted = await compactor.compact(messages, system=system)
            if llm_compacted:
                result.compacted = True
                await emit("compact", level="auto", messages=len(messages))

        messages_full = turns == 1
        request_payload: Dict[str, Any] = {
            "tools": len(tool_defs),
            "estimated_tokens": counter.count(messages),
            "messages_full": messages_full,
        }
        if messages_full:
            request_payload["messages"] = messages_event_payload(messages)
        else:
            request_payload["messages"] = len(messages)
        await emit("llm_request", **request_payload)

        async def _call() -> ChatResponse:
            resp_local: Optional[ChatResponse] = None
            async for event in active_client.chat_stream(
                messages,
                system=system,
                tools=tool_defs or None,
                max_tokens=escalated_max_tokens or max_tokens,
                temperature=temperature,
                thinking_budget=thinking_budget,
                thinking_effort=thinking_effort,
            ):
                if event.type == "text_delta":
                    if on_text_delta:
                        on_text_delta(event.text)
                    await emit("text_delta", text=event.text)
                elif event.type == "thinking_delta":
                    await emit("thinking_delta", text=event.text)
                elif event.type == "message" and event.response:
                    resp_local = event.response
            if resp_local is None:
                raise RuntimeError("未收到完整响应（流中断）")
            return resp_local

        try:
            resp = await with_retry(_call, max_retries=retry_times if retry_times is not None else DEFAULT_MAX_RETRIES)
        except FallbackTriggeredError:
            if fallback_client is not None and not used_fallback:
                used_fallback = True
                active_client = fallback_client
                logger.warning(
                    f"⚠️ [runner] 连续限流，切换 fallback 模型 → {getattr(fallback_client, 'model', '')} 重放本轮"
                )
                await emit("model_fallback", model=getattr(fallback_client, "model", ""))
                continue
            raise
        except ContextWindowExceededError:
            if not reacted_too_long:
                reacted_too_long = True
                messages = await compactor.reactive_compact(messages, system)
                result.compacted = True
                await emit("compact", level="reactive", messages=len(messages))
                continue
            result.stop_reason = "context_window_exceeded"
            logger.error("❌ [runner] reactive compact 后仍超窗，停止")
            break

        messages.append(resp.message)
        result.total_tokens += resp.usage.total
        record_usage(active_client, resp)

        thinking_text = _extract_thinking_text(resp)
        if thinking_text:
            await emit("thinking", text=thinking_text)

        await emit(
            "llm_response",
            stop_reason=resp.stop_reason.value,
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            cache_creation_input_tokens=resp.usage.cache_creation_input_tokens,
            cache_read_input_tokens=resp.usage.cache_read_input_tokens,
            model=getattr(resp, "model", ""),
            text=resp.text(),
        )

        counter.update_from_usage(resp.usage.input_tokens, len(messages))

        if resp.stop_reason.value == "max_tokens":
            truncated_text_parts.append(resp.text())
            if escalated_max_tokens is None:
                limits_ = resolve_output_limits(
                    getattr(active_client, "model", "") or "",
                    db_max_tokens=max_tokens,
                )
                current_cap = escalated_max_tokens or max_tokens or limits_.max_tokens
                if current_cap < limits_.upper_limit:
                    escalated_max_tokens = limits_.upper_limit
                    logger.warning(
                        f"⚠️ [runner] 输出截断，升级 max_tokens {current_cap} → "
                        f"{limits_.upper_limit} 重发"
                    )
                    messages.pop()
                    continue
            if output_recovery_count < MAX_OUTPUT_TOKENS_RECOVERY_LIMIT:
                output_recovery_count += 1
                logger.warning(
                    f"⚠️ [runner] 输出截断，注入恢复消息 ({output_recovery_count}/{MAX_OUTPUT_TOKENS_RECOVERY_LIMIT})"
                )
                messages.append(Message(role=Role.USER, content=RECOVERY_INSTRUCTION))
                continue
            logger.error("❌ [runner] 截断恢复耗尽，保留截断结果继续")
            result.final_text = "".join(truncated_text_parts).strip() or resp.text()
            result.stop_reason = resp.stop_reason.value
            break

        tool_uses = resp.tool_uses()
        if not tool_uses:
            if inbox is not None:
                injected = await inbox.drain_async()
                if injected:
                    for msg in injected:
                        messages.append(msg)
                        result.user_messages_injected += 1
                        await emit(
                            "user_message_injected",
                            text=unwrap_system_reminder(msg.content),
                        )
                    continue
            if not resp.text().strip() and not empty_response_retried:
                empty_response_retried = True
                logger.warning(
                    "⚠️ [runner] 本轮正文为空（全部输出在思考通道），注入恢复指令重试"
                )
                messages.append(
                    Message(role=Role.USER, content=(
                        "你上一条回复只包含思考过程，没有输出任何正文内容。"
                        "请直接输出正式的正文报告，不要再只写思考。"
                    ))
                )
                continue
            result.final_text = resp.text()
            result.stop_reason = resp.stop_reason.value
            break

        outputs = await _execute_partitioned(
            reg, tool_uses, safe_map, extra_defs=extra_defs, emit=emit, task_id=task_id
        )
        result.tool_calls_executed += len(tool_uses)
        result_blocks = [
            ToolResultBlock(
                tool_use_id=tu.id,
                content=out,
                is_error=out.startswith("错误") or out.startswith("工具执行失败"),
            )
            for tu, out in zip(tool_uses, outputs)
        ]
        messages.append(Message(role=Role.USER, content=result_blocks))

        if inbox is not None:
            injected = await inbox.drain_async()
            for msg in injected:
                messages.append(msg)
                result.user_messages_injected += 1
                await emit(
                    "user_message_injected",
                    text=unwrap_system_reminder(msg.content),
                )

    result.turns = min(turns, max_turns)
    return result

async def _execute_partitioned(
    reg,
    tool_uses: List[ToolUseBlock],
    safe_map: dict,
    extra_defs: Optional[dict] = None,
    task_id: str = "",
    emit: Optional[Any] = None,
) -> List[str]:

    async def _exec(tu: ToolUseBlock) -> str:
        logger.info(f"🔧 [runner] 工具调用: {tu.name}({str(tu.input)[:500]}{'...' if len(str(tu.input)) > 500 else ''})")
        start = time.time()
        if emit is not None:
            await emit("tool_call", tool=tu.name, tool_use_id=tu.id, input=tu.input)
        try:
            if extra_defs and tu.name in extra_defs:
                result = extra_defs[tu.name].handler(**tu.input)
                if inspect.isawaitable(result):
                    result = await result
                out = str(result)
            else:
                out = await reg.execute(tu.name, tu.input, task_id=task_id)
        except Exception as e:
            out = f"工具执行失败: {e}"
        if emit is not None:
            await emit(
                "tool_result",
                tool=tu.name,
                tool_use_id=tu.id,
                output=out[:TOOL_RESULT_MAX_CHARS],
                duration_ms=int((time.time() - start) * 1000),
                is_error=out.startswith("错误") or out.startswith("工具执行失败"),
            )
        return out

    batches = partition_tool_calls(tool_uses, lambda name: safe_map.get(name, False))
    return await run_batches(batches, _exec)

def _build_skill_listing(skill_dirs: Optional[List[str]]) -> str:
    try:
        from .skills.loader import SkillStore

        store = SkillStore(skill_dirs)
        return store.listing_text()
    except Exception as e:
        logger.warning(f"⚠️ [runner] skill 清单生成失败: {e}")
        return ""

```
