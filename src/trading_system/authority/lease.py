from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from threading import Lock

from trading_system.authority.evaluator import AuthorityDecision
from trading_system.core.ids import new_id
from trading_system.core.time import require_utc


@dataclass(frozen=True, slots=True)
class VersionBindings:
    scope_hash: str
    state_snapshot_id: str
    market_snapshot_id: str
    portfolio_version: str
    position_version: str
    reconciliation_version: str
    policy_hash: str
    release_hash: str


@dataclass(frozen=True, slots=True)
class AuthorizationLease:
    lease_id: str
    authorization_id: str
    bindings: VersionBindings
    issued_at: datetime
    expires_at: datetime
    single_use: bool = True
    consumed_at: datetime | None = None
    revoked_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class LeaseResult:
    allowed: bool
    reason_code: str
    lease: AuthorizationLease | None


class AuthorizationLeaseStore:
    """In-memory boundary preserving production compare-and-set semantics."""

    def __init__(self) -> None:
        self._leases: dict[str, AuthorizationLease] = {}
        self._lock = Lock()

    def issue(
        self,
        decision: AuthorityDecision,
        bindings: VersionBindings,
        *,
        issued_at: datetime,
        ttl: timedelta,
    ) -> LeaseResult:
        now = require_utc(issued_at)
        if not decision.final_authorized:
            return LeaseResult(False, "LEASE_AUTHORITY_DENIED", None)
        if decision.scope_hash != bindings.scope_hash:
            return LeaseResult(False, "LEASE_SCOPE_MISMATCH", None)
        if ttl <= timedelta(0):
            return LeaseResult(False, "LEASE_INVALID_TTL", None)
        lease = AuthorizationLease(
            lease_id=new_id("lease"),
            authorization_id=decision.authorization_id,
            bindings=bindings,
            issued_at=now,
            expires_at=now + ttl,
        )
        with self._lock:
            self._leases[lease.lease_id] = lease
        return LeaseResult(True, "LEASE_ISSUED", lease)

    def consume(
        self,
        lease_id: str,
        current: VersionBindings,
        *,
        consumed_at: datetime,
        safety_predicates_pass: bool,
    ) -> LeaseResult:
        now = require_utc(consumed_at)
        with self._lock:
            lease = self._leases.get(lease_id)
            if lease is None:
                return LeaseResult(False, "LEASE_NOT_FOUND", None)
            if lease.revoked_at is not None:
                return LeaseResult(False, "LEASE_REVOKED", lease)
            if lease.consumed_at is not None:
                return LeaseResult(False, "LEASE_ALREADY_CONSUMED", lease)
            if now >= lease.expires_at:
                return LeaseResult(False, "LEASE_EXPIRED", lease)
            if lease.bindings != current:
                return LeaseResult(False, "LEASE_VERSION_MISMATCH", lease)
            if not safety_predicates_pass:
                return LeaseResult(False, "LEASE_SAFETY_PREDICATE_FAILED", lease)
            consumed = replace(lease, consumed_at=now)
            self._leases[lease_id] = consumed
            return LeaseResult(True, "LEASE_CONSUMED", consumed)

    def revoke(self, lease_id: str, *, revoked_at: datetime) -> LeaseResult:
        now = require_utc(revoked_at)
        with self._lock:
            lease = self._leases.get(lease_id)
            if lease is None:
                return LeaseResult(False, "LEASE_NOT_FOUND", None)
            if lease.revoked_at is not None:
                return LeaseResult(False, "LEASE_ALREADY_REVOKED", lease)
            revoked = replace(lease, revoked_at=now)
            self._leases[lease_id] = revoked
            return LeaseResult(True, "LEASE_REVOKED", revoked)

    def snapshot(self) -> tuple[AuthorizationLease, ...]:
        """Return a deterministic recovery image; callers persist it transactionally."""
        with self._lock:
            return tuple(sorted(self._leases.values(), key=lambda lease: lease.lease_id))

    def restore(self, leases: tuple[AuthorizationLease, ...]) -> None:
        with self._lock:
            if len({lease.lease_id for lease in leases}) != len(leases):
                raise ValueError("lease recovery image contains duplicate IDs")
            self._leases = {lease.lease_id: lease for lease in leases}
