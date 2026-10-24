---
type: 原始源码副本
---

来源：`app/engine/orchestrator/invoker.py`。原始完整文件，未修改代码。

```python
from typing import List, Optional

from app.constants.llm_defaults import DEFAULT_CONTEXT_WINDOW, DEFAULT_MAX_TOKENS
from app.llm.core.base import BaseLLMClient
from app.llm.core.types import Message
from app.llm.runner import run_conversation
from app.llm.tools.registry import ToolRegistry

def _is_bundle(llm: object) -> bool:
    return hasattr(llm, "primary")

async def run_agent_turn(
    llm: object,
    history: List[Message],
    user_message: str,
    *,
    system: str,
    task_id: str = "",
    agent_key: str = "",
    phase: str = "",
    user_id: str = "",
    event_sink: Optional[object] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> str:

    bundle = llm if _is_bundle(llm) else None
    primary: BaseLLMClient = bundle.primary if bundle else llm
    fallback = bundle.fallback if bundle is not None else None
    retries = bundle.retry_times if bundle is not None else None

    eff_max_tokens = max_tokens or (bundle.max_tokens if bundle else None) or DEFAULT_MAX_TOKENS
    eff_temperature = temperature if temperature is not None else (bundle.temperature if bundle else None)

    compact_config = None
    if bundle is not None:
        from app.llm.compact.auto_compactor import CompactConfig

        compact_config = CompactConfig(
            context_window=getattr(bundle, "context_window", None) or DEFAULT_CONTEXT_WINDOW,
            max_output_tokens=getattr(bundle, "max_tokens", None) or DEFAULT_MAX_TOKENS,
        )

    result = await run_conversation(
        primary,
        user_message,
        system=system,
        tools=[],
        registry=ToolRegistry(),
        max_turns=1,
        max_tokens=eff_max_tokens,
        temperature=eff_temperature,
        fallback_client=fallback,
        retry_times=retries,
        compact_config=compact_config,
        history=history,
        task_id=task_id,
        agent_key=agent_key,
        phase=phase,
        user_id=user_id,
        event_sink=event_sink,
    )
    return result.final_text or ""

```
