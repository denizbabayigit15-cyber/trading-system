from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.feed import MarketEvent
from trading_system.market_data.ingestion import HistoricalIngestion, InMemoryRawEventStore
from trading_system.market_data.models import (
    InstrumentIdentity,
    InstrumentType,
    normalize_financial,
)

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def instrument() -> InstrumentIdentity:
    return InstrumentIdentity(
        instrument_id="equity:test",
        symbol="TEST",
        instrument_type=InstrumentType.EQUITY,
        venue_id="paper",
        currency="USD",
        tick_size=FinancialNumber(value="0.01", scale=2, unit="USD"),
        quantity_step=FinancialNumber(value="1", scale=0, unit="UNIT"),
        valid_from=NOW,
        valid_to=None,
    )


def event(sequence: int) -> MarketEvent:
    return MarketEvent(
        provider="historical-synthetic",
        instrument_id=instrument().instrument_id,
        sequence=sequence,
        event_time=NOW,
        first_available_at=NOW,
        received_at=NOW,
        price=FinancialNumber(value="10", scale=2, unit="USD"),
        quantity=FinancialNumber(value="1", scale=0, unit="UNIT"),
    )


def test_normalization_rejects_float_and_ingestion_quarantines_gaps() -> None:
    with pytest.raises(ValidationError):
        normalize_financial(1.25, scale=2, unit="USD")
    store = InMemoryRawEventStore()
    results = HistoricalIngestion(store).ingest((event(1), event(3), event(2)))
    assert [result.accepted for result in results] == [True, False, True]
    assert [item.sequence for item in store.events()] == [1, 2]
