from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.financial import FinancialNumber
from trading_system.core.time import require_utc
from trading_system.execution.accounting import PositionProjection
from trading_system.execution.orders import ExecutionReport, Fill, OrderIntent, OrderState
from trading_system.reconciliation.models import (
    ReconciliationDecision,
    SourceObservation,
    compare_sources,
)


class PaperAccountSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    account_id: str = Field(min_length=1)
    currency: str = Field(min_length=3, max_length=3)
    cash: FinancialNumber
    positions: tuple[PositionProjection, ...]
    observed_at: datetime
    source_id: str = "paper-simulator"

    @field_validator("observed_at")
    @classmethod
    def observed_at_utc(cls, value: datetime) -> datetime:
        return require_utc(value)


@dataclass(slots=True)
class PaperAccount:
    account_id: str
    currency: str = "USD"
    cash: FinancialNumber = field(
        default_factory=lambda: FinancialNumber(value=Decimal("0"), scale=2, unit="USD")
    )
    _positions: dict[str, PositionProjection] = field(default_factory=dict)
    _reports: list[ExecutionReport] = field(default_factory=list)

    def apply_fill(self, intent: OrderIntent, fill: Fill) -> ExecutionReport:
        from trading_system.execution.accounting import apply_fill

        previous = self._positions.get(intent.instrument_id)
        self._positions[intent.instrument_id] = apply_fill(
            previous, instrument_id=intent.instrument_id, side=intent.side, fill=fill
        )
        report = ExecutionReport(
            order_id=intent.order_id,
            state=OrderState.FILLED,
            cumulative_quantity=fill.quantity,
            leaves_quantity=FinancialNumber(
                value=Decimal("0"), scale=fill.quantity.scale, unit=fill.quantity.unit
            ),
            fill=fill,
        )
        self._reports.append(report)
        return report

    def snapshot(self, *, observed_at: datetime | None = None) -> PaperAccountSnapshot:
        observed = observed_at or datetime.now(UTC)
        return PaperAccountSnapshot(
            account_id=self.account_id,
            currency=self.currency,
            cash=self.cash,
            positions=tuple(self._positions.values()),
            observed_at=observed,
        )

    def reconcile(self, provider_snapshot: PaperAccountSnapshot) -> ReconciliationDecision:
        local = self.snapshot(observed_at=provider_snapshot.observed_at)
        local_hash = sha256(local.model_dump_json().encode()).hexdigest()
        provider_hash = sha256(provider_snapshot.model_dump_json().encode()).hexdigest()
        # Hashes are only an in-process comparison; durable evidence uses the audit lineage.
        return compare_sources(
            (
                SourceObservation(
                    source_id="paper-ledger",
                    version="1",
                    state_hash=local_hash,
                    observed_at=local.observed_at,
                ),
                SourceObservation(
                    source_id=provider_snapshot.source_id,
                    version="1",
                    state_hash=provider_hash,
                    observed_at=provider_snapshot.observed_at,
                ),
            )
        )
