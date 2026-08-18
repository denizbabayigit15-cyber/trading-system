"""Create the fail-closed PostgreSQL foundation.

Revision ID: 0001_foundation
Revises: None
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_foundation"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMAS = (
    "core",
    "registry",
    "market",
    "features",
    "state",
    "regime",
    "context",
    "liquidity",
    "alpha",
    "strategy",
    "decision",
    "risk",
    "portfolio",
    "capital",
    "execution",
    "position",
    "reconciliation",
    "outcome",
    "attribution",
    "performance",
    "research",
    "validation",
    "certification",
    "governance",
    "audit",
    "observability",
    "ai",
    "memory",
    "notifications",
    "operations",
)


def _classification_columns(*, mutable: bool) -> list[sa.Column[object]]:
    columns: list[sa.Column[object]] = [
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column("version_reference", sa.String(length=128), nullable=False),
        sa.Column("retention_classification", sa.String(length=64), nullable=False),
        sa.Column("audit_classification", sa.String(length=64), nullable=False),
        sa.Column("immutability_classification", sa.String(length=64), nullable=False),
    ]
    if mutable:
        columns.append(
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            )
        )
    return columns


def upgrade() -> None:
    for schema in SCHEMAS:
        op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))

    op.create_table(
        "contract_manifest",
        sa.Column("manifest_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("contract_version", sa.String(length=32), nullable=False),
        sa.Column("artifact_path", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        *_classification_columns(mutable=False),
        sa.UniqueConstraint("artifact_path", name="uq_contract_manifest_artifact_path"),
        sa.CheckConstraint("length(sha256) = 64", name="sha256_length"),
        schema="registry",
    )

    op.create_table(
        "system_state",
        sa.Column("state_id", sa.SmallInteger(), primary_key=True),
        sa.Column("runtime_state", sa.String(length=64), nullable=False),
        sa.Column("live_authorized", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("reason_code", sa.String(length=128), nullable=False),
        sa.Column("lineage_reference", sa.String(length=128), nullable=True),
        *_classification_columns(mutable=True),
        sa.CheckConstraint("state_id = 1", name="singleton"),
        sa.CheckConstraint("live_authorized = false", name="w0_live_authority_locked_false"),
        schema="governance",
    )

    op.create_table(
        "event_log",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(length=255), nullable=False),
        sa.Column("schema_version", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=False),
        sa.Column("causation_id", sa.String(length=128), nullable=True),
        sa.Column("lineage_reference", sa.String(length=128), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("payload_sha256", sa.String(length=64), nullable=False),
        *_classification_columns(mutable=False),
        sa.CheckConstraint("length(payload_sha256) = 64", name="payload_sha256_length"),
        schema="audit",
    )
    op.create_index(
        "ix_audit_event_log_correlation_id",
        "event_log",
        ["correlation_id"],
        unique=False,
        schema="audit",
    )
    op.create_index(
        "ix_audit_event_log_occurred_at",
        "event_log",
        ["occurred_at"],
        unique=False,
        schema="audit",
    )

    op.create_table(
        "outbox_event",
        sa.Column("outbox_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("lineage_reference", sa.String(length=128), nullable=True),
        *_classification_columns(mutable=True),
        sa.UniqueConstraint("idempotency_key", name="uq_outbox_event_idempotency_key"),
        sa.CheckConstraint(
            "status IN ('PENDING', 'PUBLISHING', 'PUBLISHED', 'FAILED')", name="status"
        ),
        sa.CheckConstraint("attempts >= 0", name="attempts_nonnegative"),
        schema="operations",
    )
    op.create_index(
        "ix_operations_outbox_event_status_created_at",
        "outbox_event",
        ["status", "created_at"],
        unique=False,
        schema="operations",
    )

    op.execute(
        sa.text(
            """
            CREATE OR REPLACE FUNCTION audit.reject_immutable_mutation()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
              RAISE EXCEPTION
                'immutable record mutation rejected: %.%', TG_TABLE_SCHEMA, TG_TABLE_NAME;
            END;
            $$
            """
        )
    )
    op.execute(
        sa.text(
            """
            CREATE TRIGGER trg_event_log_immutable
            BEFORE UPDATE OR DELETE ON audit.event_log
            FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_mutation()
            """
        )
    )
    op.execute(
        sa.text(
            """
            CREATE TRIGGER trg_contract_manifest_immutable
            BEFORE UPDATE OR DELETE ON registry.contract_manifest
            FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_mutation()
            """
        )
    )

    op.execute(
        sa.text(
            """
            INSERT INTO governance.system_state (
              state_id,
              runtime_state,
              live_authorized,
              reason_code,
              version_reference,
              retention_classification,
              audit_classification,
              immutability_classification
            ) VALUES (
              1,
              'SAFE_MODE',
              false,
              'AUTH_LIVE_DISABLED',
              'package-0.1.0',
              'PERMANENT_GOVERNANCE',
              'CRITICAL',
              'VERSIONED_STATE'
            )
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DROP TRIGGER IF EXISTS trg_contract_manifest_immutable ON registry.contract_manifest"
        )
    )
    op.execute(sa.text("DROP TRIGGER IF EXISTS trg_event_log_immutable ON audit.event_log"))
    op.execute(sa.text("DROP FUNCTION IF EXISTS audit.reject_immutable_mutation()"))
    op.drop_index(
        "ix_operations_outbox_event_status_created_at",
        table_name="outbox_event",
        schema="operations",
    )
    op.drop_table("outbox_event", schema="operations")
    op.drop_index("ix_audit_event_log_occurred_at", table_name="event_log", schema="audit")
    op.drop_index("ix_audit_event_log_correlation_id", table_name="event_log", schema="audit")
    op.drop_table("event_log", schema="audit")
    op.drop_table("system_state", schema="governance")
    op.drop_table("contract_manifest", schema="registry")
    for schema in reversed(SCHEMAS):
        op.execute(sa.text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
