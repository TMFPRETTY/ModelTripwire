from __future__ import annotations

from pathlib import Path

from modeltripwire.benchmarks import get_benchmark_suite
from modeltripwire.models.schemas import EvaluationResult, ExperimentSummary


def evaluate_benchmark_gate(summary: ExperimentSummary, results: list[EvaluationResult], suite_name: str) -> dict:
    suite = get_benchmark_suite(suite_name)
    gates = suite.get("gates", {})

    per_case_max_compliance = gates.get("per_case_max_compliance_score", 1.0)
    per_case_max_tripwires = gates.get("per_case_max_tripwire_count", 999)

    case_evaluations = []
    pass_count = 0
    for result in results:
        case_pass = result.scorecard.compliance_score <= per_case_max_compliance and result.tripwire_count <= per_case_max_tripwires
        case_evaluations.append(
            {
                "prompt_id": result.prompt_case.id,
                "scenario": result.prompt_case.scenario_name,
                "benchmark_suite": result.prompt_case.benchmark_suite or suite_name,
                "compliance_score": result.scorecard.compliance_score,
                "tripwire_count": result.tripwire_count,
                "passed": case_pass,
            }
        )
        if case_pass:
            pass_count += 1

    pass_rate = round(pass_count / max(len(results), 1), 3)
    checks = {
        "min_mean_refusal_score": summary.aggregate_metrics.get("mean_refusal_score", 0.0) >= gates.get("min_mean_refusal_score", 0.0),
        "max_mean_compliance_score": summary.aggregate_metrics.get("mean_compliance_score", 1.0) <= gates.get("max_mean_compliance_score", 1.0),
        "max_mean_tripwire_count": summary.aggregate_metrics.get("mean_tripwire_count", 999.0) <= gates.get("max_mean_tripwire_count", 999.0),
        "min_pass_rate": pass_rate >= gates.get("min_pass_rate", 0.0),
    }
    passed = all(checks.values())

    return {
        "suite_name": suite_name,
        "title": suite["title"],
        "run_id": summary.run_id,
        "run_label": summary.run_label,
        "passed": passed,
        "checks": checks,
        "thresholds": gates,
        "aggregate_metrics": summary.aggregate_metrics,
        "pass_rate": pass_rate,
        "case_evaluations": case_evaluations,
    }


def write_benchmark_gate_report(gate_result: dict, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    check_lines = "\n".join(
        f"- **{name}**: {'PASS' if value else 'FAIL'}"
        for name, value in gate_result["checks"].items()
    )
    case_lines = "\n".join(
        f"- {case['prompt_id']} ({case['scenario']}): {'PASS' if case['passed'] else 'FAIL'} | compliance={case['compliance_score']} | tripwires={case['tripwire_count']}"
        for case in gate_result["case_evaluations"]
    )

    content = f"""# Benchmark Gate Report

## Benchmark

- Suite: {gate_result['suite_name']}
- Title: {gate_result['title']}
- Run ID: {gate_result['run_id'] or 'n/a'}
- Run label: {gate_result['run_label'] or 'n/a'}
- Overall result: {'PASS' if gate_result['passed'] else 'FAIL'}

## Aggregate metrics

- {gate_result['aggregate_metrics']}
- Pass rate: {gate_result['pass_rate']}

## Gate checks

{check_lines}

## Per-case results

{case_lines}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
