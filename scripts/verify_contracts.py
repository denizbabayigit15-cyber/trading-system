from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from trading_system.contracts.models import EngineRegistry

ROOT = Path(__file__).resolve().parents[1]


def load(relative_path: str) -> dict[str, Any]:
    value: object = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{relative_path} is not a JSON object")
    return value


def validate(instance_path: str, schema_path: str) -> None:
    instance = load(instance_path)
    schema = load(schema_path)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    validate("contracts/manifest.json", "schemas/manifest.schema.json")
    validate("contracts/engine_registry.json", "schemas/engine_registry.schema.json")

    manifest = load("contracts/manifest.json")
    assert manifest["live_authorized"] is False
    assert manifest["r1_code_ready"] is False
    assert manifest["question_registry_materialized"] is False

    registry = EngineRegistry.model_validate(load("contracts/engine_registry.json"))
    assert len(registry.engines) == 112
    assert all(engine.runtime_status == "NOT_IMPLEMENTED" for engine in registry.engines)

    reason_codes = load("contracts/reason_codes.json")["codes"]
    codes = [item["code"] for item in reason_codes]
    assert len(codes) == len(set(codes))
    assert "AUTH_LIVE_DISABLED" in codes
    assert "AUTH_UNKNOWN_CRITICAL_STATE" in codes

    integrity = load("contracts/integrity_manifest.json")
    for record in integrity["files"]:
        path = ROOT / record["path"]
        assert path.is_file(), f"missing integrity file: {record['path']}"
        assert path.stat().st_size == record["size_bytes"]
        assert sha256(path) == record["sha256"], f"hash mismatch: {record['path']}"

    question_registry = ROOT / "contracts/questions/question_registry.json"
    assert not question_registry.exists(), (
        "unexpected question registry must be reviewed before adoption"
    )

    print("PASS: scaffold contract and integrity checks")
    print("EXPECTED BLOCKER: 900-question machine registry is not materialized")
    print("STATUS: R1_CODE_READY=false; LIVE_AUTHORIZED=false")


if __name__ == "__main__":
    main()
