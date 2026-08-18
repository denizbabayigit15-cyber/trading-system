from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def test_every_contract_and_schema_is_valid_json() -> None:
    paths = sorted((ROOT / "contracts").rglob("*.json")) + sorted((ROOT / "schemas").glob("*.json"))
    assert paths
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_json_schemas_are_valid_draft_2020_12() -> None:
    paths = sorted((ROOT / "schemas").glob("*.schema.json"))
    assert paths
    for path in paths:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
