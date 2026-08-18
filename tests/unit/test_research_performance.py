from decimal import Decimal

from trading_system.research.performance import attribution, correlation, drift_score


def test_performance_metrics_are_deterministic() -> None:
    assert attribution((Decimal("2"), Decimal("1")), (Decimal("1"), Decimal("1"))).value == Decimal(
        "1"
    )
    assert drift_score((Decimal("1"),), (Decimal("3"),)).value == Decimal("2")
    assert correlation((Decimal("1"), Decimal("2")), (Decimal("2"), Decimal("4"))).value == Decimal(
        "1"
    )
