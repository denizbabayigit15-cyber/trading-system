# Foundation verification evidence

Date: 2026-08-18  
Package: `trading-system` 0.1.0  
Authority state: `LIVE_AUTHORIZED=false`

## Passed checks

| Check | Result |
|---|---|
| Python runtime | PASS — CPython 3.14.7 |
| Dependency resolution | PASS — 52 packages resolved; `uv.lock` generated with uv 0.12.5 |
| Dependency synchronization | PASS — 50 packages installed in an isolated environment |
| Unit/contract/schema/failure tests | PASS — 20 tests |
| Ruff lint | PASS |
| Ruff formatting | PASS — 63 files checked |
| Mypy strict mode | PASS — 16 source files |
| Contract and integrity verification | PASS with the declared question-registry blocker |
| Alembic offline migration generation | PASS — 190 lines of PostgreSQL SQL |
| Compose document structure | PASS — pinned PostgreSQL and pgAdmin images verified |
| Python package build | PASS — wheel and source distribution |

The test run emitted one dependency deprecation warning from Starlette's test
client compatibility layer; no application test failed.

## Deliberately not claimed

- The Docker daemon was not available in the packaging sandbox.
- The migration has not yet been applied to the user's local PostgreSQL container.
- The referenced machine-readable 900-question registry was not present in the supplied baseline.
- The 112 catalog entries are registered as `NOT_IMPLEMENTED`; registration is not runtime evidence.
- R1, R2, R3, R4, strategy activation, profitability certification, and live authority remain false.

The local bootstrap run is the next evidence step. It must execute Docker
Compose, apply Alembic revision `0001_foundation`, rerun the checks, and preserve
the resulting output before the next implementation slice begins.
