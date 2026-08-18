from __future__ import annotations

import argparse
import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / ".env"


def build_content() -> str:
    postgres_password = secrets.token_hex(32)
    pgadmin_password = secrets.token_urlsafe(40)
    return "\n".join(
        [
            "APP_ENV=development",
            "LIVE_TRADING_ENABLED=false",
            "",
            "POSTGRES_HOST=127.0.0.1",
            "POSTGRES_PORT=5432",
            "POSTGRES_DB=trading_system",
            "POSTGRES_USER=trading_app",
            f"POSTGRES_PASSWORD={postgres_password}",
            "",
            "PGADMIN_PORT=5050",
            "PGADMIN_DEFAULT_EMAIL=admin@trading-system.dev",
            f"PGADMIN_DEFAULT_PASSWORD={pgadmin_password}",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create untracked local development secrets")
    parser.add_argument("--force", action="store_true", help="replace an existing .env")
    args = parser.parse_args()

    if TARGET.exists() and not args.force:
        raise SystemExit(".env already exists; refusing to overwrite it")

    temporary = TARGET.with_suffix(".env.tmp")
    temporary.write_text(build_content(), encoding="utf-8")
    os.chmod(temporary, 0o600)
    temporary.replace(TARGET)
    print("created .env with mode 0600; secrets were not printed")


if __name__ == "__main__":
    main()
