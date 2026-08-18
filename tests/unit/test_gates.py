from trading_system.core.gates import evaluate_gate


def test_gate_reports_exact_missing_requirements() -> None:
    result = evaluate_gate("R4", ("BACKTEST", "INDEPENDENT_REVIEW"), frozenset({"BACKTEST"}))
    assert result.allowed is False
    assert result.missing == ("INDEPENDENT_REVIEW",)
