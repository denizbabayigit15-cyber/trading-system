from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class GovernanceState(StrEnum):
    INITIALIZING = "INITIALIZING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


@dataclass(frozen=True, slots=True)
class GovernanceEvent:
    event_id: str
    state: GovernanceState
    occurred_at: datetime
    reason_code: str


class GovernanceOrchestrator:
    def __init__(self) -> None:
        self._state = GovernanceState.INITIALIZING
        self._events: list[GovernanceEvent] = []

    @property
    def state(self) -> GovernanceState:
        return self._state

    def transition(self, event: GovernanceEvent) -> None:
        allowed = {
            GovernanceState.INITIALIZING: {GovernanceState.ACTIVE, GovernanceState.SUSPENDED},
            GovernanceState.ACTIVE: {GovernanceState.SUSPENDED},
            GovernanceState.SUSPENDED: {GovernanceState.ACTIVE},
        }
        if event.state not in allowed[self._state]:
            raise ValueError("invalid governance lifecycle transition")
        if any(existing.event_id == event.event_id for existing in self._events):
            raise ValueError("governance event is immutable")
        self._events.append(event)
        self._state = event.state

    def events(self) -> tuple[GovernanceEvent, ...]:
        return tuple(self._events)
