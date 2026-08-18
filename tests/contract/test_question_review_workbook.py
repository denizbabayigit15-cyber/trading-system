from __future__ import annotations

from jsonschema import Draft202012Validator

from trading_system.contracts.loader import (
    load_json,
    load_question_review_queue,
    load_question_review_workbook_manifest,
    repository_root,
)
from trading_system.contracts.question_review_workbook import (
    sheet_names,
    validate_question_review_workbook,
)


def test_review_workbook_manifest_and_binary_are_valid() -> None:
    raw = load_json("contracts/questions/question_review_workbook_manifest.json")
    schema = load_json("schemas/question_review_workbook_manifest.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(raw)

    manifest = load_question_review_workbook_manifest()
    validate_question_review_workbook(manifest, load_question_review_queue(), repository_root())


def test_review_workbook_is_non_authoritative_and_empty() -> None:
    manifest = load_question_review_workbook_manifest()
    assert manifest.authority_status == "NON_AUTHORITATIVE_REVIEW_INPUT_TEMPLATE"
    assert manifest.editable_decision_statuses == ("DRAFT", "READY_FOR_REVIEW")
    assert manifest.prefilled_decision_count == 0
    assert manifest.approved_count == 0
    assert manifest.adopted_count == 0
    assert manifest.runtime_pass_count == 0
    assert manifest.live_authorized is False


def test_review_workbook_exposes_only_review_sheets() -> None:
    manifest = load_question_review_workbook_manifest()
    path = repository_root() / manifest.workbook_path
    assert sheet_names(path) == ("Yönergeler", "İnceleme", "Sözlük")
