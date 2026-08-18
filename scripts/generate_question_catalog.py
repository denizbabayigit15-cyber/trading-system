from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trading_system.contracts.question_catalog import (
    SOURCE_DOCUMENT,
    TARGET_DOCUMENT,
    build_question_catalog,
    render_question_catalog,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / SOURCE_DOCUMENT
TARGET = ROOT / TARGET_DOCUMENT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the non-authoritative 900-question candidate catalog."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that the committed catalog matches deterministic generation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rendered = render_question_catalog(build_question_catalog(SOURCE))

    if args.check:
        if not TARGET.is_file():
            print(f"FAIL: missing generated catalog: {TARGET.relative_to(ROOT)}", file=sys.stderr)
            return 1
        if TARGET.read_text(encoding="utf-8") != rendered:
            print(
                "FAIL: question catalog is stale; run "
                "`uv run python scripts/generate_question_catalog.py`",
                file=sys.stderr,
            )
            return 1
        print("PASS: question catalog matches its reviewed Markdown source")
        return 0

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(rendered, encoding="utf-8")
    print(f"generated {TARGET.relative_to(ROOT)} with 900 safe candidate records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
