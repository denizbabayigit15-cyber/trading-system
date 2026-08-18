from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from trading_system.research.validation import (
    StatisticalValidationResult,
    TrialRecord,
    TrialRegistry,
    ValidationStatus,
    purged_temporal_split,
    validate_returns,
)


def test_trial_registry_is_append_only() -> None:
    record = TrialRecord(
        trial_id="t1",
        strategy_id="s",
        strategy_version="1",
        dataset_id="d",
        hypothesis="test",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        synthetic=True,
    )
    registry = TrialRegistry()
    registry.register(record)
    assert registry.records() == (record,)
    with pytest.raises(ValueError):
        registry.register(record)


def test_temporal_split_purges_boundaries() -> None:
    stamps = tuple(datetime(2026, 1, 1, tzinfo=UTC) + timedelta(days=i) for i in range(10))
    split = purged_temporal_split(stamps, purge=1)
    assert split.train[-1] < split.validation[0]
    assert split.validation[-1] < split.test[0]


def test_validation_never_claims_independent_review() -> None:
    result = validate_returns((Decimal("1"), Decimal("-2"), Decimal("3")))
    assert isinstance(result, StatisticalValidationResult)
    assert result.status is ValidationStatus.BLOCKED
    assert result.independent_reviewed is False
    assert "INDEPENDENT_REVIEW_REQUIRED" in result.reason_codes
