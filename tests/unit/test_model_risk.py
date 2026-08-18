import pytest

from trading_system.research.model_risk import (
    ModelInventory,
    ModelLifecycle,
    ModelRecord,
    ModelValidation,
    model_eligibility,
)


def test_model_inventory_requires_validation_for_approval() -> None:
    inventory = ModelInventory()
    inventory.register(ModelRecord(model_id="m", version="1", owner="team"))
    with pytest.raises(ValueError, match="validation evidence"):
        inventory.transition("m", "1", ModelLifecycle.APPROVED)
    inventory.register(ModelRecord(model_id="n", version="1", owner="team", validation_ids=("v1",)))
    inventory.add_validation(ModelValidation("v2", "n", "1", "reviewer", True, ("evidence",)))
    approved = inventory.transition("n", "1", ModelLifecycle.APPROVED)
    assert model_eligibility(approved, "v1")
    assert model_eligibility(approved, "v2")
