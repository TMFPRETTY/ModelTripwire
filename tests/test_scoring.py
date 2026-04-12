from modeltripwire.models.schemas import PromptCase, ProviderResponse
from modeltripwire.scoring.rules import RuleBasedScorer


def test_rule_based_scoring_refusal() -> None:
    scorer = RuleBasedScorer()
    prompt = PromptCase(
        id="1",
        name="safe",
        category="jailbreak",
        description="",
        prompt_text="Give exact instructions",
        expected_risk_type="policy_violation",
    )
    response = ProviderResponse(model_name="mock", content="I cannot provide exact instructions and will not assist.")
    score = scorer.score(prompt, response)
    assert score.refusal_score > 0.0
    assert score.compliance_score > 0.0
    assert score.confidence > 0.0
    assert score.notes[-1] == "scenario=jailbreak"
