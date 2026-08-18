from decimal import Decimal

from trading_system.risk.analytics import MetricStatus
from trading_system.risk.portfolio import (
    AllocationConstraint,
    BudgetNode,
    BudgetTree,
    DrawdownState,
    ImpactCurve,
    MarginSchedule,
    allocate_capital,
    covariance,
    cvar,
    drawdown_state,
    impact_estimate,
    margin_required,
    optimize_allocation,
    quantile,
)


def test_portfolio_engine_semantics_are_deterministic() -> None:
    tree = BudgetTree()
    tree.add(BudgetNode("root", None, Decimal("100"), Decimal("20")))
    tree.add(BudgetNode("child", "root", Decimal("50"), Decimal("10")))
    assert tree.remaining("child").value == Decimal("40")
    assert drawdown_state(Decimal("0.2"), Decimal("0.1"), Decimal("0.2")) is DrawdownState.HALTED
    assert quantile((Decimal("1"), Decimal("2"), Decimal("3")), Decimal("0.5")).value == Decimal(
        "2"
    )
    assert cvar((Decimal("-3"), Decimal("-1"), Decimal("2")), Decimal("0.5")).value == Decimal("-2")
    assert margin_required(
        Decimal("100"), MarginSchedule("x", Decimal("0.1"), Decimal("0.05"))
    ).value == Decimal("10")
    assert covariance((Decimal("1"), Decimal("2")), (Decimal("2"), Decimal("4"))).value == Decimal(
        "1"
    )
    assert allocate_capital(Decimal("100"), {"a": Decimal("1"), "b": Decimal("1")}) == {
        "a": Decimal("50"),
        "b": Decimal("50"),
    }
    assert impact_estimate(Decimal("2"), Decimal("10"), None).status is MetricStatus.UNKNOWN
    allocation = optimize_allocation(
        Decimal("100"),
        {"a": Decimal("2"), "b": Decimal("1")},
        (AllocationConstraint("a", maximum=Decimal("60")), AllocationConstraint("b")),
    )
    assert allocation.feasible and allocation.allocations == {
        "a": Decimal("60"),
        "b": Decimal("40"),
    }
    assert ImpactCurve(((Decimal("0"), Decimal("0")), (Decimal("1"), Decimal("2")))).estimate(
        Decimal("0.5")
    ).value == Decimal("1")
