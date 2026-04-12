from __future__ import annotations

from pathlib import Path

from modeltripwire.models.schemas import ExperimentSummary


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
