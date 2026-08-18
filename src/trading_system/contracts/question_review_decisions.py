from __future__ import annotations

from trading_system.contracts.models import QuestionReviewDecisionLedger, QuestionReviewQueue


def validate_decision_ledger_against_queue(
    ledger: QuestionReviewDecisionLedger,
    queue: QuestionReviewQueue,
) -> None:
    queue_ids = {item.question_id for item in queue.items}
    unknown_ids = sorted(
        record.question_id for record in ledger.decisions if record.question_id not in queue_ids
    )
    if unknown_ids:
        raise ValueError(f"decision ledger contains IDs outside the review queue: {unknown_ids}")
