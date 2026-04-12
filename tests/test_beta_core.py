from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.cli import app
from modeltripwire.config import load_config
from modeltripwire.evals.dataset_loader import load_prompt_dataset


runner = CliRunner()


def test_beta_core_dataset_exists_and_loads() -> None:
    project_root = Path(__file__).resolve().parent.parent
    dataset = load_prompt_dataset(project_root / "data" / "benchmarks" / "beta_core.json")
    assert len(dataset) == 4
    assert dataset[0].benchmark_suite == "beta_core"
    assert any(item.turns for item in dataset)


def test_beta_core_benchmark_gate_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    config_path = tmp_path / "beta-core-config.yaml"
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

    list_result = runner.invoke(app, ["list-benchmarks"])
    assert list_result.exit_code == 0
    assert "beta_core" in list_result.output

    run_result = runner.invoke(app, ["run-benchmark", "beta_core", "--config", str(config_path)])
    assert run_result.exit_code == 0
    run_id = run_result.output.strip().split("run_id=")[-1]

    gate_result = runner.invoke(app, ["benchmark-gate", run_id, "--config", str(config_path)])
    assert '"suite_name": "beta_core"' in gate_result.output
    assert '"scenario_checks"' in gate_result.output
    assert gate_result.exit_code in (0, 1)


def test_beta_core_direct_run_metadata(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")
    config.scoring.enable_llm_judge = True

    result = run_benchmark_suite(config, project_root, "beta_core")
    assert result["run"].metadata["benchmark_suite"] == "beta_core"
    assert result["run"].metadata["llm_judge_enabled"] is True
