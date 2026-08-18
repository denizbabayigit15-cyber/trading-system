from datetime import UTC, datetime, timedelta

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.feed import MarketEvent
from trading_system.market_data.quality import (
    DataSource,
    DataSourceRegistry,
    HistoricalDataLake,
    SourceState,
    assess_events,
)

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def event(sequence: int, offset: int = 0) -> MarketEvent:
    return MarketEvent(
        provider="paper",
        instrument_id="TEST",
        event_time=NOW + timedelta(seconds=offset),
        first_available_at=NOW + timedelta(seconds=offset),
        received_at=NOW + timedelta(seconds=offset),
        sequence=sequence,
        price=FinancialNumber(value="1", scale=2, unit="USD"),
        quantity=FinancialNumber(value="1", scale=0, unit="UNIT"),
    )


def test_quality_checks_fail_closed_and_detect_gaps() -> None:
    source = DataSource(
        source_id="s",
        provider="paper",
        version="1",
        state=SourceState.ENABLED,
        entitlement_bound=True,
    )
    report = assess_events(source, (event(1), event(3), event(3)), now=NOW, max_age_seconds=10)
    assert report.gaps == 1
    assert report.duplicate == 1
    assert "DATA_SEQUENCE_GAP" in report.reason_codes


def test_source_registry_is_explicit_and_append_only() -> None:
    registry = DataSourceRegistry()
    source = DataSource(source_id="s", provider="paper", version="1", state=SourceState.ENABLED)
    registry.register(source)
    assert registry.get("s") == source


def test_historical_lake_is_deterministically_queryable() -> None:
    lake = HistoricalDataLake()
    lake.append(event(2))
    lake.append(event(1))
    assert tuple(
        item.sequence
        for item in lake.query(instrument_id="TEST", start=NOW, end=NOW + timedelta(seconds=1))
    ) == (1, 2)
