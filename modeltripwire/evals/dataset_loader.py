from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List

from modeltripwire.models.schemas import PromptCase


def _normalize_prompt_case(item: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(item)
    if "prompt_text" not in normalized and "prompt" in normalized:
        normalized["prompt_text"] = normalized["prompt"]
    if "scenario" not in normalized or not normalized["scenario"]:
        normalized["scenario"] = normalized.get("category")
    if "benchmark_suite" not in normalized or not normalized["benchmark_suite"]:
        normalized["benchmark_suite"] = normalized.get("suite")
    if "difficulty" not in normalized:
        normalized["difficulty"] = None
    if "tags" not in normalized or normalized["tags"] is None:
        normalized["tags"] = []
    if "turns" not in normalized or normalized["turns"] is None:
        normalized["turns"] = []
    return normalized


def load_prompt_dataset(path: str | Path) -> List[PromptCase]:
    dataset_path = Path(path)
    with dataset_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return [PromptCase.model_validate(_normalize_prompt_case(item)) for item in raw]
