from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GateResult:
    gate_id: str
    allowed: bool
    missing: tuple[str, ...]


def evaluate_gate(gate_id: str, required: tuple[str, ...], available: frozenset[str]) -> GateResult:
    missing = tuple(item for item in required if item not in available)
    return GateResult(gate_id, not missing, missing)
