from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.canonical import sha256_digest
from trading_system.core.time import require_utc


class PolicySnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    policy_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    effective_at: datetime
    expires_at: datetime | None = None
    rules: dict[str, str]
    approved: bool = False

    @field_validator("effective_at", "expires_at")
    @classmethod
    def timestamps_are_utc(cls, value: datetime | None) -> datetime | None:
        return None if value is None else require_utc(value)

    @property
    def policy_hash(self) -> str:
        return sha256_digest(self.model_dump(mode="python"))

    def active_at(self, now: datetime) -> bool:
        checked = require_utc(now)
        return (
            self.approved
            and self.effective_at <= checked
            and (self.expires_at is None or checked < self.expires_at)
        )

    def evaluate(self, facts: dict[str, str], *, at: datetime) -> tuple[bool, tuple[str, ...]]:
        if not self.active_at(at):
            return False, ("POLICY_INACTIVE",)
        missing = tuple(key for key in self.rules if facts.get(key) != self.rules[key])
        return not missing, tuple(f"POLICY_RULE_FAILED:{key}" for key in missing)
