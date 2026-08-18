from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from trading_system.governance.identity import Principal, PrincipalKind, independently_approved
from trading_system.governance.policy import PolicySnapshot
from trading_system.governance.scope import MarketScopeCandidate, ScopeStatus, bind_scope

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def principal(principal_id: str, *roles: str) -> Principal:
    return Principal(
        principal_id=principal_id,
        kind=PrincipalKind.HUMAN,
        roles=frozenset(roles),
        authenticated_at=NOW - timedelta(minutes=1),
        expires_at=NOW + timedelta(minutes=1),
    )


def test_independent_approval_requires_distinct_active_approver() -> None:
    owner = principal("owner", "CONTROL_OWNER")
    approver = principal("reviewer", "INDEPENDENT_APPROVER")
    assert independently_approved(owner, approver, at=NOW)
    assert not independently_approved(owner, owner, at=NOW)


def test_invalid_identity_window_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Principal(
            principal_id="bad",
            kind=PrincipalKind.SERVICE,
            roles=frozenset({"SERVICE"}),
            authenticated_at=NOW,
            expires_at=NOW,
        )


def test_scope_binding_fails_closed_and_hashes_deterministically() -> None:
    blocked = bind_scope(MarketScopeCandidate())
    assert blocked.status is ScopeStatus.BLOCKED
    assert blocked.scope_hash is None
    assert blocked.reason_codes == ("SCOPE_EXTERNAL_BINDING_MISSING",)
    assert "jurisdiction" in blocked.missing_bindings

    candidate = MarketScopeCandidate(
        market_profile_id="profile-v1",
        jurisdiction="TEST-JURISDICTION",
        asset_class="EQUITY",
        universe_id="universe-v1",
        broker_id="paper-broker",
        venue_id="paper-venue",
        account_id="paper-account",
        data_entitlement_id="test-entitlement",
        policy_versions={"risk": "v1", "data": "v2"},
    )
    first = bind_scope(candidate)
    second = bind_scope(candidate)
    assert first.status is ScopeStatus.ACTIVE
    assert first.scope_hash == second.scope_hash


def test_unapproved_policy_never_becomes_active() -> None:
    policy = PolicySnapshot(
        policy_id="test-policy",
        version="v1",
        effective_at=NOW - timedelta(days=1),
        rules={"mode": "DENY"},
    )
    assert not policy.active_at(NOW)
    assert len(policy.policy_hash) == 64
