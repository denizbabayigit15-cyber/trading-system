from __future__ import annotations

from trading_system.contracts.loader import (
    load_question_review_decision_ledger,
    load_question_review_queue,
)
from trading_system.contracts.question_review_decisions import (
    validate_decision_ledger_against_queue,
)


def main() -> None:
    ledger = load_question_review_decision_ledger()
    queue = load_question_review_queue()
    validate_decision_ledger_against_queue(ledger, queue)

    print(
        "PASS: question review decision ledger is valid; "
        f"decisions={ledger.decision_count}, approved={ledger.approved_count}"
    )
    print("STATUS: adopted=0; runtime_pass=0; LIVE_AUTHORIZED=false")


if __name__ == "__main__":
    main()
