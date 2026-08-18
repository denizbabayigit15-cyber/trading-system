from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime

from trading_system.core.canonical import sha256_digest
from trading_system.market_data.feed import MarketEvent


@dataclass(frozen=True, slots=True)
class ReplayResult:
    event_count: int
    input_hash: str
    output_hash: str


@dataclass(slots=True)
class SimulationClock:
    current: datetime | None = None

    def advance_to(self, timestamp: datetime) -> datetime:
        if self.current is not None and timestamp < self.current:
            raise ValueError("simulation clock cannot move backwards")
        self.current = timestamp
        return timestamp


def replay(
    events: Iterable[MarketEvent], consumer: Callable[[MarketEvent], object]
) -> ReplayResult:
    ordered = tuple(events)
    ordering = [
        (event.first_available_at, event.provider, event.instrument_id, event.sequence)
        for event in ordered
    ]
    if ordering != sorted(ordering):
        raise ValueError("replay input must be ordered by availability and source sequence")
    inputs = [
        {
            "provider": event.provider,
            "instrument_id": event.instrument_id,
            "sequence": event.sequence,
            "event_time": event.event_time,
            "first_available_at": event.first_available_at,
            "received_at": event.received_at,
            "price": event.price.canonical(),
            "quantity": event.quantity.canonical(),
        }
        for event in ordered
    ]
    outputs = [consumer(event) for event in ordered]
    return ReplayResult(len(ordered), sha256_digest(inputs), sha256_digest(outputs))
