# CODING HANDOFF INSTRUCTIONS — V3.0.0

## Developer directive

Implement this package exactly under `DEVELOPER_CONSTITUTION_V2_0`. Begin with W0 and stop at each gate. Do not start live integration or strategy activation merely because later artifacts exist.

## Mandatory repository shape

```text
docs/                 normative contract, constitution, readiness
contracts/engines/    112 engine contracts
contracts/questions/  900 control mappings and traceability
contracts/strategies/ disabled research candidates
contracts/policies/   policy registry; values may be UNBOUND_REQUIRED
schemas/              JSON Schema 2020-12 contracts
events/               224 engine events and common event envelope
state/                engine, trade, order, strategy, certification states
tests/contract/       schema and consumer contracts
tests/unit/           deterministic calculations
tests/integration/    orchestrator and external adapter boundaries
tests/failure/        timeout, duplicate, stale, unknown, partial failure
tests/security/       authorization, provenance, tamper and injection
tests/replay/         temporal truth and deterministic replay
tests/economic/       net cost, impact, capacity and tail stress
evidence/             immutable per-gate outputs
```

## First implementation slice

1. Load and validate manifests/schemas.
2. Implement fixed-decimal numeric policy and reason-code types.
3. Implement immutable IDs, version/scope hashes and event envelope.
4. Implement Engines 97, 103, 109, 111 and existing governance/security/version/audit boundaries.
5. Implement temporal truth, lineage, reconciliation and external-state UNKNOWN handling.
6. Implement Engines 99 and 100 with property tests proving that missing/changed state denies authority.
7. Only then implement data/strategy/execution domains in dependency order.

## Absolute stop conditions

- Missing/ambiguous material behavior.
- Any attempt to use float as canonical financial truth.
- Direct engine call bypassing orchestrator.
- External parameter replaced with developer-chosen default.
- Unknown order/position/cash treated as safe.
- AI/manual control granting authority.
- Test marked PASS without executed immutable evidence.

## Completion statement required from developer

“I implemented only approved behavior, preserved UNBOUND external inputs, did not activate a strategy, did not claim runtime PASS without evidence, and did not grant live authority.”
