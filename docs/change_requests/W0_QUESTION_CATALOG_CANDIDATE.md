# W0 question catalog candidate slice

Date: 2026-08-18  
Branch: `feat/w0-question-catalog`  
Source change requests: `CR-V3.0.0-PRECODE-001`, `CR-V2.3.1-ASQ-001`

## Purpose

Materialize the retained 900-question Markdown bank as a deterministic,
machine-readable candidate without inventing the missing authoritative
owner, policy, test, scope, criticality, applicability, or fail-action bindings.

## Delivered artifacts

- deterministic parser and generator;
- Pydantic fail-closed catalog model;
- Draft 2020-12 JSON Schema;
- 900-record generated candidate catalog;
- source-hash, ordering, uniqueness, count, status, and regeneration tests;
- contract verification and integrity-manifest coverage.

## Preserved boundaries

- `authority_status=NON_AUTHORITATIVE_CANDIDATE`;
- `runtime_pass_count=0`;
- all 900 records remain `UNKNOWN / NOT_EXECUTED`;
- all missing operational mappings remain `UNBOUND`;
- `question_registry_materialized=false`;
- `R1_CODE_READY=false`;
- `LIVE_AUTHORIZED=false`.

## Acceptance commands

```bash
uv run python scripts/generate_question_catalog.py --check
uv run python scripts/verify_contracts.py
uv run pytest
uv run ruff check .
uv run mypy src
```

The slice may be accepted only when all commands pass and review confirms that
`contracts/questions/question_registry.json` has not been synthesized. The next
mapping step requires explicit change control and reviewed source values.
