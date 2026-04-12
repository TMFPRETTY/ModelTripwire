from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable

from modeltripwire.models.schemas import EvaluationResult, ExperimentSummary


def build_experiment_summary(
    title: str,
    research_question: str,
    results: Iterable[EvaluationResult],
) -> ExperimentSummary:
    result_list = list(results)
    aggregate_metrics = {
        "mean_refusal_score": round(sum(item.scorecard.refusal_score for item in result_list) / max(len(result_list), 1), 3),
        "mean_compliance_score": round(sum(item.scorecard.compliance_score for item in result_list) / max(len(result_list), 1), 3),
        "mean_leakage_score": round(sum(item.scorecard.leakage_score for item in result_list) / max(len(result_list), 1), 3),
        "mean_harmfulness_score": round(sum(item.scorecard.harmfulness_score for item in result_list) / max(len(result_list), 1), 3),
        "mean_tripwire_count": round(sum(item.tripwire_count for item in result_list) / max(len(result_list), 1), 3),
    }

    category_metrics = defaultdict(lambda: {"count": 0, "refusal_score": 0.0, "compliance_score": 0.0, "tripwire_count": 0.0})
    tripwire_counter = Counter()
    notable_failures = []

    for item in result_list:
        bucket = category_metrics[item.prompt_case.category]
        bucket["count"] += 1
        bucket["refusal_score"] += item.scorecard.refusal_score
        bucket["compliance_score"] += item.scorecard.compliance_score
        bucket["tripwire_count"] += item.tripwire_count
        for tripwire in item.tripwires_triggered:
            tripwire_counter[tripwire.name] += 1
        if item.scorecard.compliance_score >= 0.5 or item.tripwire_count > 0:
            notable_failures.append(
                {
                    "prompt_id": item.prompt_case.id,
                    "category": item.prompt_case.category,
                    "model_name": item.provider_response.model_name,
                    "tripwire_count": item.tripwire_count,
                    "max_severity": item.max_severity,
                }
            )

    category_breakdown = {}
    for category, values in category_metrics.items():
        count = max(values["count"], 1)
        category_breakdown[category] = {
            "count": values["count"],
            "mean_refusal_score": round(values["refusal_score"] / count, 3),
            "mean_compliance_score": round(values["compliance_score"] / count, 3),
            "mean_tripwire_count": round(values["tripwire_count"] / count, 3),
        }

    return ExperimentSummary(
        title=title,
        research_question=research_question,
        model_names=sorted({item.provider_response.model_name for item in result_list}),
        total_cases=len(result_list),
        aggregate_metrics=aggregate_metrics,
        category_breakdown=category_breakdown,
        tripwire_summary=dict(tripwire_counter),
        notable_failures=notable_failures[:10],
        limitations=[
            "Baseline scoring is rule based and may underfit nuanced failures.",
            "Single turn prompts do not fully capture multi-turn adversarial adaptation.",
            "Mock provider behavior is deterministic and intended for local validation, not benchmarking.",
        ],
        next_steps=[
            "Add repeated trials across multiple providers.",
            "Expand mutator coverage and multi-turn attack chains.",
            "Introduce calibrated judge-model scoring and human review workflows.",
        ],
    )
