from decimal import Decimal

from trading_system.risk.analytics import MetricStatus
from trading_system.risk.portfolio import (
    budget_remaining,
    capacity_remaining,
    risk_of_ruin,
    transaction_cost,
)


def test_portfolio_risk_requires_bound_limits() -> None:
    assert budget_remaining(None, Decimal("1")).status is MetricStatus.UNKNOWN
    assert risk_of_ruin(Decimal("100"), Decimal("2")).value == Decimal("0.02")
    assert transaction_cost(Decimal("10"), Decimal("5"), Decimal("0.01")).value == Decimal("0.5")
    assert capacity_remaining(Decimal("10"), Decimal("3")).value == Decimal("7")
