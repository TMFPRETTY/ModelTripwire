from __future__ import annotations

import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from uuid import uuid4


def sha256_file(path: str | Path) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()


def make_run_id() -> str:
    return uuid4().hex[:12]


def make_run_label(prefix: str = "run") -> str:
    return f"{prefix}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"


def detect_git_commit(project_root: str | Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() or None
    except Exception:
        return None
