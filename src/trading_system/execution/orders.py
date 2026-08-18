from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from threading import Lock
from typing import Protocol

from trading_system.core.financial import FinancialNumber


class OrderState(StrEnum):
    CREATED = "CREATED"
    AUTHORIZED = "AUTHORIZED"
    SUBMITTED = "SUBMITTED"
    UNKNOWN = "UNKNOWN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True, slots=True)
class OrderIntent:
    order_id: str
    idempotency_key: str
    instrument_id: str
    side: OrderSide
    quantity: FinancialNumber
    limit_price: FinancialNumber | None
    authorization_lease_id: str
    state: OrderState = OrderState.CREATED
    external_order_id: str | None = None


@dataclass(frozen=True, slots=True)
class SubmitResult:
    accepted: bool
    state: OrderState
    external_order_id: str | None
    reason_code: str | None


@dataclass(frozen=True, slots=True)
class AmendRequest:
    order_id: str
    new_quantity: FinancialNumber | None = None
    new_limit_price: FinancialNumber | None = None
    idempotency_key: str = ""


@dataclass(frozen=True, slots=True)
class CancelResult:
    accepted: bool
    state: OrderState
    reason_code: str | None


@dataclass(frozen=True, slots=True)
class Fill:
    fill_id: str
    order_id: str
    quantity: FinancialNumber
    price: FinancialNumber
    fee: FinancialNumber
    external_trade_id: str


@dataclass(frozen=True, slots=True)
class ExecutionReport:
    order_id: str
    state: OrderState
    cumulative_quantity: FinancialNumber
    leaves_quantity: FinancialNumber
    fill: Fill | None = None
    reject_reason: str | None = None


_ALLOWED_TRANSITIONS: dict[OrderState, frozenset[OrderState]] = {
    OrderState.CREATED: frozenset({OrderState.AUTHORIZED, OrderState.CANCELLED}),
    OrderState.AUTHORIZED: frozenset({OrderState.SUBMITTED, OrderState.CANCELLED}),
    OrderState.SUBMITTED: frozenset(
        {
            OrderState.UNKNOWN,
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.REJECTED,
            OrderState.CANCELLED,
            OrderState.EXPIRED,
        }
    ),
    OrderState.UNKNOWN: frozenset(
        {
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.REJECTED,
            OrderState.CANCELLED,
            OrderState.EXPIRED,
        }
    ),
    OrderState.PARTIALLY_FILLED: frozenset(
        {OrderState.PARTIALLY_FILLED, OrderState.FILLED, OrderState.CANCELLED}
    ),
    OrderState.FILLED: frozenset(),
    OrderState.REJECTED: frozenset(),
    OrderState.CANCELLED: frozenset(),
    OrderState.EXPIRED: frozenset(),
}


def transition_order(order: OrderIntent, target: OrderState) -> OrderIntent:
    if target not in _ALLOWED_TRANSITIONS[order.state]:
        raise ValueError(f"invalid order transition: {order.state} -> {target}")
    return replace(order, state=target)


class OrderBook:
    """In-memory deterministic OMS projection keyed by idempotency and client order ID."""

    def __init__(self) -> None:
        self._orders: dict[str, OrderIntent] = {}
        self._fills: dict[str, tuple[Fill, ...]] = {}
        self._lock = Lock()

    def add(self, order: OrderIntent) -> OrderIntent:
        with self._lock:
            existing = self._orders.get(order.idempotency_key)
            if existing is not None:
                same_intent = (
                    existing.order_id == order.order_id
                    and existing.instrument_id == order.instrument_id
                    and existing.side is order.side
                    and existing.quantity == order.quantity
                    and existing.limit_price == order.limit_price
                    and existing.authorization_lease_id == order.authorization_lease_id
                )
                if not same_intent:
                    raise ValueError("idempotency key is bound to a different order")
                return existing
            self._orders[order.idempotency_key] = order
            self._fills.setdefault(order.order_id, ())
            return order

    def apply_report(self, report: ExecutionReport) -> OrderIntent:
        with self._lock:
            order = next(
                (item for item in self._orders.values() if item.order_id == report.order_id), None
            )
            if order is None:
                raise KeyError(report.order_id)
            updated = transition_order(order, report.state)
            self._orders[order.idempotency_key] = updated
            if report.fill is not None:
                self._fills[order.order_id] = (*self._fills[order.order_id], report.fill)
            return updated

    def fills(self, order_id: str) -> tuple[Fill, ...]:
        with self._lock:
            return self._fills.get(order_id, ())


class ExecutionAdapter(Protocol):
    async def submit(self, intent: OrderIntent) -> SubmitResult: ...

    async def query_by_idempotency_key(self, idempotency_key: str) -> SubmitResult: ...

    async def amend(self, request: AmendRequest) -> SubmitResult: ...

    async def cancel(self, order_id: str, idempotency_key: str) -> CancelResult: ...


class PaperExecutionAdapter:
    """Deterministic adapter that records paper acknowledgements and never reaches a venue."""

    def __init__(self) -> None:
        self._results: dict[str, SubmitResult] = {}
        self._orders: dict[str, OrderIntent] = {}
        self._lock = Lock()

    async def submit(self, intent: OrderIntent) -> SubmitResult:
        if intent.state is not OrderState.AUTHORIZED:
            return SubmitResult(False, intent.state, None, "ORDER_NOT_AUTHORIZED")
        with self._lock:
            prior = self._results.get(intent.idempotency_key)
            if prior is not None:
                return prior
            result = SubmitResult(True, OrderState.SUBMITTED, f"paper-{intent.order_id}", None)
            self._results[intent.idempotency_key] = result
            self._orders[intent.order_id] = replace(
                intent,
                state=OrderState.SUBMITTED,
                external_order_id=result.external_order_id,
            )
            return result

    async def query_by_idempotency_key(self, idempotency_key: str) -> SubmitResult:
        with self._lock:
            return self._results.get(
                idempotency_key,
                SubmitResult(False, OrderState.UNKNOWN, None, "ORDER_EXTERNAL_STATE_UNKNOWN"),
            )

    async def amend(self, request: AmendRequest) -> SubmitResult:
        with self._lock:
            order = self._orders.get(request.order_id)
            if order is None:
                return SubmitResult(False, OrderState.UNKNOWN, None, "ORDER_NOT_FOUND")
            if order.state not in {OrderState.SUBMITTED, OrderState.PARTIALLY_FILLED}:
                return SubmitResult(
                    False, order.state, order.external_order_id, "ORDER_AMEND_NOT_ALLOWED"
                )
            if request.new_quantity is None and request.new_limit_price is None:
                return SubmitResult(
                    False, order.state, order.external_order_id, "ORDER_AMEND_EMPTY"
                )
            amended = replace(
                order,
                quantity=request.new_quantity or order.quantity,
                limit_price=request.new_limit_price or order.limit_price,
            )
            self._orders[request.order_id] = amended
            return SubmitResult(True, amended.state, amended.external_order_id, None)

    async def cancel(self, order_id: str, idempotency_key: str) -> CancelResult:
        with self._lock:
            order = self._orders.get(order_id)
            if order is None:
                return CancelResult(False, OrderState.UNKNOWN, "ORDER_NOT_FOUND")
            if order.idempotency_key != idempotency_key:
                return CancelResult(False, OrderState.UNKNOWN, "ORDER_IDEMPOTENCY_MISMATCH")
            if order.state in {
                OrderState.CANCELLED,
                OrderState.FILLED,
                OrderState.REJECTED,
                OrderState.EXPIRED,
            }:
                return CancelResult(False, order.state, "ORDER_CANCEL_NOT_ALLOWED")
            self._orders[order_id] = replace(order, state=OrderState.CANCELLED)
            return CancelResult(True, OrderState.CANCELLED, None)


def authorize_order(intent: OrderIntent, *, lease_consumed: bool) -> OrderIntent:
    if intent.state is not OrderState.CREATED:
        raise ValueError("only a created order can be authorized")
    if not lease_consumed:
        raise ValueError("order authorization requires an atomically consumed lease")
    return replace(intent, state=OrderState.AUTHORIZED)
