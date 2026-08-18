from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from trading_system.core.time import require_utc


class PrincipalKind(StrEnum):
    HUMAN = "HUMAN"
    SERVICE = "SERVICE"


class Principal(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    principal_id: str = Field(min_length=1)
    kind: PrincipalKind
    roles: frozenset[str] = Field(min_length=1)
    authenticated_at: datetime
    expires_at: datetime
    disabled: bool = False

    @model_validator(mode="after")
    def validate_identity_window(self) -> Principal:
        authenticated = require_utc(self.authenticated_at)
        expires = require_utc(self.expires_at)
        if expires <= authenticated:
            raise ValueError("identity expiry must follow authentication")
        return self

    def active_at(self, now: datetime) -> bool:
        checked = require_utc(now)
        return not self.disabled and self.authenticated_at <= checked < self.expires_at


def independently_approved(owner: Principal, approver: Principal, *, at: datetime) -> bool:
    return (
        owner.principal_id != approver.principal_id
        and owner.active_at(at)
        and approver.active_at(at)
        and "INDEPENDENT_APPROVER" in approver.roles
    )
