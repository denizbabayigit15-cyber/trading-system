from __future__ import annotations

from trading_system.contracts.loader import load_json


def test_manifest_tells_the_truth() -> None:
    manifest = load_json("contracts/manifest.json")
    assert manifest["implementation_wave"] == "W0"
    assert manifest["r1_code_ready"] is False
    assert manifest["r2_test_ready"] is False
    assert manifest["r3_operationally_live_ready"] is False
    assert manifest["r4_profitability_certified"] is False
    assert manifest["live_authorized"] is False
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
    assert manifest["blockers"]
