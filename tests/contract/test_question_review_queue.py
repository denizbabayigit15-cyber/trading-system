from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

from trading_system.contracts.loader import load_question_review_queue
from trading_system.contracts.question_review_queue import (
    SOURCE_CATALOG,
    build_question_review_queue_from_path,
    render_question_review_queue,
)

ROOT = Path(__file__).resolve().parents[2]
QUEUE_PATH = ROOT / "contracts/questions/first_wave_review_queue.json"


def test_review_queue_is_deterministic_and_catalog_bound() -> None:
    generated = render_question_review_queue(
        build_question_review_queue_from_path(ROOT / SOURCE_CATALOG)
    )
    assert QUEUE_PATH.read_text(encoding="utf-8") == generated


def test_review_queue_matches_its_json_schema() -> None:
    queue: object = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    schema: object = json.loads(
        (ROOT / "schemas/question_review_queue.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(queue)


def test_review_queue_selects_exactly_six_ordered_families() -> None:
    queue = load_question_review_queue()
    assert queue.family_order == ("SV", "EP", "MI", "VC", "CY", "OR")
    assert len(queue.items) == 150
    assert [item.review_ordinal for item in queue.items] == list(range(1, 151))
    assert [item.catalog_ordinal for item in queue.items] == list(range(688, 838))
    assert Counter(item.family for item in queue.items) == {
        "SV": 25,
        "EP": 25,
        "MI": 25,
        "VC": 25,
        "CY": 25,
        "OR": 25,
    }
    assert queue.items[0].question_id == "SV-001"
    assert queue.items[-1].question_id == "OR-025"


def test_review_queue_cannot_claim_approval_execution_or_authority() -> None:
    queue = load_question_review_queue()
    assert queue.authority_status == "NON_AUTHORITATIVE_REVIEW_QUEUE"
    assert queue.review_required_count == 150
    assert queue.approved_count == 0
    assert queue.adopted_count == 0
    assert queue.runtime_pass_count == 0
    assert queue.live_authorized is False
    assert all(item.review_status == "REVIEW_REQUIRED" for item in queue.items)
    assert all(item.applicability == "UNBOUND" for item in queue.items)
    assert all(item.criticality == "UNBOUND" for item in queue.items)
    assert all(item.contract_id == "UNBOUND" for item in queue.items)
    assert all(item.policy_id == "UNBOUND" for item in queue.items)
    assert all(item.test_id == "UNBOUND" for item in queue.items)
    assert all(item.fail_action == "UNBOUND" for item in queue.items)
    assert all(item.owner == "UNBOUND" for item in queue.items)
    assert all(item.approver == "UNBOUND" for item in queue.items)
    assert all(item.independent_approval_status == "NOT_EXECUTED" for item in queue.items)
