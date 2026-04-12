from __future__ import annotations

import logging
from typing import Iterable, List

from modeltripwire.models.schemas import EvaluationResult, PromptCase, ProviderRequest
from modeltripwire.providers.base import BaseProvider
from modeltripwire.scoring.rules import RuleBasedScorer
from modeltripwire.tripwires.base import Tripwire


class EvaluationRunner:
    def __init__(
        self,
        provider: BaseProvider,
        scorer: RuleBasedScorer,
        tripwires: Iterable[Tripwire],
        logger: logging.Logger | None = None,
    ) -> None:
        self.provider = provider
        self.scorer = scorer
        self.tripwires = list(tripwires)
        self.logger = logger or logging.getLogger("modeltripwire.runner")

    def run(self, prompt_cases: Iterable[PromptCase]) -> List[EvaluationResult]:
        results: List[EvaluationResult] = []
        for prompt_case in prompt_cases:
            self.logger.info("Evaluating prompt", extra={"prompt_id": prompt_case.id, "category": prompt_case.category})
            request = ProviderRequest(
                prompt=prompt_case.prompt_text,
                model_name=self.provider.model_name,
                metadata={"prompt_id": prompt_case.id, "category": prompt_case.category},
            )
            provider_response = self.provider.generate(request)
            scorecard = self.scorer.score(prompt_case, provider_response)
            matches = [
                match
                for tripwire in self.tripwires
                if (match := tripwire.evaluate(prompt_case, provider_response)) is not None
            ]
            results.append(
                EvaluationResult(
                    prompt_case=prompt_case,
                    provider_type=self.provider.provider_type,
                    provider_response=provider_response,
                    scorecard=scorecard,
                    tripwires_triggered=matches,
                    metadata={"runner_version": "0.1.0"},
                )
            )
        return results
