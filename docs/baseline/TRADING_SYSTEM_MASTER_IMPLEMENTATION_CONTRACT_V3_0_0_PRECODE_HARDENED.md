# TRADING SYSTEM MASTER IMPLEMENTATION CONTRACT V3.0.0 — PRE-CODE HARDENED DEVELOPER HANDOFF

**Current version:** `3.0.0`  
**Change request:** `CR-V3.0.0-PRECODE-001`  
**Current status:** `REVIEW CANDIDATE / SOFTWARE NOT IMPLEMENTED / LIVE AUTHORITY FALSE`  
**Precedence notice:** Sections 180–199 in the V3.0.0 amendment override conflicting retained V2.x wording. Historical PASS statements do not prove current code, current artifact availability, profitability or live authority.

---

# TRADING SYSTEM — MASTER IMPLEMENTATION CONTRACT V2.2.5 — HARDENED MASTER BASELINE

> **V2.2.5 is the current master baseline. It retains the approved V2.2.x contract surface and appends a normative hardening package that overrides conflicting legacy wording. V2.2.4 remains the historical R1 artifact-materialization baseline. Where this amendment conflicts with retained text, V2.2.5 wins.**

**Important:** This document is a contract-completion artifact, not proof of implementation, profitability, or live trading authorization.

# TRADING SYSTEM — MASTER IMPLEMENTATION CONTRACT V2.2.2 PROFITABILITY-CERTIFIED

**Document status:** MASTER BASELINE — EXECUTABLE IMPLEMENTATION CONTRACT + PROFITABILITY CERTIFICATION + ADVERSARIAL EXAM FRAMEWORK  
**Version:** 2.2.2  
**Supersedes:** `TRADING_SYSTEM_MASTER_IMPLEMENTATION_CONTRACT_V2_1`  
**Scope:** Autonomous Adaptive Real-Market Trading System  
**Primary objective:** Build a real-world trading platform that can ingest real market data through licensed/authorized APIs and feeds, evaluate opportunities across multiple evidence layers, control risk and capital deterministically, execute only authorized actions, reconcile live broker/venue state, measure outcomes, and improve only through governed research and certification.  
**Important boundary:** No document or software can guarantee profit. The engineering objective is durable positive **net expectancy under bounded and explicitly governed risk**, with fail-closed behavior whenever critical information, state, authorization, or reconciliation is uncertain.

---

# 0. MASTER DECISION

This document is the single implementation baseline for the system.

The implementation team must not invent missing business rules during coding. Every material behavior must be traceable to this contract. If coding discovers a case that is not covered, the case becomes a **Change Request** rather than an undocumented implementation decision.

The system is designed around five absolute questions:

1. **What does the system know right now?**
2. **What does the system believe is happening, and how certain is that belief?**
3. **Is there a measurable and historically validated edge after all real costs?**
4. **Is the opportunity safe and feasible for the current account, portfolio, liquidity and execution conditions?**
5. **What happened afterwards, why did it happen, and what may legitimately be learned from it?**

A sixth question applies globally:

> **What could make the current conclusion wrong, unknown, stale, non-observable, non-executable, or unsafe?**

If a critical answer is unknown, the default action is **NO TRADE / SAFE MODE / RECONCILE**, depending on the layer.

---

# 1. SYSTEM MISSION

The platform shall:

- acquire real-time and historical market data from authorized sources;
- preserve raw observations immutably;
- maintain point-in-time temporal truth;
- distinguish observed facts from derived calculations and probabilistic inference;
- build multi-dimensional market state;
- classify market regimes and regime transitions;
- map liquidity, market structure and microstructure;
- detect candidate setups;
- separate alpha from strategy implementation;
- estimate probability and expectancy;
- include commissions, spread, slippage, market impact, funding, financing, borrow and other applicable costs;
- evaluate trade-level, portfolio-level and tail risk;
- allocate capital across competing opportunities;
- generate and manage real order intents;
- maintain OMS/EMS/venue/broker lifecycle state;
- reconcile internal state against external truth;
- manage live positions and thesis invalidation;
- calculate outcome and attribution;
- detect edge, strategy, model, feature and data degradation;
- perform controlled research and validation;
- prevent research and AI from directly changing production;
- support champion/challenger governance;
- operate under explicit security and authorization boundaries;
- recover safely from technical, market-data, broker, venue and state failures;
- preserve complete decision lineage;
- provide operator notifications and constrained mobile control;
- support deterministic historical replay;
- promote production candidates only through objective certification gates.

---

# 2. NON-GOALS / ABSOLUTE PROHIBITIONS

The system shall not:

- guarantee profit;
- assume future information in backtest/replay;
- treat model inference as observed fact;
- treat a candidate setup as an approved trade;
- treat signal approval as capital approval;
- treat capital approval as execution approval;
- bypass risk policy because an AI component is confident;
- bypass reconciliation;
- silently assume missing data is neutral;
- silently replace a failing source with a lower-quality source;
- use unregistered production data;
- modify immutable historical raw data;
- deploy an unvalidated research result directly to production;
- silently replace a production champion with an uncertified challenger;
- allow unknown position state to authorize new orders;
- allow notification failure to create an unauthorized trade;
- permit hidden operational state to become a trading authority.

---

# 3. REAL-MARKET OPERATING PRINCIPLE

The system is not allowed to confuse three different universes:

## 3.1 Observable market

Information directly delivered by a venue, broker, authorized vendor, official publication, or verified source.

## 3.2 Derived market information

Values computed deterministically or statistically from observed information.

Examples:

- VWAP;
- CVD;
- volatility;
- GEX;
- beta;
- liquidity capacity;
- impact estimate.

## 3.3 Inferred / probabilistic market information

Information that cannot be directly observed and must remain an inference.

Examples:

- possible iceberg;
- likely opening/closing options flow;
- probable position reconstruction;
- dealer inventory estimate;
- latent liquidity;
- expected market reaction.

Every production object shall explicitly identify its information class:

`OBSERVED | DERIVED | INFERRED | VENDOR_MODEL | UNKNOWN | UNAVAILABLE`

No inferred value may be persisted or presented as confirmed observed truth.

---

# 4. MARKET COVERAGE CONTRACT

The platform is **multi-asset capable**, but an asset class is not automatically tradable merely because a connector exists.

Each asset class uses a **Market Profile**.

A Market Profile must define:

- asset class;
- instruments;
- venues;
- trading hours;
- market-data sources;
- historical-data sources;
- maximum accessible data tier;
- minimum acceptable data tier;
- point-in-time capability;
- execution venue capability;
- margin model;
- settlement model;
- transaction cost model;
- liquidity model;
- borrow/funding model where relevant;
- corporate-action behavior where relevant;
- regulatory/compliance restrictions;
- allowed strategy families;
- mandatory risk inputs;
- mandatory reconciliation inputs;
- failover sources;
- NO-TRADE conditions;
- certification status.

A market profile has lifecycle:

`UNASSESSED → DATA_VALIDATED → REPLAY_VALIDATED → PAPER_VALIDATED → SHADOW_VALIDATED → MICRO_VALIDATED → CERTIFIED → ACTIVE`

Any profile that fails a critical requirement remains non-tradable.

---

# 5. DATA ACCESS TIERS

Data is classified by capability, not marketing label.

## Tier D0 — Reference / delayed

- end-of-day;
- delayed quotes;
- periodic positioning;
- historical releases.

Not sufficient for low-latency execution decisions.

## Tier D1 — Real-time top-of-book

- best bid;
- best ask;
- last trade;
- top-level quote conditions;
- real-time trades.

Suitable only for strategies explicitly certified for D1.

## Tier D2 — Aggregated depth

- multiple price levels;
- aggregate quantity;
- order counts where provided;
- depth events where available.

## Tier D3 — Event-level / order-level depth

- order additions;
- cancels;
- modifies;
- queue/order identifiers where provided;
- full depth where provided;
- exchange timestamps;
- sequence information.

## Tier D4 — Specialized / premium / proprietary authorized data

Examples may include:

- auction imbalance feeds;
- specialized options analytics;
- specialized borrow/short data;
- premium institutional datasets;
- venue-native execution analytics;
- authorized alternative datasets.

D4 data must never be assumed to be universally obtainable by a retail operator. Entitlement and licensing are part of the Market Profile.

---

# 6. VERIFIED ACCESS REALITY

The architecture shall explicitly recognize the current market-data access reality:

- Nasdaq TotalView provides full depth-of-book for displayed Nasdaq Market Center activity and also disseminates NOII auction information; access is entitlement/licensing dependent. [Official source: https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview]
- NYSE OpenBook Ultra is an event-based depth-of-book feed, and NYSE also provides real-time order-imbalance information. [Official source: https://www.nyse.com/market-data/real-time]
- CME MBO provides order-based futures market data including full depth, queue/order identifiers and individual order sizes where available. [Official source: https://www.cmegroup.com/articles/faqs/market-by-order-mbo.html]
- OPRA disseminates consolidated last-sale and quotation information from participating U.S. listed-options exchanges. [Official source: https://www.opraplan.com/]

These examples establish a **capability taxonomy**, not a promise that every feed is universally available or that one vendor gives a complete view of an entire market.

The system must record whether each dataset is:

`LIVE | DELAYED | HISTORICAL | REVISED | POINT_IN_TIME | AGGREGATED | VENUE_SPECIFIC | CONSOLIDATED | PROPRIETARY | UNAVAILABLE`

---

# 7. MASTER DATA UNIVERSE

## 7.1 Core price/trade data

Mandatory data families where the market provides them:

- tick data;
- trades;
- quote updates;
- OHLC;
- volume;
- turnover;
- session statistics;
- auction prints;
- market state/status messages.

## 7.2 L1 / top-of-book

- bid;
- ask;
- bid size;
- ask size;
- spread;
- quote timestamp;
- quote condition;
- trade condition;
- quote age;
- last trade;
- last trade size.

## 7.3 L2 / MBP

- price-level depth;
- quantity per level;
- number of orders where available;
- depth updates;
- spread depth;
- book snapshots;
- incremental book events.

## 7.4 MBO / L3

Where legally and technically available:

- anonymous order ID;
- priority ID;
- add;
- modify;
- cancel;
- execute;
- replace;
- queue position;
- order lifetime;
- sequence number;
- exchange timestamp;
- receive timestamp;
- processing timestamp;
- book reset/snapshot events;
- sequence-gap diagnostics.

## 7.5 Auction data

Where provided:

- opening imbalance;
- closing imbalance;
- paired quantity;
- imbalance side;
- indicative clearing price;
- auction state;
- auction extension;
- halt/IPO cross data;
- auction reaction.

## 7.6 Futures

- outright contracts;
- contract expiry;
- front/back contracts;
- continuous contracts;
- calendar spreads;
- inter-commodity spreads;
- implied/spread liquidity where provided;
- OI;
- OI change;
- settlement;
- tick size;
- tick value;
- point value;
- contract multiplier;
- margin requirements;
- trading hours;
- first notice date;
- last trade date;
- delivery/settlement methodology;
- roll schedule;
- roll liquidity;
- basis;
- curve shape;
- term structure.

## 7.7 Options

- underlying;
- call/put;
- strike;
- expiration;
- 0DTE flag;
- quote;
- trade;
- bid/ask;
- spread;
- volume;
- OI;
- trade size;
- trade condition;
- quote condition;
- venue/source;
- timestamp;
- implied volatility;
- Greeks;
- skew;
- term structure;
- smile/surface;
- volatility percentile;
- IV/RV relationship;
- sweeps;
- blocks;
- multi-leg/complex order metadata where provided;
- probable opening/closing inference;
- dealer positioning inference;
- GEX/DEX model outputs;
- gamma walls;
- zero-gamma level;
- gamma concentration;
- expiration exposure.

## 7.8 Crypto

For every enabled venue where feasible:

- spot books;
- spot trades;
- futures books;
- perpetual books;
- MBO/MBO-like event data where venue supports it;
- open interest;
- funding rate;
- funding acceleration;
- basis;
- mark price;
- index price;
- liquidation events;
- insurance/funding mechanics where public;
- venue-specific position metrics;
- exchange flows;
- on-chain flows where legally/technically available;
- stablecoin data where relevant;
- ETF flow data where relevant;
- options IV/skew/OI;
- cross-venue spreads;
- cross-venue liquidity;
- cross-venue latency.

No single exchange shall be treated as the complete crypto market.

## 7.9 Equities

Where in scope:

- consolidated NBBO;
- venue BBO;
- venue trades;
- venue depth;
- displayed order data where available;
- auction imbalance;
- opening/closing auction data;
- halts;
- LULD state;
- short-sale restrictions;
- short volume;
- short interest;
- securities lending/borrow data where available;
- borrow rate/availability where available;
- ETF holdings;
- ETF flows;
- index membership;
- index rebalance data;
- corporate actions;
- earnings;
- guidance;
- fundamentals;
- estimates and revisions.

## 7.10 Off-exchange / ATS / OTC

The platform shall support delayed/aggregate off-exchange datasets where available.

It shall **not assume access to a real-time complete dark-pool order book**.

Every such dataset must be labeled:

`DELAYED | AGGREGATED | INCOMPLETE`

when applicable.

## 7.11 Macro

- CPI;
- PPI;
- NFP;
- unemployment;
- GDP;
- retail sales;
- PMI;
- ISM;
- consumer data;
- Treasury yields;
- real yields;
- yield curve;
- Fed expectations;
- central-bank decisions;
- rate probabilities;
- credit spreads;
- DXY / currency basket;
- liquidity conditions;
- financial conditions indexes where available.

Every macro release shall preserve:

`CONSENSUS | ACTUAL | PREVIOUS | REVISION | RELEASE_TIME | FIRST_AVAILABLE_TIME | VINTAGE | SURPRISE`

## 7.12 Fundamental data

If equities are enabled:

- income statement;
- balance sheet;
- cash flow;
- EPS;
- revenue;
- margins;
- debt;
- cash;
- guidance;
- valuation metrics;
- analyst consensus;
- estimate revisions;
- buybacks;
- dividends;
- insider transactions;
- institutional ownership;
- corporate actions;
- filings.

## 7.13 FX

If FX is enabled:

- spot;
- forward;
- swap points;
- carry;
- interest-rate differentials;
- real-rate differentials;
- central-bank divergence;
- volatility surface;
- risk reversals;
- butterflies;
- COT;
- fixing events;
- cross-currency basis;
- macro surprise.

## 7.14 Rates / fixed income

If enabled:

- government yield curves;
- futures;
- OIS;
- SOFR/funding;
- swap curve;
- real yields;
- breakevens;
- Treasury auctions;
- bid-to-cover;
- dealer/indirect/direct allocation where available;
- on/off-the-run;
- repo conditions;
- duration;
- convexity;
- curve spreads.

## 7.15 Positioning / flow

- COT;
- short interest;
- short volume;
- borrow;
- ETF flow;
- futures OI;
- options OI;
- funding;
- liquidation flow;
- venue flow;
- cross-asset positioning;
- institutional/retail aggregate datasets where legally available.

## 7.16 News / event / sentiment

- headline;
- article;
- source;
- publisher;
- first-seen time;
- publication time;
- effective time;
- source reliability;
- asset mapping;
- entity mapping;
- sector mapping;
- novelty;
- duplicate cluster;
- sentiment;
- surprise;
- narrative;
- narrative change;
- confirmation state;
- rumor/official classification;
- correction/retraction;
- market reaction.

---

# 8. DATA TRUTH CONTRACT

Every observation must preserve:

```yaml
event_time:
publish_time:
exchange_time:
receive_time:
availability_time:
processing_time:
effective_time:
source_id:
source_version:
sequence_number:
quality_state:
quality_score:
revision_id:
point_in_time_version:
```

The system must answer:

> **“At exactly this decision timestamp, what information was actually available to the trading system?”**

No backtest or replay may use later revisions unless the experiment explicitly and visibly requests a revised-data research mode that is prohibited for production certification.

---

# 9. DATA QUALITY CONTRACT

Every critical feed is evaluated for:

- missing data;
- stale data;
- duplicates;
- sequence gaps;
- out-of-order messages;
- timestamp anomalies;
- corrupted values;
- abnormal spread;
- impossible prices;
- impossible sizes;
- zero/negative price where invalid;
- negative volume where invalid;
- clock drift;
- source disconnect;
- vendor methodology change;
- revision state;
- coverage gaps;
- book inconsistency.

Outputs:

`VALID | DEGRADED | INVALID | STALE | UNKNOWN`

and:

`quality_score`, `quality_confidence`, `block_flags`, `reason_codes`.

---

# 10. DATA SOURCE REGISTRY

Every production source must have:

- vendor;
- product;
- feed type;
- asset coverage;
- instrument coverage;
- venue coverage;
- entitlement;
- licensing classification;
- real-time/historical availability;
- latency;
- retention;
- revision behavior;
- expected sequencing;
- outage policy;
- cost;
- usage limit;
- rate limit;
- API key/credential identity;
- quality score;
- failover source;
- owner;
- certification state.

No unregistered source may feed production decisions.

---

# 11. DATA FAILOVER

For critical data:

`PRIMARY → SECONDARY → VALIDATED FALLBACK → NO TRADE`

Failover must never silently lower the data quality requirement.

Every source switch must produce:

- source-change event;
- reason code;
- quality delta;
- latency delta;
- coverage delta;
- decision impact;
- audit record.

---

# 12. INSTRUMENT / CONTRACT MASTER

Every instrument must have:

- canonical ID;
- vendor symbol(s);
- venue symbol;
- asset class;
- currency;
- tick size;
- tick value;
- multiplier;
- lot size;
- trading hours;
- timezone;
- expiration;
- settlement;
- contract lineage;
- continuous-contract mapping;
- corporate-action mapping;
- margin metadata;
- fee metadata;
- borrow/funding metadata where applicable;
- active/inactive state.

RAW CONTRACT ≠ CONTINUOUS CONTRACT.

---

# 13. UNIVERSE / MARKET COVERAGE ENGINE

The system must decide which instruments are eligible for analysis and which are eligible for trading.

Required states:

`DISCOVERED → VALIDATED → COVERED → RESEARCHABLE → TRADEABLE`

An instrument may be visible but non-tradeable because of:

- insufficient data;
- insufficient liquidity;
- missing execution route;
- margin restriction;
- compliance restriction;
- certification failure;
- stale instrument master;
- corporate action uncertainty;
- venue outage.

---

# 14. FEATURE FABRIC

Feature groups:

### Price

Returns, range, ATR, realized volatility, gap, VWAP, AVWAP, HOD/LOD, session statistics.

### Fractal

Swing hierarchy, fractal highs/lows, nested structure, compression, expansion, multi-timeframe alignment.

### Structure

HH/HL/LH/LL, break of structure, change of character, trend, range, compression, expansion.

### Volume/Profile

POC, VAH, VAL, HVN, LVN, developing POC, migration, session profiles, composite profiles.

### Order flow

Delta, CVD, bid/ask volume, aggressor, trade velocity, trade clusters, imbalance, stacked imbalance, absorption, exhaustion, divergence.

### Microstructure

Queue arrival, cancel, modify, replenish, pulling, adding, spread depth, order lifetime, queue imbalance, execution intensity.

### Liquidity

Resting liquidity, persistence, cancellation rate, executed volume, stop clusters, liquidation clusters, liquidity quality.

### Volatility

RV, IV, IVR, IV percentile, VIX-like measures, skew, term structure, expected move, IV/RV spread.

### Cross-asset

Lead/lag, beta, relative strength, correlation, correlation breakdown, regime-conditioned correlation.

### Positioning

OI, COT, short interest, funding, borrow, ETF flows, positioning percentiles.

---

# 15. MARKET STATE

Market State answers:

- What is happening?
- Where is price relative to structure?
- What is volatility doing?
- What is liquidity doing?
- What is order flow doing?
- What is positioning doing?
- What is derivatives positioning doing?
- What is macro doing?
- What is event risk?
- What are cross-asset relationships doing?
- What is observable versus inferred?
- What is uncertain?

State and regime are distinct.

---

# 16. REGIME

Separate states:

- structural;
- volatility;
- gamma;
- liquidity;
- microstructure;
- event;
- correlation;
- positioning;
- macro;
- composite.

Regime transition states:

`STABLE → TRANSITION → NEW_REGIME`

Normal strategy expectancy cannot automatically be assumed during transition.

---

# 17. CONTEXT / EXPECTATION ENGINE

The system must model:

- what the market is doing;
- why it may be doing it;
- what participants may be expecting;
- what would confirm the thesis;
- what would invalidate it;
- what would surprise the market;
- what the market has already priced;
- whether the opportunity exists because information is new or because price is merely noisy.

---

# 18. LIQUIDITY MAP

Map:

- above price liquidity;
- below price liquidity;
- value;
- stops;
- liquidation clusters;
- resting liquidity;
- gamma zones;
- auction zones;
- high-volume nodes;
- low-volume nodes;
- expected exit liquidity;
- emergency liquidation capacity.

The map is descriptive until setup validation and risk admission.

---

# 19. SETUP ENGINE

A setup is a candidate, not a trade.

Required setup information:

- setup type;
- direction;
- trigger;
- context;
- evidence;
- invalidation;
- expected path;
- expected duration;
- liquidity condition;
- regime compatibility;
- historical similarity;
- execution feasibility.

---

# 20. ALPHA ENGINE

Alpha and strategy are separate.

Alpha asks:

> **Is there a measurable predictive advantage in this condition?**

Strategy asks:

> **How do we express that advantage in a trade?**

Alpha metadata:

- alpha definition;
- condition;
- expected direction;
- historical expectancy;
- probability;
- stability;
- half-life;
- capacity;
- dependency;
- regime sensitivity;
- decay;
- confidence.

---

# 21. STRATEGY RESEARCH UNIVERSE

Strategy families are research candidates. Presence in this registry does not imply production approval.

## Structure / Trend

- Trend Following;
- Momentum Continuation;
- Breakout;
- Breakout Retest;
- Range Expansion;
- Impulse Continuation.

## Liquidity / Order Flow

- Liquidity Sweep Reversal;
- Absorption Reversal;
- Exhaustion Reversal;
- Liquidity Exhaustion;
- Queue Imbalance;
- Order-flow Divergence;
- Replenishment/Fade;
- Auction Imbalance;
- Stop/Liquidation Cascade.

## Mean Reversion / Value

- VWAP Mean Reversion;
- Anchored VWAP Reversion;
- Value Area Reversion;
- Profile Migration Reversion;
- Gamma Reversion;
- Volatility Mean Reversion;
- Statistical Spread Mean Reversion.

## Volatility

- Volatility Compression → Expansion;
- Realized/Implied Divergence;
- Volatility Breakout;
- Expected-Move Failure;
- Volatility Term-Structure Relative Value.

## Derivatives

- Options Flow Follow-through;
- Options Flow Divergence;
- Gamma Breakout;
- Gamma Reversion;
- Skew Relative Value;
- Volatility Surface Relative Value;
- Calendar Spread;
- Vertical Spread Relative Value;
- Spot/Futures Basis;
- Perpetual Funding;
- Futures Curve Carry;
- OI + Price;
- Liquidation Cascade.

## Statistical / Relative Value

- Pairs;
- Cointegration;
- Residual Mean Reversion;
- Cross-sectional Relative Value;
- Relative Strength;
- Beta-neutral spread;
- Sector-neutral spread;
- Index-vs-components;
- ETF-vs-underlying;
- Dispersion;
- Cross-venue relative value.

## Event-driven

- Macro Surprise;
- CPI/NFP/FOMC response;
- Earnings Surprise;
- Guidance Surprise;
- OPEX/Expiry;
- Rebalance;
- Opening Auction;
- Closing Auction;
- Event Drift;
- Post-event Mean Reversion.

## Cross-asset

- Cross-Asset Divergence;
- Lead-Lag;
- Relative Value;
- Regime-conditioned correlation;
- Yield-equity relationship;
- DXY-equity/commodity relationships;
- BTC/TradFi relationships.

## Time / Seasonality

- Session Conditional Expectancy;
- Time-of-Day Momentum;
- Time-of-Day Mean Reversion;
- Day-of-Week Effects;
- Month-End;
- Quarter-End;
- Holiday;
- Expiration Seasonality.

Each candidate strategy must be classified by its underlying alpha factors so correlated strategies cannot independently consume unlimited risk.

---

# 22. SETUP QUALITY

Every candidate gets:

- completeness score;
- historical similarity;
- regime compatibility;
- liquidity quality;
- execution feasibility;
- alpha quality;
- probability quality;
- data quality;
- conflict level.

Low-quality or incomplete candidates remain ineligible.

---

# 23. CONFLICT ENGINE

Conflict is not a simple vote count.

The engine evaluates:

- evidence independence;
- correlation between evidence sources;
- evidence quality;
- reliability;
- regime dependency;
- source freshness;
- model dependence.

Example:

`STRUCTURE BULLISH + CVD BEARISH + OPTIONS BULLISH + OI BEARISH + MACRO NEUTRAL`

may produce `HIGH_CONFLICT → WAIT`, depending on calibrated evidence quality.

---

# 24. PROBABILITY / EXPECTANCY / EDGE

These must remain separate:

`CONFIDENCE ≠ PROBABILITY ≠ EXPECTED VALUE`

Gross expectancy:

`P(win) × AvgWin − P(loss) × AvgLoss`

Net expectancy must subtract all applicable costs:

- commission;
- spread;
- slippage;
- market impact;
- funding;
- financing;
- borrow;
- exchange fees;
- roll cost;
- other execution/holding costs.

Net expectancy is the production gating measure.

Probability must be calibrated and monitored by regime where sufficient data exists.

---

# 25. EDGE QUALITY

Track:

- edge strength;
- edge stability;
- edge decay;
- edge half-life;
- edge capacity;
- edge dependency;
- edge concentration;
- edge uncertainty.

An edge is not considered execution-safe merely because its expected return is high.

---

# 26. NO-TRADE ENGINE

Hard veto reasons include:

- invalid data;
- stale data;
- insufficient data quality;
- sequence gap;
- critical clock drift;
- unavailable point-in-time truth;
- extreme spread;
- insufficient liquidity;
- negative net expectancy;
- uncalibrated probability;
- unacceptable conflict;
- unacceptable tail risk;
- unacceptable ruin risk;
- strategy ineligible;
- strategy degraded;
- regime transition;
- event risk;
- portfolio limit breach;
- capital unavailable;
- venue unavailable;
- execution infeasible;
- reconciliation required;
- compliance restriction;
- system health degraded;
- unknown position state.

Canonical reason-code examples:

`NO_TRADE_DATA_INVALID`, `NO_TRADE_DATA_STALE`, `NO_TRADE_SEQUENCE_GAP`, `NO_TRADE_NEGATIVE_EV`, `NO_TRADE_LIQUIDITY`, `NO_TRADE_TAIL_RISK`, `NO_TRADE_PORTFOLIO_LIMIT`, `NO_TRADE_EXECUTION_INFEASIBLE`, `NO_TRADE_RECONCILIATION_REQUIRED`, `NO_TRADE_COMPLIANCE`, `NO_TRADE_SYSTEM_HEALTH`.

---

# 27. TRADE THESIS

Every trade candidate must define:

- direction;
- entry reason;
- expected path;
- catalyst;
- confirmation;
- invalidation;
- target(s);
- expected holding period;
- risk;
- liquidity condition;
- execution mode;
- edge half-life;
- expected exit condition.

The system must know what would prove the thesis wrong.

---

# 28. RISK

Risk shall be deterministic.

Risk sizing considers:

`ACCOUNT → RISK BUDGET → STOP DISTANCE → CONTRACT VALUE → VOLATILITY → CORRELATION → PORTFOLIO ADJUSTMENT → FINAL SIZE`

Risk cannot be increased by AI.

---

# 29. RISK BUDGET HIERARCHY

`TOTAL CAPITAL → SURVIVAL CAPITAL → MAX PORTFOLIO LOSS → MAX DAILY LOSS → MAX WEEKLY LOSS → STRATEGY RISK → ASSET RISK → FACTOR RISK → TRADE RISK`

No lower layer may exceed an upper-layer ceiling.

---

# 30. DRAWDOWN RESPONSE

States:

`NORMAL → CAUTION → DEFENSIVE → CRITICAL → HALT`

Each state must have deterministic risk multipliers and trade-admission rules.

---

# 31. LOSS / RUIN / TAIL RISK

Loss Distribution Engine tracks:

- mean;
- median;
- variance;
- skew;
- kurtosis;
- tail percentiles;
- consecutive losses;
- loss clustering;
- win clustering;
- extreme loss frequency.

Risk of Ruin evaluates critical drawdown and capital impairment probability.

Tail Risk evaluates:

- VaR;
- Expected Shortfall;
- liquidity-adjusted loss;
- gap risk;
- jump risk;
- forced liquidation;
- volatility shock;
- correlation shock;
- spread expansion;
- execution failure;
- data failure.

Positive expectancy never overrides unacceptable tail or ruin risk.

---

# 32. STRESS SCENARIO ENGINE

Required baseline scenarios:

- volatility shock;
- liquidity shock;
- correlation shock;
- gap shock;
- rate shock;
- DXY shock;
- BTC cascade;
- options gamma shock;
- spread expansion;
- order-book collapse;
- market-data outage;
- broker outage;
- exchange outage;
- execution failure;
- clock failure;
- reconciliation failure.

Every scenario produces:

- P&L impact;
- margin impact;
- liquidation impact;
- liquidity impact;
- recovery time;
- portfolio heat.

---

# 33. PORTFOLIO EXPOSURE

Portfolio exposure must aggregate:

- market risk;
- beta;
- factor exposure;
- currency exposure;
- delta;
- gamma;
- vega;
- theta;
- vanna/charm where relevant;
- duration/convexity where relevant;
- liquidity exposure;
- event exposure;
- strategy exposure;
- alpha-factor exposure;
- venue exposure;
- model exposure.

A new trade must be evaluated as an addition to the existing portfolio, not as an isolated trade.

---

# 34. CAPITAL ALLOCATION

Capital allocation considers:

- net EV;
- calibrated probability;
- risk;
- drawdown state;
- portfolio exposure;
- correlation;
- liquidity capacity;
- market impact;
- execution quality;
- strategy health;
- strategy decay;
- tail risk;
- capacity;
- alpha dependency.

Highest EV does not automatically mean highest capital allocation.

---

# 35. CAPITAL COMPETITION

Simultaneous opportunities compete for scarce capital.

The system must compare:

- net edge;
- marginal risk;
- marginal portfolio contribution;
- alpha redundancy;
- liquidity consumption;
- capital efficiency;
- capacity;
- execution feasibility.

---

# 36. CAPACITY

Capacity must be calculated against:

- available liquidity;
- exit liquidity;
- market impact;
- expected slippage;
- spread;
- execution speed;
- stress liquidity;
- emergency liquidation capacity;
- venue limits.

Strategy EV is not assumed to remain constant as capital size increases.

---

# 37. OMS — ORDER MANAGEMENT

OMS is a first-class domain.

It owns:

- order intent;
- client order ID;
- venue order ID;
- parent/child relationship;
- order type;
- order quantity;
- remaining quantity;
- filled quantity;
- average fill price;
- status;
- cancel request;
- replace request;
- acknowledgement;
- rejection;
- expiry;
- timeout;
- duplicate detection;
- venue mapping;
- order lifecycle reconciliation.

OMS does not independently create authority to trade. It consumes authorized order intent.

---

# 38. EMS / EXECUTION ENGINE

Execution controls:

- market;
- limit;
- passive limit;
- aggressive limit;
- stop where allowed;
- cancel/replace;
- slicing;
- participation constraints;
- timing;
- urgency;
- fill probability;
- spread;
- impact;
- latency;
- edge half-life.

Execution must answer:

> Is the edge still alive while this order is being executed?

---

# 39. VENUE / BROKER MANAGEMENT

Each venue adapter must expose:

- connectivity;
- authentication;
- supported order types;
- tick/lot rules;
- trading status;
- venue timestamps;
- rate limits;
- margin rules;
- fee schedule;
- order acknowledgements;
- execution reports;
- maintenance status;
- position semantics;
- balance semantics;
- capability version.

Venue quality is measurable through:

- latency;
- rejection rate;
- fill rate;
- slippage;
- outage frequency;
- reconciliation reliability.

---

# 40. BROKER / ACCOUNT MASTER

Account master must track:

- account ID;
- broker;
- venue(s);
- base currency;
- cash;
- buying power;
- margin;
- leverage;
- reserved capital;
- realized P&L;
- unrealized P&L;
- fees;
- funding;
- borrow;
- settlement;
- account status;
- trading permission state.

---

# 41. CASH / TREASURY

Treasury layer must track:

- cash;
- reserved cash;
- available cash;
- settlement cash;
- funding requirements;
- financing;
- collateral;
- currency balances;
- minimum cash buffer;
- margin buffer;
- concentration.

---

# 42. POSITION MANAGER

Position lifecycle:

`FLAT → ENTRY_PENDING → PARTIAL → OPEN → MANAGING → EXIT_PENDING → CLOSED`

Additional states:

`RECONCILIATION_REQUIRED | HALTED | UNKNOWN`

Thesis invalidation must be capable of forcing an exit decision.

---

# 43. TRADE STATE MACHINE

Canonical lifecycle:

`WATCHING → CANDIDATE → VALIDATING → APPROVED → ENTRY_PENDING → PARTIALLY_FILLED → OPEN → MANAGING → EXIT_PENDING → CLOSED → ANALYZING`

Terminal/exception states:

`REJECTED | CANCELLED | HALTED | RECONCILIATION_REQUIRED`

Every state transition requires:

- triggering event;
- guard;
- authorized actor/service;
- timestamp;
- state version;
- audit record;
- side effect;
- next valid states.

---

# 44. RECONCILIATION

Reconciliation compares internal truth to external truth for:

- orders;
- fills;
- positions;
- balances;
- cash;
- margin;
- fees;
- funding;
- settlements.

Example:

`BOT: +2 | BROKER: +1 → NEW ORDERS BLOCKED → RECONCILIATION_REQUIRED`

No new order is allowed until the discrepancy is resolved or an explicitly certified safe fallback exists.

---

# 45. COMPLIANCE / SURVEILLANCE

A first-class domain must evaluate, where applicable:

- instrument restrictions;
- account restrictions;
- venue rules;
- order-size limits;
- short-sale restrictions;
- borrow availability;
- restricted securities;
- market status;
- duplicate orders;
- erroneous orders;
- abnormal order behavior;
- unauthorized automation;
- audit requirements;
- production policy violations.

Compliance failure is a hard admission block.

---

# 46. OUTCOME

Every closed trade must produce:

- realized P&L;
- R;
- MFE;
- MAE;
- duration;
- entry slippage;
- exit slippage;
- total cost;
- execution quality;
- thesis outcome;
- strategy outcome;
- data quality;
- market regime;
- liquidity regime.

---

# 47. ATTRIBUTION

P&L attribution must distinguish:

- alpha;
- selection;
- sizing;
- timing;
- execution;
- cost;
- market movement;
- regime;
- liquidity;
- feature contribution;
- feature failure.

Negative attribution is mandatory.

---

# 48. PERFORMANCE

Performance must include:

- net expectancy;
- profit factor;
- average R;
- average winner;
- average loser;
- max drawdown;
- Sharpe;
- Sortino;
- Calmar;
- recovery factor;
- MAE/MFE;
- consecutive losses;
- turnover;
- time in market;
- slippage;
- commission;
- tail risk;
- capacity;
- risk-adjusted return;
- tail-adjusted return.

All performance must be segmented by:

- asset;
- strategy;
- regime;
- session;
- venue;
- market condition;
- time period.

---

# 49. STRATEGY DECAY / DRIFT

Strategy states:

`NORMAL → WATCH → DEGRADING → DEFENSIVE → PROBATION → DISABLED → RESEARCH`

Drift must include:

- input distribution drift;
- feature drift;
- missingness drift;
- feature importance drift;
- calibration drift;
- regime drift;
- vendor methodology change;
- data quality drift;
- execution drift;
- latency drift;
- cost drift.

---

# 50. MODEL RISK

Every model must have:

- purpose;
- inputs;
- assumptions;
- limitations;
- failure modes;
- training data;
- validation data;
- test data;
- version;
- evaluation;
- calibration;
- drift monitoring;
- decommission criteria;
- rollback version.

---

# 51. FEATURE LIFECYCLE

Features move through:

`PROPOSED → RESEARCHED → VALIDATED → REGISTERED → ACTIVE → MONITORED → DEGRADED → DEPRECATED → RETIRED`

Each feature must have:

- definition;
- formula;
- data sources;
- transformations;
- lineage;
- leakage risk;
- cost;
- latency;
- availability;
- stability;
- predictive evidence.

---

# 52. MODEL TRAINING / EVALUATION

Research runtime must support:

- dataset construction;
- point-in-time joins;
- feature computation;
- training;
- hyperparameter search;
- validation;
- test;
- calibration;
- model packaging;
- reproducibility;
- artifact registry;
- model-risk registration.

No trained artifact becomes production-capable without validation/certification.

---

# 53. RESEARCH TRIAL REGISTRY

Every experiment stores:

- research ID;
- hypothesis;
- dataset version;
- time period;
- features;
- parameters;
- strategies tested;
- number of trials;
- selection rule;
- outputs;
- rejected candidates;
- final selection reason.

The registry exists to control multiple-testing and selection bias.

---

# 54. BACKTEST

Backtest modes:

- in-sample;
- out-of-sample;
- walk-forward;
- purged validation;
- embargo;
- CPCV where appropriate;
- Monte Carlo;
- stress;
- transaction-cost realism;
- market-impact realism;
- execution realism.

No future information.

---

# 55. MARKET REPLAY

Replay must reproduce historical runtime truth using:

- historical availability;
- historical latency;
- historical source state;
- historical revisions as known then;
- historical risk rules;
- historical capital state;
- historical execution rules;
- historical slippage/cost assumptions;
- historical market path.

For fixed inputs and fixed version, replay must be deterministic within explicitly defined numerical tolerances.

---

# 56. OVERFITTING / STATISTICAL VALIDATION

Required evaluation:

- data snooping;
- multiple testing;
- selection bias;
- survivorship bias;
- look-ahead bias;
- parameter instability;
- feature redundancy;
- regime robustness;
- PBO;
- DSR;
- calibration;
- bootstrap;
- Monte Carlo;
- confidence intervals;
- sample-size adequacy;
- stationarity;
- autocorrelation;
- heteroskedasticity;
- dependence assumptions.

A high backtest Sharpe alone is never a certification condition.

---

# 57. LIVE SHADOW

Shadow:

`LIVE MARKET → REAL-TIME SIGNAL → REAL-TIME DECISION → VIRTUAL EXECUTION`

Measures:

- signal latency;
- decision latency;
- virtual fill realism;
- expected vs realized slippage;
- expected vs realized probability;
- execution feasibility;
- risk behavior;
- reconciliation behavior;
- system reliability.

---

# 58. PAPER

Paper validates the operational system without capital exposure:

- order lifecycle;
- latency;
- fills;
- slippage;
- costs;
- reconciliation;
- risk;
- compliance;
- reliability.

P&L is not the only metric.

---

# 59. MICRO / PROBATION

Promotion requires objective gates.

At every stage:

`EXPECTED vs REALIZED`

must be compared for:

- probability;
- EV;
- fill probability;
- slippage;
- impact;
- risk;
- drawdown;
- execution;
- reconciliation;
- system health.

---

# 60. LEARNING / FEEDBACK

Learning lifecycle:

`OBSERVE → DETECT → HYPOTHESIZE → RESEARCH → VALIDATE → CERTIFY → PAPER → SHADOW → MICRO → PROBATION → DEPLOY`

Feedback may propose changes but may not silently modify production.

Feedback categories:

`SUCCESS | FAILURE | PARTIAL | THESIS_INVALIDATED | EXECUTION_FAILURE | DATA_FAILURE | RISK_FAILURE | RECONCILIATION_FAILURE | SYSTEM_FAILURE`

---

# 61. AI GOVERNANCE

AI may:

- interpret;
- research;
- summarize;
- rank;
- hypothesize;
- compare historical cases;
- investigate anomalies;
- recommend.

AI may never directly:

- increase risk limits;
- increase capital ceilings;
- disable kill switches;
- bypass reconciliation;
- alter security roles;
- modify production code;
- silently deploy a model;
- certify itself.

AI authority levels:

`L0 ANALYSIS → L1 SIGNAL SUGGESTION → L2 VALIDATED RECOMMENDATION → L3 EXECUTION RECOMMENDATION → L4 LIMITED AUTOMATION → L5 CONTROLLED AUTONOMY`

Hard prohibitions remain at every level.

---

# 62. DECISION COUNCIL

Council must evaluate:

- independence;
- correlation;
- confidence;
- data quality;
- historical validity;
- regime compatibility;
- model dependency.

It must not perform simple majority voting.

---

# 63. EXECUTIVE DECISION

Every final decision carries:

- decision ID;
- instrument;
- direction;
- probability;
- net EV;
- confidence;
- data quality;
- regime;
- strategy;
- risk budget;
- capital allocation;
- expected holding period;
- invalidation;
- execution mode;
- versions of all critical dependencies.

Final decisions:

`LONG | SHORT | WAIT | NO_TRADE`

---

# 64. IMMUTABLE DECISION LEDGER

Every production decision must be reconstructable years later.

The ledger stores or references:

- market snapshot;
- data versions;
- feature versions;
- model versions;
- strategy versions;
- parameter versions;
- policy versions;
- risk decision;
- capital decision;
- execution decision;
- decision reasoning;
- source lineage;
- consumer path;
- outcome link.

---

# 65. REQUIRED DECISION CHAIN

The following is a hard invariant:

`ENGINE → CALLER → ORCHESTRATOR → DECISION → SQL WRITE → DECISION CONSUMER → OUTCOME → ATTRIBUTION → FEEDBACK → LEARNING`

An engine being implemented is **not** equivalent to functionality being complete.

A feature is complete only when its full lifecycle is connected and tested.

---

# 66. EVENT CONTRACT

Every event:

```yaml
event_id: UUID
event_type: string
event_version: semver
event_time: UTC timestamp
source: string
producer: string
correlation_id: UUID
causation_id: UUID|null
instrument_id: UUID|null
schema_version: semver
payload: object
```

Transport:

- at-least-once;
- idempotent consumers;
- no assumption of transport-level exactly-once.

Each event type must additionally define:

- canonical subject;
- stream;
- consumer group;
- ack policy;
- retry policy;
- maximum delivery;
- dead-letter policy;
- retention;
- ordering requirement;
- payload schema.

---

# 67. DOMAIN CONTRACT SCHEMA RULE

Every production domain object must define:

- ID;
- schema version;
- created time;
- effective time;
- source version;
- code version;
- status;
- confidence/quality;
- lineage ID;
- data version where applicable.

Decision-bearing objects also reference:

- decision version;
- model version;
- policy version;
- parameter version;
- execution version.

---

# 68. DATABASE CONTRACT

PostgreSQL namespaces:

`core, registry, market, features, state, regime, context, liquidity, alpha, strategy, decision, risk, portfolio, capital, execution, position, reconciliation, outcome, attribution, performance, research, validation, certification, governance, audit, observability, ai, memory, notifications, operations`

Additional implementation tables/domains may exist for:

- accounts;
- venues;
- oms;
- compliance;
- treasury;
- market_profiles;
- dataset_manifests;
- source_entitlements;
- reason_codes.

Every table requires:

- PK;
- FK where applicable;
- unique constraints;
- check constraints;
- created_at;
- updated_at when mutable;
- version references;
- indexes;
- retention policy;
- audit policy;
- immutability classification.

Alembic is schema authority.

---

# 69. REASON CODE REGISTRY

Canonical reason code namespaces:

`DATA_*`
`MARKET_*`
`REGIME_*`
`STRATEGY_*`
`EDGE_*`
`RISK_*`
`CAPITAL_*`
`EXECUTION_*`
`OMS_*`
`VENUE_*`
`RECON_*`
`COMPLIANCE_*`
`POSITION_*`
`SYSTEM_*`
`SECURITY_*`
`RESEARCH_*`
`VALIDATION_*`
`CERTIFICATION_*`
`AI_*`

Free-text reasons may supplement but cannot replace canonical codes.

---

# 70. STATE MACHINES

State machines requiring explicit transition contracts:

1. runtime;
2. market profile;
3. data source;
4. dataset;
5. strategy;
6. model;
7. feature;
8. trade;
9. order;
10. position;
11. reconciliation;
12. incident;
13. recovery;
14. certification;
15. learning;
16. champion/challenger.

Every state machine must define legal transitions, guards, events, side effects, recovery states and terminal states.

---

# 71. SECURITY / IAM

Required roles at minimum:

- read-only;
- research;
- strategy-admin;
- risk-admin;
- execution-admin;
- system-admin;
- release-admin;
- auditor.

AI is never system-admin.

Secrets require:

- secure storage;
- rotation;
- least privilege;
- revocation;
- audit;
- environment separation.

High-impact mobile actions require stronger authorization than read-only queries.

---

# 72. OBSERVABILITY

Every critical engine exposes:

- health;
- latency;
- throughput;
- error rate;
- stale rate;
- output rate;
- dependency state;
- input quality;
- confidence where relevant.

Critical alerts include:

- feed loss;
- stale data;
- clock drift;
- sequence gap;
- broker disconnect;
- venue disconnect;
- position mismatch;
- order mismatch;
- risk breach;
- capital breach;
- abnormal execution;
- system health degradation;
- backup failure;
- security failure.

---

# 73. FAILURE / RECOVERY

Runtime states:

`BOOT → SELF_CHECK → READY → MONITORING → TRADING_ENABLED`

Failure:

`DEGRADED → SAFE_MODE → HALTED`

Recovery:

`RECOVERING → RECONCILING → VALIDATED → READY`

Execution faults may require:

`ISOLATED → SAFE → RECONCILING → VALIDATED → RESUME`

No recovery state may silently restore trading authority before required validations complete.

---

# 74. BACKUP / DISASTER RECOVERY

The platform shall define and test:

- backup frequency;
- retention;
- off-site backup;
- database recovery;
- object-store recovery;
- configuration recovery;
- secret recovery procedures;
- integrity validation;
- restore tests;
- recovery-point objective;
- recovery-time objective.

Recovery tests are part of production certification.

---

# 75. COST / RESOURCE GOVERNOR

Spend must be attributable to:

- vendor;
- dataset;
- feed;
- API request;
- AI model;
- tokens;
- storage;
- environment.

Limits:

- daily;
- monthly;
- per strategy;
- per research job;
- per model;
- per source.

Budget failure may throttle or safe-fallback but cannot silently authorize unsafe behavior.

---

# 76. GAME MODE

Game Mode may throttle:

- research;
- non-critical AI;
- background analysis;
- batch work.

It must preserve:

- market feeds;
- risk;
- OMS;
- execution;
- positions;
- reconciliation;
- watchdog;
- critical notifications.

Trading-path performance must be acceptance-tested with and without game workload.

---

# 77. MOBILE CONTROL

Mobile functions must be capability-scoped.

Read-only actions may include:

- system status;
- position status;
- decision status;
- risk status;
- current exposure;
- notifications.

High-impact control functions must require stronger authorization and confirmation.

No mobile interface may bypass the same governance and risk policy used by the main runtime.

---

# 78. CANONICAL ARCHITECTURE TOPOLOGY

```text
WINDOWS HOST
  │
  ├── SYSTEM SUPERVISOR
  │    ├── BOOTSTRAP
  │    ├── WATCHDOG
  │    ├── SHUTDOWN
  │    ├── RESOURCE MANAGER
  │    └── RECOVERY
  │
  ├── TRADING CORE
  │    ├── DATA FOUNDATION
  │    ├── MARKET INTELLIGENCE
  │    ├── ALPHA / STRATEGY
  │    ├── DECISION
  │    ├── RISK / PORTFOLIO
  │    ├── CAPITAL
  │    ├── OMS / EMS
  │    ├── POSITION
  │    ├── RECONCILIATION
  │    └── OUTCOME / PERFORMANCE
  │
  ├── RESEARCH RUNTIME
  │    ├── REPLAY
  │    ├── BACKTEST
  │    ├── MODEL TRAINING
  │    ├── VALIDATION
  │    └── CERTIFICATION
  │
  ├── CONTROL PLANE
  │    ├── GOVERNANCE
  │    ├── SECURITY
  │    ├── REGISTRIES
  │    ├── RELEASES
  │    ├── CHAMPION / CHALLENGER
  │    └── COMPLIANCE
  │
  └── INFRASTRUCTURE
       ├── POSTGRESQL
       ├── NATS JETSTREAM
       ├── PARQUET / OBJECT STORE
       ├── PROMETHEUS / GRAFANA
       └── TELEGRAM / MOBILE GATEWAY
```

---

# 79. IMPLEMENTATION DAG

The implementation order is locked conceptually as follows:

`00 CONTRACT FREEZE`

`01 REPOSITORY / RUNTIME`

`02 POSTGRES / ALEMBIC`

`03 EVENT CONTRACTS / NATS`

`04 SOURCE REGISTRY / ENTITLEMENTS`

`05 MARKET PROFILES / INSTRUMENT MASTER`

`06 RAW DATA / CURATED DATA / FEATURE DATA LAKE`

`07 TEMPORAL TRUTH / CLOCK`

`08 DATA QUALITY / FAILOVER`

`09 FEATURE FABRIC`

`10 MARKET STATE`

`11 REGIME / CONTEXT`

`12 LIQUIDITY / MICROSTRUCTURE / ORDER FLOW`

`13 DERIVATIVES / OPTIONS / FUTURES / CRYPTO`

`14 MACRO / NEWS / POSITIONING / CROSS-ASSET`

`15 SETUP / CONFLICT / ALPHA`

`16 STRATEGY LIBRARY / ELIGIBILITY`

`17 EXPECTANCY / COST / IMPACT / PROBABILITY / EDGE`

`18 NO-TRADE / SIGNAL / THESIS`

`19 RISK / TAIL / RUIN / STRESS`

`20 PORTFOLIO / EXPOSURE / CAPACITY`

`21 CAPITAL ALLOCATION / COMPETITION`

`22 COMPLIANCE`

`23 OMS / VENUE / BROKER / ACCOUNT`

`24 EXECUTION / POSITION`

`25 RECONCILIATION / TREASURY / SETTLEMENT`

`26 OUTCOME / ATTRIBUTION / PERFORMANCE`

`27 DRIFT / MODEL RISK`

`28 RESEARCH / REPLAY / BACKTEST`

`29 MODEL TRAINING / FEATURE LIFECYCLE`

`30 OVERFITTING / STATISTICAL VALIDATION`

`31 CERTIFICATION / SHADOW / PAPER`

`32 MICRO / PROBATION`

`33 LEARNING / FEEDBACK / CHAMPION-CHALLENGER`

`34 AI GOVERNANCE`

`35 OBSERVABILITY / INCIDENT / BACKUP`

`36 SECURITY / RELEASE`

`37 FULL END-TO-END REPLAY`

`38 PRODUCTION GATE`

---

# 80. PRODUCTION CERTIFICATION GATES

No direct production deployment.

Required chain:

`ARCHITECTURE PASS`
→ `CONTRACT PASS`
→ `DATA PASS`
→ `TEMPORAL TRUTH PASS`
→ `REPLAY PASS`
→ `BACKTEST PASS`
→ `OVERFITTING PASS`
→ `STATISTICAL VALIDATION PASS`
→ `MODEL RISK PASS`
→ `PAPER PASS`
→ `SHADOW PASS`
→ `COMPLIANCE PASS`
→ `MICRO PASS`
→ `PROBATION PASS`
→ `PRODUCTION`

A single failed hard gate blocks promotion.

---

# 81. NUMERICAL ACCEPTANCE PRINCIPLE

Generic “tests green” is not sufficient.

Every critical engine must eventually have measurable thresholds for:

- maximum latency;
- minimum data freshness;
- minimum data quality;
- maximum error rate;
- maximum reconciliation discrepancy;
- maximum execution deviation;
- maximum model drift;
- minimum calibration quality;
- minimum sample size;
- maximum tail risk;
- maximum drawdown;
- maximum capacity utilization;
- maximum system resource contention.

Thresholds are versioned policies, not arbitrary constants hidden in code.

---

# 82. ENGINE DEFINITION OF READY

An engine is NOT implementation-ready until all of these exist:

- purpose;
- non-purpose;
- exact input schema;
- exact output schema;
- dependencies;
- state;
- transitions;
- invariants;
- hard vetoes;
- failure modes;
- error codes;
- fallback;
- recovery;
- events;
- persistence;
- versioning;
- security;
- observability;
- performance target;
- acceptance criteria;
- replay behavior;
- caller;
- orchestrator;
- downstream consumer;
- outcome link;
- feedback link.

---

# 83. ENGINE DEFINITION OF DONE

An engine is complete only when:

- implementation exists;
- contract tests pass;
- integration tests pass;
- persistence exists;
- events exist;
- consumer exists;
- lineage exists;
- observability exists;
- failure tests pass;
- replay is compatible;
- performance target is met;
- security checks pass;
- documentation is complete;
- acceptance gate is passed;
- decision-to-outcome chain is verified where applicable.

---

# 84. MASTER SYSTEM QUESTIONS

The system must be designed to answer these question classes.

## Market

- What is happening now?
- What changed recently?
- What is stable?
- What is transitioning?
- What is unknown?

## Data

- Where did this value come from?
- Was it available at decision time?
- Was it revised?
- Is it delayed?
- Is the source healthy?
- Is the source authoritative?

## Structure

- What structure is dominant?
- Where are key levels?
- Where is liquidity?
- Where is price relative to value?

## Order flow / microstructure

- Who is aggressive?
- Is aggression being absorbed?
- Is liquidity persistent?
- Is liquidity being pulled?
- Is queue pressure changing?
- Is a pattern observed or inferred?

## Derivatives

- How is OI changing?
- What is funding doing?
- What is basis doing?
- What does the options surface imply?
- What are the Greeks doing?
- How confident are positioning inferences?

## Macro / event

- What was expected?
- What happened?
- What was revised?
- Was the surprise meaningful?
- How did assets react?
- Has the reaction already been priced?

## Alpha

- What is the measurable edge?
- Under which conditions does it exist?
- How stable is it?
- How long does it survive?
- What other strategies depend on it?

## Strategy

- Is the strategy eligible now?
- Is it certified?
- Is it degraded?
- Has its expected edge decayed?

## Risk

- What can go wrong?
- How bad can it become?
- What happens under stress?
- What happens if liquidity disappears?
- What happens if correlations break?
- What happens if execution fails?

## Capital

- Is this the best use of scarce capital?
- What marginal portfolio risk is added?
- How much can actually be traded?

## Execution

- Is execution feasible?
- Is edge half-life greater than execution time?
- What is expected impact?
- What is expected slippage?
- What happens on partial fill?

## Reconciliation

- Do our orders match the venue?
- Do fills match the venue?
- Does position match the venue?
- Does cash match the venue?
- Does margin match the venue?

## Outcome

- Did the trade work?
- Why?
- Why not?
- What was expected vs realized?

## Learning

- Is the failure an alpha problem, execution problem, risk problem, data problem, model problem, regime problem, or operational problem?
- What evidence supports the conclusion?
- Is the proposed change robust enough to research?

---

# 85. OBSERVABILITY QUESTIONS

The system must always be able to answer:

- Is the system healthy?
- Can the system trade?
- Why can it not trade?
- Which critical dependency is degraded?
- Which source is active?
- Which data is stale?
- Which strategy is active?
- Which strategy is disabled?
- How much capital is available?
- How much capital is reserved?
- What positions exist externally?
- What positions does the system believe exist?
- What mismatches exist?
- What is the current portfolio heat?
- What are the latest decisions?
- What are the current open orders?
- What is the latest incident?

---

# 86. TRACEABILITY MATRIX

Every requirement must trace:

`REQUIREMENT → DOMAIN → ENGINE → CONTRACT → EVENT → TABLE → DECISION → CONSUMER → OUTCOME → FEEDBACK → TEST → ACCEPTANCE GATE`

No critical requirement may be orphaned.

No production table may exist without a business responsibility.

No production event may exist without a consumer.

No decision engine may exist without a downstream consumer or explicit non-trading terminal outcome.

No production learning proposal may exist without validation/certification state.

---

# 87. PRODUCTION TRADING AUTHORITY

Trading authority is granted only if all required states are true:

```text
SYSTEM_HEALTH = ACCEPTABLE
DATA_HEALTH = ACCEPTABLE
CLOCK_HEALTH = ACCEPTABLE
VENUE_HEALTH = ACCEPTABLE
RECONCILIATION = CLEAN
COMPLIANCE = PASS
STRATEGY = CERTIFIED_AND_ELIGIBLE
PROBABILITY = CALIBRATED_OR_APPROVED_POLICY
NET_EV = POSITIVE_AND_ABOVE_GATE
RISK = WITHIN_LIMITS
TAIL = ACCEPTABLE
RUIN = ACCEPTABLE
PORTFOLIO = ACCEPTABLE
CAPITAL = AVAILABLE
LIQUIDITY = SUFFICIENT
EXECUTION = FEASIBLE
```

If any hard requirement fails:

`NO TRADE`

---

# 88. CRITICAL UNKNOWN POLICY

The system shall explicitly represent:

`UNKNOWN`

rather than forcing:

`FALSE`, `TRUE`, `NEUTRAL`, or `0`.

Examples:

- unknown position;
- unknown market state;
- unknown source health;
- unknown options positioning;
- unknown liquidity;
- unknown execution capability.

Unknown critical state cannot authorize trading.

---

# 89. MARKET DATA ENTITLEMENT / LICENSING

The system must never assume that technically observable data is automatically licensed for every use.

Each source has:

- display rights;
- non-display rights;
- historical rights;
- redistribution rights;
- automated-use rights;
- storage rights;
- derived-data restrictions where applicable.

The implementation must separate **technical capability** from **legal/contractual entitlement**.

---

# 90. REALITY BOUNDARY

The system must not attempt to manufacture information that is structurally unavailable.

Examples:

- complete hidden institutional intent;
- complete dark-pool real-time order book when unavailable;
- guaranteed dealer inventory;
- guaranteed iceberg detection;
- guaranteed participant identity;
- guaranteed causality from correlation.

The correct response to unobservable information is probabilistic inference where justified, explicit uncertainty, or NO TRADE — never fabricated certainty.

---

# 91. DEPENDENCY / ALPHA CONCENTRATION

Strategy A, B and C may appear independent while sharing the same alpha driver.

The system must identify common factors such as:

- reversal;
- momentum;
- liquidity;
- volatility compression;
- gamma;
- macro surprise;
- funding;
- correlation breakdown.

Shared alpha factors consume a shared risk budget.

---

# 92. CHANGE CONTROL

New discoveries during implementation are classified as:

`BUG | CONTRACT_CORRECTION | ENHANCEMENT | NEW_REQUIREMENT | EXTERNAL_CONSTRAINT`

No new functionality is silently inserted into production code.

The required flow is:

`DISCOVERY → IMPACT ANALYSIS → CONTRACT CHANGE → VERSION → TEST → APPROVAL → IMPLEMENTATION`

---

# 93. REPOSITORY CONTRACT

```text
trading_system/
├─ app/
├─ contracts/
│  ├─ domain/
│  ├─ events/
│  ├─ enums/
│  ├─ state/
│  └─ policies/
├─ domains/
│  ├─ data/
│  ├─ market/
│  ├─ alpha/
│  ├─ strategy/
│  ├─ risk/
│  ├─ capital/
│  ├─ execution/
│  ├─ portfolio/
│  ├─ reconciliation/
│  ├─ outcome/
│  ├─ research/
│  └─ governance/
├─ infrastructure/
│  ├─ postgres/
│  ├─ nats/
│  ├─ object_store/
│  ├─ telemetry/
│  └─ connectors/
├─ runtime/
├─ research/
├─ migrations/
├─ configs/
├─ scripts/
├─ tests/
├─ data/
└─ docs/
```

---

# 94. REQUIRED TEST MATRIX

The platform shall include:

- unit tests;
- schema tests;
- contract tests;
- integration tests;
- property-based tests;
- deterministic replay tests;
- look-ahead tests;
- revision/vintage tests;
- sequence-gap tests;
- failover tests;
- failure injection tests;
- broker disconnect tests;
- venue disconnect tests;
- position mismatch tests;
- duplicate-order tests;
- authorization tests;
- compliance tests;
- backup/restore tests;
- resource contention tests;
- paper-vs-live consistency tests;
- end-to-end decision-to-outcome tests.

---

# 95. END-TO-END ACCEPTANCE TEST

At minimum, the platform must demonstrate a fully traceable synthetic/historical execution path:

`MARKET DATA`
→ `QUALITY`
→ `TEMPORAL SNAPSHOT`
→ `FEATURES`
→ `MARKET STATE`
→ `REGIME`
→ `CONTEXT`
→ `SETUP`
→ `ALPHA`
→ `STRATEGY`
→ `EXPECTANCY`
→ `PROBABILITY`
→ `EDGE`
→ `NO-TRADE`
→ `SIGNAL`
→ `RISK`
→ `CAPITAL`
→ `COMPLIANCE`
→ `EXECUTION AUTH`
→ `OMS`
→ `VENUE`
→ `FILL`
→ `POSITION`
→ `RECONCILIATION`
→ `OUTCOME`
→ `ATTRIBUTION`
→ `PERFORMANCE`
→ `FEEDBACK`

Every stage must be queryable by common correlation/decision identifiers.

---

# 96. FINAL FUNCTIONAL COMPLETENESS CHECKLIST

Before implementation begins, the following must all be marked PASS:

- [ ] Asset-class scope defined
- [ ] Venue scope defined
- [ ] Market profile model defined
- [ ] Maximum accessible data tiers identified
- [ ] Minimum required data tiers identified
- [ ] Source/entitlement matrix defined
- [ ] Observed/derived/inferred taxonomy defined
- [ ] Point-in-time truth defined
- [ ] Data revisions defined
- [ ] Data quality rules defined
- [ ] Data failover defined
- [ ] Instrument master defined
- [ ] Universe management defined
- [ ] Equities data scope defined where applicable
- [ ] Futures data scope defined where applicable
- [ ] Options data scope defined where applicable
- [ ] Crypto multi-venue scope defined where applicable
- [ ] FX scope defined where applicable
- [ ] Rates scope defined where applicable
- [ ] Fundamental scope defined where applicable
- [ ] Short/borrow scope defined where applicable
- [ ] Market internals scope defined where applicable
- [ ] News/sentiment scope defined
- [ ] Auction data scope defined
- [ ] Portfolio exposure scope defined
- [ ] Account scope defined
- [ ] Cash/treasury scope defined
- [ ] OMS scope defined
- [ ] EMS scope defined
- [ ] Venue/broker scope defined
- [ ] Settlement/accounting scope defined
- [ ] Compliance scope defined
- [ ] Strategy research universe defined
- [ ] Alpha dependency model defined
- [ ] Expectancy model defined
- [ ] Probability calibration defined
- [ ] Edge half-life defined
- [ ] No-trade conditions defined
- [ ] Risk hierarchy defined
- [ ] Tail-risk model defined
- [ ] Portfolio-risk model defined
- [ ] Capacity model defined
- [ ] Capital competition defined
- [ ] Position lifecycle defined
- [ ] Reconciliation defined
- [ ] Outcome model defined
- [ ] Attribution model defined
- [ ] Performance decomposition defined
- [ ] Drift lifecycle defined
- [ ] Research registry defined
- [ ] Replay defined
- [ ] Backtest defined
- [ ] Overfitting validation defined
- [ ] Statistical validation defined
- [ ] Model lifecycle defined
- [ ] Feature lifecycle defined
- [ ] Learning governance defined
- [ ] AI authority defined
- [ ] Champion/challenger defined
- [ ] Security roles defined
- [ ] Operational recovery defined
- [ ] Backup/restore defined
- [ ] Event taxonomy defined
- [ ] Domain schemas defined
- [ ] DB schema defined
- [ ] State machines defined
- [ ] Reason codes defined
- [ ] Engine dependency DAG defined
- [ ] Caller/orchestrator/consumer chain defined
- [ ] Numerical acceptance criteria defined
- [ ] Production certification gates defined
- [ ] Traceability matrix complete

Any unchecked item means the project is **not ready for implementation freeze**.

---

# 97. FINAL IMPLEMENTATION RULE

Once all Section 96 gates are PASS, implementation follows this principle:

> **The developer does not redesign the system during coding. The developer implements the contract.**

For every implementation step:

`CONTRACT → CODE → TEST → RUN → EVIDENCE → AUDIT → ACCEPT → NEXT`

Operational evidence supplied from the real environment may include:

- terminal output;
- SQL output;
- logs;
- screenshots;
- metrics;
- API responses;
- broker/venue reconciliation output;
- replay results.

Evidence that contradicts the contract triggers a controlled change request rather than an undocumented patch.

---

# 98. MASTER PRINCIPLE

The objective is not to build the largest possible trading system.

The objective is to build a system that:

1. knows what it actually knows;
2. knows what it does not know;
3. refuses to trade when critical information is invalid or unavailable;
4. distinguishes predictive evidence from narrative;
5. measures edge after real costs;
6. accounts for portfolio and tail risk;
7. executes only what is authorized and actually executable;
8. reconciles against external truth;
9. records exactly why each decision happened;
10. measures what actually happened;
11. separates alpha from execution and operational effects;
12. detects when its advantage disappears;
13. researches changes without contaminating production;
14. promotes changes only through objective evidence;
15. can be audited and reconstructed years later.

The desired end state is therefore:

```text
REAL MARKET
    ↓
REAL DATA
    ↓
TEMPORAL TRUTH
    ↓
MARKET INTELLIGENCE
    ↓
MEASURABLE ALPHA
    ↓
CALIBRATED PROBABILITY
    ↓
NET EXPECTANCY
    ↓
RISK / PORTFOLIO / TAIL CONTROL
    ↓
CAPITAL EFFICIENCY
    ↓
REAL EXECUTION
    ↓
REAL RECONCILIATION
    ↓
REAL OUTCOME
    ↓
REAL ATTRIBUTION
    ↓
CONTROLLED LEARNING
```

This is the intended operating model of the system.

---

# APPENDIX A — VERIFIED EXTERNAL DATA CAPABILITY REFERENCES

These references are used to establish what kinds of exchange/vendor data are technically available in the real market. They are not endorsements of any vendor and do not imply universal retail entitlement.

1. Nasdaq TotalView — full depth-of-book and NOII capabilities:  
   https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview

2. NYSE Real-Time Market Data — OpenBook Ultra, BBO, Trades and Order Imbalances:  
   https://www.nyse.com/market-data/real-time

3. CME Market by Order (MBO):  
   https://www.cmegroup.com/articles/faqs/market-by-order-mbo.html

4. OPRA — consolidated U.S. listed options quote and last-sale dissemination:  
   https://www.opraplan.com/

5. CFTC Commitment of Traders:  
   https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm

6. FRED real-time period / vintage concepts:  
   https://fred.stlouisfed.org/docs/api/fred/realtime_period.html

7. SEC EDGAR APIs:  
   https://www.sec.gov/search-filings/edgar-application-programming-interfaces

8. FINRA OTC Transparency:  
   https://www.finra.org/filing-reporting/otc-transparency

9. Nasdaq data/API capabilities:  
   https://www.nasdaq.com/solutions/data/nextgen-solutions

---

# APPENDIX B — STATUS INTERPRETATION

This V2 document is intentionally a **master contract candidate** rather than a claim that every numeric threshold, every individual venue entitlement, or every asset class has already been certified. Those concrete values belong in versioned policies and market profiles.

The functional architecture is considered complete only when the Section 96 checklist is explicitly reviewed and every production-scoped market profile has passed its own data, execution, risk, compliance, replay and certification gates.

**No software implementation should begin under the assumption that a missing contract item can be safely invented later.**

---

# FINAL FREEZE STATEMENT

When this document and all linked domain/event/database/state contracts are approved, it becomes the baseline for implementation.

New discoveries during development must enter the change-control process. They must not be silently appended into production logic.

**MASTER CONTRACT → IMPLEMENTATION → EVIDENCE → CERTIFICATION → CONTROLLED PRODUCTION**


# 99. IMPLEMENTATION FREEZE PACK V2.1

## 99.1 Authority and intent

This section converts the V2 master architecture from a functional architecture baseline into an executable contract baseline.

It does **not** introduce a new system architecture. It closes implementation ambiguity that would otherwise force the developer to invent material behavior during coding.

The authority order is:

`MASTER CONTRACT V2.1 → DOMAIN CONTRACTS → EVENT CONTRACTS → STATE CONTRACTS → POLICY CONTRACTS → MARKET PROFILE → CODE`

A lower layer may specialize an upper layer only where the upper layer explicitly permits specialization. A lower layer may never weaken a hard invariant.

The existing V2 engine registry remains authoritative for domain purpose and responsibility. The contracts below are authoritative for shared schemas, lifecycle semantics, events, persistence, policy evaluation, acceptance, and implementation boundaries.

## 99.2 Implementation scope boundary

The platform is multi-asset capable, but implementation is divided into three scopes:

`PLATFORM_CORE`

Universal infrastructure and governance that must not depend on a specific asset class:

- contracts;
- versioning;
- event transport;
- database;
- lineage;
- audit;
- policy evaluation;
- runtime supervision;
- observability;
- security;
- recovery;
- research registry;
- certification framework.

`MARKET_PROFILE_RUNTIME`

Market-specific behavior selected through a registered Market Profile:

- instruments;
- venues;
- data tiers;
- source adapters;
- market hours;
- transaction costs;
- execution capabilities;
- risk model;
- margin model;
- compliance rules;
- strategy eligibility;
- numerical thresholds.

`ACTIVE_PRODUCTION_SCOPE`

Only the market profiles that have completed all certification gates may authorize live trading.

An empty `ACTIVE_PRODUCTION_SCOPE` is valid and means:

`ANALYSIS_ONLY / PAPER_ONLY / NO_LIVE_TRADING`

This allows the entire platform to be implemented and tested before a production market is activated.

## 99.3 Required canonical contract package

The following repository artifacts are mandatory before implementation freeze:

```text
contracts/
├─ domain/
│  ├─ common.py
│  ├─ market.py
│  ├─ data.py
│  ├─ feature.py
│  ├─ state.py
│  ├─ regime.py
│  ├─ context.py
│  ├─ liquidity.py
│  ├─ alpha.py
│  ├─ strategy.py
│  ├─ expectancy.py
│  ├─ probability.py
│  ├─ risk.py
│  ├─ capital.py
│  ├─ execution.py
│  ├─ position.py
│  ├─ reconciliation.py
│  ├─ outcome.py
│  ├─ attribution.py
│  ├─ research.py
│  ├─ governance.py
│  ├─ certification.py
│  └─ ai.py
├─ events/
│  ├─ envelope.py
│  ├─ market.py
│  ├─ decision.py
│  ├─ execution.py
│  ├─ reconciliation.py
│  ├─ outcome.py
│  ├─ governance.py
│  └─ operations.py
├─ enums/
│  ├─ information_class.py
│  ├─ quality.py
│  ├─ reason_code.py
│  ├─ lifecycle.py
│  └─ authority.py
├─ state/
│  ├─ runtime.py
│  ├─ market_profile.py
│  ├─ source.py
│  ├─ strategy.py
│  ├─ model.py
│  ├─ feature.py
│  ├─ trade.py
│  ├─ order.py
│  ├─ position.py
│  ├─ reconciliation.py
│  ├─ incident.py
│  ├─ recovery.py
│  ├─ certification.py
│  ├─ learning.py
│  └─ champion_challenger.py
└─ policies/
   ├─ global_policy.py
   ├─ data_policy.py
   ├─ risk_policy.py
   ├─ capital_policy.py
   ├─ execution_policy.py
   ├─ portfolio_policy.py
   ├─ compliance_policy.py
   ├─ research_policy.py
   ├─ ai_policy.py
   ├─ runtime_policy.py
   └─ certification_policy.py
```

The directory is the minimum logical contract surface. Additional files may specialize a domain but may not create a parallel incompatible contract system.

## 99.4 Canonical identifier rules

Every persisted or decision-bearing object must use stable identifiers.

Required identifiers:

- `system_id` — immutable installation/system identity;
- `account_id` — external trading account identity;
- `venue_id` — venue/broker identity;
- `instrument_id` — canonical instrument identity;
- `market_profile_id` — market capability profile;
- `source_id` — registered data source;
- `dataset_id` — dataset identity;
- `feature_id` — feature identity;
- `strategy_id` — strategy identity;
- `model_id` — model identity;
- `policy_id` — policy identity;
- `decision_id` — final decision identity;
- `order_intent_id` — internal order authority identity;
- `client_order_id` — client-side order identity;
- `venue_order_id` — external venue order identity;
- `position_id` — position identity;
- `trade_id` — economic trade lifecycle identity;
- `outcome_id` — closed-trade outcome identity;
- `attribution_id` — attribution identity;
- `experiment_id` — research trial identity;
- `certification_id` — certification decision identity;
- `incident_id` — operational incident identity;
- `lineage_id` — end-to-end provenance identity;
- `correlation_id` — execution/event correlation identity;
- `causation_id` — direct event causality identity where applicable.

IDs are not reused. Retired IDs remain resolvable historically.

## 99.5 Versioning contract

All changeable decision-bearing artifacts require immutable versions:

`code_version`
`schema_version`
`data_version`
`feature_version`
`model_version`
`strategy_version`
`parameter_version`
`policy_version`
`execution_version`
`market_profile_version`
`contract_version`

Version format is semantic where the artifact is versioned semantically:

`MAJOR.MINOR.PATCH`

A version change that can alter a production decision requires at least a MINOR change and a new certification lineage. A breaking contract change requires MAJOR versioning and compatibility review.

Historical records reference the exact versions used. Historical records are never rewritten to the newest version.

## 99.6 Canonical contract envelope

Every production domain object uses the following envelope:

```yaml
id: UUID
object_type: string
schema_version: semver
status: enum
created_at: timestamp_utc
effective_at: timestamp_utc
observed_at: timestamp_utc|null
expires_at: timestamp_utc|null
source_id: UUID|null
source_version: string|null
code_version: string
lineage_id: UUID
correlation_id: UUID
quality_state: VALID|DEGRADED|INVALID|STALE|UNKNOWN|null
quality_score: float|null
information_class: OBSERVED|DERIVED|INFERRED|VENDOR_MODEL|UNKNOWN|UNAVAILABLE
payload: object
```

Decision-bearing objects additionally include:

```yaml
decision_id: UUID
policy_version: string
parameter_version: string
feature_version: string|null
model_version: string|null
strategy_version: string|null
execution_version: string|null
reason_codes: [string]
```

## 99.7 Canonical market data observation contract

Every raw observation conforms conceptually to:

```yaml
observation_id: UUID
source_id: UUID
source_version: string
instrument_id: UUID
venue_id: UUID
event_type: string
event_time: timestamp_utc
exchange_time: timestamp_utc|null
publish_time: timestamp_utc|null
receive_time: timestamp_utc
availability_time: timestamp_utc
processing_time: timestamp_utc
sequence_number: integer|null
revision_id: string|null
point_in_time_version: string
information_class: OBSERVED
quality_state: VALID|DEGRADED|INVALID|STALE|UNKNOWN
raw_payload_ref: string
checksum: string
```

Raw payload bytes are immutable. Parsed/curated representations reference the raw observation rather than replacing it.

## 99.8 Temporal snapshot contract

A temporal snapshot freezes the information set available to a decision at time `T`.

Required fields:

```yaml
snapshot_id: UUID
decision_time: timestamp_utc
market_profile_id: UUID
source_cutoff_map: object
dataset_versions: object
latest_allowed_availability_time: timestamp_utc
clock_state: object
included_observations: [UUID]
excluded_future_observations: [UUID]
revision_policy: string
snapshot_hash: string
```

A consumer may read only the snapshot or data explicitly authorized by it when performing a certified historical decision.

## 99.9 Quality result contract

```yaml
quality_id: UUID
subject_id: UUID
subject_type: string
state: VALID|DEGRADED|INVALID|STALE|UNKNOWN
quality_score: float
quality_confidence: float
block_flags: [string]
reason_codes: [string]
missingness_ratio: float|null
staleness_seconds: float|null
sequence_gap_count: integer
out_of_order_count: integer
duplicate_count: integer
clock_drift_seconds: float|null
coverage_ratio: float|null
evaluated_at: timestamp_utc
policy_version: string
```

A critical `block_flag` is authoritative for trade admission and cannot be downgraded by an alpha or AI component.

## 99.10 Feature value contract

```yaml
feature_value_id: UUID
feature_id: UUID
feature_version: string
instrument_id: UUID
as_of: timestamp_utc
value: scalar|vector|object
unit: string
information_class: DERIVED|INFERRED|VENDOR_MODEL
input_lineage_ids: [UUID]
quality_state: enum
quality_score: float
availability_latency_ms: float
formula_hash: string
```

A feature is not production-eligible without registration, lineage and leakage assessment.

## 99.11 Market state contract

```yaml
market_state_id: UUID
instrument_id: UUID
as_of: timestamp_utc
structure_state: object
volatility_state: object
liquidity_state: object
orderflow_state: object
positioning_state: object
derivatives_state: object
macro_state: object
event_state: object
cross_asset_state: object
uncertainty: object
quality: object
```

Observed values, deterministic derivatives and probabilistic inference are stored separately inside the state.

## 99.12 Regime contract

```yaml
regime_id: UUID
instrument_id: UUID
as_of: timestamp_utc
structural_regime: enum
volatility_regime: enum
liquidity_regime: enum
microstructure_regime: enum
event_regime: enum
correlation_regime: enum
positioning_regime: enum
macro_regime: enum
composite_regime: enum
transition_state: STABLE|TRANSITION|NEW_REGIME
confidence: float
quality: float
model_version: string
```

`TRANSITION` is a first-class state and is never silently mapped to a stable regime.

## 99.13 Context contract

```yaml
context_id: UUID
market_state_id: UUID
regime_id: UUID
expectations: object
priced_information: object
catalysts: [object]
confirmations: [object]
invalidation_conditions: [object]
surprise_conditions: [object]
unknowns: [object]
context_quality: object
```

## 99.14 Liquidity map contract

```yaml
liquidity_map_id: UUID
instrument_id: UUID
as_of: timestamp_utc
above_price: [object]
below_price: [object]
value_zones: [object]
stop_clusters: [object]
liquidation_clusters: [object]
resting_liquidity: [object]
gamma_zones: [object]
auction_zones: [object]
hvn_lvn: [object]
expected_exit_liquidity: [object]
emergency_liquidation_capacity: object
quality: object
```

Liquidity maps are descriptive until setup, edge, risk and execution admission authorize use.

## 99.15 Setup contract

```yaml
setup_id: UUID
instrument_id: UUID
type: string
direction: LONG|SHORT|NEUTRAL
trigger: object
context_id: UUID
evidence: [object]
invalidation: object
expected_path: object
expected_duration_seconds: float
liquidity_condition: object
regime_compatibility: object
historical_similarity: object
execution_feasibility: object
quality: object
```

A setup has no trading authority.

## 99.16 Alpha contract

```yaml
alpha_id: UUID
alpha_version: string
setup_id: UUID
condition_definition: object
direction: LONG|SHORT|NEUTRAL
historical_expectancy: object
probability_estimate: float|null
stability: float
half_life_seconds: float
capacity: object
dependency_factors: [string]
regime_sensitivity: object
decay_state: enum
uncertainty: object
```

## 99.17 Expectancy contract

```yaml
expectancy_id: UUID
alpha_id: UUID
gross_ev: financial_number
cost_breakdown:
  commission: financial_number
  spread: financial_number
  slippage: financial_number
  impact: financial_number
  funding: financial_number
  financing: financial_number
  borrow: financial_number
  exchange_fees: financial_number
  roll_cost: financial_number
  other: financial_number
net_ev: financial_number
currency: string
horizon_seconds: float
model_version: string
quality: object
```

`net_ev` is the production admission metric, subject to all policy gates.

## 99.18 Probability contract

```yaml
probability_id: UUID
model_id: UUID
model_version: string
instrument_id: UUID
strategy_id: UUID|None
regime_id: UUID|None
prediction_timestamp: timestamp_utc
probability_win: float
calibration_method: string
calibration_score: float
sample_size: integer
confidence_interval: object
calibration_state: enum
```

A confidence score can never substitute for calibrated probability.

## 99.19 Edge contract

```yaml
edge_id: UUID
alpha_id: UUID
probability_id: UUID
expectancy_id: UUID
edge_strength: float
edge_stability: float
edge_half_life_seconds: float
edge_capacity: object
edge_dependency: object
edge_concentration: object
edge_uncertainty: object
decay_state: NORMAL|WATCH|DEGRADING|DEFENSIVE|PROBATION|DISABLED
```

## 99.20 Trade thesis contract

```yaml
thesis_id: UUID
setup_id: UUID
alpha_id: UUID
direction: LONG|SHORT
entry_reason: object
expected_path: object
catalyst: object
confirmation: object
invalidation: object
targets: [object]
expected_holding_period_seconds: float
risk_definition: object
liquidity_condition: object
execution_mode: string
edge_half_life_seconds: float
expected_exit_condition: object
```

The thesis remains immutable after authorization except through a new versioned thesis transition.

## 99.21 Risk decision contract

```yaml
risk_decision_id: UUID
decision_id: UUID
account_id: UUID
instrument_id: UUID
strategy_id: UUID
risk_budget_available: financial_number
risk_requested: financial_number
risk_approved: financial_number
stop_distance: financial_number|None
volatility_adjustment: financial_number
correlation_adjustment: financial_number
portfolio_adjustment: financial_number
liquidity_adjustment: financial_number
tail_adjustment: financial_number
drawdown_adjustment: financial_number
final_size_cap: financial_number
risk_state: NORMAL|CAUTION|DEFENSIVE|CRITICAL|HALT
decision: APPROVE|REDUCE|REJECT
reason_codes: [string]
policy_version: string
```

Risk may reduce or reject risk. It may never be enlarged by an AI recommendation.

## 99.22 Capital decision contract

```yaml
capital_decision_id: UUID
decision_id: UUID
capital_available: financial_number
capital_requested: financial_number
capital_approved: financial_number
marginal_risk: financial_number
marginal_portfolio_contribution: financial_number
alpha_redundancy: float
liquidity_consumption: financial_number
capital_efficiency: float
capacity_usage: float
strategy_health: object
decision: ALLOCATE|ALLOCATE_REDUCED|REJECT
reason_codes: [string]
policy_version: string
```

## 99.23 Execution authorization contract

```yaml
execution_authorization_id: UUID
decision_id: UUID
account_id: UUID
venue_id: UUID
instrument_id: UUID
order_type: string
side: BUY|SELL
quantity_cap: financial_number
price_constraints: object
participation_cap: financial_number|None
urgency: string
max_slippage: financial_number
max_impact: financial_number
expiry_time: timestamp_utc
edge_half_life_remaining_seconds: float
execution_feasible: bool
reason_codes: [string]
execution_version: string
```

No order may be created without a valid execution authorization.

## 99.24 Order intent contract

```yaml
order_intent_id: UUID
decision_id: UUID
execution_authorization_id: UUID
client_order_id: string
account_id: UUID
venue_id: UUID
instrument_id: UUID
side: BUY|SELL
order_type: string
quantity: financial_number
limit_price: financial_number|null
stop_price: financial_number|null
time_in_force: string
parent_order_id: UUID|null
idempotency_key: string
created_at: timestamp_utc
expires_at: timestamp_utc|null
authority_status: AUTHORIZED|EXPIRED|CANCELLED|REVOKED
```

An Order Intent is authority to request an order, not evidence that the venue accepted it.

## 99.25 Fill contract

```yaml
fill_id: UUID
order_intent_id: UUID
client_order_id: string
venue_order_id: string
venue_execution_id: string
instrument_id: UUID
side: BUY|SELL
quantity: financial_number
price: financial_number
fee: financial_number
fee_currency: string
venue_time: timestamp_utc
receive_time: timestamp_utc
execution_latency_ms: float
```

Venue execution identifiers are idempotency keys for fill ingestion.

## 99.26 Position contract

```yaml
position_id: UUID
account_id: UUID
venue_id: UUID
instrument_id: UUID
side: LONG|SHORT|FLAT
quantity: financial_number
average_entry_price: financial_number
mark_price: financial_number
realized_pnl: financial_number
unrealized_pnl: financial_number
fees: financial_number
funding: float
margin_used: financial_number
thesis_id: UUID|null
state: FLAT|ENTRY_PENDING|PARTIAL|OPEN|MANAGING|EXIT_PENDING|CLOSED|RECONCILIATION_REQUIRED|HALTED|UNKNOWN
as_of: timestamp_utc
```

## 99.27 Reconciliation contract

```yaml
reconciliation_id: UUID
account_id: UUID
venue_id: UUID
run_at: timestamp_utc
orders_internal: integer
orders_external: integer
fills_internal: integer
fills_external: integer
positions_internal: object
positions_external: object
balances_internal: object
balances_external: object
margin_internal: object
margin_external: object
discrepancies: [object]
status: CLEAN|MISMATCH|UNKNOWN|FAILED
new_orders_allowed: bool
reason_codes: [string]
```

`new_orders_allowed` must be false for `MISMATCH`, `UNKNOWN`, and `FAILED` unless a separately certified safe fallback explicitly allows a limited operation.

## 99.28 Outcome contract

```yaml
outcome_id: UUID
trade_id: UUID
decision_id: UUID
entry_time: timestamp_utc
exit_time: timestamp_utc
gross_pnl: float
net_pnl: float
r_multiple: float
mfe: float
mae: float
duration_seconds: float
entry_slippage: float
exit_slippage: float
total_cost: float
execution_quality: object
thesis_outcome: object
strategy_outcome: object
data_quality: object
market_regime: object
liquidity_regime: object
```

## 99.29 Attribution contract

```yaml
attribution_id: UUID
outcome_id: UUID
alpha_contribution: float
selection_contribution: float
sizing_contribution: float
timing_contribution: float
execution_contribution: float
cost_contribution: float
market_contribution: float
regime_contribution: float
liquidity_contribution: float
feature_contributions: object
feature_failures: object
operational_contribution: float
unexplained_residual: float
attribution_quality: float
```

Attribution residual must be explicit. The system may not force the residual into an arbitrary cause.

## 99.30 Feedback / learning contract

```yaml
feedback_id: UUID
outcome_id: UUID|None
problem_class: ALPHA|EXECUTION|RISK|DATA|MODEL|REGIME|OPERATIONAL|RECONCILIATION|UNKNOWN
observed_evidence: [UUID]
hypothesis: object
proposed_change: object
research_required: bool
validation_required: bool
certification_required: bool
production_change_allowed: false
status: OBSERVED|RESEARCH|VALIDATING|REJECTED|CERTIFICATION_REQUIRED|CERTIFIED
```

No feedback object has direct production mutation authority.

## 99.31 Event envelope and delivery contract

All events use:

```yaml
event_id: UUID
event_type: string
event_version: semver
event_time: timestamp_utc
source: string
producer: string
correlation_id: UUID
causation_id: UUID|null
instrument_id: UUID|null
schema_version: semver
payload: object
```

Required transport semantics:

- transport: NATS JetStream;
- delivery: at-least-once;
- consumer processing: idempotent;
- acknowledgement: explicit;
- retry: bounded;
- dead letter: mandatory for non-recoverable messages;
- ordering: defined per subject where stateful;
- retention: policy-defined per event class;
- replay: supported for retained certified event classes.

No component may claim exactly-once business behavior merely because transport is durable.

## 99.32 Canonical NATS subject taxonomy

```text
market.raw.<asset>.<venue>.<instrument>
market.curated.<asset>.<venue>.<instrument>
market.quality.<source>
market.snapshot.<market_profile>
feature.<feature_id>
state.market.<instrument>
state.regime.<instrument>
context.<instrument>
liquidity.<instrument>
setup.<instrument>
alpha.<strategy>
expectancy.<strategy>
probability.<model>
edge.<strategy>
decision.signal.<instrument>
decision.risk.<instrument>
decision.capital.<account>
decision.execution.<account>
execution.intent.<venue>
execution.ack.<venue>
execution.fill.<venue>
position.<account>.<instrument>
reconciliation.<account>
outcome.<trade>
attribution.<trade>
feedback.<strategy>
learning.<strategy>
governance.policy
certification.<artifact>
operations.health
operations.incident
operations.recovery
```

Subject names are versioned through event schemas; producers must not change payload semantics without a schema version change.

## 99.33 Idempotency contract

Every external side effect must have an idempotency key.

Mandatory examples:

- order submission: `order_intent_id + venue_id`;
- cancel: `order_intent_id + cancel_version`;
- replace: `order_intent_id + replace_version`;
- fill ingestion: `venue_execution_id`;
- reconciliation run: `account_id + venue_id + run_timestamp_bucket`;
- migration: Alembic revision ID;
- release: release ID.

A retry must not create a second financial side effect.

## 99.34 State machine contracts

### Runtime

```text
BOOT
→ SELF_CHECK
→ READY
→ MONITORING
→ TRADING_ENABLED

Failure:
MONITORING/TRADING_ENABLED → DEGRADED → SAFE_MODE → HALTED

Recovery:
HALTED/SAFE_MODE → RECOVERING → RECONCILING → VALIDATED → READY
```

Trading authority may only be enabled from `VALIDATED`/`READY` conditions where all production authority predicates are true.

### Market profile

```text
UNASSESSED
→ DATA_VALIDATED
→ REPLAY_VALIDATED
→ PAPER_VALIDATED
→ SHADOW_VALIDATED
→ MICRO_VALIDATED
→ CERTIFIED
→ ACTIVE
```

### Strategy

```text
PROPOSED → RESEARCHED → VALIDATED → REGISTERED → ACTIVE → WATCH → DEGRADED → PROBATION → DISABLED → RESEARCH
```

### Trade

```text
WATCHING → CANDIDATE → VALIDATING → APPROVED → ENTRY_PENDING
→ PARTIALLY_FILLED → OPEN → MANAGING → EXIT_PENDING → CLOSED → ANALYZING
```

Exception states:

`REJECTED | CANCELLED | HALTED | RECONCILIATION_REQUIRED`

### Order

```text
CREATED → AUTHORIZED → SUBMITTED → ACKNOWLEDGED
→ PARTIALLY_FILLED → FILLED
```

Exception paths:

`REJECTED | CANCEL_REQUESTED | CANCELLED | REPLACE_REQUESTED | EXPIRED | UNKNOWN | RECONCILIATION_REQUIRED`

### Reconciliation

```text
CLEAN → CHECKING → MATCH | MISMATCH | UNKNOWN | FAILED
MISMATCH/UNKNOWN/FAILED → RECONCILIATION_REQUIRED
RECONCILIATION_REQUIRED → RESOLVING → CLEAN
```

### Certification

```text
UNASSESSED → DATA_PASS → TEMPORAL_PASS → REPLAY_PASS → BACKTEST_PASS
→ OVERFITTING_PASS → STATISTICAL_PASS → MODEL_RISK_PASS
→ PAPER_PASS → SHADOW_PASS → COMPLIANCE_PASS → MICRO_PASS
→ PROBATION_PASS → CERTIFIED
```

Any hard-gate failure moves the candidate to a non-production state and requires re-evaluation after remediation.

## 99.35 Source / entitlement matrix contract

Every real production source must have a registry record containing:

```yaml
source_id
vendor
product
feed_type
asset_class
venue_set
instrument_set
maximum_data_tier
minimum_required_tier
real_time_available
historical_available
point_in_time_available
latency_target
retention
revision_behavior
entitlement_display
entitlement_non_display
entitlement_automated_use
entitlement_historical
entitlement_storage
entitlement_redistribution
cost_model
rate_limit
failover_source_id
owner
certification_state
```

An implementation connector may exist without production entitlement. Such a connector is `NON_PRODUCTION` until entitlement is verified.

## 99.36 Feature-to-data dependency contract

Every production feature declares:

```yaml
feature_id
required_sources
required_data_types
minimum_data_tier
maximum_staleness
minimum_quality_score
required_temporal_fields
required_instrument_fields
fallback_behavior
missing_data_behavior
compute_latency_target
leakage_risk
certification_status
```

This makes it impossible for an engine to silently accept a lower-quality or stale input merely because a value exists.

## 99.37 Strategy-to-feature dependency contract

Every strategy declares:

```yaml
strategy_id
strategy_version
required_features
required_market_states
allowed_regimes
blocked_regimes
required_event_states
minimum_probability
minimum_net_ev
maximum_risk
maximum_capacity_usage
minimum_data_quality
maximum_staleness
execution_requirements
fallback
certification_state
```

No strategy can become eligible by simply returning a signal.

## 99.38 Policy contract

Policies are externalized from engines.

Mandatory policy families:

`SYSTEM | DATA | MARKET | STRATEGY | RISK | PORTFOLIO | CAPITAL | EXECUTION | COMPLIANCE | RESEARCH | AI | RUNTIME | CERTIFICATION`

Every policy has:

```yaml
policy_id
policy_version
effective_from
effective_until|null
scope
parameters
hard_rules
soft_rules
reason_codes
approval_state
approved_by
approved_at
checksum
```

The code may evaluate policies. It may not create hidden replacement thresholds.

## 99.39 Numerical policy contract
## 99.39.1 Financial-number canonical representation

All fields declared as `financial_number` in the canonical contracts are represented using the shared `FinancialNumber` schema. The implementation MUST bind precision, scale and rounding policy from the active numerical policy. A binary floating-point field MUST NOT be used as the source of truth for a decision-bearing financial quantity.


The following parameters must exist in the active Market Profile and policy set before live activation:

### Data

- maximum age by data type;
- minimum quality score;
- maximum gap tolerance;
- maximum clock drift;
- minimum coverage;
- maximum out-of-order rate.

### Alpha / probability

- minimum sample size;
- minimum calibration quality;
- calibration confidence interval policy;
- minimum net expectancy;
- minimum edge stability;
- maximum edge decay;
- maximum uncertainty.

### Risk

- maximum trade risk;
- maximum strategy risk;
- maximum factor risk;
- maximum asset risk;
- maximum portfolio heat;
- maximum daily loss;
- maximum weekly loss;
- maximum drawdown;
- maximum leverage;
- minimum margin buffer;
- maximum tail exposure;
- maximum ruin probability.

### Execution

- maximum spread;
- maximum slippage;
- maximum market impact;
- maximum participation;
- order acknowledgement timeout;
- cancel timeout;
- replace timeout;
- maximum execution latency;
- minimum edge half-life remaining.

### Operations

- maximum CPU threshold;
- maximum memory threshold;
- maximum queue age;
- maximum dependency outage duration;
- recovery timeout;
- heartbeat timeout.

**No global numerical default is silently assumed for live trading.** A missing required parameter makes the applicable profile `NON_CERTIFIED` and prevents live activation.

This preserves implementation determinism without inventing account-, venue- or strategy-specific risk values.

## 99.40 Risk calculation contract

Risk sizing is evaluated in this exact order:

`ACCOUNT → SURVIVAL CAPITAL → LOSS LIMIT → STRATEGY RISK → ASSET RISK → FACTOR RISK → TRADE RISK → STOP/INVALIDATION → VOLATILITY → CORRELATION → PORTFOLIO → LIQUIDITY → TAIL → CAPACITY → FINAL SIZE`

At each stage:

`approved_next = min(previous_ceiling, stage_ceiling)`

No downstream stage may increase the approved value.

If a stage cannot be evaluated because required information is `UNKNOWN`, the result is `REJECT` unless an explicitly certified conservative fallback exists.

## 99.41 Capital allocation contract

Capital allocation must compare all active candidates simultaneously.

The optimizer input set includes:

`net_ev, calibrated_probability, marginal_risk, portfolio_contribution, alpha_redundancy, liquidity_consumption, capacity, execution_feasibility, strategy_health, decay, tail_risk, capital_efficiency`

The result is:

`ALLOCATE | ALLOCATE_REDUCED | WAIT | REJECT`

The algorithm must be deterministic for a fixed versioned input snapshot and policy.

## 99.42 Execution contract

Execution must evaluate:

```text
EDGE_ALIVE?
DATA_HEALTH?
VENUE_HEALTH?
ORDER_VALID?
RISK_STILL_VALID?
CAPITAL_STILL_AVAILABLE?
POSITION_STATE_KNOWN?
```

Any hard failure revokes or expires execution authorization.

The execution engine may improve execution quality within the authorization envelope but may not increase quantity, risk, or capital beyond the authorization.

## 99.43 Reconciliation authority matrix

External truth authority is domain-specific:

- venue execution report: external execution truth;
- broker/venue position endpoint: external position truth;
- account/broker statement: external cash and balance truth;
- venue margin endpoint: external margin truth where applicable;
- internal decision ledger: decision-authority truth;
- internal audit ledger: system-action truth;
- settlement source: settlement truth.

When external sources disagree with each other, the system enters `UNKNOWN` and blocks new trading until the source hierarchy and reconciliation policy resolves the conflict.

## 99.44 Database implementation contract

The database is divided into these schema families:

```text
core
registry
market
features
state
regime
context
liquidity
alpha
strategy
decision
risk
portfolio
capital
execution
position
reconciliation
outcome
attribution
performance
research
validation
certification
governance
audit
observability
ai
memory
notifications
operations
```

Each production table requires:

- primary key;
- foreign keys where applicable;
- uniqueness constraints;
- check constraints;
- creation timestamp;
- update timestamp for mutable objects;
- version references;
- lineage reference where decision-bearing;
- indexes based on query/access contract;
- retention classification;
- audit classification;
- immutability classification.

Immutable fact tables may never receive in-place update or delete from application code.

Mutable state tables may change only through versioned state transitions.

Alembic migrations are the only schema authority.

## 99.45 Transaction boundary contract

A single business transaction must never depend on a distributed transaction across PostgreSQL, NATS and an external venue.

The system uses:

`DB transaction → durable event/outbox → consumer → external side effect → confirmation → reconciliation`

Where external side effects exist, the system must use an idempotent command/outbox pattern so that database commit and event publication cannot silently diverge.

## 99.46 Decision ledger contract

Every production decision must contain or reference:

```text
market_snapshot
source_versions
feature_versions
market_state_version
regime_version
context_version
setup_version
alpha_version
strategy_version
probability_version
expectancy_version
edge_version
risk_version
capital_version
execution_version
policy_versions
parameter_versions
reason_codes
authorization_chain
consumer_chain
outcome_link
```

A decision without complete critical lineage is not considered production-grade and may not be promoted.

## 99.47 Caller / orchestrator / consumer contract

Every material engine must declare:

```yaml
engine_id
caller
orchestrator
inputs
outputs
success_event
failure_event
downstream_consumer
persistence_target
outcome_link
feedback_link
```

Canonical control pattern:

`CALLER → ENGINE → ORCHESTRATOR → DECISION OBJECT → PERSISTENCE → EVENT → CONSUMER`

An engine may not silently call an unrelated downstream engine merely because a Python import is available.

The orchestrator owns sequence and admission. Engines own domain calculations.

## 99.48 Error and failure contract

Every failure is classified as one of:

`TRANSIENT | DATA | CONTRACT | POLICY | AUTHORIZATION | EXECUTION | RECONCILIATION | INFRASTRUCTURE | SECURITY | RESEARCH | MODEL | UNKNOWN`

Every failure emits:

```yaml
error_id
error_class
reason_code
component
severity
recoverable
retryable
first_seen
last_seen
correlation_id
causation_id
safe_state
operator_action_required
```

Unknown failures default to the safest valid state.

## 99.49 Recovery contract

Recovery is state-aware.

A recovered process may not automatically regain trading authority merely because the process is alive.

Required sequence after a trading-critical recovery:

`PROCESS_HEALTH → DATA_HEALTH → CLOCK_HEALTH → VENUE_HEALTH → ACCOUNT_SYNC → POSITION_RECONCILIATION → OPEN_ORDER_RECONCILIATION → RISK_REVALIDATION → CAPITAL_REVALIDATION → TRADING_AUTHORITY`

Failure at any stage keeps the system in `SAFE_MODE`, `HALTED`, or `RECONCILIATION_REQUIRED` as appropriate.

## 99.50 Release contract

A release is a binding manifest:

```yaml
release_id
code_version
contract_version
schema_version
data_contract_version
feature_versions
model_versions
strategy_versions
parameter_versions
policy_versions
execution_version
market_profile_versions
build_hash
created_at
approved_at
approved_by
rollback_release_id
```

A release cannot be activated if any required artifact is missing or uncertified.

## 99.51 Research / production isolation contract

Research may read production-derived data only through authorized versioned datasets.

Research may write:

- experiments;
- candidate features;
- candidate models;
- candidate strategies;
- validation artifacts;
- proposed policy changes.

Research may not write directly to:

- production policy;
- active strategy state;
- risk ceilings;
- production capital limits;
- live order authority;
- active model pointer.

Promotion is performed only by certification/release control.

## 99.52 Champion / challenger contract

Exactly one champion may be authoritative for a production decision role within a defined scope.

Challengers may run:

`OFFLINE | SHADOW | PAPER | MICRO`

A challenger may not replace a champion through performance observation alone.

Promotion requires:

`VALIDATION → RISK REVIEW → MODEL RISK → CERTIFICATION → RELEASE → ACTIVATION`

Rollback must reference the last certified champion release.

## 99.53 AI contract

AI outputs are structured recommendations, not authority.

Every AI output stores:

```yaml
ai_run_id
provider
model
model_version
prompt_template_version
input_context_hash
output_schema_version
recommendation
uncertainty
supporting_evidence
contradicting_evidence
safety_flags
latency
cost
```

AI authority remains bounded by deterministic policy.

AI cannot alter:

- risk limits;
- capital ceilings;
- margin limits;
- kill switches;
- reconciliation rules;
- security roles;
- production code;
- certification status;
- release state.

## 99.54 Observability contract

Every critical engine exposes at least:

```text
health_state
latency_p50
latency_p95
latency_p99
throughput
error_rate
stale_rate
input_quality
output_count
last_success_time
last_failure_time
dependency_state
```

Decision-bearing engines additionally expose:

```text
decision_count
reject_count
veto_count
reason_code_distribution
confidence_distribution
probability_distribution
expected_vs_realized
```

Critical alerts map to canonical incident reason codes.

## 99.55 Incident contract

Incident severity:

`INFO | WARNING | HIGH | CRITICAL`

Critical incidents may force:

`SAFE_MODE | HALT | RECONCILIATION_REQUIRED`

Every incident has:

```yaml
incident_id
severity
component
first_seen
last_seen
impact
current_state
mitigation
recovery_event
root_cause
related_decisions
related_orders
related_positions
postmortem_required
```

## 99.56 Backup / restore acceptance contract

A backup is not considered valid merely because it completed.

Acceptance requires:

1. backup artifact exists;
2. checksum/integrity validates;
3. restore environment is bootable;
4. migrations apply consistently;
5. critical tables restore;
6. audit/decision lineage remains queryable;
7. restore point satisfies the configured recovery objective;
8. a trading-disabled recovery test passes.

Restores never directly enable trading.

## 99.57 Resource governance contract

Resource governor protects the critical path.

Priority order:

`RISK / OMS / POSITION / RECONCILIATION / MARKET DATA > EXECUTION > CONTROL PLANE > RESEARCH > AI BACKGROUND`

When resources become constrained, low-priority work is throttled first.

No resource exhaustion path may create additional trading authority.

## 99.58 Exact production gate evidence

Every certification gate must produce an immutable evidence record:

```yaml
gate_id
artifact_id
scope
inputs
policy_versions
execution_versions
test_run_ids
metrics
observations
pass_fail
blocking_reasons
reviewer_or_approver
timestamp
```

A green dashboard without evidence is not a certification pass.

## 99.59 Traceability matrix schema

The master traceability table must contain:

```text
requirement_id
requirement_text
domain_id
engine_id
contract_id
event_id
table_name
decision_id_pattern
consumer_id
outcome_id_pattern
feedback_id_pattern
test_id
acceptance_gate
status
owner
version
```

Required invariant:

`status != COMPLETE` for any critical requirement means implementation freeze is not complete.

## 99.60 Acceptance matrix schema

Every engine acceptance record contains:

```text
engine_id
contract_test
schema_test
unit_test
integration_test
replay_test
failure_test
performance_test
security_test
observability_test
persistence_test
lineage_test
consumer_test
outcome_test
status
blocking_failure
```

The final status is:

`PASS` only when every applicable hard test is `PASS`.

## 99.61 End-to-end golden path

At least one deterministic golden dataset must be versioned and replayable.

The golden path must exercise:

`DATA → QUALITY → TEMPORAL SNAPSHOT → FEATURES → STATE → REGIME → CONTEXT → SETUP → ALPHA → STRATEGY → EV → PROBABILITY → EDGE → NO-TRADE → SIGNAL → RISK → CAPITAL → COMPLIANCE → EXECUTION AUTH → OMS → VENUE SIMULATOR → FILL → POSITION → RECONCILIATION → OUTCOME → ATTRIBUTION → FEEDBACK`

The golden run must prove:

- identical fixed input yields identical decision output within documented numerical tolerance;
- no future information is consumed;
- every state transition is legal;
- every decision has lineage;
- every event has a consumer;
- every persisted object is queryable;
- every failure test ends in a safe state where required.

## 99.62 Implementation readiness classification

The system recognizes five readiness levels:

### R0 — Architecture Ready

Master contract and domain responsibilities approved.

### R1 — Code Ready

Exact schemas, events, state contracts, policies, repository, database contract and engine dependency contracts exist.

### R2 — Test Ready

Golden data, test matrix, acceptance criteria and observability contracts exist.

### R3 — Operationally Live-Ready (V2.2.2 override)

A specific Market Profile, source entitlement set, account configuration, numerical policy, venue/execution integration, operational recovery controls and complete non-performance evidence package have passed all applicable operational gates.

`R3` is **not** trading authority and must not be interpreted as profitability certification.

R1 does not imply R3. R3 does not imply R4.

This distinction is mandatory.

## 99.63 Remaining external prerequisites for live activation

The architecture cannot and must not invent these real-world values:

- actual broker/venue account;
- actual source/vendor entitlements;
- actual credentials;
- actual instrument universe;
- actual venue trading permissions;
- actual transaction-fee schedules;
- actual margin rules;
- actual borrowing/funding terms;
- actual account capital;
- actual risk appetite parameters approved for the account;
- applicable legal/compliance requirements;
- actual latency measurements;
- actual data-quality measurements;
- actual execution measurements.

These are not architecture gaps. They are **runtime configuration and external certification inputs**.

The system remains non-tradable until they are registered and certified.

## 99.64 Freeze decision rule

The master contract may be declared:

`ARCHITECTURE_FROZEN = TRUE`

Historical V2.2.1/V2.2.2 freeze wording; this criterion is superseded by Section 152 and is not an active freeze rule.

The implementation repository may be declared:

`CODE_READY = TRUE`

only when R1 is complete.

Operational live readiness may be declared:

`R3_OPERATIONALLY_LIVE_READY = TRUE`

only when R3 is complete.

Actual trading authority may be declared:

`LIVE_AUTHORIZED = TRUE`

only when **R4 is complete** and all applicable external prerequisites, operational gates and profitability gates are simultaneously valid.

These readiness and authority states must never be conflated.

## 99.65 Final implementation invariant

From R1 onward:

> **The developer does not decide missing business behavior during coding. The developer resolves only defects against the approved contract.**

If code reveals a missing rule:

`STOP → CREATE CHANGE REQUEST → CLASSIFY → IMPACT ANALYSIS → VERSION CONTRACT → TEST → APPROVE → IMPLEMENT`

No silent production patch is permitted.

---

# 99.66 ENGINE CONTRACT / ORCHESTRATOR / CONSUMER MATRIX

The legacy engine registry names 96 engines. The following matrix is the executable routing baseline. It does not replace the engine-specific contracts; it removes ambiguity about the primary typed inputs, output contract, orchestrator ownership and downstream consumer.

| ID | Engine | Orchestrator | Primary typed inputs | Primary output | Downstream consumer |
|---:|---|---|---|---|---|
| 01 | SYSTEM GOVERNANCE ENGINE | GovernanceOrchestrator | governance contract / policy state | governance event / audit record | Control Plane / Audit |
| 02 | POLICY & LIMITS ENGINE | GovernanceOrchestrator | governance contract / policy state | governance event / audit record | Control Plane / Audit |
| 94 | SECURITY / ACCESS CONTROL | GovernanceOrchestrator | governance contract / policy state | governance event / audit record | Control Plane / Audit |
| 95 | VERSION CONTROL ENGINE | GovernanceOrchestrator | governance contract / policy state | governance event / audit record | Control Plane / Audit |
| 96 | AUDIT ENGINE | GovernanceOrchestrator | governance contract / policy state | governance event / audit record | Control Plane / Audit |
| 03 | DATA SOURCE REGISTRY | DataFoundationOrchestrator | SourceRegistry + EntitlementPolicy | SourceRegistered/SourceHealth | Ingestion + Quality |
| 04 | DATA INGESTION ENGINE | DataFoundationOrchestrator | SourceRegistry + Connectors + Clock | RawObservation | Temporal Truth / Quality |
| 05 | DATA QUALITY ENGINE | DataFoundationOrchestrator | RawObservation + TemporalClock | QualityResult | Market Snapshot / No-Trade |
| 06 | TEMPORAL TRUTH ENGINE | DataFoundationOrchestrator | RawObservation + ClockState | TemporalSnapshot | Feature / Replay |
| 07 | DATA LINEAGE ENGINE | DataFoundationOrchestrator | Observation/Feature/Decision artifacts | LineageRecord | Decision Ledger |
| 08 | CONTRACT / INSTRUMENT MASTER ENGINE | MarketProfileOrchestrator | SourceRegistry + MarketProfile | InstrumentMasterRecord | Universe / Data |
| 09 | HISTORICAL DATA LAKE | DataFoundationOrchestrator | RawObservation + DatasetManifest | DatasetVersion | Replay / Research |
| 92 | MARKET DATA FAILOVER ENGINE | DataFoundationOrchestrator | SourceHealth + QualityPolicy | SourceSelectionDecision | Ingestion / Quality |
| 93 | CLOCK / TIME SYNCHRONIZATION ENGINE | ControlPlaneOrchestrator | SystemClock + VenueClockObservations | ClockState | Temporal Truth / Health |
| 10 | FEATURE FABRIC | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 11 | VOLUME / PROFILE ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 12 | ORDER FLOW ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 13 | MICROSTRUCTURE ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 14 | LIQUIDITY BEHAVIOR ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 15 | LIQUIDITY CAPACITY ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 16 | OPTIONS ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 17 | GREEKS / GEX ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 18 | FUTURES / OI ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 19 | BTC DERIVATIVES ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 20 | VOLATILITY ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 21 | MACRO ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 22 | NEWS / EVENT ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 23 | CROSS-ASSET ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 24 | POSITIONING / COT ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 25 | SESSION ENGINE | MarketIntelligenceOrchestrator | TemporalSnapshot + domain market data | Feature/DomainState | Market State / Context |
| 26 | MARKET STATE ENGINE | MarketIntelligenceOrchestrator | FeatureSet + domain states | MarketState | Regime / Context / Setup |
| 27 | REGIME ENGINE | MarketIntelligenceOrchestrator | MarketState + history | RegimeState | Context / Strategy Eligibility |
| 28 | CONTEXT ENGINE | MarketIntelligenceOrchestrator | MarketState + RegimeState + EventState | ContextState | Setup / Alpha |
| 29 | LIQUIDITY MAP ENGINE | MarketIntelligenceOrchestrator | LiquidityState + MarketState | LiquidityMap | Setup / Risk |
| 30 | SETUP DETECTION ENGINE | DecisionResearchOrchestrator | Context/Setup/Feature evidence | SetupQuality/Conflict/Dependency | Alpha / Strategy |
| 31 | SETUP QUALITY ENGINE | DecisionResearchOrchestrator | Context/Setup/Feature evidence | SetupQuality/Conflict/Dependency | Alpha / Strategy |
| 32 | CONFLICT ENGINE | DecisionResearchOrchestrator | Context/Setup/Feature evidence | SetupQuality/Conflict/Dependency | Alpha / Strategy |
| 33 | ALPHA ENGINE | DecisionResearchOrchestrator | SetupQuality + FeatureSet + RegimeState | AlphaAssessment | Expectancy / Probability |
| 34 | ALPHA DEPENDENCY ENGINE | DecisionResearchOrchestrator | Context/Setup/Feature evidence | SetupQuality/Conflict/Dependency | Alpha / Strategy |
| 35 | STRATEGY LIBRARY | GovernanceOrchestrator | StrategyRegistry + ResearchArtifacts | StrategyDefinition | Eligibility / Research |
| 36 | STRATEGY ELIGIBILITY ENGINE | DecisionResearchOrchestrator | StrategyDefinition + Regime + DataQuality + Policy | StrategyEligibility | Signal / No-Trade |
| 37 | EXPECTANCY ENGINE | DecisionResearchOrchestrator | AlphaAssessment + Cost/Impact assumptions | ExpectancyAssessment | Edge / Decision |
| 38 | PROBABILITY CALIBRATION ENGINE | ResearchValidationOrchestrator | Model + historical outcomes + regime | ProbabilityAssessment | Edge / Decision |
| 39 | EDGE QUALITY ENGINE | DecisionResearchOrchestrator | Alpha + Probability + Expectancy | EdgeAssessment | No-Trade / Signal |
| 40 | NO-TRADE ENGINE | DecisionOrchestrator | All hard veto contracts | TradeAdmissionVeto | Signal Authorization |
| 41 | SIGNAL AUTHORIZATION ENGINE | DecisionOrchestrator | NoTrade + Edge + StrategyEligibility + Thesis | SignalAuthorization | Risk |
| 42 | TRADE THESIS ENGINE | DecisionOrchestrator | Setup + Alpha + Context + Invalidation | TradeThesis | Decision Council |
| 85 | DECISION COUNCIL | DecisionOrchestrator | Signal/Thesis + evidence independence | CouncilAssessment | Executive Decision |
| 86 | EXECUTIVE DECISION ENGINE | DecisionOrchestrator | Council + Risk preview + policy | ExecutiveDecision | Decision Consumer / Ledger |
| 87 | DECISION CONSUMER | DecisionOrchestrator | ExecutiveDecision | DecisionConsumerRecord | Risk / Capital / Audit |
| 43 | RISK ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 44 | RISK BUDGET HIERARCHY ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 45 | DRAWDOWN RESPONSE ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 46 | LOSS DISTRIBUTION ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 47 | RISK OF RUIN ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 48 | TAIL RISK ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 49 | STRESS SCENARIO ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 50 | MARGIN ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 51 | PORTFOLIO RISK ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 52 | CAPITAL ALLOCATION ENGINE | CapitalOrchestrator | RiskDecision + CandidateSet + PortfolioState | CapitalDecision | Execution Approval |
| 53 | CAPITAL COMPETITION ENGINE | CapitalOrchestrator | RiskDecision + CandidateSet + PortfolioState | CapitalDecision | Execution Approval |
| 54 | PORTFOLIO OPTIMIZATION ENGINE | CapitalOrchestrator | RiskDecision + CandidateSet + PortfolioState | CapitalDecision | Execution Approval |
| 55 | EXECUTION APPROVAL ENGINE | ExecutionOrchestrator | CapitalDecision + RiskDecision + VenueState | ExecutionAuthorization | OMS |
| 56 | EXECUTION ENGINE | ExecutionOrchestrator | ExecutionAuthorization + OrderIntent | VenueCommand/Fills | Position / Reconciliation |
| 57 | TRANSACTION COST ENGINE | ExecutionOrchestrator | MarketSnapshot + VenueCostModel | CostEstimate | Expectancy / Execution |
| 58 | MARKET IMPACT ENGINE | ExecutionOrchestrator | LiquidityMap + OrderIntentCandidate + CostModel | ImpactEstimate | Expectancy / Execution |
| 59 | RECONCILIATION ENGINE | ExecutionOrchestrator | InternalOrders/Fills/Positions + ExternalState | ReconciliationResult | Trading Authority / Position |
| 60 | FAILSAFE / RESILIENCE ENGINE | ControlPlaneOrchestrator | Health + Incidents + Policy | SafeStateDecision | Runtime / Trading Authority |
| 61 | POSITION MANAGER | ExecutionOrchestrator | Fills + Reconciliation | PositionState | Outcome / Risk |
| 62 | TRADE STATE MACHINE | DecisionOrchestrator | TradeEvents + Guards | TradeStateTransition | Execution / Outcome |
| 63 | IMMUTABLE DECISION LEDGER | AuditOrchestrator | Decision + Lineage + Versions | DecisionLedgerEntry | Outcome / Audit / Research |
| 64 | JOURNAL ENGINE | OutcomeOrchestrator | Decision/Trade/Position events | JournalRecord | Outcome / Attribution |
| 65 | OUTCOME ENGINE | OutcomeOrchestrator | ClosedTrade + Position/Fills + Cost | OutcomeRecord | Attribution / Performance |
| 66 | ATTRIBUTION ENGINE | OutcomeOrchestrator | Outcome + DecisionLineage + MarketState | AttributionRecord | Performance / Feedback |
| 67 | PERFORMANCE ENGINE | OutcomeOrchestrator | Outcome + Attribution | PerformanceMetrics | Drift / Certification |
| 68 | PERFORMANCE DECOMPOSITION ENGINE | OutcomeOrchestrator | Outcome + Attribution | PerformanceDecomposition | Research / Learning |
| 69 | STRATEGY DECAY ENGINE | LearningOrchestrator | Performance + Edge + Regime | StrategyHealth/Decay | Eligibility / Certification |
| 70 | MODEL / FEATURE DRIFT ENGINE | LearningOrchestrator | Feature/Model monitoring data | DriftAssessment | Model Risk / Eligibility |
| 71 | STRATEGY CORRELATION + ALPHA DEPENDENCY ENGINE | DecisionResearchOrchestrator | Context/Setup/Feature evidence | SetupQuality/Conflict/Dependency | Alpha / Strategy |
| 72 | RESEARCH TRIAL REGISTRY | ResearchValidationOrchestrator | Experiment + Dataset + Parameters | ResearchTrial | Validation / Certification |
| 88 | FEEDBACK ENGINE | LearningOrchestrator | Outcome + Attribution + Drift | FeedbackProposal | Research Registry |
| 89 | LEARNING GOVERNOR | LearningOrchestrator | FeedbackProposal + ValidationState | LearningDecision | Certification / Release |
| 73 | BACKTEST ENGINE | ResearchValidationOrchestrator | VersionedDataset + Strategy/Model + Policy | ValidationArtifact | Certification |
| 74 | MARKET REPLAY ENGINE | ResearchValidationOrchestrator | VersionedDataset + Strategy/Model + Policy | ValidationArtifact | Certification |
| 75 | OVERFITTING ENGINE | ResearchValidationOrchestrator | VersionedDataset + Strategy/Model + Policy | ValidationArtifact | Certification |
| 76 | STATISTICAL VALIDATION ENGINE | ResearchValidationOrchestrator | VersionedDataset + Strategy/Model + Policy | ValidationArtifact | Certification |
| 77 | STRATEGY CERTIFICATION ENGINE | CertificationOrchestrator | ValidationArtifacts + Policy + MarketProfile | CertificationRecord | Release / MarketProfile |
| 78 | LIVE SHADOW ENGINE | CertificationOrchestrator | CertifiedCandidate + LiveMarket | StageResult | Certification / Learning |
| 79 | PAPER TRADING ENGINE | CertificationOrchestrator | CertifiedCandidate + LiveMarket | StageResult | Certification / Learning |
| 80 | MICRO LIVE / PROBATION ENGINE | CertificationOrchestrator | CertifiedCandidate + LiveMarket | StageResult | Certification / Learning |
| 81 | CAPACITY ENGINE | RiskOrchestrator | Liquidity + Impact + Execution + Strategy | CapacityAssessment | Capital / Eligibility |
| 82 | MODEL RISK ENGINE | RiskOrchestrator | ExecutiveDecision + PortfolioState + RiskPolicy | RiskDecision/RiskState | Capital / Execution / No-Trade |
| 83 | AI RESEARCH ENGINE | AIOrchestrator | Market/Decision/Research Context | AIResearchArtifact | Research / Decision Council |
| 84 | AI AUTHORITY ENGINE | AIOrchestrator | AIResearchArtifact + AI policy | AIAuthorityDecision | Decision / Governance |
| 90 | OBSERVABILITY ENGINE | OperationsOrchestrator | EngineTelemetry + Events | TelemetryRecord | System Health / Incident |
| 91 | SYSTEM HEALTH ENGINE | OperationsOrchestrator | Telemetry + DependencyHealth + Incidents | SystemHealthState | Trading Authority / Failsafe |

### Matrix invariants

1. An engine may receive additional declared dependencies, but it may not invent undeclared dependencies at runtime.
2. The orchestrator owns sequencing, admission, retries, transaction boundaries and publication.
3. The engine owns only its domain calculation or state transition.
4. The consumer owns interpretation of the engine output in its own domain.
5. A missing consumer is a contract defect.
6. A direct engine-to-engine hidden call is prohibited when an orchestrator boundary exists.
7. Every row resolves to the common lineage model through `correlation_id`, `lineage_id`, `decision_id` where applicable.
8. Every output is persisted or explicitly classified as ephemeral telemetry; decision-bearing outputs are always persisted.
9. Every failure uses the canonical error envelope and safe-state contract.
10. Every production row must have corresponding contract, event, table and acceptance-test identifiers in the Traceability Matrix.

# 100. V2.1 FREEZE AUDIT

The V2 master architecture is considered **contract-complete for implementation planning** when all of the following are true:

- [ ] Master scope and authority frozen
- [ ] Canonical identifiers frozen
- [ ] Versioning contract frozen
- [ ] Shared object envelopes frozen
- [ ] Raw observation contract frozen
- [ ] Temporal snapshot contract frozen
- [ ] Data quality contract frozen
- [ ] Feature contract frozen
- [ ] Market state contract frozen
- [ ] Regime contract frozen
- [ ] Context contract frozen
- [ ] Liquidity contract frozen
- [ ] Setup contract frozen
- [ ] Alpha contract frozen
- [ ] Expectancy contract frozen
- [ ] Probability contract frozen
- [ ] Edge contract frozen
- [ ] Thesis contract frozen
- [ ] Risk decision contract frozen
- [ ] Capital decision contract frozen
- [ ] Execution authorization contract frozen
- [ ] Order intent contract frozen
- [ ] Fill contract frozen
- [ ] Position contract frozen
- [ ] Reconciliation contract frozen
- [ ] Outcome contract frozen
- [ ] Attribution contract frozen
- [ ] Feedback/learning contract frozen
- [ ] Event envelope frozen
- [ ] Event taxonomy frozen
- [ ] Idempotency rules frozen
- [ ] State machines frozen
- [ ] Source/entitlement matrix schema frozen
- [ ] Feature-to-data dependency schema frozen
- [ ] Strategy-to-feature dependency schema frozen
- [ ] Policy families frozen
- [ ] Numerical policy schema frozen
- [ ] Risk calculation order frozen
- [ ] Capital allocation semantics frozen
- [ ] Execution authorization boundaries frozen
- [ ] Reconciliation authority frozen
- [ ] DB transaction boundaries frozen
- [ ] Decision ledger frozen
- [ ] Caller/orchestrator/consumer contract frozen
- [ ] Error/failure contract frozen
- [ ] Recovery contract frozen
- [ ] Release contract frozen
- [ ] Research/production isolation frozen
- [ ] Champion/challenger lifecycle frozen
- [ ] AI output contract frozen
- [ ] Observability contract frozen
- [ ] Incident contract frozen
- [ ] Backup/restore acceptance frozen
- [ ] Resource governance frozen
- [ ] Certification evidence frozen
- [ ] Traceability matrix schema frozen
- [ ] Acceptance matrix schema frozen
- [ ] Golden path defined
- [ ] R0/R1/R2/R3/R4 readiness separation frozen
- [ ] R3 operational readiness explicitly separated from R4 profitability certification
- [ ] Live activation prerequisites explicitly separated from R3/R4 authority

**Freeze interpretation:** An unchecked item above is an implementation-governance defect. It does not necessarily block non-production scaffolding, but it blocks the claim that the platform is fully executable from contract alone.

# 101. V2.1 IMPLEMENTATION HANDOFF

Once R1 is reached, the implementation sequence becomes:

```text
01 CONTRACT PACKAGE
02 REPOSITORY / ENVIRONMENT
03 DATABASE / MIGRATIONS
04 EVENT TRANSPORT / OUTBOX
05 SOURCE REGISTRY / MARKET PROFILE
06 RAW INGESTION / TEMPORAL TRUTH
07 DATA QUALITY / FAILOVER
08 FEATURE FABRIC
09 MARKET STATE / REGIME / CONTEXT
10 LIQUIDITY / ORDER FLOW / MICROSTRUCTURE
11 SETUP / ALPHA / STRATEGY
12 EXPECTANCY / PROBABILITY / EDGE
13 NO-TRADE / SIGNAL / THESIS
14 RISK / PORTFOLIO / TAIL / STRESS
15 CAPITAL
16 COMPLIANCE
17 OMS / VENUE / ACCOUNT
18 EXECUTION / POSITION
19 RECONCILIATION / TREASURY
20 OUTCOME / ATTRIBUTION / PERFORMANCE
21 DRIFT / MODEL RISK
22 RESEARCH / REPLAY / BACKTEST
23 VALIDATION / CERTIFICATION
24 SHADOW / PAPER / MICRO
25 FEEDBACK / LEARNING / CHAMPION-CHALLENGER
26 AI GATEWAY / AI GOVERNANCE
27 OBSERVABILITY / INCIDENT / BACKUP
28 SECURITY / RELEASE
29 GOLDEN REPLAY
30 PRODUCTION GATE
```

At every step:

`CONTRACT → CODE → TEST → RUN → EVIDENCE → AUDIT → ACCEPT → NEXT`

No later phase may silently repair a contract defect belonging to an earlier phase.

# 102. MASTER STATUS AFTER V2.1

This document is no longer only a conceptual architecture specification.

It is the **master contract plus executable implementation contract framework**.

The remaining items that cannot be truthfully hardcoded in an architecture document are explicitly classified as external runtime/certification inputs rather than left as ambiguous implementation behavior.

The system's authority model is therefore:

```text
ARCHITECTURE FROZEN
        ↓
CONTRACTS FROZEN
        ↓
CODE READY
        ↓
TEST READY
        ↓
MARKET PROFILE CERTIFIED
        ↓
LIVE AUTHORIZED
```

No stage may be skipped.

# 103. FINAL V2.1 FREEZE STATEMENT

**MASTER CONTRACT → IMPLEMENTATION → EVIDENCE → CERTIFICATION → CONTROLLED PRODUCTION**

The system may be built without redesigning its architecture during coding.

Business behavior is defined by versioned contracts and policies.

Market-specific reality is defined by certified Market Profiles.

Unknowns fail closed.

Research remains isolated from production.

AI remains bounded by deterministic authority controls.

Execution remains subordinate to risk, capital, authorization and reconciliation.

Every production decision remains reconstructable.

Every material learning proposal remains subject to research, validation and certification.

**This is the executable architecture baseline.**

---

# APPENDIX C — V1 ENGINE MASTER REGISTRY RETAINED AS BASELINE

The complete V1 engine registry is retained below as the legacy baseline. V2 functional contracts and new domains in this document supersede any V1 statement that conflicts with the V2 master contract.

---

# TRADING SYSTEM - ARCHITECTURE CONTRACT V1

**Document status:** FROZEN FOR IMPLEMENTATION

**Version:** 1.0.0  
**Source basis:** MASTER ARCHITECTURE V2 (17 Aug 2026)  
**Scope:** Autonomous Adaptive Trading System (independent project; not ALADDIN)

## 0. Executive Contract
The system is an autonomous, adaptive trading platform designed to operate from a single-button Windows startup, monitor markets continuously in the background, detect and validate opportunities, manage risk and capital, execute authorized trades, notify the operator, preserve decision/outcome memory, and evolve only through controlled research/validation/certification. No return or win-rate outcome is guaranteed; the engineering objective is durable positive net expectancy under bounded risk.

## 1. Scope and Non-Goals
### In scope
- Real-time market surveillance and multi-source data ingestion
- Historical data lake and temporal truth
- Feature/market-state/regime intelligence
- Alpha/strategy/expectancy/probability decisioning
- Deterministic risk, portfolio risk and capital allocation
- Execution, reconciliation and position management
- Outcome, attribution, performance and drift
- Research, replay, overfitting and statistical validation
- AI research and controlled authority
- Immutable decision/audit lineage
- One-click runtime, watchdog, game-mode resource management and notifications
### Non-goals
- No guaranteed profitability
- No uncontrolled live self-modification of production strategies/models
- No AI authority to bypass risk/policy/reconciliation
- No vendor-specific coupling inside trading engines
- No direct production deployment from a research experiment

## 2. Locked Technology Decisions
| Layer | Locked decision |
|---|---|
| OS/runtime host | Windows workstation initially; runtime isolated from game workload |
| Language | Python 3.14.x |
| IDE | VS Code |
| Operational DB | PostgreSQL 18.x |
| DB administration | pgAdmin 4 |
| ORM/DB access | SQLAlchemy 2.x |
| DB migrations | Alembic |
| Typed contracts | Pydantic |
| Internal/API surface | FastAPI |
| Event transport | NATS JetStream |
| Research dataframe | Polars |
| Numerics | NumPy/SciPy/scikit-learn/statsmodels |
| Columnar format | Apache Parquet |
| Research query | DuckDB |
| Observability | Prometheus + Grafana OSS |
| Notifications | Telegram Bot API |
| Version control | Git |
| Raw/archive storage | Object storage abstraction; B2-compatible target initially |
| AI | Provider-agnostic AI Gateway; OpenAI models supported initially |

## 3. Architecture Topology
```text
Windows
  └─ System Supervisor
      ├─ Trading Core (modular monolith)
      │   ├─ Data Foundation
      │   ├─ Market Intelligence
      │   ├─ Alpha & Decision
      │   ├─ Risk & Portfolio
      │   ├─ Execution & Position
      │   └─ Outcome / Learning
      ├─ Research Runtime
      ├─ Control Plane
      │   ├─ Watchdog
      │   ├─ Scheduler
      │   ├─ Resource Manager
      │   ├─ Notifications
      │   └─ Recovery
      └─ Infrastructure
          ├─ PostgreSQL
          ├─ NATS JetStream
          ├─ Parquet/Object Store
          └─ Prometheus/Grafana
```

## 4. Global Invariants (Hard Rules)
1. Invalid critical data => NO TRADE.
2. Stale critical data => NO TRADE.
3. Future information => inaccessible to backtest/replay decision logic.
4. Observed facts and inferred states are stored separately.
5. Signal approval is not capital approval.
6. Capital approval is not execution approval.
7. Execution cannot bypass authorization.
8. Broker/internal mismatch => new orders blocked and reconciliation required.
9. Unknown position state => safe state + reconciliation.
10. Risk policy is deterministic and cannot be overridden by AI.
11. AI cannot change risk ceilings, margin ceilings, kill switches or reconciliation policy.
12. Every production decision is append-only in the immutable decision ledger.
13. Every production decision references code/data/feature/model/parameter/policy/execution versions.
14. Learning cannot directly modify production.
15. Production strategy changes require research, validation, certification and gated redeployment.
16. Unacceptable probability calibration, ruin risk, tail risk, model drift or execution degradation can veto trading.
17. Every consumer is idempotent on event_id.
18. Every critical state transition is auditable.
19. Fail-closed is the default for trading-critical uncertainty.
20. Operational notification failure must not silently create an unauthorized trade state.

## 5. Canonical Decision Chain
```text
MARKET / WORLD
↓ DATA ACQUISITION
↓ DATA INTEGRITY
↓ DATA NORMALIZATION
↓ TEMPORAL TRUTH
↓ HISTORICAL DATA LAKE
↓ FEATURE FABRIC
↓ MARKET STATE
↓ REGIME
↓ CONTEXT
↓ LIQUIDITY MAP
↓ SETUP DETECTION
↓ CONFLICT ANALYSIS
↓ ALPHA / STRATEGY
↓ STRATEGY ELIGIBILITY
↓ EXPECTANCY
↓ PROBABILITY CALIBRATION
↓ NET EDGE
↓ NO-TRADE
↓ SIGNAL AUTHORIZATION
↓ RISK
↓ TAIL RISK
↓ PORTFOLIO RISK
↓ CAPITAL ALLOCATION
↓ EXECUTION AUTHORIZATION
↓ EXECUTION
↓ RECONCILIATION
↓ POSITION MANAGEMENT
↓ TRADE STATE MACHINE
↓ OUTCOME
↓ ATTRIBUTION
↓ PERFORMANCE
↓ DECAY / DRIFT
↓ RESEARCH
↓ VALIDATION
↓ CERTIFICATION
↓ REDEPLOYMENT
↺
```

## 6. Event Contract
Every runtime event uses the envelope below:
```yaml
event_id: UUID
event_type: string
event_version: semver
event_time: UTC timestamp
source: string
producer: string
correlation_id: UUID
causation_id: UUID|null
instrument_id: UUID|null
schema_version: semver
payload: object
```
Delivery policy: at-least-once + idempotent consumers. Exactly-once semantics are not assumed at the transport layer.

## 7. Shared Domain Contract
Every production domain object must expose or be traceable to: `id`, `schema_version`, `created_at`, `effective_time`, `source_version`, `code_version`, `status`, and `confidence/quality` where meaningful. Decision-bearing objects additionally carry `decision_id`, `data_version`, `model_version`, `policy_version`, and `execution_version` references.

## 8. Database Contract
### PostgreSQL schema namespaces
`core`, `registry`, `market`, `features`, `state`, `regime`, `context`, `liquidity`, `alpha`, `strategy`, `decision`, `risk`, `portfolio`, `capital`, `execution`, `position`, `reconciliation`, `outcome`, `attribution`, `performance`, `research`, `validation`, `certification`, `governance`, `audit`, `observability`, `ai`, `memory`, `notifications`, `operations`
### Persistence rules
- Decision, audit and version records are append-only.
- Raw market data is not stored as an unconstrained operational table; large historical payloads live in the data lake.
- Every mutable business table has created/updated timestamps and version references.
- Production writes are executed through application services, not ad-hoc manual edits.
- pgAdmin is an administration and inspection tool, not the source of schema truth; Alembic migrations are authoritative.

## 9. Data Lake Contract
```text
data/raw/<vendor>/<asset>/<instrument>/<YYYY>/<MM>/<DD>/*.parquet
data/curated/<dataset>/<version>/*.parquet
data/features/<feature_set>/<version>/*.parquet
data/replay/<run_id>/*
data/research/<research_id>/*
```
Raw data is immutable; every dataset has a manifest, checksum, coverage interval, vendor metadata and quality state.

## 10. Runtime / One-Click Operation Contract
Startup sequence: `BOOT → SELF_CHECK → READY → MONITORING → TRADING_ENABLED`. Failure states route to `DEGRADED → SAFE_MODE → HALTED` and recovery uses `RECOVERING → RECONCILING → READY`.
### Game Mode
Game Mode throttles non-critical research/AI workloads while preserving market feed, risk, execution, position management, watchdog and reconciliation. Critical trading-path latency and correctness are acceptance-tested with and without an active game workload.

## 11. Notifications and Mobile Control
Telegram Bot API is the initial notification transport. Notification classes: TRADE, RISK, SYSTEM, LEARNING, CRITICAL, DAILY SUMMARY. Notifications are asynchronous; notification failure cannot create a new trade. Mobile control is authenticated and capability-scoped; high-impact actions require stronger authorization.

## 12. Memory and Learning
Memory layers: Raw Memory, Decision Memory, Outcome Memory, Pattern Memory, Research Memory, Model Memory, Regime Memory, Execution Memory. LLM context is not the system of record; AI retrieves structured historical cases from governed memory stores.
Learning lifecycle: `OBSERVE → DETECT → HYPOTHESIZE → RESEARCH → VALIDATE → CERTIFY → PAPER → PROBATION → DEPLOY`.
Champion/Challenger is required for production strategy evolution: a certified challenger cannot replace a champion without objective gates and rollback support.

## 13. AI Governance Contract
AI may analyze, interpret, rank, research, hypothesize and recommend. AI may not change risk limits, capital ceilings, kill switches, reconciliation policy, security roles or production code directly. AI is not required on the critical low-latency path. AI model usage is budgeted and versioned.

## 14. Execution and Reconciliation Contract
Order path: `Signal → Risk Authorization → Capital Authorization → Execution Authorization → Order Intent → Venue Adapter → Fill → Position Update → Reconciliation`. Any mismatch in orders, fills, positions or balances blocks new orders until reconciled.

## 15. Testing and Acceptance Contract
- Unit tests
- Contract/schema tests
- Integration tests
- Property-based tests
- Deterministic replay tests
- Look-ahead/data-leak tests
- Failure injection / resilience tests
- Performance/latency tests
- Security/authorization tests
- Backup/restore tests
- End-to-end decision-to-outcome tests
- Game-mode resource contention tests
### Definition of Ready (per engine)
Purpose, inputs, outputs, dependencies, state, invariants, failure modes, fallback, persistence, versioning, events, metrics, security requirements and acceptance tests are defined.
### Definition of Done (per engine)
Contract implemented, tests green, integration verified, observability emitted, persistence versioned, failure modes tested, replay compatible, performance target met, documentation complete and acceptance gate passed.

## 16. Production Certification Gates
`Architecture PASS → Contracts PASS → Data PASS → Replay PASS → Backtest PASS → Overfitting PASS → Statistical Validation PASS → Paper PASS → Shadow PASS → Micro PASS → Probation PASS → Production`

## 17. Engine Master Contract Registry
### Governance & Control Plane
#### 01. SYSTEM GOVERNANCE ENGINE
**Purpose:** Define authority, activation, approval, version, emergency and audit policies for the whole platform.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** policy set, approval records, emergency authority state.
**Dependencies:** governance store, policy engine, version control, audit.
**Invariant:** Policy is never modified by an AI component; every production policy change is versioned and approved.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bunu önceki mimaride yeterince yukarı koymamışız. Kod yazılmadan önce sistemin **hangi kurallara göre değiştirilebileceği** belirlenmeli. Governance Engine Sorumlulukları: strategy activation policy risk policy capital policy model approval parameter approval data vendor approval deployment approval emergency authority

#### 02. POLICY & LIMITS ENGINE
**Purpose:** Enforce immutable account, portfolio, strategy, asset, factor, event, liquidity, execution, loss and margin limits.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** limits, effective policy version, admission decisions.
**Dependencies:** system governance, portfolio/risk inputs.
**Invariant:** No decision may bypass an active hard limit.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Risk Engine'den bile önce gelen katman. Burada sistemin değişmez sınırları bulunacak. ACCOUNT LIMITS PORTFOLIO LIMITS STRATEGY LIMITS ASSET LIMITS FACTOR LIMITS EVENT LIMITS LIQUIDITY LIMITS EXECUTION LIMITS LOSS LIMITS MARGIN LIMITS Örneğin bir strategy ne kadar iyi olursa olsun: MAX_ACCOUNT_RISK MAX_STRATEGY_RISK MAX

#### 94. SECURITY / ACCESS CONTROL
**Purpose:** Enforce role separation, least privilege, secret hygiene and access control.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** authorization decisions/audit events.
**Dependencies:** identity store, secrets, policy.
**Invariant:** AI cannot have system-admin privileges.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Üretim sisteminde: read-only research strategy-admin risk-admin execution system-admin gibi yetkiler ayrılmalı. Hiçbir AI bileşeni: > system-admin yetkisine sahip olmamalı.

#### 95. VERSION CONTROL ENGINE
**Purpose:** Version data, features, strategy, model, parameters, risk policy and execution artifacts.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** version registry and lineage references.
**Dependencies:** Git, registry, DB metadata.
**Invariant:** Every production decision references immutable versions.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her sonuç: Data Version Feature Version Strategy Version Model Version Parameter Version Risk Policy Version Execution Version ile saklanacak. Orijinal blueprint bunu zaten doğru şekilde tanımlıyor.

#### 96. AUDIT ENGINE
**Purpose:** Audit who/what/when/why/version/input/output/policy/action for critical events.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** audit records.
**Dependencies:** all domains.
**Invariant:** Audit is append-only and independently queryable.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her kritik olay: WHO WHAT WHEN WHY WHICH VERSION WHAT INPUT WHAT OUTPUT WHAT POLICY WHAT ACTION şeklinde loglanacak.

### Data Foundation
#### 03. DATA SOURCE REGISTRY
**Purpose:** Register every external data source with quality, latency, licensing and cost metadata.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** source registry records, health/quality status, entitlements.
**Dependencies:** configuration, vendor APIs.
**Invariant:** No unregistered production data source may feed a decision path.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Eski mimaride veri kaynakları vardı; ama **hangi veriye ne kadar güvenildiği** ayrı bir sistem olmalı. Her source: vendor instrument coverage latency historical depth timestamp quality revision behavior availability licensing cost quality score ile tanımlanacak. Bu, ileride: > “Vendor A değişti, strategy neden bozuldu?

#### 04. DATA INGESTION ENGINE
**Purpose:** Acquire tick, trades, OHLC, quotes, MBP/MBO, derivatives, macro, news, positioning and calendar data.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** immutable raw observations / batches.
**Dependencies:** source registry, connectors, clock.
**Invariant:** Raw observations are append-only and preserve source timestamps.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal yapı korunuyor. Tick Trades OHLC Bid/Ask MBP MBO Volume OI Futures Options Greeks IV GEX Macro News COT Cross Asset Session Calendar Orijinal blueprint bu geniş veri yelpazesini zaten tanımlıyor. Ancak bundan sonra önemli bir fark geliyor.

#### 05. DATA QUALITY ENGINE
**Purpose:** Detect invalid, stale, incomplete, duplicate, unordered, delayed or corrupted data and produce quality state.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** quality score/state/confidence, block flags.
**Dependencies:** data ingestion, temporal truth.
**Invariant:** Critical quality failure blocks decision admission.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her veri: valid? fresh? complete? duplicated? ordered? delayed? corrupted? kontrolünden geçecek. Ama yeni mimaride yalnızca: > DATA VALID / INVALID değil: QUALITY SCORE QUALITY STATE QUALITY CONFIDENCE üretilecek. Örneğin: DATA_QUALITY = 97.8 LATENCY = 4ms SEQUENCE = VALID COMPLETENESS = 99.9% CONFIDENCE = HIGH ve krit

#### 06. TEMPORAL TRUTH ENGINE
**Purpose:** Preserve temporal truth and determine what information was actually available at decision time.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** availability-aware observation/snapshot.
**Dependencies:** ingestion, clock, source metadata.
**Invariant:** Future information must never be accessible to replay/backtest decision logic.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bence bunu artık **Temporal Alignment Engine**'den daha büyük düşünmeliyiz. Her observation: event_time publish_time receive_time effective_time processing_time availability_time taşıyacak. Amaç: “O anda sistem gerçekten ne biliyordu?” sorusunu kesin olarak cevaplamak. Bu özellikle: macro news COT options revised econo

#### 07. DATA LINEAGE ENGINE
**Purpose:** Trace each feature/model/decision back to raw source data and transformations.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** lineage graph / lineage IDs.
**Dependencies:** data lake, feature fabric, model registry.
**Invariant:** Every production decision must have a resolvable lineage path.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni eklediğim kritik engine. Her feature'ın: RAW DATA ↓ TRANSFORMATION ↓ FEATURE ↓ MODEL ↓ DECISION soy ağacı bulunacak. Örneğin sistem: GEX = +4.2B derse aylar sonra: > Bu değer nereden geldi? sorusunun cevabı bulunabilecek.

#### 08. CONTRACT / INSTRUMENT MASTER ENGINE
**Purpose:** Canonicalize instrument identity, contract lifecycle and continuous-contract lineage.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** instrument master records.
**Dependencies:** source registry, market data.
**Invariant:** Raw contract identity must remain distinct from continuous contract identity.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Futures için mevcut tasarım korunuyor: symbol expiration tick size tick value multiplier trading hours settlement first notice last trade roll date ve: RAW CONTRACT ≠ CONTINUOUS CONTRACT Bu ayrım kesinlikle korunmalı. Buna: instrument identity contract lineage corporate action roll adjustment settlement methodology ekl

#### 09. HISTORICAL DATA LAKE
**Purpose:** Store immutable RAW, curated and feature datasets for historical analysis and replay.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** dataset versions, partitions, manifests.
**Dependencies:** ingestion, object storage.
**Invariant:** RAW datasets are never overwritten.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Raw data **asla overwrite edilmemeli.** Üç katman: RAW CURATED FEATURE olacak. Ve: RAW DATA → IMMUTABLE olmalı. Araştırmacı feature'ı değiştirebilir ama tarihsel ham veriyi değiştiremez.

#### 92. MARKET DATA FAILOVER ENGINE
**Purpose:** Fail over data sources and reduce to NO TRADE when reliable data cannot be obtained.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** active source state and failover event.
**Dependencies:** source registry, quality engine.
**Invariant:** Failover does not silently increase uncertainty.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bir veri kaynağı düşerse: PRIMARY ↓ SECONDARY ↓ FALLBACK ↓ NO TRADE mekanizması bulunacak.

#### 93. CLOCK / TIME SYNCHRONIZATION ENGINE
**Purpose:** Maintain event-time correctness and monitor clock drift/order/timestamp/latency asymmetry.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** clock health and temporal diagnostics.
**Dependencies:** host/network clocks, feed timestamps.
**Invariant:** Critical clock drift blocks time-sensitive trading.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Özellikle MBO/order-flow/execution için: clock drift event ordering timestamp discrepancy latency asymmetry izlenecek.

### Feature & Market Intelligence
#### 10. FEATURE FABRIC
**Purpose:** Compute reusable price, fractal and structure features.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** versioned feature snapshots.
**Dependencies:** curated market data, instrument/session context.
**Invariant:** Feature calculation is deterministic for fixed inputs and version.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Eski Feature Engine yapısını daha düzgün bir mimariye dönüştürüyoruz. A — Price Engine return ATR realized volatility range gap HOD/LOD VWAP AVWAP session statistics B — Fractal Engine swing hierarchy fractal highs/lows nested structure compression expansion multi-timeframe alignment C — Structure Engine HH HL LH LL BO

#### 11. VOLUME / PROFILE ENGINE
**Purpose:** Compute volume/profile structures including POC, value areas, HVN/LVN and transitions.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** profile state and transition features.
**Dependencies:** trade/volume data, session.
**Invariant:** Profile definitions are versioned and reproducible.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Korunacak: POC VAH VAL HVN LVN Developing POC Session Profile Daily Weekly Monthly Composite VWAP AVWAP POC migration Ama yeni olarak: Profile Transition Engine eklenmeli. Çünkü: > POC nerede? kadar: > POC nereye hareket ediyor? daha önemli olabilir.

#### 12. ORDER FLOW ENGINE
**Purpose:** Compute order-flow pressure and auction dynamics.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** delta, CVD, aggressor, imbalance, absorption, exhaustion and divergence features.
**Dependencies:** trade/quote/MBO data.
**Invariant:** Observed facts and inferred states must be separately represented.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Korunacak: Delta CVD Bid Volume Ask Volume Aggressor Trade Velocity Trade Size Clusters Imbalance Stacked Imbalance Absorption Exhaustion Divergence Orijinal mimaride bu bölüm zaten oldukça iyi.

#### 13. MICROSTRUCTURE ENGINE
**Purpose:** Model MBO/MBP queue and microstructure behavior.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** queue/depth/order-lifetime features.
**Dependencies:** MBO/MBP feed, clock.
**Invariant:** Inference such as possible iceberg must never be stored as confirmed fact.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** MBO/MBP: queue arrival cancel modify replenishment pulling adding spread depth market-order intensity order lifetime queue imbalance Ama buna çok önemli bir kavram ekliyoruz: OBSERVED vs INFERRED Örneğin: Observed: repeated replenishment Inferred: possible iceberg Sistem bunu kesin gerçek olarak yazmayacak. Orijinal ta

#### 14. LIQUIDITY BEHAVIOR ENGINE
**Purpose:** Model dynamic liquidity behavior, not only resting size.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** liquidity behavior state.
**Dependencies:** order book, trades, liquidity map.
**Invariant:** Liquidity quality must account for persistence and cancellations.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Liquidity artık yalnızca: > “orada kaç kontrat var?” değil. Şunlar birlikte hesaplanacak: resting liquidity adding pulling replenishment persistence cancellation rate executed volume stop clusters liquidation clusters liquidity quality Orijinal liquidity map bu seviyeyi zaten hedefliyor.

#### 15. LIQUIDITY CAPACITY ENGINE
**Purpose:** Estimate maximum safe position from available, exit and stress liquidity.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** max safe position, capacity and confidence.
**Dependencies:** liquidity behavior, market impact, volatility.
**Invariant:** Invalid or stale liquidity inputs produce BLOCK/NO TRADE.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bu yeni. Sistem şunu hesaplayacak: > “Bu piyasada kaç adet pozisyon açılabilir?” Yani: available liquidity expected market impact spread depth exit liquidity stress liquidity emergency liquidation capacity üzerinden: Maximum Safe Position hesaplanacak.

#### 16. OPTIONS ENGINE
**Purpose:** Analyze options chains, flow and probable position reconstruction.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** options state and flow probabilities.
**Dependencies:** options feed, instrument master.
**Invariant:** Open/close inference remains probabilistic.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Korunacak: calls puts strikes expirations volume OI premium IV bid/ask trade size Greeks sweeps blocks ve: Position Reconstruction Engine Opening / closing: > kesin bilgi olarak değil, > probability olarak tutulacak. Bu orijinal blueprint'te doğru yaklaşım.

#### 17. GREEKS / GEX ENGINE
**Purpose:** Compute Greeks and GEX regime structures.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** Greeks, GEX, walls, flips, exposures with assumptions/confidence.
**Dependencies:** options data, pricing model.
**Invariant:** Every modelled derivative output declares estimate/assumption/confidence.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Delta Gamma Vega Theta Vanna Charm GEX DEX Gamma Wall Call Wall Put Wall Zero Gamma Gamma Flip Gamma concentration Expiration exposure 0DTE Her model: ESTIMATE ASSUMPTION CONFIDENCE taşımalı.

#### 18. FUTURES / OI ENGINE
**Purpose:** Interpret futures price/OI dynamics and positioning transitions.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** OI regime and positioning features.
**Dependencies:** futures price/OI.
**Invariant:** Contract lineage and roll state are explicit.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Price ↑ OI ↑ Price ↑ OI ↓ Price ↓ OI ↑ Price ↓ OI ↓ ve: new positioning covering liquidation closing OI acceleration korunuyor.

#### 19. BTC DERIVATIVES ENGINE
**Purpose:** Model BTC derivatives relationships across spot, futures and liquidations.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** funding/basis/liquidation/flow state.
**Dependencies:** crypto spot/futures/options sources.
**Invariant:** Venue and timestamp provenance retained.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** BTC için ayrı stack: perpetual OI funding funding acceleration basis futures premium liquidations spot/futures flow exchange flows BTC options IV skew options OI ve özellikle: SPOT ↓ FUTURES ↓ LIQUIDATIONS ilişkisi modellenmeli.

#### 20. VOLATILITY ENGINE
**Purpose:** Measure realized/implied volatility and volatility regime.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** RV/IV/Skew/term structure/expected move.
**Dependencies:** price/options/VIX-like sources.
**Invariant:** Outputs must support strategy, stop and sizing decisions.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** RV IV IVR IV Percentile VIX VVIX Skew Term Structure Expected Move IV/RV Vol compression Vol expansion Fakat çıktısı yalnızca: > VOLATILITY = HIGH olmayacak. Üç karar verecek: STRATEGY SELECTION STOP DISTANCE POSITION SIZE Bu orijinal mimaride de belirtilmişti.

#### 21. MACRO ENGINE
**Purpose:** Model macro state and surprise context.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** macro regime/surprise state.
**Dependencies:** macro data/time-aware calendar.
**Invariant:** Revisions and release availability are preserved.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Fed CPI PPI NFP GDP PMI ISM Retail Sales Unemployment Treasury Yields Real Yields DXY Credit Spreads Fed Expectations Ama yeni: Macro Surprise Engine Expected Actual Previous Revision Surprise Historical Surprise Distribution Asset Reaction üretmeli.

#### 22. NEWS / EVENT ENGINE
**Purpose:** Model news/events with pre/during/post-event state and event risk.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** event state, importance, risk state.
**Dependencies:** news/calendar/macro.
**Invariant:** Event publish/effective timestamps are authoritative.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her event: event publish time effective time importance asset expected actual previous revision taşımalı. Ve: PRE-EVENT EVENT POST-EVENT ayrımı korunmalı. Yeni olarak: Event Risk State NORMAL ELEVATED CRITICAL olmalı.

#### 23. CROSS-ASSET ENGINE
**Purpose:** Model cross-asset lead/lag, beta and correlation regime changes.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** cross-asset state.
**Dependencies:** multi-asset curated data.
**Invariant:** Correlation is never treated as causality.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Sadece correlation değil: lead/lag beta relative strength correlation breakdown regime-conditioned correlation ölçülecek. Orijinal blueprint bunu doğru yönde tanımlıyor. Yeni olarak: Causal Candidate / Lead-Lag Research eklenebilir. Ama **correlation hiçbir zaman causality olarak kabul edilmeyecek.**

#### 24. POSITIONING / COT ENGINE
**Purpose:** Model COT positioning for macro/swing context.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** positioning state and percentiles.
**Dependencies:** CFTC data.
**Invariant:** Not treated as intraday signal unless explicitly certified.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** COT: commercials managed money dealers leveraged funds asset managers net positioning weekly change percentile olarak kalacak. Ama intraday signal değil: > macro/swing context. Orijinal yaklaşım doğru.

#### 25. SESSION ENGINE
**Purpose:** Model trading sessions, openings, OPEX, expiries and time-of-day conditional expectancy.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** session state / time-of-day context.
**Dependencies:** clock, calendar, instrument hours.
**Invariant:** Session definitions are versioned and timezone-aware.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Asia London NY NY Open Opening Range Lunch Power Hour OPEX 0DTE Month-End Quarter-End Friday Holiday Expiration ve: Time-of-Day Conditional Expectancy hesaplanacak.

#### 26. MARKET STATE ENGINE
**Purpose:** Describe the present market state before strategy selection.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** structured market state.
**Dependencies:** feature fabric, derivatives, liquidity, session.
**Invariant:** State and regime are distinct concepts.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burası hâlâ sistemin kalbi. Regime'den önce: > **“Şu anda tam olarak ne oluyor?”** sorusunu cevaplayacak. Örneğin: Structure = Bullish Volatility = High Gamma = Negative Liquidity = Thin Order Flow = Aggressive Buy State = Expansion Orijinal blueprint'teki bu ayrımı koruyorum.

#### 27. REGIME ENGINE
**Purpose:** Classify structural, volatility, gamma, liquidity, microstructure, event, correlation and composite regimes.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** regime states and transition metadata.
**Dependencies:** market state/context.
**Invariant:** Transitioning/uncertain state can invalidate normal expectancy.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Ayrı state'ler: STRUCTURAL VOLATILITY GAMMA LIQUIDITY MICROSTRUCTURE EVENT CORRELATION ve: COMPOSITE REGIME oluşturulacak. Ama burada yeni kritik motor var: REGIME TRANSITION ENGINE Çünkü: RANGE ↓ TRANSITION ↓ BREAKOUT olabilir. Ve transition sırasında normal strategy expectancy geçerli olmayabilir. State: STABLE TRANS

#### 28. CONTEXT ENGINE
**Purpose:** Construct contextual thesis around what/why/where/when and market expectations.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** context snapshot, confirmation/invalidation conditions.
**Dependencies:** market state, regime, events.
**Invariant:** Context does not itself authorize a trade.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Sistem: WHAT? WHY? WHERE? WHEN? sorularını cevaplayacak. Fakat buna: WHAT WOULD INVALIDATE THIS THESIS? WHAT WOULD CONFIRM IT? WHAT IS THE MARKET EXPECTING? WHAT WOULD SURPRISE THE MARKET? sorularını ekliyoruz.

#### 29. LIQUIDITY MAP ENGINE
**Purpose:** Map liquidity above/below price, value, stops, liquidations, resting and gamma zones.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** liquidity map.
**Dependencies:** profile, order book, options, liquidation data.
**Invariant:** Map is descriptive until a setup is validated.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Piyasanın: above price below price inside value outside value stop liquidity liquidation liquidity resting liquidity gamma liquidity haritasını çıkaracak.

### Alpha & Decision
#### 30. SETUP DETECTION ENGINE
**Purpose:** Detect candidate trade setups without treating detection as authorization.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** setup candidates.
**Dependencies:** market state, regime, liquidity, patterns.
**Invariant:** Candidate setup != approved trade.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burada henüz trade yok. Örneğin: Liquidity Sweep yalnızca: > CANDIDATE SETUP dir. Sonra: Sweep + Absorption + Rejection + Structure reversal → valid setup.

#### 31. SETUP QUALITY ENGINE
**Purpose:** Score setup completeness, history, regime compatibility, liquidity and execution feasibility.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** setup quality score/confidence.
**Dependencies:** setup candidates, memory, regime, liquidity, execution models.
**Invariant:** Low-quality or incomplete setups remain ineligible.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni. Her setup: setup quality completeness historical similarity regime compatibility liquidity quality execution feasibility ile puanlanacak.,

#### 32. CONFLICT ENGINE
**Purpose:** Detect conflicts across independent evidence sources.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** conflict level and contributing evidence.
**Dependencies:** market state, derivatives, macro, flow, AI council inputs.
**Invariant:** High conflict can force WAIT/NO TRADE.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bu kesinlikle kalacak. Örneğin: Structure = Bullish Options = Bullish GEX = Bullish Delta = Bearish CVD = Bearish OI = Neutral Macro = Neutral → CONFLICT = HIGH → WAIT Bu mantık çok değerli.

#### 33. ALPHA ENGINE
**Purpose:** Define measurable market advantage separately from strategy implementation.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** alpha assessment.
**Dependencies:** features, state, regime, history.
**Invariant:** Alpha and strategy are separate entities.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burada çok kritik bir mimari değişiklik yapıyorum. **Strategy Library ile Alpha aynı şey olmayacak.** Alpha: > belirli koşullarda piyasada ölçülebilir avantaj Strategy: > o avantajı nasıl trade ettiğimiz. Örneğin: Liquidity reversal bir alpha olabilir. Bunu: Sweep Reversal Absorption Reversal Exhaustion Reversal gibi f

#### 34. ALPHA DEPENDENCY ENGINE
**Purpose:** Identify common underlying alpha factors across strategies.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** alpha dependency graph/buckets.
**Dependencies:** strategy metadata, performance history.
**Invariant:** Correlated strategies share alpha-risk budget.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni ve çok önemli. Sistem: Strategy A Strategy B Strategy C arasındaki ortak kaynak faktörlerini çıkaracak. Örneğin: A → Orderflow reversal B → Absorption reversal C → Liquidity exhaustion ve: Underlying Alpha Factor = Reversal / Liquidity ise bunların toplam riskini tek bir alpha bucket altında değerlendirecek.

#### 35. STRATEGY LIBRARY
**Purpose:** Registry of strategy definitions and implementations.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** versioned strategy specs.
**Dependencies:** alpha library, policy/governance.
**Invariant:** Strategy cannot become active solely by being coded.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Senin mevcut stratejilerin korunuyor: Trend Following Breakout Breakout Retest Liquidity Sweep Reversal Absorption Reversal Exhaustion Reversal VWAP Mean Reversion Value Area Reversion Gamma Reversion Gamma Breakout Options Flow Follow-through Options Flow Divergence OI + Price BTC Liquidation Cascade Cross-Asset Diver

#### 36. STRATEGY ELIGIBILITY ENGINE
**Purpose:** Determine strategy eligibility by regime/context/policy.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** eligible/disabled strategy set.
**Dependencies:** regime, strategy library, certification.
**Invariant:** Ineligible strategy cannot allocate capital.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Regime: Positive Gamma Range Low Vol No major event → Strategy active ama: Negative Gamma High Vol Breakout → disabled. Orijinal mekanizma korunacak.

#### 37. EXPECTANCY ENGINE
**Purpose:** Compute gross and net expectancy including full trading costs.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** gross EV, net EV, components.
**Dependencies:** strategy, outcome history, cost models.
**Invariant:** Net expectancy is the production gating measure.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her setup: win probability average winner average loser average R transaction cost slippage impact regime EV session EV üretecek. Ama artık: GROSS EXPECTANCY ve NET EXPECTANCY ayrılacak. Net expectancy: gross edge - commission - spread - slippage - market impact - funding - financing - other execution costs olacak.

#### 38. PROBABILITY CALIBRATION ENGINE
**Purpose:** Calibrate predicted probabilities against realized frequencies.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** calibration curves, reliability, Brier, drift.
**Dependencies:** outcomes, predictions, regimes.
**Invariant:** Uncalibrated critical probabilities can block trading.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni kritik engine. Sistemin söylediği: Probability = 0.65 gerçek hayatta yaklaşık 65% olay gerçekleşmesine karşılık geliyor mu? Kontrol: calibration curve reliability Brier bucket stability regime calibration probability drift

#### 39. EDGE QUALITY ENGINE
**Purpose:** Separate confidence, probability and EV and measure edge strength/stability/decay/capacity/dependency/half-life.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** edge quality assessment.
**Dependencies:** expectancy, calibration, performance, drift.
**Invariant:** Confidence is never substituted for probability or EV.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burada üç kavram kesinlikle ayrılacak: CONFIDENCE PROBABILITY EXPECTED VALUE Orijinal blueprint'in bu ayrımı korunacak. Ama üstüne: EDGE STRENGTH EDGE STABILITY EDGE DECAY EDGE CAPACITY EDGE DEPENDENCY EDGE HALF-LIFE eklenecek.

#### 40. NO-TRADE ENGINE
**Purpose:** Central admission blocker for data, latency, spread, event, EV, risk, strategy, tail, liquidity and drift failures.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** NO TRADE decision and reason codes.
**Dependencies:** all upstream decision/risk health signals.
**Invariant:** Any hard no-trade condition vetoes execution.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bu engine sistemin en güçlü savunmalarından biri olacak. Şunlardan herhangi biri: DATA INVALID LATENCY HIGH SPREAD EXTREME MAJOR EVENT NO VALID STRATEGY NEGATIVE EV HIGH CONFLICT PORTFOLIO RISK EXCEEDED DAILY LOSS LIMIT STRATEGY DEGRADATION TAIL RISK EXTREME REGIME TRANSITION LIQUIDITY INSUFFICIENT PROBABILITY UNCALIBR

#### 41. SIGNAL AUTHORIZATION ENGINE
**Purpose:** Authorize signals as LONG/SHORT/WAIT/NO TRADE before risk/capital.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** signal authorization.
**Dependencies:** edge, conflict, no-trade, thesis.
**Invariant:** Signal is not capital.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni. Burada sonuç: LONG SHORT WAIT NO TRADE olabilir. Ama signal henüz sermaye tahsisi değildir.

#### 42. TRADE THESIS ENGINE
**Purpose:** Create explicit trade thesis and invalidation path.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** thesis object.
**Dependencies:** setup, context, strategy, risk.
**Invariant:** Invalidation must be actionable and auditable.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her approved candidate için sistem: THESIS ENTRY REASON EXPECTED PATH INVALIDATION TARGET TIME HORIZON CATALYST RISK üretecek. Bu daha sonra attribution için kullanılacak.

#### 85. DECISION COUNCIL
**Purpose:** Combine independent evidence sources using independence/correlation/confidence/evidence quality rather than majority vote.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** council assessment.
**Dependencies:** structure, order flow, liquidity, derivatives, macro, cross-asset, volatility, AI.
**Invariant:** Correlated models do not count as independent votes.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Birden fazla bağımsız değerlendirme: Structure Order Flow Liquidity Derivatives Macro Cross Asset Volatility AI verecek. Ama majority vote mantığı kullanılmamalı. Örneğin: 7 model BUY olması tek başına BUY anlamına gelmemeli. Council önce: independence correlation confidence evidence quality değerlendirmeli.

#### 86. EXECUTIVE DECISION ENGINE
**Purpose:** Produce final LONG/SHORT/WAIT/NO TRADE decision with full decision context.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** executive decision.
**Dependencies:** council, edge, risk admission state.
**Invariant:** Decision is immutable after authorization.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Nihai karar: LONG SHORT WAIT NO TRADE olacak. Fakat artık her kararın yanında: probability net EV risk budget capital allocation confidence data quality regime strategy expected holding period invalidation execution mode bulunacak.

#### 87. DECISION CONSUMER
**Purpose:** Consume authorized decisions and drive downstream persistence/execution/outcome chain.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** consumer actions and acknowledgements.
**Dependencies:** decision ledger, orchestration events.
**Invariant:** Every decision must have a traceable consumer path.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Ve burada önceki ALADDIN çalışmalarımızdaki çok önemli prensip devreye giriyor: ENGINE ↓ CALLER ↓ ORCHESTRATOR ↓ DECISION ↓ SQL WRITE ↓ DECISION CONSUMER ↓ OUTCOME ↓ FEEDBACK ↓ LEARNING Bu zincir **tasarımın zorunlu invariant'ı** olmalı. Bir engine'in çalışmış olması artık “özellik tamamlandı” sayılmayacak.

### Risk & Portfolio
#### 43. RISK ENGINE
**Purpose:** Deterministic trade-level risk sizing and stop computation.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** risk decision / size.
**Dependencies:** policy, account, volatility, liquidity, correlation.
**Invariant:** AI cannot override risk policy.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burada AI'nin yetkisi bitiyor. Risk: > **deterministic** olacak. Orijinal yapı korunuyor: Stop Structure Liquidity Volatility Order Flow Time Event ve: Account ↓ Risk Budget ↓ Stop Distance ↓ Contract Value ↓ Volatility Adjustment ↓ Correlation Adjustment ↓ Portfolio Adjustment ↓ Final Size

#### 44. RISK BUDGET HIERARCHY ENGINE
**Purpose:** Cascade total capital limits into strategy/asset/factor/trade risk ceilings.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** risk budgets.
**Dependencies:** policy, portfolio state.
**Invariant:** Every lower layer is bounded by an upper layer ceiling.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni en kritik engine'lerden biri. TOTAL CAPITAL ↓ SURVIVAL CAPITAL ↓ MAX PORTFOLIO LOSS ↓ MAX DAILY LOSS ↓ MAX WEEKLY LOSS ↓ STRATEGY RISK BUDGET ↓ ASSET RISK BUDGET ↓ FACTOR RISK BUDGET ↓ TRADE RISK BUDGET Her üst katman alt katmana ceiling koyacak.

#### 45. DRAWDOWN RESPONSE ENGINE
**Purpose:** Reduce risk automatically across drawdown states and halt when required.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** drawdown state and risk multipliers.
**Dependencies:** P&L, risk budget, policy.
**Invariant:** Drawdown response is deterministic.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Sistem zarara girdiğinde sadece: > DD = -X% yazmayacak. Davranacak. NORMAL ↓ CAUTION ↓ DEFENSIVE ↓ CRITICAL ↓ HALT ve risk bütçesini otomatik olarak düşürecek. Bu, risk yönetiminin “ölçen” değil **aktif sermaye koruyan** hale gelmesini sağlar.

#### 46. LOSS DISTRIBUTION ENGINE
**Purpose:** Model loss distribution shape, clustering and extreme losses.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** loss distribution statistics.
**Dependencies:** outcomes.
**Invariant:** Tail-aware sizing uses the empirical distribution where available.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Artık yalnızca: Average Winner Average Loser yok. Dağılım: mean median variance skew kurtosis tail percentiles loss clustering win clustering consecutive losses extreme loss olarak tutulacak.

#### 47. RISK OF RUIN ENGINE
**Purpose:** Estimate probability of critical drawdown, capital impairment and ruin.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** risk of ruin metrics.
**Dependencies:** loss distribution, equity, frequency, correlation.
**Invariant:** Positive EV does not override unacceptable ruin risk.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni. Sistem: current equity risk per trade win probability loss distribution trade frequency correlation tail behavior drawdown kullanarak: Probability of critical drawdown Probability of ruin Probability of capital impairment hesaplayacak. Edge pozitif olsa bile ruin riski kabul edilemezse: NO TRADE

#### 48. TAIL RISK ENGINE
**Purpose:** Model tail loss using VaR/ES/stress/gap/liquidity/forced liquidation/jump risk.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** tail risk state.
**Dependencies:** portfolio, market, liquidity, stress models.
**Invariant:** Tail risk can veto capital allocation.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burası önceki mimaride en büyük eksiklerden biriydi. VaR Expected Shortfall Stress Loss Gap Risk Liquidity-adjusted Loss Forced Liquidation Loss Correlation Shock Volatility Shock Jump Risk hesaplanacak. Basel'in piyasa riski framework'ünde VaR yerine stressed Expected Shortfall'a geçiş ve illiquidity riskinin ayrıca d

#### 49. STRESS SCENARIO ENGINE
**Purpose:** Run predefined adverse scenarios and quantify P&L/margin/liquidation/recovery impact.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** scenario results.
**Dependencies:** portfolio/execution/market snapshots.
**Invariant:** Scenarios are deterministic for fixed inputs.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Hazır scenario library: VOLATILITY SHOCK LIQUIDITY SHOCK CORRELATION SHOCK GAP SHOCK RATE SHOCK DXY SHOCK BTC CASCADE OPTIONS GAMMA SHOCK SPREAD EXPANSION ORDER BOOK COLLAPSE EXECUTION FAILURE DATA OUTAGE BROKER OUTAGE Her scenario: P&L margin liquidation ES portfolio heat recovery time üretecek. Bu yaklaşım, Basel'in 

#### 50. MARGIN ENGINE
**Purpose:** Model margin, buying power and liquidation distance.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** margin state.
**Dependencies:** account, venue rules, positions, stress.
**Invariant:** Margin shock can reduce or block allocation.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** initial margin maintenance margin buying power leverage concentration margin utilization korunacak. Buna: stress margin liquidation distance margin buffer margin shock eklenecek.

#### 51. PORTFOLIO RISK ENGINE
**Purpose:** Aggregate market, factor, liquidity, volatility, event, correlation, model and execution risk.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** portfolio risk state.
**Dependencies:** positions, risk models, capital.
**Invariant:** Portfolio constraints supersede individual trade attractiveness.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Artık: correlation beta factor exposure USD exposure vol exposure tail risk var. Ama bunlar ayrı risk buckets olarak tutulacak: MARKET RISK FACTOR RISK LIQUIDITY RISK VOLATILITY RISK EVENT RISK CORRELATION RISK MODEL RISK EXECUTION RISK

#### 52. CAPITAL ALLOCATION ENGINE
**Purpose:** Allocate safe capital using net EV, probability, risk, correlation, liquidity, capacity and strategy health.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** capital allocation.
**Dependencies:** risk, portfolio, opportunity set.
**Invariant:** Signal approval never implies full capital allocation.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bu, bütün mimarinin en önemli yeni parçası. Trade approved olması: > sermaye hak ettiği anlamına gelmez. Capital Allocator: Expected Net EV Probability Confidence Drawdown state Portfolio risk Factor risk Correlation Liquidity capacity Tail risk Execution quality Strategy quality Strategy decay kullanarak: Optimal / Sa

#### 53. CAPITAL COMPETITION ENGINE
**Purpose:** Rank simultaneous opportunities for scarce capital.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** capital competition ranking.
**Dependencies:** opportunity set, portfolio context.
**Invariant:** Highest EV is not necessarily highest allocation.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Aynı anda 15 fırsat varsa sistem: > hepsini açmayacak. Bunları birbirleriyle yarıştıracak. Örneğin: Opportunity A EV +0.41R Risk 0.30 Opportunity B EV +0.28R Risk 0.10 Opportunity C EV +0.65R Risk 0.80 Fakat C'nin portföy correlation'ı yüksekse B daha iyi sermaye kullanımı olabilir. Bu yüzden: > **highest EV ≠ highest 

#### 54. PORTFOLIO OPTIMIZATION ENGINE
**Purpose:** Optimize risk-adjusted capital efficiency without maximizing leverage.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** portfolio allocation proposal.
**Dependencies:** expected returns, risks, correlations, factors, tail, capacity.
**Invariant:** Optimization is constrained by policy and survival capital.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Burada: expected return risk correlation factor exposure tail risk liquidity capacity birlikte değerlendirilecek. Ama sistemin amacı: > matematiksel olarak maksimum leverage değil. Amaç: > **risk-adjusted capital efficiency.**

### Execution & Position
#### 55. EXECUTION APPROVAL ENGINE
**Purpose:** Require explicit execution approval after signal, risk and capital approval.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** execution authorization.
**Dependencies:** signal/risk/capital/venue health.
**Invariant:** Execution approval is a separate gate.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Artık: SIGNAL APPROVED RISK APPROVED CAPITAL APPROVED olmuş olsa bile: EXECUTION APPROVED? sorulacak.

#### 56. EXECUTION ENGINE
**Purpose:** Translate authorized intent into live order management.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** order intents, order states, fills.
**Dependencies:** execution adapter, market data, policy.
**Invariant:** No raw order path can bypass authorization.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal: Market Limit Passive Aggressive Order Routing Cancel/Replace Partial Fill Slippage Latency Fill Probability Market Impact korunacak. Yeni: ALPHA HALF-LIFE ENGINE ekleniyor. Çünkü sinyal oluştuğunda edge'in kaç milisaniye/saniye/dakika yaşadığı execution kararının parçası olacak.

#### 57. TRANSACTION COST ENGINE
**Purpose:** Calculate all transaction costs for net expectancy and attribution.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** cost breakdown.
**Dependencies:** venue rules, fills, market conditions.
**Invariant:** Cost model version is recorded with every decision.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her trade: commission spread slippage impact funding roll cost financing execution cost ile netleştirilecek. Bu engine expectancy'nin **önünde** çalışmalı.

#### 58. MARKET IMPACT ENGINE
**Purpose:** Model expected impact/slippage as a function of size and liquidity.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** impact/slippage estimates.
**Dependencies:** order book, size, venue, liquidity.
**Invariant:** Capacity and execution feasibility must reflect impact.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Pozisyon büyüklüğü: size → expected impact → expected slippage → exit impact şeklinde modellenmeli. Böylece: > “Teoride kârlı” ile > “bu sermaye büyüklüğüyle uygulanabilir” ayrılacak.

#### 59. RECONCILIATION ENGINE
**Purpose:** Compare internal and external broker/venue state and block on mismatch.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** reconciliation result.
**Dependencies:** orders, fills, positions, broker state.
**Invariant:** Mismatch can force system halt.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal örneği aynen koruyorum: BOT THINKS: +2 GC BROKER: +1 GC → SYSTEM HALT Bu kesinlikle kaldırılmayacak.

#### 60. FAILSAFE / RESILIENCE ENGINE
**Purpose:** Fail safe under feed/broker/exchange/data/clock/order/position anomalies.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** fault state, cancel/freeze/recovery actions.
**Dependencies:** health, execution, reconciliation.
**Invariant:** Failure defaults to safe state.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** feed lost broker lost exchange disconnected stale data clock drift duplicate orders position mismatch runaway order abnormal fill → CANCEL FREEZE RECONCILE ALERT RECOVER Orijinal yapı korunuyor. Yeni olarak: Recovery State Machine FAULT ↓ ISOLATED ↓ SAFE ↓ RECONCILING ↓ VALIDATED ↓ RECOVERY ↓ RESUME

#### 61. POSITION MANAGER
**Purpose:** Manage position lifecycle including TP, runner, trailing and thesis invalidation.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** position management actions.
**Dependencies:** position, thesis, market state, risk.
**Invariant:** Thesis invalidation may force exit.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Entry Management TP1 TP2 Runner Trailing Exit ve en önemlisi: THESIS INVALIDATION → EXIT Orijinal yapı korunuyor.

#### 62. TRADE STATE MACHINE
**Purpose:** Enforce complete trade lifecycle state machine.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** trade state transitions.
**Dependencies:** order/fill/position/outcome.
**Invariant:** Only valid state transitions are allowed.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Korunuyor: WATCHING CANDIDATE VALIDATING APPROVED ENTRY_PENDING PARTIALLY_FILLED OPEN MANAGING EXIT_PENDING CLOSED ANALYZING Buna: REJECTED CANCELLED HALTED RECONCILIATION_REQUIRED eklenmeli.

#### 63. IMMUTABLE DECISION LEDGER
**Purpose:** Immutable decision ledger for full decision reconstruction.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** ledger records.
**Dependencies:** decision snapshot, versioning, lineage.
**Invariant:** Ledger entries are append-only.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni. Her kararın değiştirilemez kaydı: market snapshot features regime setup strategy probability EV risk capital decision execution model version data version policy version olacak. Böylece: > “Bu trade neden açıldı?” sorusunun tam cevabı yıllar sonra bile çıkarılabilir.

#### 64. JOURNAL ENGINE
**Purpose:** Maintain pre-decision, decision, execution, position, exit and post-trade journal states.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** journal snapshots.
**Dependencies:** decision/execution/position/outcome.
**Invariant:** Journal is append-only and version-linked.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal journal korunuyor. Ama sadece trade snapshot değil: PRE-DECISION STATE DECISION STATE EXECUTION STATE POSITION STATE EXIT STATE POST-TRADE STATE ayrı tutulacak.

### Outcome, Performance & Learning
#### 65. OUTCOME ENGINE
**Purpose:** Calculate realized trade outcomes including P&L, R, MFE, MAE, duration, slippage and thesis result.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** trade outcome.
**Dependencies:** fills, positions, market path, thesis.
**Invariant:** Outcome is required before learning.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bu, önceki ALADDIN çalışmalarımızda özellikle eksik kalan kritik zincirlerden biriydi. Her trade için: realized P&L R MFE MAE duration slippage execution quality thesis outcome oluşturulacak.

#### 66. ATTRIBUTION ENGINE
**Purpose:** Attribute positive and negative P&L contribution across market factors and execution.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** attribution result.
**Dependencies:** outcome, features, decision lineage.
**Invariant:** Attribution must separate alpha from execution/timing/cost.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Trade neden kazandı? Structure Order Flow Liquidity Options GEX OI Macro Cross Asset Execution katkıları ölçülecek. Orijinal blueprint'te bu zaten doğru tanımlanmış. Ama artık: NEGATIVE ATTRIBUTION da tutulacak. Yani: > hangi feature trade'i yanlış yöne itti? de ölçülecek.

#### 67. PERFORMANCE ENGINE
**Purpose:** Measure comprehensive performance and risk-adjusted returns.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** performance snapshots.
**Dependencies:** outcomes, portfolio state, costs.
**Invariant:** Performance is segmented by asset, strategy, regime and time.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Sadece: win rate profit yok. Expectancy PF Average R Average Winner Average Loser Max DD Sharpe Sortino Calmar Recovery Factor MAE MFE Consecutive Losses Frequency Time in Market Slippage Commission Tail Risk korunacak. Ek olarak: Net Expectancy Capacity Turnover Risk-adjusted return Tail-adjusted return olacak.

#### 68. PERFORMANCE DECOMPOSITION ENGINE
**Purpose:** Decompose P&L into alpha, selection, sizing, execution, timing and cost.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** performance decomposition.
**Dependencies:** outcome, attribution, capital, execution.
**Invariant:** Decomposition components must reconcile to total P&L within accounting tolerance.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Toplam P&L: alpha + selection + sizing + execution + timing + cost şeklinde ayrılmalı. Bu sayede: > Sistem gerçekten edge'den mi kazanıyor? yoksa: > Sadece iyi execution sayesinde mi? anlaşılacak.

#### 69. STRATEGY DECAY ENGINE
**Purpose:** Detect strategy degradation and apply lifecycle states.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** strategy health state.
**Dependencies:** performance, EV, drift, calibration.
**Invariant:** Degrading strategies lose risk budget before disablement.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal: Expected EV +0.35R Realized EV -0.10R → degradation → risk reduction mantığı korunuyor. Ama yeni lifecycle: NORMAL WATCH DEGRADING DEFENSIVE PROBATION DISABLED RESEARCH olmalı.

#### 70. MODEL / FEATURE DRIFT ENGINE
**Purpose:** Detect feature/model/data/execution drift.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** drift metrics and alerts.
**Dependencies:** feature distributions, model outputs, vendor metadata, runtime telemetry.
**Invariant:** Critical drift can block or downgrade strategies.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** feature drift distribution shift regime shift calibration drift vendor changes data methodology changes model degradation korunacak. Yeni olarak: feature importance drift input missingness drift latency drift execution drift eklensin.

#### 71. STRATEGY CORRELATION + ALPHA DEPENDENCY ENGINE
**Purpose:** Measure strategy correlation and underlying alpha dependency.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** correlation/dependency matrices.
**Dependencies:** strategy outcomes, factor metadata.
**Invariant:** Portfolio risk must account for shared alpha exposure.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal strateji correlation korunacak. Ama artık iki seviyeli: STRATEGY CORRELATION ve: ALPHA FACTOR DEPENDENCY olacak.

#### 72. RESEARCH TRIAL REGISTRY
**Purpose:** Register every research experiment to control multiple testing and selection bias.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** research trial records.
**Dependencies:** research inputs, dataset versions.
**Invariant:** No unregistered production-affecting research result.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni ve **zorunlu**. Her araştırma: Research ID Hypothesis Dataset Time period Features Parameters Strategies tested Number of trials Selection rule Results kaydedilecek. Bunun amacı: > “Başarılı sonucu bulana kadar binlerce şey denedim ama sadece başarılı olanı hatırlıyorum.” problemini ortadan kaldırmak. Multiple tes

#### 88. FEEDBACK ENGINE
**Purpose:** Classify outcomes and propagate feedback to strategy, feature, regime, execution, risk and capital layers.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** feedback events.
**Dependencies:** outcome, attribution, performance.
**Invariant:** Feedback does not alter production directly.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Outcome: SUCCESS FAILURE PARTIAL INVALIDATION EXECUTION FAILURE DATA FAILURE olarak sınıflandırılacak. Sonra: strategy feature regime execution risk capital allocation katmanlarına geri besleme yapılacak.

#### 89. LEARNING GOVERNOR
**Purpose:** Govern the learning loop from observation through certification and deployment.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** learning proposals/status.
**Dependencies:** feedback, research, validation, certification.
**Invariant:** Deployment is gated and versioned.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Learning otomatik olarak canlı sisteme geçemeyecek. Döngü: OBSERVE ↓ DETECT ↓ HYPOTHESIZE ↓ RESEARCH ↓ VALIDATE ↓ CERTIFY ↓ PAPER ↓ PROBATION ↓ DEPLOY olacak. Bu ayrım çok önemli; aksi halde sistem kendi geçmiş davranışına aşırı uyum sağlayarak bir feedback loop içinde overfit olabilir.

### Research & Certification
#### 73. BACKTEST ENGINE
**Purpose:** Run in-sample, out-of-sample, walk-forward, purge/embargo, Monte Carlo and stress validation.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** backtest result bundle.
**Dependencies:** dataset, strategy version, cost model.
**Invariant:** Future information is prohibited.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Her strategy: in-sample out-of-sample walk-forward purged validation embargo Monte Carlo stress ile test edilecek. Ama yeni ek: CPCV **Combinatorial Purged Cross-Validation** olmalı. 2024 tarihli bir karşılaştırmalı çalışmada CPCV'nin PBO/DSR açısından geleneksel walk-forward yaklaşımlarına göre daha güçlü overfitting 

#### 74. MARKET REPLAY ENGINE
**Purpose:** Replay the real runtime against historical data with historical availability, latency, execution and risk rules.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** replay run and reproducible results.
**Dependencies:** raw/curated data, runtime version.
**Invariant:** Replay must be deterministic for fixed inputs/version.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal MBO replay sistemi korunuyor: > geçmişte sistem sadece o anda sahip olduğu bilgiyle hareket edecek. Buna: same latency same data availability same execution rules same slippage model same risk engine eklenmeli. Yani replay: > gerçek sistemin geçmişteki simülasyonu olmalı.

#### 75. OVERFITTING ENGINE
**Purpose:** Detect backtest overfitting, PBO, DSR, stability and regime robustness issues.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** overfitting assessment.
**Dependencies:** research registry, validation results.
**Invariant:** Single best backtest cannot certify a strategy.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Korunacak: data snooping multiple testing parameter overfit feature redundancy selection bias look-ahead survivorship bias backtest overfitting Yeni: PBO DSR Probability Calibration Parameter Stability Feature Stability Regime Robustness

#### 76. STATISTICAL VALIDATION ENGINE
**Purpose:** Perform statistical validation across confidence intervals, bootstrap, Monte Carlo, stationarity and dependence assumptions.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** statistical validation result.
**Dependencies:** backtest/replay results.
**Invariant:** Insufficient sample size invalidates certification.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni bağımsız katman. Kontrol: confidence intervals bootstrap Monte Carlo distribution stability sample size adequacy statistical significance multiple testing stationarity assumptions autocorrelation heteroskedasticity Çünkü: > “Sharpe 2.8 çıktı” tek başına hiçbir şey kanıtlamaz.

#### 77. STRATEGY CERTIFICATION ENGINE
**Purpose:** Move strategy through research/candidate/validated/robust/paper/micro/probation/production gates.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** certification status.
**Dependencies:** all validation evidence, governance approval.
**Invariant:** Production activation requires objective gate pass.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Bu, bence yeni mimarinin **en önemli bileşenlerinden biri**. Bir strategy: RESEARCH ↓ CANDIDATE ↓ VALIDATED ↓ ROBUST ↓ PAPER ↓ MICRO-LIVE ↓ PROBATION ↓ PRODUCTION şeklinde ilerleyecek. Ve production'a geçebilmek için objektif kriterleri geçmek zorunda.

#### 78. LIVE SHADOW ENGINE
**Purpose:** Run live market signals/decisions with virtual execution.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** shadow outcomes.
**Dependencies:** live feeds, decision runtime, virtual execution.
**Invariant:** Shadow is non-capitalized but production-like.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Gerçek para kullanmadan: LIVE MARKET ↓ REAL-TIME SIGNAL ↓ REAL-TIME DECISION ↓ VIRTUAL EXECUTION çalışacak. Amaç: > Backtest ile canlı veri akışı arasındaki farkı bulmak.

#### 79. PAPER TRADING ENGINE
**Purpose:** Test paper execution realism, latency, slippage, fill probability, reconciliation and compliance.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** paper performance and reliability report.
**Dependencies:** live market, virtual execution.
**Invariant:** Paper must validate operations as well as P&L.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Orijinal roadmap'teki paper phase korunacak. Ama paper trading sadece P&L test etmeyecek: signal latency execution realism slippage fill probability risk compliance reconciliation system reliability de ölçülecek.

#### 80. MICRO LIVE / PROBATION ENGINE
**Purpose:** Control micro-live/probation promotion and compare expected vs realized behavior.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** probation state and gate metrics.
**Dependencies:** paper/shadow/micro outcomes, policy.
**Invariant:** Production promotion requires all gates.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Production'a doğrudan geçilmeyecek. PAPER ↓ MICRO ↓ PROBATION ↓ PRODUCTION Her aşamada canlı sonuç: EXPECTED vs REALIZED karşılaştırılacak.

#### 81. CAPACITY ENGINE
**Purpose:** Measure maximum strategy capacity at different capital scales.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** capacity curve and recommended capital range.
**Dependencies:** liquidity, impact, execution, size.
**Invariant:** Capacity is regime and venue dependent.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Yeni. Strateji teorik olarak: EV +0.40R olabilir. Ama: capital = $10k ile başka, capital = $10M ile başka sonuç verebilir. Bu yüzden: maximum capacity liquidity capacity impact capacity execution capacity ölçülecek.

#### 82. MODEL RISK ENGINE
**Purpose:** Track model assumptions, limitations, failure modes, validation, monitoring and decommission lifecycle.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** model risk register.
**Dependencies:** model registry, validation, drift.
**Invariant:** Models may be disabled without changing historical records.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Sistem kendi modelinin de yanlış olabileceğini kabul edecek. MODEL ASSUMPTION MODEL LIMITATION MODEL FAILURE MODE MODEL VALIDATION MODEL MONITORING MODEL DECOMMISSION AI tarafında NIST'in yönetişim, ölçüm, yönetim ve yaşam döngüsü yaklaşımı da tam burada kullanılabilir. NIST AI RMF, risk yönetiminin tasarım/planlamadan

#### 83. AI RESEARCH ENGINE
**Purpose:** Use AI for interpretation, research, hypothesis generation, historical query, strategy comparison and post-trade analysis.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** structured AI research artifacts.
**Dependencies:** structured platform memory/context.
**Invariant:** AI research cannot directly modify production policy/code.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** AI ancak bundan sonra geliyor. AI: market interpretation context interpretation hypothesis generation research feature investigation historical query strategy comparison trade thesis post-trade analysis anomaly detection yapabilir.

#### 84. AI AUTHORITY ENGINE
**Purpose:** Define AI authority levels from analysis to full autonomy while enforcing hard prohibitions.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** AI authority decision.
**Dependencies:** AI outputs, policy.
**Invariant:** AI never changes risk ceilings, kill switches or reconciliation policy.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Seviyeler: LEVEL 0 ANALYSIS LEVEL 1 SIGNAL SUGGESTION LEVEL 2 QUANT VALIDATED RECOMMENDATION LEVEL 3 EXECUTION RECOMMENDATION LEVEL 4 LIMITED AUTOMATION LEVEL 5 FULL AUTONOMY Orijinal mimari bu yaklaşımı zaten içeriyordu. Ama benim tasarımımda: LEVEL 5'e bile AI şu haklara sahip olmayacak: risk limit değiştir stop geni

### Observability & Operations
#### 90. OBSERVABILITY ENGINE
**Purpose:** Measure health, latency, throughput, errors, staleness, outputs, confidence and dependencies per engine.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** telemetry metrics/traces.
**Dependencies:** runtime instrumentation.
**Invariant:** Critical metrics have alert thresholds.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Sistemin kendisini izlemesi gerekiyor. Her engine: health latency throughput error rate stale rate output rate confidence dependency status raporlayacak.

#### 91. SYSTEM HEALTH ENGINE
**Purpose:** Aggregate global health and trading admission state.
**Inputs:** Upstream typed contracts and required source data for this domain; exact schema is versioned in `contracts/`.
**Outputs:** HEALTHY/DEGRADED/WARNING/CRITICAL/HALTED.
**Dependencies:** engine health, dependencies, fail-safe.
**Invariant:** Critical health can disable new trades.
**Failure policy:** On trading-critical failure, emit a typed failure reason, preserve diagnostics, and fail closed unless an explicitly approved fallback is valid.
**Persistence:** Versioned PostgreSQL record for operational state; immutable snapshot/ledger where decision-bearing.
**Observability:** latency, throughput, error rate, stale rate, output rate and dependency state; domain-specific metrics as defined in implementation telemetry.
**Acceptance:** Unit + contract + integration + replay compatibility tests pass; no unresolved critical invariant violations.
**Historical rationale (non-normative):** Global state: HEALTHY DEGRADED WARNING CRITICAL HALTED olacak. Örneğin: Data Healthy Risk Healthy Execution Degraded ise sistem yeni trade açmayabilir.

## 18. Operational Subsystems (Implementation-Added Contract)
### O01. System Supervisor
**Purpose:** Own process lifecycle, service dependency ordering and runtime state transitions.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O02. Watchdog
**Purpose:** Detect process/service/DB/feed/broker/clock/resource faults and initiate safe recovery.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O03. Startup/Bootstrap Manager
**Purpose:** Perform deterministic readiness checks before trading is enabled.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O04. Shutdown Manager
**Purpose:** Stop new trading first, then drain/close controlled services while preserving state.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O05. Host Resource Manager
**Purpose:** Protect the trading critical path from game and research resource contention.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O06. Connectivity Manager
**Purpose:** Track network/venue/AI/notification connectivity and route safe degradation.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O07. Secret/Credential Manager
**Purpose:** Keep API/broker credentials out of source control and enforce least privilege.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O08. Notification Gateway
**Purpose:** Send prioritized mobile alerts with deduplication and offline buffering.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O09. Mobile Control Gateway
**Purpose:** Expose authenticated read-only and constrained control actions.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O10. Job Scheduler
**Purpose:** Run daily/weekly/monthly research, performance and maintenance jobs.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O11. Backup/Recovery Manager
**Purpose:** Create, verify and periodically restore DB/data/config backups.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O12. Release Manager
**Purpose:** Bind code/data/model/policy/execution versions into deployable releases with rollback.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O13. Model Registry
**Purpose:** Register model artifacts, versions, validation, drift and approval state.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O14. Feature Registry
**Purpose:** Register feature definitions, versions, lineage and deprecation state.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O15. Cost/Usage Governor
**Purpose:** Track data, AI and infrastructure spend and enforce budget policies.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O16. Champion/Challenger Manager
**Purpose:** Compare certified production candidates without uncontrolled substitution.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O17. Incident Manager
**Purpose:** Track critical operational incidents and link them to audit/recovery records.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.
### O18. Configuration Governor
**Purpose:** Version, validate and lock runtime configuration by environment.
**Invariant:** operational uncertainty cannot authorize a trade; runtime control remains fail-closed.

## 19. Repository Contract
```text
trading_system/
├─ app/
├─ contracts/
├─ domains/
├─ infrastructure/
├─ runtime/
├─ research/
├─ migrations/
├─ configs/
├─ scripts/
├─ tests/
├─ data/
└─ docs/
```

## 20. Implementation Sequence (Locked)
00. Architecture/contract freeze
01. Repository/runtime foundation
02. PostgreSQL/migrations
03. Event bus/contracts
04. Data source registry/connectors
05. RAW/CURATED/FEATURE lake
06. Instrument + temporal truth
07. Feature fabric
08. Market state + regime
09. Liquidity/microstructure/derivatives
10. Setup/alpha/strategy/decision
11. Expectancy/probability/edge/no-trade
12. Risk/tail/portfolio
13. Capital allocation
14. Execution/reconciliation/position
15. Outcome/attribution/performance
16. Drift/research/validation
17. Memory/learning governor
18. AI gateway/governance
19. Watchdog/host/notification/mobile
20. Observability/backup/deployment
21. Full replay
22. Shadow
23. Paper
24. Micro
25. Probation
26. Production

## 21. Cost Control Contract
All external spend must be attributable by vendor, dataset, model, tokens/requests, storage and environment. AI and data vendors receive daily/monthly budgets; exceeding a budget triggers throttling or safe fallback, never silent uncontrolled spend.

## 22. Final Freeze Statement
This V2.2.2 contract is the implementation baseline. New ideas discovered during coding are not to be inserted directly into production code. They are entered as change requests, classified as bug/contract correction/enhancement, reviewed for dependency impact, versioned, tested, and incorporated into V1.x/V2 as appropriate.


---

# 23. V2.2 NORMATIVE AMENDMENT — PROFITABILITY CERTIFICATION

## 23.1 Authority and precedence

This section is **normative** and overrides any earlier V2.1 wording wherever the two conflict. V2.1 architecture, domain topology, technology decisions, governance model, event model, lineage model, failure philosophy and implementation sequencing remain preserved unless explicitly overridden by a V2.2 rule below.

The V2.2 objective is not to redesign the system. It closes profitability-critical ambiguity by converting previously qualitative requirements into:

- exact contract families;
- explicit required data sufficiency rules;
- deterministic decision invariants;
- uncertainty-aware expectancy rules;
- execution/fill realism requirements;
- strategy-specific eligibility policies;
- adaptive market-change controls;
- adversarial certification questions;
- evidence requirements;
- production-blocking gates.

**Critical principle:** a requirement is not implementation-complete because the document mentions it. A requirement is complete only when the contract, policy, test and evidence required by this document exist and are linked in the traceability matrix.

## 23.2 Readiness is now a five-state model

V2.2.2 supersedes the prior V2.1 interpretation of live authorization. The five states are:

`R0 ARCHITECTURE READY`
→ `R1 CODE READY`
→ `R2 TEST READY`
→ `R3 OPERATIONALLY LIVE-READY`
→ `R4 PROFITABILITY CERTIFIED`

`R3 OPERATIONALLY LIVE-READY` means that the runtime, Market Profile, external entitlements, numerical policy set, venue/execution integration, operational controls and required non-performance evidence are complete. **R3 never grants trading authority.**

`R4 PROFITABILITY CERTIFIED` means that a specific strategy/market-profile/release has additionally passed the profitability, statistical, execution-realism, capacity, shadow/paper/micro/probation and adversarial evidence gates required by this contract for live operation under the tested conditions.

`R4 PROFITABILITY CERTIFIED` does **not** mean guaranteed profit.

No release may claim `R4` without:

1. certified market profile;
2. certified data sufficiency;
3. point-in-time verified dataset;
4. deterministic replay;
5. leakage/overfitting validation;
6. calibrated probability where probability is used;
7. uncertainty-aware net expectancy;
8. realistic execution simulation;
9. portfolio/risk/capacity validation;
10. live shadow/paper/micro/probation evidence;
11. complete decision-to-outcome lineage;
12. adversarial exam pass.

## 23.3 Profitability certification unit

The certification unit is not merely a strategy name.

The canonical unit is:

```text
CERTIFICATION_SCOPE =
    market_profile
    + instrument_universe
    + data_profile
    + strategy_version
    + feature_set_version
    + model_version
    + parameter_version
    + cost_model_version
    + execution_model_version
    + risk_policy_version
    + capital_policy_version
    + time_window
```

A strategy certified for one scope is not automatically certified for another.

## 23.4 Universal decision invariant

No production trade is permitted unless:

```text
DATA_SUFFICIENT
AND DATA_VALID
AND DATA_POINT_IN_TIME_VALID
AND FEATURE_VALID
AND REGIME_VALID
AND STRATEGY_ELIGIBLE
AND ALPHA_EVIDENCE_VALID
AND PROBABILITY_VALID_IF_REQUIRED
AND NET_EV_LOWER_BOUND_ABOVE_EDGE_FLOOR
AND EXECUTION_FEASIBLE
AND CAPACITY_VALID
AND PORTFOLIO_RISK_VALID
AND RISK_OF_RUIN_VALID
AND CAPITAL_VALID
AND POSITION_STATE_KNOWN
AND RECONCILIATION_VALID
AND SYSTEM_HEALTH_VALID
AND CERTIFICATION_SCOPE_MATCH
```

Any critical predicate that is `UNKNOWN` is treated as `FAIL`.

---

# 24. STRATEGY → DATA SUFFICIENCY CONTRACT

## 24.1 Purpose

Prevent a strategy from running merely because some required data exists. A strategy may execute only when **all data required for the strategy's specific mechanism, feature set, target, risk model and execution model is available with certified quality**.

## 24.2 Required strategy data profile

Every strategy definition MUST reference a versioned `StrategyDataProfile` containing:

```yaml
strategy_id
strategy_version
market_profile_id
required_data_tiers
required_sources
required_features
required_feature_versions
required_timeframes
required_market_fields
required_venue_fields
required_derivative_fields
required_book_depth
requires_l1
requires_l2
requires_l3
requires_mbo
requires_trade_prints
requires_quote_prints
requires_open_interest
requires_funding
requires_options_surface
requires_macro_vintage
requires_fundamental_vintage
minimum_history
minimum_coverage
maximum_missingness
maximum_staleness
maximum_sequence_gap_rate
maximum_out_of_order_rate
maximum_clock_error
minimum_source_quality
minimum_feature_quality
fallback_policy
certification_state
```

## 24.3 Examples

### BTC breakout

L1 may be sufficient **only if the validated strategy contract explicitly proves that its signal and execution model do not depend on deeper order-book state**. The system must not infer sufficiency from the strategy name.

### Queue imbalance

L2 may be insufficient when the strategy's alpha depends on individual queue events, queue priority or order lifetime. Such a strategy requires the minimum depth and event fidelity proved by its certification scope.

### Queue-position model

MBO or an explicitly certified equivalent is required when the model claims individual-order/queue-level information. A reconstructed estimate must be labeled `INFERRED`, not `OBSERVED`.

### Options flow

Spot price + spot volume alone are insufficient if the strategy claims options-flow information. Required fields must include the exact option transaction/quote/OI/surface inputs used by the validated strategy.

### Gamma model

Gamma exposure may not be treated as production-valid unless the exact strike/expiry/OI/IV/Greek inputs and the model assumptions used to derive exposure are present and current enough for the certification scope.

## 24.4 Hard invariants

1. Missing required data => `NO_TRADE_DATA_INSUFFICIENT`.
2. Required data below certified quality => `NO_TRADE_DATA_QUALITY`.
3. Required field stale beyond policy => `NO_TRADE_DATA_STALE`.
4. Required MBO/L2/L3 field unavailable => the affected strategy is ineligible.
5. A fallback may not silently reduce the required data tier.
6. A strategy may not substitute a correlated proxy unless the proxy is explicitly part of the certified strategy definition.

## 24.5 Required evidence

Every strategy certification must contain a machine-readable Data Sufficiency Report proving:

- requested fields;
- actual fields received;
- coverage;
- missingness;
- staleness;
- sequence integrity;
- source quality;
- feature availability;
- fallback activation frequency;
- affected decisions;
- blocked decisions;
- historical validation of the data profile.

---

# 25. TEMPORAL AUTHORITY CONTRACT

## 25.1 Objective

The system must prove not merely that a value existed in storage, but that the value was **actually available to the trading process before the decision**.

## 25.2 Timestamp authority hierarchy

The canonical hierarchy is:

```text
VENUE/PRIMARY_SOURCE_TIMESTAMP
    ↓
SOURCE_SEQUENCE / VERSION
    ↓
FIRST_AVAILABLE_TIME
    ↓
RECEIVE_TIME
    ↓
PROCESSING_TIME
    ↓
PERSISTENCE_TIME
```

Persistence time may never be used as a substitute for market availability time.

## 25.3 Point-in-time invariant

For any decision `D` at timestamp `T_D`, every decision-bearing input `X` MUST satisfy:

```text
X.first_available_time <= T_D
AND
X.point_in_time_version = version_known_at(T_D)
```

unless the experiment is explicitly marked as non-production revised-data research.

## 25.4 Revision invariant

Any observation later corrected, restated, cancelled, busted or revised must preserve both:

- the historical version known at decision time;
- later revision metadata.

Production replay may not retroactively replace the historical decision-time version.

## 25.5 Historical universe invariant

Historical research MUST reconstruct the universe available at each point in time, including where relevant:

- listing date;
- delisting date;
- suspension;
- merger/acquisition;
- ticker/symbol change;
- contract expiry;
- corporate action;
- index membership at that time;
- tradability status at that time.

---

# 26. ORDER BOOK RECONSTRUCTION CONTRACT

## 26.1 Objective

Convert raw L2/L3/MBO events into a deterministic, auditable market-state book without treating corrupted or incomplete reconstruction as valid.

## 26.2 Required reconstruction states

`UNINITIALIZED → SNAPSHOT_LOADING → REPLAYING → LIVE_VALID → DEGRADED → INVALID → RECOVERY → LIVE_VALID`

## 26.3 Required handling

The reconstruction engine MUST explicitly handle:

- snapshot bootstrap;
- incremental updates;
- sequence gaps;
- duplicate events;
- out-of-order events;
- book reset;
- venue corrections;
- add/modify/cancel/execute/replace;
- crossed book;
- locked book;
- impossible price levels;
- impossible size changes;
- trade/book synchronization;
- stale book state;
- recovery verification.

## 26.4 Hard invariants

1. Sequence gap in a trading-critical book => `INVALID` until certified recovery.
2. Unknown queue state cannot be represented as observed queue state.
3. A derived queue position must carry `INFERRED` classification.
4. Book reconstruction must be deterministic for a fixed event stream and engine version.
5. Recovery cannot silently restore trading authority.

## 26.5 Certification tests

A golden dataset MUST contain known book states and known sequence disruptions. The reconstruction engine must reproduce expected states within the documented numerical and sequencing tolerance.

---

# 27. TARGET / LABEL CONTRACT

## 27.1 Objective

Every predictive feature, alpha, model and strategy MUST define exactly what outcome it predicts.

## 27.2 Required schema

```yaml
label_id
label_version
entry_timestamp_rule
entry_price_rule
side_rule
horizon
exit_target_rule
stop_rule
timeout_rule
partial_fill_rule
partial_exit_rule
same_bar_conflict_rule
gap_rule
cost_model_version
execution_model_version
currency_normalization
outcome_definition
censoring_rule
overlap_policy
regime_condition
```

## 27.3 Same-bar rule

If both stop and target are observed in an interval and the exact event ordering cannot be reconstructed, the label MUST NOT assume favorable ordering. The strategy must use a certified conservative rule or finer-granularity data.

## 27.4 Cost-aware outcome

Where the production alpha depends on net returns, the label used for certification MUST incorporate the appropriate certified cost model. A gross-return label may be used for research, but it cannot by itself certify net profitability.

## 27.5 Overlap invariant

Overlapping observations must be marked and the statistical validation method must account for dependence. Observation count is not automatically independent sample count.

---

# 28. ALPHA DISCOVERY CONTRACT

## 28.1 Objective

Separate genuine economic hypotheses from accidental historical correlations.

## 28.2 Required alpha object

```yaml
alpha_id
alpha_version
hypothesis
economic_mechanism
observed_condition
expected_direction
target_label_id
horizon
required_features
required_data_profile
expected_regimes
excluded_regimes
historical_expectancy
gross_expectancy
net_expectancy
probability
calibration_state
stability
half_life
capacity
dependency
correlation_group
decay_state
uncertainty
research_id
trial_count
selection_context
validation_scope
```

## 28.3 Economic-mechanism requirement

A production alpha MUST have a documented hypothesis explaining why the relationship could persist. A purely retrospective correlation is not sufficient certification evidence.

## 28.4 Alpha independence

Multiple feature expressions of the same underlying mechanism MUST NOT be counted as independent evidence merely because they have different names.

---

# 29. PROBABILITY CALIBRATION CONTRACT V2.2

## 29.1 Required metrics

Where probability is part of the decision, the certification record MUST contain as applicable:

- Brier score;
- calibration curve;
- expected calibration error;
- reliability by probability bucket;
- calibration by regime;
- calibration by strategy;
- calibration sample size;
- confidence interval;
- calibration drift;
- recent-vs-long-term calibration.

## 29.2 Hard gate

A probability may not be marked `CERTIFIED` solely because a calibration routine ran. It must satisfy the numeric policy registered for its certification scope.

Required policy fields:

```yaml
minimum_sample_size
minimum_effective_sample_size
maximum_brier
maximum_ece
maximum_calibration_error
maximum_regime_calibration_error
maximum_confidence_interval_width
maximum_drift
```

The exact numeric values are versioned policy inputs and MUST be supplied by certification rather than silently hardcoded by the developer.

---

# 30. NET EXPECTANCY AND UNCERTAINTY CONTRACT

## 30.1 Canonical equation

```text
NET_EV
=
GROSS_EV
-
COMMISSION
-
SPREAD_COST
-
SLIPPAGE
-
MARKET_IMPACT
-
FUNDING
-
FINANCING
-
BORROW
-
ROLL_COST
-
OTHER_APPLICABLE_COSTS
```

The model MUST support conditional costs by:

- instrument;
- venue;
- order type;
- order size;
- liquidity state;
- volatility state;
- spread state;
- urgency;
- time-of-day;
- strategy;
- market regime.

## 30.2 Uncertainty-aware EV

Production admission MUST NOT rely only on point-estimate `NET_EV`.

Required estimates where applicable:

```text
EV_POINT
EV_LOWER_BOUND
EV_UPPER_BOUND
EV_STANDARD_ERROR
EV_CONFIDENCE_LEVEL
COST_UNCERTAINTY
EXECUTION_UNCERTAINTY
MODEL_UNCERTAINTY
```

## 30.3 Edge safety invariant

```text
EV_LOWER_BOUND
-
UNCERTAINTY_BUFFER
>
MINIMUM_EDGE_FLOOR
```

If the inequality fails, the result is `NO_TRADE_NEGATIVE_OR_INSUFFICIENT_EDGE`.

A positive point estimate does not override a non-positive lower bound.

---

# 31. MINIMUM SAMPLE / EFFECTIVE SAMPLE CONTRACT

## 31.1 Objective

Prevent a strategy from passing certification based on a large nominal sample that contains too few independent observations.

## 31.2 Required sample measures

The certification record must distinguish:

- nominal observation count;
- independent event count;
- effective sample size;
- regime-specific sample size;
- strategy-direction sample size;
- execution-mode sample size;
- session-specific sample size;
- instrument-specific sample size.

## 31.3 Hard gate

Production certification requires every required sample dimension to meet its versioned minimum policy or the affected slice must be excluded from production eligibility.

## 31.4 No aggregation shortcut

Ten thousand highly overlapping observations do not automatically equal ten thousand independent trades.

---

# 32. DYNAMIC COST AND MARKET IMPACT CONTRACT

## 32.1 Cost model layers

```text
EXPLICIT FEES
+
HALF-SPREAD / REALIZED SPREAD
+
SLIPPAGE
+
ADVERSE SELECTION
+
MARKET IMPACT
+
LATENCY COST
+
FUNDING / BORROW / FINANCING
+
ROLL / HOLDING COST
```

## 32.2 Required conditional dimensions

Cost and impact MUST be modeled as functions of, where applicable:

- size;
- participation rate;
- depth consumed;
- volatility;
- spread;
- liquidity;
- urgency;
- side;
- order type;
- time-of-day;
- venue;
- market regime.

## 32.3 Impact sanity checks

The model MUST be rejected if it predicts materially smaller impact for materially larger participation without an explicit certified mechanism explaining the relationship.

## 32.4 Model drift

Expected-vs-realized cost error must be monitored and can veto trading when it exceeds the registered policy.

---

# 33. EXECUTION / FILL SIMULATION CONTRACT V2.2

## 33.1 Required simulation dimensions

Historical execution simulation MUST address, where applicable:

- arrival timestamp;
- decision timestamp;
- order submission latency;
- venue acknowledgement latency;
- queue position;
- book movement;
- partial fills;
- cancel/replace latency;
- adverse selection;
- order rejection;
- order expiry;
- stop behavior;
- gap-through-stop;
- spread widening;
- liquidity collapse;
- venue interruption.

## 33.2 Fill authorization invariant

A simulated fill is permitted only when the historical market state and the order's certified execution model jointly support that fill.

The simulator may not assume a fill merely because historical price touched the limit price.

## 33.3 Fill realism calibration

Paper/shadow/live observations must be used to compare:

- expected fill probability vs realized fill probability;
- expected slippage vs realized slippage;
- expected impact vs realized impact;
- expected latency vs realized latency.

Significant model error triggers execution-model degradation and can block strategy promotion.

---

# 34. EDGE SAFETY MARGIN CONTRACT

## 34.1 Objective

Prevent economically meaningless positive expectancy from becoming a production trade.

## 34.2 Required buffers

The decision may account for:

- model uncertainty;
- probability uncertainty;
- cost uncertainty;
- execution uncertainty;
- regime uncertainty;
- liquidity uncertainty;
- data-quality uncertainty.

## 34.3 Hard rule

```text
ROBUST_NET_EDGE =
    NET_EV_LOWER_BOUND
    - UNCERTAINTY_BUFFER
```

`ROBUST_NET_EDGE` must exceed the certified `MINIMUM_EDGE_FLOOR`.

The edge floor is a versioned policy parameter; it is not permitted to be hidden in implementation code.

---

# 35. DETERMINISTIC POSITION SIZING CONTRACT

## 35.1 Required calculation order

```text
ACCOUNT_CAPITAL
→ SURVIVAL_CAPITAL
→ TOTAL_RISK_BUDGET
→ TRADE_RISK_BUDGET
→ STOP / INVALIDATION DISTANCE
→ CONTRACT / LOT VALUE
→ VOLATILITY ADJUSTMENT
→ LIQUIDITY ADJUSTMENT
→ CORRELATION ADJUSTMENT
→ PORTFOLIO HEAT ADJUSTMENT
→ DRAWdown ADJUSTMENT
→ CAPACITY ADJUSTMENT
→ EDGE CONFIDENCE ADJUSTMENT
→ FINAL SIZE
```

## 35.2 Invariants

1. Final size may not exceed any upper-layer ceiling.
2. Increased model uncertainty may not increase risk.
3. Worsening liquidity may not increase final size.
4. Worse calibration may not increase final size.
5. Higher leverage availability does not automatically increase risk budget.
6. AI cannot override final size ceilings.

---

# 36. EXIT MANAGEMENT CONTRACT

## 36.1 Required exit mechanisms

Every trade must declare the applicable combination of:

- hard stop;
- soft thesis invalidation;
- profit target;
- partial profit target;
- time stop;
- trailing logic;
- volatility-based exit;
- regime invalidation;
- event-risk exit;
- liquidity emergency exit;
- execution emergency exit;
- maximum holding period.

## 36.2 Exit authority

Signal, risk, capital and execution authorization remain separate. An exit may be forced by a higher-priority risk or safety layer even when the original strategy still prefers holding.

## 36.3 Exit capacity invariant

A position may not be considered fully executable unless the certified exit model can support the expected liquidation path under both normal and required stress conditions.

---

# 37. REGIME TRANSITION CONTRACT V2.2

## 37.1 Regime states

`STABLE → WATCHING_TRANSITION → CONFIRMED_TRANSITION → NEW_REGIME → UNKNOWN`

## 37.2 Transition evidence

A transition must have:

- trigger evidence;
- persistence evidence;
- confidence;
- timing;
- affected strategies;
- expected strategy impact;
- fallback action.

## 37.3 Hard rule

During a certified regime transition, a strategy may be:

`ACTIVE | SIZE_REDUCED | WAIT | DISABLED`

according to the strategy's versioned transition policy.

Unknown regime cannot authorize a new trade unless the strategy certification explicitly covers unknown-regime operation.

---

# 38. STRATEGY DECAY / DRIFT GATES V2.2

## 38.1 Required monitors

Every production strategy must monitor, where applicable:

- rolling net expectancy;
- lower-confidence-bound net expectancy;
- probability calibration;
- feature drift;
- missingness drift;
- regime drift;
- liquidity drift;
- execution drift;
- cost drift;
- latency drift;
- capacity drift;
- attribution drift.

## 38.2 State transition policy

`NORMAL → WATCH → DEGRADING → DEFENSIVE → PROBATION → DISABLED → RESEARCH`

Transitions require registered numerical thresholds and evidence windows.

## 38.3 No silent degradation

A strategy may not remain `ACTIVE` solely because its long-term backtest remains strong when the current certified live-scope metrics violate a hard decay threshold.

---

# 39. CAPACITY / CAPITAL CURVE CONTRACT

## 39.1 Objective

Determine how much capital a strategy can absorb before costs and impact materially destroy the certified edge.

## 39.2 Required curve

Every strategy that may receive meaningful capital must produce a versioned curve of:

```text
capital_size
→ participation
→ fill_probability
→ expected_slippage
→ expected_impact
→ net_EV
→ risk
→ capacity_utilization
```

## 39.3 Capacity rule

The system may not treat strategy EV as capital-size invariant.

## 39.4 Production allocation

Capital allocation must remain within the certified capacity range for the current market/liquidity regime.

---

# 40. PORTFOLIO COVARIANCE / FACTOR RISK CONTRACT

The portfolio layer must support regime-aware dependence estimates where appropriate.

Required dimensions may include:

- return covariance;
- factor covariance;
- tail dependence;
- stress correlation;
- alpha-factor overlap;
- liquidity correlation;
- venue correlation;
- model correlation.

A new trade must be evaluated on **marginal portfolio contribution**, not solely on standalone trade risk.

---

# 41. EVENT / BLACKOUT CONTRACT

Every event-driven or event-sensitive strategy MUST define:

```yaml
event_class
pre_event_window
active_event_window
post_event_window
minimum_data_freshness
allowed_order_types
disabled_order_types
spread_limit
liquidity_limit
volatility_limit
position_policy
exit_policy
```

The system must distinguish:

`PRE_EVENT | EVENT_ACTIVE | POST_EVENT | NORMALIZED`

where applicable.

Major event uncertainty is a hard veto unless the strategy has a specific certified event regime.

---

# 42. RESEARCH SEARCH-BUDGET CONTRACT

Every research campaign must record:

```yaml
research_id
hypothesis
search_space_definition
parameter_space
feature_space
strategy_space
number_of_trials
number_of_failed_trials
number_of_selected_trials
selection_rule
stopping_rule
validation_reuse_count
test_exposure_count
research_budget
```

The purpose is to quantify selection pressure and prevent undisclosed repeated testing.

A candidate selected after excessive uncontrolled search cannot pass certification solely on its selected backtest metrics.

---

# 43. FUTURE-MARKET ADAPTATION CONTRACT

## 43.1 Objective

The system must remain adaptive without granting uncontrolled self-modification authority.

## 43.2 Detectable change classes

The monitoring framework must be capable of detecting evidence of:

- feature distribution change;
- target distribution change;
- regime-frequency change;
- volatility regime change;
- liquidity structure change;
- spread behavior change;
- execution-latency change;
- fee-model change;
- market-impact change;
- order-book structure change;
- cross-asset relationship change;
- strategy crowding/decay;
- data-vendor methodology change;
- instrument-universe change.

## 43.3 Adaptive loop

```text
OBSERVE
→ DETECT
→ DIAGNOSE
→ HYPOTHESIZE
→ RESEARCH
→ VALIDATE
→ CERTIFY
→ SHADOW
→ PAPER
→ MICRO
→ PROBATION
→ DEPLOY
```

Learning may propose changes but cannot directly modify production.

---

# 44. ADVERSARIAL PROFITABILITY EXAMINATION FRAMEWORK

## 44.1 Examination rule

The system must be subjected to a repeatable exam before implementation freeze and after each major contract/version change.

Every question record contains:

```yaml
question_id
domain
question
criticality
required_contract
required_data
required_test
required_evidence
numerical_policy
pass_condition
fail_action
production_blocking
status
exam_version
```

## 44.2 Status rules

`PASS` = complete evidence satisfies the contract.

`FAIL` = evidence contradicts the contract.

`UNKNOWN` = insufficient evidence.

`NOT_APPLICABLE` = explicitly justified by market profile and strategy scope.

For all production-critical questions:

```text
UNKNOWN = FAIL
```

## 44.3 Master exam question bank

The following questions are mandatory. The exact implementation may expand this list but may not delete a production-blocking question without a versioned change request.

### DATA SUFFICIENCY — DS

1. `DS-001` Does the strategy have an explicit minimum data tier?
2. `DS-002` Does every required feature map to its raw source data?
3. `DS-003` Is the required source available at decision time?
4. `DS-004` Is the required source quality above policy?
5. `DS-005` Is data coverage above policy?
6. `DS-006` Is data missingness below policy?
7. `DS-007` Is staleness below policy?
8. `DS-008` Is sequence-gap rate below policy?
9. `DS-009` Is out-of-order rate below policy?
10. `DS-010` Is clock error below policy?
11. `DS-011` Is every strategy-specific L1/L2/L3/MBO dependency explicitly declared?
12. `DS-012` Is every options-data dependency explicitly declared?
13. `DS-013` Is every futures-data dependency explicitly declared?
14. `DS-014` Is every macro vintage dependency explicitly declared?
15. `DS-015` Is every fundamental vintage dependency explicitly declared?
16. `DS-016` Does fallback preserve required data quality?
17. `DS-017` Does missing critical data veto the strategy?
18. `DS-018` Does proxy substitution require explicit certification?
19. `DS-019` Is the fallback activation rate measured?
20. `DS-020` Is the strategy's data sufficiency report versioned?

### TEMPORAL TRUTH — TT

21. `TT-001` Was every decision-bearing input actually available before decision time?
22. `TT-002` Is first-available time distinct from persistence time?
23. `TT-003` Is revision history preserved?
24. `TT-004` Is historical replay using the version known then?
25. `TT-005` Is macro vintage preserved?
26. `TT-006` Is fundamental vintage preserved?
27. `TT-007` Are news first-seen and publication timestamps distinct?
28. `TT-008` Are corrections and retractions versioned?
29. `TT-009` Are corporate actions point-in-time correct?
30. `TT-010` Is historical universe reconstruction deterministic?

### ORDER BOOK — OB

31. `OB-001` Is the book reconstructed deterministically?
32. `OB-002` Are sequence gaps detected?
33. `OB-003` Are duplicate events detected?
34. `OB-004` Are out-of-order events handled?
35. `OB-005` Are book resets detected?
36. `OB-006` Are corrections handled?
37. `OB-007` Are trade/book timestamps reconciled?
38. `OB-008` Is queue state explicitly classified as observed or inferred?
39. `OB-009` Does incomplete book state disable dependent strategies?
40. `OB-010` Is reconstruction recovery independently certified?

### LABEL — LB

41. `LB-001` Is the target explicitly defined?
42. `LB-002` Is horizon explicitly defined?
43. `LB-003` Is entry price rule explicit?
44. `LB-004` Is exit rule explicit?
45. `LB-005` Is stop rule explicit?
46. `LB-006` Is timeout rule explicit?
47. `LB-007` Is partial fill handled?
48. `LB-008` Is partial exit handled?
49. `LB-009` Is same-bar stop/target ambiguity handled conservatively?
50. `LB-010` Is label construction cost-aware where required?
51. `LB-011` Is overlapping observation dependence handled?
52. `LB-012` Is censoring handled?

### ALPHA — AL

53. `AL-001` Does every production alpha have a hypothesis?
54. `AL-002` Does it have an economic mechanism?
55. `AL-003` Is expected direction documented?
56. `AL-004` Is target label linked?
57. `AL-005` Is required data linked?
58. `AL-006` Is expected regime linked?
59. `AL-007` Is excluded regime linked?
60. `AL-008` Is gross expectancy measured?
61. `AL-009` Is net expectancy measured?
62. `AL-010` Is uncertainty measured?
63. `AL-011` Is half-life measured?
64. `AL-012` Is capacity measured?
65. `AL-013` Is dependency measured?
66. `AL-014` Is stability measured?
67. `AL-015` Is decay measured?
68. `AL-016` Is the alpha validated out-of-sample?
69. `AL-017` Is the alpha stable across required regimes?
70. `AL-018` Does reverse-direction testing contradict the claimed mechanism?
71. `AL-019` Does removing the largest winner destroy the result?
72. `AL-020` Does the edge survive realistic execution?

### PROBABILITY — PB

73. `PB-001` Is probability distinct from confidence?
74. `PB-002` Is probability calibrated?
75. `PB-003` Is Brier score within policy?
76. `PB-004` Is calibration error within policy?
77. `PB-005` Is regime calibration within policy?
78. `PB-006` Is minimum effective sample met?
79. `PB-007` Are confidence intervals acceptable?
80. `PB-008` Is probability drift monitored?
81. `PB-009` Does calibration failure block production?

### EXPECTANCY / COST — EV

82. `EV-001` Is gross EV calculated?
83. `EV-002` Is commission included?
84. `EV-003` Is spread cost included?
85. `EV-004` Is slippage included?
86. `EV-005` Is market impact included?
87. `EV-006` Is funding included where applicable?
88. `EV-007` Is borrow included where applicable?
89. `EV-008` Is financing included where applicable?
90. `EV-009` Is roll/holding cost included where applicable?
91. `EV-010` Is adverse selection included where applicable?
92. `EV-011` Is latency cost modeled where material?
93. `EV-012` Is EV uncertainty measured?
94. `EV-013` Is EV lower bound calculated?
95. `EV-014` Does lower-bound EV exceed the edge floor?
96. `EV-015` Does cost uncertainty remain below the certified edge buffer?

### EXECUTION — EX

97. `EX-001` Is order submission latency modeled?
98. `EX-002` Is acknowledgement latency modeled?
99. `EX-003` Is queue position modeled when required?
100. `EX-004` Is limit-fill probability modeled?
101. `EX-005` Are partial fills modeled?
102. `EX-006` Are cancel/replace delays modeled?
103. `EX-007` Is adverse selection modeled?
104. `EX-008` Are order rejections modeled?
105. `EX-009` Are spread expansions modeled?
106. `EX-010` Are liquidity collapses modeled?
107. `EX-011` Are gap-through-stop conditions modeled?
108. `EX-012` Is fill realism calibrated to shadow/paper/live evidence?
109. `EX-013` Is expected-vs-realized slippage monitored?
110. `EX-014` Is expected-vs-realized fill probability monitored?
111. `EX-015` Is expected-vs-realized impact monitored?
112. `EX-016` Does execution stop when edge half-life is exceeded?

### RISK — RK

113. `RK-001` Is risk deterministic?
114. `RK-002` Is trade risk below strategy risk?
115. `RK-003` Is strategy risk below factor risk?
116. `RK-004` Is factor risk below asset risk?
117. `RK-005` Is asset risk below portfolio risk?
118. `RK-006` Is drawdown response active?
119. `RK-007` Is risk-of-ruin within policy?
120. `RK-008` Is expected shortfall within policy?
121. `RK-009` Is gap risk modeled?
122. `RK-010` Is spread expansion modeled?
123. `RK-011` Is liquidity-adjusted loss modeled?
124. `RK-012` Is forced liquidation modeled?
125. `RK-013` Does positive EV fail to override unacceptable tail risk?

### PORTFOLIO / CAPITAL — PC

126. `PC-001` Is the trade evaluated against current portfolio state?
127. `PC-002` Is marginal portfolio risk measured?
128. `PC-003` Is factor concentration measured?
129. `PC-004` Is alpha-factor concentration measured?
130. `PC-005` Is venue concentration measured?
131. `PC-006` Is event concentration measured?
132. `PC-007` Is model concentration measured?
133. `PC-008` Is correlation regime-aware where required?
134. `PC-009` Are tail dependencies measured?
135. `PC-010` Is capital competition deterministic?
136. `PC-011` Is capacity respected?
137. `PC-012` Is capital-size dependence of EV measured?

### EXIT / POSITION — PX

138. `PX-001` Is hard-stop behavior defined?
139. `PX-002` Is thesis invalidation defined?
140. `PX-003` Is time-stop defined?
141. `PX-004` Is target behavior defined?
142. `PX-005` Is partial exit behavior defined?
143. `PX-006` Is emergency exit defined?
144. `PX-007` Is exit capacity validated?
145. `PX-008` Is gap risk handled?
146. `PX-009` Is event-risk exit handled?
147. `PX-010` Is regime invalidation handled?

### REGIME / ADAPTATION — RG

148. `RG-001` Is current regime classified?
149. `RG-002` Is regime confidence measured?
150. `RG-003` Is transition state measurable?
151. `RG-004` Is transition confirmation defined?
152. `RG-005` Is unknown regime handled safely?
153. `RG-006` Is strategy-specific transition response defined?
154. `RG-007` Is regime drift monitored?
155. `RG-008` Is new-regime discovery possible?
156. `RG-009` Is regime detection latency within strategy half-life?

### DECAY / DRIFT — DR

157. `DR-001` Is rolling expectancy monitored?
158. `DR-002` Is lower-bound EV monitored?
159. `DR-003` Is probability calibration drift monitored?
160. `DR-004` Is feature drift monitored?
161. `DR-005` Is data-quality drift monitored?
162. `DR-006` Is execution drift monitored?
163. `DR-007` Is cost drift monitored?
164. `DR-008` Is latency drift monitored?
165. `DR-009` Is capacity drift monitored?
166. `DR-010` Are state transitions thresholded?
167. `DR-011` Does strategy degradation block or reduce trading?

### CAPACITY — CP

168. `CP-001` Is capacity measured?
169. `CP-002` Is capacity a function of liquidity?
170. `CP-003` Is impact size-dependent?
171. `CP-004` Is fill probability size-dependent?
172. `CP-005` Is exit liquidity size-dependent?
173. `CP-006` Is stress liquidity included?
174. `CP-007` Is a capital-to-edge curve produced?
175. `CP-008` Is production allocation inside certified capacity?

### RESEARCH / OVERFITTING — RS

176. `RS-001` Is every trial registered?
177. `RS-002` Are failed trials recorded?
178. `RS-003` Is trial count tracked?
179. `RS-004` Is selection rule explicit?
180. `RS-005` Is stopping rule explicit?
181. `RS-006` Is search-space exposure measured?
182. `RS-007` Is validation reuse tracked?
183. `RS-008` Is test-set exposure controlled?
184. `RS-009` Are multiple-testing risks evaluated?
185. `RS-010` Is PBO evaluated where applicable?
186. `RS-011` Is DSR evaluated where applicable?
187. `RS-012` Is parameter instability evaluated?
188. `RS-013` Is regime robustness evaluated?
189. `RS-014` Is stationarity evaluated where relevant?
190. `RS-015` Is serial dependence handled?

### REPLAY / CERTIFICATION — RP

191. `RP-001` Is replay deterministic?
192. `RP-002` Does replay reproduce decision-time data availability?
193. `RP-003` Does replay reproduce source state?
194. `RP-004` Does replay reproduce risk policy?
195. `RP-005` Does replay reproduce capital state?
196. `RP-006` Does replay reproduce execution assumptions?
197. `RP-007` Does replay reproduce cost assumptions?
198. `RP-008` Does replay reproduce strategy version?
199. `RP-009` Does replay reproduce model/feature versions?
200. `RP-010` Does replay preserve decision lineage?

### FAILURE / RECOVERY — FR

201. `FR-001` Does stale data enter safe mode?
202. `FR-002` Does sequence failure block dependent trades?
203. `FR-003` Does clock failure block critical decisions?
204. `FR-004` Does broker/internal mismatch block new orders?
205. `FR-005` Does unknown position state block new orders?
206. `FR-006` Does database loss preserve safe authority?
207. `FR-007` Does event-bus failure preserve safe authority?
208. `FR-008` Does process restart require reconciliation?
209. `FR-009` Does recovery require risk revalidation?
210. `FR-010` Does restore keep trading disabled until certification?

### LEARNING — LG

211. `LG-001` Can learning write production policy directly? (Must be NO.)
212. `LG-002` Is feedback evidence-linked?
213. `LG-003` Is every learning proposal versioned?
214. `LG-004` Is every candidate validated before promotion?
215. `LG-005` Is champion/challenger state explicit?
216. `LG-006` Is rollback available?
217. `LG-007` Are negative outcomes retained?
218. `LG-008` Can a failed challenger displace a champion? (Must be NO.)

### SECURITY / AUTHORITY — SC

219. `SC-001` Can AI alter risk ceilings? (Must be NO.)
220. `SC-002` Can AI alter kill switches? (Must be NO.)
221. `SC-003` Can research alter production directly? (Must be NO.)
222. `SC-004` Can notification failure create trading authority? (Must be NO.)
223. `SC-005` Is release state versioned?
224. `SC-006` Are secrets separated by environment?
225. `SC-007` Is high-impact control capability-scoped?

### FUTURE MARKET — FM

226. `FM-001` Can the system detect feature-distribution change?
227. `FM-002` Can it detect target-distribution change?
228. `FM-003` Can it detect market-structure change?
229. `FM-004` Can it detect liquidity-structure change?
230. `FM-005` Can it detect execution-latency change?
231. `FM-006` Can it detect cost-model change?
232. `FM-007` Can it detect strategy crowding/decay?
233. `FM-008` Can it detect vendor methodology change?
234. `FM-009` Can it discover previously unseen regimes?
235. `FM-010` Can it isolate an affected strategy without disabling unrelated certified strategies?
236. `FM-011` Does adaptation require governed research/certification?
237. `FM-012` Can the system return to the last certified champion?

---

# 45. ADVERSARIAL TEST SCENARIO LIBRARY

The exam is not limited to static questions. The implementation MUST support repeatable scenario injection.

## 45.1 Data failures

- complete feed loss;
- delayed feed;
- burst packet loss;
- sequence gap;
- duplicated events;
- out-of-order events;
- corrupt price;
- corrupt size;
- impossible negative values;
- crossed book;
- locked book;
- stale snapshot;
- source methodology change;
- revision flood;
- clock jump.

## 45.2 Market failures

- spread explosion;
- liquidity collapse;
- volatility shock;
- gap move;
- order-book collapse;
- correlation shock;
- cross-venue divergence;
- liquidation cascade;
- event shock;
- venue halt.

## 45.3 Execution failures

- acknowledgement timeout;
- duplicate acknowledgement;
- order reject;
- partial fill;
- delayed fill;
- cancel rejection;
- replace rejection;
- stale quote at execution;
- market impact shock;
- emergency liquidation.

## 45.4 State failures

- unknown position;
- internal/external mismatch;
- duplicated fill;
- missing fill;
- orphan order;
- stale balance;
- stale margin;
- settlement mismatch.

## 45.5 Research failures

- intentional look-ahead injection;
- revised-data leakage;
- survivorship-only universe;
- hidden parameter tuning;
- test-set reuse;
- correlated features counted as independent;
- false calibration;
- unrealistic fills;
- omitted costs;
- omitted capacity.

Every scenario must end in one of:

`SAFE | HALTED | RECONCILIATION_REQUIRED | CERTIFICATION_FAIL | CONTROLLED_RECOVERY`

unless the scenario is explicitly non-critical and the documented fallback is certified.

---

# 46. NUMERICAL POLICY REGISTRY V2.2

The following policies MUST exist as versioned objects rather than literals hidden in code.

```yaml
DataPolicy:
  min_coverage
  max_missingness
  max_staleness
  max_sequence_gap_rate
  max_out_of_order_rate
  max_clock_error
  min_quality_score

CalibrationPolicy:
  min_sample_size
  min_effective_sample_size
  max_brier
  max_ece
  max_calibration_error
  max_drift

EdgePolicy:
  min_edge_floor
  confidence_level
  max_uncertainty_buffer_fraction
  min_lower_bound_ev

ExecutionPolicy:
  max_order_latency
  max_ack_latency
  max_slippage
  max_impact
  min_fill_probability
  max_execution_deviation

RiskPolicy:
  max_trade_risk
  max_strategy_risk
  max_factor_risk
  max_asset_risk
  max_portfolio_risk
  max_drawdown
  max_tail_loss
  max_ruin_probability

CapacityPolicy:
  max_capacity_utilization
  max_participation_rate
  max_expected_impact
  min_exit_liquidity

DriftPolicy:
  max_feature_drift
  max_target_drift
  max_calibration_drift
  max_cost_drift
  max_execution_drift
  max_latency_drift

ResearchPolicy:
  max_trial_count_without_review
  max_validation_reuse
  max_test_exposure
  minimum_oos_period
  minimum_regime_coverage
```

A production release cannot activate if a required numeric policy field is absent.

---

# 47. PROFITABILITY CERTIFICATION GATE MATRIX

A strategy can reach `R4 PROFITABILITY CERTIFIED` only if all applicable gates pass:

```text
G01 CONTRACT PASS
G02 DATA SUFFICIENCY PASS
G03 TEMPORAL TRUTH PASS
G04 HISTORICAL UNIVERSE PASS
G05 FEATURE PASS
G06 LABEL/TARGET PASS
G07 ALPHA PASS
G08 PROBABILITY PASS
G09 NET EXPECTANCY PASS
G10 EV UNCERTAINTY PASS
G11 EDGE SAFETY PASS
G12 EXECUTION SIMULATION PASS
G13 COST/IMPACT PASS
G14 RISK/TAIL PASS
G15 PORTFOLIO PASS
G16 CAPITAL PASS
G17 CAPACITY PASS
G18 REPLAY PASS
G19 OVERFITTING PASS
G20 STATISTICAL VALIDATION PASS
G21 SHADOW PASS
G22 PAPER PASS
G23 MICRO PASS
G24 PROBATION PASS
G25 ADVERSARIAL EXAM PASS
G26 DECISION→OUTCOME LINEAGE PASS
G27 DRIFT/ADAPTATION PASS
G28 RELEASE/ROLLBACK PASS
```

A single production-blocking FAIL or UNKNOWN prevents promotion.

---

# 48. EVIDENCE CONTRACT V2.2

Every certification gate must produce an immutable evidence record:

```yaml
gate_id
certification_scope
artifact_id
code_version
contract_version
data_version
feature_versions
model_versions
strategy_version
parameter_version
policy_versions
cost_model_version
execution_model_version
risk_policy_version
capital_policy_version
research_id
run_id
test_run_ids
metrics
confidence_intervals
observations
question_results
scenario_results
failures
blocking_reasons
reviewer_or_approver
timestamp
```

A green dashboard without immutable evidence is not a PASS.

---

# 49. TRACEABILITY EXTENSION V2.2

The traceability matrix is extended with:

```text
question_id
contract_id
policy_id
invariant_id
test_id
scenario_id
evidence_id
certification_scope
strategy_id
market_profile_id
status
blocking
```

Every production-critical question must resolve to at least one contract, one test and one evidence artifact.

---

# 50. IMPLEMENTATION DEFINITION OF READY V2.2

An implementation item is not ready for coding unless:

1. purpose exists;
2. non-purpose exists;
3. exact inputs exist;
4. exact outputs exist;
5. dependencies exist;
6. state exists;
7. transitions exist;
8. invariants exist;
9. hard vetoes exist;
10. failure modes exist;
11. error codes exist;
12. recovery exists;
13. persistence exists;
14. events exist;
15. versioning exists;
16. security exists;
17. observability exists;
18. numerical policies exist where applicable;
19. replay behavior exists;
20. caller exists;
21. orchestrator exists;
22. consumer exists;
23. outcome link exists;
24. feedback link exists;
25. profitability questions are mapped;
26. acceptance tests are defined.

---

# 51. IMPLEMENTATION DEFINITION OF DONE V2.2

An item is not done unless:

- implementation exists;
- contract tests pass;
- schema tests pass;
- unit tests pass;
- integration tests pass;
- replay tests pass;
- failure-injection tests pass;
- performance tests pass;
- security tests pass;
- observability tests pass;
- persistence tests pass;
- lineage tests pass;
- consumer tests pass;
- outcome tests pass where applicable;
- adversarial questions pass;
- required numerical thresholds are satisfied;
- evidence is persisted;
- certification status is current.

---

# 52. NO-SILENT-ASSUMPTION RULE V2.2

The developer may not resolve any of the following by assumption:

- data sufficiency;
- target/label semantics;
- fill behavior;
- stop ordering;
- transaction costs;
- market impact;
- probability calibration;
- minimum sample size;
- edge floor;
- regime transition thresholds;
- strategy decay thresholds;
- capacity;
- position sizing;
- exit behavior;
- portfolio dependence;
- historical universe;
- revision semantics.

Any missing rule triggers:

`STOP → CHANGE REQUEST → IMPACT ANALYSIS → CONTRACT VERSION → TEST → APPROVAL → IMPLEMENTATION`

---

# 53. PROFITABILITY MASTER INVARIANTS

1. **No required data, no trade.**
2. **No point-in-time truth, no production certification.**
3. **No strategy-specific data sufficiency evidence, no strategy activation.**
4. **No target/label contract, no predictive certification.**
5. **No validated alpha mechanism, no production strategy.**
6. **Confidence never substitutes for probability.**
7. **Probability never substitutes for expected value.**
8. **Positive point-estimate EV never overrides negative EV lower bound.**
9. **Positive EV never overrides unacceptable tail/ruin risk.**
10. **Historical touch never guarantees executable fill.**
11. **Backtest fill must be supported by the certified execution model.**
12. **Strategy EV is not assumed constant with capital size.**
13. **Unknown regime is not a production-valid regime unless specifically certified.**
14. **Decay can veto an otherwise historically profitable strategy.**
15. **Research cannot write production behavior.**
16. **AI cannot increase risk authority.**
17. **Reconciliation uncertainty blocks new trading.**
18. **Unknown position state blocks new trading.**
19. **A failed critical adversarial question blocks certification.**
20. **An absent evidence artifact is not a PASS.**
21. **A missing numerical policy is not a PASS.**
22. **A nominal sample count does not equal an independent sample count.**
23. **Correlated evidence cannot be counted as independent confirmation.**
24. **New market regimes trigger explicit diagnosis rather than silent adaptation.**
25. **Production adaptation occurs only through governed promotion.**

---

# 54. V2.2 MASTER DECISION

The implementation objective is now explicitly:

```text
REAL MARKET
↓
REAL DATA
↓
STRATEGY-SPECIFIC DATA SUFFICIENCY
↓
POINT-IN-TIME TRUTH
↓
VALIDATED FEATURES
↓
MARKET STATE / REGIME
↓
SETUP
↓
ALPHA + ECONOMIC MECHANISM
↓
TARGET / LABEL
↓
CALIBRATED PROBABILITY
↓
UNCERTAINTY-AWARE NET EXPECTANCY
↓
EDGE SAFETY MARGIN
↓
NO-TRADE / SIGNAL
↓
DETERMINISTIC RISK
↓
PORTFOLIO / TAIL / RUIN
↓
CAPACITY / CAPITAL
↓
REALISTIC EXECUTION
↓
RECONCILIATION
↓
OUTCOME
↓
ATTRIBUTION
↓
DECAY / DRIFT
↓
CONTROLLED RESEARCH
↓
ADVERSARIAL CERTIFICATION
↓
GOVERNED ADAPTATION
```

The objective is not to maximize trade count, model complexity or backtest Sharpe. The objective is to maximize the probability that every production trade is supported by:

- sufficient information;
- valid temporal truth;
- measurable predictive evidence;
- calibrated probability where applicable;
- uncertainty-aware positive net expectancy;
- realistic execution;
- bounded risk;
- sufficient capacity;
- complete lineage;
- controlled adaptation.

---

# 55. V2.2.2 FINAL FREEZE RULE

`ARCHITECTURE_FROZEN = TRUE` only when the V2.2 architecture and all normative amendments are approved.

`CODE_READY = TRUE` only when R1 is complete.

`TEST_READY = TRUE` only when R2 is complete.

`R3_OPERATIONALLY_LIVE_READY = TRUE` only when R3 is complete.

`PROFITABILITY_CERTIFIED = TRUE` only when R4 is complete for the selected certification scope **and** the selected certification scope satisfies every applicable V2.2.2 profitability gate and adversarial exam requirement.

`LIVE_AUTHORIZED = TRUE` only when R4 is complete and the selected scope remains inside all live operational gates, external prerequisites and hard safety constraints.

Additional hard authority invariant:

```text
R0 ≠ R1 ≠ R2 ≠ R3 ≠ R4
R3 never authorizes trading.
R4 certifies only the exact certification scope and tested conditions.
LIVE_AUTHORIZED requires: R4 + current operational safety + external prerequisites.
Any loss of an R4 prerequisite, certification-scope match, or live safety predicate immediately revokes trading authority.
```

These states are never interchangeable.

---

# 56. V2.2.2 FINAL IMPLEMENTATION RULE

From V2.2 onward:

> **The developer does not invent trading behavior during implementation. The developer implements the approved contract and proves it with tests and evidence.**

The mandatory loop is:

```text
QUESTION
→ CONTRACT
→ INVARIANT
→ NUMERICAL POLICY
→ CODE
→ TEST
→ ADVERSARIAL TEST
→ RUN
→ EVIDENCE
→ AUDIT
→ ACCEPT
→ NEXT
```

If a new market condition exposes an uncovered business behavior:

```text
STOP
→ CHANGE REQUEST
→ CLASSIFY
→ IMPACT ANALYSIS
→ CONTRACT VERSION
→ TEST
→ APPROVE
→ IMPLEMENT
→ RECERTIFY
```

No silent production repair is permitted.

---

# 57. V2.2.2 CERTIFICATION STATUS

At document creation time, this V2.2.2 contract is a **prepared certification baseline**, not evidence that any strategy is profitable and not itself an R4 certificate. R4 is an empirical release/scope state produced only by approved evidence artifacts.

The following must remain explicitly unclaimed until real evidence exists:

- guaranteed profit;
- guaranteed win rate;
- guaranteed Sharpe;
- guaranteed future alpha;
- guaranteed execution quality;
- guaranteed market-regime persistence.

The contract is designed to make these claims testable rather than assumed.

# 58. POST-V2.2.2 EXAM REQUIREMENT

After V2.2.2 is frozen, the mandatory certification activity is a full adversarial re-examination of the entire normative contract surface: all V2.2.x profitability amendments, all retained V2.1 sections that govern live behavior, all applicable engine contracts, all policies, all readiness/authority rules, and the complete V2.2.x adversarial question bank. No retained baseline section is exempt merely because it originated in V2.1.

The output MUST be:

```text
QUESTION_ID
→ QUESTION
→ SCOPE
→ PASS / FAIL / UNKNOWN / N/A
→ EVIDENCE_ID(s)
→ OBSERVATION
→ GAP
→ CONTRACT_ID
→ POLICY_ID / THRESHOLD
→ TEST_ID(s)
→ REQUIRED CHANGE
→ RECERTIFICATION STATUS
```

Every production-blocking question must have a unique `QUESTION_ID`, at least one linked `EVIDENCE_ID` when marked PASS, an explicit `FAIL_ACTION`, and a traceable contract/test linkage. `PASS` without evidence linkage is invalid. `UNKNOWN` on a production-blocking question is equivalent to FAIL until remediated or formally classified `NOT_APPLICABLE` with evidence.

No implementation freeze may be called “complete” until all production-blocking questions are `PASS` or justified `NOT_APPLICABLE` with evidence.

---

## V2.2.2 CORRECTION / CERTIFICATION LOG — EXAM FINDINGS REMEDIATED

The V2.2 adversarial review identified the following contract-level ambiguity and it is corrected in V2.2.2:

| Finding | Risk | Correction | Status |
|---|---|---|---|
| R3 was simultaneously described as live activation and followed by R4 profitability certification | Could allow an interpretation that R3 alone grants production trading authority | R3 renamed `OPERATIONALLY LIVE-READY`; R4 is mandatory for profitability certification; `LIVE_AUTHORIZED` now requires R4 + current operational safety | CLOSED |
| Legacy V2.1 readiness section could contradict V2.2.1 authority semantics | Coding could implement conflicting authority gates | Explicit V2.2.2 override inserted into retained baseline section | CLOSED |
| Adversarial exam PASS lacked mandatory unique evidence linkage | A green result could exist without auditable proof | Mandatory `QUESTION_ID → EVIDENCE_ID → CONTRACT/POLICY/TEST → RECERTIFICATION` linkage | CLOSED |

No claim is made that this correction proves profitability. It removes a governance/authority ambiguity discovered during examination. Profitability itself remains an empirical certification outcome requiring real data and execution evidence.

# V2.2.2 END STATE

The intended end state is not “a very large trading application”. It is an auditable, adaptive operating system whose production authority is continuously constrained by data truth, statistical evidence, execution reality, risk, capacity and independently recorded outcomes.

`KNOWN → MEASURED → VALIDATED → CERTIFIED → EXECUTED → RECONCILED → LEARNED`

Anything outside that chain is research, observation, or uncertainty — not production trading authority.

# 59. V2.2.2 ADVERSARIAL EXAM CLOSURE RULE

The following are mandatory conditions for the implementation contract to be considered **software-implementation-ready**:

1. Every production-blocking question has a unique `QUESTION_ID`.
2. Every `PASS` has an `EVIDENCE_ID` and links to the applicable `CONTRACT_ID`, `POLICY_ID/THRESHOLD`, and `TEST_ID`.
3. Every `FAIL` has a mandatory `FAIL_ACTION`.
4. Every `UNKNOWN` on a production-blocking question is treated as `FAIL` until remediated or justified `NOT_APPLICABLE` with evidence.
5. Every critical requirement is traceable through `REQUIREMENT → CONTRACT → POLICY → CODE → TEST → EVIDENCE → CERTIFICATION GATE`.
6. No retained V2.1 live-behavior section may override V2.2.x authority, profitability, evidence, or fail-closed rules.
7. A certification scope may not inherit profitability certification from a different market profile, instrument universe, data profile, model/feature version, cost/execution model, risk policy, or time window unless the contract explicitly permits that equivalence and evidence proves it.
8. Loss of a current certification prerequisite causes immediate `R4_REVOKED` and removes `LIVE_AUTHORIZED`.
9. Document freeze does not imply implementation evidence, profitability, or live authorization.
10. No software implementation may be declared complete merely because schemas and code exist; the applicable tests and evidence must exist and pass.

Final authority chain:

```text
ARCHITECTURE_FROZEN
    ↓
CODE_READY
    ↓
TEST_READY
    ↓
R3_OPERATIONALLY_LIVE_READY
    ↓
R4_PROFITABILITY_CERTIFIED (scope-specific)
    ↓
LIVE_AUTHORIZED (current operational safety + external prerequisites)
```

Any break in the chain terminates production authority at the first invalid state.

# 60. V2.2.2 EXAM RESULT INTERPRETATION

The contract may be described as **implementation-ready baseline** only when the documentation-level adversarial exam finds no unresolved critical contract contradiction. This is distinct from software implementation readiness and distinct from profitability certification.

The contract may be described as **R4 certified** only from immutable runtime evidence generated by the implemented system for a defined certification scope. This document can define that gate; it cannot manufacture its evidence.




---

# V2.2.3 — R1 CODE-READY NORMATIVE CLOSURE

**Document status:** MASTER IMPLEMENTATION CONTRACT — R1 CODE-READY CONTRACT CLOSURE EDITION

**Version:** 2.2.3

**Supersedes:** V2.2.2 wherever this closure package adds, clarifies, or strengthens an implementation rule. Existing V2.2.2 rules remain valid unless explicitly overridden below.

**Purpose:** Close the remaining implementation-level ambiguities identified by the R1 CODE-READY audit without weakening any V2.2.2 profitability, safety, authority, evidence, fail-closed, or certification invariant.

**Important distinction:** This amendment makes the contract surface materially more executable. It does **not** manufacture runtime evidence, real broker entitlement, profitability, or LIVE_AUTHORIZED state. Those remain external/runtime certification outputs.

## 104. V2.2.3 NORMATIVE PRECEDENCE RULE

The authoritative precedence order is:

```text
V2.2.3 MASTER CONTRACT
    ↓
V2.2.2 NORMATIVE AMENDMENTS
    ↓
V2.1 IMPLEMENTATION FREEZE PACK
    ↓
V1 RETAINED BASELINE
    ↓
CODE
```

Where an explicit conflict exists, the highest applicable normative rule wins. A lower layer may specialize but may not weaken a hard invariant.

A contradiction discovered after coding is a `CONTRACT_CORRECTION`, not permission for silent implementation behavior.

## 105. DATA NORMALIZATION / UNIT / PRECISION CONTRACT

Every source observation must be normalized before entering cross-domain decision logic.

### 105.1 Canonical normalization fields

```yaml
normalization_id
normalization_version
source_id
instrument_id
venue_id
canonical_symbol
source_symbol
asset_class
quote_currency
base_currency
price_unit
quantity_unit
volume_unit
notional_unit
timestamp_timezone
price_scale
quantity_scale
fee_scale
currency_conversion_version
unit_conversion_version
rounding_policy_version
precision_policy_version
normalization_status
```

### 105.2 Hard invariants

1. A value with an unknown unit is `UNKNOWN` and cannot enter a production decision path.
2. Cross-venue/cross-asset calculations require canonical unit and currency normalization.
3. Tick size, lot size, quantity precision, minimum notional and venue rounding rules must be applied before an order is considered executable.
4. Display precision is never assumed to equal execution precision.
5. Financial calculations must use an explicitly versioned numerical representation and rounding policy; hidden language/runtime floating-point behavior cannot define economic truth.
6. Historical records preserve the exact normalization and precision policy used at decision time.

## 106. MARKET CALENDAR / SESSION / TRADING-STATE CONTRACT

Every Market Profile must bind a versioned market calendar.

```yaml
calendar_id
calendar_version
venue_id
market_profile_id
timezone
sessions
holidays
half_days
auction_windows
maintenance_windows
halt_rules
resume_rules
pre_open_state
open_state
closed_state
post_close_state
trading_halt_state
settlement_windows
expiry_windows
roll_windows
special_event_windows
```

Canonical market state:

`PRE_OPEN | OPEN | AUCTION | HALTED | MAINTENANCE | CLOSED | SETTLEMENT | UNKNOWN`

A strategy may only operate in sessions explicitly certified for that strategy.

Calendar uncertainty on a trading-critical decision path is a hard block unless a certified safe fallback exists.

## 107. INSTRUMENT LIFECYCLE / CORPORATE-ACTION / CONTRACT-LINEAGE CONTRACT

The Instrument Master must preserve a complete lifecycle:

```text
DISCOVERED → ACTIVE → SUSPENDED → EXPIRED/DELISTED → RETIRED
```

Where applicable, the lifecycle must include:

- listing and first-tradable time;
- suspension/halt intervals;
- delisting time;
- ticker/symbol changes;
- corporate actions;
- split/adjustment factors;
- dividend/cash adjustments;
- merger/acquisition lineage;
- futures expiry/roll lineage;
- continuous-contract mapping;
- options contract lifecycle;
- venue migration;
- settlement method.

Raw contract identity and adjusted/continuous analytics identity must never be conflated.

A historical strategy must use the instrument state that existed at that historical point in time.

## 108. BROKER / ACCOUNT / POSITION SEMANTICS CONTRACT

Every production account must declare:

```yaml
account_id
broker_id
venue_set
base_currency
position_mode
margin_mode
leverage_policy
settlement_model
hedge_or_one_way_mode
netting_semantics
fee_schedule_version
funding_schedule_version
borrow_schedule_version
balance_semantics_version
position_semantics_version
order_semantics_version
trading_permission_state
```

The system must explicitly model, where applicable:

- isolated/cross margin;
- one-way/hedge position semantics;
- netted vs separately tracked positions;
- reduce-only behavior;
- close-position semantics;
- realized/unrealized P&L rules;
- funding/borrow accrual;
- settlement timing;
- fee currency;
- liquidation semantics.

Unknown broker/account semantics block live authorization.

## 109. ORDER CONSTRAINT / VENUE SAFETY CONTRACT

Before any order reaches a venue adapter, the system must validate:

```yaml
price_tick
quantity_step
minimum_quantity
maximum_quantity
minimum_notional
maximum_notional
price_band
allowed_order_types
time_in_force_rules
post_only_rules
reduce_only_rules
self_trade_prevention_rules
position_mode_constraints
margin_constraints
rate_limit_state
venue_status
instrument_status
account_status
```

### 109.1 Hard invariants

- Invalid tick/lot/precision => reject locally.
- Unsupported order type => reject locally.
- Exceeded account/venue limit => reject locally.
- Unknown venue status => no new order.
- Duplicate order intent => idempotently return the existing authority state.
- A retry cannot create a second economic order.
- Self-trade prevention behavior must be explicit where supported or the relevant strategy must be ineligible where required by policy.

## 110. KILL SWITCH / CIRCUIT BREAKER / MANUAL OVERRIDE CONTRACT

Kill switches are first-class state, never hidden booleans.

Required scopes:

```text
GLOBAL
ACCOUNT
VENUE
INSTRUMENT
STRATEGY
EXECUTION
RESEARCH
AI
```

Required fields:

```yaml
switch_id
scope
state
trigger
activated_at
activated_by
reason_code
release_condition
expiry
approval_requirement
```

States:

`ARMED | ACTIVE | RELEASE_PENDING | RELEASED`

A kill switch activation must be fail-closed for the affected scope.

Manual override cannot weaken a hard safety invariant. Any override that can affect trading authority requires authenticated authorization, explicit reason, expiry, audit trail and, where policy requires, dual approval.

## 111. TIME SYNCHRONIZATION CONTRACT

The system must maintain an explicit clock health object:

```yaml
clock_state
reference_sources
system_offset_ms
venue_offset_ms
max_observed_error_ms
jitter_ms
last_sync_time
sync_method
sync_health
clock_policy_version
```

The time service must use an approved synchronization method and a registered reference set. A critical clock error beyond policy blocks dependent decisions.

`processing_time` is never used as a substitute for `market availability time`.

## 112. EVENT SCHEMA REGISTRY / COMPATIBILITY CONTRACT

Every event type must exist in a versioned schema registry with:

```yaml
event_type
event_version
schema_id
schema_hash
producer_contract
consumer_contract
compatibility_mode
deprecation_date
retention_policy
ordering_policy
```

Compatibility rules:

- backward-compatible payload changes require compatible schema versioning;
- breaking changes require a new major event schema;
- consumers must reject unsupported schema versions safely;
- replay requires the exact historical event schema version.

No producer may change payload semantics without schema-version change.

## 113. TRANSACTIONAL OUTBOX / INBOX CONTRACT

Where a database write and an event publication belong to the same business transaction, the canonical pattern is:

```text
BUSINESS TRANSACTION
→ OUTBOX RECORD
→ COMMIT
→ EVENT DISPATCH
→ CONSUMER INBOX / IDEMPOTENCY CHECK
→ BUSINESS SIDE EFFECT
→ ACK
```

The outbox record must contain:

```yaml
outbox_id
aggregate_id
event_id
event_type
schema_version
payload_hash
created_at
published_at
attempt_count
next_attempt_at
dispatch_state
```

A consumer inbox/idempotency record must preserve:

```yaml
consumer_id
event_id
first_seen
processed_at
processing_state
result_hash
```

No business workflow may rely on an unsafe assumption of database/event atomicity without the registered outbox mechanism.

## 114. CONCURRENCY / LOCKING / BACKPRESSURE CONTRACT

The runtime must define concurrency semantics for every stateful production domain.

Required controls where applicable:

- optimistic version checks;
- pessimistic locks for explicitly identified critical state;
- compare-and-swap semantics for authority state;
- single-writer ownership for account/position authority;
- bounded worker pools;
- bounded queues;
- backpressure;
- retry budgets;
- circuit breakers;
- dead-letter handling;
- poison-message quarantine.

Resource exhaustion must reduce capability or enter safe state; it must never create additional trading authority.

## 115. RETRY / TIMEOUT / CIRCUIT-BREAKER CONTRACT

Every external dependency call must define:

```yaml
timeout
retryable_errors
max_attempts
backoff_policy
jitter_policy
circuit_breaker_threshold
circuit_breaker_window
half_open_policy
safe_fallback
```

Financial side effects are retried only through idempotent command keys.

An exhausted retry budget on a trading-critical dependency causes a safe-state transition rather than unbounded retry.

## 116. SECURITY / SECRETS / IAM IMPLEMENTATION CONTRACT

Secrets must never exist in source code, test fixtures, logs, event payloads or decision records.

Required secret lifecycle:

`ISSUE → STORE → USE → ROTATE → REVOKE → AUDIT`

Required controls:

- least privilege;
- environment separation;
- secure secret storage;
- rotation policy;
- revocation procedure;
- service identity;
- credential ownership;
- access audit;
- break-glass process;
- no-secret logging rule.

High-impact actions must be capability-scoped and authenticated.

Where policy marks an action as dual-control, two independent authorized approvals are required.

## 117. CONFIGURATION / POLICY LIFECYCLE CONTRACT

Runtime configuration must be separated into:

```text
CODE
SCHEMA
POLICY
PARAMETER
MARKET PROFILE
SECRET
RUNTIME STATE
```

Each changeable artifact requires:

```yaml
artifact_id
artifact_type
version
effective_from
effective_to
scope
created_by
approved_by
status
checksum
rollback_version
change_request_id
```

Effective-time selection must be deterministic and point-in-time reproducible.

No environment variable or local configuration file may silently override a higher-authority policy.

## 118. NUMERICAL DETERMINISM / ROUNDING CONTRACT

Production economic calculations must define:

- numerical type/precision;
- rounding mode;
- tick/lot normalization;
- currency conversion rounding;
- fee rounding;
- P&L rounding;
- quantity truncation/rounding;
- comparison tolerances;
- serialization precision.

Replay determinism is evaluated after applying the documented numerical tolerance.

A comparison that changes an admission decision because of undocumented floating-point noise is a contract defect.

## 119. ACCOUNTING / FEE / FUNDING / SETTLEMENT CONTRACT

Every production scope must define the economic accounting model for:

- commission;
- exchange fees;
- maker/taker classification;
- spread cost;
- funding;
- financing;
- borrow;
- rebates;
- taxes/levies where applicable;
- roll cost;
- settlement cost;
- conversion FX;
- realized P&L;
- unrealized P&L;
- cash movements.

The outcome engine and reconciliation engine must use the same certified accounting semantics.

A discrepancy between execution economics and recorded outcome must be classified rather than silently absorbed.

## 120. DATASET MANIFEST / RETENTION / REPRODUCIBILITY CONTRACT

Every certification-eligible dataset must have:

```yaml
dataset_id
dataset_version
manifest_hash
source_versions
coverage_start
coverage_end
instrument_universe_hash
schema_version
normalization_version
quality_policy_version
revision_policy
snapshot_policy
created_at
immutable_uri
retention_policy
checksum
```

Deleting or mutating certification evidence requires a governed retention action; certification evidence is immutable for its retention period.

## 121. MODEL / FEATURE ARTIFACT REPRODUCIBILITY CONTRACT

Every model and production feature artifact must be reproducible from:

```text
CODE VERSION
+ DATASET VERSION
+ FEATURE VERSION
+ PARAMETER VERSION
+ RANDOM SEED
+ ENVIRONMENT MANIFEST
+ DEPENDENCY LOCK
```

For stochastic algorithms, the reproducibility policy must specify whether exact determinism or bounded numerical equivalence is required.

## 122. ENVIRONMENT / BUILD REPRODUCIBILITY CONTRACT

A release must be reproducible from a pinned environment manifest containing:

- language/runtime version;
- dependency lockfile/hash;
- OS/runtime assumptions;
- configuration artifact hashes;
- build tool version;
- schema/migration revision;
- model/feature artifacts;
- container or environment image identity where used.

The release manifest must uniquely identify the resulting executable artifact.

## 123. RELEASE SIGNING / ROLLBACK / ACTIVATION CONTRACT

A production release requires:

```text
BUILD → VERIFY → SIGN/OFFICIALIZE → CERTIFY → APPROVE → ACTIVATE
```

Activation requires a known rollback target.

Rollback must restore the last certified release and may not silently restore an uncertified state.

A failed health gate after activation must follow the registered rollback or safe-state policy.

## 124. OPERATOR INTERVENTION CONTRACT

Operator interventions must be explicit commands, not database edits.

Every high-impact intervention requires:

```yaml
command_id
operator_id
scope
requested_action
reason_code
requested_at
approval_state
expiry
result
```

Direct mutation of production authority tables outside the approved command path is prohibited.

## 125. RESEARCH DATA SPLIT / VINTAGE CONTRACT

Every predictive research dataset must define:

```yaml
train_period
validation_period
test_period
embargo_period
purge_period
regime_coverage
instrument_coverage
universe_reconstruction_method
revision_policy
feature_generation_version
label_version
```

The test set cannot be used as a tuning loop input without creating a new certification scope and evidence trail.

## 126. STRATEGY PARAMETER / SEARCH REGISTRY CONTRACT

Every production strategy must expose a versioned parameter registry describing:

- parameter name;
- semantic meaning;
- allowed range;
- default;
- selected value;
- selection method;
- search budget;
- training/validation scope;
- sensitivity evidence;
- change impact;
- certification dependency.

Hidden strategy constants are prohibited for decision-bearing behavior.

## 127. HEALTH / SLO / AUTHORITY CONTRACT

System health must distinguish:

`HEALTHY | DEGRADED | SAFE_MODE | HALTED | RECONCILIATION_REQUIRED | UNKNOWN`

Each critical dependency needs versioned thresholds for:

- latency;
- availability;
- freshness;
- error rate;
- backlog;
- sequence integrity;
- resource utilization;
- dependency health.

A dashboard state alone never grants authority. Authority is derived from machine-evaluated predicates and evidence.

## 128. INCIDENT / PROBLEM / POSTMORTEM CONTRACT

Critical incidents require:

```yaml
incident_id
severity
first_seen
last_seen
scope
impact
trigger
mitigation
safe_state
recovery_event
root_cause
related_decisions
related_orders
related_positions
corrective_action
preventive_action
postmortem_status
```

A production incident that can materially affect profitability, safety or authority must create an auditable remediation or change request.

## 129. R1 ARTIFACT EXISTENCE CONTRACT

R1 `CODE_READY` cannot be declared from prose alone.

The following artifacts must physically exist and be versioned:

```text
contracts/domain/*
contracts/events/*
contracts/enums/*
contracts/state/*
contracts/policies/*
contracts/engine_registry.*
contracts/traceability.*
contracts/acceptance_matrix.*
contracts/reason_codes.*
migrations/*
schemas/*
tests/contract/*
tests/schema/*
tests/replay/*
tests/failure/*
tests/lineage/*
tests/consumer/*
docs/runbooks/*
docs/market_profiles/*
configs/*
```

R1 status is `FALSE` when any critical artifact is absent, malformed, unversioned or untraceable.

## 130. ENGINE CONTRACT REGISTRY MATERIALIZATION

The 96-engine matrix in Section 99.66 is the authoritative routing baseline. Before R1, each engine row must materialize into a machine-readable contract record with at least:

```yaml
engine_id
engine_name
purpose
non_purpose
orchestrator
caller
inputs
outputs
dependencies
state
transitions
invariants
hard_vetoes
failure_modes
error_codes
fallback
recovery
success_event
failure_event
persistence_target
downstream_consumer
outcome_link
feedback_link
versioning
security
observability
performance_target
replay_behavior
acceptance_tests
certification_scope_dependencies
```

A row in the routing matrix without a materialized engine contract is a `CODE_READY = FALSE` condition.

## 131. CANONICAL ENGINE EVENT NAMING

Unless an engine contract explicitly defines a domain-specific event name, the canonical event family is:

```text
<domain>.<engine_name_normalized>.succeeded.v1
<domain>.<engine_name_normalized>.failed.v1
```

Domain-specific event subjects remain governed by Section 99.32 and the Event Schema Registry.

## 132. DECISION AUTHORITY GATE EVALUATION CONTRACT

Final trade authorization must be produced by a single deterministic authority evaluator that computes the complete predicate set from the current versioned state.

The evaluator must return:

```yaml
authorization_id
decision_id
scope
all_predicates
failed_predicates
unknown_predicates
reason_codes
risk_state
capital_state
reconciliation_state
certification_scope_match
final_authorized
policy_versions
computed_at
```

`final_authorized = true` only when every hard predicate is true.

No downstream engine may elevate `false` or `unknown` to `true`.

## 133. SAFE-STATE LATTICE

The runtime must define an ordered safety lattice:

```text
TRADING_ENABLED
    ↓
DEGRADED
    ↓
SAFE_MODE
    ↓
RECONCILIATION_REQUIRED
    ↓
HALTED
```

Components may force a transition toward a safer state, but no component may independently transition toward a less-safe state without satisfying the registered recovery predicates.

## 134. CERTIFICATION REVOCATION CONTRACT

R4 is continuously revocable for the certified scope.

Any loss of:

- required data entitlement;
- required data quality;
- required point-in-time capability;
- required execution capability;
- required risk/capital policy;
- required calibration;
- required edge lower bound;
- required capacity;
- required operational health;
- required reconciliation cleanliness;
- required model/feature/strategy version integrity

causes:

`R4_REVOKED → LIVE_AUTHORIZED = FALSE`

Revocation is immediate; reactivation requires the defined recertification or recovery path.

## 135. R1 IMPLEMENTATION READINESS MATRIX

The following classification distinguishes **contract completeness** from **actual evidence of implementation**.

| Domain | Contract status after V2.2.3 | Code-ready condition | Evidence required before R1=TRUE |
|---|---|---|---|
| Governance / policy | ✅ CLOSED | Policy/schema/approval artifacts materialized | Registry + tests + evidence |
| Data source / entitlement | ✅ CLOSED | Source registry + entitlement records | Real entitlement evidence |
| Raw ingestion | ✅ CLOSED | Immutable adapter contract implemented | Live source capture |
| Temporal truth | ✅ CLOSED | Snapshot engine + clock contract implemented | PIT replay proof |
| Data quality / failover | ✅ CLOSED | Quality policies + failover tests | Failure injection evidence |
| Normalization / precision | ✅ CLOSED | Unit/currency/precision layer implemented | Golden numerical tests |
| Instrument / calendar | ✅ CLOSED | Instrument lifecycle + calendar registry | Historical universe proof |
| Feature fabric | ✅ CLOSED | Feature contracts registered | Leakage + determinism evidence |
| Market state / regime | ✅ CLOSED | State/transition contracts implemented | Replay + transition tests |
| Liquidity / order flow / microstructure | ✅ CLOSED | Data-tier-specific contracts implemented | Book reconstruction evidence |
| Setup / alpha | ✅ CLOSED | Target + economic mechanism + dependency registry | OOS research evidence |
| Probability | ✅ CLOSED | Calibration policy + versioned model | Calibration evidence |
| Expectancy / edge | ✅ CLOSED | Cost-aware lower-bound EV | Statistical evidence |
| Strategy eligibility | ✅ CLOSED | Data profile + policy evaluator | Eligibility tests |
| Risk / tail / ruin | ✅ CLOSED | Deterministic calculators + policies | Stress evidence |
| Portfolio / capital / capacity | ✅ CLOSED | Marginal risk/capacity engine | Portfolio/capacity evidence |
| Execution / OMS / venue | ✅ CLOSED | Venue constraints + idempotent command path | Shadow/paper/live execution evidence |
| Position / reconciliation | ✅ CLOSED | External truth sync + blocking rules | Reconciliation evidence |
| Outcome / attribution | ✅ CLOSED | Full decision-to-outcome chain | Golden-path evidence |
| Research / replay | ✅ CLOSED | Versioned dataset + replay registry | Deterministic replay evidence |
| Model / feature risk | ✅ CLOSED | Artifact reproducibility + drift gates | Model-risk evidence |
| AI | ✅ CLOSED | AI gateway + authority boundaries + audit | AI governance tests |
| Security / secrets | ✅ CLOSED | IAM/secrets/approval implementation | Security evidence |
| Observability / incident | ✅ CLOSED | Machine health predicates + runbooks | Incident/failure evidence |
| Backup / recovery | ✅ CLOSED | Restore-tested artifacts | Recovery evidence |
| Release / rollback | ✅ CLOSED | Reproducible manifest + rollback target | Release evidence |
| Certification | ✅ CLOSED | Evidence/traceability/adversarial engine | Gate evidence |

**Interpretation:** every row is now contractually closed, but `R1=TRUE` still requires the physical implementation artifacts and their evidence. This distinction is mandatory.

## 136. R1 ENTRY GATE

R1 may be marked `TRUE` only if all of the following are true:

```text
ALL_CRITICAL_CONTRACTS_MATERIALIZED
AND ALL_SCHEMAS_VERSIONED
AND ALL_EVENTS_REGISTERED
AND ALL_STATE_MACHINES_REGISTERED
AND ALL_POLICIES_REGISTERED
AND ALL_96_ENGINE_CONTRACTS_MATERIALIZED
AND DB_SCHEMA_AUTHORITY_ESTABLISHED
AND MIGRATION_PATH_VERIFIED
AND TRACEABILITY_MATRIX_PRESENT
AND ACCEPTANCE_MATRIX_PRESENT
AND REASON_CODE_REGISTRY_PRESENT
AND CONTRACT_TEST_SUITE_PRESENT
AND FAILURE_TEST_SKELETON_PRESENT
AND REPLAY_TEST_SKELETON_PRESENT
AND SECURITY_CONTRACT_IMPLEMENTED
AND OBSERVABILITY_CONTRACT_IMPLEMENTED
AND NO_CRITICAL_ORPHANS
```

A missing real broker, vendor entitlement or production account does **not** block construction of R1; it blocks the later market-profile/operational/live gates. This preserves the distinction between implementation readiness and external certification prerequisites.

## 137. R2 ENTRY GATE

R2 requires, in addition to R1:

```text
GOLDEN_DATASET_PRESENT
AND GOLDEN_REPLAY_PASSING
AND ACCEPTANCE_MATRIX_EXECUTED
AND OBSERVABILITY_ASSERTIONS_EXECUTED
AND FAILURE_INJECTION_SUITE_EXECUTED
AND LINEAGE_TESTS_PASSING
AND CONSUMER_TESTS_PASSING
AND PERSISTENCE_TESTS_PASSING
AND SECURITY_TESTS_PASSING
AND PERFORMANCE_TESTS_PASSING
```

## 138. R3 ENTRY GATE

R3 requires a specific Market Profile and all non-performance operational prerequisites:

```text
SOURCE_ENTITLEMENTS_VALID
AND ACCOUNT_REGISTERED
AND VENUE_CAPABILITIES_VALIDATED
AND MARKET_CALENDAR_VALIDATED
AND NUMERICAL_POLICIES_BOUND
AND EXECUTION_ADAPTER_VALIDATED
AND RECONCILIATION_OPERATIONAL
AND BACKUP_RESTORE_VALIDATED
AND OPERATIONAL_RUNBOOKS_APPROVED
AND SAFE_RECOVERY_TESTED
AND COMPLETE_NON_PERFORMANCE_EVIDENCE_PACKAGE
```

R3 remains non-authorizing.

## 139. R4 ENTRY GATE

R4 requires the exact certification scope to pass:

```text
DATA_SUFFICIENCY_PASS
AND TEMPORAL_TRUTH_PASS
AND REPLAY_PASS
AND BACKTEST_PASS
AND LEAKAGE_PASS
AND OVERFITTING_PASS
AND STATISTICAL_PASS
AND MODEL_RISK_PASS
AND EXECUTION_REALISM_PASS
AND COST_REALISM_PASS
AND CAPACITY_PASS
AND PORTFOLIO_RISK_PASS
AND PAPER_PASS
AND SHADOW_PASS
AND MICRO_PASS
AND PROBATION_PASS
AND ADVERSARIAL_EXAM_PASS
AND EVIDENCE_CHAIN_COMPLETE
```

## 140. LIVE AUTHORIZATION RECHECK

Before each new trading authority grant, the current scope must be re-evaluated against:

- current market profile;
- current source entitlements;
- current data quality;
- current clock health;
- current venue state;
- current account state;
- current position state;
- current reconciliation;
- current strategy eligibility;
- current probability/calibration state;
- current net-edge lower bound;
- current risk/capital/capacity state;
- current release integrity;
- current certification validity.

A currently certified release can be `R4` while a specific instant is not `LIVE_AUTHORIZED`.

## 141. FINAL V2.2.3 CLOSURE STATEMENT

The master contract is considered **contractually closed for R1 implementation** when Sections 0–141 and all retained superseded sections are approved and the engine/contract/traceability schemas defined herein are materialized in the repository.

This state means:

```text
THE CONTRACT NO LONGER REQUIRES THE DEVELOPER
TO INVENT MATERIAL TRADING BEHAVIOR.
```

It does **not** mean:

- the software is implemented;
- tests pass;
- profitability is proven;
- a broker is connected;
- live trading is authorized.

The implementation loop remains:

`CONTRACT → CODE → TEST → ADVERSARIAL TEST → RUN → EVIDENCE → AUDIT → ACCEPT → NEXT`

The production authority loop remains:

`R1 → R2 → R3 → R4 → LIVE_AUTHORIZED`

with immediate fail-closed revocation whenever a hard predicate becomes invalid.


---

# V2.2.4 — R1 ARTIFACT MATERIALIZATION AMENDMENT

**Document status:** MASTER IMPLEMENTATION CONTRACT — R1 CONTRACT ARTIFACT MATERIALIZATION EDITION  
**Version:** 2.2.5  
**Supersedes:** V2.2.3 for any conflicting materialization wording only.  
**Artifact package:** `trading_system_r1_code_ready_v2_2_5/`

## 142. R1 ARTIFACT MATERIALIZATION

The V2.2.3 contract surface is now materialized into a repository contract package containing:

- `contracts/domain/`
- `contracts/engines/` — exactly 96 machine-readable engine contracts
- `contracts/events/`
- `contracts/enums/`
- `contracts/state/`
- `contracts/policies/`
- `schemas/`
- `policies/`
- `events/`
- `state/`
- `migrations/versions/`
- `tests/`
- `evidence/r1/`
- `docs/DEVELOPER_CONSTITUTION_V1_1.md`

The artifact package is part of the implementation baseline and is versioned with this master contract.

## 143. R1 STATUS TRUTH RULE

The following states are distinct and machine-readable:

```text
CONTRACT_CLOSED
R1_ARTIFACTS_MATERIALIZED
R1_CODE_READY
R2_TEST_READY
R3_OPERATIONALLY_LIVE_READY
R4_PROFITABILITY_CERTIFIED
LIVE_AUTHORIZED
```

Materialization of the contract package proves only `R1_ARTIFACTS_MATERIALIZED = TRUE` after the artifact-integrity gate passes. It does not manufacture runtime implementation evidence, profitability, market entitlements, operational safety or live authorization.

`R1_CODE_READY = TRUE` requires the complete R1 entry predicates in Section 136 plus successful execution of the applicable implementation evidence tests.

## 144. CANONICAL ENGINE CALLER RULE

Every engine is invoked through its declared orchestrator dispatcher:

```text
<Orchestrator>.dispatch(engine_id, correlation_id, causation_id, typed_input)
```

Direct hidden engine-to-engine calls are prohibited when an orchestrator boundary exists. The orchestrator owns sequencing, admission, retries, transaction boundaries and event publication. The engine owns only its declared domain calculation/state transition.

## 145. ENGINE RUNTIME LIFECYCLE

All engines use the common runtime execution state unless an engine-specific contract explicitly declares a stricter state machine:

```text
IDLE → VALIDATING → READY → RUNNING → SUCCEEDED
                         ↓         ↓
                      BLOCKED ← FAILED → RECOVERING → READY
```

A failed or blocked engine cannot silently return a successful result. Recovery requires dependency, policy and state revalidation.

## 146. ARTIFACT VERSION BINDING

All materialized contract artifacts in the R1 package must resolve to `contract_version = 2.2.5`. Any package artifact with a conflicting contract version is an R1 blocking defect.

## 147. DEVELOPER CONSTITUTION BINDING

`docs/DEVELOPER_CONSTITUTION_V1_1.md` is binding implementation policy. It does not supersede the Master Contract; it operationalizes the Master Contract for developers, reviewers and AI-assisted coding agents.

## 148. MATERIALIZATION VERIFICATION

The package must pass:

```text
96 ENGINE CONTRACTS
+ 192 ENGINE EVENTS
+ DOMAIN CONTRACT INVENTORY
+ STATE CONTRACTS
+ POLICY REGISTRY
+ JSON SCHEMAS
+ TRACEABILITY MATRIX
+ ACCEPTANCE MATRIX
+ MIGRATION DECLARATION
+ CONTRACT INTEGRITY TESTS
+ DEVELOPER CONSTITUTION
```

before the artifact materialization gate is considered PASS.

## 149. NO GUARANTEE CLAUSE

No implementation document, code package, model, backtest, simulation or constitution can guarantee future trading profit. The system's measurable engineering objective remains durable positive net expectancy under bounded and explicitly governed risk. Certification must remain empirical and scope-specific.

## 150. FINAL IMPLEMENTATION HANDOFF

The project is no longer at the idea-definition stage. The master contract, R1 contract closure and R1 contract artifacts are materialized. The next implementation phase is software construction and evidence generation under the binding Developer Constitution.

The mandatory loop remains:

`CONTRACT → CODE → TEST → RUN → EVIDENCE → AUDIT → ACCEPT → NEXT`


---

# V2.2.5 — NORMATIVE HARDENING & REAL-WORLD PERFORMANCE AMENDMENT

**Document status:** CURRENT MASTER IMPLEMENTATION CONTRACT — HARDENED BASELINE  
**Version:** 2.2.5  
**Authority:** This section is normative and overrides conflicting retained V2.2.x wording. It does not weaken any previously stricter safety, evidence, fail-closed, lineage, reconciliation, or certification requirement.  
**Purpose:** Remove remaining implementation ambiguity discovered during full-contract adversarial review and bind the engineering system to safe, reproducible, economically realistic production behavior.

## 151. CANONICAL MASTER VERSION / PRECEDENCE

The canonical active master is exactly:

```text
MASTER_CONTRACT_VERSION = 2.2.5
```

The active precedence order is:

```text
V2.2.5 MASTER CONTRACT
    ↓
V2.2.4 R1 ARTIFACT MATERIALIZATION HISTORY
    ↓
V2.2.3 R1 CODE-READY CLOSURE HISTORY
    ↓
V2.2.2 NORMATIVE AMENDMENTS
    ↓
V2.1 / V1 RETAINED BASELINE HISTORY
    ↓
CODE
```

Retained historical sections are informative or lower-precedence normative history only where not superseded. No developer, parser, generator or reviewer may select a lower-precedence rule when a V2.2.5 rule exists.

`V2.2.5` is the only version eligible for new implementation artifacts, active policy binding, active certification lineage and new production decision records.

## 152. FREEZE CRITERION CANONICALIZATION

There is exactly one architectural/contract freeze condition:

```text
ARCHITECTURE_FROZEN = TRUE
iff
ALL_ACTIVE_NORMATIVE_SECTIONS_APPROVED
AND
NO_UNRESOLVED_CRITICAL_AMBIGUITY
```

The phrase `Sections 0–99` is historical and MUST NOT be used as a current freeze criterion.

The current freeze review covers Sections 0–151 and all retained normative material after precedence resolution.

## 153. R1 SEMANTIC CLARIFICATION

`R1_ARTIFACTS_MATERIALIZED` means the versioned contract artifact package exists and its integrity tests pass.

`R1_CODE_READY` means the implementation repository satisfies the R1 entry predicates and applicable implementation evidence tests have passed.

These are distinct:

```text
R1_ARTIFACTS_MATERIALIZED != R1_CODE_READY
```

The artifact package MUST be rematerialized for `contract_version = 2.2.5` before R1 artifact status can be re-certified after this amendment.

## 154. CANONICAL DECISION AUTHORITY PREDICATE

Final trading authority MUST be evaluated by one deterministic authority evaluator from one versioned decision snapshot.

The canonical economic gate is:

```text
EV_LOWER_BOUND
- UNCERTAINTY_BUFFER
> MINIMUM_EDGE_FLOOR
```

A positive point estimate, average expectancy, or raw `NET_EV` value MUST NOT substitute for this lower-bound gate where uncertainty-aware EV is applicable.

If a strategy explicitly has no probability/EV model, the strategy contract MUST declare that fact and define its alternative admissibility predicate. A developer MUST NOT infer such an exception.

## 155. PROBABILITY GATE SEMANTICS

`PROBABILITY = CALIBRATED_OR_APPROVED_POLICY` is not sufficient as a free-form bypass.

The canonical rule is:

```text
IF strategy.requires_probability = TRUE
    THEN calibrated probability predicates MUST PASS
ELSE
    probability requirement MUST be explicitly NOT_APPLICABLE
    AND the strategy contract MUST define the alternative admissibility method
```

An approved policy may define the calibration method or its required evidence; it may not silently waive a required probability gate.

## 156. AUTHORIZATION LEASE, SNAPSHOT BINDING AND TOCTOU CONTROL

Every execution authorization is a short-lived, single-purpose, version-bound lease.

Minimum authorization record:

```yaml
authorization_id: UUID
scope_hash: string
state_snapshot_id: UUID
market_snapshot_id: UUID
portfolio_version: string
position_version: string
reconciliation_version: string
policy_hash: string
release_hash: string
issued_at: timestamp_utc
expires_at: timestamp_utc
single_use: boolean
consumed_at: timestamp_utc|null
```

`SUBMIT_ALLOWED` requires all of the following:

```text
authorization exists
AND authorization not expired
AND authorization not consumed
AND scope hash matches current scope
AND release hash matches current release
AND required state versions still match
AND required safety predicates still pass
```

A state change between authorization and venue submission MUST invalidate the authorization unless the affected change is explicitly certified as non-material for the exact authorization scope.

This rule exists to prevent time-of-check/time-of-use authority races.

## 157. MANUAL OVERRIDE / KILL SWITCH AUTHORITY BOUNDARY

Manual control, kill switches and operator controls may only reduce, suspend, or revoke trading authority.

They MUST NOT directly grant, enlarge, or restore trading authority.

```text
MANUAL_OVERRIDE → can BLOCK / HALT / SAFE_MODE / REVOKE
MANUAL_OVERRIDE → cannot GRANT / ENLARGE / BYPASS
```

Trading authority restoration MUST pass through the deterministic authority evaluator and all current certification/operational predicates.

## 158. EMERGENCY / RISK-REDUCTION AUTHORITY

Fail-closed behavior MUST distinguish opening risk from reducing existing risk.

Canonical operation classes:

```text
NEW_ENTRY
POSITION_INCREASE
NORMAL_MODIFY
RISK_REDUCTION
EMERGENCY_EXIT
KNOWN_ORDER_CANCEL
```

`NEW_ENTRY` and `POSITION_INCREASE` are blocked by any hard authority failure.

`RISK_REDUCTION`, `EMERGENCY_EXIT` and `KNOWN_ORDER_CANCEL` may continue only through separately certified safe paths whose exact guards, venue semantics and reconciliation behavior are explicitly defined by policy.

Unknown position or unknown order state MUST NOT be treated as permission to create a new financial action.

## 159. UNKNOWN ORDER RECOVERY

The canonical unresolved-order lifecycle is:

```text
SUBMITTED
  ↓ timeout / uncertain acknowledgement
UNKNOWN
  ↓ external order reconciliation
KNOWN_FILLED
KNOWN_REJECTED
KNOWN_CANCELLED
KNOWN_EXPIRED
RECONCILIATION_REQUIRED
```

An `UNKNOWN` order MUST NOT be blindly retried.

Any retry MUST prove idempotency and external-state safety before another financial side effect is permitted.

## 160. CERTIFICATION REVOCATION AND IN-FLIGHT EFFECTS

Loss of any R4 prerequisite MUST immediately revoke new trading authority.

The revocation path is:

```text
CERTIFICATION_PREREQUISITE_INVALID
→ R4_REVOKED
→ LIVE_AUTHORIZED = FALSE
→ NEW_ENTRY BLOCKED
→ OPEN_ORDER_POLICY EVALUATED
→ POSITION_POLICY EVALUATED
→ RISK_REDUCTION / EMERGENCY PATH AS APPLICABLE
→ AUDIT EVENT
```

An in-flight order or already-open position is not silently assumed safe merely because authorization existed earlier. The current operational safety state determines its subsequent handling.

## 161. CERTIFICATION SCOPE EXACT-MATCH ENFORCEMENT

Every R4 certificate MUST have:

```yaml
certification_scope_id: UUID
certification_scope_hash: string
```

The scope hash MUST cover, at minimum:

```text
market_profile
instrument_universe
data_profile
strategy_version
feature_version
model_version
parameter_version
cost_model_version
execution_model_version
risk_policy_version
capital_policy_version
time_window
venue_scope
release_hash
```

A certified release may authorize only when:

```text
CURRENT_SCOPE_HASH == CERTIFIED_SCOPE_HASH
```

unless an explicit contract-defined equivalence rule exists and independently valid evidence proves that equivalence.

## 162. KILL-SWITCH PRECEDENCE

Effective kill-switch state is the most restrictive state across all applicable scopes.

At minimum:

```text
GLOBAL
ACCOUNT
VENUE
INSTRUMENT
STRATEGY
EXECUTION
```

are evaluated as a restrictive intersection. A higher-level halt cannot be cleared by a lower-level enablement.

`RESEARCH` and `AI` kill switches govern their own scopes and may only affect trading authority when a separately declared safety rule says so.

## 163. NUMERICAL REPRESENTATION / FINANCIAL DETERMINISM

The following values are decision-bearing financial quantities and MUST NOT rely on unspecified binary floating-point behavior as economic truth:

```text
price
quantity
notional
fee
commission
spread_cost
slippage_cost
impact_cost
funding
financing
borrow
exchange_fee
roll_cost
cash
capital
margin
risk_budget
risk_requested
risk_approved
position_value
gross_pnl
net_pnl
realized_pnl
unrealized_pnl
EV_POINT
EV_LOWER_BOUND
EV_UPPER_BOUND
minimum_edge_floor
```

These values MUST use an explicit decimal/fixed-point representation with versioned precision and rounding policies.

The active numerical policy MUST define:

```text
precision
scale
rounding_mode
tick_rounding
lot_rounding
fee_rounding
currency_conversion_rule
NaN/Infinity rejection
overflow behavior
```

Ratios, probabilities and statistical scores may remain floating-point where appropriate, but the contract MUST specify the numerical tolerance used for certification/replay.

## 164. CURRENCY / ACCOUNTING DETERMINISM

All multi-currency valuation and P&L calculations MUST specify:

```text
base_currency
FX source
FX snapshot timestamp
FX conversion direction
valuation timestamp
fee currency
funding currency
rounding policy
```

No developer may choose a convenient FX timestamp or valuation price during implementation.

## 165. POLICY PRECEDENCE / OVERLAP CONTROL

For decision-bearing policies, overlapping active policies with the same scope and family are prohibited unless an explicit precedence rule exists.

Canonical precedence for hard safety constraints is:

```text
SECURITY / SYSTEM SAFETY
>
COMPLIANCE
>
ACCOUNT CEILING
>
PORTFOLIO CEILING
>
MARKET PROFILE CONSTRAINT
>
STRATEGY ELIGIBILITY
>
EXECUTION CONSTRAINT
>
OPTIMIZATION PREFERENCE
>
AI RECOMMENDATION
```

A lower layer may only further restrict a higher layer; it may never weaken a hard ceiling.

## 166. POLICY, CLOCK AND STATE VERSION BINDING

Decision-bearing policy application MUST identify the exact active policy set by hash and version.

Time semantics MUST distinguish:

```text
wall_clock
monotonic_clock
venue_clock
event_time
availability_time
```

Expiry, timeout, latency and lease duration calculations MUST use an approved monotonic reference where appropriate. Wall-clock timestamps remain the audit record of when an event occurred.

## 167. EVENT CONSUMER LIVENESS / BUSINESS EFFECT SEMANTICS

`consumer_exists` is not equivalent to `consumer_healthy`.

Critical consumers MUST expose:

```text
consumer_status
last_processed_event_id
consumer_lag
processing_error_rate
retry_count
dead_letter_count
terminal_failure_state
```

Transport is at-least-once unless explicitly otherwise certified. Financial business effects MUST be idempotent even when delivery is duplicated.

A duplicate event MAY be delivered more than once; a duplicate financial state transition MUST NOT be applied more than once.

## 168. RECONCILIATION AUTHORITY

Where broker, venue, internal state or settlement sources disagree:

```text
UNKNOWN
→ RECONCILIATION_REQUIRED
```

until an explicitly registered source hierarchy and reconciliation policy resolves the conflict.

The resolver MUST record:

```text
source_priority
source_observations
resolution_rule
resolved_by
resolution_time
resolution_evidence
```

Manual database edits MUST NOT substitute for reconciliation resolution.

## 169. SAMPLE-SUFFICIENCY / EFFECTIVE-INFORMATION STANDARD

R4 evidence MUST distinguish nominal sample size from effective independent information.

At minimum, applicable certification scopes MUST expose:

```text
nominal_observations
winning_observations
losing_observations
effective_sample_size
ess_method
regime_coverage
instrument_coverage
session_coverage
execution_mode_coverage
tail_event_coverage
```

The ESS method MUST be versioned. The developer may not silently choose an ESS method during implementation.

## 170. STATISTICAL METRIC DEFINITIONS

Certification metrics MUST have canonical definitions, including where applicable:

```text
Sharpe
Sortino
Calmar
profit_factor
max_drawdown
recovery_factor
VaR
Expected Shortfall
Brier score
ECE
calibration error
```

Each metric must declare its return frequency, annualization method, risk-free assumption, overlapping-return treatment, missing-data treatment and numerical tolerance where relevant.

A metric without a canonical calculation specification is not a certification-grade metric.

## 171. ATTRIBUTION QUALITY GATE

`unexplained_residual` MUST be measured and policy-bounded.

A feedback or learning process MUST NOT treat an attribution result as causally trustworthy when:

```text
attribution_quality < MIN_ATTRIBUTION_QUALITY
OR
abs(unexplained_residual) > MAX_UNEXPLAINED_ATTRIBUTION
```

unless an explicitly approved research-only mode says otherwise.

## 172. AI FRESHNESS AND CONTEXT BINDING

Every AI output used anywhere in the decision process MUST include:

```text
ai_output_id
model_version
prompt_or_policy_version
context_snapshot_id
input_versions
created_at
expires_at
scope_hash
recommendation_type
```

A stale or expired AI output MUST NOT be used as current context.

AI remains a governed recommendation/research component. It MUST NOT become a hidden authority dependency.

## 173. CONTINUOUS CERTIFICATION VALIDITY

`R4_PROFITABILITY_CERTIFIED` is not permanent.

Certification validity is continuously conditional on:

```text
scope match
current data validity
current execution reality
current cost model
current strategy eligibility
current drift state
current risk/capacity state
current release integrity
current operational safety
```

A certification may remain recorded as historical evidence while current live authorization is revoked.

## 174. ECONOMIC SUCCESS / REAL-WORLD PROFITABILITY DISCIPLINE

The engineering target is not raw trade count, hit rate or backtest Sharpe. The target is:

```text
DURABLE POSITIVE NET EXPECTANCY
UNDER REAL COSTS
WITHIN VERIFIED CAPACITY
UNDER BOUNDED RISK
WITH CONTROLLED DRAWDOWN
AND REVERSIBLE DEPLOYMENT
```

The following are mandatory engineering principles for economic viability:

1. Every production economic claim MUST be net of applicable commission, spread, slippage, impact, funding/financing, borrow, exchange fees, roll and other known costs.
2. Every strategy MUST be tested against capacity and liquidity limits; EV MUST NOT be assumed constant as capital size increases.
3. Edge half-life MUST be compared with realistic execution time.
4. Strategy performance MUST be segmented by regime, instrument, session, venue, execution mode and cost environment where applicable.
5. Shared alpha factors MUST share risk budgets even when strategy names differ.
6. The system MUST prefer no-trade over negative or uncertainty-adjusted unattractive expectancy.
7. Capital preservation and bounded drawdown take priority over maximizing nominal return.
8. Production promotion MUST be incremental and reversible through shadow → paper → micro → probation before durable scale.
9. No single successful backtest window may be treated as durable evidence of future market profitability.
10. No learning loop may promote a hypothesis without preserving the rejected alternatives, search budget, selection rule and evidence lineage.

These are engineering constraints for increasing the probability of durable success; they are not promises of future profit.

## 175. FAILURE-TO-EXPLAIN BLOCK

A production-critical subsystem is not ready for live use if the platform cannot answer:

```text
WHY DID IT TRADE?
WHY DID IT REFUSE TO TRADE?
WHICH DATA WAS USED?
WHICH POLICY WAS ACTIVE?
WHICH CERTIFICATION SCOPE APPLIED?
WHICH AUTHORIZATION WAS GRANTED?
WHAT STATE CHANGED?
WHAT ORDER WAS SENT?
WHAT HAPPENED EXTERNALLY?
WHY WAS THE OUTCOME ATTRIBUTED THIS WAY?
```

This extends the existing observability contract from operational health to decision explainability.

## 176. IMPLEMENTATION FREEZE AFTER HARDENING

After V2.2.5 is approved, the next mandatory sequence is:

```text
V2.2.5 CONTRACT FREEZE
→ REMATERIALIZE ALL R1 ARTIFACTS TO 2.2.5
→ REGENERATE MANIFEST / HASHES
→ RUN R1 INTEGRITY SUITE
→ RE-EXECUTE ADVERSARIAL CONTRACT EXAM
→ CODE
→ TEST
→ RUN
→ EVIDENCE
→ AUDIT
→ ACCEPT
```

No prior V2.2.4 artifact package may be silently treated as V2.2.5 evidence.

## 177. FINAL V2.2.5 HARDENED AUTHORITY CHAIN

```text
ARCHITECTURE_FROZEN
    ↓
R1_ARTIFACTS_MATERIALIZED
    ↓
R1_CODE_READY
    ↓
R2_TEST_READY
    ↓
R3_OPERATIONALLY_LIVE_READY
    ↓
R4_PROFITABILITY_CERTIFIED (EXACT SCOPE)
    ↓
CURRENT OPERATIONAL SAFETY
    ↓
LIVE_AUTHORIZED
```

At any point, the first invalid hard predicate terminates downstream authority.

`R4` is evidence of a validated historical scope. `LIVE_AUTHORIZED` is a current runtime state, never a permanent property.

## 178. FINAL NON-NEGOTIABLE RULE

> **The developer may optimize implementation details, but may never invent material trading behavior, weaken a hard safety rule, bypass evidence, or convert uncertainty into authority. Where the contract is silent, implementation stops and the change-control process begins.**


## 179. V2.2.5 CANONICAL NUMERIC SCHEMA OVERRIDE

The `float` notation appearing in retained legacy examples is non-authoritative wherever the field represents a decision-bearing financial quantity. For such fields, Sections 163 and 179 control and the canonical type is `financial_number`.

This override is normative and exists solely to eliminate ambiguity between retained examples and the active V2.2.5 numerical contract.


---

# V3.0.0 — PRE-CODE COMPLETION AND DEVELOPER HANDOFF AMENDMENT

**Change Request:** `CR-V3.0.0-PRECODE-001`  
**Status:** `CURRENT REVIEW CANDIDATE / NOT IMPLEMENTED / NOT LIVE AUTHORIZED`  
**Authority:** This amendment has precedence over conflicting retained V2.x history. Stricter retained safety, evidence, reconciliation, lineage and certification rules remain binding.  
**Purpose:** Adopt the 900-question control surface, close explicit ownership gaps, prevent developer invention, and create a machine-readable implementation handoff.

## 180. Truth and readiness separation

```text
DESIGN_PACKAGE_INTEGRITY_PASS != R1_CODE_READY
RESEARCH_CANDIDATE != PROFITABLE_STRATEGY
BACKTEST_PASS != R4_PROFITABILITY_CERTIFIED
R4_PROFITABILITY_CERTIFIED != PERMANENT_LIVE_AUTHORITY
```

Current truth at publication: software is not implemented; all runtime questions are `UNKNOWN / NOT_EXECUTED`; `LIVE_AUTHORIZED = FALSE`.

## 181. 900-question normative control surface

The 237 retained core questions and 663 extended questions are prepared for adoption as mandatory pre-code control requirements under this change request. They become binding for V3.0.0 when the owner accepts this package. The authoritative mapping is `contracts/questions/question_registry.json`. A question is never PASS merely because it exists or is mapped.

## 182. Engine registry expansion: 96 → 112

The retained 96 engines remain. Sixteen engines are added because the 900-question review found decision-bearing responsibilities without an explicit single owner:

| ID | Engine | Orchestrator | Primary output |
|---:|---|---|---|
| 97 | MARKET PROFILE / SCOPE BINDING ENGINE | ScopeGovernanceOrchestrator | ActiveScope/ScopeBlocked |
| 98 | VENUE / BROKER / ACCOUNT CAPABILITY ENGINE | ExternalRealityOrchestrator | CapabilitySnapshot |
| 99 | DETERMINISTIC TRADING AUTHORITY EVALUATOR | AuthorityOrchestrator | AuthorityDecision |
| 100 | AUTHORIZATION LEASE / TOCTOU ENGINE | AuthorityOrchestrator | AuthorizationLease/LeaseRevocation |
| 101 | SMART ORDER ROUTING / VENUE SELECTION ENGINE | ExecutionOrchestrator | RoutePlan |
| 102 | MARKET INTEGRITY SURVEILLANCE ENGINE | IntegrityOrchestrator | IntegrityAssessment/IntegrityAlert |
| 103 | LEGAL / COMPLIANCE ELIGIBILITY ENGINE | ComplianceOrchestrator | ComplianceDecision |
| 104 | COUNTERPARTY / CUSTODY / SETTLEMENT RISK ENGINE | ExternalRealityOrchestrator | CounterpartyRiskDecision |
| 105 | TREASURY / CASH / COLLATERAL ENGINE | CapitalOrchestrator | TreasuryState |
| 106 | ACCOUNTING / PNL / FX VALUATION ENGINE | OutcomeOrchestrator | AccountingSnapshot |
| 107 | CORPORATE ACTION / INSTRUMENT LIFECYCLE ENGINE | MarketProfileOrchestrator | LifecycleAdjustedInstrumentState |
| 108 | REFERENCE PRICE / ORACLE / FIXING ENGINE | MarketIntelligenceOrchestrator | ReferencePriceSnapshot |
| 109 | CYBERSECURITY / SUPPLY-CHAIN INTEGRITY ENGINE | SecurityOrchestrator | SecurityIntegrityDecision |
| 110 | INCIDENT / BCP / DISASTER-RECOVERY ENGINE | OperationsOrchestrator | RecoveryAuthorityDecision |
| 111 | MODEL / STRATEGY ARTIFACT & RELEASE ATTESTATION ENGINE | ReleaseOrchestrator | ReleaseAttestation |
| 112 | DATA ENTITLEMENT / LICENSING ENGINE | DataFoundationOrchestrator | EntitlementDecision |

Exactly 112 engine contracts and 224 canonical engine success/failure event definitions are required for this version.

## 183. Single decision-authority chain

```text
SCOPE BINDING (97)
→ LEGAL/COMPLIANCE (103)
→ DATA/TEMPORAL/LINEAGE VALIDITY
→ STRATEGY/EDGE/PROBABILITY/EV
→ RISK/CAPITAL/COUNTERPARTY
→ EXECUTIVE DECISION
→ DETERMINISTIC AUTHORITY EVALUATOR (99)
→ SINGLE-USE LEASE (100)
→ ROUTE PLAN (101)
→ EXECUTION (56)
→ RECONCILIATION (59)
```

Only Engine 99 grants new-risk authority. Engines 40, 41, 55, 60, 85 and 86 produce vetoes or prerequisites; they cannot bypass Engine 99. Engine 100 prevents time-of-check/time-of-use races.

## 184. Scope and external-input binding

MarketProfile, jurisdiction, broker, venue, account, data entitlement, capital, fee, margin, funding, borrow, latency, fill, impact, capacity and policy values remain `UNBOUND_REQUIRED` until real evidence exists. A developer may implement schema and guards but may not choose material values. UNBOUND blocks only the affected gate and can never increase authority.

## 185. Strategy truth

The strategy catalog contains research archetypes, not promised edges. Every candidate is disabled by default and must pass registered hypothesis, point-in-time data, global trial accounting, purged temporal validation, multiple-testing control, full costs, capacity, tail risk, regime segmentation, independent validation and staged deployment. No strategy name, indicator, AI output or backtest screenshot creates authority.

## 186. Data truth

Every decision-bearing observation carries source, event time, first availability time, receive time, revision/version, quality, entitlement and lineage. RAW data is append-only. Adjusted series never overwrite raw identity. Future, corrected or survivorship-cleaned knowledge cannot leak into historical decisions.

## 187. Statistical truth

Nominal trade count is not effective information. Global trial/search history includes failed and manual trials. Selection, optional stopping, dependence, PBO/DSR and applicable Reality Check/SPA or approved equivalents are declared before final evaluation. Metric definitions and tolerances are versioned.

## 188. Economic truth

Authority requires uncertainty-adjusted lower-bound net EV after all applicable commission, spread, slippage, impact, adverse selection, latency, funding, financing, borrow, exchange, roll, FX and tax-relevant economic effects. Financial quantities use explicit decimal/fixed-point policy. Capacity includes stressed exit, not only entry.

## 189. Execution and external truth

Unknown orders are never blindly retried. Transport may be at-least-once; financial effects are idempotent. Broker/venue/internal disagreement becomes `RECONCILIATION_REQUIRED`. Risk-reduction paths are separate from new-entry authority and require certified guards.

## 190. Risk and survival priority

Capital preservation, bounded drawdown, risk of ruin, tail dependence, liquidation, counterparty failure, liquidity collapse and recovery capacity outrank nominal return. Positive EV never overrides a hard risk, compliance, security, integrity or reconciliation veto.

## 191. Market integrity and compliance

Spoofing, layering, wash, self-match, momentum ignition, venue gaming and prohibited/restricted-product risks are monitored before and after order submission. Profit or opportunity pressure cannot waive these controls. Applicable legal uncertainty blocks affected new risk.

## 192. Cybersecurity and resilience

Signed artifacts, SBOM/provenance, least privilege, separated environments, secret rotation, data/model poisoning defenses, tamper-evident audit, RTO/RPO, runbooks, failure injection and independently reconciled recovery are mandatory. Restart never restores authority by itself.

## 193. AI boundary

AI may research, summarize, propose and challenge. AI cannot grant authority, alter hard limits, change kill switches, write production policy directly, approve its own output or substitute for market/broker/reconciliation truth.

## 194. Question-result semantics

Each result requires QUESTION_ID, QUESTION_VERSION, SCOPE_HASH, APPLICABILITY, CRITICALITY, STATUS, INFORMATION_CLASS, CONTRACT_ID, POLICY_ID, TEST_ID, FAIL_ACTION and—only for PASS—immutable EVIDENCE_ID plus independent approval when required. Production-critical UNKNOWN equals deny/block.

## 195. Developer stop rule

When behavior, numerical value, market semantics, legal applicability, external capability or recovery action is not bound, the developer must stop the affected path and open change control. “Reasonable default” is prohibited for material trading behavior.

## 196. Implementation waves

```text
W0 contracts/schemas/reason-codes/hash manifest
W1 identity, scope, policy, security, temporal truth, lineage
W2 authority evaluator, authorization lease, reconciliation, risk
W3 market data, feature, strategy research, replay/backtest
W4 OMS/execution/routing/counterparty/treasury/accounting
W5 full acceptance, failure injection, security and performance
W6 shadow → paper → micro → probation
W7 scope-exact R4 review → current live authorization
```

No later wave may be used as evidence for an unpassed earlier wave.

## 197. Pre-code handoff gate

`FRAMEWORK_IMPLEMENTATION_MAY_START` only after package integrity passes and the owner accepts this change request. This permits implementation of contracts and fail-closed scaffolding. It does not permit inventing external values, activating strategies or live trading.

## 198. Independent review

The author of a material strategy/model/control cannot be its sole independent validator and production approver. Internal generator checks are integrity evidence, not independent validation.

## 199. Final non-guarantee

The system is engineered to improve the probability of durable positive net expectancy under bounded risk. No contract, strategy, backtest, AI system or developer can guarantee future profit. The correct response to insufficient evidence is no trade.
