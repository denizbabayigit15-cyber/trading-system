from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import DBAPIError

from trading_system.core.canonical import sha256_digest
from trading_system.db.repositories import append_event
from trading_system.db.semantic_repositories import (
    append_decision_record,
    append_decomposition_record,
    append_delivery,
    append_feature_materialization,
    append_feedback_event,
    append_governance_event,
    register_feature_definition,
)
from trading_system.db.session import get_engine
from trading_system.governance.orchestrator import GovernanceEvent, GovernanceState
from trading_system.research.decision import DecisionRecord, Delivery, FeedbackEvent
from trading_system.research.fabric import FeatureDefinition, FeatureMaterialization
from trading_system.research.performance import decomposition_records


@pytest.fixture(scope="module")
def engine():
    candidate = get_engine()
    try:
        with candidate.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - exercised only without local Postgres
        pytest.skip(f"local PostgreSQL unavailable: {exc}")
    return candidate


def audit_values() -> dict[str, object]:
    now = datetime.now(UTC)
    return {
        "created_at": now,
        "version_reference": "3.0.0",
        "retention_classification": "TEST",
        "audit_classification": "TEST",
        "immutability_classification": "IMMUTABLE",
    }


def test_runtime_schema_and_constraints(engine) -> None:  # type: ignore[no-untyped-def]
    inspector = inspect(engine)
    for schema, table in (
        ("audit", "event_log"),
        ("evidence", "evidence_record"),
        ("execution", "order_intent"),
        ("execution", "fill"),
        ("position", "position_projection"),
        ("reconciliation", "reconciliation_decision"),
        ("governance", "governance_event"),
        ("feature", "definition"),
        ("feature", "materialization"),
        ("decision", "decision_record"),
        ("decision", "delivery"),
        ("feedback", "event"),
        ("performance", "decomposition_record"),
    ):
        assert inspector.has_table(table, schema=schema)
    with engine.connect() as connection:
        assert (
            connection.execute(
                text("SELECT live_authorized FROM governance.system_state WHERE state_id=1")
            ).scalar_one()
            is False
        )


def test_runtime_transaction_and_domain_records(engine) -> None:  # type: ignore[no-untyped-def]
    order_id = f"runtime-order-{uuid4()}"
    event_id = str(uuid4())
    payload = {"kind": "runtime-test", "order_id": order_id}
    payload_hash = sha256_digest(payload)
    audit = audit_values()
    with engine.begin() as connection:
        connection.execute(
            text(
                """INSERT INTO audit.event_log
                (event_id,event_type,schema_version,occurred_at,correlation_id,producer,payload,
                 payload_sha256,version_reference,retention_classification,audit_classification,
                 immutability_classification)
                VALUES (:event_id,'RUNTIME_TEST','3.0.0',:occurred_at,:correlation_id,'pytest',
                        CAST(:payload AS jsonb),:payload_sha256,:version_reference,
                        :retention_classification,:audit_classification,:immutability_classification)"""
            ),
            {
                "event_id": event_id,
                "occurred_at": audit["created_at"],
                "correlation_id": order_id,
                "payload": str(payload).replace("'", '"'),
                "payload_sha256": payload_hash,
                **audit,
            },
        )
        connection.execute(
            text(
                """INSERT INTO execution.order_intent
                (order_id,idempotency_key,instrument_id,side,quantity,authorization_lease_id,state,
                 created_at,version_reference,retention_classification,audit_classification,immutability_classification)
                VALUES (:order_id,:idempotency_key,'TEST','BUY','{"value":"1"}'::jsonb,
                        'runtime-lease',
                        'AUTHORIZED',:created_at,:version_reference,:retention_classification,:audit_classification,
                        :immutability_classification)"""
            ),
            {"order_id": order_id, "idempotency_key": f"runtime-idem-{uuid4()}", **audit},
        )
        connection.execute(
            text(
                """INSERT INTO execution.fill
                (fill_id,order_id,quantity,price,fee,external_trade_id,created_at,version_reference,
                 retention_classification,audit_classification,immutability_classification)
                VALUES (:fill_id,:order_id,'{"value":"1"}'::jsonb,'{"value":"10"}'::jsonb,
                        '{"value":"0"}'::jsonb,:trade,:created_at,:version_reference,
                        :retention_classification,:audit_classification,:immutability_classification)"""
            ),
            {
                "fill_id": f"runtime-fill-{uuid4()}",
                "order_id": order_id,
                "trade": f"runtime-trade-{uuid4()}",
                **audit,
            },
        )
        assert (
            connection.execute(
                text("SELECT count(*) FROM execution.fill WHERE order_id=:id"), {"id": order_id}
            ).scalar_one()
            == 1
        )
        append_event(
            connection,
            event_id=str(uuid4()),
            event_type="REPOSITORY_RUNTIME_TEST",
            schema_version="3.0.0",
            occurred_at=audit["created_at"],
            correlation_id=order_id,
            producer="pytest",
            payload={"order_id": order_id},
        )


def test_runtime_immutable_trigger_and_rollback(engine) -> None:  # type: ignore[no-untyped-def]
    event_id = str(uuid4())
    audit = audit_values()
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text(
                    """INSERT INTO audit.event_log
                    (event_id,event_type,schema_version,occurred_at,correlation_id,producer,payload,
                     payload_sha256,version_reference,retention_classification,audit_classification,
                     immutability_classification)
                    VALUES (:id,'IMMUTABILITY_TEST','3.0.0',:at,:correlation,'pytest','{}'::jsonb,
                            :hash,:version_reference,:retention_classification,:audit_classification,
                            :immutability_classification)"""
                ),
                {
                    "id": event_id,
                    "at": audit["created_at"],
                    "correlation": event_id,
                    "hash": sha256_digest({}),
                    **audit,
                },
            )
            nested = connection.begin_nested()
            try:
                with pytest.raises(DBAPIError):
                    connection.execute(
                        text("UPDATE audit.event_log SET event_type='MUTATED' WHERE event_id=:id"),
                        {"id": event_id},
                    )
            finally:
                nested.rollback()
            connection.execute(
                text(
                    """INSERT INTO operations.outbox_event
                    (outbox_id,subject,idempotency_key,payload,version_reference,
                     retention_classification,audit_classification,immutability_classification)
                    VALUES (:id,'rollback',:idem,'{}'::jsonb,:version_reference,
                            :retention_classification,:audit_classification,'VERSIONED_STATE')"""
                ),
                {"id": str(uuid4()), "idem": f"rollback-{uuid4()}", **audit},
            )


def test_runtime_transaction_rolls_back_on_error(engine) -> None:  # type: ignore[no-untyped-def]
    outbox_id = str(uuid4())
    idempotency_key = f"rollback-check-{uuid4()}"
    audit = audit_values()
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    """INSERT INTO operations.outbox_event
                    (outbox_id,subject,idempotency_key,payload,version_reference,
                     retention_classification,audit_classification,immutability_classification)
                    VALUES (:id,'rollback-check',:idem,'{}'::jsonb,:version_reference,
                            :retention_classification,:audit_classification,'VERSIONED_STATE')"""
                ),
                {"id": outbox_id, "idem": idempotency_key, **audit},
            )
            raise RuntimeError("synthetic transaction failure")
    except RuntimeError:
        pass
    with engine.connect() as connection:
        assert (
            connection.execute(
                text("SELECT count(*) FROM operations.outbox_event WHERE outbox_id=:id"),
                {"id": outbox_id},
            ).scalar_one()
            == 0
        )


def test_semantic_governance_and_feature_persistence(engine) -> None:  # type: ignore[no-untyped-def]
    event_id = f"semantic-event-{uuid4()}"
    occurred = datetime.now(UTC)
    definition = FeatureDefinition(
        feature_id=f"feature-{uuid4()}",
        version="1",
        source_ids=("raw-1",),
        transformation="identity",
    )
    materialized = FeatureMaterialization(
        feature_id=definition.feature_id,
        version=definition.version,
        available_at=occurred,
        value="1.25",
        lineage_ids=("raw-1",),
    )
    with engine.begin() as connection:
        append_governance_event(
            connection,
            GovernanceEvent(event_id, GovernanceState.ACTIVE, occurred, "TEST_BOOTSTRAP"),
        )
        register_feature_definition(connection, definition, occurred)
        append_feature_materialization(connection, materialized)
        assert (
            connection.execute(
                text("SELECT state FROM governance.governance_event WHERE event_id=:id"),
                {"id": event_id},
            ).scalar_one()
            == "ACTIVE"
        )
        assert (
            connection.execute(
                text("SELECT value->>'value' FROM feature.materialization WHERE feature_id=:id"),
                {"id": definition.feature_id},
            ).scalar_one()
            == "1.25"
        )


def test_decision_feedback_and_decomposition_persistence(engine) -> None:  # type: ignore[no-untyped-def]
    now = datetime.now(UTC)
    record = DecisionRecord(
        decision_id=f"decision-{uuid4()}",
        version="1",
        members=("a",),
        approvals=("a",),
        dissent=(),
        quorum=1,
        provenance_ids=("evidence-1",),
        created_at=now,
    )
    feedback = FeedbackEvent(
        event_id=f"feedback-{uuid4()}",
        subject_id=record.decision_id,
        provenance_ids=("fill-1",),
        state="RECEIVED",
        payload={"outcome": "paper"},
    )
    decomposition = decomposition_records(record.decision_id, {"pnl": Decimal("2")}, "source-1")[0]
    with engine.begin() as connection:
        append_decision_record(connection, record, now)
        append_delivery(connection, Delivery(record.decision_id, 1, False), now)
        append_feedback_event(connection, feedback, now)
        append_decomposition_record(connection, decomposition, now)
        assert (
            connection.execute(
                text("SELECT passed FROM decision.decision_record WHERE decision_id=:id"),
                {"id": record.decision_id},
            ).scalar_one()
            is True
        )
        assert (
            connection.execute(
                text("SELECT state FROM feedback.event WHERE event_id=:id"),
                {"id": feedback.event_id},
            ).scalar_one()
            == "RECEIVED"
        )
