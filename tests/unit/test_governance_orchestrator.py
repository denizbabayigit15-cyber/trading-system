from datetime import UTC, datetime

import pytest

from trading_system.governance.orchestrator import (
    GovernanceEvent,
    GovernanceOrchestrator,
    GovernanceState,
)


def test_governance_orchestrator_has_deterministic_immutable_lifecycle() -> None:
    orchestrator = GovernanceOrchestrator()
    event = GovernanceEvent(
        "e1", GovernanceState.ACTIVE, datetime(2026, 1, 1, tzinfo=UTC), "BOOTSTRAP"
    )
    orchestrator.transition(event)
    assert orchestrator.state is GovernanceState.ACTIVE
    with pytest.raises(ValueError):
        orchestrator.transition(event)
