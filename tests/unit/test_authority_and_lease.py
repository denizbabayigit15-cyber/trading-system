from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

from trading_system.authority.evaluator import (
    AuthoritySnapshot,
    PredicateValue,
    evaluate_authority,
)
from trading_system.authority.lease import AuthorizationLeaseStore, VersionBindings

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def snapshot(**changes: object) -> AuthoritySnapshot:
    values: dict[str, object] = {
        "decision_id": "decision-1",
        "scope_hash": "scope-1",
        "state_snapshot_id": "state-1",
        "market_snapshot_id": "market-1",
        "predicates": {"risk": PredicateValue.PASS, "data": PredicateValue.PASS},
        "hard_predicates": frozenset({"risk", "data"}),
        "policy_versions": {"risk": "v1"},
        "risk_state": "PASS",
        "capital_state": "PASS",
        "reconciliation_state": "CLEAN",
        "certification_scope_match": True,
        "r4_certified": True,
        "live_authorized": True,
        "computed_at": NOW,
    }
    values.update(changes)
    return AuthoritySnapshot(**values)


def bindings() -> VersionBindings:
    return VersionBindings("scope-1", "state-1", "market-1", "p1", "pos1", "rec1", "ph1", "r1")


def test_unknown_and_live_disabled_both_deny_authority() -> None:
    unknown = snapshot(predicates={"risk": PredicateValue.UNKNOWN, "data": PredicateValue.PASS})
    result = evaluate_authority(unknown)
    assert not result.final_authorized
    assert "risk" in result.unknown_predicates

    disabled = evaluate_authority(snapshot(live_authorized=False))
    assert not disabled.final_authorized
    assert "AUTH_LIVE_DISABLED" in disabled.reason_codes


def test_lease_is_version_bound_and_single_use() -> None:
    decision = evaluate_authority(snapshot())
    store = AuthorizationLeaseStore()
    issued = store.issue(decision, bindings(), issued_at=NOW, ttl=timedelta(seconds=1))
    assert issued.allowed and issued.lease is not None

    mismatch = replace(bindings(), position_version="pos2")
    denied = store.consume(
        issued.lease.lease_id,
        mismatch,
        consumed_at=NOW + timedelta(milliseconds=1),
        safety_predicates_pass=True,
    )
    assert not denied.allowed
    assert denied.reason_code == "LEASE_VERSION_MISMATCH"

    consumed = store.consume(
        issued.lease.lease_id,
        bindings(),
        consumed_at=NOW + timedelta(milliseconds=2),
        safety_predicates_pass=True,
    )
    assert consumed.allowed
    duplicate = store.consume(
        issued.lease.lease_id,
        bindings(),
        consumed_at=NOW + timedelta(milliseconds=3),
        safety_predicates_pass=True,
    )
    assert not duplicate.allowed
    assert duplicate.reason_code == "LEASE_ALREADY_CONSUMED"


def test_denied_authority_cannot_issue_lease() -> None:
    store = AuthorizationLeaseStore()
    denied = store.issue(
        evaluate_authority(snapshot(live_authorized=False)),
        bindings(),
        issued_at=NOW,
        ttl=timedelta(seconds=1),
    )
    assert not denied.allowed
    assert denied.lease is None
