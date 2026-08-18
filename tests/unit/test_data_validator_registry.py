from trading_system.market_data.models import OrderBookSnapshot, Quote, Trade
from trading_system.market_data.quality import EventValidatorRegistry


def test_unknown_event_schema_fails_closed() -> None:
    registry = EventValidatorRegistry()
    assert registry.validate("unknown", {}).valid is False
    registry.register("quote", lambda payload: "bid" in payload)
    assert registry.validate("quote", {"bid": 1}).valid
    assert registry.validate("quote", {}).valid is False


def test_supported_market_event_models_are_typed_validators() -> None:
    registry = EventValidatorRegistry()
    for schema_id, model in (("quote", Quote), ("trade", Trade), ("order_book", OrderBookSnapshot)):
        registry.register_model(schema_id, model)
    assert all(
        not registry.validate(schema_id, {}).valid for schema_id in ("quote", "trade", "order_book")
    )
