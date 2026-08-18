from __future__ import annotations

from datetime import date, timedelta
from typing import Protocol

from trading_system.contracts.futures import ContractResolution, FuturesContract, FuturesRoot
from trading_system.execution.orders import (
    AmendRequest,
    CancelResult,
    ExecutionReport,
    OrderIntent,
    SubmitResult,
)
from trading_system.market_data.feed import FeedState, MarketEvent


class BrokerSession(Protocol):
    @property
    def state(self) -> FeedState: ...

    @property
    def paper_only(self) -> bool: ...

    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...


class ContractProvider(Protocol):
    async def resolve_contracts(self, root: FuturesRoot, as_of: date) -> ContractResolution: ...


class MarketDataProvider(Protocol):
    async def subscribe(self, contract: FuturesContract) -> None: ...

    async def next_event(self, timeout: timedelta) -> MarketEvent: ...


class ExecutionProvider(Protocol):
    async def submit(self, intent: OrderIntent) -> SubmitResult: ...

    async def amend(self, request: AmendRequest) -> SubmitResult: ...

    async def cancel(self, order_id: str, idempotency_key: str) -> CancelResult: ...

    async def reports(self) -> tuple[ExecutionReport, ...]: ...
