from datetime import UTC, datetime
from decimal import Decimal

import pytest

from trading_system.research.fabric import FeatureDefinition, FeatureFabric, FeatureMaterialization


def test_feature_fabric_is_versioned_lineage_safe_and_immutable() -> None:
    at = datetime(2026, 1, 1, tzinfo=UTC)
    fabric = FeatureFabric()
    fabric.register(
        FeatureDefinition(
            feature_id="f", version="1", source_ids=("raw",), transformation="identity"
        )
    )
    value = FeatureMaterialization(
        feature_id="f", version="1", available_at=at, value=Decimal("2"), lineage_ids=("raw-1",)
    )
    fabric.materialize(value)
    assert fabric.get("f", "1", at) == value
    with pytest.raises(ValueError):
        fabric.materialize(value.model_copy(update={"value": Decimal("3")}))
