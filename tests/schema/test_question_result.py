from __future__ import annotations

from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator, ValidationError

from trading_system.contracts.loader import load_json


def valid_unknown_result() -> dict[str, object]:
    return {
        "question_id": "DS-001",
        "question_version": "3.0.0",
        "scope_hash": "sha256:scope",
        "applicability": "APPLICABLE",
        "criticality": "AUTHORITY_OR_GATE_BLOCKING",
        "status": "UNKNOWN",
        "information_class": "UNKNOWN",
        "contract_id": "REQ-V3.0.0-DS-001",
        "policy_id": "POL-V3.0.0-DS-ACTIVE",
        "test_id": "AT-V3.0.0-DS-001",
        "fail_action": "BLOCK_NEW_RISK",
    }


def validator() -> Draft202012Validator:
    return Draft202012Validator(load_json("schemas/question_result.schema.json"))


def test_unknown_question_result_is_valid_without_evidence() -> None:
    validator().validate(valid_unknown_result())


def test_question_result_requires_criticality() -> None:
    result = valid_unknown_result()
    del result["criticality"]
    with pytest.raises(ValidationError):
        validator().validate(result)


def test_pass_requires_immutable_evidence_identifier() -> None:
    result = deepcopy(valid_unknown_result())
    result["status"] = "PASS"
    result["information_class"] = "OBSERVED"
    with pytest.raises(ValidationError):
        validator().validate(result)

    result["evidence_id"] = "evidence:sha256:abc"
    validator().validate(result)


@pytest.mark.parametrize(
    ("applicability", "status"),
    [("NOT_APPLICABLE", "UNKNOWN"), ("APPLICABLE", "NOT_APPLICABLE")],
)
def test_not_applicable_status_and_applicability_must_agree(
    applicability: str, status: str
) -> None:
    result = valid_unknown_result()
    result["applicability"] = applicability
    result["status"] = status
    with pytest.raises(ValidationError):
        validator().validate(result)
