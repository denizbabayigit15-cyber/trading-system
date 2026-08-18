from __future__ import annotations

from datetime import UTC, datetime, timedelta

from trading_system.authority.evaluator import AuthoritySnapshot, PredicateValue, evaluate_authority
from trading_system.authority.lease import AuthorizationLeaseStore, VersionBindings

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def test_lease_recovery_image_preserves_consumed_state() -> None:
    snapshot = AuthoritySnapshot(
        decision_id="d",
        scope_hash="scope",
        state_snapshot_id="state",
        market_snapshot_id="market",
        predicates={"risk": PredicateValue.PASS},
        hard_predicates=frozenset({"risk"}),
        policy_versions={"risk": "v1"},
        risk_state="PASS",
        capital_state="PASS",
        reconciliation_state="CLEAN",
        certification_scope_match=True,
        r4_certified=True,
        live_authorized=True,
        computed_at=NOW,
    )
    decision = evaluate_authority(snapshot)
    bindings = VersionBindings("scope", "state", "market", "p", "pos", "rec", "policy", "release")
    first = AuthorizationLeaseStore()
    issued = first.issue(decision, bindings, issued_at=NOW, ttl=timedelta(minutes=1))
    assert issued.lease is not None
    consumed = first.consume(
        issued.lease.lease_id,
        bindings,
        consumed_at=NOW + timedelta(seconds=1),
        safety_predicates_pass=True,
    )
    assert consumed.allowed
    recovered = AuthorizationLeaseStore()
    recovered.restore(first.snapshot())
    duplicate = recovered.consume(
        issued.lease.lease_id,
        bindings,
        consumed_at=NOW + timedelta(seconds=2),
        safety_predicates_pass=True,
    )
    assert not duplicate.allowed
    assert duplicate.reason_code == "LEASE_ALREADY_CONSUMED"
