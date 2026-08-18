from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from trading_system.core.financial import FinancialNumber


def test_decimal_string_is_quantized_half_even() -> None:
    value = FinancialNumber(value="12.345", scale=2, unit="USD")
    assert value.value == Decimal("12.34")
    assert value.canonical() == "12.34"


def test_even_rounding_moves_when_required() -> None:
    value = FinancialNumber(value="12.355", scale=2)
    assert value.canonical() == "12.36"


@pytest.mark.parametrize("invalid", [1.25, True, float("nan"), float("inf")])
def test_binary_float_and_bool_are_rejected(invalid: object) -> None:
    with pytest.raises(ValidationError):
        FinancialNumber(value=invalid, scale=2)
