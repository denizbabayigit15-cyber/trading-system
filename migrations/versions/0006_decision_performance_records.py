"""Persist decision delivery, feedback, and performance decomposition records.

Revision ID: 0006_decision_performance_records
Revises: 0005_semantic_persistence
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_dec_perf_records"
down_revision: str | Sequence[str] | None = "0005_semantic_persistence"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _audit_columns() -> list[sa.Column[object]]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version_reference", sa.String(length=128), nullable=False),
        sa.Column("retention_classification", sa.String(length=64), nullable=False),
        sa.Column("audit_classification", sa.String(length=64), nullable=False),
        sa.Column("immutability_classification", sa.String(length=64), nullable=False),
    ]


def _immutable(schema: str, table: str) -> None:
    op.execute(
        sa.text(
            f"CREATE TRIGGER trg_{table}_immutable BEFORE UPDATE OR DELETE ON {schema}.{table} "
            "FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_mutation()"
        )
    )


def upgrade() -> None:
    op.create_table(
        "decision_record",
        sa.Column("decision_id", sa.String(length=255), primary_key=True),
        sa.Column("version", sa.String(length=128), nullable=False),
        sa.Column("members", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("approvals", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("dissent", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("provenance_ids", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("quorum", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        *_audit_columns(),
        sa.CheckConstraint("quorum > 0", name="positive_quorum"),
        schema="decision",
    )
    _immutable("decision", "decision_record")
    op.create_table(
        "delivery",
        sa.Column("delivery_id", sa.String(length=255), primary_key=True),
        sa.Column("decision_id", sa.String(length=255), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("decision_id", "attempt", name="uq_decision_delivery_attempt"),
        schema="decision",
    )
    _immutable("decision", "delivery")
    op.execute(sa.text('CREATE SCHEMA IF NOT EXISTS "feedback"'))
    op.create_table(
        "event",
        sa.Column("event_id", sa.String(length=255), primary_key=True),
        sa.Column("subject_id", sa.String(length=255), nullable=False),
        sa.Column("provenance_ids", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("state", sa.String(length=64), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        *_audit_columns(),
        schema="feedback",
    )
    _immutable("feedback", "event")
    op.execute(sa.text('CREATE SCHEMA IF NOT EXISTS "performance"'))
    op.create_table(
        "decomposition_record",
        sa.Column("record_id", sa.String(length=255), primary_key=True),
        sa.Column("subject_id", sa.String(length=255), nullable=False),
        sa.Column("dimension", sa.String(length=255), nullable=False),
        sa.Column("contribution", postgresql.JSONB(), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=False),
        *_audit_columns(),
        schema="performance",
    )
    _immutable("performance", "decomposition_record")


def downgrade() -> None:
    for schema, table in (
        ("performance", "decomposition_record"),
        ("feedback", "event"),
        ("decision", "delivery"),
        ("decision", "decision_record"),
    ):
        op.execute(sa.text(f"DROP TRIGGER IF EXISTS trg_{table}_immutable ON {schema}.{table}"))
        op.drop_table(table, schema=schema)
    op.execute(sa.text('DROP SCHEMA IF EXISTS "performance"'))
    op.execute(sa.text('DROP SCHEMA IF EXISTS "feedback"'))
