from __future__ import annotations

from trading_system.authority.evaluator import AuthoritySnapshot, PredicateValue, evaluate_authority
from trading_system.contracts.loader import load_json
from trading_system.governance.scope import MarketScopeCandidate, bind_scope


def test_v3_authoritative_question_control_surface() -> None:
    registry = load_json("contracts/questions/question_registry.json")
    relations = load_json("contracts/questions/question_relations.json")
    traceability = load_json("contracts/questions/traceability_matrix.json")
    acceptance = load_json("contracts/questions/acceptance_matrix.json")

    questions = registry["questions"]
    assert registry["contract_version"] == "3.0.0"
    assert registry["question_count"] == 900
    assert len(questions) == 900

    by_id = {item["question_id"]: item for item in questions}
    assert len(by_id) == 900
    assert all(item["runtime_status"] == "UNKNOWN" for item in questions)
    assert all(item["implementation_status"] == "NOT_IMPLEMENTED" for item in questions)
    assert all(item["independent_approval_status"] == "PENDING" for item in questions)
    assert all(item["evidence_id"] is None for item in questions)

    assert len(relations["relations"]) == 4
    for relation in relations["relations"]:
        assert all(qid in by_id for qid in relation["question_ids"])

    assert traceability["row_count"] == 900
    assert len(traceability["rows"]) == 900
    assert {row["question_id"] for row in traceability["rows"]} == set(by_id)

    assert acceptance["test_count"] == 900
    assert len(acceptance["tests"]) == 900
    assert {test["question_id"] for test in acceptance["tests"]} == set(by_id)


def test_existing_w0_questions_match_v3_registry() -> None:
    registry = load_json("contracts/questions/question_registry.json")
    catalog = load_json("contracts/questions/question_catalog_candidate.json")
    queue = load_json("contracts/questions/first_wave_review_queue.json")

    by_id = {item["question_id"]: item for item in registry["questions"]}

    for item in catalog["questions"]:
        source = by_id[item["question_id"]]
        assert (item.get("question") or item.get("question_text")) == source["question"]

    for item in queue["items"]:
        source = by_id[item["question_id"]]
        assert (item.get("question") or item.get("question_text")) == source["question"]


def test_implemented_control_reason_codes_are_registered() -> None:
    registered = {item["code"] for item in load_json("contracts/reason_codes.json")["codes"]}
    scope_codes = set(bind_scope(MarketScopeCandidate()).reason_codes)
    authority = evaluate_authority(
        AuthoritySnapshot(
            decision_id="test",
            scope_hash="scope",
            state_snapshot_id="state",
            market_snapshot_id="market",
            predicates={"hard": PredicateValue.UNKNOWN},
            hard_predicates=frozenset({"hard"}),
            policy_versions={"policy": "v1"},
            risk_state="UNKNOWN",
            capital_state="UNKNOWN",
            reconciliation_state="RECONCILIATION_REQUIRED",
            certification_scope_match=False,
            r4_certified=False,
            live_authorized=False,
            computed_at="2026-08-18T00:00:00Z",
        )
    )
    assert scope_codes | set(authority.reason_codes) <= registered
