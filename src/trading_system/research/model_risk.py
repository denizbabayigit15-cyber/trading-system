from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class ModelLifecycle(StrEnum):
    REGISTERED = "REGISTERED"
    VALIDATING = "VALIDATING"
    APPROVED = "APPROVED"
    SUSPENDED = "SUSPENDED"


@dataclass(frozen=True, slots=True)
class ModelRecord:
    model_id: str
    version: str
    owner: str
    lifecycle: ModelLifecycle = ModelLifecycle.REGISTERED
    validation_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ModelValidation:
    validation_id: str
    model_id: str
    model_version: str
    owner: str
    passed: bool
    evidence_ids: tuple[str, ...]


class ModelInventory:
    """Immutable-in-value model inventory with fail-closed eligibility."""

    def __init__(self) -> None:
        self._models: dict[tuple[str, str], ModelRecord] = {}
        self._validations: dict[str, ModelValidation] = {}

    def register(self, record: ModelRecord) -> None:
        key = (record.model_id, record.version)
        if key in self._models:
            raise ValueError("model version already registered")
        self._models[key] = record

    def transition(self, model_id: str, version: str, lifecycle: ModelLifecycle) -> ModelRecord:
        key = (model_id, version)
        current = self._models.get(key)
        if current is None:
            raise KeyError(key)
        if lifecycle is ModelLifecycle.APPROVED and not current.validation_ids:
            raise ValueError("approved model requires validation evidence")
        updated = replace(current, lifecycle=lifecycle)
        self._models[key] = updated
        return updated

    def get(self, model_id: str, version: str) -> ModelRecord | None:
        return self._models.get((model_id, version))

    def add_validation(self, validation: ModelValidation) -> None:
        if validation.validation_id in self._validations or not validation.evidence_ids:
            raise ValueError("validation evidence must be unique and non-empty")
        if (validation.model_id, validation.model_version) not in self._models:
            raise KeyError((validation.model_id, validation.model_version))
        self._validations[validation.validation_id] = validation
        key = (validation.model_id, validation.model_version)
        record = self._models[key]
        if validation.passed:
            validation_ids = tuple(sorted(set((*record.validation_ids, validation.validation_id))))
            self._models[key] = replace(record, validation_ids=validation_ids)


def model_eligibility(record: ModelRecord | None, required_validation_id: str) -> bool:
    if record is None or record.lifecycle is not ModelLifecycle.APPROVED:
        return False
    return required_validation_id in record.validation_ids
