from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.domain import (
    CapacityInput,
    FuturesContract,
    GexPosition,
    GreeksInput,
    LiquidityChangeConfig,
    LiquidityChangePointDetector,
    LiquidityEvent,
    LiquidityEventSeries,
    MarketState,
    MetricStatus,
    OptionChain,
    OptionContract,
    OptionRight,
    OrderFlowPolicy,
    RegimeClassifier,
    RollPolicy,
    SessionState,
    SessionWindow,
    VolumeProfileConfig,
    aggregate_gex,
    aggregate_gex_positions,
    build_volume_profile,
    capacity_check,
    classify_market_state,
    classify_trade,
    compose_context,
    derivative_basis,
    greeks_available,
    liquidity_change,
    realized_volatility,
    select_front_contract,
    session_state,
    signed_volume,
    standard_greeks,
    synchronized_join,
)
from trading_system.market_data.models import InstrumentIdentity, InstrumentType, Trade

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def instrument() -> InstrumentIdentity:
    return InstrumentIdentity(
        instrument_id="TEST",
        symbol="TEST",
        instrument_type=InstrumentType.EQUITY,
        venue_id="paper",
        currency="USD",
        tick_size=FinancialNumber(value="0.01", scale=2, unit="USD"),
        quantity_step=FinancialNumber(value="1", scale=0, unit="UNIT"),
        valid_from=NOW,
        valid_to=None,
    )


def trade(sequence: int, price: str, quantity: str = "1") -> Trade:
    return Trade(
        instrument=instrument(),
        price=FinancialNumber(value=price, scale=2, unit="USD"),
        quantity=FinancialNumber(value=quantity, scale=0, unit="UNIT"),
        event_time=NOW,
        sequence=sequence,
        trade_id=f"t-{sequence}",
    )


def test_market_domain_aggregations_and_fail_closed_inputs() -> None:
    profile = build_volume_profile(
        (trade(1, "10"), trade(2, "10.4"), trade(3, "11")),
        VolumeProfileConfig(bucket_size=Decimal("1"), value_area_fraction=Decimal("0.7")),
    )
    assert profile.poc == Decimal("10")
    assert (
        classify_trade(
            trade(1, "11"), previous_price=Decimal("10"), quote=None, policy=OrderFlowPolicy()
        ).value
        == "BUY"
    )
    assert signed_volume(
        (trade(1, "10"), trade(2, "11")), quote=None, policy=OrderFlowPolicy()
    ).value == Decimal("1")
    assert (
        realized_volatility((Decimal("1"), Decimal("2"), Decimal("4"))).status is MetricStatus.VALID
    )
    assert (
        capacity_check(
            CapacityInput(order_quantity=Decimal("1"), displayed_liquidity=Decimal("2"))
        ).status
        is MetricStatus.UNKNOWN
    )
    assert (
        greeks_available(
            GreeksInput(spot=Decimal("10"), strike=Decimal("9"), time_to_expiry=Decimal("1"))
        ).status
        is MetricStatus.UNKNOWN
    )
    bound = GreeksInput(
        spot=Decimal("10"),
        strike=Decimal("9"),
        time_to_expiry=Decimal("1"),
        volatility=Decimal("0.2"),
        rate=Decimal("0.01"),
        dividend=Decimal("0"),
    )
    greeks = standard_greeks(bound)
    assert greeks is not None
    assert greeks.delta == pytest.approx(Decimal("0.7507"), abs=Decimal("0.001"))
    assert aggregate_gex(((greeks, Decimal("2")),)).status is MetricStatus.VALID
    assert (
        aggregate_gex_positions(
            (
                GexPosition(
                    greeks=greeks,
                    open_interest=Decimal("2"),
                    contract_multiplier=Decimal("100"),
                    position_sign=Decimal("1"),
                ),
            )
        ).status
        is MetricStatus.VALID
    )
    assert derivative_basis(Decimal("11"), Decimal("10")).value == Decimal("0.1")
    assert (
        liquidity_change(
            (Decimal("1"), Decimal("10")),
            (Decimal("2"), Decimal("12")),
            LiquidityChangeConfig(spread_threshold=Decimal("0.5"), depth_threshold=Decimal("1")),
        ).reason_code
        == "LIQUIDITY_CHANGE"
    )
    series = LiquidityEventSeries()
    series.append(
        LiquidityEvent(observed_at=NOW, spread=Decimal("1"), displayed_depth=Decimal("10"))
    )
    series.append(
        LiquidityEvent(observed_at=NOW, spread=Decimal("2"), displayed_depth=Decimal("12"))
    )
    assert (
        LiquidityChangePointDetector()
        .detect(
            series,
            LiquidityChangeConfig(spread_threshold=Decimal("0.5"), depth_threshold=Decimal("1")),
        )[0]
        .reason_code
        == "LIQUIDITY_CHANGE"
    )
    front = FuturesContract(
        instrument_id="F1",
        root="TEST",
        expiry=date(2026, 9, 1),
        multiplier=Decimal("1"),
        open_interest=Decimal("100"),
        first_notice=date(2026, 8, 15),
        last_trade=date(2026, 8, 20),
    )
    assert front.calendar_valid()
    next_contract = FuturesContract(
        instrument_id="F2",
        root="TEST",
        expiry=date(2026, 12, 1),
        multiplier=Decimal("1"),
        open_interest=Decimal("120"),
    )
    assert (
        select_front_contract(
            (front, next_contract), RollPolicy(minimum_open_interest_ratio=Decimal("1.1"))
        )
        == next_contract
    )


def test_market_domain_temporal_and_state_boundaries() -> None:
    contract = OptionContract(
        instrument_id="O",
        underlying_id="TEST",
        strike=Decimal("10"),
        expiry=date(2026, 12, 31),
        right=OptionRight.CALL,
    )
    assert OptionChain(underlying_id="TEST", contracts=(contract,)).validate_expiry(
        date(2026, 1, 1)
    )
    start = NOW
    assert (
        session_state((SessionWindow(start, start + timedelta(hours=1), SessionState.OPEN),), NOW)
        is SessionState.OPEN
    )
    volatility = realized_volatility((Decimal("1"), Decimal("2")))
    assert classify_market_state(volatility, active_threshold=Decimal("0")) is MarketState.ACTIVE
    assert RegimeClassifier().classify(volatility, threshold=None) is None
    assert compose_context({"v": volatility}, max_staleness={"v": True}) is not None
    assert synchronized_join({NOW: Decimal("1")}, {NOW: Decimal("2")}) == (
        (NOW, Decimal("1"), Decimal("2")),
    )
