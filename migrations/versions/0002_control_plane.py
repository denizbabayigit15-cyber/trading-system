"""Add W1/W2 immutable control-plane persistence.

Revision ID: 0002_control_plane
Revises: 0001_foundation
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_control_plane"
down_revision: str | Sequence[str] | None = "0001_foundation"
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


def _immutable_trigger(schema: str, table: str) -> None:
    op.execute(
        sa.text(
            f"""
            CREATE TRIGGER trg_{table}_immutable
            BEFORE UPDATE OR DELETE ON {schema}.{table}
            FOR EACH ROW EXECUTE FUNCTION audit.reject_immutable_mutation()
            """
        )
    )


def upgrade() -> None:
    op.create_table(
        "scope_decision",
        sa.Column("scope_decision_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("scope_hash", sa.String(length=64), nullable=True),
        sa.Column("candidate", postgresql.JSONB(), nullable=False),
        sa.Column("reason_codes", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("missing_bindings", postgresql.ARRAY(sa.Text()), nullable=False),
        *_audit_columns(),
        sa.CheckConstraint("status IN ('ACTIVE', 'BLOCKED')", name="valid_status"),
        sa.CheckConstraint(
            "(status = 'ACTIVE' AND scope_hash IS NOT NULL AND cardinality(reason_codes) = 0) "
            "OR (status = 'BLOCKED' AND scope_hash IS NULL AND cardinality(reason_codes) > 0)",
            name="fail_closed_scope",
        ),
        schema="governance",
    )
    _immutable_trigger("governance", "scope_decision")

    op.create_table(
        "lineage_node",
        sa.Column("artifact_id", sa.String(length=255), primary_key=True),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("producer", sa.String(length=255), nullable=False),
        sa.Column("source_ids", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("content_sha256", sa.String(length=64), nullable=False),
        sa.Column("lineage_hash", sa.String(length=64), nullable=False, unique=True),
        sa.Column("transformation", sa.Text(), nullable=True),
        sa.Column("transformation_version", sa.String(length=128), nullable=True),
        *_audit_columns(),
        sa.CheckConstraint("kind IN ('RAW', 'DERIVED')", name="valid_kind"),
        sa.CheckConstraint("length(content_sha256) = 64", name="content_hash_length"),
        sa.CheckConstraint("length(lineage_hash) = 64", name="lineage_hash_length"),
        sa.CheckConstraint(
            "(kind = 'RAW' AND cardinality(source_ids) = 0 AND transformation IS NULL "
            "AND transformation_version IS NULL) OR "
            "(kind = 'DERIVED' AND cardinality(source_ids) > 0 AND transformation IS NOT NULL "
            "AND transformation_version IS NOT NULL)",
            name="raw_derived_separation",
        ),
        schema="registry",
    )
    _immutable_trigger("registry", "lineage_node")

    op.create_table(
        "authority_decision",
        sa.Column("authorization_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("decision_id", sa.String(length=128), nullable=False),
        sa.Column("scope_hash", sa.String(length=64), nullable=False),
        sa.Column("snapshot_hash", sa.String(length=64), nullable=False),
        sa.Column("predicates", postgresql.JSONB(), nullable=False),
        sa.Column("failed_predicates", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("unknown_predicates", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("reason_codes", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("policy_versions", postgresql.JSONB(), nullable=False),
        sa.Column("final_authorized", sa.Boolean(), nullable=False),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        *_audit_columns(),
        sa.CheckConstraint("length(scope_hash) > 0", name="scope_hash_present"),
        sa.CheckConstraint("length(snapshot_hash) = 64", name="snapshot_hash_length"),
        sa.CheckConstraint(
            "NOT final_authorized OR (cardinality(failed_predicates) = 0 "
            "AND cardinality(unknown_predicates) = 0 AND cardinality(reason_codes) = 0)",
            name="authorized_has_no_failures",
        ),
        schema="decision",
    )
    _immutable_trigger("decision", "authority_decision")

    op.create_table(
        "authorization_lease",
        sa.Column("lease_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "authorization_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("decision.authority_decision.authorization_id"),
            nullable=False,
        ),
        sa.Column("bindings_hash", sa.String(length=64), nullable=False),
        sa.Column("bindings", postgresql.JSONB(), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("single_use", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("row_version", sa.Integer(), nullable=False, server_default="1"),
        sa.CheckConstraint("expires_at > issued_at", name="positive_validity_window"),
        sa.CheckConstraint("single_use", name="single_use_required"),
        sa.CheckConstraint("length(bindings_hash) = 64", name="bindings_hash_length"),
        schema="decision",
    )
    op.create_index(
        "ix_authorization_lease_expiry",
        "authorization_lease",
        ["expires_at"],
        schema="decision",
    )

    op.create_table(
        "reconciliation_decision",
        sa.Column("reconciliation_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("source_priority", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("source_observations", postgresql.JSONB(), nullable=False),
        sa.Column("resolution_rule", sa.Text(), nullable=True),
        sa.Column("resolved_by", sa.String(length=255), nullable=True),
        sa.Column("resolution_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolution_evidence", sa.Text(), nullable=True),
        *_audit_columns(),
        sa.CheckConstraint("status IN ('CLEAN', 'RECONCILIATION_REQUIRED')", name="valid_status"),
        sa.CheckConstraint(
            "status <> 'RECONCILIATION_REQUIRED' OR resolution_evidence IS NULL",
            name="unresolved_has_no_evidence",
        ),
        schema="reconciliation",
    )
    _immutable_trigger("reconciliation", "reconciliation_decision")


def downgrade() -> None:
    op.execute(
        sa.text(
            "DROP TRIGGER IF EXISTS trg_reconciliation_decision_immutable "
            "ON reconciliation.reconciliation_decision"
        )
    )
    op.drop_table("reconciliation_decision", schema="reconciliation")
    op.drop_index(
        "ix_authorization_lease_expiry", table_name="authorization_lease", schema="decision"
    )
    op.drop_table("authorization_lease", schema="decision")
    op.execute(
        sa.text(
            "DROP TRIGGER IF EXISTS trg_authority_decision_immutable ON decision.authority_decision"
        )
    )
    op.drop_table("authority_decision", schema="decision")
    op.execute(
        sa.text("DROP TRIGGER IF EXISTS trg_lineage_node_immutable ON registry.lineage_node")
    )
    op.drop_table("lineage_node", schema="registry")
    op.execute(
        sa.text("DROP TRIGGER IF EXISTS trg_scope_decision_immutable ON governance.scope_decision")
    )
    op.drop_table("scope_decision", schema="governance")
