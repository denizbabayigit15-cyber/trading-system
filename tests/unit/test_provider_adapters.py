from __future__ import annotations

import asyncio

import pytest

from trading_system.market_data.adapters import (
    AdapterError,
    RestClient,
    WebSocketClient,
)
from trading_system.market_data.feed import ConnectionState


class RestDouble:
    def __init__(self) -> None:
        self.calls = 0

    async def request(
        self, method: str, path: str, payload: dict[str, object] | None
    ) -> dict[str, object]:
        self.calls += 1
        if self.calls < 2:
            raise OSError("transient")
        return {"ok": True}


class SocketDouble:
    def __init__(self) -> None:
        self.closed = False

    async def connect(self) -> None:
        return None

    async def close(self) -> None:
        self.closed = True

    async def send(self, payload: dict[str, object]) -> None:
        return None

    async def receive(self) -> dict[str, object]:
        return {"ok": True}


def test_rest_retries_transient_transport_failure() -> None:
    async def scenario() -> None:
        transport = RestDouble()
        result = await RestClient(transport).request("GET", "/health")
        assert result == {"ok": True}
        assert transport.calls == 2

    asyncio.run(scenario())


def test_websocket_lifecycle_requires_authentication_and_sync() -> None:
    async def scenario() -> None:
        client = WebSocketClient(SocketDouble())
        await client.connect()
        assert client.state.state is ConnectionState.AUTHENTICATING
        with pytest.raises(AdapterError):
            await client.mark_streaming()
        await client.authenticate({"token": "synthetic-test-token"})
        await client.mark_streaming()
        assert client.state.state is ConnectionState.STREAMING
        await client.close()
        assert client.state.state is ConnectionState.DISCONNECTED

    asyncio.run(scenario())
