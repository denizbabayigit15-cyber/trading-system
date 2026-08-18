from __future__ import annotations

import asyncio

from trading_system.core.financial import FinancialNumber
from trading_system.execution.orders import (
    AmendRequest,
    OrderIntent,
    OrderSide,
    OrderState,
    PaperExecutionAdapter,
)


def make_order() -> OrderIntent:
    return OrderIntent(
        order_id="amend-order",
        idempotency_key="amend-idem",
        instrument_id="TEST",
        side=OrderSide.BUY,
        quantity=FinancialNumber(value="2", scale=0, unit="UNIT"),
        limit_price=FinancialNumber(value="10", scale=2, unit="USD"),
        authorization_lease_id="lease",
        state=OrderState.AUTHORIZED,
    )


def test_paper_amend_and_cancel_are_idempotency_bound() -> None:
    async def scenario() -> None:
        adapter = PaperExecutionAdapter()
        await adapter.submit(make_order())
        amended = await adapter.amend(
            AmendRequest(
                order_id="amend-order",
                new_limit_price=FinancialNumber(value="11", scale=2, unit="USD"),
            )
        )
        assert amended.accepted
        mismatch = await adapter.cancel("amend-order", "wrong")
        assert not mismatch.accepted
        cancelled = await adapter.cancel("amend-order", "amend-idem")
        assert cancelled.accepted

    asyncio.run(scenario())
