from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from itertools import pairwise
from math import erf, exp, log, pi, sqrt

from pydantic import BaseModel, ConfigDict, Field

from trading_system.market_data.models import OrderBookSnapshot, Quote, Trade


class MetricStatus(StrEnum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"


class Metric(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    value: Decimal | None
    status: MetricStatus
    reason_code: str | None = None


class LiquidityChangeConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    spread_threshold: Decimal | None = Field(default=None, ge=0)
    depth_threshold: Decimal | None = Field(default=None, ge=0)


class LiquidityEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    observed_at: datetime
    spread: Decimal = Field(ge=0)
    displayed_depth: Decimal = Field(ge=0)


class LiquidityEventSeries:
    def __init__(self) -> None:
        self._events: list[LiquidityEvent] = []

    def append(self, event: LiquidityEvent) -> None:
        if self._events and event.observed_at < self._events[-1].observed_at:
            raise ValueError("liquidity events must be monotonic")
        self._events.append(event)

    def events(self) -> tuple[LiquidityEvent, ...]:
        return tuple(self._events)


class LiquidityChangePointDetector:
    def detect(
        self, series: LiquidityEventSeries, config: LiquidityChangeConfig
    ) -> tuple[Metric, ...]:
        events = series.events()
        return tuple(
            liquidity_change(
                (previous.spread, previous.displayed_depth),
                (current.spread, current.displayed_depth),
                config,
            )
            for previous, current in pairwise(events)
        )


def liquidity_change(
    previous: tuple[Decimal, Decimal],
    current: tuple[Decimal, Decimal],
    config: LiquidityChangeConfig,
) -> Metric:
    if config.spread_threshold is None or config.depth_threshold is None:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="LIQUIDITY_THRESHOLD_UNBOUND"
        )
    spread_delta = abs(current[0] - previous[0])
    depth_delta = abs(current[1] - previous[1])
    changed = spread_delta >= config.spread_threshold or depth_delta >= config.depth_threshold
    return Metric(
        value=spread_delta + depth_delta,
        status=MetricStatus.VALID,
        reason_code="LIQUIDITY_CHANGE" if changed else None,
    )


class VolumeProfileConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    bucket_size: Decimal = Field(gt=0)
    value_area_fraction: Decimal = Field(gt=0, lt=1)


class VolumeProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    buckets: dict[Decimal, Decimal]
    poc: Decimal | None
    value_area_low: Decimal | None
    value_area_high: Decimal | None


def build_volume_profile(trades: tuple[Trade, ...], config: VolumeProfileConfig) -> VolumeProfile:
    if not trades:
        return VolumeProfile(buckets={}, poc=None, value_area_low=None, value_area_high=None)
    buckets: dict[Decimal, Decimal] = {}
    for trade in trades:
        bucket = (trade.price.value // config.bucket_size) * config.bucket_size
        buckets[bucket] = buckets.get(bucket, Decimal("0")) + trade.quantity.value
    poc = max(buckets, key=lambda key: (buckets[key], -key))
    target = sum(buckets.values()) * config.value_area_fraction
    selected = {poc}
    while sum(buckets[item] for item in selected) < target and len(selected) < len(buckets):
        candidates = [item for item in buckets if item not in selected]
        selected.add(max(candidates, key=lambda item: (buckets[item], -item)))
    return VolumeProfile(
        buckets=buckets,
        poc=poc,
        value_area_low=min(selected),
        value_area_high=max(selected),
    )


class TradeDirection(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    UNKNOWN = "UNKNOWN"


class OrderFlowPolicy(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    tick_rule_enabled: bool = True
    quote_rule_enabled: bool = True


def classify_trade(
    trade: Trade, *, previous_price: Decimal | None, quote: Quote | None, policy: OrderFlowPolicy
) -> TradeDirection:
    if policy.quote_rule_enabled and quote and quote.bid and quote.ask:
        if trade.price.value >= quote.ask.value:
            return TradeDirection.BUY
        if trade.price.value <= quote.bid.value:
            return TradeDirection.SELL
    if policy.tick_rule_enabled and previous_price is not None:
        if trade.price.value > previous_price:
            return TradeDirection.BUY
        if trade.price.value < previous_price:
            return TradeDirection.SELL
    return TradeDirection.UNKNOWN


def signed_volume(
    trades: tuple[Trade, ...], *, quote: Quote | None, policy: OrderFlowPolicy
) -> Metric:
    if not trades:
        return Metric(value=None, status=MetricStatus.UNKNOWN, reason_code="FLOW_SAMPLE_MISSING")
    total = Decimal("0")
    previous: Decimal | None = None
    for trade in trades:
        direction = classify_trade(trade, previous_price=previous, quote=quote, policy=policy)
        if direction is TradeDirection.BUY:
            total += trade.quantity.value
        elif direction is TradeDirection.SELL:
            total -= trade.quantity.value
        previous = trade.price.value
    return Metric(value=total, status=MetricStatus.VALID)


def microprice(quote: Quote) -> Metric:
    if not quote.bid or not quote.ask or not quote.bid_size or not quote.ask_size:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="FEATURE_QUOTE_INCOMPLETE"
        )
    denominator = quote.bid_size.value + quote.ask_size.value
    if denominator <= 0:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="FEATURE_QUOTE_INCOMPLETE"
        )
    value = Decimal(
        quote.ask.value * quote.bid_size.value + quote.bid.value * quote.ask_size.value
    ) / Decimal(denominator)
    return Metric(value=value, status=MetricStatus.VALID)


def depth_imbalance(book: OrderBookSnapshot) -> Metric:
    bid = sum(level.quantity.value for level in book.bids)
    ask = sum(level.quantity.value for level in book.asks)
    if bid + ask <= 0:
        return Metric(value=None, status=MetricStatus.UNKNOWN, reason_code="FEATURE_BOOK_MISSING")
    return Metric(value=Decimal(bid - ask) / Decimal(bid + ask), status=MetricStatus.VALID)


class CapacityInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    order_quantity: Decimal = Field(ge=0)
    displayed_liquidity: Decimal = Field(ge=0)
    participation_limit: Decimal | None = Field(default=None, gt=0)
    impact_limit: Decimal | None = Field(default=None, gt=0)


def capacity_check(value: CapacityInput) -> Metric:
    if value.participation_limit is None or value.impact_limit is None:
        return Metric(value=None, status=MetricStatus.UNKNOWN, reason_code="RISK_LIMIT_UNBOUND")
    if value.displayed_liquidity <= 0:
        return Metric(value=None, status=MetricStatus.UNKNOWN, reason_code="FEATURE_BOOK_MISSING")
    participation = value.order_quantity / value.displayed_liquidity
    return Metric(value=participation, status=MetricStatus.VALID)


class OptionRight(StrEnum):
    CALL = "CALL"
    PUT = "PUT"


class OptionContract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument_id: str
    underlying_id: str
    strike: Decimal = Field(gt=0)
    expiry: date
    right: OptionRight


class OptionChain(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    underlying_id: str
    contracts: tuple[OptionContract, ...]

    def validate_expiry(self, as_of: date) -> bool:
        return all(contract.expiry >= as_of for contract in self.contracts)


class GreeksInput(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    spot: Decimal = Field(gt=0)
    strike: Decimal = Field(gt=0)
    time_to_expiry: Decimal = Field(gt=0)
    right: OptionRight = OptionRight.CALL
    volatility: Decimal | None = Field(default=None, gt=0)
    rate: Decimal | None = None
    dividend: Decimal | None = None


class GreeksResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    delta: Decimal
    gamma: Decimal
    vega: Decimal
    theta: Decimal


class GexPosition(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    greeks: GreeksResult
    open_interest: Decimal = Field(ge=0)
    contract_multiplier: Decimal = Field(gt=0)
    position_sign: Decimal = Field(description="+1 for long, -1 for short")


def standard_greeks(inputs: GreeksInput) -> GreeksResult | None:
    if inputs.volatility is None or inputs.rate is None or inputs.dividend is None:
        return None
    if inputs.rate <= -1 or inputs.dividend <= -1:
        return None
    spot = float(inputs.spot)
    strike = float(inputs.strike)
    maturity = float(inputs.time_to_expiry)
    volatility = float(inputs.volatility)
    rate = float(inputs.rate)
    dividend = float(inputs.dividend)
    root_t = sqrt(maturity)
    sigma_root_t = volatility * root_t
    if spot <= 0 or strike <= 0 or maturity <= 0 or sigma_root_t <= 0:
        return None
    d1 = (log(spot / strike) + (rate - dividend + 0.5 * volatility**2) * maturity) / sigma_root_t
    d2 = d1 - sigma_root_t

    def normal(value: float) -> float:
        return 0.5 * (1.0 + erf(value / sqrt(2.0)))

    density = exp(-0.5 * d1 * d1) / sqrt(2.0 * pi)
    discount_q = exp(-dividend * maturity)
    discount_r = exp(-rate * maturity)
    if inputs.right is OptionRight.CALL:
        delta_value = discount_q * normal(d1)
        theta_value = (
            -spot * discount_q * density * volatility / (2.0 * root_t)
            - rate * strike * discount_r * normal(d2)
            + dividend * spot * discount_q * normal(d1)
        )
    else:
        delta_value = discount_q * (normal(d1) - 1.0)
        theta_value = (
            -spot * discount_q * density * volatility / (2.0 * root_t)
            + rate * strike * discount_r * normal(-d2)
            - dividend * spot * discount_q * normal(-d1)
        )
    gamma_value = discount_q * density / (spot * sigma_root_t)
    vega_value = spot * discount_q * density * root_t
    delta = Decimal(str(delta_value))
    gamma = Decimal(str(gamma_value))
    vega = Decimal(str(vega_value))
    theta = Decimal(str(theta_value))
    return GreeksResult(delta=delta, gamma=gamma, vega=vega, theta=theta)


def aggregate_gex(results: tuple[tuple[GreeksResult, Decimal], ...]) -> Metric:
    if not results:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="DERIVATIVE_INPUT_UNBOUND"
        )
    total = sum(
        (result.gamma * open_interest for result, open_interest in results),
        Decimal("0"),
    )
    return Metric(value=total, status=MetricStatus.VALID)


def aggregate_gex_positions(positions: tuple[GexPosition, ...]) -> Metric:
    if not positions or any(
        position.position_sign not in (Decimal("-1"), Decimal("1")) for position in positions
    ):
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="DERIVATIVE_INPUT_UNBOUND"
        )
    total = sum(
        (
            position.greeks.gamma
            * position.open_interest
            * position.contract_multiplier
            * position.position_sign
            for position in positions
        ),
        Decimal("0"),
    )
    return Metric(value=total, status=MetricStatus.VALID)


def greeks_available(inputs: GreeksInput) -> Metric:
    if inputs.volatility is None or inputs.rate is None or inputs.dividend is None:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="DERIVATIVE_INPUT_UNBOUND"
        )
    # Deterministic, provider-independent intrinsic/delta proxy. Full pricing is
    # deliberately a separate calibrated model boundary.
    return Metric(value=(inputs.spot - inputs.strike), status=MetricStatus.VALID)


class FuturesContract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument_id: str
    root: str
    expiry: date
    multiplier: Decimal = Field(gt=0)
    open_interest: Decimal | None = Field(default=None, ge=0)
    first_notice: date | None = None
    last_trade: date | None = None
    settlement_type: str | None = None

    def calendar_valid(self) -> bool:
        return (self.first_notice is None or self.first_notice <= self.expiry) and (
            self.last_trade is None or self.last_trade <= self.expiry
        )


class RollPolicy(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    minimum_open_interest_ratio: Decimal | None = Field(default=None, gt=0)


def select_front_contract(
    contracts: tuple[FuturesContract, ...], policy: RollPolicy
) -> FuturesContract | None:
    if policy.minimum_open_interest_ratio is None or not contracts:
        return None
    ordered = sorted(contracts, key=lambda contract: contract.expiry)
    if any(contract.open_interest is None for contract in ordered):
        return None
    selected = ordered[0]
    assert selected.open_interest is not None
    for candidate in ordered[1:]:
        assert candidate.open_interest is not None
        if candidate.open_interest >= selected.open_interest * policy.minimum_open_interest_ratio:
            selected = candidate
    return selected


class DerivativeObservation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument_id: str
    observed_at: datetime
    open_interest: Decimal | None = Field(default=None, ge=0)
    funding_rate: Decimal | None = None
    basis: Decimal | None = None


def derivative_basis(future_price: Decimal, spot_price: Decimal) -> Metric:
    if spot_price <= 0:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="DERIVATIVE_INPUT_UNBOUND"
        )
    return Metric(value=(future_price - spot_price) / spot_price, status=MetricStatus.VALID)


def realized_volatility(prices: tuple[Decimal, ...], *, window: int | None = None) -> Metric:
    values = prices[-window:] if window else prices
    if len(values) < 2:
        return Metric(
            value=None, status=MetricStatus.UNKNOWN, reason_code="FEATURE_SAMPLE_INSUFFICIENT"
        )
    returns = tuple(values[index] - values[index - 1] for index in range(1, len(values)))
    mean = sum(returns, Decimal("0")) / Decimal(len(returns))
    variance = sum((value - mean) ** 2 for value in returns) / Decimal(len(returns))
    return Metric(value=variance.sqrt(), status=MetricStatus.VALID)


class MacroRelease(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    series_id: str
    release_id: str
    release_time: datetime
    vintage: int = Field(ge=1)
    value: Decimal
    source_id: str


class NormalizedNewsEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str
    source_id: str
    published_at: datetime
    received_at: datetime
    revision: int = Field(ge=1)
    headline: str
    content_hash: str


class PositioningRelease(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    release_id: str
    report_date: date
    vintage: int = Field(ge=1)
    positions: dict[str, Decimal]
    source_id: str


def synchronized_join(
    left: dict[datetime, Decimal], right: dict[datetime, Decimal]
) -> tuple[tuple[datetime, Decimal, Decimal], ...]:
    return tuple(
        (timestamp, left[timestamp], right[timestamp])
        for timestamp in sorted(left.keys() & right.keys())
    )


class SessionState(StrEnum):
    PREOPEN = "PREOPEN"
    OPEN = "OPEN"
    AUCTION = "AUCTION"
    CLOSED = "CLOSED"


@dataclass(frozen=True, slots=True)
class SessionWindow:
    start: datetime
    end: datetime
    state: SessionState


def session_state(windows: tuple[SessionWindow, ...], at: datetime) -> SessionState:
    for window in windows:
        if window.start <= at < window.end:
            return window.state
    return SessionState.CLOSED


class MarketState(StrEnum):
    UNKNOWN = "UNKNOWN"
    CALM = "CALM"
    ACTIVE = "ACTIVE"


def classify_market_state(volatility: Metric, *, active_threshold: Decimal | None) -> MarketState:
    if volatility.status is MetricStatus.UNKNOWN or active_threshold is None:
        return MarketState.UNKNOWN
    return (
        MarketState.ACTIVE
        if volatility.value is not None and volatility.value >= active_threshold
        else MarketState.CALM
    )


class RegimeClassifier:
    def classify(self, volatility: Metric, *, threshold: Decimal | None) -> str | None:
        state = classify_market_state(volatility, active_threshold=threshold)
        return None if state is MarketState.UNKNOWN else state.value


def compose_context(
    values: dict[str, Metric], *, max_staleness: dict[str, bool]
) -> dict[str, Metric] | None:
    if any(
        value.status is MetricStatus.UNKNOWN or not max_staleness.get(key, False)
        for key, value in values.items()
    ):
        return None
    return dict(values)


def liquidity_map(book: OrderBookSnapshot) -> dict[Decimal, Decimal]:
    levels: dict[Decimal, Decimal] = {}
    for level in (*book.bids, *book.asks):
        levels[level.price.value] = (
            levels.get(level.price.value, Decimal("0")) + level.quantity.value
        )
    return dict(sorted(levels.items()))
