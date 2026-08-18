# Question catalog candidate and registry blocker

The V3.0.0 baseline references `contracts/questions/question_registry.json` as
the authoritative 900-question mapping. That JSON artifact was not present in
the supplied baseline files.

`question_catalog_candidate.json` is a deterministic, source-faithful extraction
of the retained Markdown question bank. It makes all 900 question IDs and texts
machine-readable, but it is deliberately marked `NON_AUTHORITATIVE_CANDIDATE`.
It is not an equivalent substitute for the missing owner/policy/test/fail-action
registry.

`first_wave_review_queue.json` selects the baseline-designated `SV`, `EP`, `MI`,
`VC`, `CY`, and `OR` families: 25 questions per family, 150 total. It is a
non-authoritative work queue, not an approval artifact. Every item remains
`REVIEW_REQUIRED`; every operational mapping remains `UNBOUND`.

`question_review_decision_ledger.json` is the fail-closed change-control ledger
for those 150 items. It begins with zero decisions. Draft records may remain
unbound; an `APPROVED` record must have complete mappings, a versioned and
hashed scope, different owner and approver identities, independent approval,
and ordered UTC timestamps. Approval still does not mean adoption, execution,
runtime PASS, or live authority.

The Excel template under `research/question_review/templates/` mirrors all 150
source questions for human data entry. Its editable states are limited to
`DRAFT` and `READY_FOR_REVIEW`; it cannot record approval or adoption. Copy the
template before entering real review data.

This package therefore records:

- expected questions: 900;
- candidate records materialized: 900 (237 binding-core source records + 663 proposed records);
- first-wave review items materialized: 150; approved/adopted: 0;
- review decisions materialized: 0; independently approved/adopted: 0;
- runtime PASS: 0;
- runtime UNKNOWN/NOT_EXECUTED: 900;
- scope/criticality/owner/policy/test/fail-action bindings: UNBOUND;
- authoritative machine registry materialized: false;
- R1 impact: blocking.

Do not generate owner, policy, legal applicability, or fail-action mappings by
guessing. Restore the authoritative artifact or open change control.

Regenerate and verify the candidate deterministically with:

```bash
uv run python scripts/generate_question_catalog.py
uv run python scripts/generate_question_catalog.py --check
uv run python scripts/generate_question_review_queue.py --check
uv run python scripts/validate_question_review_decisions.py
uv run python scripts/validate_question_review_workbook.py
```
