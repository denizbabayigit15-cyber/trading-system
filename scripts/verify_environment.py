from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> str:
    # Every executable is resolved locally and every argument is defined by this script.
    completed = subprocess.run(  # noqa: S603
        command, check=True, capture_output=True, text=True
    )
    return (completed.stdout or completed.stderr).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the pinned local development environment")
    parser.add_argument("--skip-docker", action="store_true")
    args = parser.parse_args()

    if sys.version_info[:2] != (3, 14):
        raise SystemExit(f"Python 3.14.x required, got {sys.version.split()[0]}")
    pinned = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
    if sys.version.split()[0] != pinned:
        raise SystemExit(f"Python must match .python-version exactly: {pinned}")

    uv = shutil.which("uv")
    if uv is None:
        raise SystemExit("uv is not available on PATH")
    print(run([uv, "--version"]))
    print(f"Python {sys.version.split()[0]}")

    if not args.skip_docker:
        docker = shutil.which("docker")
        if docker is None:
            raise SystemExit("docker is not available on PATH")
        print(
            run(
                [
                    docker,
                    "version",
                    "--format",
                    "Docker client {{.Client.Version}} / server {{.Server.Version}}",
                ]
            )
        )
        print(run([docker, "compose", "version"]))

    print("PASS: environment version checks")


if __name__ == "__main__":
    main()
