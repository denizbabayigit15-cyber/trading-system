from __future__ import annotations

from threading import Lock
from typing import Protocol

from sqlalchemy import text
from sqlalchemy.engine import Connection

from trading_system.core.canonical import canonical_json, sha256_digest
from trading_system.evidence.models import EvidenceRecord


class EvidenceRepository(Protocol):
    def append(self, record: EvidenceRecord) -> EvidenceRecord: ...

    def get(self, evidence_id: str) -> EvidenceRecord | None: ...

    def list_for_subject(self, subject_id: str) -> tuple[EvidenceRecord, ...]: ...


class InMemoryEvidenceRepository:
    """Deterministic test double with immutable append-only semantics."""

    def __init__(self) -> None:
        self._records: dict[str, EvidenceRecord] = {}
        self._lock = Lock()

    def append(self, record: EvidenceRecord) -> EvidenceRecord:
        with self._lock:
            existing = self._records.get(record.evidence_id)
            if existing is not None:
                if existing != record:
                    raise ValueError("evidence ID already contains a different immutable record")
                return existing
            self._records[record.evidence_id] = record
            return record

    def get(self, evidence_id: str) -> EvidenceRecord | None:
        with self._lock:
            return self._records.get(evidence_id)

    def list_for_subject(self, subject_id: str) -> tuple[EvidenceRecord, ...]:
        with self._lock:
            return tuple(
                record for record in self._records.values() if record.subject_id == subject_id
            )


def append_event(
    connection: Connection,
    *,
    event_id: str,
    event_type: str,
    schema_version: str,
    occurred_at: object,
    correlation_id: str,
    producer: str,
    payload: dict[str, object],
    lineage_reference: str | None = None,
) -> None:
    """Persist an immutable event inside the caller's transaction."""
    payload_hash = sha256_digest(payload)
    connection.execute(
        text(
            """INSERT INTO audit.event_log
            (event_id, event_type, schema_version, occurred_at, correlation_id,
             producer, lineage_reference, payload, payload_sha256, version_reference,
             retention_classification, audit_classification, immutability_classification)
            VALUES (:event_id, :event_type, :schema_version, :occurred_at, :correlation_id,
                    :producer, :lineage_reference, CAST(:payload AS jsonb), :payload_sha256,
                    :version_reference, :retention_classification, :audit_classification,
                    :immutability_classification)"""
        ),
        {
            "event_id": event_id,
            "event_type": event_type,
            "schema_version": schema_version,
            "occurred_at": occurred_at,
            "correlation_id": correlation_id,
            "producer": producer,
            "lineage_reference": lineage_reference,
            "payload": canonical_json(payload).decode(),
            "payload_sha256": payload_hash,
            "version_reference": "3.0.0",
            "retention_classification": "PERMANENT_AUDIT",
            "audit_classification": "CRITICAL",
            "immutability_classification": "IMMUTABLE",
        },
    )
