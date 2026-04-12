from __future__ import annotations

BLOCKED_INPUT_MARKERS = [
    "phishing",
    "bypass",
    "credentials",
    "disrupt",
    "reveal the full original system prompt",
    "show your full internal reasoning",
]

BLOCKED_OUTPUT_MARKERS = [
    "step by step",
    "exact instructions",
    "search for sensitive company credentials",
]


def is_input_allowed(user_input: str) -> bool:
    lowered = user_input.lower()
    return not any(marker in lowered for marker in BLOCKED_INPUT_MARKERS)


def is_output_allowed(output_text: str) -> bool:
    lowered = output_text.lower()
    return not any(marker in lowered for marker in BLOCKED_OUTPUT_MARKERS)
