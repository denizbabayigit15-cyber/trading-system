from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from trading_system.core.financial import FinancialNumber


class ActionClass(StrEnum):
    NEW_ENTRY = "NEW_ENTRY"
    POSITION_INCREASE = "POSITION_INCREASE"
    NORMAL_MODIFY = "NORMAL_MODIFY"
    RISK_REDUCTION = "RISK_REDUCTION"
    EMERGENCY_EXIT = "EMERGENCY_EXIT"
    KNOWN_ORDER_CANCEL = "KNOWN_ORDER_CANCEL"


class LimitBinding(BaseModel):
    """An explicit external risk limit. None is never interpreted as unlimited."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1)
    value: FinancialNumber | None
    version: str | None = None


class Exposure(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    gross: FinancialNumber
    net: FinancialNumber
    instrument: FinancialNumber
    margin: FinancialNumber


class RiskAssessment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    allowed: bool
    action: ActionClass
    reason_codes: tuple[str, ...]
    limit_versions: dict[str, str]


def assess_pre_trade(
    action: ActionClass,
    *,
    projected: Exposure,
    limits: tuple[LimitBinding, ...],
    kill_switch_active: bool,
    reconciliation_clean: bool,
) -> RiskAssessment:
    reasons: list[str] = []
    limit_map = {item.name: item for item in limits}
    required = {"gross", "net", "instrument", "margin"}
    missing = sorted(required - limit_map.keys())
    if missing or any(limit_map[name].value is None for name in required if name in limit_map):
        reasons.append("RISK_LIMIT_UNBOUND")
    else:
        values = {
            "gross": projected.gross.value,
            "net": abs(projected.net.value),
            "instrument": abs(projected.instrument.value),
            "margin": projected.margin.value,
        }
        for name, actual in values.items():
            bound = limit_map[name].value
            if bound is not None and actual > bound.value:
                reasons.append("RISK_LIMIT_EXCEEDED")
    if kill_switch_active:
        reasons.append("KILL_SWITCH_ACTIVE")
    if not reconciliation_clean:
        reasons.append("RECONCILIATION_REQUIRED")
    if (
        action
        in {
            ActionClass.NEW_ENTRY,
            ActionClass.POSITION_INCREASE,
            ActionClass.NORMAL_MODIFY,
        }
        and reasons
    ):
        return RiskAssessment(
            allowed=False,
            action=action,
            reason_codes=tuple(dict.fromkeys(reasons)),
            limit_versions={item.name: item.version for item in limits if item.version},
        )
    if action in {ActionClass.RISK_REDUCTION, ActionClass.EMERGENCY_EXIT}:
        safe_reasons = tuple(reason for reason in reasons if reason == "RISK_LIMIT_UNBOUND")
        return RiskAssessment(
            allowed=not safe_reasons,
            action=action,
            reason_codes=safe_reasons,
            limit_versions={item.name: item.version for item in limits if item.version},
        )
    return RiskAssessment(
        allowed=not reasons,
        action=action,
        reason_codes=tuple(dict.fromkeys(reasons)),
        limit_versions={item.name: item.version for item in limits if item.version},
    )


class SafetyState(StrEnum):
    TRADING_ENABLED = "TRADING_ENABLED"
    DEGRADED = "DEGRADED"
    SAFE_MODE = "SAFE_MODE"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"
    HALTED = "HALTED"


_SAFETY_RANK = {
    SafetyState.TRADING_ENABLED: 0,
    SafetyState.DEGRADED: 1,
    SafetyState.SAFE_MODE: 2,
    SafetyState.RECONCILIATION_REQUIRED: 3,
    SafetyState.HALTED: 4,
}


@dataclass(frozen=True, slots=True)
class KillSwitchState:
    global_state: SafetyState = SafetyState.SAFE_MODE
    account_state: SafetyState = SafetyState.SAFE_MODE
    venue_state: SafetyState = SafetyState.SAFE_MODE
    instrument_state: SafetyState = SafetyState.SAFE_MODE
    strategy_state: SafetyState = SafetyState.SAFE_MODE
    execution_state: SafetyState = SafetyState.SAFE_MODE

    @property
    def effective_state(self) -> SafetyState:
        return max(
            (
                self.global_state,
                self.account_state,
                self.venue_state,
                self.instrument_state,
                self.strategy_state,
                self.execution_state,
            ),
            key=_SAFETY_RANK.__getitem__,
        )

    @property
    def new_risk_blocked(self) -> bool:
        return self.effective_state is not SafetyState.TRADING_ENABLED

    def restrict_global(self, state: SafetyState) -> KillSwitchState:
        if _SAFETY_RANK[state] < _SAFETY_RANK[self.global_state]:
            raise ValueError("a kill switch cannot weaken the current global state")
        return KillSwitchState(
            global_state=state,
            account_state=self.account_state,
            venue_state=self.venue_state,
            instrument_state=self.instrument_state,
            strategy_state=self.strategy_state,
            execution_state=self.execution_state,
        )


@dataclass(frozen=True, slots=True)
class RecoveryCheck:
    allowed: bool
    reason_codes: tuple[str, ...]


def validate_recovery(
    current: KillSwitchState,
    *,
    health_ok: bool,
    reconciliation_clean: bool,
    authority_revalidated: bool,
) -> RecoveryCheck:
    reasons: list[str] = []
    if not health_ok:
        reasons.append("RECOVERY_HEALTH_NOT_VERIFIED")
    if not reconciliation_clean:
        reasons.append("RECONCILIATION_REQUIRED")
    if not authority_revalidated:
        reasons.append("RECOVERY_AUTHORITY_REVALIDATION_REQUIRED")
    if current.effective_state is SafetyState.HALTED:
        reasons.append("HALT_REQUIRES_MANUAL_RECOVERY")
    return RecoveryCheck(not reasons, tuple(reasons))
