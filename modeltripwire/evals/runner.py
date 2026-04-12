from __future__ import annotations

import logging
from typing import Iterable, List

from modeltripwire.models.schemas import EvaluationResult, PromptCase, ProviderRequest
from modeltripwire.providers.base import BaseProvider
from modeltripwire.scoring.judge import LLMAssistedJudge, blend_scorecards
from modeltripwire.scoring.rules import RuleBasedScorer
from modeltripwire.tripwires.base import Tripwire


class EvaluationRunner:
    def __init__(
        self,
        provider: BaseProvider,
        scorer: RuleBasedScorer,
        tripwires: Iterable[Tripwire],
        logger: logging.Logger | None = None,
        judge: LLMAssistedJudge | None = None,
    ) -> None:
        self.provider = provider
        self.scorer = scorer
        self.tripwires = list(tripwires)
        self.logger = logger or logging.getLogger("modeltripwire.runner")
        self.judge = judge

    def run(self, prompt_cases: Iterable[PromptCase]) -> List[EvaluationResult]:
        results: List[EvaluationResult] = []
        for prompt_case in prompt_cases:
            self.logger.info(
                "Evaluating prompt",
                extra={
                    "prompt_id": prompt_case.id,
                    "category": prompt_case.category,
                    "scenario": prompt_case.scenario_name,
                },
            )
            prompt_text = "\n\n".join(prompt_case.turns) if prompt_case.turns else prompt_case.prompt_text
            request = ProviderRequest(
                prompt=prompt_text,
                model_name=self.provider.model_name,
                metadata={
                    "prompt_id": prompt_case.id,
                    "category": prompt_case.category,
                    "scenario": prompt_case.scenario_name,
                    "turn_count": len(prompt_case.turns) if prompt_case.turns else 1,
                },
            )
            provider_response = self.provider.generate(request)
            scorecard = self.scorer.score(prompt_case, provider_response)
            if self.judge is not None:
                judge_result = self.judge.judge(prompt_case, provider_response)
                if judge_result.get("available") and judge_result.get("scorecard") is not None:
                    scorecard = blend_scorecards(scorecard, judge_result["scorecard"])
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
                    metadata={
                        "runner_version": "0.1.0",
                        "scenario": prompt_case.scenario_name,
                        "turn_count": len(prompt_case.turns) if prompt_case.turns else 1,
                        "multi_turn": bool(prompt_case.turns),
                    },
                )
            )
        return results
