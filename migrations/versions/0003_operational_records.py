"""Add W3/W4 market, OMS, accounting, and evidence persistence.

Revision ID: 0003_operational_records
Revises: 0002_control_plane
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_operational_records"
down_revision: str | Sequence[str] | None = "0002_control_plane"
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
    op.execute(sa.text('CREATE SCHEMA IF NOT EXISTS "evidence"'))
    op.create_table(
        "raw_event",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider", sa.String(length=128), nullable=False),
        sa.Column("instrument_id", sa.String(length=255), nullable=False),
        sa.Column("sequence", sa.BigInteger(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("payload_sha256", sa.String(length=64), nullable=False),
        *_audit_columns(),
        sa.UniqueConstraint("provider", "instrument_id", "sequence", name="uq_raw_event_sequence"),
        sa.CheckConstraint("sequence >= 0", name="sequence_nonnegative"),
        sa.CheckConstraint("length(payload_sha256) = 64", name="payload_hash_length"),
        schema="market",
    )
    _immutable("market", "raw_event")

    op.create_table(
        "order_intent",
        sa.Column("order_id", sa.String(length=255), primary_key=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False, unique=True),
        sa.Column("instrument_id", sa.String(length=255), nullable=False),
        sa.Column("side", sa.String(length=8), nullable=False),
        sa.Column("quantity", postgresql.JSONB(), nullable=False),
        sa.Column("limit_price", postgresql.JSONB(), nullable=True),
        sa.Column("authorization_lease_id", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("external_order_id", sa.String(length=255), nullable=True),
        *_audit_columns(),
        sa.CheckConstraint("side IN ('BUY', 'SELL')", name="valid_side"),
        sa.CheckConstraint(
            "state IN ('CREATED', 'AUTHORIZED', 'SUBMITTED', 'UNKNOWN', 'PARTIALLY_FILLED', "
            "'FILLED', 'REJECTED', 'CANCELLED', 'EXPIRED')",
            name="valid_state",
        ),
        schema="execution",
    )
    op.create_table(
        "fill",
        sa.Column("fill_id", sa.String(length=255), primary_key=True),
        sa.Column("order_id", sa.String(length=255), nullable=False),
        sa.Column("quantity", postgresql.JSONB(), nullable=False),
        sa.Column("price", postgresql.JSONB(), nullable=False),
        sa.Column("fee", postgresql.JSONB(), nullable=False),
        sa.Column("external_trade_id", sa.String(length=255), nullable=False, unique=True),
        *_audit_columns(),
        sa.ForeignKeyConstraint(["order_id"], ["execution.order_intent.order_id"]),
        schema="execution",
    )
    _immutable("execution", "fill")

    op.create_table(
        "evidence_record",
        sa.Column("evidence_id", sa.String(length=255), primary_key=True),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("subject_id", sa.String(length=255), nullable=False),
        sa.Column("contract_version", sa.String(length=32), nullable=False),
        sa.Column("scope_hash", sa.String(length=64), nullable=True),
        sa.Column("producer", sa.String(length=255), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        sa.Column("payload_sha256", sa.String(length=64), nullable=False),
        *_audit_columns(),
        sa.CheckConstraint("length(payload_sha256) = 64", name="payload_hash_length"),
        schema="evidence",
    )
    _immutable("evidence", "evidence_record")

    op.create_table(
        "position_projection",
        sa.Column("instrument_id", sa.String(length=255), primary_key=True),
        sa.Column("quantity", postgresql.JSONB(), nullable=False),
        sa.Column("average_price", postgresql.JSONB(), nullable=False),
        sa.Column("realized_pnl", postgresql.JSONB(), nullable=False),
        sa.Column("fees", postgresql.JSONB(), nullable=False),
        sa.Column("projection_version", sa.BigInteger(), nullable=False),
        *_audit_columns(),
        schema="position",
    )


def downgrade() -> None:
    op.execute(
        sa.text("DROP TRIGGER IF EXISTS trg_evidence_record_immutable ON evidence.evidence_record")
    )
    op.drop_table("position_projection", schema="position")
    op.drop_table("evidence_record", schema="evidence")
    op.execute(sa.text("DROP TRIGGER IF EXISTS trg_fill_immutable ON execution.fill"))
    op.drop_table("fill", schema="execution")
    op.drop_table("order_intent", schema="execution")
    op.execute(sa.text("DROP TRIGGER IF EXISTS trg_raw_event_immutable ON market.raw_event"))
    op.drop_table("raw_event", schema="market")
    op.execute(sa.text('DROP SCHEMA IF EXISTS "evidence"'))
