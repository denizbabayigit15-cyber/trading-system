from datetime import UTC, date, datetime
from decimal import Decimal

import pytest

from trading_system.contracts.futures import FuturesContract, FuturesRoot, resolve_nearest_contract
from trading_system.core.financial import FinancialNumber
from trading_system.providers.normalization import normalize_ibkr_event, normalize_timestamp
from trading_system.providers.paper import PaperAccount


def contract(root: FuturesRoot, expiry: date, *, bound: bool = True) -> FuturesContract:
    return FuturesContract(
        con_id=1,
        root=root,
        local_symbol=f"{root}X",
        exchange="CME",
        currency="USD",
        expiry=expiry,
        multiplier=FinancialNumber(value="2", scale=0, unit="USD"),
        min_tick=FinancialNumber(value="0.25", scale=2, unit="USD"),
        trading_class=str(root),
        market_data_entitlement_bound=bound,
        order_permission_bound=bound,
    )


def test_contract_resolution_fails_closed_without_entitlement() -> None:
    result = resolve_nearest_contract(
        FuturesRoot.MNQ,
        (contract(FuturesRoot.MNQ, date(2027, 3, 1), bound=False),),
        date(2026, 8, 18),
    )
    assert result.contract is None
    assert result.reason_code == "FUTURES_CONTRACT_BINDINGS_UNAVAILABLE"


def test_timestamp_and_event_normalization_are_utc() -> None:
    assert normalize_timestamp("2026-08-18T12:00:00+03:00").tzinfo is UTC
    event = normalize_ibkr_event(
        {
            "instrument_id": "MNQ-202709",
            "sequence": 4,
            "event_time": "2026-08-18T09:00:00Z",
            "price": "19000.25",
            "quantity": "1",
        },
        received_at=datetime(2026, 8, 18, 9, 0, 1, tzinfo=UTC),
    )
    assert event.price.value == Decimal("19000.2500")


def test_naive_provider_timestamp_is_rejected() -> None:
    with pytest.raises(ValueError, match="naive"):
        normalize_timestamp("2026-08-18T09:00:00")


def test_paper_account_reconciliation_is_explicit() -> None:
    account = PaperAccount("paper-test")
    snapshot = account.snapshot()
    decision = account.reconcile(snapshot)
    assert decision.status.value == "CLEAN"
