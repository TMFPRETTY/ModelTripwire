import json
import sqlite3
from pathlib import Path

from modeltripwire.config import load_config
from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.experiments.baseline_safety_stress_test import run_baseline_experiment


def test_run_metadata_is_persisted(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    result = run_baseline_experiment(config, project_root)

    run = result["run"]
    assert run.run_id
    assert run.run_label.startswith("baseline-")
    assert result["results"][0].metadata["run_id"] == run.run_id

    connection = sqlite3.connect(config.resolve_sqlite_path(project_root))
    try:
        run_row = connection.execute("SELECT run_id, run_label, total_cases, metadata_json FROM experiment_runs").fetchone()
        assert run_row is not None
        assert run_row[0] == run.run_id
        assert run_row[1] == run.run_label
        assert run_row[2] == len(result["results"])
        metadata = json.loads(run_row[3])
        assert "tripwires_enabled" in metadata

        result_row = connection.execute("SELECT run_id, scenario, expected_risk_type, evaluation_focus_json, turns_json, rule_scorecard_json, judge_scorecard_json, blended_scorecard_json, metadata_json FROM evaluation_results LIMIT 1").fetchone()
        assert result_row is not None
        assert result_row[0] == run.run_id
        assert result_row[1]
        assert result_row[2]
        assert result_row[3] is not None
        assert result_row[4] is not None
        assert result_row[5] is not None
        metadata_json = json.loads(result_row[8])
        assert metadata_json.get("evaluator_mode") == "rule_only"
        assert metadata_json.get("rule_scorecard") is not None
        assert result_row[6] is None
        assert result_row[7] is None
    finally:
        connection.close()


def test_benchmark_run_persists_frozen_benchmark_metadata(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    result = run_benchmark_suite(config, project_root, "beta_core")

    connection = sqlite3.connect(config.resolve_sqlite_path(project_root))
    try:
        run_row = connection.execute("SELECT metadata_json FROM experiment_runs WHERE run_id = ?", (result["run"].run_id,)).fetchone()
        assert run_row is not None
        metadata = json.loads(run_row[0])
        assert metadata["benchmark_suite"] == "beta_core"
        assert metadata["benchmark_version"] == "2026-04-beta-core-v1"
        assert metadata["benchmark_dataset_hash"]
        assert metadata["benchmark_dataset_path"].endswith("beta_core.json")
    finally:
        connection.close()
