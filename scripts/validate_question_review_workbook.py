from __future__ import annotations

from trading_system.contracts.loader import (
    load_question_review_queue,
    load_question_review_workbook_manifest,
    repository_root,
)
from trading_system.contracts.question_review_workbook import (
    validate_question_review_workbook,
)


def main() -> None:
    manifest = load_question_review_workbook_manifest()
    validate_question_review_workbook(manifest, load_question_review_queue(), repository_root())
    print("PASS: review workbook contains all 150 first-wave questions and matches its hash")
    print("STATUS: decisions=0; approved=0; adopted=0; LIVE_AUTHORIZED=false")


if __name__ == "__main__":
    main()
