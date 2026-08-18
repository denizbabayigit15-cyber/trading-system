"""Add producer ownership to immutable audit events.

Revision ID: 0004_event_producer
Revises: 0003_operational_records
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_event_producer"
down_revision: str | Sequence[str] | None = "0003_operational_records"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "event_log",
        sa.Column("producer", sa.String(length=255), nullable=False, server_default="unknown"),
        schema="audit",
    )
    op.alter_column("event_log", "producer", server_default=None, schema="audit")


def downgrade() -> None:
    op.drop_column("event_log", "producer", schema="audit")
