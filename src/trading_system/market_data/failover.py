from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProviderState(StrEnum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ProviderHealth:
    provider_id: str
    state: ProviderState
    sequence: int | None


def choose_provider(providers: tuple[ProviderHealth, ...]) -> ProviderHealth:
    healthy = tuple(item for item in providers if item.state is ProviderState.HEALTHY)
    if not healthy:
        raise RuntimeError("MARKET_DATA_FAILOVER_NO_HEALTHY_PROVIDER")
    return max(healthy, key=lambda item: item.sequence if item.sequence is not None else -1)
