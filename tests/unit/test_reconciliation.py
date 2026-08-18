from __future__ import annotations

from datetime import UTC, datetime

from trading_system.reconciliation.models import (
    ReconciliationStatus,
    SourceObservation,
    compare_sources,
)

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def source(source_id: str, digest: str) -> SourceObservation:
    return SourceObservation(
        source_id=source_id, version="v1", state_hash=digest * 64, observed_at=NOW
    )


def test_external_state_disagreement_requires_reconciliation() -> None:
    decision = compare_sources((source("internal", "a"), source("broker", "b")))
    assert decision.status is ReconciliationStatus.REQUIRED
    assert decision.resolution_evidence is None


def test_exact_external_state_agreement_is_clean() -> None:
    decision = compare_sources((source("internal", "a"), source("broker", "a")))
    assert decision.status is ReconciliationStatus.CLEAN
    assert decision.resolution_rule == "EXACT_STATE_HASH_MATCH"
