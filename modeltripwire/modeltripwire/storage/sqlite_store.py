from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from modeltripwire.models.schemas import EvaluationResult


class SQLiteStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _ensure_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluation_results (
                    prompt_id TEXT,
                    prompt_name TEXT,
                    category TEXT,
                    provider_type TEXT,
                    model_name TEXT,
                    prompt_text TEXT,
                    response_text TEXT,
                    refusal_score REAL,
                    compliance_score REAL,
                    leakage_score REAL,
                    harmfulness_score REAL,
                    tripwire_count INTEGER,
                    max_severity INTEGER,
                    tripwires_json TEXT,
                    metadata_json TEXT,
                    timestamp TEXT
                )
                """
            )
            connection.commit()

    def save_results(self, results: Iterable[EvaluationResult]) -> None:
        rows = []
        for result in results:
            rows.append(
                (
                    result.prompt_case.id,
                    result.prompt_case.name,
                    result.prompt_case.category,
                    result.provider_type,
                    result.provider_response.model_name,
                    result.prompt_case.prompt_text,
                    result.provider_response.content,
                    result.scorecard.refusal_score,
                    result.scorecard.compliance_score,
                    result.scorecard.leakage_score,
                    result.scorecard.harmfulness_score,
                    result.tripwire_count,
                    result.max_severity,
                    json.dumps([match.model_dump() for match in result.tripwires_triggered]),
                    json.dumps(result.metadata),
                    result.provider_response.timestamp.isoformat(),
                )
            )
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO evaluation_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()
