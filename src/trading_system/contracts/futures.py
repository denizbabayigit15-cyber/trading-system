from __future__ import annotations

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from trading_system.core.financial import FinancialNumber


class FuturesRoot(StrEnum):
    MNQ = "MNQ"
    MGC = "MGC"
    MBT = "MBT"


class FuturesContract(BaseModel):
    """A resolved, orderable futures contract returned by a provider."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    con_id: int = Field(gt=0)
    root: FuturesRoot
    local_symbol: str = Field(min_length=1)
    exchange: str = Field(min_length=1)
    currency: str = Field(min_length=3, max_length=3)
    expiry: date
    last_trade_date: date | None = None
    multiplier: FinancialNumber
    min_tick: FinancialNumber
    trading_class: str = Field(min_length=1)
    market_data_entitlement_bound: bool = False
    order_permission_bound: bool = False

    @model_validator(mode="after")
    def validate_contract(self) -> FuturesContract:
        if self.last_trade_date and self.last_trade_date > self.expiry:
            raise ValueError("last trade date cannot be after contract expiry")
        if self.multiplier.value <= 0 or self.min_tick.value <= 0:
            raise ValueError("contract multiplier and minimum tick must be positive")
        return self

    @property
    def orderable(self) -> bool:
        return self.market_data_entitlement_bound and self.order_permission_bound


class ContractResolution(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    requested_root: FuturesRoot
    contract: FuturesContract | None
    reason_code: str | None = None
    candidates: int = Field(ge=0)


def resolve_nearest_contract(
    root: FuturesRoot, contracts: tuple[FuturesContract, ...], as_of: date
) -> ContractResolution:
    candidates = tuple(
        contract for contract in contracts if contract.root is root and contract.expiry >= as_of
    )
    if not candidates:
        return ContractResolution(
            requested_root=root,
            contract=None,
            reason_code="FUTURES_CONTRACT_UNAVAILABLE",
            candidates=0,
        )
    ordered = sorted(candidates, key=lambda contract: (contract.expiry, contract.con_id))
    if len({item.expiry for item in ordered if item.expiry == ordered[0].expiry}) > 1:
        return ContractResolution(
            requested_root=root,
            contract=None,
            reason_code="FUTURES_CONTRACT_AMBIGUOUS",
            candidates=len(ordered),
        )
    selected = ordered[0]
    if not selected.orderable:
        return ContractResolution(
            requested_root=root,
            contract=None,
            reason_code="FUTURES_CONTRACT_BINDINGS_UNAVAILABLE",
            candidates=len(ordered),
        )
    return ContractResolution(requested_root=root, contract=selected, candidates=len(ordered))
