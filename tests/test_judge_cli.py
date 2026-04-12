from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.cli import app
from modeltripwire.config import load_config


runner = CliRunner()


def test_run_benchmark_with_judge_enabled(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    config_path = tmp_path / "judge-config.yaml"
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

    run_result = runner.invoke(app, ["run-benchmark", "alpha_core", "--config", str(config_path)])
    assert run_result.exit_code == 0
    assert "Benchmark run complete." in run_result.output

    run_id = run_result.output.strip().split("run_id=")[-1]
    show_result = runner.invoke(app, ["show-run", run_id, "--config", str(config_path)])
    assert show_result.exit_code == 0
    assert '"mean_score_confidence"' in show_result.output
