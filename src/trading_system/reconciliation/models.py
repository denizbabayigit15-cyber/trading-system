from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.time import require_utc


class ReconciliationStatus(StrEnum):
    CLEAN = "CLEAN"
    REQUIRED = "RECONCILIATION_REQUIRED"


class SourceObservation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    state_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    observed_at: datetime

    @field_validator("observed_at")
    @classmethod
    def observed_at_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)


class ReconciliationDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: ReconciliationStatus
    source_priority: tuple[str, ...]
    source_observations: tuple[SourceObservation, ...]
    resolution_rule: str | None
    resolved_by: str | None
    resolution_time: datetime | None
    resolution_evidence: str | None


def compare_sources(observations: tuple[SourceObservation, ...]) -> ReconciliationDecision:
    if len(observations) < 2 or len({item.source_id for item in observations}) != len(observations):
        raise ValueError("reconciliation requires at least two distinct sources")
    hashes = {item.state_hash for item in observations}
    clean = len(hashes) == 1
    return ReconciliationDecision(
        status=ReconciliationStatus.CLEAN if clean else ReconciliationStatus.REQUIRED,
        source_priority=tuple(item.source_id for item in observations),
        source_observations=observations,
        resolution_rule="EXACT_STATE_HASH_MATCH" if clean else None,
        resolved_by="DETERMINISTIC_COMPARISON" if clean else None,
        resolution_time=max(item.observed_at for item in observations) if clean else None,
        resolution_evidence=next(iter(hashes)) if clean else None,
    )
