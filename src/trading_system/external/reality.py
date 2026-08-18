from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from trading_system.core.financial import FinancialNumber
from trading_system.core.time import require_utc


class DecisionStatus(StrEnum):
    PASS = "PASS"  # noqa: S105 - contract status, not a credential
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class CapabilitySnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    provider_id: str = Field(min_length=1)
    venue_id: str = Field(min_length=1)
    account_id: str = Field(min_length=1)
    as_of: datetime
    supported_order_types: frozenset[str]
    supports_paper: bool
    supports_live: bool
    fresh: bool
    source_evidence_id: str | None

    @field_validator("as_of")
    @classmethod
    def as_of_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    def can_submit(self, order_type: str, *, live: bool) -> bool:
        return (
            self.fresh
            and order_type in self.supported_order_types
            and (self.supports_live if live else self.supports_paper)
            and self.source_evidence_id is not None
        )


class EntitlementDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str = Field(min_length=1)
    use: str = Field(min_length=1)
    status: DecisionStatus
    entitlement_id: str | None
    expires_at: datetime | None
    reason_code: str

    @field_validator("expires_at")
    @classmethod
    def expiry_is_utc(cls, value: datetime | None) -> datetime | None:
        return None if value is None else require_utc(value)


def evaluate_entitlement(
    source_id: str,
    use: str,
    *,
    entitlement_id: str | None,
    expires_at: datetime | None,
    at: datetime,
) -> EntitlementDecision:
    checked_at = require_utc(at)
    if entitlement_id is None or expires_at is None:
        return EntitlementDecision(
            source_id=source_id,
            use=use,
            status=DecisionStatus.BLOCKED,
            entitlement_id=entitlement_id,
            expires_at=expires_at,
            reason_code="DATA_ENTITLEMENT_UNBOUND",
        )
    if require_utc(expires_at) <= checked_at:
        return EntitlementDecision(
            source_id=source_id,
            use=use,
            status=DecisionStatus.BLOCKED,
            entitlement_id=entitlement_id,
            expires_at=expires_at,
            reason_code="DATA_ENTITLEMENT_EXPIRED",
        )
    return EntitlementDecision(
        source_id=source_id,
        use=use,
        status=DecisionStatus.PASS,
        entitlement_id=entitlement_id,
        expires_at=expires_at,
        reason_code="DATA_ENTITLEMENT_BOUND",
    )


class ComplianceDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    scope_hash: str = Field(min_length=1)
    status: DecisionStatus
    applicable_law_bound: bool
    restricted_product_clear: bool
    reason_codes: tuple[str, ...]


def evaluate_compliance(
    scope_hash: str,
    *,
    applicable_law_bound: bool,
    restricted_product_clear: bool,
) -> ComplianceDecision:
    reasons: list[str] = []
    if not applicable_law_bound:
        reasons.append("COMPLIANCE_LAW_UNBOUND")
    if not restricted_product_clear:
        reasons.append("COMPLIANCE_RESTRICTED_PRODUCT")
    return ComplianceDecision(
        scope_hash=scope_hash,
        status=DecisionStatus.PASS if not reasons else DecisionStatus.BLOCKED,
        applicable_law_bound=applicable_law_bound,
        restricted_product_clear=restricted_product_clear,
        reason_codes=tuple(reasons),
    )


class CounterpartyDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    counterparty_id: str = Field(min_length=1)
    status: DecisionStatus
    exposure_limit: FinancialNumber | None
    settlement_known: bool
    reason_codes: tuple[str, ...]


def evaluate_counterparty(
    counterparty_id: str,
    *,
    exposure_limit: FinancialNumber | None,
    settlement_known: bool,
) -> CounterpartyDecision:
    reasons: list[str] = []
    if exposure_limit is None:
        reasons.append("COUNTERPARTY_LIMIT_UNBOUND")
    if not settlement_known:
        reasons.append("COUNTERPARTY_SETTLEMENT_UNKNOWN")
    return CounterpartyDecision(
        counterparty_id=counterparty_id,
        status=DecisionStatus.PASS if not reasons else DecisionStatus.BLOCKED,
        exposure_limit=exposure_limit,
        settlement_known=settlement_known,
        reason_codes=tuple(reasons),
    )


class TreasuryState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    account_id: str = Field(min_length=1)
    cash: FinancialNumber | None
    collateral: FinancialNumber | None
    encumbered: FinancialNumber | None
    settlement_known: bool
    reason_codes: tuple[str, ...]

    @property
    def spendable(self) -> FinancialNumber | None:
        if self.cash is None or self.collateral is None or self.encumbered is None:
            return None
        if not self.settlement_known:
            return None
        return FinancialNumber(
            value=self.cash.value + self.collateral.value - self.encumbered.value,
            scale=self.cash.scale,
            unit=self.cash.unit,
        )


class RoutePlan(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    route_id: str = Field(min_length=1)
    authorization_id: str = Field(min_length=1)
    venue_id: str = Field(min_length=1)
    capability: CapabilitySnapshot
    status: DecisionStatus
    reason_codes: tuple[str, ...]


def build_route(
    route_id: str,
    authorization_id: str,
    capability: CapabilitySnapshot,
    *,
    order_type: str,
) -> RoutePlan:
    allowed = capability.can_submit(order_type, live=False)
    return RoutePlan(
        route_id=route_id,
        authorization_id=authorization_id,
        venue_id=capability.venue_id,
        capability=capability,
        status=DecisionStatus.PASS if allowed else DecisionStatus.BLOCKED,
        reason_codes=() if allowed else ("VENUE_CAPABILITY_UNKNOWN",),
    )


class ReferencePriceSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    instrument_id: str = Field(min_length=1)
    price: FinancialNumber | None
    source_id: str | None
    as_of: datetime
    fresh: bool
    verified: bool

    @field_validator("as_of")
    @classmethod
    def timestamp_is_utc(cls, value: datetime) -> datetime:
        return require_utc(value)

    @property
    def usable(self) -> bool:
        return (
            self.price is not None and self.source_id is not None and self.fresh and self.verified
        )
