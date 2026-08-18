from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator

from trading_system.core.canonical import sha256_digest
from trading_system.core.financial import FinancialNumber
from trading_system.core.time import require_utc
from trading_system.market_data.feed import MarketEvent


class ResearchUse(StrEnum):
    RESEARCH = "RESEARCH"
    BACKTEST = "BACKTEST"
    PAPER = "PAPER"
    LIVE = "LIVE"


class DatasetManifest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dataset_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    source_ids: tuple[str, ...]
    lineage_ids: tuple[str, ...]
    point_in_time: bool
    synthetic: bool
    use: ResearchUse
    event_start: datetime
    event_end: datetime
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def validate_dataset(self) -> DatasetManifest:
        if require_utc(self.event_end) <= require_utc(self.event_start):
            raise ValueError("dataset event window must be increasing")
        if self.use is ResearchUse.LIVE or not self.point_in_time:
            raise ValueError("research datasets cannot directly authorize live use")
        return self


class FeatureSpec(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    feature_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    source_ids: tuple[str, ...] = Field(min_length=1)
    max_age_seconds: int | None = Field(default=None, ge=0)
    transformation: str = Field(min_length=1)


class FeatureValue(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    spec: FeatureSpec
    value: FinancialNumber
    available_at: datetime
    lineage_ids: tuple[str, ...] = Field(min_length=1)
    value_hash: str

    @model_validator(mode="after")
    def verify_hash(self) -> FeatureValue:
        if (
            sha256_digest(
                {
                    "feature_id": self.spec.feature_id,
                    "version": self.spec.version,
                    "value": self.value.canonical(),
                    "available_at": require_utc(self.available_at),
                    "lineage_ids": self.lineage_ids,
                }
            )
            != self.value_hash
        ):
            raise ValueError("feature value hash mismatch")
        return self


class StrategyContext(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    timestamp: datetime
    features: tuple[FeatureValue, ...]
    research_only: bool = True


class StrategySignal(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    strategy_id: str = Field(min_length=1)
    strategy_version: str = Field(min_length=1)
    instrument_id: str = Field(min_length=1)
    direction: int = Field(ge=-1, le=1)
    confidence: Decimal | None
    research_only: bool = True


class Strategy(Protocol):
    strategy_id: str
    strategy_version: str

    def evaluate(self, context: StrategyContext) -> StrategySignal: ...


class StrategyRegistry:
    def __init__(self) -> None:
        self._strategies: dict[tuple[str, str], Strategy] = {}

    def register(self, strategy: Strategy) -> None:
        key = (strategy.strategy_id, strategy.strategy_version)
        if key in self._strategies:
            raise ValueError("strategy version already registered")
        self._strategies[key] = strategy

    def get(self, strategy_id: str, version: str) -> Strategy:
        try:
            return self._strategies[(strategy_id, version)]
        except KeyError as exc:
            raise KeyError("strategy version is not registered") from exc


class BacktestFill(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    timestamp: datetime
    instrument_id: str
    direction: int
    price: FinancialNumber


class BacktestResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dataset_id: str
    strategy_id: str
    strategy_version: str
    fills: tuple[BacktestFill, ...]
    synthetic: bool
    profitability_certified: bool = False


def backtest(
    dataset: DatasetManifest,
    strategy: Strategy,
    events: tuple[MarketEvent, ...],
) -> BacktestResult:
    if dataset.use is not ResearchUse.BACKTEST or not dataset.synthetic:
        raise ValueError(
            "local backtest requires an explicitly labelled synthetic backtest dataset"
        )
    fills = tuple(
        BacktestFill(
            timestamp=event.event_time,
            instrument_id=event.instrument_id,
            direction=0,
            price=event.price,
        )
        for event in events
    )
    return BacktestResult(
        dataset_id=dataset.dataset_id,
        strategy_id=strategy.strategy_id,
        strategy_version=strategy.strategy_version,
        fills=fills,
        synthetic=True,
    )
