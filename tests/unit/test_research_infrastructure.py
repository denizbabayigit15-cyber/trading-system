from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from trading_system.core.canonical import sha256_digest
from trading_system.core.financial import FinancialNumber
from trading_system.market_data.feed import MarketEvent
from trading_system.research.models import (
    DatasetManifest,
    FeatureSpec,
    FeatureValue,
    ResearchUse,
    StrategyContext,
    StrategyRegistry,
    StrategySignal,
    backtest,
)

NOW = datetime(2026, 8, 18, tzinfo=UTC)


class SyntheticStrategy:
    strategy_id = "SYNTHETIC"
    strategy_version = "1.0.0"

    def evaluate(self, context: StrategyContext) -> StrategySignal:
        return StrategySignal(
            strategy_id=self.strategy_id,
            strategy_version=self.strategy_version,
            instrument_id="TEST",
            direction=0,
            confidence=None,
        )


def event() -> MarketEvent:
    return MarketEvent(
        provider="synthetic",
        instrument_id="TEST",
        sequence=1,
        event_time=NOW,
        first_available_at=NOW,
        received_at=NOW,
        price=FinancialNumber(value="100", scale=2, unit="USD"),
        quantity=FinancialNumber(value="1", scale=0, unit="UNIT"),
    )


def dataset() -> DatasetManifest:
    return DatasetManifest(
        dataset_id="synthetic-dataset",
        version="1.0.0",
        source_ids=("synthetic",),
        lineage_ids=("lineage-1",),
        point_in_time=True,
        synthetic=True,
        use=ResearchUse.BACKTEST,
        event_start=NOW,
        event_end=NOW + timedelta(days=1),
        content_sha256="a" * 64,
    )


def test_feature_lineage_hash_is_required() -> None:
    spec = FeatureSpec(
        feature_id="mid",
        version="1",
        source_ids=("synthetic",),
        transformation="identity",
    )
    value = FinancialNumber(value="100", scale=2, unit="USD")
    payload = {
        "feature_id": "mid",
        "version": "1",
        "value": value.canonical(),
        "available_at": NOW,
        "lineage_ids": ("lineage-1",),
    }
    FeatureValue(
        spec=spec,
        value=value,
        available_at=NOW,
        lineage_ids=("lineage-1",),
        value_hash=sha256_digest(payload),
    )


def test_registry_and_backtest_remain_research_only() -> None:
    registry = StrategyRegistry()
    strategy = SyntheticStrategy()
    registry.register(strategy)
    assert registry.get("SYNTHETIC", "1.0.0") is strategy
    result = backtest(dataset(), strategy, (event(),))
    assert result.synthetic
    assert not result.profitability_certified
    with pytest.raises(ValueError):
        backtest(dataset().model_copy(update={"use": ResearchUse.LIVE}), strategy, (event(),))
