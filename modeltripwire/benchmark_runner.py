from __future__ import annotations

from pathlib import Path

from modeltripwire.benchmarks import get_benchmark_manifest, get_benchmark_suite, resolve_benchmark_dataset_path
from modeltripwire.config import AppConfig
from modeltripwire.experiments.baseline_safety_stress_test import run_baseline_experiment


def run_benchmark_suite(config: AppConfig, project_root: str | Path, suite_name: str, config_path: str = "configs/default.yaml") -> dict:
    suite = get_benchmark_suite(suite_name)
    manifest = get_benchmark_manifest(project_root, suite_name)
    config.dataset.path = str(resolve_benchmark_dataset_path(project_root, suite_name))
    config.reporting.title = suite["title"]
    config.reporting.research_question = suite["research_question"]
    return run_baseline_experiment(
        config,
        project_root,
        config_path=config_path,
        run_label_prefix=f"benchmark-{suite_name}",
        extra_run_metadata={
            "benchmark_suite": suite_name,
            "benchmark_version": manifest["version"],
            "benchmark_dataset_hash": manifest["dataset_hash"],
            "benchmark_dataset_path": manifest["dataset_path"],
        },
    )
