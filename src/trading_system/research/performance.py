from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from trading_system.risk.analytics import MetricStatus, RiskMetric, _unknown


@dataclass(frozen=True, slots=True)
class PerformancePoint:
    observed_at: datetime
    strategy_id: str
    value: Decimal
    benchmark: Decimal | None = None


class PerformanceSeries:
    def __init__(self) -> None:
        self._points: list[PerformancePoint] = []

    def append(self, point: PerformancePoint) -> None:
        if self._points and point.observed_at < self._points[-1].observed_at:
            raise ValueError("performance points must be monotonic")
        self._points.append(point)

    def points(self) -> tuple[PerformancePoint, ...]:
        return tuple(self._points)


@dataclass(frozen=True, slots=True)
class DecompositionRecord:
    subject_id: str
    dimension: str
    contribution: Decimal
    source_id: str


def decomposition_records(
    subject_id: str, returns: dict[str, Decimal], source_id: str
) -> tuple[DecompositionRecord, ...]:
    if not subject_id or not source_id or not returns:
        return ()
    return tuple(
        DecompositionRecord(subject_id, dimension, contribution, source_id)
        for dimension, contribution in sorted(returns.items())
    )


def decompose_returns(returns: dict[str, Decimal]) -> RiskMetric:
    if not returns:
        return _unknown("performance_decomposition", "PERFORMANCE_INPUT_MISSING")
    return RiskMetric(
        metric_id="performance_decomposition",
        status=MetricStatus.VALID,
        value=sum(returns.values(), Decimal("0")),
        sample_size=len(returns),
        reason_codes=(),
    )


def decay_state(
    recent: tuple[Decimal, ...], baseline: tuple[Decimal, ...], threshold: Decimal | None
) -> RiskMetric:
    if threshold is None or not recent or not baseline:
        return _unknown("strategy_decay", "DRIFT_INPUT_MISSING")
    recent_mean = sum(recent, Decimal("0")) / Decimal(len(recent))
    baseline_mean = sum(baseline, Decimal("0")) / Decimal(len(baseline))
    gap = baseline_mean - recent_mean
    return RiskMetric(
        metric_id="strategy_decay",
        status=MetricStatus.VALID,
        value=gap,
        sample_size=len(recent),
        reason_codes=("DECAY_ALERT",) if gap >= threshold else (),
    )


class SharedAlphaGraph:
    def __init__(self) -> None:
        self._edges: dict[str, set[str]] = {}

    def link(self, strategy_id: str, alpha_id: str) -> None:
        self._edges.setdefault(alpha_id, set()).add(strategy_id)

    def strategies_for(self, alpha_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._edges.get(alpha_id, set())))


@dataclass(frozen=True, slots=True)
class DriftBaseline:
    baseline_id: str
    version: str
    observations: tuple[Decimal, ...]


@dataclass(frozen=True, slots=True)
class DriftAlert:
    baseline_id: str
    current_version: str
    score: Decimal
    threshold: Decimal
    active: bool


class DriftMonitor:
    def compare(
        self,
        baseline: DriftBaseline,
        current_version: str,
        current: tuple[Decimal, ...],
        threshold: Decimal | None,
    ) -> DriftAlert | None:
        if threshold is None or not current or not baseline.observations:
            return None
        metric = drift_score(baseline.observations, current)
        if metric.value is None:
            return None
        return DriftAlert(
            baseline.baseline_id,
            current_version,
            metric.value,
            threshold,
            metric.value >= threshold,
        )


def attribution(
    strategy_returns: tuple[Decimal, ...], benchmark_returns: tuple[Decimal, ...]
) -> RiskMetric:
    if not strategy_returns or len(strategy_returns) != len(benchmark_returns):
        return _unknown("attribution", "PERFORMANCE_INPUT_MISSING")
    value = sum(
        (a - b for a, b in zip(strategy_returns, benchmark_returns, strict=True)), Decimal("0")
    )
    return RiskMetric(
        metric_id="attribution",
        status=MetricStatus.VALID,
        value=value,
        sample_size=len(strategy_returns),
        reason_codes=(),
    )


def drift_score(reference: tuple[Decimal, ...], current: tuple[Decimal, ...]) -> RiskMetric:
    if not reference or len(reference) != len(current):
        return _unknown("drift_score", "DRIFT_INPUT_MISSING")
    value = sum((abs(a - b) for a, b in zip(reference, current, strict=True)), Decimal("0"))
    return RiskMetric(
        metric_id="drift_score",
        status=MetricStatus.VALID,
        value=value,
        sample_size=len(reference),
        reason_codes=(),
    )


def correlation(first: tuple[Decimal, ...], second: tuple[Decimal, ...]) -> RiskMetric:
    if not first or len(first) != len(second):
        return _unknown("correlation", "CORRELATION_INPUT_MISSING")
    mean_first = sum(first, Decimal("0")) / Decimal(len(first))
    mean_second = sum(second, Decimal("0")) / Decimal(len(second))
    numerator = sum(
        (a - mean_first) * (b - mean_second) for a, b in zip(first, second, strict=True)
    )
    left = sum((a - mean_first) ** 2 for a in first)
    right = sum((b - mean_second) ** 2 for b in second)
    if left == 0 or right == 0:
        return _unknown("correlation", "CORRELATION_VARIANCE_ZERO")
    value = numerator / (left * right).sqrt()
    return RiskMetric(
        metric_id="correlation",
        status=MetricStatus.VALID,
        value=value,
        sample_size=len(first),
        reason_codes=(),
    )
