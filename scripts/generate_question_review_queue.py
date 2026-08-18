from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trading_system.contracts.question_review_queue import (
    SOURCE_CATALOG,
    TARGET_QUEUE,
    build_question_review_queue_from_path,
    render_question_review_queue,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / SOURCE_CATALOG
TARGET = ROOT / TARGET_QUEUE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the fail-closed W0 first-wave question review queue."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that the committed queue matches deterministic generation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rendered = render_question_review_queue(build_question_review_queue_from_path(SOURCE))

    if args.check:
        if not TARGET.is_file():
            print(
                f"FAIL: missing generated review queue: {TARGET.relative_to(ROOT)}", file=sys.stderr
            )
            return 1
        if TARGET.read_text(encoding="utf-8") != rendered:
            print(
                "FAIL: review queue is stale; run "
                "`uv run python scripts/generate_question_review_queue.py`",
                file=sys.stderr,
            )
            return 1
        print("PASS: first-wave review queue matches the 900-question candidate catalog")
        return 0

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(rendered, encoding="utf-8")
    print(f"generated {TARGET.relative_to(ROOT)} with 150 fail-closed review items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
