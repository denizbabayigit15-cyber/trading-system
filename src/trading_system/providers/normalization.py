from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import cast

from trading_system.core.financial import FinancialNumber
from trading_system.market_data.feed import MarketEvent


def normalize_timestamp(value: object) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise ValueError("provider timestamp is naive")
        return value.astimezone(UTC)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("provider timestamp is naive")
        return parsed.astimezone(UTC)
    if isinstance(value, (int, Decimal)) and not isinstance(value, bool):
        return datetime.fromtimestamp(float(value), UTC)
    raise ValueError("unsupported provider timestamp")


def normalize_ibkr_event(payload: dict[str, object], *, received_at: datetime) -> MarketEvent:
    event_time = normalize_timestamp(payload["event_time"])
    received = normalize_timestamp(received_at)
    price_scale_value = payload.get("price_scale", 4)
    quantity_scale_value = payload.get("quantity_scale", 0)
    if not isinstance(price_scale_value, (str, int)) or isinstance(price_scale_value, bool):
        raise ValueError("invalid price scale")
    if not isinstance(quantity_scale_value, (str, int)) or isinstance(quantity_scale_value, bool):
        raise ValueError("invalid quantity scale")
    price_scale = int(price_scale_value)
    quantity_scale = int(quantity_scale_value)
    sequence_value = payload["sequence"]
    if not isinstance(sequence_value, (str, int)) or isinstance(sequence_value, bool):
        raise ValueError("invalid market event sequence")
    price = Decimal(str(cast(str | int | Decimal, payload["price"])))
    quantity = Decimal(str(cast(str | int | Decimal, payload["quantity"])))
    return MarketEvent(
        provider="IBKR",
        instrument_id=str(payload["instrument_id"]),
        sequence=int(sequence_value),
        event_time=event_time,
        first_available_at=normalize_timestamp(payload.get("first_available_at", event_time)),
        received_at=received,
        price=FinancialNumber(value=price, scale=price_scale, unit="USD"),
        quantity=FinancialNumber(
            value=quantity,
            scale=quantity_scale,
            unit="contracts",
        ),
    )
