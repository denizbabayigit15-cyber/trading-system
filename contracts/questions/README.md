# V3.0.0 question control surface

The authoritative V3.0.0 900-question mapping is now materialized as
`question_registry.json` under accepted change request `CR-V3.0.0-PRECODE-001`.

The materialized control surface contains:

- `question_registry.json` — 900 authoritative design mappings;
- `question_relations.json` — explicit cross-control/evidence relationships;
- `traceability_matrix.json` — 900 requirement/policy/test mappings;
- `acceptance_matrix.json` — 900 planned acceptance records;
- `schemas/question_result.schema.json` — runtime question-result contract.

The earlier `question_catalog_candidate.json` remains retained as the deterministic,
source-faithful W0 extraction artifact. It is not the authoritative owner/policy/test
mapping. The 150-item first-wave queue and review workbook remain human-review aids.

Materialization and owner acceptance do not create runtime PASS or live authority.
Current safety truth remains:

- authoritative design questions: 900;
- runtime PASS: 0;
- runtime status: UNKNOWN;
- implementation status: NOT_IMPLEMENTED;
- independent approval: PENDING;
- R1 CODE_READY: false;
- LIVE_AUTHORIZED: false.

External scope, broker, venue, account, entitlement, capital, fee, threshold and
legal values must not be invented. Missing required evidence remains fail-closed.
