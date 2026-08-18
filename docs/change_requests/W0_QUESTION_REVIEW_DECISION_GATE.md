# W0 question review decision gate

## Purpose

This slice materializes a fail-closed ledger for human review decisions on the
150 first-wave questions. The committed ledger starts empty and
non-authoritative. It does not invent owners, policies, tests, evidence, scope,
criticality, observation windows, or fail actions.

## Decision states

- `DRAFT` may retain `UNBOUND` mappings and cannot claim independent approval.
- `APPROVED` requires a semantic question version, SHA-256 scope hash, complete
  operational mappings, distinct owner and approver identities, explicit
  independent approval, and ordered UTC timestamps.
- Approval does not mean adoption. Every decision remains `NOT_ADOPTED`.
- Approval does not answer or execute a question. `UNKNOWN / NOT_EXECUTED`
  remains mandatory.
- No ledger record can grant live authority. `live_authorized` is constrained
  to `false`.

## Initial state

| Measure | Value |
|---|---:|
| First-wave questions | 150 |
| Decisions | 0 |
| Drafts | 0 |
| Independently approved | 0 |
| Adopted | 0 |
| Runtime PASS | 0 |
| Live authorized | false |

## Verification

```bash
uv run python scripts/validate_question_review_decisions.py
uv run python scripts/verify_contracts.py
uv run pytest
```

The next step requires real, reviewable decision inputs under change control.
Synthetic values used by contract tests are test fixtures only and must never
be copied into the committed ledger.
