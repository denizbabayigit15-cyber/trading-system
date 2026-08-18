from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.engine import Connection

from trading_system.core.canonical import canonical_json

if TYPE_CHECKING:
    from trading_system.governance.orchestrator import GovernanceEvent
    from trading_system.research.decision import DecisionRecord, Delivery, FeedbackEvent
    from trading_system.research.fabric import FeatureDefinition, FeatureMaterialization
    from trading_system.research.performance import DecompositionRecord


def _audit(now: datetime) -> dict[str, object]:
    return {
        "created_at": now,
        "version_reference": "3.0.0",
        "retention_classification": "PERMANENT_AUDIT",
        "audit_classification": "CRITICAL",
        "immutability_classification": "IMMUTABLE",
    }


def append_governance_event(connection: Connection, event: GovernanceEvent) -> None:
    payload = {
        "event_id": event.event_id,
        "state": event.state.value,
        "reason_code": event.reason_code,
    }
    connection.execute(
        text(
            """INSERT INTO governance.governance_event
            (event_id,state,occurred_at,reason_code,payload,created_at,version_reference,
             retention_classification,audit_classification,immutability_classification)
            VALUES (:event_id,:state,:occurred_at,:reason_code,CAST(:payload AS jsonb),
                    :created_at,:version_reference,:retention_classification,
                    :audit_classification,:immutability_classification)"""
        ),
        {
            **payload,
            "occurred_at": event.occurred_at,
            "payload": canonical_json(payload).decode(),
            **_audit(event.occurred_at),
        },
    )


def register_feature_definition(
    connection: Connection, definition: FeatureDefinition, now: datetime
) -> None:
    connection.execute(
        text(
            """INSERT INTO feature.definition
            (feature_id,version,source_ids,transformation,created_at,version_reference,
             retention_classification,audit_classification,immutability_classification)
            VALUES (:feature_id,:version,:source_ids,:transformation,:created_at,:version_reference,
                    :retention_classification,:audit_classification,:immutability_classification)"""
        ),
        {
            "feature_id": definition.feature_id,
            "version": definition.version,
            "source_ids": list(definition.source_ids),
            "transformation": definition.transformation,
            **_audit(now),
        },
    )


def append_feature_materialization(connection: Connection, value: FeatureMaterialization) -> None:
    payload = {"value": str(value.value)}
    connection.execute(
        text(
            """INSERT INTO feature.materialization
            (feature_id,version,available_at,value,lineage_ids,created_at,version_reference,
             retention_classification,audit_classification,immutability_classification)
            VALUES (:feature_id,:version,:available_at,CAST(:value AS jsonb),:lineage_ids,
                    :created_at,:version_reference,:retention_classification,
                    :audit_classification,:immutability_classification)"""
        ),
        {
            "feature_id": value.feature_id,
            "version": value.version,
            "available_at": value.available_at,
            "value": canonical_json(payload).decode(),
            "lineage_ids": list(value.lineage_ids),
            **_audit(value.available_at),
        },
    )


def append_decision_record(connection: Connection, record: DecisionRecord, now: datetime) -> None:
    connection.execute(
        text(
            """INSERT INTO decision.decision_record
            (decision_id,version,members,approvals,dissent,provenance_ids,quorum,passed,
             authority_lease_id,state,created_at,
             version_reference,retention_classification,audit_classification,immutability_classification)
            VALUES (:decision_id,:version,:members,:approvals,:dissent,:provenance_ids,
                    :quorum,:passed,:authority_lease_id,:state,
                    :created_at,:version_reference,:retention_classification,:audit_classification,
                    :immutability_classification)"""
        ),
        {
            "decision_id": record.decision_id,
            "version": record.version,
            "members": list(record.members),
            "approvals": list(record.approvals),
            "dissent": list(record.dissent),
            "provenance_ids": list(record.provenance_ids),
            "quorum": record.quorum,
            "passed": record.passed,
            "authority_lease_id": record.authority_lease_id,
            "state": record.state,
            **_audit(now),
        },
    )


def append_delivery(connection: Connection, delivery: Delivery, now: datetime) -> None:
    connection.execute(
        text(
            """INSERT INTO decision.delivery
            (delivery_id,decision_id,attempt,acknowledged,created_at,version_reference,
             retention_classification,audit_classification,immutability_classification)
            VALUES (:delivery_id,:decision_id,:attempt,:acknowledged,:created_at,:version_reference,
                    :retention_classification,:audit_classification,:immutability_classification)"""
        ),
        {
            "delivery_id": f"{delivery.decision_id}:{delivery.attempt}",
            "decision_id": delivery.decision_id,
            "attempt": delivery.attempt,
            "acknowledged": delivery.acknowledged,
            **_audit(now),
        },
    )


def append_feedback_event(connection: Connection, event: FeedbackEvent, now: datetime) -> None:
    connection.execute(
        text(
            """INSERT INTO feedback.event
            (event_id,subject_id,provenance_ids,state,payload,created_at,version_reference,
             retention_classification,audit_classification,immutability_classification)
            VALUES (:event_id,:subject_id,:provenance_ids,:state,CAST(:payload AS jsonb),
                    :created_at,
                    :version_reference,:retention_classification,:audit_classification,
                    :immutability_classification)"""
        ),
        {
            "event_id": event.event_id,
            "subject_id": event.subject_id,
            "provenance_ids": list(event.provenance_ids),
            "state": event.state,
            "payload": canonical_json(event.payload).decode(),
            **_audit(now),
        },
    )


def append_decomposition_record(
    connection: Connection, record: DecompositionRecord, now: datetime
) -> None:
    connection.execute(
        text(
            """INSERT INTO performance.decomposition_record
            (record_id,subject_id,dimension,contribution,source_id,created_at,version_reference,
             retention_classification,audit_classification,immutability_classification)
            VALUES (:record_id,:subject_id,:dimension,CAST(:contribution AS jsonb),:source_id,
                    :created_at,
                    :version_reference,:retention_classification,:audit_classification,
                    :immutability_classification)"""
        ),
        {
            "record_id": f"{record.subject_id}:{record.dimension}:{record.source_id}",
            "subject_id": record.subject_id,
            "dimension": record.dimension,
            "contribution": canonical_json({"value": str(record.contribution)}).decode(),
            "source_id": record.source_id,
            **_audit(now),
        },
    )
