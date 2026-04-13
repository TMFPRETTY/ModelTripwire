from __future__ import annotations

from pathlib import Path

from modeltripwire.models.schemas import ExperimentSummary


def write_provider_comparison_report(
    summaries: list[ExperimentSummary],
    path: str | Path,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metric_keys = sorted({key for summary in summaries for key in summary.aggregate_metrics})
    provider_lines = []
    for summary in summaries:
        provider_name = ", ".join(summary.model_names) or "unknown"
        provider_lines.append(
            f"- **{provider_name}** | run_id={summary.run_id or 'n/a'} | run_label={summary.run_label or 'n/a'}"
            f" | decision={summary.decision_summary.get('status', 'n/a')}"
        )

    metric_sections = []
    for key in metric_keys:
        metric_sections.append(f"### {key}\n")
        ordered = sorted(
            summaries,
            key=lambda item: item.aggregate_metrics.get(key, 0.0),
            reverse=key.startswith("mean_refusal")
        )
        for summary in ordered:
            provider_name = ", ".join(summary.model_names) or "unknown"
            metric_sections.append(f"- **{provider_name}**: {summary.aggregate_metrics.get(key, 0.0)}")
        metric_sections.append("")

    content = f"""# ModelTripwire Provider Comparison

## Compared runs

{chr(10).join(provider_lines) or '- No runs provided'}

## Aggregate metric leaderboard

{chr(10).join(metric_sections).strip() or '- No aggregate metrics available'}

## Decision overview

{chr(10).join(f"- **{', '.join(summary.model_names) or 'unknown'}**: {summary.decision_summary.get('status', 'n/a')} | action={summary.decision_summary.get('recommended_action', 'n/a')} | reasons={summary.decision_summary.get('reasons', [])}" for summary in summaries)}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path


def write_run_comparison_report(
    baseline: ExperimentSummary,
    candidate: ExperimentSummary,
    path: str | Path,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metric_lines = []
    metric_keys = sorted(set(baseline.aggregate_metrics) | set(candidate.aggregate_metrics))
    for key in metric_keys:
        left = baseline.aggregate_metrics.get(key, 0.0)
        right = candidate.aggregate_metrics.get(key, 0.0)
        delta = round(right - left, 3)
        metric_lines.append(f"- **{key}**: baseline={left}, candidate={right}, delta={delta}")

    category_lines = []
    category_keys = sorted(set(baseline.category_breakdown) | set(candidate.category_breakdown))
    for key in category_keys:
        left = baseline.category_breakdown.get(key, {})
        right = candidate.category_breakdown.get(key, {})
        category_lines.append(f"- **{key}**: baseline={left} | candidate={right}")

    scenario_lines = []
    scenario_keys = sorted(set(baseline.scenario_breakdown) | set(candidate.scenario_breakdown))
    for key in scenario_keys:
        left = baseline.scenario_breakdown.get(key, {})
        right = candidate.scenario_breakdown.get(key, {})
        scenario_lines.append(f"- **{key}**: baseline={left} | candidate={right}")

    tripwire_lines = []
    tripwire_keys = sorted(set(baseline.tripwire_summary) | set(candidate.tripwire_summary))
    for key in tripwire_keys:
        left = baseline.tripwire_summary.get(key, 0)
        right = candidate.tripwire_summary.get(key, 0)
        delta = right - left
        tripwire_lines.append(f"- **{key}**: baseline={left}, candidate={right}, delta={delta}")

    content = f"""# ModelTripwire Run Comparison

## Baseline run

- Run ID: {baseline.run_id or 'n/a'}
- Run label: {baseline.run_label or 'n/a'}

## Candidate run

- Run ID: {candidate.run_id or 'n/a'}
- Run label: {candidate.run_label or 'n/a'}

## Decision comparison

- Baseline: {baseline.decision_summary.get('status', 'n/a')} | action={baseline.decision_summary.get('recommended_action', 'n/a')} | reasons={baseline.decision_summary.get('reasons', [])}
- Candidate: {candidate.decision_summary.get('status', 'n/a')} | action={candidate.decision_summary.get('recommended_action', 'n/a')} | reasons={candidate.decision_summary.get('reasons', [])}

## Aggregate metric deltas

{chr(10).join(metric_lines) or '- No aggregate metrics'}

## Category comparison

{chr(10).join(category_lines) or '- No category breakdown'}

## Scenario comparison

{chr(10).join(scenario_lines) or '- No scenario breakdown'}

## Tripwire comparison

{chr(10).join(tripwire_lines) or '- No tripwire data'}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
