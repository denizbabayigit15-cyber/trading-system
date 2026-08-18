from datetime import UTC, datetime
from decimal import Decimal

from trading_system.research.performance import (
    DriftBaseline,
    DriftMonitor,
    PerformancePoint,
    PerformanceSeries,
    SharedAlphaGraph,
    decay_state,
    decompose_returns,
    decomposition_records,
)


def test_performance_governance_semantics_are_deterministic() -> None:
    series = PerformanceSeries()
    series.append(PerformancePoint(datetime(2026, 1, 1, tzinfo=UTC), "s", Decimal("1")))
    assert len(series.points()) == 1
    assert decompose_returns({"fees": Decimal("-1"), "pnl": Decimal("3")}).value == Decimal("2")
    assert tuple(
        record.dimension
        for record in decomposition_records("s", {"fees": Decimal("-1"), "pnl": Decimal("3")}, "e")
    ) == ("fees", "pnl")
    assert decay_state((Decimal("1"),), (Decimal("2"),), Decimal("0.5")).value == Decimal("1")
    graph = SharedAlphaGraph()
    graph.link("s1", "a")
    graph.link("s2", "a")
    assert graph.strategies_for("a") == ("s1", "s2")
    alert = DriftMonitor().compare(
        DriftBaseline("b", "1", (Decimal("1"),)), "2", (Decimal("2"),), Decimal("0.5")
    )
    assert alert is not None and alert.active
