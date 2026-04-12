#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ALLOWED_TOP_LEVEL = {
    ".env.example",
    ".github",
    ".gitignore",
    "LICENSE",
    "README.md",
    "UNKNOWN.egg-info",
    "configs",
    "data",
    "docs",
    "modeltripwire",
    "notebooks",
    "outputs",
    "pyproject.toml",
    "scripts",
    "setup.cfg",
    "setup.py",
    "tests",
}


def git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    tracked = git("ls-tree", "--name-only", "HEAD", cwd=repo_root).splitlines()
    tracked = [item.strip() for item in tracked if item.strip()]

    unexpected = sorted(item for item in tracked if item not in ALLOWED_TOP_LEVEL)
    missing_core = sorted(
        item
        for item in ["README.md", "configs", "data", "modeltripwire", "pyproject.toml", "tests"]
        if item not in tracked
    )

    if unexpected or missing_core:
        print("ModelTripwire repo boundary check failed.", file=sys.stderr)
        if unexpected:
            print("Unexpected top-level entries:", file=sys.stderr)
            for item in unexpected:
                print(f"  - {item}", file=sys.stderr)
        if missing_core:
            print("Missing expected core entries:", file=sys.stderr)
            for item in missing_core:
                print(f"  - {item}", file=sys.stderr)
        print(
            "Refusing push because the repo root does not look like a clean ModelTripwire checkout.",
            file=sys.stderr,
        )
        return 1

    print("ModelTripwire repo boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
