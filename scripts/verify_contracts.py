from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from trading_system.contracts.models import (
    EngineRegistry,
    QuestionCatalogCandidate,
    QuestionReviewQueue,
)
from trading_system.contracts.question_catalog import (
    SOURCE_DOCUMENT,
    build_question_catalog,
    render_question_catalog,
)
from trading_system.contracts.question_review_queue import (
    SOURCE_CATALOG,
    build_question_review_queue_from_path,
    render_question_review_queue,
)

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
    validate(
        "contracts/questions/question_catalog_candidate.json",
        "schemas/question_catalog_candidate.schema.json",
    )
    validate(
        "contracts/questions/first_wave_review_queue.json",
        "schemas/question_review_queue.schema.json",
    )

    manifest = load("contracts/manifest.json")
    assert manifest["live_authorized"] is False
    assert manifest["r1_code_ready"] is False
    assert manifest["question_catalog_candidate_materialized"] is True
    assert manifest["question_catalog_candidate_count"] == 900
    assert manifest["question_first_wave_review_queue_materialized"] is True
    assert manifest["question_first_wave_review_queue_count"] == 150
    assert manifest["question_first_wave_review_approved_count"] == 0
    assert manifest["question_registry_materialized"] is False

    registry = EngineRegistry.model_validate(load("contracts/engine_registry.json"))
    assert len(registry.engines) == 112
    assert all(engine.runtime_status == "NOT_IMPLEMENTED" for engine in registry.engines)

    catalog_path = ROOT / "contracts/questions/question_catalog_candidate.json"
    catalog = QuestionCatalogCandidate.model_validate(
        load("contracts/questions/question_catalog_candidate.json")
    )
    assert len(catalog.questions) == 900
    assert catalog.runtime_pass_count == 0
    assert catalog.unbound_count == 900
    assert catalog.live_authorized is False
    regenerated = render_question_catalog(build_question_catalog(ROOT / SOURCE_DOCUMENT))
    assert catalog_path.read_text(encoding="utf-8") == regenerated, (
        "question catalog is stale relative to its reviewed Markdown source"
    )

    queue_path = ROOT / "contracts/questions/first_wave_review_queue.json"
    queue = QuestionReviewQueue.model_validate(
        load("contracts/questions/first_wave_review_queue.json")
    )
    assert len(queue.items) == 150
    assert queue.review_required_count == 150
    assert queue.approved_count == 0
    assert queue.adopted_count == 0
    assert queue.runtime_pass_count == 0
    assert queue.live_authorized is False
    regenerated_queue = render_question_review_queue(
        build_question_review_queue_from_path(ROOT / SOURCE_CATALOG)
    )
    assert queue_path.read_text(encoding="utf-8") == regenerated_queue, (
        "first-wave review queue is stale relative to the candidate catalog"
    )

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

    print("PASS: contracts, integrity, 900-question catalog, and 150-item review queue")
    print("EXPECTED BLOCKER: authoritative owner/policy/test/fail-action registry is absent")
    print("STATUS: R1_CODE_READY=false; LIVE_AUTHORIZED=false")


if __name__ == "__main__":
    main()
