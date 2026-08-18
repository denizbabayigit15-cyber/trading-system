from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from trading_system.contracts.loader import load_question_catalog_candidate
from trading_system.contracts.question_catalog import (
    SOURCE_DOCUMENT,
    build_question_catalog,
    render_question_catalog,
)

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "contracts/questions/question_catalog_candidate.json"


def test_candidate_is_deterministic_and_source_bound() -> None:
    generated = render_question_catalog(build_question_catalog(ROOT / SOURCE_DOCUMENT))
    assert CATALOG_PATH.read_text(encoding="utf-8") == generated


def test_candidate_matches_its_json_schema() -> None:
    catalog: object = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    schema: object = json.loads(
        (ROOT / "schemas/question_catalog_candidate.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(catalog)


def test_catalog_contains_900_unique_ordered_source_records() -> None:
    catalog = load_question_catalog_candidate()
    assert catalog.expected_count == 900
    assert len(catalog.questions) == 900
    assert [record.ordinal for record in catalog.questions] == list(range(1, 901))
    assert len({record.question_id for record in catalog.questions}) == 900
    assert catalog.questions[0].question_id == "DS-001"
    assert catalog.questions[236].question_id == "FM-012"
    assert catalog.questions[237].question_id == "ME-001"
    assert catalog.questions[-1].question_id == "GV-018"


def test_candidate_cannot_claim_bindings_execution_or_authority() -> None:
    catalog = load_question_catalog_candidate()
    assert catalog.authority_status == "NON_AUTHORITATIVE_CANDIDATE"
    assert catalog.authoritative_registry_materialized is False
    assert catalog.runtime_pass_count == 0
    assert catalog.unbound_count == 900
    assert catalog.live_authorized is False
    assert all(record.question_version == "UNBOUND" for record in catalog.questions)
    assert all(record.scope_hash == "UNBOUND" for record in catalog.questions)
    assert all(record.applicability == "UNBOUND" for record in catalog.questions)
    assert all(record.criticality == "UNBOUND" for record in catalog.questions)
    assert all(record.answer_status == "UNKNOWN" for record in catalog.questions)
    assert all(record.execution_status == "NOT_EXECUTED" for record in catalog.questions)
    assert all(record.contract_id == "UNBOUND" for record in catalog.questions)
    assert all(record.policy_id == "UNBOUND" for record in catalog.questions)
    assert all(record.test_id == "UNBOUND" for record in catalog.questions)
    assert all(record.fail_action == "UNBOUND" for record in catalog.questions)
    assert all(record.owner == "UNBOUND" for record in catalog.questions)
    assert all(record.approver == "UNBOUND" for record in catalog.questions)
