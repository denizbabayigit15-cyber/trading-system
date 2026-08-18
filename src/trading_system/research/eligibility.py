from __future__ import annotations

from decimal import Decimal

from trading_system.research.validation import StatisticalValidationResult, ValidationStatus


def strategy_eligible(
    validation: StatisticalValidationResult,
    *,
    required_sample_size: int,
    required_mean_return: Decimal,
    paper_evidence: bool,
) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if validation.status is not ValidationStatus.VALID:
        reasons.append("STRATEGY_VALIDATION_NOT_COMPLETE")
    if validation.sample_size < required_sample_size:
        reasons.append("STRATEGY_SAMPLE_INSUFFICIENT")
    if validation.mean_return is None or validation.mean_return < required_mean_return:
        reasons.append("STRATEGY_EXPECTANCY_UNBOUND_OR_INSUFFICIENT")
    if not paper_evidence:
        reasons.append("PAPER_EVIDENCE_REQUIRED")
    return not reasons, tuple(reasons)
