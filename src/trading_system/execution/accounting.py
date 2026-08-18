from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from threading import Lock

from trading_system.core.financial import FinancialNumber
from trading_system.execution.orders import Fill, OrderSide


@dataclass(frozen=True, slots=True)
class PositionProjection:
    instrument_id: str
    quantity: FinancialNumber
    average_price: FinancialNumber
    realized_pnl: FinancialNumber
    fees: FinancialNumber


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    entry_id: str
    account_id: str
    currency: str
    amount: FinancialNumber
    entry_type: str
    source_id: str


class Ledger:
    """Append-only accounting ledger; balances are projections, not mutable history."""

    def __init__(self) -> None:
        self._entries: dict[str, LedgerEntry] = {}
        self._lock = Lock()

    def append(self, entry: LedgerEntry) -> LedgerEntry:
        with self._lock:
            existing = self._entries.get(entry.entry_id)
            if existing is not None:
                if existing != entry:
                    raise ValueError("ledger entry ID already contains different accounting data")
                return existing
            self._entries[entry.entry_id] = entry
            return entry

    def balance(self, account_id: str, currency: str) -> FinancialNumber | None:
        with self._lock:
            entries = tuple(
                entry
                for entry in self._entries.values()
                if entry.account_id == account_id and entry.currency == currency
            )
        if not entries:
            return None
        total = sum((entry.amount.value for entry in entries), Decimal("0"))
        first = entries[0].amount
        return FinancialNumber(value=total, scale=first.scale, unit=first.unit)


def apply_fill(
    current: PositionProjection | None,
    *,
    instrument_id: str,
    side: OrderSide,
    fill: Fill,
) -> PositionProjection:
    if current is None:
        current = PositionProjection(
            instrument_id=instrument_id,
            quantity=FinancialNumber(
                value=Decimal("0"), scale=fill.quantity.scale, unit=fill.quantity.unit
            ),
            average_price=fill.price,
            realized_pnl=FinancialNumber(
                value=Decimal("0"), scale=fill.price.scale, unit=fill.price.unit
            ),
            fees=FinancialNumber(value=Decimal("0"), scale=fill.fee.scale, unit=fill.fee.unit),
        )
    signed = fill.quantity.value if side is OrderSide.BUY else -fill.quantity.value
    new_quantity = current.quantity.value + signed
    old_quantity = current.quantity.value
    if old_quantity == 0 or (old_quantity > 0 and signed > 0) or (old_quantity < 0 and signed < 0):
        weighted = (
            abs(old_quantity) * current.average_price.value + abs(signed) * fill.price.value
        ) / abs(new_quantity)
        average = FinancialNumber(
            value=weighted, scale=current.average_price.scale, unit=current.average_price.unit
        )
        realized = current.realized_pnl
    else:
        closed = min(abs(old_quantity), abs(signed))
        pnl = (fill.price.value - current.average_price.value) * closed
        if old_quantity < 0:
            pnl = -pnl
        realized = FinancialNumber(
            value=current.realized_pnl.value + pnl,
            scale=current.realized_pnl.scale,
            unit=current.realized_pnl.unit,
        )
        average = current.average_price if new_quantity else fill.price
    return PositionProjection(
        instrument_id=instrument_id,
        quantity=FinancialNumber(
            value=new_quantity, scale=current.quantity.scale, unit=current.quantity.unit
        ),
        average_price=average,
        realized_pnl=realized,
        fees=FinancialNumber(
            value=current.fees.value + fill.fee.value,
            scale=current.fees.scale,
            unit=current.fees.unit,
        ),
    )
