from __future__ import annotations

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DecisionStatus(StrEnum):
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class StrategyDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    strategy_id: str = Field(min_length=1)
    status: DecisionStatus
    score: Decimal | None
    reason_codes: tuple[str, ...]


def evaluate_setup(
    strategy_id: str,
    *,
    alpha_score: Decimal | None,
    minimum_score: Decimal | None,
    dependencies_valid: bool,
    no_trade: bool,
) -> StrategyDecision:
    if no_trade:
        return StrategyDecision(
            strategy_id=strategy_id,
            status=DecisionStatus.BLOCKED,
            score=alpha_score,
            reason_codes=("NO_TRADE_CONDITION",),
        )
    if alpha_score is None or minimum_score is None:
        return StrategyDecision(
            strategy_id=strategy_id,
            status=DecisionStatus.UNKNOWN,
            score=alpha_score,
            reason_codes=("STRATEGY_INPUT_UNBOUND",),
        )
    if not dependencies_valid:
        return StrategyDecision(
            strategy_id=strategy_id,
            status=DecisionStatus.BLOCKED,
            score=alpha_score,
            reason_codes=("STRATEGY_DEPENDENCY_INVALID",),
        )
    status = DecisionStatus.ALLOWED if alpha_score >= minimum_score else DecisionStatus.BLOCKED
    reasons = () if status is DecisionStatus.ALLOWED else ("EDGE_BELOW_THRESHOLD",)
    return StrategyDecision(
        strategy_id=strategy_id, status=status, score=alpha_score, reason_codes=reasons
    )
