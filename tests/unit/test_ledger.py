from __future__ import annotations

from dataclasses import replace

import pytest

from trading_system.core.financial import FinancialNumber
from trading_system.execution.accounting import Ledger, LedgerEntry


def test_ledger_is_append_only_and_projects_balance() -> None:
    ledger = Ledger()
    first = LedgerEntry(
        "entry-1",
        "account-1",
        "USD",
        FinancialNumber(value="100", scale=2, unit="USD"),
        "DEPOSIT",
        "treasury-1",
    )
    ledger.append(first)
    ledger.append(first)
    ledger.append(
        LedgerEntry(
            "entry-2",
            "account-1",
            "USD",
            FinancialNumber(value="-5", scale=2, unit="USD"),
            "FEE",
            "fill-1",
        )
    )
    assert ledger.balance("account-1", "USD").value == FinancialNumber(value="95", scale=2).value
    with pytest.raises(ValueError):
        ledger.append(replace(first, source_id="other"))
