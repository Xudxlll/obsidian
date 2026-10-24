---
type: 原始源码副本
---

来源：`app/llm/events.py`。原始完整文件，未修改代码。

```python
import asyncio
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import logging

logger = logging.getLogger("app.llm.events")

TOOL_RESULT_MAX_CHARS = 8000
REPORT_CONTENT_MAX_CHARS = 30000

_SYSTEM_REMINDER_PATTERN = re.compile(
    r"^\s*<system-reminder>\s*(.*?)\s*</system-reminder>\s*$", re.DOTALL
)

def unwrap_system_reminder(text: str) -> str:
    try:
        m = _SYSTEM_REMINDER_PATTERN.match(text or "")
        return m.group(1) if m else (text or "")
    except Exception:
        return text or ""

def flatten_message_content(content: Any) -> str:
    try:
        if isinstance(content, str):
            return content
        if content is None:
            return ""
        if isinstance(content, (list, tuple)):
            parts: List[str] = []
            for b in content:
                if isinstance(b, str):
                    parts.append(b)
                    continue
                text = getattr(b, "text", None)
                if isinstance(text, str) and text:
                    parts.append(text)
                elif hasattr(b, "name") and hasattr(b, "id"):
                    parts.append(f"[tool_use:{getattr(b, 'name', '')}]")
                elif hasattr(b, "tool_use_id"):
                    parts.append(f"[tool_result:{getattr(b, 'content', '')}]")
                else:
                    parts.append(str(b))
            return "".join(parts)
        return str(content)
    except Exception:
        try:
            return str(content)
        except Exception:
            return ""

def messages_event_payload(messages: List[Any]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for m in messages or []:
        role = getattr(m, "role", "")
        role = getattr(role, "value", role)
        out.append({
            "role": str(role),
            "content": flatten_message_content(getattr(m, "content", "")),
        })
    return out

REALTIME_ONLY = {"text_delta", "thinking_delta", "status"}
PROGRESS_ONLY = {"progress"}

@dataclass
class Event:
    task_id: str
    seq: int
    ts: float
    agent_key: str
    event_type: str
    phase: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "seq": self.seq,
            "ts": self.ts,
            "phase": self.phase,
            "agent_key": self.agent_key,
            "event_type": self.event_type,
            "payload": self.payload,
        }

class EventSink:

    def __init__(
        self,
        task_id: str = "",
        on_event: Optional[Callable[[Event], Any]] = None,
        on_persist: Optional[Callable[[List[Event]], Any]] = None,
        persist_batch: int = 20,
        persist_interval: float = 2.0,
        on_progress: Optional[Callable[[str], Any]] = None,
    ):
        self.task_id = task_id
        self._on_event = on_event
        self._on_persist = on_persist
        self._on_progress = on_progress
        self._persist_batch = persist_batch
        self._persist_interval = persist_interval
        self._buffer: List[Event] = []
        self._seq = 0
        self._last_flush = time.time()
        self._agent_status: Dict[str, str] = {}

    def mark_running(self, agent_key: str) -> None:
        self._agent_status[agent_key] = "running"

    def mark_completed(self, agent_key: str) -> None:
        self._agent_status[agent_key] = "completed"

    def is_running(self, agent_key: str) -> bool:
        return self._agent_status.get(agent_key) == "running"

    @property
    def running_agents(self) -> List[str]:
        return [k for k, v in self._agent_status.items() if v == "running"]

    async def emit(self, event_type: str, agent_key: str = "", phase: str = "", **payload: Any) -> Event:
        self._seq += 1
        ev = Event(
            task_id=self.task_id,
            seq=self._seq,
            ts=time.time(),
            agent_key=agent_key,
            event_type=event_type,
            phase=phase,
            payload=payload,
        )
        if self._on_event is not None:
            try:
                result = self._on_event(ev)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.warning(f"⚠️ [events] 实时回调失败: {e}")
        if event_type in PROGRESS_ONLY and self._on_progress is not None:
            try:
                result = self._on_progress(payload)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.warning(f"⚠️ [events] 进度回调失败: {e}")
        if self._on_persist is not None and event_type not in REALTIME_ONLY and event_type not in PROGRESS_ONLY:
            self._buffer.append(ev)
            if len(self._buffer) >= self._persist_batch or (
                self._buffer and time.time() - self._last_flush >= self._persist_interval
            ):
                await self.flush()
        return ev

    async def flush(self) -> None:
        if not self._buffer or self._on_persist is None:
            return
        batch, self._buffer = self._buffer, []
        self._last_flush = time.time()
        try:
            result = self._on_persist(batch)
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            logger.warning(f"⚠️ [events] 落库失败（丢弃 {len(batch)} 条）: {e}")

```
