from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.cli import app, _load_results_as_models
from modeltripwire.config import load_config
from modeltripwire.reporting.summaries import build_experiment_summary
from modeltripwire.storage.sqlite_store import SQLiteStore
from modeltripwire.trend_gates import evaluate_trend_gate


runner = CliRunner()


def test_evaluate_trend_gate_for_beta_core(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    for _ in range(3):
        run_benchmark_suite(config, project_root, "beta_core")

    store = SQLiteStore(config.resolve_sqlite_path(project_root))
    runs = store.list_runs_for_benchmark_suite("beta_core")[:3]

    summaries = []
    run_results = []
    for run in runs:
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

    result = evaluate_trend_gate("beta_core", summaries, run_results)
    assert result["suite_name"] == "beta_core"
    assert result["run_count"] == 3
    assert "checks" in result
    assert "scenario_checks" in result


def test_trend_gate_and_report_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    config_path = tmp_path / "trend-gate-config.yaml"
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
  enable_llm_judge: true
  llm_judge_model: judge-beta-v1

reporting:
  title: Baseline Safety Stress Test of General Purpose LLMs Under Adversarial Prompting
  research_question: How consistently do general purpose LLMs resist common adversarial prompt patterns across jailbreak, injection, leakage, escalation, and agent misuse scenarios?
""".strip(),
        encoding="utf-8",
    )

    trials_result = runner.invoke(app, ["run-benchmark-trials", "beta_core", "--trials", "3", "--config", str(config_path)])
    assert trials_result.exit_code == 0

    gate_result = runner.invoke(app, ["trend-gate", "beta_core", "--limit", "3", "--config", str(config_path)])
    assert gate_result.exit_code == 0
    assert '"suite_name": "beta_core"' in gate_result.output
    assert '"passed": true' in gate_result.output.lower()

    report_dir = tmp_path / "trend_reports"
    report_result = runner.invoke(
        app,
        ["trend-report", "beta_core", "--limit", "3", "--config", str(config_path), "--output-dir", str(report_dir)],
    )
    assert report_result.exit_code == 0
    assert "Trend gate report written to" in report_result.output
    assert list(report_dir.glob("*.md"))
