from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DeploymentMode(StrEnum):
    DISABLED = "DISABLED"
    SHADOW = "SHADOW"
    PAPER = "PAPER"
    MICRO = "MICRO"
    PROBATION = "PROBATION"
    LIVE = "LIVE"


_ORDER = {
    DeploymentMode.DISABLED: 0,
    DeploymentMode.SHADOW: 1,
    DeploymentMode.PAPER: 2,
    DeploymentMode.MICRO: 3,
    DeploymentMode.PROBATION: 4,
    DeploymentMode.LIVE: 5,
}


@dataclass(frozen=True, slots=True)
class PromotionCheck:
    allowed: bool
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RolloutState:
    mode: DeploymentMode = DeploymentMode.DISABLED
    version: str = "unbound"
    reason_code: str = "ROLLOUT_DISABLED"

    def promote(
        self,
        target: DeploymentMode,
        *,
        evidence_complete: bool,
        live_authorized: bool,
    ) -> RolloutState:
        if _ORDER[target] != _ORDER[self.mode] + 1:
            raise ValueError("rollout promotion must advance exactly one mode")
        if target is DeploymentMode.LIVE:
            raise PermissionError("live mode is disabled in this package")
        if not evidence_complete:
            raise PermissionError("promotion requires evidence")
        if live_authorized:
            raise PermissionError("live authority cannot be supplied by rollout state")
        return RolloutState(target, self.version, "ROLLOUT_PROMOTED")

    def demote(self, reason_code: str) -> RolloutState:
        if not reason_code:
            raise ValueError("demotion requires a reason code")
        return RolloutState(DeploymentMode.DISABLED, self.version, reason_code)


def check_promotion(
    current: RolloutState,
    target: DeploymentMode,
    *,
    required_evidence: set[str],
    available_evidence: set[str],
    operational_health: bool,
    live_authorized: bool,
) -> PromotionCheck:
    reasons: list[str] = []
    if _ORDER[target] != _ORDER[current.mode] + 1:
        reasons.append("ROLLOUT_ORDER_INVALID")
    if target is DeploymentMode.LIVE:
        reasons.append("AUTH_LIVE_DISABLED")
    if not required_evidence <= available_evidence:
        reasons.append("ROLLOUT_EVIDENCE_MISSING")
    if not operational_health:
        reasons.append("RECOVERY_HEALTH_NOT_VERIFIED")
    if live_authorized:
        reasons.append("ROLLOUT_LIVE_AUTHORITY_MUST_BE_EXTERNAL")
    return PromotionCheck(not reasons, tuple(reasons))
