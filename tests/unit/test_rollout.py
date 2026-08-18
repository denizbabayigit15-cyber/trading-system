from __future__ import annotations

import pytest

from trading_system.operations.rollout import (
    DeploymentMode,
    RolloutState,
    check_promotion,
)


def test_rollout_requires_sequential_evidence_backed_promotion() -> None:
    state = RolloutState()
    assert (
        check_promotion(
            state,
            DeploymentMode.SHADOW,
            required_evidence={"shadow"},
            available_evidence=set(),
            operational_health=True,
            live_authorized=False,
        ).allowed
        is False
    )
    promoted = state.promote(DeploymentMode.SHADOW, evidence_complete=True, live_authorized=False)
    assert promoted.mode is DeploymentMode.SHADOW


def test_live_promotion_is_hard_disabled_and_demotion_is_available() -> None:
    state = RolloutState(DeploymentMode.PROBATION, "v1", "test")
    with pytest.raises(PermissionError):
        state.promote(DeploymentMode.LIVE, evidence_complete=True, live_authorized=False)
    assert state.demote("KILL_SWITCH_ACTIVE").mode is DeploymentMode.DISABLED
