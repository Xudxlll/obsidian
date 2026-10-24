---
type: 原始源码副本
---

来源：`app/llm/core/types.py`。原始完整文件，未修改代码。

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class StopReason(str, Enum):

    END_TURN = "end_turn"
    TOOL_USE = "tool_use"
    MAX_TOKENS = "max_tokens"
    STOP_SEQUENCE = "stop_sequence"
    OTHER = "other"

@dataclass
class TextBlock:
    text: str

@dataclass
class ToolUseBlock:

    id: str
    name: str
    input: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolResultBlock:

    tool_use_id: str
    content: str
    is_error: bool = False

@dataclass
class ThinkingBlock:

    thinking: str
    signature: str = ""

ContentBlock = TextBlock | ToolUseBlock | ToolResultBlock | ThinkingBlock

@dataclass
class Message:
    role: Role
    content: Any

    def blocks(self) -> List[ContentBlock]:
        if isinstance(self.content, str):
            return [TextBlock(text=self.content)]
        if isinstance(self.content, (TextBlock, ToolUseBlock, ToolResultBlock, ThinkingBlock)):
            return [self.content]
        return list(self.content)

@dataclass
class ToolDef:

    name: str
    description: str
    params_schema: Dict[str, Any] = field(default_factory=dict)
    handler: Any = None
    is_concurrency_safe: bool = False

@dataclass
class Usage:

    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens

@dataclass
class ChatResponse:

    message: Message
    stop_reason: StopReason
    usage: Usage = field(default_factory=Usage)
    model: str = ""
    raw: Any = None

    def text(self) -> str:
        return "".join(b.text for b in self.message.blocks() if isinstance(b, TextBlock))

    def tool_uses(self) -> List[ToolUseBlock]:
        return [b for b in self.message.blocks() if isinstance(b, ToolUseBlock)]

```
