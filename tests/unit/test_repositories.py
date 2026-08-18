from __future__ import annotations

from datetime import UTC, datetime

import pytest

from trading_system.core.canonical import sha256_digest
from trading_system.db.repositories import InMemoryEvidenceRepository
from trading_system.evidence.models import EvidenceKind, EvidenceRecord


def record() -> EvidenceRecord:
    payload = {"result": "UNKNOWN"}
    return EvidenceRecord(
        kind=EvidenceKind.TEST,
        subject_id="subject-1",
        contract_version="3.0.0",
        scope_hash=None,
        producer="test",
        observed_at=datetime(2026, 8, 18, tzinfo=UTC),
        payload=payload,
        payload_sha256=sha256_digest(payload),
    )


def test_evidence_repository_is_append_only_and_idempotent() -> None:
    repository = InMemoryEvidenceRepository()
    first = repository.append(record())
    assert repository.append(first) == first
    assert repository.get(first.evidence_id) == first
    assert repository.list_for_subject("subject-1") == (first,)

    with pytest.raises(ValueError):
        repository.append(first.model_copy(update={"producer": "different"}))
