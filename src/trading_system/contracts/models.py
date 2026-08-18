from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from trading_system.core.ids import new_id
from trading_system.core.time import require_utc, utc_now


class EngineRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    engine_id: int = Field(ge=1, le=112)
    engine_name: str = Field(min_length=1)
    orchestrator: str = Field(min_length=1)
    source: Literal["V2.2.5_RETAINED", "V3.0.0_ADDED"]
    primary_output: str = Field(min_length=1)
    runtime_status: Literal["NOT_IMPLEMENTED"]


class EngineRegistry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal["1.0.0"]
    contract_version: Literal["3.0.0"]
    expected_count: Literal[112]
    engines: tuple[EngineRecord, ...]

    @model_validator(mode="after")
    def validate_complete_catalog(self) -> Self:
        ids = [engine.engine_id for engine in self.engines]
        if ids != list(range(1, 113)):
            raise ValueError("engine registry must contain ordered unique IDs 1..112")
        return self


def _payload_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


class EventEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str = Field(default_factory=lambda: new_id("evt"), pattern=r"^evt_[0-9a-f]{32}$")
    event_type: str = Field(pattern=r"^[a-z0-9_]+\.[a-z0-9_]+\.(succeeded|failed)\.v[0-9]+$")
    event_version: int = Field(default=1, ge=1)
    schema_version: str = Field(default="1.0.0", pattern=r"^[0-9]+\.[0-9]+\.[0-9]+$")
    occurred_at: datetime
    produced_at: datetime = Field(default_factory=utc_now)
    producer: str = Field(min_length=1)
    correlation_id: str = Field(min_length=1)
    causation_id: str | None = None
    decision_id: str | None = None
    lineage_id: str | None = None
    scope_hash: str | None = None
    payload: dict[str, Any]
    payload_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")

    @field_validator("occurred_at", "produced_at")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    @model_validator(mode="after")
    def bind_payload_hash(self) -> Self:
        expected = _payload_hash(self.payload)
        if self.payload_sha256 is not None and self.payload_sha256 != expected:
            raise ValueError("payload_sha256 does not match canonical payload")
        object.__setattr__(self, "payload_sha256", expected)
        return self
