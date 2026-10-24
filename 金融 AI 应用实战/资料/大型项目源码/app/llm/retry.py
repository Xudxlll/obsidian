import asyncio
import logging
from typing import Awaitable, Callable, TypeVar

from .core.errors import AuthError, LLMError, RateLimitError

logger = logging.getLogger("app.llm.retry")

DEFAULT_MAX_RETRIES = 10
BASE_DELAY_MS = 500
RATE_LIMIT_FALLBACK_THRESHOLD = 3
MAX_DELAY_MS = 60_000

T = TypeVar("T")

class FallbackTriggeredError(LLMError):

    def __init__(self, message: str = "连续限流达到阈值，触发 fallback"):
        super().__init__(message)

def _delay_ms(attempt: int) -> int:
    return min(BASE_DELAY_MS * (2**attempt), MAX_DELAY_MS)

def _should_retry(exc: Exception) -> bool:
    if isinstance(exc, AuthError):
        return False
    if isinstance(exc, (RateLimitError, TimeoutError, ConnectionError, LLMError)):
        return True
    return False

async def with_retry(
    fn: Callable[[], Awaitable[T]],
    *,
    max_retries: int = DEFAULT_MAX_RETRIES,
    on_fallback_trigger: Callable[[], None] = lambda: None,
) -> T:
    rate_limit_streak = 0
    attempt = 0
    while True:
        try:
            return await fn()
        except Exception as e:
            if not _should_retry(e):
                raise
            if isinstance(e, RateLimitError):
                rate_limit_streak += 1
                if rate_limit_streak >= RATE_LIMIT_FALLBACK_THRESHOLD:
                    on_fallback_trigger()
                    raise FallbackTriggeredError(f"连续 {rate_limit_streak} 次限流: {e}") from e
            else:
                rate_limit_streak = 0
            if attempt >= max_retries:
                raise
            delay = _delay_ms(attempt)
            logger.warning(
                f"⚠️ [retry] 第 {attempt + 1}/{max_retries} 次重试（{type(e).__name__}），{delay}ms 后重试: {e}"
            )
            await asyncio.sleep(delay / 1000)
            attempt += 1
