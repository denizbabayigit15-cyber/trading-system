# IBKR paper integration

The `providers` package defines provider-neutral session, contract, market-data, and execution
ports. `IBKRAdapter` is the first concrete implementation and accepts only paper mode. It uses a
transport port so the repository remains testable without installing TWS API or contacting IBKR.

Supported roots are MNQ, MGC, and MBT. Contract metadata is resolved from IBKR at runtime; expiry,
exchange, multiplier, tick size, account identity, permissions, and market-data entitlements are
never invented in code. A contract is not orderable until both permission and entitlement bindings
are present. Continuous futures are not used for orders or real-time subscriptions.

IBKR's official TWS API contract-details flow returns `conId`, local symbol, expiry, trading class,
minimum tick, and trading hours. The API also requires the relevant trading permissions and market
data subscription for real-time data. See the [contract details](https://interactivebrokers.github.io/tws-api/contract_details.html),
[contracts](https://interactivebrokers.github.io/tws-api/contracts.html), and [market-data](https://interactivebrokers.github.io/tws-api/market_data.html)
documentation for the external prerequisites. Those prerequisites remain UNKNOWN/PENDING until
the owner supplies a configured paper TWS or IB Gateway session.

No module in this integration enables `LIVE_AUTHORIZED`, places a live order, or treats API
connectivity as authority. PostgreSQL migration `0008_paper_provider_records` stores immutable
lineage-bearing contract, market-event, and paper-order-event records; secrets and credentials are
not persisted.
