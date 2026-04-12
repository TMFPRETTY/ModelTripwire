from __future__ import annotations

from modeltripwire.models.schemas import PromptCase, ProviderResponse


class LLMAssistedJudge:
    """Scaffold for future LLM-judge based scoring."""

    def judge(self, prompt_case: PromptCase, response: ProviderResponse) -> dict:
        return {
            "available": False,
            "message": "LLM judge scaffold is present but disabled by default.",
            "prompt_id": prompt_case.id,
            "model_name": response.model_name,
        }
