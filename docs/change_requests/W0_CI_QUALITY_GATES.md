# W0 continuous-integration quality gates

Date: 2026-08-18  
Branch: `chore/ci-quality-gates`

## Purpose

Run the repository's fail-closed contract and code-quality checks on every pull
request to `main`, every push to `main`, and an explicit manual dispatch.

## Enforced checks

- the committed 900-question candidate matches deterministic generation;
- contract schemas and integrity hashes validate;
- the complete test suite passes;
- Ruff lint and formatting checks pass;
- strict Mypy checking passes.

## Supply-chain and authority boundaries

- third-party actions are pinned to immutable 40-character commit SHAs;
- workflow permissions are read-only (`contents: read`);
- checkout credentials are not persisted;
- dependency synchronization is locked and all subsequent runs are frozen;
- no secret, deployment, database mutation, strategy activation, or live-trading
  authority is granted by this workflow.

The first successful GitHub-hosted run is required before this configuration is
accepted as executed CI evidence.
