from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from trading_system.contracts.models import (
    EngineRegistry,
    QuestionCatalogCandidate,
    QuestionReviewDecisionLedger,
    QuestionReviewQueue,
    QuestionReviewWorkbookManifest,
)
from trading_system.contracts.question_catalog import (
    SOURCE_DOCUMENT,
    build_question_catalog,
    render_question_catalog,
)
from trading_system.contracts.question_review_decisions import (
    validate_decision_ledger_against_queue,
)
from trading_system.contracts.question_review_queue import (
    SOURCE_CATALOG,
    build_question_review_queue_from_path,
    render_question_review_queue,
)
from trading_system.contracts.question_review_workbook import (
    validate_question_review_workbook,
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
    validate("contracts/reason_codes.json", "schemas/reason_codes.schema.json")
    validate(
        "contracts/questions/question_catalog_candidate.json",
        "schemas/question_catalog_candidate.schema.json",
    )
    validate(
        "contracts/questions/first_wave_review_queue.json",
        "schemas/question_review_queue.schema.json",
    )
    validate(
        "contracts/questions/question_review_decision_ledger.json",
        "schemas/question_review_decision_ledger.schema.json",
    )
    validate(
        "contracts/questions/question_review_workbook_manifest.json",
        "schemas/question_review_workbook_manifest.schema.json",
    )
    validate(
        "contracts/questions/question_registry.json",
        "schemas/question_registry.schema.json",
    )
    validate(
        "contracts/questions/question_relations.json",
        "schemas/question_relations.schema.json",
    )
    validate(
        "contracts/questions/traceability_matrix.json",
        "schemas/question_traceability_matrix.schema.json",
    )
    validate(
        "contracts/questions/acceptance_matrix.json",
        "schemas/question_acceptance_matrix.schema.json",
    )
    validate(
        "contracts/engine_implementation_coverage.json",
        "schemas/engine_implementation_coverage.schema.json",
    )

    manifest = load("contracts/manifest.json")
    assert manifest["live_authorized"] is False
    assert manifest["r1_code_ready"] is False
    assert manifest["question_catalog_candidate_materialized"] is True
    assert manifest["question_catalog_candidate_count"] == 900
    assert manifest["question_first_wave_review_queue_materialized"] is True
    assert manifest["question_first_wave_review_queue_count"] == 150
    assert manifest["question_first_wave_review_approved_count"] == 0
    assert manifest["question_review_decision_ledger_materialized"] is True
    assert manifest["question_review_decision_count"] == 0
    assert manifest["question_review_decision_approved_count"] == 0
    assert manifest["question_review_decision_adopted_count"] == 0
    assert manifest["question_review_workbook_materialized"] is True
    assert manifest["question_review_workbook_question_count"] == 150
    assert manifest["question_review_workbook_prefilled_decision_count"] == 0
    assert manifest["question_registry_materialized"] is True
    assert manifest["question_registry_count"] == 900
    assert manifest["question_relations_materialized"] is True
    assert manifest["question_relations_count"] == 4
    assert manifest["question_traceability_matrix_materialized"] is True
    assert manifest["question_traceability_row_count"] == 900
    assert manifest["question_acceptance_matrix_materialized"] is True
    assert manifest["question_acceptance_test_count"] == 900
    assert manifest["question_result_schema_materialized"] is True
    assert manifest["owner_acceptance_recorded"] is True
    assert manifest["framework_implementation_may_start"] is True
    assert manifest["independent_validation_complete"] is False

    registry = EngineRegistry.model_validate(load("contracts/engine_registry.json"))
    assert len(registry.engines) == 112
    assert all(engine.runtime_status == "NOT_IMPLEMENTED" for engine in registry.engines)

    coverage = load("contracts/engine_implementation_coverage.json")
    assert coverage["engine_count"] == 112
    assert len(coverage["engines"]) == 112
    assert {row["engine_id"] for row in coverage["engines"]} == set(range(1, 113))

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

    decision_ledger = QuestionReviewDecisionLedger.model_validate(
        load("contracts/questions/question_review_decision_ledger.json")
    )
    validate_decision_ledger_against_queue(decision_ledger, queue)
    assert decision_ledger.decision_count == 0
    assert decision_ledger.draft_count == 0
    assert decision_ledger.approved_count == 0
    assert decision_ledger.adopted_count == 0
    assert decision_ledger.runtime_pass_count == 0
    assert decision_ledger.live_authorized is False

    workbook_manifest = QuestionReviewWorkbookManifest.model_validate(
        load("contracts/questions/question_review_workbook_manifest.json")
    )
    validate_question_review_workbook(workbook_manifest, queue, ROOT)

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

    question_registry = load("contracts/questions/question_registry.json")
    questions = question_registry["questions"]
    assert question_registry["contract_version"] == "3.0.0"
    assert question_registry["question_count"] == 900
    assert len(questions) == 900

    registry_by_id = {item["question_id"]: item for item in questions}
    assert len(registry_by_id) == 900
    assert all(item["question_version"] == "3.0.0" for item in questions)
    assert all(item["runtime_status"] == "UNKNOWN" for item in questions)
    assert all(item["implementation_status"] == "NOT_IMPLEMENTED" for item in questions)
    assert all(item["independent_approval_status"] == "PENDING" for item in questions)
    assert all(item["evidence_id"] is None for item in questions)
    assert {item["source_order"] for item in questions} == set(range(1, 901))
    assert all(item["primary_owner_engine_id"] in item["owner_engine_ids"] for item in questions)

    catalog_raw = load("contracts/questions/question_catalog_candidate.json")["questions"]
    assert len(catalog_raw) == 900
    for item in catalog_raw:
        source = registry_by_id[item["question_id"]]
        text = item.get("question") or item.get("question_text")
        assert text == source["question"]

    queue_raw = load("contracts/questions/first_wave_review_queue.json")["items"]
    assert len(queue_raw) == 150
    for item in queue_raw:
        source = registry_by_id[item["question_id"]]
        text = item.get("question") or item.get("question_text")
        assert text == source["question"]

    relations = load("contracts/questions/question_relations.json")
    assert relations["contract_version"] == "3.0.0"
    assert len(relations["relations"]) == 4
    for relation in relations["relations"]:
        assert all(qid in registry_by_id for qid in relation["question_ids"])

    traceability = load("contracts/questions/traceability_matrix.json")
    assert traceability["contract_version"] == "3.0.0"
    assert traceability["row_count"] == 900
    assert len(traceability["rows"]) == 900
    assert len({row["question_id"] for row in traceability["rows"]}) == 900
    for row in traceability["rows"]:
        source = registry_by_id[row["question_id"]]
        assert row["requirement_id"] == source["contract_id"]
        assert row["policy_id"] == source["policy_id"]
        assert row["test_id"] == source["planned_test_id"]
        assert row["scenario_id"] == source["planned_scenario_id"]
        assert row["owner_engine_ids"] == source["owner_engine_ids"]
        assert row["primary_owner_engine_id"] == source["primary_owner_engine_id"]

    acceptance = load("contracts/questions/acceptance_matrix.json")
    assert acceptance["contract_version"] == "3.0.0"
    assert acceptance["test_count"] == 900
    assert len(acceptance["tests"]) == 900
    assert len({test["test_id"] for test in acceptance["tests"]}) == 900
    assert len({test["question_id"] for test in acceptance["tests"]}) == 900
    for test in acceptance["tests"]:
        source = registry_by_id[test["question_id"]]
        assert test["test_id"] == source["planned_test_id"]
        assert test["requirement_id"] == source["contract_id"]
        assert test["policy_id"] == source["policy_id"]
        assert test["implementation_status"] == "PLANNED_NOT_EXECUTED"
        assert test["pass_evidence_required"] is True

    result_schema = load("schemas/question_result.schema.json")
    Draft202012Validator.check_schema(result_schema)

    print(
        "PASS: contracts, integrity, V3 900-question authoritative registry, "
        "traceability, acceptance matrix, first-wave review controls, and workbook"
    )
    print(
        "EXPECTED BLOCKER: zero independently approved/adopted decisions; "
        "runtime implementation and external bindings remain incomplete"
    )
    print(
        "STATUS: FRAMEWORK_IMPLEMENTATION_MAY_START=true; "
        "R1_CODE_READY=false; LIVE_AUTHORIZED=false"
    )


if __name__ == "__main__":
    main()
