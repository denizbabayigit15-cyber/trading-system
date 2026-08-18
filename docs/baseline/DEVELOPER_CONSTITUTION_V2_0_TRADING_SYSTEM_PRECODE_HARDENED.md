# DEVELOPER CONSTITUTION V2.0 — TRADING SYSTEM V3.0.0

This file retains V1.1 and adds binding V2.0 articles. The V2.0 articles have precedence where wording conflicts.

---
# DEVELOPER CONSTITUTION — TRADING SYSTEM V2.2.5 / V1.1

**Document type:** Binding Developer Constitution / Engineering Law
**Authority:** This document is subordinate only to the Master Implementation Contract V2.2.5 and applicable approved policies. It binds every developer, reviewer, DevOps engineer, data engineer, ML engineer and AI-assisted coding agent working on the system.
**Primary objective:** Build the system exactly as contracted, prove it with deterministic evidence, preserve capital and operational safety, and never invent material trading behavior.

> **Important limitation:** No constitution can guarantee future market profitability. This constitution can guarantee neither returns nor survival against every market event. It is designed to prevent engineering shortcuts, unproven assumptions, unsafe authority escalation and undocumented behavior, and to maximize the probability of reaching a validated, auditable production system.

---

## Article 1 — Supremacy of the Contract

1. The Master Implementation Contract is the source of truth for business behavior.
2. Code is subordinate to contract, policy, state and authorization contracts.
3. A developer may optimize implementation, but may not change material trading behavior without a Change Request.
4. The existence of an easier implementation is never evidence that the contract should be weakened.
5. The words `probably`, `should`, `usually`, `normally`, `safe enough`, and `we can assume` are not valid substitutes for a missing production rule.

## Article 2 — No Silent Assumptions

A developer shall never silently decide:

- data sufficiency;
- target/label semantics;
- fill behavior;
- stop/exit ordering;
- transaction costs;
- market impact;
- probability calibration;
- sample size;
- edge floor;
- regime transitions;
- decay thresholds;
- capacity;
- position sizing;
- portfolio dependence;
- historical universe;
- revision semantics;
- broker/venue state semantics;
- numerical precision;
- accounting treatment.

When any such rule is missing:

`STOP → CHANGE REQUEST → IMPACT ANALYSIS → CONTRACT VERSION → TEST → APPROVAL → IMPLEMENT`

## Article 3 — No Unapproved Trading Authority

1. No engine, model, feature, AI component, UI, script or database record may independently grant trading authority.
2. The single deterministic authority evaluator is the only final admission authority.
3. `false` and `UNKNOWN` cannot be promoted to `true` by a downstream component.
4. Signal approval, risk approval, capital approval and execution approval remain separate.
5. Unknown position state, unresolved reconciliation, invalid critical data, expired certification and unbound policy all block live authorization.

## Article 4 — Fail Closed

1. Critical uncertainty is represented explicitly as `UNKNOWN`.
2. No critical UNKNOWN may be coerced to zero, false, neutral or stale-but-usable.
3. Critical failure moves the runtime toward the safer state.
4. Recovery never restores trading authority merely because a process restarted.
5. Recovery must revalidate process, data, clock, venue, account, positions, orders, risk, capital and authority predicates.

## Article 5 — Data Truth

1. Raw observations are immutable.
2. Observed, derived, inferred and vendor-model information are never silently merged.
3. Point-in-time availability is authoritative for historical certification.
4. No future information may reach replay/backtest decision logic.
5. All material outputs preserve source, version, lineage, timestamp and quality metadata.
6. Registered source entitlement is distinct from technical connectivity.

## Article 6 — Strategy Discipline

1. A setup is not a trade.
2. A strategy registry entry is not production approval.
3. Alpha is separate from strategy expression.
4. Probability is separate from confidence.
5. Net expectancy is separate from probability.
6. Positive point-estimate EV cannot override negative uncertainty-adjusted EV, unacceptable tail risk or ruin risk.
7. Strategy eligibility is evaluated against current market profile, data quality, regime, cost, execution and policy.
8. Correlated strategies sharing an alpha factor share the appropriate risk budget.

## Article 7 — Execution Discipline

1. No order is created without valid execution authorization.
2. Venue constraints are validated locally before submission.
3. External side effects are idempotent.
4. A retry must not create a duplicate financial action.
5. Partial fills, rejects, cancels, replacements, expiry and unknown states are explicit states.
6. Execution must continuously compare edge half-life against expected execution time.
7. Reconciliation is mandatory after material execution uncertainty.

## Article 8 — Reconciliation Supremacy

1. External venue/broker truth must be reconciled against internal state.
2. MISMATCH, UNKNOWN or FAILED reconciliation blocks new orders unless a separately certified safe fallback exists.
3. Manual database edits must never be used to hide a reconciliation discrepancy.
4. Any manual operational intervention must be auditable and reversible.

## Article 9 — Risk and Capital

1. Risk sizing is deterministic.
2. AI may never enlarge risk authority.
3. No lower risk layer may exceed an upper-layer ceiling.
4. Capital allocation is portfolio-aware, not trade-isolated.
5. Capacity is a function of liquidity, impact, slippage, spread, speed, venue limits and emergency liquidation capacity.
6. Drawdown response must remain policy-driven.

## Article 10 — AI Governance

1. AI is a governed recommendation/research component.
2. Every AI output is versioned, attributable and auditable.
3. AI may not modify production code, risk ceilings, capital ceilings, security roles, kill switches, reconciliation rules or certification state.
4. AI may propose hypotheses; it may not silently deploy them.
5. AI failure must never increase trading authority.
6. AI must not become a hidden dependency of the low-latency critical path unless explicitly certified.

## Article 11 — Database and Event Discipline

1. Alembic is schema authority.
2. Manual production schema edits are prohibited.
3. Event delivery is at-least-once; consumers must be idempotent.
4. Transactional outbox/inbox patterns are required where database state and external side effects interact.
5. Every persisted decision-bearing object is traceable to its contract/version lineage.
6. No production event may exist without a consumer or explicit terminal classification.

## Article 12 — State Machines

1. Every state transition requires an explicit guard.
2. Illegal transitions must be rejected and audited.
3. State versioning is mandatory for critical state machines.
4. Recovery states are not normal operating states.
5. A state machine cannot bypass another state machine's authority boundary.

## Article 13 — Testing Law

No implementation item is DONE unless applicable tests pass:

- contract;
- schema;
- unit;
- integration;
- replay;
- failure injection;
- performance;
- security;
- observability;
- persistence;
- lineage;
- consumer;
- outcome;
- adversarial examination.

`GREEN_TESTS_WITHOUT_EVIDENCE = NOT_CERTIFIED`.

## Article 14 — Reproducibility

1. A decision must be reproducible from its recorded versions, snapshot, policies, parameters and inputs within documented numerical tolerance.
2. Dataset manifests, checksums, model artifacts, feature versions and build hashes are immutable evidence.
3. A model cannot be promoted if it cannot be reproduced.
4. A release cannot be activated without a complete manifest and rollback target.

## Article 15 — Security

1. Least privilege is mandatory.
2. AI is never system-admin.
3. Secrets may not appear in source control, fixtures, logs, telemetry or event payloads.
4. High-impact operations require explicit authorization and auditable identity.
5. Credential rotation and revocation are operational requirements.
6. Security failures are hard production blockers.

## Article 16 — Observability

Every critical engine must expose health, latency, throughput, error, staleness, input-quality, output and dependency state. Decision-bearing engines additionally expose decision counts, rejections, vetoes, reason-code distributions and expected-vs-realized measurements.

A system that cannot explain **why it cannot trade** is not production-ready.

## Article 17 — Incident and Recovery Discipline

1. Incidents are classified and linked to affected decisions/orders/positions.
2. Critical incidents may force SAFE_MODE, HALT or RECONCILIATION_REQUIRED.
3. Recovery must be tested, not merely documented.
4. Postmortems are required for defined critical incidents.
5. Repeated incidents trigger root-cause remediation or certification review.

## Article 18 — Research / Production Separation

1. Research may create candidates, never production authority.
2. Research datasets are versioned and point-in-time safe.
3. Research search budgets are enforced.
4. Multiple testing and selection bias must be recorded.
5. Production changes require validation and certification.

## Article 19 — Code Review Constitution

Every material change must answer:

- Which contract requirement does this implement?
- Which policy version governs it?
- Which state transitions are affected?
- What failure modes were considered?
- What tests prove correctness?
- What evidence will be persisted?
- What downstream consumers are affected?
- Does the change alter trading authority?
- Does the certification scope change?

A pull request without these answers is incomplete for production-critical work.

## Article 20 — Change Control

All non-trivial discoveries are classified as:

`BUG | CONTRACT_CORRECTION | ENHANCEMENT | NEW_REQUIREMENT | EXTERNAL_CONSTRAINT`

No undocumented production patch is permitted.

## Article 21 — Prohibited Shortcuts

The following are prohibited:

- hardcoded market data in production;
- fake fills in live execution code;
- silently falling back to lower-quality data;
- disabling a veto to “see if it works” in production;
- bypassing reconciliation;
- using mocks as production evidence;
- manually editing production decisions to make tests pass;
- deleting adverse outcomes;
- changing historical data to improve backtests;
- reporting a PASS without evidence;
- changing policy thresholds without versioning;
- bypassing security to speed development;
- hiding errors instead of classifying them.

## Article 22 — Definition of SUCCESS

For this system, success is not “the program runs.” Success means:

`CONTRACTED → IMPLEMENTED → TESTED → REPLAYABLE → OBSERVABLE → TRACEABLE → CERTIFIED → OPERATIONALLY SAFE → EMPIRICALLY VALIDATED`

Profitability is an empirical outcome and must never be fabricated by documentation.

## Article 23 — Developer Freedom

Developers may choose implementation details where the choice does not materially change trading behavior, authority, safety, accounting, reproducibility or certification scope. Such choices must remain documented and reversible.

## Article 24 — Final Oath of Implementation

Before merging production-critical code, the developer must be able to truthfully state:

> “I did not invent a material trading rule. I implemented the approved contract. I tested the failure paths. I preserved lineage. I did not create hidden authority. I can explain the behavior from contract to outcome. I can reproduce the result from the recorded versions. I know what the system does, what it does not do, and why it is allowed or forbidden to trade.”

If that statement is not true, the change is not ready for acceptance.


---

# V1.1 HARDENING ARTICLES — MANDATORY IMPLEMENTATION LAW

## Article 25 — Authority Lease and TOCTOU Protection

Execution authorization is a short-lived, scope-bound lease. A developer MUST NOT treat an earlier authorization decision as sufficient after a material state change.

Every order submission MUST prove that the authorization snapshot, scope, release, portfolio state, position state and reconciliation state remain valid.

`CHECK → AUTHORIZE → STATE CHANGE → SUBMIT` is invalid when the state change is material and the authorization is not revalidated.

## Article 26 — Manual Control Cannot Grant Authority

Operator controls, manual overrides and kill switches may revoke or reduce trading authority, but may never grant or enlarge it.

A developer MUST NOT implement an operator shortcut that changes final authorization from `false/unknown` to `true` outside the deterministic authority evaluator.

## Article 27 — Emergency and Risk-Reduction Law

The system MUST distinguish:

`NEW_ENTRY | INCREASE | NORMAL_MODIFY | RISK_REDUCTION | EMERGENCY_EXIT | CANCEL_KNOWN_ORDER`

Fail-closed behavior blocks the creation of new risk. Separately certified emergency/risk-reduction paths may operate only under explicit guards and audit requirements.

An unknown position or order state MUST NOT authorize a new financial action.

## Article 28 — Financial Numerical Determinism

Decision-bearing financial quantities MUST use explicit decimal/fixed-point semantics and versioned rounding rules.

The developer MUST NOT rely on unspecified binary floating-point behavior for economic truth.

The implementation MUST explicitly define precision, scale, rounding, tick/lot conversion, fee rounding, currency conversion, overflow behavior and invalid-number handling.

## Article 29 — Certification Scope Integrity

R4 certification is exact-scope evidence, not a transferable label.

The implementation MUST enforce a certification scope hash covering the applicable market profile, universe, data profile, strategy, features, model, parameters, costs, execution model, policies, time window, venue and release.

A certification from a different scope MUST NOT be inherited silently.

## Article 30 — Continuous Certification Validity

Certification is historical evidence plus current eligibility, not permanent permission.

A currently recorded R4 certificate may coexist with:

`LIVE_AUTHORIZED = FALSE`

Whenever current operational, data, execution, risk, capacity, drift, release or certification-scope predicates fail.

## Article 31 — Real-World Economic Success Discipline

The developer shall optimize for durable positive net expectancy rather than superficial metrics such as raw win rate, trade count or a single backtest Sharpe.

Production-critical implementations MUST:

1. model all applicable real costs;
2. validate execution realism and capacity;
3. monitor edge half-life and decay;
4. account for shared alpha-factor concentration;
5. preserve capital and bound drawdown before optimizing nominal return;
6. promote strategy releases incrementally and reversibly;
7. preserve rejected research alternatives and search budgets;
8. prevent learning from unsupported attribution or contaminated data;
9. prefer no-trade to low-quality or uncertainty-dominated opportunities;
10. treat live performance deterioration as a certification/research problem, not as permission to silently loosen gates.

These rules increase the probability of economic success; they do not guarantee future profit.

## Article 32 — Data and Execution Reality Law

No data vendor, API, broker, venue, feed or connector is considered production-capable merely because it technically connects.

Entitlement, latency, quality, point-in-time capability, sequencing, revision behavior, execution behavior and cost must be measured and certified for the exact production scope.

A technically available but uncertified source is not production truth.

## Article 33 — Event / Consumer Liveness Law

Every production event must have:

- a declared consumer;
- an observable consumer health state;
- idempotent business effect semantics;
- retry and dead-letter behavior;
- a terminal classification for unrecoverable failure.

Transport may be at-least-once. Financial state transitions must remain idempotent.

## Article 34 — Policy and Configuration Precedence

Policies, market profiles, account limits, execution constraints and optimization preferences must have deterministic precedence.

A lower layer may tighten a hard restriction, but must never weaken a higher-layer safety ceiling.

No developer may resolve overlapping policy versions by intuition.

## Article 35 — Reconciliation Supremacy in Uncertainty

When internal and external truth disagree, the developer must preserve uncertainty as uncertainty.

The system MUST enter reconciliation or another explicitly certified safe state rather than choosing the prettier value, newest value or most convenient source.

Manual database edits are never a reconciliation mechanism.

## Article 36 — Statistical Honesty

No metric is certification-grade unless its calculation definition is fixed.

The implementation must record the scope and method for:

- sample size;
- effective sample size;
- Sharpe/Sortino/Calmar;
- drawdown;
- calibration metrics;
- tail metrics;
- bootstrap/Monte Carlo assumptions where used.

The developer must never tune to the test set and then describe the same test set as independent validation evidence.

## Article 37 — Learning Must Preserve Economic Causality Boundaries

Learning may only consume governed outcome and attribution evidence.

Large unexplained attribution residuals, corrupted lineage, stale data, ambiguous execution or unresolved reconciliation invalidate production learning for the affected scope.

The system must preserve hypotheses, rejected candidates, search budget, experiment version, selected candidate and reason for selection.

## Article 38 — AI Freshness and Non-Authority

AI outputs are versioned recommendations/research artifacts.

They must carry a context snapshot, model version, policy/prompt version, creation time, expiry time and scope.

An expired AI result cannot be reused as current truth.

AI may never grant authority, enlarge risk, weaken policy, change certification, disable reconciliation or become an undocumented critical dependency.

## Article 39 — Production Explainability Law

Before production acceptance of any decision-bearing change, the developer must be able to answer from recorded evidence:

```text
WHY TRADE?
WHY NO TRADE?
WHAT DATA?
WHAT POLICY?
WHAT VERSION?
WHAT CERTIFICATION SCOPE?
WHAT AUTHORIZATION?
WHAT STATE?
WHAT ORDER?
WHAT EXTERNAL RESULT?
WHAT OUTCOME?
WHAT ATTRIBUTION?
```

Failure to explain a production-critical decision is an acceptance failure.

## Article 40 — Economic Success Is Empirical

The developer is responsible for building a system that maximizes the probability of durable economic success through:

`DATA TRUTH → VALIDATED EDGE → COST REALISM → EXECUTION REALISM → RISK CONTROL → CAPACITY → RECONCILIATION → OUTCOME → ATTRIBUTION → GOVERNED LEARNING`

The developer is NOT permitted to manufacture profitability claims, inflate metrics, remove adverse outcomes, weaken thresholds to obtain a PASS, or treat a successful backtest as a promise of future profit.

## Article 41 — V1.1 Final Oath

Before merging production-critical code, the developer must truthfully state:

> “I implemented V2.2.5 as the source of truth. I did not invent material trading behavior. I did not convert uncertainty into authority. I preserved numerical determinism, scope integrity, reconciliation supremacy and evidence lineage. I tested failure and recovery paths. I can explain the decision, the order, the external outcome and the feedback path from recorded evidence. I know the conditions under which the system is allowed to trade and the conditions under which it must stop.”

If this statement is not true, the change is not ready for acceptance.


---

# V2.0 PRE-CODE AND IMPLEMENTATION ARTICLES — BINDING

**Version:** 2.0  
**Bound master:** 3.0.0  
**Status:** Review candidate; becomes binding on owner acceptance.

## Article 42 — Truth before optimism
Design, code, test, runtime evidence, economic certification and live authority are separate states. Never report a higher state from lower-state evidence.

## Article 43 — No invented trading behavior
If a material behavior or value is silent/unbound, stop the affected implementation and open change control. Do not select a convenient threshold, data source, order type, fallback, clock or recovery rule.

## Article 44 — 900-control ownership
Every question has an owner engine, contract, policy family, planned test and fail action. An applicable orphan is a release blocker.

## Article 45 — 112-engine boundary
All engine calls cross their declared orchestrator. Direct hidden calls, shared mutable decision state and unversioned side channels are forbidden.

## Article 46 — Authority is singular
Only the deterministic authority evaluator may grant new-risk authority. Manual, AI, research and notification components may reduce/revoke but never enlarge authority.

## Article 47 — Authorization lease
Every side effect uses an unexpired, unconsumed, scope/release/state-matching single-use lease. A state change invalidates affected leases.

## Article 48 — External truth and reconciliation
Unknown broker order, fill, position, cash, margin or settlement state is not permission. Retry requires proven idempotency and reconciliation safety.

## Article 49 — Financial arithmetic
Decision-bearing financial values use explicit decimal/fixed point, precision, scale and rounding. NaN, Infinity, overflow and implicit FX conversion are rejected.

## Article 50 — Temporal truth
Historical decisions use only information actually available then, including correct revision/vintage, universe and corporate-action state.

## Article 51 — Strategy humility
Every catalog strategy begins disabled and uncertified. A strategy is code only after its full definition is bound; it becomes live only after scope-exact empirical evidence.

## Article 52 — Statistical honesty
All trials and failed alternatives are registered. Holdout exposure, selection, dependence and stopping decisions are recorded. Hidden test leakage invalidates certification.

## Article 53 — Full economic costs
Gross alpha is not edge. Net lower-bound EV includes all applicable execution, holding, funding, borrow, impact, latency and uncertainty costs.

## Article 54 — Capacity and exit
Allocation cannot exceed certified capacity. Capacity includes stressed liquidation/exit and counterparty transfer constraints.

## Article 55 — Risk outranks return
Tail risk, ruin, drawdown, compliance, integrity, security, reconciliation and kill switches cannot be bypassed by positive EV or P&L pressure.

## Article 56 — AI is not authority
AI output is versioned, expiring, scoped and advisory. Prompt injection or stale context cannot enter an authority path.

## Article 57 — Secure supply chain
Dependencies, artifacts, models, data and configurations carry provenance and signatures where applicable. A compromised scope is revoked and revalidated.

## Article 58 — Recovery is proven
Restart, green dashboards or recovered connectivity do not restore authority. External truth, policy, state, lineage and certification are revalidated.

## Article 59 — Explain every decision
The platform must explain why it traded or refused, which inputs/policies/certification/lease/order/external outcome applied and what changed.

## Article 60 — Evidence is immutable
PASS requires executed tests and immutable, scope-exact evidence. Test skeletons, screenshots, documentation and self-approval are not evidence.

## Article 61 — Independent control
Material creators cannot be sole validators and production approvers. Exceptions are time-bounded, scope-bounded, owned and auto-expiring.

## Article 62 — Change control
Every material change follows STOP → CR → impact → version → test design → approval → implementation → evidence → recertification.

## Article 63 — No profit promise
The objective is durable positive net expectancy under verified costs/capacity and bounded risk. Future profit is never guaranteed.
