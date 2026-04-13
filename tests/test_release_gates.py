from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.cli import app
from modeltripwire.config import load_config


runner = CliRunner()


def test_rc_gate_and_report_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    result = run_benchmark_suite(config, project_root, "beta_core")
    run_benchmark_suite(config, project_root, "beta_core")
    run_id = result["run"].run_id

    config_path = tmp_path / "rc-gate-config.yaml"
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

    gate_result = runner.invoke(app, ["rc-gate", run_id, "--config", str(config_path), "--trend-limit", "2"])
    assert '"suite_name": "beta_core"' in gate_result.output
    assert '"decision_summary"' in gate_result.output
    assert gate_result.exit_code in (0, 1)

    report_dir = tmp_path / "rc_reports"
    report_result = runner.invoke(
        app,
        ["rc-report", run_id, "--config", str(config_path), "--output-dir", str(report_dir), "--trend-limit", "2"],
    )
    assert report_result.exit_code == 0
    assert "RC gate report written to" in report_result.output
    report_files = list(report_dir.glob("*.md"))
    assert report_files
    content = report_files[0].read_text(encoding="utf-8")
    assert "Release Candidate Gate Report" in content
    assert "Decision summary" in content
