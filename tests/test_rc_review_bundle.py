import json
from pathlib import Path

from typer.testing import CliRunner

from modeltripwire.benchmark_runner import run_benchmark_suite
from modeltripwire.cli import app
from modeltripwire.config import load_config


runner = CliRunner()


def test_rc_review_bundle_cli(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    config.output.directory = str(tmp_path / "outputs")
    config.output.sqlite_path = str(tmp_path / "outputs" / "modeltripwire.db")

    first = run_benchmark_suite(config, project_root, "beta_core")
    run_benchmark_suite(config, project_root, "beta_core")

    config_path = tmp_path / "bundle-config.yaml"
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

    bundle_out = tmp_path / "rc_bundle"
    result = runner.invoke(
        app,
        [
            "rc-review-bundle",
            first["run"].run_id,
            "--config",
            str(config_path),
            "--output-dir",
            str(bundle_out),
            "--trend-limit",
            "2",
        ],
    )
    assert result.exit_code in (0, 1)
    payload = json.loads(result.output)
    assert payload["run_id"] == first["run"].run_id
    assert payload["suite_name"] == "beta_core"
    assert Path(payload["benchmark_report"]).exists()
    assert Path(payload["rc_report"]).exists()
    assert Path(payload["case_review"]).exists()
    assert Path(payload["html_report"]).exists()
    assert Path(payload["html_dashboard"]).exists()
    if payload["trend_report"]:
        assert Path(payload["trend_report"]).exists()
