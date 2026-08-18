from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal
from enum import StrEnum
from itertools import pairwise

from trading_system.risk.analytics import MetricStatus, RiskMetric, StressScenario, _unknown


def budget_remaining(budget: Decimal | None, allocated: Decimal) -> RiskMetric:
    if budget is None:
        return _unknown("budget_remaining", "RISK_LIMIT_UNBOUND")
    return RiskMetric(
        metric_id="budget_remaining",
        status=MetricStatus.VALID,
        value=budget - allocated,
        sample_size=1,
        reason_codes=(),
    )


def risk_of_ruin(capital: Decimal | None, loss_per_trade: Decimal | None) -> RiskMetric:
    if capital is None or loss_per_trade is None or capital <= 0 or loss_per_trade <= 0:
        return _unknown("risk_of_ruin", "RISK_LIMIT_UNBOUND")
    # This is a conservative deterministic bound, not a profitability claim.
    return RiskMetric(
        metric_id="risk_of_ruin",
        status=MetricStatus.VALID,
        value=min(Decimal("1"), loss_per_trade / capital),
        sample_size=1,
        reason_codes=(),
    )


def transaction_cost(quantity: Decimal, price: Decimal, fee_rate: Decimal) -> RiskMetric:
    if quantity < 0 or price < 0 or fee_rate < 0:
        return _unknown("transaction_cost", "RISK_INPUT_INVALID")
    return RiskMetric(
        metric_id="transaction_cost",
        status=MetricStatus.VALID,
        value=quantity * price * fee_rate,
        sample_size=1,
        reason_codes=(),
    )


def capacity_remaining(capacity: Decimal | None, utilized: Decimal) -> RiskMetric:
    if capacity is None:
        return _unknown("capacity_remaining", "RISK_LIMIT_UNBOUND")
    if utilized < 0:
        return _unknown("capacity_remaining", "RISK_INPUT_INVALID")
    return RiskMetric(
        metric_id="capacity_remaining",
        status=MetricStatus.VALID,
        value=capacity - utilized,
        sample_size=1,
        reason_codes=(),
    )


@dataclass(frozen=True, slots=True)
class BudgetNode:
    node_id: str
    parent_id: str | None
    limit: Decimal | None
    consumed: Decimal = Decimal("0")


class BudgetTree:
    def __init__(self) -> None:
        self._nodes: dict[str, BudgetNode] = {}

    def add(self, node: BudgetNode) -> None:
        if node.node_id in self._nodes or (node.parent_id and node.parent_id not in self._nodes):
            raise ValueError("invalid budget hierarchy")
        self._nodes[node.node_id] = node

    def remaining(self, node_id: str) -> RiskMetric:
        node = self._nodes[node_id]
        return budget_remaining(node.limit, node.consumed)


class DrawdownState(StrEnum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    HALTED = "HALTED"


def drawdown_state(
    drawdown: Decimal, warning: Decimal | None, halt: Decimal | None
) -> DrawdownState | None:
    if warning is None or halt is None:
        return None
    if drawdown >= halt:
        return DrawdownState.HALTED
    if drawdown >= warning:
        return DrawdownState.WARNING
    return DrawdownState.NORMAL


def quantile(values: tuple[Decimal, ...], probability: Decimal) -> RiskMetric:
    if not values or not Decimal("0") <= probability <= Decimal("1"):
        return _unknown("quantile", "RISK_SAMPLE_MISSING")
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(probability * Decimal(len(ordered) - 1)))
    return RiskMetric(
        metric_id="quantile",
        status=MetricStatus.VALID,
        value=ordered[index],
        sample_size=len(values),
        reason_codes=(),
    )


def cvar(values: tuple[Decimal, ...], probability: Decimal) -> RiskMetric:
    if not values or not Decimal("0") < probability <= Decimal("1"):
        return _unknown("cvar", "RISK_SAMPLE_MISSING")
    ordered = sorted(values)
    tail_count = max(
        1,
        int(
            ((Decimal("1") - probability) * Decimal(len(ordered))).to_integral_value(
                rounding=ROUND_CEILING
            )
        ),
    )
    return RiskMetric(
        metric_id="cvar",
        status=MetricStatus.VALID,
        value=sum(ordered[:tail_count], Decimal("0")) / Decimal(tail_count),
        sample_size=len(values),
        reason_codes=(),
    )


@dataclass(frozen=True, slots=True)
class MarginSchedule:
    instrument_id: str
    initial_rate: Decimal | None
    maintenance_rate: Decimal | None


@dataclass(frozen=True, slots=True)
class AllocationConstraint:
    instrument_id: str
    minimum: Decimal = Decimal("0")
    maximum: Decimal | None = None


@dataclass(frozen=True, slots=True)
class AllocationResult:
    allocations: dict[str, Decimal]
    objective_value: Decimal
    feasible: bool
    reason_code: str | None = None


def optimize_allocation(
    capital: Decimal | None,
    scores: dict[str, Decimal],
    constraints: tuple[AllocationConstraint, ...],
) -> AllocationResult:
    if capital is None or capital < 0 or not scores:
        return AllocationResult({}, Decimal("0"), False, "ALLOCATION_INPUT_UNBOUND")
    bounds = {item.instrument_id: item for item in constraints}
    if set(bounds) != set(scores):
        return AllocationResult({}, Decimal("0"), False, "ALLOCATION_CONSTRAINT_MISSING")
    if any(
        item.minimum < 0 or (item.maximum is not None and item.maximum < item.minimum)
        for item in constraints
    ):
        return AllocationResult({}, Decimal("0"), False, "ALLOCATION_CONSTRAINT_INVALID")
    minimum_total = sum((item.minimum for item in constraints), Decimal("0"))
    maximum_total = sum(
        (item.maximum if item.maximum is not None else capital for item in constraints),
        Decimal("0"),
    )
    if minimum_total > capital or maximum_total < capital:
        return AllocationResult({}, Decimal("0"), False, "ALLOCATION_INFEASIBLE")
    allocation = {item.instrument_id: item.minimum for item in constraints}
    remaining = capital - minimum_total
    for instrument_id in sorted(scores, key=lambda key: (-scores[key], key)):
        room = bounds[instrument_id].maximum
        available = remaining if room is None else min(remaining, room - allocation[instrument_id])
        allocation[instrument_id] += available
        remaining -= available
        if remaining == 0:
            break
    if remaining != 0:
        return AllocationResult({}, Decimal("0"), False, "ALLOCATION_INFEASIBLE")
    objective = sum((allocation[key] * scores[key] for key in allocation), Decimal("0"))
    return AllocationResult(allocation, objective, True)


def margin_required(notional: Decimal, schedule: MarginSchedule) -> RiskMetric:
    if schedule.initial_rate is None or schedule.maintenance_rate is None:
        return _unknown("margin_required", "MARGIN_SCHEDULE_UNBOUND")
    return RiskMetric(
        metric_id="margin_required",
        status=MetricStatus.VALID,
        value=notional * schedule.initial_rate,
        sample_size=1,
        reason_codes=(),
    )


def covariance(first: tuple[Decimal, ...], second: tuple[Decimal, ...]) -> RiskMetric:
    if not first or len(first) != len(second) or len(first) < 2:
        return _unknown("covariance", "RISK_SAMPLE_MISSING")
    left = sum(first, Decimal("0")) / Decimal(len(first))
    right = sum(second, Decimal("0")) / Decimal(len(second))
    value = sum((a - left) * (b - right) for a, b in zip(first, second, strict=True)) / Decimal(
        len(first) - 1
    )
    return RiskMetric(
        metric_id="covariance",
        status=MetricStatus.VALID,
        value=value,
        sample_size=len(first),
        reason_codes=(),
    )


def allocate_capital(
    capital: Decimal | None, weights: dict[str, Decimal]
) -> dict[str, Decimal] | None:
    if capital is None or not weights or any(value < 0 for value in weights.values()):
        return None
    total = sum(weights.values(), Decimal("0"))
    if total <= 0:
        return None
    return {key: capital * value / total for key, value in weights.items()}


def impact_estimate(
    quantity: Decimal, displayed_liquidity: Decimal, coefficient: Decimal | None
) -> RiskMetric:
    if coefficient is None or displayed_liquidity <= 0 or quantity < 0:
        return _unknown("impact_estimate", "IMPACT_CALIBRATION_UNBOUND")
    return RiskMetric(
        metric_id="impact_estimate",
        status=MetricStatus.VALID,
        value=coefficient * quantity / displayed_liquidity,
        sample_size=1,
        reason_codes=(),
    )


@dataclass(frozen=True, slots=True)
class ImpactCurve:
    points: tuple[tuple[Decimal, Decimal], ...]

    def estimate(self, participation: Decimal) -> RiskMetric:
        if participation < 0 or not self.points or any(x < 0 for x, _ in self.points):
            return _unknown("impact_curve", "IMPACT_INPUT_INVALID")
        ordered = tuple(sorted(self.points))
        if participation > ordered[-1][0]:
            return _unknown("impact_curve", "IMPACT_CALIBRATION_UNBOUND")
        for (left_x, left_y), (right_x, right_y) in pairwise(ordered):
            if left_x <= participation <= right_x:
                if right_x == left_x:
                    return RiskMetric(
                        metric_id="impact_curve",
                        status=MetricStatus.VALID,
                        value=right_y,
                        sample_size=1,
                        reason_codes=(),
                    )
                fraction = (participation - left_x) / (right_x - left_x)
                value = left_y + fraction * (right_y - left_y)
                return RiskMetric(
                    metric_id="impact_curve",
                    status=MetricStatus.VALID,
                    value=value,
                    sample_size=1,
                    reason_codes=(),
                )
        return RiskMetric(
            metric_id="impact_curve",
            status=MetricStatus.VALID,
            value=ordered[-1][1],
            sample_size=1,
            reason_codes=(),
        )


def stress_portfolio(exposures: dict[str, Decimal], scenario: StressScenario) -> RiskMetric:
    from trading_system.risk.analytics import stress_exposure

    return stress_exposure(exposures, scenario)
