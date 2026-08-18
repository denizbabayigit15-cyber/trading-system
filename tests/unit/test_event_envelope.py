from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from trading_system.contracts.models import EventEnvelope


def build_event(**overrides: object) -> EventEnvelope:
    values: dict[str, object] = {
        "event_type": "governance.system_governance_engine.failed.v1",
        "occurred_at": datetime(2026, 8, 18, tzinfo=UTC),
        "producer": "test-suite",
        "correlation_id": "corr_test",
        "payload": {"reason_code": "AUTH_LIVE_DISABLED"},
    }
    values.update(overrides)
    return EventEnvelope.model_validate(values)


def test_payload_hash_is_bound() -> None:
    first = build_event()
    second = build_event(event_id=first.event_id, produced_at=first.produced_at)
    assert first.payload_sha256 == second.payload_sha256
    assert first.payload_sha256 is not None
    assert len(first.payload_sha256) == 64


def test_wrong_payload_hash_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_event(payload_sha256="0" * 64)


def test_naive_timestamp_is_rejected() -> None:
    with pytest.raises(ValidationError):
        build_event(occurred_at=datetime(2026, 8, 18))
