from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.cli import app
from modeltripwire.config import load_config
from modeltripwire.evals.dataset_loader import load_prompt_dataset


runner = CliRunner()


def test_dataset_loader_reads_multiturn_benchmark() -> None:
    project_root = Path(__file__).resolve().parent.parent
    dataset = load_prompt_dataset(project_root / "data" / "benchmarks" / "beta_multiturn.json")
    assert len(dataset) == 3
    assert len(dataset[0].turns) >= 3
    assert dataset[0].scenario == "escalating_phishing_sequence"


def test_run_multiturn_benchmark_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    config_path = tmp_path / "multiturn-config.yaml"
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

    list_result = runner.invoke(app, ["list-benchmarks"])
    assert list_result.exit_code == 0
    assert "beta_multiturn" in list_result.output

    run_result = runner.invoke(app, ["run-benchmark", "beta_multiturn", "--config", str(config_path)])
    assert run_result.exit_code == 0
    assert "Benchmark run complete." in run_result.output
    assert "run_id=" in run_result.output


def test_multiturn_benchmark_run_metadata(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    result = run_benchmark_suite(config, project_root, "beta_multiturn")
    assert result["run"].metadata["benchmark_suite"] == "beta_multiturn"
    assert any(item.metadata.get("multi_turn") for item in result["results"])
    assert all(item.metadata.get("turn_count", 1) >= 1 for item in result["results"])
