from __future__ import annotations

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
from modeltripwire.scoring.rules import RuleBasedScorer
from modeltripwire.storage.export import export_results_csv, export_results_json
from modeltripwire.storage.sqlite_store import SQLiteStore
from modeltripwire.tripwires.rules import build_default_tripwires


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


def run_baseline_experiment(config: AppConfig, project_root: str | Path) -> dict:
    root = Path(project_root)
    logger = configure_logging()
    provider = build_provider(config)
    dataset = load_prompt_dataset(config.resolve_dataset_path(root))
    tripwires = build_default_tripwires(config.tripwires.enabled)
    scorer = RuleBasedScorer()
    runner = EvaluationRunner(provider=provider, scorer=scorer, tripwires=tripwires, logger=logger)
    results = runner.run(dataset)

    output_dir = config.resolve_output_directory(root)
    output_dir.mkdir(parents=True, exist_ok=True)

    sqlite_store = SQLiteStore(config.resolve_sqlite_path(root))
    sqlite_store.save_results(results)

    json_path = export_results_json(results, output_dir / "results.json")
    csv_path = export_results_csv(results, output_dir / "results.csv")

    summary = build_experiment_summary(config.reporting.title, config.reporting.research_question, results)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(summary.model_dump_json(indent=2), encoding="utf-8")
    report_path = write_markdown_report(summary, output_dir / "report.md")
    chart_paths = generate_all_charts(results, output_dir / "charts")

    logger.info("Baseline experiment complete", extra={"output_dir": str(output_dir)})
    return {
        "results": results,
        "json_path": json_path,
        "csv_path": csv_path,
        "summary_path": summary_path,
        "report_path": report_path,
        "chart_paths": chart_paths,
        "output_dir": output_dir,
    }
