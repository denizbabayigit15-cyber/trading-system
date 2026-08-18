from __future__ import annotations

from datetime import UTC, datetime, timedelta

from trading_system.governance.identity import Principal, PrincipalKind
from trading_system.security.boundaries import SecretReference, SecurityContext, attest_artifact


def test_secret_reference_never_fabricates_a_secret(monkeypatch) -> None:
    monkeypatch.delenv("TRADING_TEST_SECRET", raising=False)
    assert SecretReference(env_var="TRADING_TEST_SECRET").resolve() is None


def test_unsigned_artifact_is_not_authority_eligible() -> None:
    now = datetime(2026, 8, 18, tzinfo=UTC)
    principal = Principal(
        principal_id="test",
        kind=PrincipalKind.SERVICE,
        roles=frozenset({"SERVICE"}),
        authenticated_at=now,
        expires_at=now + timedelta(hours=1),
    )
    artifact = attest_artifact("artifact", b"synthetic", signer_id=None)
    context = SecurityContext(principal, artifact, "test")
    assert not context.authority_eligible
