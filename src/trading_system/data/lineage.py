from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from trading_system.core.canonical import sha256_digest
from trading_system.core.time import require_utc


class LineageKind(StrEnum):
    RAW = "RAW"
    DERIVED = "DERIVED"


class LineageNode(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    artifact_id: str = Field(min_length=1)
    kind: LineageKind
    created_at: datetime
    producer: str = Field(min_length=1)
    source_ids: tuple[str, ...]
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    transformation: str | None = None
    transformation_version: str | None = None

    @field_validator("created_at")
    @classmethod
    def timestamp_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    @model_validator(mode="after")
    def enforce_lineage_shape(self) -> LineageNode:
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ValueError("lineage source IDs must be unique")
        if self.kind is LineageKind.RAW:
            if self.source_ids or self.transformation or self.transformation_version:
                raise ValueError("raw lineage cannot claim derived inputs or transformation")
        elif not self.source_ids or not self.transformation or not self.transformation_version:
            raise ValueError("derived lineage requires sources and a versioned transformation")
        if self.artifact_id in self.source_ids:
            raise ValueError("lineage cannot directly reference itself")
        return self

    @property
    def lineage_hash(self) -> str:
        return sha256_digest(self.model_dump(mode="python"))
