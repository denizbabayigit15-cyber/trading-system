from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RuleResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    rule_id: str
    version: str
    passed: bool
    reason_codes: tuple[str, ...]


class RuleRegistry:
    def __init__(self) -> None:
        self._rules: dict[tuple[str, str], Callable[[dict[str, object]], bool]] = {}

    def register(
        self, rule_id: str, version: str, evaluator: Callable[[dict[str, object]], bool]
    ) -> None:
        key = (rule_id, version)
        if key in self._rules:
            raise ValueError("rule version already registered")
        self._rules[key] = evaluator

    def evaluate(self, rule_id: str, version: str, facts: dict[str, object]) -> RuleResult:
        try:
            passed = bool(self._rules[(rule_id, version)](facts))
        except KeyError:
            return RuleResult(
                rule_id=rule_id, version=version, passed=False, reason_codes=("RULE_UNKNOWN",)
            )
        return RuleResult(
            rule_id=rule_id,
            version=version,
            passed=passed,
            reason_codes=() if passed else ("RULE_FAILED",),
        )


class SetupState(StrEnum):
    DETECTED = "DETECTED"
    QUALIFIED = "QUALIFIED"
    INVALIDATED = "INVALIDATED"
    CONSUMED = "CONSUMED"


@dataclass(frozen=True, slots=True)
class SetupLifecycle:
    setup_id: str
    version: str
    state: SetupState = SetupState.DETECTED

    def transition(self, target: SetupState) -> SetupLifecycle:
        allowed = {
            SetupState.DETECTED: {SetupState.QUALIFIED, SetupState.INVALIDATED},
            SetupState.QUALIFIED: {SetupState.CONSUMED, SetupState.INVALIDATED},
            SetupState.INVALIDATED: set(),
            SetupState.CONSUMED: set(),
        }
        if target not in allowed[self.state]:
            raise ValueError("invalid setup lifecycle transition")
        return SetupLifecycle(self.setup_id, self.version, target)


def score_setup(features: dict[str, Decimal], weights: dict[str, Decimal] | None) -> Decimal | None:
    if weights is None or not weights or any(key not in features for key in weights):
        return None
    return Decimal(sum(features[key] * weight for key, weight in weights.items()))


class ConflictGraph:
    def __init__(self) -> None:
        self._edges: set[frozenset[str]] = set()

    def add_conflict(self, left: str, right: str) -> None:
        if left == right:
            raise ValueError("a signal cannot conflict with itself")
        self._edges.add(frozenset((left, right)))

    def conflicts(self, active: set[str]) -> tuple[tuple[str, str], ...]:
        return tuple(sorted((min(edge), max(edge)) for edge in self._edges if edge <= active))


class AlphaEnsemble:
    def combine(
        self, contributions: dict[str, Decimal], weights: dict[str, Decimal] | None
    ) -> Decimal | None:
        if weights is None or set(contributions) != set(weights):
            return None
        return Decimal(sum(contributions[key] * weights[key] for key in contributions))


class DependencyGraph:
    def __init__(self) -> None:
        self._dependencies: dict[str, set[str]] = {}

    def add(self, node: str, depends_on: str) -> None:
        if node == depends_on:
            raise ValueError("dependency self-cycle")
        self._dependencies.setdefault(node, set()).add(depends_on)

    def invalidated_by(self, changed: str) -> tuple[str, ...]:
        return tuple(sorted(node for node, deps in self._dependencies.items() if changed in deps))


class NoTradeRules:
    def __init__(self) -> None:
        self._rules: dict[str, Callable[[dict[str, object]], bool]] = {}

    def register(self, rule_id: str, evaluator: Callable[[dict[str, object]], bool]) -> None:
        if rule_id in self._rules:
            raise ValueError("no-trade rule already registered")
        self._rules[rule_id] = evaluator

    def evaluate(self, facts: dict[str, object]) -> tuple[bool, tuple[str, ...]]:
        failed = tuple(
            sorted(rule_id for rule_id, evaluator in self._rules.items() if not evaluator(facts))
        )
        return not failed, failed or ()


def authorize_signal(
    *, policy_ok: bool, lease_ok: bool, fresh: bool, in_scope: bool, risk_ok: bool
) -> tuple[bool, tuple[str, ...]]:
    failures = tuple(
        name
        for name, value in (
            ("POLICY_DENIED", policy_ok),
            ("AUTHORITY_LEASE_INVALID", lease_ok),
            ("DATA_STALE", fresh),
            ("SCOPE_DENIED", in_scope),
            ("RISK_DENIED", risk_ok),
        )
        if not value
    )
    return not failures, failures


class TradeThesis(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    thesis_id: str
    version: str
    signal_id: str
    evidence_ids: tuple[str, ...]
    assumptions: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    created_at: datetime


class DecisionRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    decision_id: str
    version: str
    members: tuple[str, ...]
    approvals: tuple[str, ...]
    dissent: tuple[str, ...]
    quorum: int = Field(gt=0)
    provenance_ids: tuple[str, ...] = ()
    created_at: datetime | None = None
    authority_lease_id: str | None = None
    state: str = "CREATED"

    @property
    def passed(self) -> bool:
        return len(self.approvals) >= self.quorum


@dataclass(frozen=True, slots=True)
class Delivery:
    decision_id: str
    attempt: int
    acknowledged: bool


class FeedbackEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: str
    subject_id: str
    provenance_ids: tuple[str, ...] = Field(min_length=1)
    state: str
    payload: dict[str, object]


class FeedbackProcessor:
    def __init__(self) -> None:
        self._states: dict[str, str] = {}

    def process(self, event: FeedbackEvent) -> str:
        current = self._states.get(event.event_id)
        if current is not None:
            return current
        if not event.provenance_ids:
            raise ValueError("feedback provenance is required")
        self._states[event.event_id] = "PROCESSED"
        return "PROCESSED"


class DecisionConsumer:
    def __init__(self) -> None:
        self._delivered: set[str] = set()
        self._acknowledged: set[str] = set()

    def deliver(self, decision_id: str, attempt: int) -> Delivery:
        if decision_id in self._delivered:
            return Delivery(decision_id, attempt, True)
        self._delivered.add(decision_id)
        return Delivery(decision_id, attempt, False)

    def acknowledge(self, decision_id: str) -> Delivery:
        if decision_id not in self._delivered:
            raise KeyError(decision_id)
        self._acknowledged.add(decision_id)
        return Delivery(decision_id, 0, True)
