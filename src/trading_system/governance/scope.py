from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from trading_system.core.canonical import sha256_digest


class ScopeStatus(StrEnum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class MarketScopeCandidate(BaseModel):
    """Engine 97 input. Missing external facts remain None and deny activation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    market_profile_id: str | None = None
    jurisdiction: str | None = None
    asset_class: str | None = None
    universe_id: str | None = None
    broker_id: str | None = None
    venue_id: str | None = None
    account_id: str | None = None
    data_entitlement_id: str | None = None
    policy_versions: dict[str, str] = Field(default_factory=dict)


class ScopeDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: ScopeStatus
    scope_hash: str | None
    reason_codes: tuple[str, ...]
    missing_bindings: tuple[str, ...]


_EXTERNAL_FIELDS = (
    "market_profile_id",
    "jurisdiction",
    "asset_class",
    "universe_id",
    "broker_id",
    "venue_id",
    "account_id",
    "data_entitlement_id",
)


def bind_scope(candidate: MarketScopeCandidate) -> ScopeDecision:
    missing = tuple(field for field in _EXTERNAL_FIELDS if not getattr(candidate, field))
    if not candidate.policy_versions:
        missing += ("policy_versions",)
    if missing:
        return ScopeDecision(
            status=ScopeStatus.BLOCKED,
            scope_hash=None,
            reason_codes=("SCOPE_EXTERNAL_BINDING_MISSING",),
            missing_bindings=missing,
        )
    return ScopeDecision(
        status=ScopeStatus.ACTIVE,
        scope_hash=sha256_digest(candidate.model_dump(mode="python")),
        reason_codes=(),
        missing_bindings=(),
    )
