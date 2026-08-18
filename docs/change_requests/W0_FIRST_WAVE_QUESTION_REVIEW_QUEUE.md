# W0 first-wave question review queue

Date: 2026-08-18  
Branch: `feat/w0-question-review-queue`  
Source: V3.0.0 question-bank adoption candidate, section 8

## Purpose

Materialize a deterministic review queue for the baseline-designated first
families: `SV`, `EP`, `MI`, `VC`, `CY`, and `OR`. Each family contributes 25
questions, for 150 items total.

## Fail-closed state

- all 150 items are `REVIEW_REQUIRED`;
- approved and adopted counts are zero;
- scope, applicability, criticality, contract, policy, test, evidence,
  fail-action, owner, and approver values remain `UNBOUND`;
- runtime PASS count is zero;
- R1 and live authority remain false.

## Review boundary

The queue does not assign or recommend operational values. A later record may
leave `REVIEW_REQUIRED` only through explicit change control, impact analysis,
independent approval, executable tests, and immutable evidence. Queue generation
is not adoption evidence.

## Acceptance commands

```bash
uv run python scripts/generate_question_review_queue.py --check
uv run python scripts/verify_contracts.py
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```
