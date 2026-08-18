from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from trading_system.core.time import require_utc
from trading_system.market_data.feed import MarketEvent


@dataclass(slots=True)
class FeedMetrics:
    events: int = 0
    duplicates: int = 0
    gaps: int = 0
    stale: int = 0
    reconnects: int = 0
    last_event_at: datetime | None = None
    latencies_ms: list[float] = field(default_factory=list)

    def observe(
        self, event: MarketEvent, *, accepted: bool, duplicate: bool = False, gap: bool = False
    ) -> None:
        self.events += int(accepted)
        self.duplicates += int(duplicate)
        self.gaps += int(gap)
        require_utc(event.received_at)
        latency = (event.received_at - event.event_time).total_seconds() * 1000
        if latency >= 0:
            self.latencies_ms.append(latency)
        self.last_event_at = event.received_at

    @property
    def p95_latency_ms(self) -> float | None:
        if not self.latencies_ms:
            return None
        values = sorted(self.latencies_ms)
        return values[min(len(values) - 1, int(len(values) * 0.95))]
