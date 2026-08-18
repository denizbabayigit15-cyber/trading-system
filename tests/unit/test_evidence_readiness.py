from __future__ import annotations

from datetime import UTC, datetime

from trading_system.core.canonical import sha256_digest
from trading_system.evidence.models import EvidenceKind, EvidenceRecord, calculate_readiness


def test_evidence_hash_and_readiness_blockers_are_explicit() -> None:
    payload = {"passed": True, "test": "contract"}
    evidence = EvidenceRecord(
        kind=EvidenceKind.TEST,
        subject_id="contract-suite",
        contract_version="3.0.0",
        scope_hash=None,
        producer="local-test",
        observed_at=datetime(2026, 8, 18, tzinfo=UTC),
        payload=payload,
        payload_sha256=sha256_digest(payload),
    )
    report = calculate_readiness(
        evidence=(evidence,),
        required_by_gate={"R1": ("contract-suite",), "R2": ("full-suite",)},
        question_runtime_pass_count=0,
        independent_review_complete=False,
        external_bindings_complete=False,
    )
    assert report.r1_code_ready
    assert not report.r2_test_ready
    assert not report.r3_operationally_live_ready
    assert not report.live_authorized
    assert report.gates[1].missing_requirements == ("full-suite",)
