from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from trading_system.contracts.loader import (
    load_json,
    load_question_review_decision_ledger,
    load_question_review_queue,
)
from trading_system.contracts.models import (
    QuestionReviewDecisionLedger,
    QuestionReviewDecisionRecord,
)
from trading_system.contracts.question_review_decisions import (
    validate_decision_ledger_against_queue,
)


def approved_values() -> dict[str, Any]:
    submitted_at = datetime(2026, 8, 18, 9, 0, tzinfo=UTC)
    return {
        "decision_id": "qrd_0123456789abcdef0123456789abcdef",
        "question_id": "SV-001",
        "queue_version": "0.1.0",
        "decision_status": "APPROVED",
        "change_request_id": "CR-W0-QUESTION-SV-001",
        "question_version": "1.0.0",
        "scope_hash": "a" * 64,
        "applicability": "APPLICABLE",
        "criticality": "PRODUCTION_BLOCKING",
        "information_class": "UNKNOWN",
        "evidence_id": "EVD-W0-SV-001",
        "contract_id": "CONTRACT-W0-SV-001",
        "policy_id": "POLICY-W0-SV-001",
        "test_id": "TEST-W0-SV-001",
        "scenario_id": "SCENARIO-W0-SV-001",
        "observation_window": "WINDOW-W0-SV-001",
        "fail_action": "DENY_NEW_RISK",
        "recertification_status": "REQUIRED_BEFORE_ADOPTION",
        "owner_id": "owner_test",
        "approver_id": "approver_test",
        "independent_approval_status": "APPROVED",
        "submitted_at": submitted_at,
        "approved_at": submitted_at + timedelta(minutes=5),
        "adoption_status": "NOT_ADOPTED",
        "answer_status": "UNKNOWN",
        "execution_status": "NOT_EXECUTED",
        "live_authorized": False,
    }


def draft_values(*, question_id: str = "SV-001") -> dict[str, Any]:
    return {
        "decision_id": "qrd_fedcba9876543210fedcba9876543210",
        "question_id": question_id,
        "queue_version": "0.1.0",
        "decision_status": "DRAFT",
        "change_request_id": "UNBOUND",
        "question_version": "UNBOUND",
        "scope_hash": "UNBOUND",
        "applicability": "UNBOUND",
        "criticality": "UNBOUND",
        "information_class": "UNKNOWN",
        "evidence_id": "UNBOUND",
        "contract_id": "UNBOUND",
        "policy_id": "UNBOUND",
        "test_id": "UNBOUND",
        "scenario_id": "UNBOUND",
        "observation_window": "UNBOUND",
        "fail_action": "UNBOUND",
        "recertification_status": "UNBOUND",
        "owner_id": "UNBOUND",
        "approver_id": "UNBOUND",
        "independent_approval_status": "NOT_EXECUTED",
        "submitted_at": datetime(2026, 8, 18, 9, 0, tzinfo=UTC),
        "approved_at": None,
        "adoption_status": "NOT_ADOPTED",
        "answer_status": "UNKNOWN",
        "execution_status": "NOT_EXECUTED",
        "live_authorized": False,
    }


def test_committed_decision_ledger_is_empty_and_fail_closed() -> None:
    raw_ledger = load_json("contracts/questions/question_review_decision_ledger.json")
    schema = load_json("schemas/question_review_decision_ledger.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(raw_ledger)

    ledger = load_question_review_decision_ledger()
    validate_decision_ledger_against_queue(ledger, load_question_review_queue())

    assert ledger.decision_count == 0
    assert ledger.draft_count == 0
    assert ledger.approved_count == 0
    assert ledger.adopted_count == 0
    assert ledger.runtime_pass_count == 0
    assert ledger.live_authorized is False
    assert ledger.decisions == ()


def test_draft_may_remain_unbound_without_claiming_approval() -> None:
    record = QuestionReviewDecisionRecord.model_validate(draft_values())

    assert record.decision_status == "DRAFT"
    assert record.independent_approval_status == "NOT_EXECUTED"
    assert record.approved_at is None


def test_valid_independent_approval_still_grants_no_adoption_or_authority() -> None:
    record = QuestionReviewDecisionRecord.model_validate(approved_values())

    assert record.decision_status == "APPROVED"
    assert record.adoption_status == "NOT_ADOPTED"
    assert record.answer_status == "UNKNOWN"
    assert record.execution_status == "NOT_EXECUTED"
    assert record.live_authorized is False


@pytest.mark.parametrize(
    "field",
    [
        "change_request_id",
        "question_version",
        "scope_hash",
        "evidence_id",
        "contract_id",
        "policy_id",
        "test_id",
        "scenario_id",
        "observation_window",
        "fail_action",
        "recertification_status",
        "owner_id",
        "approver_id",
    ],
)
def test_approval_rejects_every_unbound_required_mapping(field: str) -> None:
    values = approved_values()
    values[field] = "UNBOUND"

    with pytest.raises(ValidationError):
        QuestionReviewDecisionRecord.model_validate(values)


@pytest.mark.parametrize("field", ["applicability", "criticality"])
def test_approval_rejects_unbound_classification(field: str) -> None:
    values = approved_values()
    values[field] = "UNBOUND"

    with pytest.raises(ValidationError):
        QuestionReviewDecisionRecord.model_validate(values)


def test_approval_rejects_self_approval() -> None:
    values = approved_values()
    values["approver_id"] = values["owner_id"]

    with pytest.raises(ValidationError, match="must be different"):
        QuestionReviewDecisionRecord.model_validate(values)


def test_approval_rejects_missing_independent_approval() -> None:
    values = approved_values()
    values["independent_approval_status"] = "NOT_EXECUTED"

    with pytest.raises(ValidationError, match="requires independent approval"):
        QuestionReviewDecisionRecord.model_validate(values)


def test_approval_rejects_missing_or_reversed_approval_time() -> None:
    missing = approved_values()
    missing["approved_at"] = None
    with pytest.raises(ValidationError, match="requires an approval timestamp"):
        QuestionReviewDecisionRecord.model_validate(missing)

    reversed_time = approved_values()
    reversed_time["approved_at"] = reversed_time["submitted_at"] - timedelta(seconds=1)
    with pytest.raises(ValidationError, match="cannot precede submission"):
        QuestionReviewDecisionRecord.model_validate(reversed_time)


def test_decision_timestamps_must_be_utc() -> None:
    values = approved_values()
    values["submitted_at"] = datetime(2026, 8, 18, 9, 0)

    with pytest.raises(ValidationError):
        QuestionReviewDecisionRecord.model_validate(values)


def test_ledger_rejects_decision_outside_review_queue() -> None:
    decision = draft_values(question_id="SV-999")
    ledger = QuestionReviewDecisionLedger.model_validate(
        {
            "schema_version": "1.0.0",
            "contract_version": "3.0.0",
            "ledger_version": "0.1.0",
            "ledger_id": "W0-QUESTION-REVIEW-DECISIONS",
            "authority_status": "NON_AUTHORITATIVE_DECISION_LEDGER",
            "source_queue_path": "contracts/questions/first_wave_review_queue.json",
            "source_queue_sha256": (
                "c2b36a809ffacb7a8299397771d678e1d6d77ff0f6f8608c48fe3bad8e7df057"
            ),
            "expected_question_count": 150,
            "decision_count": 1,
            "draft_count": 1,
            "approved_count": 0,
            "adopted_count": 0,
            "runtime_pass_count": 0,
            "live_authorized": False,
            "decisions": [decision],
        }
    )

    with pytest.raises(ValueError, match="outside the review queue"):
        validate_decision_ledger_against_queue(ledger, load_question_review_queue())
