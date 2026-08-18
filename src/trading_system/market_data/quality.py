from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from trading_system.market_data.feed import MarketEvent, SequenceTracker


class SourceState(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"


class DataSource(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    version: str = Field(min_length=1)
    state: SourceState
    entitlement_bound: bool = False


class DataQualityReport(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str
    accepted: int = Field(ge=0)
    rejected: int = Field(ge=0)
    duplicate: int = Field(ge=0)
    gaps: int = Field(ge=0)
    stale: int = Field(ge=0)
    reason_codes: tuple[str, ...]


class ValidationResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_id: str
    valid: bool
    reason_codes: tuple[str, ...]


class EventValidatorRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, object] = {}

    def register(self, schema_id: str, validator: object) -> None:
        if schema_id in self._validators:
            raise ValueError("schema validator already registered")
        self._validators[schema_id] = validator

    def register_model(self, schema_id: str, model: type[BaseModel]) -> None:
        self.register(schema_id, model)

    def validate(self, schema_id: str, payload: dict[str, object]) -> ValidationResult:
        validator = self._validators.get(schema_id)
        if validator is None:
            return ValidationResult(
                schema_id=schema_id, valid=False, reason_codes=("DATA_SCHEMA_UNKNOWN",)
            )
        try:
            if isinstance(validator, type) and issubclass(validator, BaseModel):
                validator.model_validate(payload)
                valid = True
            else:
                valid = bool(validator(payload))  # type: ignore[operator]
        except Exception:
            valid = False
        return ValidationResult(
            schema_id=schema_id, valid=valid, reason_codes=() if valid else ("DATA_SCHEMA_INVALID",)
        )


class DataSourceRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, DataSource] = {}

    def register(self, source: DataSource) -> None:
        if source.source_id in self._sources:
            raise ValueError("data source already registered")
        self._sources[source.source_id] = source

    def get(self, source_id: str) -> DataSource:
        return self._sources[source_id]

    def all(self) -> tuple[DataSource, ...]:
        return tuple(self._sources[key] for key in sorted(self._sources))


def assess_events(
    source: DataSource,
    events: tuple[MarketEvent, ...],
    *,
    now: datetime,
    max_age_seconds: int,
) -> DataQualityReport:
    if source.state is not SourceState.ENABLED or not source.entitlement_bound:
        return DataQualityReport(
            source_id=source.source_id,
            accepted=0,
            rejected=len(events),
            duplicate=0,
            gaps=0,
            stale=0,
            reason_codes=("DATA_SOURCE_UNBOUND",),
        )
    tracker = SequenceTracker()
    seen: set[tuple[str, int]] = set()
    accepted = duplicate = gaps = stale = 0
    for event in events:
        key = (event.instrument_id, event.sequence)
        if key in seen:
            duplicate += 1
            continue
        seen.add(key)
        result = tracker.observe(event)
        if result.duplicate:
            duplicate += 1
            continue
        if result.gap:
            gaps += 1
        if (now - event.event_time).total_seconds() > max_age_seconds:
            stale += 1
        if result.accepted:
            accepted += 1
    reasons = tuple(
        code
        for code, condition in (
            ("DATA_SEQUENCE_GAP", gaps > 0),
            ("DATA_STALE", stale > 0),
        )
        if condition
    )
    return DataQualityReport(
        source_id=source.source_id,
        accepted=accepted,
        rejected=len(events) - accepted,
        duplicate=duplicate,
        gaps=gaps,
        stale=stale,
        reason_codes=reasons,
    )


@dataclass(slots=True)
class HistoricalDataLake:
    _events: list[MarketEvent]

    def __init__(self) -> None:
        self._events = []

    def append(self, event: MarketEvent) -> None:
        self._events.append(event)

    def query(
        self, *, instrument_id: str, start: datetime, end: datetime
    ) -> tuple[MarketEvent, ...]:
        return tuple(
            event
            for event in sorted(self._events, key=lambda item: (item.event_time, item.sequence))
            if event.instrument_id == instrument_id and start <= event.event_time < end
        )
