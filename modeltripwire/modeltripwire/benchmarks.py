from __future__ import annotations

from pathlib import Path


BENCHMARK_SUITES = {
    "alpha_core": {
        "title": "Alpha Core Safety Benchmark",
        "research_question": "How consistently does the model resist core adversarial safety scenarios across jailbreak, injection, leakage, tool misuse, and robustness probes?",
        "dataset_path": "data/benchmarks/alpha_core.json",
    }
}


def get_benchmark_suite(name: str) -> dict:
    if name not in BENCHMARK_SUITES:
        raise KeyError(f"Unknown benchmark suite: {name}")
    return BENCHMARK_SUITES[name]


def resolve_benchmark_dataset_path(project_root: str | Path, suite_name: str) -> Path:
    suite = get_benchmark_suite(suite_name)
    return (Path(project_root) / suite["dataset_path"]).resolve()
