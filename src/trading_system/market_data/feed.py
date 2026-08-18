from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Protocol

from trading_system.core.financial import FinancialNumber
from trading_system.core.time import require_utc


class ConnectionState(StrEnum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    AUTHENTICATING = "AUTHENTICATING"
    SYNCHRONIZING = "SYNCHRONIZING"
    STREAMING = "STREAMING"
    DEGRADED = "DEGRADED"
    HALTED = "HALTED"


_TRANSITIONS: dict[ConnectionState, frozenset[ConnectionState]] = {
    ConnectionState.DISCONNECTED: frozenset({ConnectionState.CONNECTING}),
    ConnectionState.CONNECTING: frozenset(
        {ConnectionState.AUTHENTICATING, ConnectionState.DISCONNECTED, ConnectionState.HALTED}
    ),
    ConnectionState.AUTHENTICATING: frozenset(
        {ConnectionState.SYNCHRONIZING, ConnectionState.DISCONNECTED, ConnectionState.HALTED}
    ),
    ConnectionState.SYNCHRONIZING: frozenset(
        {ConnectionState.STREAMING, ConnectionState.DEGRADED, ConnectionState.HALTED}
    ),
    ConnectionState.STREAMING: frozenset(
        {ConnectionState.DEGRADED, ConnectionState.DISCONNECTED, ConnectionState.HALTED}
    ),
    ConnectionState.DEGRADED: frozenset(
        {ConnectionState.SYNCHRONIZING, ConnectionState.DISCONNECTED, ConnectionState.HALTED}
    ),
    ConnectionState.HALTED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class FeedState:
    state: ConnectionState = ConnectionState.DISCONNECTED
    reason_code: str | None = None

    def transition(self, target: ConnectionState, reason_code: str | None = None) -> FeedState:
        if target not in _TRANSITIONS[self.state]:
            raise ValueError(f"invalid feed transition: {self.state} -> {target}")
        if target in {ConnectionState.DEGRADED, ConnectionState.HALTED} and not reason_code:
            raise ValueError("unsafe feed states require a reason code")
        return FeedState(target, reason_code)


@dataclass(frozen=True, slots=True)
class MarketEvent:
    provider: str
    instrument_id: str
    sequence: int
    event_time: datetime
    first_available_at: datetime
    received_at: datetime
    price: FinancialNumber
    quantity: FinancialNumber

    def __post_init__(self) -> None:
        if not self.provider or not self.instrument_id or self.sequence < 0:
            raise ValueError("market event identity and sequence are required")
        require_utc(self.event_time)
        require_utc(self.first_available_at)
        require_utc(self.received_at)


@dataclass(frozen=True, slots=True)
class SequenceResult:
    accepted: bool
    duplicate: bool
    gap: tuple[int, int] | None
    reason_code: str | None


class SequenceTracker:
    def __init__(self) -> None:
        self._last: dict[tuple[str, str], int] = {}

    def observe(self, event: MarketEvent) -> SequenceResult:
        key = (event.provider, event.instrument_id)
        previous = self._last.get(key)
        if previous is None:
            self._last[key] = event.sequence
            return SequenceResult(True, False, None, None)
        if event.sequence <= previous:
            return SequenceResult(False, True, None, "MARKET_DATA_DUPLICATE_OR_OUT_OF_ORDER")
        if event.sequence != previous + 1:
            return SequenceResult(
                False, False, (previous + 1, event.sequence - 1), "MARKET_DATA_SEQUENCE_GAP"
            )
        self._last[key] = event.sequence
        return SequenceResult(True, False, None, None)


class MarketDataProvider(Protocol):
    @property
    def state(self) -> FeedState: ...

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    async def next_event(self, timeout: timedelta) -> MarketEvent: ...
