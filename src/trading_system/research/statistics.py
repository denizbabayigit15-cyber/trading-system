from __future__ import annotations

from decimal import Decimal

from trading_system.risk.analytics import MetricStatus, RiskMetric, _unknown


def expectancy(outcomes: tuple[Decimal, ...]) -> RiskMetric:
    if not outcomes:
        return _unknown("expectancy", "VALIDATION_SAMPLE_MISSING")
    return RiskMetric(
        metric_id="expectancy",
        status=MetricStatus.VALID,
        value=sum(outcomes, Decimal("0")) / Decimal(len(outcomes)),
        sample_size=len(outcomes),
        reason_codes=(),
    )


def probability_of_positive(outcomes: tuple[Decimal, ...]) -> RiskMetric:
    if not outcomes:
        return _unknown("probability_positive", "VALIDATION_SAMPLE_MISSING")
    positive = sum(1 for outcome in outcomes if outcome > 0)
    return RiskMetric(
        metric_id="probability_positive",
        status=MetricStatus.VALID,
        value=Decimal(positive) / Decimal(len(outcomes)),
        sample_size=len(outcomes),
        reason_codes=(),
    )


def overfit_gap(train: tuple[Decimal, ...], test: tuple[Decimal, ...]) -> RiskMetric:
    if not train or not test:
        return _unknown("overfit_gap", "VALIDATION_SAMPLE_MISSING")
    train_mean = sum(train, Decimal("0")) / Decimal(len(train))
    test_mean = sum(test, Decimal("0")) / Decimal(len(test))
    return RiskMetric(
        metric_id="overfit_gap",
        status=MetricStatus.VALID,
        value=train_mean - test_mean,
        sample_size=len(test),
        reason_codes=(),
    )
