from __future__ import annotations

import asyncio

import pytest

from trading_system.core.financial import FinancialNumber
from trading_system.execution.orders import (
    OrderIntent,
    OrderSide,
    OrderState,
    PaperExecutionAdapter,
    authorize_order,
)


def intent() -> OrderIntent:
    return OrderIntent(
        order_id="order-1",
        idempotency_key="decision-1:order-1",
        instrument_id="TEST",
        side=OrderSide.BUY,
        quantity=FinancialNumber(value="1", scale=0, unit="UNIT"),
        limit_price=FinancialNumber(value="100.00", scale=2, unit="USD"),
        authorization_lease_id="lease-1",
    )


def test_order_requires_consumed_authorization_lease() -> None:
    with pytest.raises(ValueError):
        authorize_order(intent(), lease_consumed=False)


def test_paper_adapter_is_idempotent_and_unknown_is_not_retried() -> None:
    async def scenario() -> None:
        adapter = PaperExecutionAdapter()
        authorized = authorize_order(intent(), lease_consumed=True)
        first = await adapter.submit(authorized)
        duplicate = await adapter.submit(authorized)
        assert first == duplicate
        assert first.state is OrderState.SUBMITTED

        unknown = await adapter.query_by_idempotency_key("missing")
        assert unknown.state is OrderState.UNKNOWN
        assert unknown.reason_code == "ORDER_EXTERNAL_STATE_UNKNOWN"

    asyncio.run(scenario())
