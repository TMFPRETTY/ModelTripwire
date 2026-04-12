from __future__ import annotations

from datetime import datetime
from pathlib import Path

from modeltripwire.config import AppConfig
from modeltripwire.evals.dataset_loader import load_prompt_dataset
from modeltripwire.evals.runner import EvaluationRunner
from modeltripwire.logging_utils import configure_logging
from modeltripwire.providers.anthropic_provider import AnthropicProvider
from modeltripwire.providers.mock_provider import MockProvider
from modeltripwire.providers.openai_provider import OpenAIProvider
from modeltripwire.reporting.charts import generate_all_charts
from modeltripwire.reporting.markdown_report import write_markdown_report
from modeltripwire.reporting.summaries import build_experiment_summary
from modeltripwire.run_metadata import detect_git_commit, make_run_id, make_run_label, sha256_file
from modeltripwire.scoring.rules import RuleBasedScorer
from modeltripwire.storage.export import export_results_csv, export_results_json
from modeltripwire.storage.sqlite_store import SQLiteStore
from modeltripwire.tripwires.rules import build_default_tripwires
from modeltripwire.models.schemas import ExperimentRun


def build_provider(config: AppConfig):
    provider_type = config.provider.type.lower()
    if provider_type == "mock":
        return MockProvider(model_name=config.provider.model_name)
    if provider_type == "openai":
        from modeltripwire.config import read_env_var

        api_key = read_env_var(config.provider.openai_api_key_env)
        if not api_key:
            raise ValueError("OpenAI API key env var is not set.")
        return OpenAIProvider(model_name=config.provider.model_name, api_key=api_key)
    if provider_type == "anthropic":
        from modeltripwire.config import read_env_var

        api_key = read_env_var(config.provider.anthropic_api_key_env)
        if not api_key:
            raise ValueError("Anthropic API key env var is not set.")
        return AnthropicProvider(model_name=config.provider.model_name, api_key=api_key)
    raise ValueError(f"Unsupported provider type: {config.provider.type}")


def run_baseline_experiment(config: AppConfig, project_root: str | Path, config_path: str = "configs/default.yaml") -> dict:
    root = Path(project_root)
    logger = configure_logging()
    provider = build_provider(config)
    dataset_path = config.resolve_dataset_path(root)
    dataset = load_prompt_dataset(dataset_path)
    tripwires = build_default_tripwires(config.tripwires.enabled)
    scorer = RuleBasedScorer()
    runner = EvaluationRunner(provider=provider, scorer=scorer, tripwires=tripwires, logger=logger)
    started_at = datetime.utcnow()
    results = runner.run(dataset)
    completed_at = datetime.utcnow()

    output_dir = config.resolve_output_directory(root)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = make_run_id()
    run_label = make_run_label("baseline")
    config_full_path = (root / config_path).resolve()
    run = ExperimentRun(
        run_id=run_id,
        run_label=run_label,
        title=config.reporting.title,
        research_question=config.reporting.research_question,
        provider_type=provider.provider_type,
        model_name=provider.model_name,
        dataset_path=str(dataset_path),
        dataset_hash=sha256_file(dataset_path),
        config_path=str(config_full_path),
        config_hash=sha256_file(config_full_path),
        git_commit=detect_git_commit(root),
        started_at=started_at,
        completed_at=completed_at,
        total_cases=len(results),
        metadata={"tripwires_enabled": config.tripwires.enabled},
    )

    for result in results:
        result.metadata["run_id"] = run_id
        result.metadata["run_label"] = run_label

    sqlite_store = SQLiteStore(config.resolve_sqlite_path(root))
    sqlite_store.save_run(run)
    sqlite_store.save_results(results, run_id=run_id)

    json_path = export_results_json(results, output_dir / "results.json")
    csv_path = export_results_csv(results, output_dir / "results.csv")

    summary = build_experiment_summary(
        config.reporting.title,
        config.reporting.research_question,
        results,
        run_id=run_id,
        run_label=run_label,
    )
    summary_path = output_dir / "summary.json"
    summary_path.write_text(summary.model_dump_json(indent=2), encoding="utf-8")
    report_path = write_markdown_report(summary, output_dir / "report.md")
    chart_paths = generate_all_charts(results, output_dir / "charts")

    logger.info("Baseline experiment complete", extra={"output_dir": str(output_dir), "run_id": run_id})
    return {
        "run": run,
        "results": results,
        "json_path": json_path,
        "csv_path": csv_path,
        "summary_path": summary_path,
        "report_path": report_path,
        "chart_paths": chart_paths,
        "output_dir": output_dir,
    }
