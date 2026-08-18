"""Add provider-neutral paper integration records.

IBKR credentials, entitlements and account identity are intentionally not stored here.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0008_paper_provider_records"
down_revision: str | Sequence[str] | None = "0007_decision_authority"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "futures_contract",
        sa.Column("con_id", sa.BigInteger(), primary_key=True),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("root", sa.String(8), nullable=False),
        sa.Column("local_symbol", sa.String(64), nullable=False),
        sa.Column("exchange", sa.String(32), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("expiry", sa.Date(), nullable=False),
        sa.Column("last_trade_date", sa.Date(), nullable=True),
        sa.Column("multiplier", sa.Numeric(28, 8), nullable=False),
        sa.Column("min_tick", sa.Numeric(28, 8), nullable=False),
        sa.Column("trading_class", sa.String(32), nullable=False),
        sa.Column(
            "market_data_entitlement_bound", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column(
            "order_permission_bound", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
        sa.Column("lineage_reference", sa.String(128), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.CheckConstraint("root IN ('MNQ', 'MGC', 'MBT')", name="supported_futures_root"),
        schema="market",
    )
    op.create_index(
        "ix_market_futures_contract_root_expiry",
        "futures_contract",
        ["root", "expiry"],
        schema="market",
    )
    op.create_table(
        "paper_order_event",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("order_id", sa.String(128), nullable=False),
        sa.Column("idempotency_key", sa.String(255), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("lineage_reference", sa.String(128), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.UniqueConstraint(
            "idempotency_key", "state", name="uq_paper_order_event_idempotency_state"
        ),
        schema="execution",
    )
    op.create_table(
        "market_event",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("instrument_id", sa.String(128), nullable=False),
        sa.Column("sequence", sa.BigInteger(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("price", sa.Numeric(28, 8), nullable=False),
        sa.Column("quantity", sa.Numeric(28, 8), nullable=False),
        sa.Column("lineage_reference", sa.String(128), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.UniqueConstraint(
            "provider", "instrument_id", "sequence", name="uq_market_event_sequence"
        ),
        schema="market",
    )


def downgrade() -> None:
    op.drop_table("market_event", schema="market")
    op.drop_table("paper_order_event", schema="execution")
    op.drop_index(
        "ix_market_futures_contract_root_expiry", table_name="futures_contract", schema="market"
    )
    op.drop_table("futures_contract", schema="market")
