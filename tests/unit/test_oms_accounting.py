from __future__ import annotations

import pytest

from trading_system.core.financial import FinancialNumber
from trading_system.execution.accounting import apply_fill
from trading_system.execution.orders import (
    ExecutionReport,
    Fill,
    OrderBook,
    OrderIntent,
    OrderSide,
    OrderState,
    authorize_order,
    transition_order,
)


def number(value: str, scale: int = 2) -> FinancialNumber:
    return FinancialNumber(value=value, scale=scale, unit="USD")


def order() -> OrderIntent:
    return OrderIntent(
        order_id="o1",
        idempotency_key="idem-1",
        instrument_id="TEST",
        side=OrderSide.BUY,
        quantity=FinancialNumber(value="2", scale=0, unit="UNIT"),
        limit_price=number("10"),
        authorization_lease_id="lease",
    )


def fill(quantity: str, price: str, trade: str = "t1") -> Fill:
    return Fill(
        "f-" + trade,
        "o1",
        FinancialNumber(value=quantity, scale=0, unit="UNIT"),
        number(price),
        number("0.10"),
        trade,
    )


def test_unknown_order_cannot_jump_to_filled() -> None:
    with pytest.raises(ValueError):
        transition_order(order(), OrderState.FILLED)


def test_order_book_deduplicates_and_tracks_partial_fill() -> None:
    book = OrderBook()
    authorized = authorize_order(order(), lease_consumed=True)
    submitted = transition_order(authorized, OrderState.SUBMITTED)
    book.add(submitted)
    book.apply_report(
        ExecutionReport(
            "o1",
            OrderState.PARTIALLY_FILLED,
            authorized.quantity,
            authorized.quantity,
            fill("1", "10"),
        )
    )
    assert len(book.fills("o1")) == 1
    assert book.add(submitted).state is OrderState.PARTIALLY_FILLED


def test_accounting_projection_is_deterministic() -> None:
    projection = apply_fill(None, instrument_id="TEST", side=OrderSide.BUY, fill=fill("1", "10"))
    projection = apply_fill(
        projection, instrument_id="TEST", side=OrderSide.SELL, fill=fill("1", "12", "t2")
    )
    assert projection.quantity.value == 0
    assert projection.realized_pnl.value == number("2").value
