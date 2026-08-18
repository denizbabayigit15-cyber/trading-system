"""Add authority binding and lifecycle state to decision records.

Revision ID: 0007_decision_authority
Revises: 0006_dec_perf_records
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_decision_authority"
down_revision: str | Sequence[str] | None = "0006_dec_perf_records"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "decision_record",
        sa.Column("authority_lease_id", sa.String(length=255), nullable=True),
        schema="decision",
    )
    op.add_column(
        "decision_record",
        sa.Column("state", sa.String(length=32), nullable=False, server_default="CREATED"),
        schema="decision",
    )


def downgrade() -> None:
    op.drop_column("decision_record", "state", schema="decision")
    op.drop_column("decision_record", "authority_lease_id", schema="decision")
