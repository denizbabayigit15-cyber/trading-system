from __future__ import annotations

import asyncio
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from datetime import date, timedelta
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from trading_system.contracts.futures import (
    ContractResolution,
    FuturesContract,
    FuturesRoot,
    resolve_nearest_contract,
)
from trading_system.core.time import require_utc, utc_now
from trading_system.execution.orders import AmendRequest, CancelResult, OrderIntent, SubmitResult
from trading_system.market_data.feed import ConnectionState, FeedState, MarketEvent
from trading_system.providers.ports import BrokerSession


class IBKRSettings(BaseModel):
    """Non-secret IBKR connection settings; credentials remain in the local TWS/Gateway."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    host: str = Field(default="127.0.0.1", min_length=1)
    port: int = Field(default=7497, ge=1, le=65535)
    client_id: int = Field(default=91, ge=0)
    account_id: str | None = None
    paper_only: bool = True
    connect_timeout_seconds: float = Field(default=10.0, gt=0)
    stale_after_seconds: float = Field(default=5.0, gt=0)
    api_secret: SecretStr | None = None

    @classmethod
    def from_environment(cls) -> IBKRSettings:
        import os

        return cls(
            host=os.getenv("IBKR_HOST", "127.0.0.1"),
            port=int(os.getenv("IBKR_PORT", "7497")),
            client_id=int(os.getenv("IBKR_CLIENT_ID", "91")),
            account_id=os.getenv("IBKR_ACCOUNT_ID"),
            paper_only=os.getenv("IBKR_PAPER_ONLY", "true").lower() == "true",
        )


class IBKRTransport(Protocol):
    async def connect(self, host: str, port: int, client_id: int) -> None: ...

    async def disconnect(self) -> None: ...

    async def request_contracts(
        self, root: FuturesRoot, as_of: date
    ) -> tuple[FuturesContract, ...]: ...

    async def subscribe(self, contract: FuturesContract) -> None: ...

    async def next_event(self, timeout: timedelta) -> MarketEvent: ...

    async def submit_paper(self, intent: OrderIntent) -> SubmitResult: ...

    async def amend_paper(self, request: AmendRequest) -> SubmitResult: ...

    async def cancel_paper(self, order_id: str, idempotency_key: str) -> CancelResult: ...


@dataclass(slots=True)
class IBKRSession(BrokerSession):
    settings: IBKRSettings
    transport: IBKRTransport
    _feed_state: FeedState = dataclass_field(default_factory=FeedState)

    @property
    def state(self) -> FeedState:
        return self._feed_state

    @property
    def paper_only(self) -> bool:
        return self.settings.paper_only

    async def connect(self) -> None:
        if not self.settings.paper_only:
            raise RuntimeError("IBKR adapter refuses non-paper mode")
        self._feed_state = self._feed_state.transition(ConnectionState.CONNECTING)
        try:
            await asyncio.wait_for(
                self.transport.connect(
                    self.settings.host, self.settings.port, self.settings.client_id
                ),
                timeout=self.settings.connect_timeout_seconds,
            )
            self._feed_state = self._feed_state.transition(ConnectionState.AUTHENTICATING)
            # Account identity and entitlements are deliberately not inferred from connectivity.
        except (TimeoutError, OSError) as exc:
            self._feed_state = self._feed_state.transition(
                ConnectionState.HALTED, "IBKR_CONNECTION_FAILED"
            )
            raise RuntimeError("IBKR paper connection failed") from exc

    async def disconnect(self) -> None:
        await self.transport.disconnect()
        if self._feed_state.state is not ConnectionState.HALTED:
            self._feed_state = self._feed_state.transition(ConnectionState.DISCONNECTED)

    async def reconnect(self, attempts: int = 3) -> None:
        if attempts < 1:
            raise ValueError("reconnect attempts must be positive")
        for attempt in range(attempts):
            try:
                if self._feed_state.state is not ConnectionState.DISCONNECTED:
                    await self.disconnect()
                await self.connect()
                return
            except RuntimeError, OSError:
                if attempt + 1 == attempts:
                    raise
                await asyncio.sleep(min(2.0, 0.25 * (2**attempt)))


class IBKRAdapter:
    """IBKR implementation of provider ports, with no live-order capability."""

    provider_name = "IBKR"

    def __init__(self, session: IBKRSession) -> None:
        self.session = session

    async def resolve_contracts(self, root: FuturesRoot, as_of: date) -> ContractResolution:
        if self.session.state.state not in {
            ConnectionState.AUTHENTICATING,
            ConnectionState.SYNCHRONIZING,
            ConnectionState.STREAMING,
        }:
            return ContractResolution(
                requested_root=root,
                contract=None,
                reason_code="IBKR_SESSION_NOT_READY",
                candidates=0,
            )
        contracts = await self.session.transport.request_contracts(root, as_of)
        return resolve_nearest_contract(root, contracts, as_of)

    async def subscribe(self, contract: FuturesContract) -> None:
        if not contract.market_data_entitlement_bound:
            raise RuntimeError("MARKET_DATA_ENTITLEMENT_UNBOUND")
        await self.session.transport.subscribe(contract)

    async def next_event(self, timeout: timedelta) -> MarketEvent:
        event = await self.session.transport.next_event(timeout)
        require_utc(event.event_time)
        if (
            utc_now() - event.event_time
        ).total_seconds() > self.session.settings.stale_after_seconds:
            raise RuntimeError("MARKET_DATA_STALE")
        return event

    async def submit(self, intent: OrderIntent) -> SubmitResult:
        if not self.session.paper_only:
            return SubmitResult(False, intent.state, None, "LIVE_EXECUTION_DISABLED")
        return await self.session.transport.submit_paper(intent)

    async def amend(self, request: AmendRequest) -> SubmitResult:
        return await self.session.transport.amend_paper(request)

    async def cancel(self, order_id: str, idempotency_key: str) -> CancelResult:
        return await self.session.transport.cancel_paper(order_id, idempotency_key)
