from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Protocol

from trading_system.market_data.feed import (
    ConnectionState,
    FeedState,
    MarketEvent,
)


class AdapterError(RuntimeError):
    """Provider transport errors never imply market or trading authority."""


class RateLimitExceeded(AdapterError):
    pass


class RestTransport(Protocol):
    async def request(
        self, method: str, path: str, payload: dict[str, object] | None
    ) -> dict[str, object]: ...


class WebSocketTransport(Protocol):
    async def connect(self) -> None: ...

    async def close(self) -> None: ...

    async def send(self, payload: dict[str, object]) -> None: ...

    async def receive(self) -> dict[str, object]: ...


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    attempts: int = 3
    base_delay: float = 0.05
    max_delay: float = 1.0

    def delay(self, attempt: int) -> float:
        return float(min(self.max_delay, self.base_delay * (2**attempt)))


class TokenBucket:
    def __init__(self, capacity: int, refill_per_second: float) -> None:
        if capacity <= 0 or refill_per_second <= 0:
            raise ValueError("rate limiter capacity and refill must be positive")
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.refill_per_second = refill_per_second
        self._last = time.monotonic()

    def consume(self) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self._last) * self.refill_per_second)
        self._last = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


class RestClient:
    def __init__(
        self,
        transport: RestTransport,
        *,
        retry: RetryPolicy | None = None,
        rate_limiter: TokenBucket | None = None,
    ) -> None:
        self.transport = transport
        self.retry = retry or RetryPolicy()
        self.rate_limiter = rate_limiter

    async def request(
        self, method: str, path: str, payload: dict[str, object] | None = None
    ) -> dict[str, object]:
        if self.rate_limiter is not None and not self.rate_limiter.consume():
            raise RateLimitExceeded("provider request rate limit exceeded")
        last_error: Exception | None = None
        for attempt in range(self.retry.attempts):
            try:
                return await asyncio.wait_for(
                    self.transport.request(method, path, payload), timeout=10.0
                )
            except (TimeoutError, OSError, AdapterError) as exc:
                last_error = exc
                if attempt + 1 < self.retry.attempts:
                    await asyncio.sleep(self.retry.delay(attempt))
        raise AdapterError("REST request exhausted retries") from last_error


class WebSocketClient:
    def __init__(self, transport: WebSocketTransport) -> None:
        self.transport = transport
        self._state = FeedState()

    @property
    def state(self) -> FeedState:
        return self._state

    async def connect(self) -> None:
        self._state = self._state.transition(ConnectionState.CONNECTING)
        try:
            await asyncio.wait_for(self.transport.connect(), timeout=10.0)
            self._state = self._state.transition(ConnectionState.AUTHENTICATING)
        except (TimeoutError, OSError) as exc:
            self._state = self._state.transition(
                ConnectionState.HALTED, "MARKET_DATA_CONNECTION_FAILED"
            )
            raise AdapterError("websocket connection failed") from exc

    async def authenticate(self, payload: dict[str, object]) -> None:
        if self._state.state is not ConnectionState.AUTHENTICATING:
            raise AdapterError("websocket is not awaiting authentication")
        await asyncio.wait_for(self.transport.send(payload), timeout=10.0)
        self._state = self._state.transition(ConnectionState.SYNCHRONIZING)

    async def mark_streaming(self) -> None:
        if self._state.state is not ConnectionState.SYNCHRONIZING:
            raise AdapterError("websocket is not synchronized")
        self._state = self._state.transition(ConnectionState.STREAMING)

    async def close(self) -> None:
        await self.transport.close()
        if self._state.state is not ConnectionState.HALTED:
            self._state = self._state.transition(ConnectionState.DISCONNECTED)


class ProviderAdapter(Protocol):
    rest: RestClient
    websocket: WebSocketClient

    def normalize(self, payload: dict[str, object]) -> MarketEvent: ...
