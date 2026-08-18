from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FeatureDefinition(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    feature_id: str
    version: str
    source_ids: tuple[str, ...] = Field(min_length=1)
    transformation: str


class FeatureMaterialization(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    feature_id: str
    version: str
    available_at: datetime
    value: Decimal
    lineage_ids: tuple[str, ...] = Field(min_length=1)


class FeatureFabric:
    def __init__(self) -> None:
        self._definitions: dict[tuple[str, str], FeatureDefinition] = {}
        self._values: dict[tuple[str, str, datetime], FeatureMaterialization] = {}

    def register(self, definition: FeatureDefinition) -> None:
        key = (definition.feature_id, definition.version)
        if key in self._definitions:
            raise ValueError("feature definition already registered")
        self._definitions[key] = definition

    def materialize(self, value: FeatureMaterialization) -> None:
        key = (value.feature_id, value.version, value.available_at)
        if (value.feature_id, value.version) not in self._definitions:
            raise ValueError("feature definition is not registered")
        if key in self._values and self._values[key] != value:
            raise ValueError("feature materialization is immutable")
        self._values[key] = value

    def get(
        self, feature_id: str, version: str, available_at: datetime
    ) -> FeatureMaterialization | None:
        return self._values.get((feature_id, version, available_at))
