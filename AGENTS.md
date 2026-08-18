# Trading System — Codex Autonomous Engineering Instructions

## Mission

Implement this repository completely and production-grade according to the authoritative V3.0.0 contracts, schemas, registries, safety rules, evidence requirements, and implementation waves already present in the repository.

Work autonomously inside this repository. Do not stop for routine implementation choices, code edits, refactors, dependency installation, local service setup, tests, linting, formatting, typing, documentation, or non-destructive debugging.

The goal is to leave the repository in the most complete, internally tested, reproducible state possible so that the owner primarily needs to perform real-world validation, supply external credentials/entitlements where required, and conduct final acceptance/testing.

## Source of truth and precedence

1. V3.0.0 normative material has precedence over conflicting retained V2.x history.
2. Preserve stricter retained safety, evidence, reconciliation, lineage, certification, and fail-closed requirements.
3. `contracts/questions/question_registry.json` is the authoritative 900-question registry.
4. Target engine inventory is 112 engines.
5. Do not reinterpret historical documents as current authority when V3 explicitly supersedes them.
6. Never fabricate external facts, thresholds, approvals, evidence, credentials, entitlements, broker capabilities, venue rules, or market-data permissions.

## Owner acceptance boundary

`CR-V3.0.0-PRECODE-001` has owner acceptance for controlled framework/scaffolding implementation.

This does NOT mean:
- independent validation is complete;
- runtime questions have PASS evidence;
- strategies are approved for live use;
- empirical thresholds are approved;
- R1_CODE_READY is true;
- R2_TEST_READY is true;
- R3_OPERATIONALLY_LIVE_READY is true;
- R4_PROFITABILITY_CERTIFIED is true;
- LIVE_AUTHORIZED is true.

Unknown or externally dependent values must remain explicitly UNKNOWN / PENDING / UNBOUND and must fail closed.

## Autonomous permissions

Within this repository you may autonomously:

- inspect all source, contract, schema, test, documentation, migration, configuration, and Git files;
- create, edit, move, or delete repository files when necessary for the implementation;
- install development/runtime dependencies required by the repository;
- run Python, uv, pytest, Ruff, mypy, schema validators, scripts, Docker/Compose, PostgreSQL tooling, and other project-local development commands;
- create migrations, fixtures, adapters, services, test doubles, simulators, mocks, and test infrastructure;
- research official technical documentation when network access is available;
- fix failures and continue iterating until the relevant validation suite is green;
- refactor code when required to satisfy contracts and maintainability;
- update implementation documentation and status files to accurately reflect reality;
- create local Git commits when useful.

Do not repeatedly ask the user for routine engineering decisions. Infer the safest contract-compliant implementation and continue.

## Actions that remain prohibited without explicit owner authorization

Never autonomously:

- place a real-money order;
- enable actual live trading;
- change `LIVE_AUTHORIZED` to true;
- claim R1/R2/R3/R4 certification without required evidence;
- transfer funds or initiate treasury movements;
- create, modify, purchase, or accept a broker/data-provider account agreement;
- perform KYC;
- purchase subscriptions or incur paid external-service charges;
- expose, print, commit, log, or transmit secrets unnecessarily;
- fabricate an API credential or external entitlement;
- bypass an explicit safety control merely to make tests pass;
- push to a remote Git repository;
- merge a pull request;
- force-push;
- run destructive Git history operations such as `git reset --hard` on user work;
- delete user work merely because it is inconvenient.

## Secrets

Never hard-code secrets.

Use environment variables, `.env.example`, secret stores, or equivalent secure configuration patterns.

Ensure actual secret files and credentials are ignored by Git.

Do not include real credentials in test fixtures, logs, snapshots, examples, or documentation.

## Trading-system safety model

The following implication is always false:

`API_CONNECTED => LIVE_AUTHORIZED`

Connectivity, successful authentication, market-data receipt, paper execution, or successful order simulation alone never grants live authority.

All execution paths must fail closed when required authorization, freshness, lineage, reconciliation, risk, policy, state, identity, or evidence is absent or invalid.

## Implementation waves

Respect dependency order:

W0 — contracts, schemas, reason codes, integrity, question control
W1 — identity, scope, policy, security, temporal truth, lineage
W2 — authority evaluator, authorization lease, reconciliation, risk
W3 — market data, features, strategy research, replay/backtest
W4 — OMS, execution, routing, counterparty, treasury, accounting
W5 — acceptance, failure injection, security, performance
W6 — shadow, paper, micro, probation
W7 — scope-exact R4 review and current live authorization

Later-wave artifacts must not be used as fake evidence that an earlier wave passed.

You may implement later-wave code when dependencies are sufficiently defined, but readiness claims must remain truthful.

## External integrations

Build real production-quality integration architecture for broker, market-data, storage, messaging, and other providers where required.

Where real credentials or subscriptions are unavailable:

- implement adapters and interfaces;
- implement configuration and secret loading;
- implement sandbox/paper/test connectivity paths;
- implement mocks/simulators where necessary;
- implement retry, reconnect, timeout, rate-limit, sequence-gap, idempotency, reconciliation, and observability behavior;
- document the exact remaining external input;
- leave live activation fail closed.

Do not replace missing real-world values with arbitrary constants.

## Engineering standards

Prefer:

- typed interfaces;
- deterministic behavior;
- explicit state machines;
- idempotency;
- immutable audit evidence where applicable;
- explicit reason codes;
- monotonic event handling where required;
- strong validation at boundaries;
- deterministic replay;
- reproducible tests;
- dependency inversion around external systems;
- structured logging;
- metrics and health checks;
- clear failure semantics.

Avoid hidden fallbacks.

A missing critical value must not silently become a permissive default.

## Question-control requirements

The V3 question registry contains 900 authoritative questions.

Materialization or mapping does not itself mean PASS.

For every runtime answer or readiness claim:

- preserve question identity/version;
- preserve ownership and policy linkage;
- preserve test/scenario linkage;
- record evidence where required;
- respect independent approval requirements;
- distinguish design binding from runtime evidence;
- keep UNKNOWN/PENDING when evidence is insufficient.

## Independent review

Generator self-check is not independent review.

Do not mark independent validation complete based solely on your own implementation or tests.

Prepare all artifacts needed for independent review, but preserve the independent-review gate.

## Testing policy

After meaningful changes, run the most relevant focused tests first.

Before declaring a work unit complete, run the full applicable baseline:

- `uv run python scripts/build_integrity_manifest.py` when integrity-covered files changed;
- `uv run python scripts/verify_contracts.py`;
- `uv run pytest`;
- `uv run ruff check .`;
- `uv run ruff format --check .`;
- `uv run mypy src`.

If formatting changes integrity-covered files, rebuild the integrity manifest and re-run verification.

Continue fixing failures until green unless the failure requires genuinely unavailable external information.

Never weaken a test, contract, schema, or safety invariant merely to obtain a green result.

## Existing work protection

Before major changes inspect:

- `git status`;
- current branch;
- existing uncommitted changes.

Preserve user work.

Do not discard or overwrite unrelated changes.

## Completion behavior

Do not stop after analysis if implementation is possible.

Use this loop:

1. inspect;
2. determine the next contract-compliant implementation slice;
3. implement it;
4. test it;
5. fix failures;
6. re-test;
7. update accurate documentation/status;
8. continue to the next feasible slice.

Stop only when:

- all currently implementable work is complete and validated; or
- a truly external dependency blocks further progress.

When externally blocked, leave the repository safe and provide a concise blocker list stating exactly what the owner must supply or validate.

The final repository state must never overstate readiness.
