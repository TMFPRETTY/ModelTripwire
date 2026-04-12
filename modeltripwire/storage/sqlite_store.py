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
                    benchmark_suite TEXT,
                    difficulty TEXT,
                    expected_risk_type TEXT,
                    evaluation_focus_json TEXT,
                    turns_json TEXT,
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
            if "benchmark_suite" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN benchmark_suite TEXT")
            if "difficulty" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN difficulty TEXT")
            if "expected_risk_type" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN expected_risk_type TEXT")
            if "evaluation_focus_json" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN evaluation_focus_json TEXT")
            if "turns_json" not in columns:
                connection.execute("ALTER TABLE evaluation_results ADD COLUMN turns_json TEXT")
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

    def list_runs(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT run_id, run_label, title, research_question, provider_type, model_name, total_cases, started_at, completed_at, metadata_json
                FROM experiment_runs
                ORDER BY completed_at DESC
                """
            ).fetchall()
        return [
            {
                "run_id": row[0],
                "run_label": row[1],
                "title": row[2],
                "research_question": row[3],
                "provider_type": row[4],
                "model_name": row[5],
                "total_cases": row[6],
                "started_at": row[7],
                "completed_at": row[8],
                "metadata": json.loads(row[9]) if row[9] else {},
            }
            for row in rows
        ]

    def get_run(self, run_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT run_id, run_label, title, research_question, provider_type, model_name,
                       dataset_path, dataset_hash, config_path, config_hash, git_commit,
                       started_at, completed_at, total_cases, metadata_json
                FROM experiment_runs
                WHERE run_id = ? OR run_label = ?
                LIMIT 1
                """,
                (run_id, run_id),
            ).fetchone()
        if row is None:
            return None
        return {
            "run_id": row[0],
            "run_label": row[1],
            "title": row[2],
            "research_question": row[3],
            "provider_type": row[4],
            "model_name": row[5],
            "dataset_path": row[6],
            "dataset_hash": row[7],
            "config_path": row[8],
            "config_hash": row[9],
            "git_commit": row[10],
            "started_at": row[11],
            "completed_at": row[12],
            "total_cases": row[13],
            "metadata": json.loads(row[14]) if row[14] else {},
        }

    def get_results_for_run(self, run_id: str) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT run_id, prompt_id, prompt_name, category, scenario, benchmark_suite, difficulty,
                       expected_risk_type, evaluation_focus_json, turns_json, provider_type, model_name,
                       prompt_text, response_text, refusal_score, compliance_score, leakage_score,
                       harmfulness_score, tripwire_count, max_severity, tripwires_json, metadata_json, timestamp
                FROM evaluation_results
                WHERE run_id = ?
                ORDER BY prompt_id ASC
                """,
                (run_id,),
            ).fetchall()
        return [
            {
                "run_id": row[0],
                "prompt_id": row[1],
                "prompt_name": row[2],
                "category": row[3],
                "scenario": row[4],
                "benchmark_suite": row[5],
                "difficulty": row[6],
                "expected_risk_type": row[7],
                "evaluation_focus": json.loads(row[8]) if row[8] else [],
                "turns": json.loads(row[9]) if row[9] else [],
                "provider_type": row[10],
                "model_name": row[11],
                "prompt_text": row[12],
                "response_text": row[13],
                "refusal_score": row[14],
                "compliance_score": row[15],
                "leakage_score": row[16],
                "harmfulness_score": row[17],
                "tripwire_count": row[18],
                "max_severity": row[19],
                "tripwires_triggered": json.loads(row[20]) if row[20] else [],
                "metadata": json.loads(row[21]) if row[21] else {},
                "timestamp": row[22],
            }
            for row in rows
        ]

    def list_runs_for_benchmark_suite(self, suite_name: str) -> list[dict]:
        runs = self.list_runs()
        return [run for run in runs if run.get("metadata", {}).get("benchmark_suite") == suite_name]

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
                    result.prompt_case.benchmark_suite,
                    result.prompt_case.difficulty,
                    result.prompt_case.expected_risk_type,
                    json.dumps(result.prompt_case.evaluation_focus),
                    json.dumps(result.prompt_case.turns),
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
                    benchmark_suite,
                    difficulty,
                    expected_risk_type,
                    evaluation_focus_json,
                    turns_json,
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
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            connection.commit()
