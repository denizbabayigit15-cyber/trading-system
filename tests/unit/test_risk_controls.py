from __future__ import annotations

import pytest

from trading_system.core.financial import FinancialNumber
from trading_system.risk.controls import (
    ActionClass,
    Exposure,
    KillSwitchState,
    LimitBinding,
    SafetyState,
    assess_pre_trade,
    validate_recovery,
)


def n(value: str) -> FinancialNumber:
    return FinancialNumber(value=value, scale=2, unit="USD")


def exposure() -> Exposure:
    return Exposure(gross=n("10"), net=n("2"), instrument=n("2"), margin=n("1"))


def limits() -> tuple[LimitBinding, ...]:
    return tuple(
        LimitBinding(name=name, value=n("100"), version="v1")
        for name in ("gross", "net", "instrument", "margin")
    )


def test_unbound_limits_deny_new_risk() -> None:
    result = assess_pre_trade(
        ActionClass.NEW_ENTRY,
        projected=exposure(),
        limits=(),
        kill_switch_active=False,
        reconciliation_clean=True,
    )
    assert not result.allowed
    assert result.reason_codes == ("RISK_LIMIT_UNBOUND",)


def test_risk_reduction_is_separate_but_unknown_limits_still_block() -> None:
    result = assess_pre_trade(
        ActionClass.RISK_REDUCTION,
        projected=exposure(),
        limits=limits(),
        kill_switch_active=True,
        reconciliation_clean=False,
    )
    assert result.allowed


def test_kill_switch_uses_most_restrictive_state_and_never_weakens() -> None:
    state = KillSwitchState(global_state=SafetyState.SAFE_MODE)
    assert state.effective_state is SafetyState.SAFE_MODE
    assert state.new_risk_blocked
    with pytest.raises(ValueError):
        state.restrict_global(SafetyState.TRADING_ENABLED)


def test_recovery_requires_health_reconciliation_and_authority() -> None:
    result = validate_recovery(
        KillSwitchState(global_state=SafetyState.RECONCILIATION_REQUIRED),
        health_ok=False,
        reconciliation_clean=False,
        authority_revalidated=False,
    )
    assert not result.allowed
    assert len(result.reason_codes) == 3
