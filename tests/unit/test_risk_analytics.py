from decimal import Decimal

from trading_system.risk.analytics import (
    MetricStatus,
    StressScenario,
    max_drawdown,
    mean_return,
    stress_exposure,
)


def test_risk_analytics_is_deterministic() -> None:
    returns = (Decimal("2"), Decimal("-5"), Decimal("1"))
    assert mean_return(returns).value == Decimal("-2") / Decimal("3")
    assert max_drawdown(returns).value == Decimal("-5")
    assert stress_exposure(
        {"A": Decimal("10")}, StressScenario(scenario_id="down", shocks={"A": Decimal("-0.2")})
    ).value == Decimal("-2")


def test_risk_analytics_unknown_without_samples() -> None:
    assert mean_return(()).status is MetricStatus.UNKNOWN
