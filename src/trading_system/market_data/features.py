from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.models import OrderBookSnapshot, Quote, Trade


class FeatureStatus(StrEnum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"


class FeatureResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    feature_id: str
    status: FeatureStatus
    value: FinancialNumber | None
    as_of: datetime | None
    reason_code: str | None
    source_sequences: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class FeatureWindow:
    quotes: tuple[Quote, ...] = ()
    trades: tuple[Trade, ...] = ()
    books: tuple[OrderBookSnapshot, ...] = ()


class MarketFeatureEngine:
    """Raw-data-only deterministic feature calculations; no inferred market intent."""

    @staticmethod
    def _unknown(feature_id: str, reason: str, sequences: tuple[int, ...] = ()) -> FeatureResult:
        return FeatureResult(
            feature_id=feature_id,
            status=FeatureStatus.UNKNOWN,
            value=None,
            as_of=None,
            reason_code=reason,
            source_sequences=sequences,
        )

    def mid_price(self, window: FeatureWindow) -> FeatureResult:
        if not window.quotes:
            return self._unknown("mid_price", "FEATURE_QUOTE_MISSING")
        quote = window.quotes[-1]
        if quote.bid is None or quote.ask is None or quote.ask.value < quote.bid.value:
            return self._unknown("mid_price", "FEATURE_QUOTE_INCOMPLETE", (quote.sequence,))
        return FeatureResult(
            feature_id="mid_price",
            status=FeatureStatus.VALID,
            value=FinancialNumber(
                value=(quote.bid.value + quote.ask.value) / Decimal("2"),
                scale=max(quote.bid.scale, quote.ask.scale),
                unit=quote.bid.unit,
            ),
            as_of=quote.event_time,
            reason_code=None,
            source_sequences=(quote.sequence,),
        )

    def quoted_spread(self, window: FeatureWindow) -> FeatureResult:
        if not window.quotes:
            return self._unknown("quoted_spread", "FEATURE_QUOTE_MISSING")
        quote = window.quotes[-1]
        if quote.bid is None or quote.ask is None or quote.ask.value < quote.bid.value:
            return self._unknown("quoted_spread", "FEATURE_QUOTE_INCOMPLETE", (quote.sequence,))
        return FeatureResult(
            feature_id="quoted_spread",
            status=FeatureStatus.VALID,
            value=FinancialNumber(
                value=quote.ask.value - quote.bid.value,
                scale=max(quote.bid.scale, quote.ask.scale),
                unit=quote.bid.unit,
            ),
            as_of=quote.event_time,
            reason_code=None,
            source_sequences=(quote.sequence,),
        )

    def traded_volume(self, window: FeatureWindow) -> FeatureResult:
        if not window.trades:
            return self._unknown("traded_volume", "FEATURE_TRADE_MISSING")
        first = window.trades[0]
        total = sum((trade.quantity.value for trade in window.trades), Decimal("0"))
        return FeatureResult(
            feature_id="traded_volume",
            status=FeatureStatus.VALID,
            value=FinancialNumber(
                value=total, scale=first.quantity.scale, unit=first.quantity.unit
            ),
            as_of=window.trades[-1].event_time,
            reason_code=None,
            source_sequences=tuple(trade.sequence for trade in window.trades),
        )

    def realized_volatility(self, window: FeatureWindow) -> FeatureResult:
        if len(window.trades) < 2:
            return self._unknown("realized_volatility", "FEATURE_SAMPLE_INSUFFICIENT")
        prices = [trade.price.value for trade in window.trades]
        returns = [prices[index] - prices[index - 1] for index in range(1, len(prices))]
        mean = sum(returns, Decimal("0")) / Decimal(len(returns))
        variance = sum((value - mean) ** 2 for value in returns) / Decimal(len(returns))
        # Decimal square root is deterministic and avoids floating point financial state.
        volatility = variance.sqrt()
        last = window.trades[-1]
        return FeatureResult(
            feature_id="realized_volatility",
            status=FeatureStatus.VALID,
            value=FinancialNumber(value=volatility, scale=last.price.scale, unit=last.price.unit),
            as_of=last.event_time,
            reason_code=None,
            source_sequences=tuple(trade.sequence for trade in window.trades),
        )

    def displayed_liquidity(self, window: FeatureWindow) -> FeatureResult:
        if not window.quotes:
            return self._unknown("displayed_liquidity", "FEATURE_QUOTE_MISSING")
        quote = window.quotes[-1]
        if quote.bid_size is None or quote.ask_size is None:
            return self._unknown(
                "displayed_liquidity", "FEATURE_QUOTE_INCOMPLETE", (quote.sequence,)
            )
        return FeatureResult(
            feature_id="displayed_liquidity",
            status=FeatureStatus.VALID,
            value=FinancialNumber(
                value=quote.bid_size.value + quote.ask_size.value,
                scale=max(quote.bid_size.scale, quote.ask_size.scale),
                unit=quote.bid_size.unit,
            ),
            as_of=quote.event_time,
            reason_code=None,
            source_sequences=(quote.sequence,),
        )

    def book_completeness(self, window: FeatureWindow) -> FeatureResult:
        if not window.books:
            return self._unknown("book_completeness", "FEATURE_BOOK_MISSING")
        book = window.books[-1]
        value = Decimal("1") if book.complete else Decimal("0")
        return FeatureResult(
            feature_id="book_completeness",
            status=FeatureStatus.VALID,
            value=FinancialNumber(value=value, scale=0, unit="BOOLEAN"),
            as_of=book.event_time,
            reason_code=None,
            source_sequences=(book.sequence,),
        )
