from decimal import Decimal

from trading_system.research.eligibility import strategy_eligible
from trading_system.research.statistics import expectancy, overfit_gap, probability_of_positive
from trading_system.research.validation import validate_returns


def test_research_statistics_and_eligibility_are_fail_closed() -> None:
    result = validate_returns((Decimal("2"), Decimal("1")), independent_reviewed=True)
    assert expectancy((Decimal("2"), Decimal("0"))).value == Decimal("1")
    assert probability_of_positive((Decimal("2"), Decimal("-1"))).value == Decimal("0.5")
    assert overfit_gap((Decimal("2"),), (Decimal("1"),)).value == Decimal("1")
    allowed, reasons = strategy_eligible(
        result,
        required_sample_size=2,
        required_mean_return=Decimal("0"),
        paper_evidence=True,
    )
    assert allowed is True
    assert reasons == ()
