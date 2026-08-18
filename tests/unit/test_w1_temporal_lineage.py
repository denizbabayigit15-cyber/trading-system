from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from trading_system.data.lineage import LineageKind, LineageNode
from trading_system.data.temporal import ObservationTime, TemporalStatus, assess_temporal_truth

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def observation(**updates: datetime) -> ObservationTime:
    values = {
        "source_id": "source-1",
        "event_time": NOW - timedelta(seconds=3),
        "first_available_at": NOW - timedelta(seconds=2),
        "received_at": NOW - timedelta(seconds=1),
        "revision": "original",
        "lineage_id": "lin-1",
    }
    values.update(updates)
    return ObservationTime(**values)


def test_temporal_truth_accepts_fresh_point_in_time_observation() -> None:
    result = assess_temporal_truth(observation(), decision_time=NOW, max_age=timedelta(seconds=5))
    assert result.status is TemporalStatus.VALID


def test_temporal_truth_rejects_late_and_unbound_freshness() -> None:
    late = observation(received_at=NOW + timedelta(microseconds=1))
    result = assess_temporal_truth(late, decision_time=NOW, max_age=timedelta(seconds=5))
    assert result.status is TemporalStatus.RECEIVED_AFTER_DECISION
    unbound = assess_temporal_truth(observation(), decision_time=NOW, max_age=None)
    assert unbound.status is TemporalStatus.CLOCK_INVALID


def test_lineage_distinguishes_raw_and_derived_artifacts() -> None:
    raw = LineageNode(
        artifact_id="raw-1",
        kind=LineageKind.RAW,
        created_at=NOW,
        producer="ingestion",
        source_ids=(),
        content_sha256="a" * 64,
    )
    derived = LineageNode(
        artifact_id="feature-1",
        kind=LineageKind.DERIVED,
        created_at=NOW,
        producer="feature-engine",
        source_ids=(raw.artifact_id,),
        content_sha256="b" * 64,
        transformation="mid-price",
        transformation_version="1.0.0",
    )
    assert raw.lineage_hash != derived.lineage_hash


def test_raw_lineage_cannot_hide_a_transformation() -> None:
    with pytest.raises(ValidationError):
        LineageNode(
            artifact_id="raw-1",
            kind=LineageKind.RAW,
            created_at=NOW,
            producer="ingestion",
            source_ids=(),
            content_sha256="a" * 64,
            transformation="adjusted-close",
        )
