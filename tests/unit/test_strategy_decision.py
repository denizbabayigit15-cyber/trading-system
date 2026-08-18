from decimal import Decimal

from trading_system.research.strategy import DecisionStatus, evaluate_setup


def test_strategy_decision_requires_bound_inputs() -> None:
    assert (
        evaluate_setup(
            "s", alpha_score=None, minimum_score=None, dependencies_valid=True, no_trade=False
        ).status
        is DecisionStatus.UNKNOWN
    )
    assert (
        evaluate_setup(
            "s",
            alpha_score=Decimal("1"),
            minimum_score=Decimal("0"),
            dependencies_valid=True,
            no_trade=False,
        ).status
        is DecisionStatus.ALLOWED
    )
    assert (
        evaluate_setup(
            "s",
            alpha_score=Decimal("1"),
            minimum_score=Decimal("0"),
            dependencies_valid=True,
            no_trade=True,
        ).status
        is DecisionStatus.BLOCKED
    )
