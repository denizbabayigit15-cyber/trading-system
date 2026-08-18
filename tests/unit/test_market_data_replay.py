from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.feed import ConnectionState, FeedState, MarketEvent, SequenceTracker
from trading_system.replay.engine import SimulationClock, replay

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def event(sequence: int, *, available_offset: int = 0) -> MarketEvent:
    available = NOW + timedelta(microseconds=available_offset)
    return MarketEvent(
        provider="simulator",
        instrument_id="TEST",
        sequence=sequence,
        event_time=available,
        first_available_at=available,
        received_at=available,
        price=FinancialNumber(value="100.00", scale=2, unit="USD"),
        quantity=FinancialNumber(value="1", scale=0, unit="UNIT"),
    )


def test_feed_state_machine_cannot_skip_synchronization() -> None:
    connecting = FeedState().transition(ConnectionState.CONNECTING)
    with pytest.raises(ValueError):
        connecting.transition(ConnectionState.STREAMING)


def test_sequence_gap_and_duplicate_fail_closed() -> None:
    tracker = SequenceTracker()
    assert tracker.observe(event(10)).accepted
    gap = tracker.observe(event(12))
    assert not gap.accepted and gap.gap == (11, 11)
    assert tracker.observe(event(10)).duplicate
    assert tracker.observe(event(11)).accepted


def test_replay_is_deterministic_and_rejects_wrong_order() -> None:
    events = (event(1), event(2, available_offset=1))
    first = replay(events, lambda item: {"sequence": item.sequence})
    second = replay(events, lambda item: {"sequence": item.sequence})
    assert first == second
    with pytest.raises(ValueError):
        replay(tuple(reversed(events)), lambda item: item.sequence)


def test_simulation_clock_is_monotonic() -> None:
    clock = SimulationClock()
    clock.advance_to(NOW)
    with pytest.raises(ValueError):
        clock.advance_to(NOW - timedelta(seconds=1))
