from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from modeltripwire.models.schemas import EvaluationResult, ExperimentRun


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
                CREATE TABLE IF NOT EXISTS experiment_runs (
                    run_id TEXT PRIMARY KEY,
                    run_label TEXT,
                    title TEXT,
                    research_question TEXT,
                    provider_type TEXT,
                    model_name TEXT,
                    dataset_path TEXT,
                    dataset_hash TEXT,
                    config_path TEXT,
                    config_hash TEXT,
                    git_commit TEXT,
                    started_at TEXT,
                    completed_at TEXT,
                    total_cases INTEGER,
                    metadata_json TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluation_results (
                    run_id TEXT,
                    prompt_id TEXT,
                    prompt_name TEXT,
                    category TEXT,
                    scenario TEXT,
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
            columns = {
                row[1] for row in connection.execute("PRAGMA table_info(evaluation_results)").fetchall()
            }
            if "scenario" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN scenario TEXT")
            if "run_id" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN run_id TEXT")
            connection.commit()

    def save_run(self, run: ExperimentRun) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO experiment_runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.run_id,
                    run.run_label,
                    run.title,
                    run.research_question,
                    run.provider_type,
                    run.model_name,
                    run.dataset_path,
                    run.dataset_hash,
                    run.config_path,
                    run.config_hash,
                    run.git_commit,
                    run.started_at.isoformat(),
                    run.completed_at.isoformat(),
                    run.total_cases,
                    json.dumps(run.metadata),
                ),
            )
            connection.commit()

    def save_results(self, results: Iterable[EvaluationResult], run_id: str | None = None) -> None:
        rows = []
        for result in results:
            rows.append(
                (
                    run_id,
                    result.prompt_case.id,
                    result.prompt_case.name,
                    result.prompt_case.category,
                    result.prompt_case.scenario_name,
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
                INSERT INTO evaluation_results (
                    run_id,
                    prompt_id,
                    prompt_name,
                    category,
                    scenario,
                    provider_type,
                    model_name,
                    prompt_text,
                    response_text,
                    refusal_score,
                    compliance_score,
                    leakage_score,
                    harmfulness_score,
                    tripwire_count,
                    max_severity,
                    tripwires_json,
                    metadata_json,
                    timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()
