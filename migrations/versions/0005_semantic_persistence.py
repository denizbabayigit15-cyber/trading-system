"""Persist governance events and versioned feature materializations.

Revision ID: 0005_semantic_persistence
Revises: 0004_event_producer
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005_semantic_persistence"
down_revision: str | Sequence[str] | None = "0004_event_producer"
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
        "governance_event",
        sa.Column("event_id", sa.String(length=255), primary_key=True),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason_code", sa.String(length=128), nullable=False),
        sa.Column("payload", postgresql.JSONB(), nullable=False),
        *_audit_columns(),
        schema="governance",
    )
    _immutable("governance", "governance_event")
    op.execute(sa.text('CREATE SCHEMA IF NOT EXISTS "feature"'))
    op.create_table(
        "definition",
        sa.Column("feature_id", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=128), nullable=False),
        sa.Column("source_ids", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("transformation", sa.Text(), nullable=False),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("feature_id", "version"),
        schema="feature",
    )
    _immutable("feature", "definition")
    op.create_table(
        "materialization",
        sa.Column("feature_id", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=128), nullable=False),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("value", postgresql.JSONB(), nullable=False),
        sa.Column("lineage_ids", postgresql.ARRAY(sa.Text()), nullable=False),
        *_audit_columns(),
        sa.ForeignKeyConstraint(
            ["feature_id", "version"],
            ["feature.definition.feature_id", "feature.definition.version"],
        ),
        sa.PrimaryKeyConstraint("feature_id", "version", "available_at"),
        schema="feature",
    )
    _immutable("feature", "materialization")


def downgrade() -> None:
    op.execute(
        sa.text("DROP TRIGGER IF EXISTS trg_materialization_immutable ON feature.materialization")
    )
    op.drop_table("materialization", schema="feature")
    op.execute(sa.text("DROP TRIGGER IF EXISTS trg_definition_immutable ON feature.definition"))
    op.drop_table("definition", schema="feature")
    op.execute(
        sa.text(
            "DROP TRIGGER IF EXISTS trg_governance_event_immutable ON governance.governance_event"
        )
    )
    op.drop_table("governance_event", schema="governance")
    op.execute(sa.text('DROP SCHEMA IF EXISTS "feature"'))
