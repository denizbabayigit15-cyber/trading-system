from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_engine_coverage_has_objective_evidence_for_all_registry_rows() -> None:
    registry = json.loads((ROOT / "contracts/engine_registry.json").read_text())
    coverage = json.loads((ROOT / "contracts/engine_implementation_coverage.json").read_text())
    assert coverage["engine_count"] == 112
    assert len(coverage["engines"]) == 112
    assert sum(coverage["counts"].values()) == 112
    assert {row["engine_id"] for row in coverage["engines"]} == set(range(1, 113))
    for row, authoritative in zip(coverage["engines"], registry["engines"], strict=True):
        assert row["engine_name"] == authoritative["engine_name"]
        assert row["authoritative_references"]
        assert row["required_contracts"]
        assert row["checks"]["required_contracts_exist"] is True
        assert row["justification"]
        assert row["owned_question_count"] == len(row["requirement_evidence"])
        assert (
            row["software_requirements_passed"] + row["software_requirements_missing"]
            == row["software_requirement_count"]
        )
        assert row["software_requirements_missing"] == len(row["missing_software"])
        for evidence in row["requirement_evidence"]:
            assert evidence["question_id"]
            assert evidence["implementation_symbols"] == row["implementation_symbols"]
            assert evidence["test_ids"] == row["test_ids"]
            assert set(evidence["evidence_obligations"]) == {
                "RUNTIME_EVIDENCE_REQUIRED",
                "INDEPENDENT_REVIEW_REQUIRED",
            }
            assert (
                evidence["evidence_status"] == "PASS"
                or row["implementation_status"] != "IMPLEMENTED"
            )
        if row["implementation_status"] == "IMPLEMENTED":
            assert row["implementation_modules"]
            assert row["implementation_symbols"]
            assert row["test_files"]
            assert row["test_ids"]
            assert row["missing_software"] == []
        if row["implementation_status"] == "PARTIALLY_IMPLEMENTED":
            assert row["missing_software"]
        assert row["software_status"] == row["implementation_status"]
        assert row["runtime_evidence_status"] == "PENDING"
        if row["external_binding_status"] == "REQUIRED":
            assert row["external_dependencies"]
