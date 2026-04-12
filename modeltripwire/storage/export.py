from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from modeltripwire.models.schemas import EvaluationResult


def _flatten_result(result: EvaluationResult) -> dict:
    return {
        "prompt_id": result.prompt_case.id,
        "prompt_name": result.prompt_case.name,
        "category": result.prompt_case.category,
        "scenario": result.prompt_case.scenario_name,
        "provider_type": result.provider_type,
        "model_name": result.provider_response.model_name,
        "prompt_text": result.prompt_case.prompt_text,
        "response_text": result.provider_response.content,
        "refusal_score": result.scorecard.refusal_score,
        "compliance_score": result.scorecard.compliance_score,
        "leakage_score": result.scorecard.leakage_score,
        "harmfulness_score": result.scorecard.harmfulness_score,
        "tripwire_count": result.tripwire_count,
        "max_severity": result.max_severity,
        "tripwires_triggered": [match.model_dump() for match in result.tripwires_triggered],
        "metadata": result.metadata,
        "timestamp": result.provider_response.timestamp.isoformat(),
    }


def export_results_json(results: Iterable[EvaluationResult], path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [_flatten_result(result) for result in results]
    output_path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")
    return output_path


def export_results_csv(results: Iterable[EvaluationResult], path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for result in results:
        row = _flatten_result(result)
        row["tripwires_triggered"] = json.dumps(row["tripwires_triggered"])
        row["metadata"] = json.dumps(row["metadata"])
        rows.append(row)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    return output_path
