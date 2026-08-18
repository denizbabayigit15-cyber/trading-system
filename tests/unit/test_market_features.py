from __future__ import annotations

from datetime import UTC, datetime, timedelta

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.features import (
    FeatureStatus,
    FeatureWindow,
    MarketFeatureEngine,
)
from trading_system.market_data.models import (
    InstrumentIdentity,
    InstrumentType,
    Quote,
    Trade,
)

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def instrument() -> InstrumentIdentity:
    return InstrumentIdentity(
        instrument_id="test",
        symbol="TEST",
        instrument_type=InstrumentType.EQUITY,
        venue_id="paper",
        currency="USD",
        tick_size=FinancialNumber(value="0.01", scale=2, unit="USD"),
        quantity_step=FinancialNumber(value="1", scale=0, unit="UNIT"),
        valid_from=NOW,
        valid_to=None,
    )


def quote(sequence: int) -> Quote:
    return Quote(
        instrument=instrument(),
        bid=FinancialNumber(value="99", scale=2, unit="USD"),
        ask=FinancialNumber(value="101", scale=2, unit="USD"),
        bid_size=FinancialNumber(value="2", scale=0, unit="UNIT"),
        ask_size=FinancialNumber(value="3", scale=0, unit="UNIT"),
        event_time=NOW,
        sequence=sequence,
    )


def trade(sequence: int, price: str) -> Trade:
    return Trade(
        instrument=instrument(),
        price=FinancialNumber(value=price, scale=2, unit="USD"),
        quantity=FinancialNumber(value="1", scale=0, unit="UNIT"),
        event_time=NOW + timedelta(seconds=sequence),
        sequence=sequence,
        trade_id=f"trade-{sequence}",
    )


def test_feature_engine_is_deterministic_and_raw_only() -> None:
    engine = MarketFeatureEngine()
    window = FeatureWindow(quotes=(quote(1),), trades=(trade(1, "100"), trade(2, "102")))
    assert engine.mid_price(window).value.value == FinancialNumber(value="100", scale=2).value
    assert engine.quoted_spread(window).value.value == FinancialNumber(value="2", scale=2).value
    assert engine.traded_volume(window).value.value == FinancialNumber(value="2", scale=0).value
    assert engine.realized_volatility(window).status is FeatureStatus.VALID
    assert (
        engine.displayed_liquidity(window).value.value == FinancialNumber(value="5", scale=0).value
    )


def test_feature_engine_preserves_unknown_when_inputs_are_missing() -> None:
    result = MarketFeatureEngine().mid_price(FeatureWindow())
    assert result.status is FeatureStatus.UNKNOWN
    assert result.reason_code == "FEATURE_QUOTE_MISSING"
