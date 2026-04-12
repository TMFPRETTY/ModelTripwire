from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.cli import app
from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.config import load_config
from modeltripwire.experiments.baseline_safety_stress_test import run_baseline_experiment


runner = CliRunner()


def test_cli_run_listing_and_comparison(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    first = run_baseline_experiment(config, project_root)
    second = run_baseline_experiment(config, project_root)

    config_path = tmp_path / "test-config.yaml"
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

    list_result = runner.invoke(app, ["list-runs", "--config", str(config_path)])
    assert list_result.exit_code == 0
    assert first["run"].run_id in list_result.output
    assert second["run"].run_id in list_result.output

    show_result = runner.invoke(app, ["show-run", first["run"].run_id, "--config", str(config_path)])
    assert show_result.exit_code == 0
    assert first["run"].run_id in show_result.output
    assert '"scenario_breakdown"' in show_result.output

    compare_out = tmp_path / "compare"
    compare_result = runner.invoke(
        app,
        [
            "compare-runs",
            first["run"].run_id,
            second["run"].run_id,
            "--config",
            str(config_path),
            "--output-dir",
            str(compare_out),
        ],
    )
    assert compare_result.exit_code == 0
    assert "Comparison report written to" in compare_result.output
    report_files = list(compare_out.glob("*.md"))
    assert report_files


def test_benchmark_case_review_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    benchmark_run = run_benchmark_suite(config, project_root, "alpha_core")

    config_path = tmp_path / "benchmark-review-config.yaml"
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

    review_out = tmp_path / "case_reviews"
    review_result = runner.invoke(
        app,
        [
            "benchmark-case-review",
            benchmark_run["run"].run_id,
            "--config",
            str(config_path),
            "--output-dir",
            str(review_out),
        ],
    )
    assert review_result.exit_code == 0
    assert "Benchmark case review report written to" in review_result.output
    report_files = list(review_out.glob("*.md"))
    assert report_files
    content = report_files[0].read_text(encoding="utf-8")
    assert "Benchmark Case Review Report" in content
    assert "Recommended calibration action" in content
