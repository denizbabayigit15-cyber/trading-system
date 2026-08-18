from __future__ import annotations

from datetime import datetime, timedelta
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.time import require_utc


class TemporalStatus(StrEnum):
    VALID = "VALID"
    FUTURE_KNOWLEDGE = "FUTURE_KNOWLEDGE"
    NOT_AVAILABLE_AT_DECISION = "NOT_AVAILABLE_AT_DECISION"
    RECEIVED_AFTER_DECISION = "RECEIVED_AFTER_DECISION"
    STALE = "STALE"
    CLOCK_INVALID = "CLOCK_INVALID"


class ObservationTime(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str = Field(min_length=1)
    event_time: datetime
    first_available_at: datetime
    received_at: datetime
    revision: str = Field(min_length=1)
    lineage_id: str = Field(min_length=1)

    @field_validator("event_time", "first_available_at", "received_at")
    @classmethod
    def timestamps_are_utc(cls, value: datetime) -> datetime:
        return require_utc(value)


class TemporalAssessment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: TemporalStatus
    reason_code: str | None
    age: timedelta | None

    @property
    def valid(self) -> bool:
        return self.status is TemporalStatus.VALID


def assess_temporal_truth(
    observation: ObservationTime, *, decision_time: datetime, max_age: timedelta | None
) -> TemporalAssessment:
    decision = require_utc(decision_time)
    if max_age is None:
        return TemporalAssessment(
            status=TemporalStatus.CLOCK_INVALID,
            reason_code="TEMPORAL_MAX_AGE_UNBOUND",
            age=None,
        )
    if max_age < timedelta(0):
        raise ValueError("max_age cannot be negative")
    if observation.event_time > observation.first_available_at:
        return TemporalAssessment(
            status=TemporalStatus.CLOCK_INVALID,
            reason_code="TEMPORAL_EVENT_AFTER_AVAILABILITY",
            age=None,
        )
    if observation.event_time > decision:
        return TemporalAssessment(
            status=TemporalStatus.FUTURE_KNOWLEDGE,
            reason_code="TEMPORAL_FUTURE_KNOWLEDGE",
            age=None,
        )
    if observation.first_available_at > decision:
        return TemporalAssessment(
            status=TemporalStatus.NOT_AVAILABLE_AT_DECISION,
            reason_code="TEMPORAL_NOT_AVAILABLE_AT_DECISION",
            age=None,
        )
    if observation.received_at > decision:
        return TemporalAssessment(
            status=TemporalStatus.RECEIVED_AFTER_DECISION,
            reason_code="TEMPORAL_RECEIVED_AFTER_DECISION",
            age=None,
        )
    age = decision - observation.first_available_at
    if age > max_age:
        return TemporalAssessment(
            status=TemporalStatus.STALE, reason_code="TEMPORAL_STALE", age=age
        )
    return TemporalAssessment(status=TemporalStatus.VALID, reason_code=None, age=age)
