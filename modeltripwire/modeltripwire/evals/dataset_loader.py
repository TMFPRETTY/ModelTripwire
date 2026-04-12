from __future__ import annotations

import json
from pathlib import Path
from typing import List

from modeltripwire.models.schemas import PromptCase


def load_prompt_dataset(path: str | Path) -> List[PromptCase]:
    dataset_path = Path(path)
    with dataset_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return [PromptCase.model_validate(item) for item in raw]
