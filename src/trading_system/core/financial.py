from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FinancialNumber(BaseModel):
    """Canonical fixed-decimal value; binary floats are never accepted."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    value: Decimal
    scale: int = Field(ge=0, le=18)
    unit: str | None = Field(default=None, min_length=1, max_length=16)

    @field_validator("value", mode="before")
    @classmethod
    def reject_float_and_parse(cls, value: object) -> Decimal:
        if isinstance(value, (float, bool)):
            raise ValueError("financial values must not cross the canonical boundary as float/bool")
        if not isinstance(value, (Decimal, int, str)):
            raise ValueError("financial value must be Decimal, int, or decimal string")
        try:
            parsed = Decimal(value)
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("invalid decimal value") from exc
        if not parsed.is_finite():
            raise ValueError("financial values must be finite")
        return parsed

    @model_validator(mode="after")
    def quantize_to_scale(self) -> Self:
        quantum = Decimal(1).scaleb(-self.scale)
        object.__setattr__(self, "value", self.value.quantize(quantum, rounding=ROUND_HALF_EVEN))
        return self

    def canonical(self) -> str:
        return format(self.value, f".{self.scale}f")
