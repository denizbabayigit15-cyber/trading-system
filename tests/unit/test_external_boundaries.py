from __future__ import annotations

from datetime import UTC, datetime

from trading_system.core.financial import FinancialNumber
from trading_system.external.reality import (
    CapabilitySnapshot,
    DecisionStatus,
    TreasuryState,
    build_route,
    evaluate_compliance,
    evaluate_counterparty,
    evaluate_entitlement,
)

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def capability(**changes: object) -> CapabilitySnapshot:
    values: dict[str, object] = {
        "provider_id": "paper",
        "venue_id": "paper-venue",
        "account_id": "paper-account",
        "as_of": NOW,
        "supported_order_types": frozenset({"LIMIT"}),
        "supports_paper": True,
        "supports_live": False,
        "fresh": True,
        "source_evidence_id": "evidence-1",
    }
    values.update(changes)
    return CapabilitySnapshot(**values)


def test_external_bindings_fail_closed_and_paper_route_can_be_exercised() -> None:
    missing = evaluate_entitlement("source", "LIVE", entitlement_id=None, expires_at=None, at=NOW)
    assert missing.status is DecisionStatus.BLOCKED
    route = build_route("route-1", "auth-1", capability(), order_type="LIMIT")
    assert route.status is DecisionStatus.PASS


def test_compliance_and_treasury_unknown_state_block() -> None:
    compliance = evaluate_compliance(
        "scope", applicable_law_bound=False, restricted_product_clear=True
    )
    assert compliance.status is DecisionStatus.BLOCKED
    treasury = TreasuryState(
        account_id="paper-account",
        cash=FinancialNumber(value="100", scale=2, unit="USD"),
        collateral=None,
        encumbered=FinancialNumber(value="0", scale=2, unit="USD"),
        settlement_known=False,
        reason_codes=("TREASURY_STATE_UNKNOWN",),
    )
    assert treasury.spendable is None
    counterparty = evaluate_counterparty("cp", exposure_limit=None, settlement_known=False)
    assert counterparty.status is DecisionStatus.BLOCKED
