from __future__ import annotations

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class MetricStatus(StrEnum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"


class RiskMetric(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    metric_id: str = Field(min_length=1)
    status: MetricStatus
    value: Decimal | None
    sample_size: int = Field(ge=0)
    reason_codes: tuple[str, ...]


class StressScenario(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    scenario_id: str = Field(min_length=1)
    shocks: dict[str, Decimal]


def _unknown(metric_id: str, reason: str) -> RiskMetric:
    return RiskMetric(
        metric_id=metric_id,
        status=MetricStatus.UNKNOWN,
        value=None,
        sample_size=0,
        reason_codes=(reason,),
    )


def mean_return(returns: tuple[Decimal, ...]) -> RiskMetric:
    if not returns:
        return _unknown("mean_return", "RISK_SAMPLE_MISSING")
    return RiskMetric(
        metric_id="mean_return",
        status=MetricStatus.VALID,
        value=sum(returns, Decimal("0")) / Decimal(len(returns)),
        sample_size=len(returns),
        reason_codes=(),
    )


def max_drawdown(returns: tuple[Decimal, ...]) -> RiskMetric:
    if not returns:
        return _unknown("max_drawdown", "RISK_SAMPLE_MISSING")
    equity = Decimal("0")
    peak = Decimal("0")
    drawdown = Decimal("0")
    for value in returns:
        equity += value
        peak = max(peak, equity)
        drawdown = min(drawdown, equity - peak)
    return RiskMetric(
        metric_id="max_drawdown",
        status=MetricStatus.VALID,
        value=drawdown,
        sample_size=len(returns),
        reason_codes=(),
    )


def stress_exposure(exposures: dict[str, Decimal], scenario: StressScenario) -> RiskMetric:
    if not exposures:
        return _unknown("stress_exposure", "RISK_EXPOSURE_MISSING")
    value = sum(
        (
            exposures[instrument] * shock
            for instrument, shock in scenario.shocks.items()
            if instrument in exposures
        ),
        Decimal("0"),
    )
    return RiskMetric(
        metric_id="stress_exposure",
        status=MetricStatus.VALID,
        value=value,
        sample_size=len(exposures),
        reason_codes=(),
    )
