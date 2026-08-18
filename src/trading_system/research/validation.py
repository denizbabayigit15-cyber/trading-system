from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ValidationStatus(StrEnum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"
    BLOCKED = "BLOCKED"


class TrialRecord(BaseModel):
    """Immutable registration of a research trial; results are never inferred."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    trial_id: str = Field(min_length=1)
    strategy_id: str = Field(min_length=1)
    strategy_version: str = Field(min_length=1)
    dataset_id: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    created_at: datetime
    synthetic: bool


class TrialRegistry:
    def __init__(self) -> None:
        self._records: dict[str, TrialRecord] = {}

    def register(self, record: TrialRecord) -> None:
        if record.trial_id in self._records:
            raise ValueError("trial_id already registered")
        self._records[record.trial_id] = record

    def get(self, trial_id: str) -> TrialRecord:
        return self._records[trial_id]

    def records(self) -> tuple[TrialRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))


@dataclass(frozen=True, slots=True)
class TemporalSplit:
    train: tuple[datetime, ...]
    validation: tuple[datetime, ...]
    test: tuple[datetime, ...]


def purged_temporal_split(
    timestamps: tuple[datetime, ...],
    *,
    train_fraction: Decimal = Decimal("0.6"),
    validation_fraction: Decimal = Decimal("0.2"),
    purge: int = 0,
) -> TemporalSplit:
    if not timestamps:
        raise ValueError("timestamps cannot be empty")
    if not Decimal("0") < train_fraction < Decimal("1"):
        raise ValueError("train_fraction must be between zero and one")
    if not Decimal("0") < validation_fraction < Decimal("1"):
        raise ValueError("validation_fraction must be between zero and one")
    if train_fraction + validation_fraction >= Decimal("1") or purge < 0:
        raise ValueError("fractions must leave a test set and purge must be non-negative")
    ordered = tuple(sorted(timestamps))
    train_end = max(1, int(len(ordered) * train_fraction))
    validation_end = max(train_end + 1, int(len(ordered) * (train_fraction + validation_fraction)))
    validation_start = min(len(ordered), train_end + purge)
    test_start = min(len(ordered), validation_end + purge)
    return TemporalSplit(
        train=ordered[:train_end],
        validation=ordered[validation_start:validation_end],
        test=ordered[test_start:],
    )


class StatisticalValidationResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: ValidationStatus
    sample_size: int = Field(ge=0)
    mean_return: Decimal | None
    max_drawdown: Decimal | None
    reason_codes: tuple[str, ...]
    independent_reviewed: bool = False


def validate_returns(
    returns: tuple[Decimal, ...], *, independent_reviewed: bool = False
) -> StatisticalValidationResult:
    if not returns:
        return StatisticalValidationResult(
            status=ValidationStatus.UNKNOWN,
            sample_size=0,
            mean_return=None,
            max_drawdown=None,
            reason_codes=("VALIDATION_SAMPLE_MISSING",),
            independent_reviewed=independent_reviewed,
        )
    equity = Decimal("0")
    peak = Decimal("0")
    drawdown = Decimal("0")
    for value in returns:
        equity += value
        peak = max(peak, equity)
        drawdown = min(drawdown, equity - peak)
    reasons = () if independent_reviewed else ("INDEPENDENT_REVIEW_REQUIRED",)
    return StatisticalValidationResult(
        status=ValidationStatus.VALID if independent_reviewed else ValidationStatus.BLOCKED,
        sample_size=len(returns),
        mean_return=sum(returns, Decimal("0")) / Decimal(len(returns)),
        max_drawdown=drawdown,
        reason_codes=reasons,
        independent_reviewed=independent_reviewed,
    )


def utc_now() -> datetime:
    return datetime.now(UTC)
