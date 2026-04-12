from __future__ import annotations

from pathlib import Path

from modeltripwire.benchmark_gates import evaluate_benchmark_gate
from modeltripwire.models.schemas import EvaluationResult, ExperimentSummary


def build_benchmark_trend_summary(
    suite_name: str,
    run_summaries: list[ExperimentSummary],
    run_results: list[list[EvaluationResult]],
) -> dict:
    entries = []
    for summary, results in zip(run_summaries, run_results):
        gate = evaluate_benchmark_gate(summary, results, suite_name)
        entries.append(
            {
                "run_id": summary.run_id,
                "run_label": summary.run_label,
                "passed": gate["passed"],
                "pass_rate": gate["pass_rate"],
                "mean_refusal_score": summary.aggregate_metrics.get("mean_refusal_score", 0.0),
                "mean_compliance_score": summary.aggregate_metrics.get("mean_compliance_score", 0.0),
                "mean_tripwire_count": summary.aggregate_metrics.get("mean_tripwire_count", 0.0),
                "scenario_checks": gate["scenario_checks"],
            }
        )

    run_count = len(entries)
    pass_count = sum(1 for entry in entries if entry["passed"])

    aggregates = {
        "avg_pass_rate": round(sum(entry["pass_rate"] for entry in entries) / max(run_count, 1), 3),
        "avg_mean_refusal_score": round(sum(entry["mean_refusal_score"] for entry in entries) / max(run_count, 1), 3),
        "avg_mean_compliance_score": round(sum(entry["mean_compliance_score"] for entry in entries) / max(run_count, 1), 3),
        "avg_mean_tripwire_count": round(sum(entry["mean_tripwire_count"] for entry in entries) / max(run_count, 1), 3),
        "pass_fraction": round(pass_count / max(run_count, 1), 3),
    }

    scenario_summary = {}
    for entry in entries:
        for scenario, scenario_check in entry["scenario_checks"].items():
            bucket = scenario_summary.setdefault(
                scenario,
                {
                    "runs_present": 0,
                    "passes": 0,
                    "avg_refusal_score": 0.0,
                    "avg_compliance_score": 0.0,
                    "avg_tripwire_count": 0.0,
                },
            )
            if scenario_check.get("present"):
                bucket["runs_present"] += 1
                if scenario_check.get("passed"):
                    bucket["passes"] += 1
                metrics = scenario_check.get("metrics", {})
                bucket["avg_refusal_score"] += metrics.get("mean_refusal_score", 0.0)
                bucket["avg_compliance_score"] += metrics.get("mean_compliance_score", 0.0)
                bucket["avg_tripwire_count"] += metrics.get("mean_tripwire_count", 0.0)

    for scenario, bucket in scenario_summary.items():
        runs_present = max(bucket["runs_present"], 1)
        bucket["pass_fraction"] = round(bucket["passes"] / runs_present, 3)
        bucket["avg_refusal_score"] = round(bucket["avg_refusal_score"] / runs_present, 3)
        bucket["avg_compliance_score"] = round(bucket["avg_compliance_score"] / runs_present, 3)
        bucket["avg_tripwire_count"] = round(bucket["avg_tripwire_count"] / runs_present, 3)

    return {
        "suite_name": suite_name,
        "run_count": run_count,
        "pass_count": pass_count,
        "aggregates": aggregates,
        "entries": entries,
        "scenario_summary": scenario_summary,
    }


def write_benchmark_trend_report(trend: dict, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    entry_lines = "\n".join(
        f"- {entry['run_id']} ({entry['run_label']}): {'PASS' if entry['passed'] else 'FAIL'} | pass_rate={entry['pass_rate']} | refusal={entry['mean_refusal_score']} | compliance={entry['mean_compliance_score']} | tripwires={entry['mean_tripwire_count']}"
        for entry in trend["entries"]
    )
    scenario_lines = "\n".join(
        f"- **{scenario}**: pass_fraction={bucket['pass_fraction']} | refusal={bucket['avg_refusal_score']} | compliance={bucket['avg_compliance_score']} | tripwires={bucket['avg_tripwire_count']}"
        for scenario, bucket in trend["scenario_summary"].items()
    )

    content = f"""# Benchmark Trend Report

## Suite

- Suite: {trend['suite_name']}
- Runs analyzed: {trend['run_count']}
- Passing runs: {trend['pass_count']}

## Aggregate trend summary

- {trend['aggregates']}

## Run-by-run results

{entry_lines or '- No runs found'}

## Scenario trend summary

{scenario_lines or '- No scenario data'}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
