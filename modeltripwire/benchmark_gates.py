from __future__ import annotations

from pathlib import Path

from modeltripwire.benchmarks import get_benchmark_suite
from modeltripwire.models.schemas import EvaluationResult, ExperimentSummary


def evaluate_benchmark_gate(summary: ExperimentSummary, results: list[EvaluationResult], suite_name: str) -> dict:
    suite = get_benchmark_suite(suite_name)
    gates = suite.get("gates", {})

    per_case_max_compliance = gates.get("per_case_max_compliance_score", 1.0)
    per_case_max_tripwires = gates.get("per_case_max_tripwire_count", 999)
    scenario_thresholds = gates.get("scenario_thresholds", {})

    case_evaluations = []
    pass_count = 0
    for result in results:
        case_checks = {
            "max_compliance_score": result.scorecard.compliance_score <= per_case_max_compliance,
            "max_tripwire_count": result.tripwire_count <= per_case_max_tripwires,
        }
        case_pass = all(case_checks.values())
        failure_reasons = [name for name, passed in case_checks.items() if not passed]
        case_evaluations.append(
            {
                "prompt_id": result.prompt_case.id,
                "prompt_name": result.prompt_case.name,
                "scenario": result.prompt_case.scenario_name,
                "benchmark_suite": result.prompt_case.benchmark_suite or suite_name,
                "expected_risk_type": result.prompt_case.expected_risk_type,
                "evaluation_focus": result.prompt_case.evaluation_focus,
                "difficulty": result.prompt_case.difficulty,
                "compliance_score": result.scorecard.compliance_score,
                "refusal_score": result.scorecard.refusal_score,
                "leakage_score": result.scorecard.leakage_score,
                "harmfulness_score": result.scorecard.harmfulness_score,
                "score_confidence": result.scorecard.confidence,
                "risk_flags": result.scorecard.risk_flags,
                "score_notes": result.scorecard.notes,
                "tripwire_count": result.tripwire_count,
                "tripwires": [
                    {
                        "name": match.name,
                        "severity": match.severity,
                        "confidence": match.confidence,
                        "match_type": match.match_type,
                        "evidence": match.evidence,
                    }
                    for match in result.tripwires_triggered
                ],
                "checks": case_checks,
                "thresholds": {
                    "max_compliance_score": per_case_max_compliance,
                    "max_tripwire_count": per_case_max_tripwires,
                },
                "failure_reasons": failure_reasons,
                "verdict_summary": "pass" if case_pass else f"fail: {', '.join(failure_reasons)}",
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

    scenario_checks = {}
    for scenario, thresholds in scenario_thresholds.items():
        metrics = summary.scenario_breakdown.get(scenario)
        if not metrics:
            scenario_checks[scenario] = {
                "present": False,
                "passed": False,
                "checks": {"scenario_present": False},
                "thresholds": thresholds,
                "metrics": {},
            }
            continue

        scenario_check_map = {
            "min_refusal_score": metrics.get("mean_refusal_score", 0.0) >= thresholds.get("min_refusal_score", 0.0),
            "max_compliance_score": metrics.get("mean_compliance_score", 1.0) <= thresholds.get("max_compliance_score", 1.0),
            "max_tripwire_count": metrics.get("mean_tripwire_count", 999.0) <= thresholds.get("max_tripwire_count", 999.0),
        }
        scenario_checks[scenario] = {
            "present": True,
            "passed": all(scenario_check_map.values()),
            "checks": scenario_check_map,
            "thresholds": thresholds,
            "metrics": metrics,
        }

    passed = all(checks.values()) and all(item["passed"] for item in scenario_checks.values())

    return {
        "suite_name": suite_name,
        "title": suite["title"],
        "run_id": summary.run_id,
        "run_label": summary.run_label,
        "passed": passed,
        "checks": checks,
        "scenario_checks": scenario_checks,
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
    scenario_lines = "\n".join(
        f"- **{scenario}**: {'PASS' if item['passed'] else 'FAIL'} | metrics={item['metrics']} | thresholds={item['thresholds']}"
        for scenario, item in gate_result["scenario_checks"].items()
    )
    case_lines = "\n".join(
        (
            f"- **{case['prompt_id']}** ({case['scenario']}): {'PASS' if case['passed'] else 'FAIL'}"
            f" | refusal={case['refusal_score']} | compliance={case['compliance_score']}"
            f" | leakage={case['leakage_score']} | harmfulness={case['harmfulness_score']}"
            f" | confidence={case['score_confidence']} | tripwires={case['tripwire_count']}"
            f" | verdict={case['verdict_summary']} | focus={case['evaluation_focus']} | risk_flags={case['risk_flags']}"
        )
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

## Scenario checks

{scenario_lines}

## Per-case results

{case_lines}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
