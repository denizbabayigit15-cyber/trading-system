from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VersionedConfig:
    config_id: str
    version: str
    content_hash: str
    effective: bool = False


class ConfigRegistry:
    def __init__(self) -> None:
        self._configs: dict[tuple[str, str], VersionedConfig] = {}

    def publish(self, config: VersionedConfig) -> None:
        key = (config.config_id, config.version)
        if key in self._configs:
            raise ValueError("configuration version already exists")
        self._configs[key] = config

    def resolve(self, config_id: str, version: str) -> VersionedConfig:
        return self._configs[(config_id, version)]
