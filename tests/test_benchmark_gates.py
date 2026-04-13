from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.cli import app
from modeltripwire.config import load_config
from modeltripwire.benchmark_runner import run_benchmark_suite


runner = CliRunner()


def test_benchmark_gate_and_report_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    result = run_benchmark_suite(config, project_root, "alpha_core")
    run_id = result["run"].run_id

    config_path = tmp_path / "benchmark-gate-config.yaml"
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

    gate_result = runner.invoke(app, ["benchmark-gate", run_id, "--config", str(config_path)])
    assert '"suite_name": "alpha_core"' in gate_result.output
    assert '"scenario_checks"' in gate_result.output
    assert '"verdict_summary"' in gate_result.output
    assert '"failure_reasons"' in gate_result.output
    assert '"decision_summary"' in gate_result.output
    assert gate_result.exit_code in (0, 1)

    report_dir = tmp_path / "benchmark_reports"
    report_result = runner.invoke(
        app,
        ["benchmark-report", run_id, "--config", str(config_path), "--output-dir", str(report_dir)],
    )
    assert report_result.exit_code == 0
    assert "Benchmark report written to" in report_result.output
    report_files = list(report_dir.glob("*.md"))
    assert report_files
    content = report_files[0].read_text(encoding="utf-8")
    assert "Decision summary" in content


def test_alpha_extended_benchmark_gate_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    result = run_benchmark_suite(config, project_root, "alpha_extended")
    run_id = result["run"].run_id

    config_path = tmp_path / "benchmark-gate-config-extended.yaml"
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

    gate_result = runner.invoke(app, ["benchmark-gate", run_id, "--config", str(config_path)])
    assert '"suite_name": "alpha_extended"' in gate_result.output
    assert '"scenario_checks"' in gate_result.output
    assert '"verdict_summary"' in gate_result.output
    assert '"decision_summary"' in gate_result.output
    assert gate_result.exit_code in (0, 1)
