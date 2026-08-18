from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from trading_system.core.canonical import sha256_digest
from trading_system.core.ids import new_id
from trading_system.core.time import require_utc


class EvidenceKind(StrEnum):
    TEST = "TEST"
    OBSERVATION = "OBSERVATION"
    APPROVAL = "APPROVAL"
    RECONCILIATION = "RECONCILIATION"
    OPERATIONAL = "OPERATIONAL"
    ECONOMIC = "ECONOMIC"


class EvidenceRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    evidence_id: str = Field(default_factory=lambda: new_id("evidence"))
    kind: EvidenceKind
    subject_id: str = Field(min_length=1)
    contract_version: str = Field(min_length=1)
    scope_hash: str | None
    producer: str = Field(min_length=1)
    observed_at: datetime
    payload: dict[str, object]
    payload_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    immutable: bool = True

    @field_validator("observed_at")
    @classmethod
    def timestamp_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    @model_validator(mode="after")
    def verify_payload_hash(self) -> EvidenceRecord:
        if sha256_digest(self.payload) != self.payload_sha256:
            raise ValueError("evidence payload hash does not match payload")
        if not self.immutable:
            raise ValueError("evidence records must be immutable")
        return self


class GateResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    gate: str
    passed: bool
    missing_requirements: tuple[str, ...]
    evidence_ids: tuple[str, ...]


class ReadinessReport(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    r1_code_ready: bool
    r2_test_ready: bool
    r3_operationally_live_ready: bool
    r4_profitability_certified: bool
    live_authorized: bool
    gates: tuple[GateResult, ...]


def calculate_readiness(
    *,
    evidence: tuple[EvidenceRecord, ...],
    required_by_gate: dict[str, tuple[str, ...]],
    question_runtime_pass_count: int,
    independent_review_complete: bool,
    external_bindings_complete: bool,
    current_live_authorization: bool = False,
) -> ReadinessReport:
    by_subject = {record.subject_id: record for record in evidence}
    gates: list[GateResult] = []
    for gate, requirements in required_by_gate.items():
        missing = tuple(
            requirement for requirement in requirements if requirement not in by_subject
        )
        gate_evidence = tuple(
            by_subject[requirement].evidence_id
            for requirement in requirements
            if requirement in by_subject
        )
        gates.append(
            GateResult(
                gate=gate,
                passed=not missing,
                missing_requirements=missing,
                evidence_ids=gate_evidence,
            )
        )
    passed = {gate.gate: gate.passed for gate in gates}
    r1 = passed.get("R1", False)
    r2 = passed.get("R2", False) and question_runtime_pass_count == 900
    r3 = r2 and passed.get("R3", False) and external_bindings_complete
    r4 = r3 and passed.get("R4", False) and independent_review_complete
    return ReadinessReport(
        r1_code_ready=r1,
        r2_test_ready=r2,
        r3_operationally_live_ready=r3,
        r4_profitability_certified=r4,
        live_authorized=(
            r4
            and independent_review_complete
            and external_bindings_complete
            and current_live_authorization
        ),
        gates=tuple(gates),
    )
