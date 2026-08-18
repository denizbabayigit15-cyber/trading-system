from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.financial import FinancialNumber
from trading_system.core.time import require_utc


class InstrumentType(StrEnum):
    EQUITY = "EQUITY"
    FUTURE = "FUTURE"
    OPTION = "OPTION"
    FX = "FX"
    CRYPTO = "CRYPTO"


class InstrumentIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument_id: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    instrument_type: InstrumentType
    venue_id: str = Field(min_length=1)
    currency: str = Field(min_length=3, max_length=3)
    tick_size: FinancialNumber
    quantity_step: FinancialNumber
    valid_from: datetime
    valid_to: datetime | None

    @field_validator("valid_from", "valid_to")
    @classmethod
    def timestamps_are_utc(cls, value: datetime | None) -> datetime | None:
        return None if value is None else require_utc(value)


class Quote(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument: InstrumentIdentity
    bid: FinancialNumber | None
    ask: FinancialNumber | None
    bid_size: FinancialNumber | None
    ask_size: FinancialNumber | None
    event_time: datetime
    sequence: int = Field(ge=0)

    @field_validator("event_time")
    @classmethod
    def event_time_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    @property
    def complete(self) -> bool:
        return None not in (self.bid, self.ask, self.bid_size, self.ask_size)


class Trade(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument: InstrumentIdentity
    price: FinancialNumber
    quantity: FinancialNumber
    event_time: datetime
    sequence: int = Field(ge=0)
    trade_id: str = Field(min_length=1)

    @field_validator("event_time")
    @classmethod
    def event_time_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)


class BookLevel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    price: FinancialNumber
    quantity: FinancialNumber


class OrderBookSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument: InstrumentIdentity
    bids: tuple[BookLevel, ...]
    asks: tuple[BookLevel, ...]
    event_time: datetime
    sequence: int = Field(ge=0)
    complete: bool

    @field_validator("event_time")
    @classmethod
    def event_time_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)


def normalize_financial(value: object, *, scale: int, unit: str) -> FinancialNumber:
    """Normalize provider numbers without allowing binary floats into decisions."""
    return FinancialNumber.model_validate({"value": value, "scale": scale, "unit": unit})
