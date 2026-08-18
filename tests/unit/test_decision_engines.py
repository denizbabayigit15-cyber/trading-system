from decimal import Decimal

from trading_system.research.decision import (
    AlphaEnsemble,
    ConflictGraph,
    DecisionConsumer,
    DecisionRecord,
    DependencyGraph,
    FeedbackEvent,
    FeedbackProcessor,
    NoTradeRules,
    RuleRegistry,
    SetupLifecycle,
    SetupState,
    authorize_signal,
    score_setup,
)


def test_decision_engines_are_versioned_and_fail_closed() -> None:
    rules = RuleRegistry()
    rules.register("r", "1", lambda facts: facts.get("ok") is True)
    assert rules.evaluate("r", "1", {"ok": True}).passed
    assert not rules.evaluate("unknown", "1", {}).passed
    lifecycle = SetupLifecycle("s", "1").transition(SetupState.QUALIFIED)
    assert lifecycle.state is SetupState.QUALIFIED
    graph = ConflictGraph()
    graph.add_conflict("a", "b")
    assert graph.conflicts({"a", "b"}) == (("a", "b"),)
    assert score_setup({"x": Decimal("2")}, {"x": Decimal("0.5")}) == Decimal("1")
    assert AlphaEnsemble().combine({"a": Decimal("2")}, None) is None
    dependencies = DependencyGraph()
    dependencies.add("alpha", "feature")
    assert dependencies.invalidated_by("feature") == ("alpha",)
    no_trade = NoTradeRules()
    no_trade.register("halt", lambda facts: not bool(facts.get("halt")))
    assert no_trade.evaluate({"halt": True}) == (False, ("halt",))
    assert (
        authorize_signal(policy_ok=True, lease_ok=True, fresh=True, in_scope=True, risk_ok=False)[0]
        is False
    )


def test_decision_records_and_consumer_are_idempotent() -> None:
    record = DecisionRecord(
        decision_id="d",
        version="1",
        members=("a", "b"),
        approvals=("a",),
        dissent=("b",),
        quorum=1,
    )
    assert record.passed
    consumer = DecisionConsumer()
    assert consumer.deliver("d", 1).acknowledged is False
    assert consumer.deliver("d", 2).acknowledged is True
    assert consumer.deliver("e", 1).acknowledged is False
    assert consumer.acknowledge("e").acknowledged is True
    assert (
        FeedbackEvent(
            event_id="f", subject_id="d", provenance_ids=("p",), state="RECEIVED", payload={}
        ).subject_id
        == "d"
    )
    processor = FeedbackProcessor()
    feedback = FeedbackEvent(
        event_id="fb", subject_id="d", provenance_ids=("p",), state="RECEIVED", payload={}
    )
    assert processor.process(feedback) == "PROCESSED"
    assert processor.process(feedback) == "PROCESSED"
