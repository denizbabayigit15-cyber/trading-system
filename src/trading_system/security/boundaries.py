from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field

from trading_system.core.canonical import sha256_digest
from trading_system.governance.identity import Principal


class SecretReference(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    env_var: str = Field(pattern=r"^[A-Z][A-Z0-9_]{2,127}$")
    required: bool = True

    def resolve(self) -> str | None:
        value = os.environ.get(self.env_var)
        if self.required and not value:
            return None
        return value


class ArtifactAttestation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    artifact_id: str = Field(min_length=1)
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    release_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    signed: bool
    signer_id: str | None

    @property
    def eligible(self) -> bool:
        return self.signed and self.signer_id is not None


@dataclass(frozen=True, slots=True)
class SecurityContext:
    principal: Principal
    artifact: ArtifactAttestation
    environment: str

    @property
    def authority_eligible(self) -> bool:
        return self.environment in {"development", "test", "staging"} and self.artifact.eligible


def attest_artifact(
    artifact_id: str, content: bytes, *, signer_id: str | None
) -> ArtifactAttestation:
    content_hash = hashlib.sha256(content).hexdigest()
    return ArtifactAttestation(
        artifact_id=artifact_id,
        content_sha256=content_hash,
        release_hash=sha256_digest({"artifact_id": artifact_id, "content_sha256": content_hash}),
        signed=signer_id is not None,
        signer_id=signer_id,
    )
