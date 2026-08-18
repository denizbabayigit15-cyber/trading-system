from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.canonical import sha256_digest
from trading_system.core.ids import new_id
from trading_system.core.time import require_utc


class PredicateValue(StrEnum):
    PASS = "PASS"  # noqa: S105 - contract status, not a credential
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class AuthoritySnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    decision_id: str = Field(min_length=1)
    scope_hash: str = Field(min_length=1)
    state_snapshot_id: str = Field(min_length=1)
    market_snapshot_id: str = Field(min_length=1)
    predicates: dict[str, PredicateValue] = Field(min_length=1)
    hard_predicates: frozenset[str] = Field(min_length=1)
    policy_versions: dict[str, str] = Field(min_length=1)
    risk_state: str = Field(min_length=1)
    capital_state: str = Field(min_length=1)
    reconciliation_state: str = Field(min_length=1)
    certification_scope_match: bool
    r4_certified: bool
    live_authorized: bool
    computed_at: datetime

    @field_validator("computed_at")
    @classmethod
    def computed_at_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)


class AuthorityDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    authorization_id: str
    decision_id: str
    scope_hash: str
    snapshot_hash: str
    all_predicates: dict[str, PredicateValue]
    failed_predicates: tuple[str, ...]
    unknown_predicates: tuple[str, ...]
    reason_codes: tuple[str, ...]
    risk_state: str
    capital_state: str
    reconciliation_state: str
    certification_scope_match: bool
    final_authorized: bool
    policy_versions: dict[str, str]
    computed_at: datetime


def evaluate_authority(snapshot: AuthoritySnapshot) -> AuthorityDecision:
    missing = sorted(snapshot.hard_predicates - snapshot.predicates.keys())
    failed = sorted(
        key
        for key in snapshot.hard_predicates
        if snapshot.predicates.get(key) is PredicateValue.FAIL
    )
    unknown = sorted(
        key
        for key in snapshot.hard_predicates
        if snapshot.predicates.get(key) in {None, PredicateValue.UNKNOWN}
    )
    reasons: list[str] = []
    if missing:
        reasons.append("AUTH_MISSING_CRITICAL_STATE")
    if failed:
        reasons.append("AUTH_HARD_PREDICATE_FAILED")
    if unknown:
        reasons.append("AUTH_UNKNOWN_CRITICAL_STATE")
    if snapshot.reconciliation_state != "CLEAN":
        reasons.append("RECONCILIATION_REQUIRED")
    if not snapshot.certification_scope_match:
        reasons.append("AUTH_CERTIFICATION_SCOPE_MISMATCH")
    if not snapshot.r4_certified:
        reasons.append("AUTH_R4_NOT_CERTIFIED")
    if not snapshot.live_authorized:
        reasons.append("AUTH_LIVE_DISABLED")

    authorized = not reasons and all(
        snapshot.predicates[key] in {PredicateValue.PASS, PredicateValue.NOT_APPLICABLE}
        for key in snapshot.hard_predicates
    )
    return AuthorityDecision(
        authorization_id=new_id("auth"),
        decision_id=snapshot.decision_id,
        scope_hash=snapshot.scope_hash,
        snapshot_hash=sha256_digest(snapshot.model_dump(mode="python")),
        all_predicates=snapshot.predicates,
        failed_predicates=tuple(failed),
        unknown_predicates=tuple(unknown),
        reason_codes=tuple(dict.fromkeys(reasons)),
        risk_state=snapshot.risk_state,
        capital_state=snapshot.capital_state,
        reconciliation_state=snapshot.reconciliation_state,
        certification_scope_match=snapshot.certification_scope_match,
        final_authorized=authorized,
        policy_versions=snapshot.policy_versions,
        computed_at=snapshot.computed_at,
    )
