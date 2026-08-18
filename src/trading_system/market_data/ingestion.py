from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from trading_system.market_data.feed import MarketEvent, SequenceResult, SequenceTracker


class RawEventStore(Protocol):
    def append(self, event: MarketEvent) -> None: ...

    def events(self) -> tuple[MarketEvent, ...]: ...


class InMemoryRawEventStore:
    def __init__(self) -> None:
        self._events: list[MarketEvent] = []

    def append(self, event: MarketEvent) -> None:
        self._events.append(event)

    def events(self) -> tuple[MarketEvent, ...]:
        return tuple(self._events)


class HistoricalIngestion:
    def __init__(self, store: RawEventStore) -> None:
        self.store = store
        self.sequences = SequenceTracker()

    def ingest(self, events: Iterable[MarketEvent]) -> tuple[SequenceResult, ...]:
        results: list[SequenceResult] = []
        for event in events:
            result = self.sequences.observe(event)
            results.append(result)
            if result.accepted:
                self.store.append(event)
        return tuple(results)
