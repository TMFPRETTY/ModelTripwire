from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.cli import app, _load_results_as_models
from modeltripwire.config import load_config
from modeltripwire.reporting.summaries import build_experiment_summary
from modeltripwire.reporting.trends import build_benchmark_trend_summary
from modeltripwire.storage.sqlite_store import SQLiteStore


runner = CliRunner()


def test_build_benchmark_trend_summary(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    first = run_benchmark_suite(config, project_root, "alpha_core")
    second = run_benchmark_suite(config, project_root, "alpha_core")

    store = SQLiteStore(config.resolve_sqlite_path(project_root))
    runs = store.list_runs_for_benchmark_suite("alpha_core")
    assert len(runs) >= 2

    summaries = []
    run_results = []
    for run in runs[:2]:
        rows = store.get_results_for_run(run["run_id"])
        results = _load_results_as_models(rows)
        summary = build_experiment_summary(
            title=run["title"],
            research_question=run["research_question"],
            results=results,
            run_id=run["run_id"],
            run_label=run["run_label"],
        )
        summaries.append(summary)
        run_results.append(results)

    trend = build_benchmark_trend_summary("alpha_core", summaries, run_results)
    assert trend["suite_name"] == "alpha_core"
    assert trend["run_count"] == 2
    assert "aggregates" in trend
    assert "scenario_summary" in trend


def test_benchmark_trials_and_trends_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    config_path = tmp_path / "trend-config.yaml"
    config_path.write_text(
        f"""
provider:
  type: mock
  model_name: mock-safe-v1
  openai_api_key_env: OPENAI_API_KEY
  anthropic_api_key_env: ANTHROPIC_API_KEY

dataset:
  path: data/prompts/baseline_adversarial_prompts.json

output:
  directory: {config.output.directory}
  sqlite_path: {config.output.sqlite_path}

tripwires:
  enabled:
    - system_prompt_leakage
    - policy_violation
    - unsafe_instruction_following
    - sensitive_data_fabrication
    - suspicious_tool_use_request
    - reasoning_exposure_attempt

scoring:
  enable_rule_based: true
  enable_llm_judge: false

reporting:
  title: Baseline Safety Stress Test of General Purpose LLMs Under Adversarial Prompting
  research_question: How consistently do general purpose LLMs resist common adversarial prompt patterns across jailbreak, injection, leakage, escalation, and agent misuse scenarios?
""".strip(),
        encoding="utf-8",
    )

    trials_result = runner.invoke(
        app,
        ["run-benchmark-trials", "alpha_core", "--trials", "3", "--config", str(config_path)],
    )
    assert trials_result.exit_code == 0
    assert '"suite_name": "alpha_core"' in trials_result.output
    assert '"trials": 3' in trials_result.output

    trend_dir = tmp_path / "benchmark_trends"
    trend_result = runner.invoke(
        app,
        [
            "benchmark-trends",
            "alpha_core",
            "--config",
            str(config_path),
            "--limit",
            "3",
            "--output-dir",
            str(trend_dir),
        ],
    )
    assert trend_result.exit_code == 0
    assert '"suite_name": "alpha_core"' in trend_result.output
    assert "Benchmark trend report written to" in trend_result.output
    assert list(trend_dir.glob("*.md"))
