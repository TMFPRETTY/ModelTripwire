from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class MTBaseModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=())


class PromptCase(MTBaseModel):
    id: str
    name: str
    category: str
    scenario: Optional[str] = None
    benchmark_suite: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    description: str
    prompt_text: str
    expected_risk_type: str
    turns: List[str] = Field(default_factory=list)
    evaluation_focus: List[str] = Field(default_factory=list)

    @property
    def scenario_name(self) -> str:
        return self.scenario or self.category


class ProviderRequest(MTBaseModel):
    prompt: str
    model_name: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProviderResponse(MTBaseModel):
    model_name: str
    content: str
    raw: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ScoreCard(MTBaseModel):
    refusal_score: float
    compliance_score: float
    leakage_score: float
    harmfulness_score: float
    confidence: float = 0.0
    risk_flags: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class TripwireMatch(MTBaseModel):
    name: str
    description: str
    severity: int
    evidence: str
    match_type: str = "keyword"
    confidence: float = 1.0


class EvaluationResult(MTBaseModel):
    prompt_case: PromptCase
    provider_type: str
    provider_response: ProviderResponse
    scorecard: ScoreCard
    rule_scorecard: Optional[ScoreCard] = None
    judge_scorecard: Optional[ScoreCard] = None
    blended_scorecard: Optional[ScoreCard] = None
    tripwires_triggered: List[TripwireMatch] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def tripwire_count(self) -> int:
        return len(self.tripwires_triggered)

    @property
    def max_severity(self) -> int:
        return max((match.severity for match in self.tripwires_triggered), default=0)


class ExperimentRun(MTBaseModel):
    run_id: str
    run_label: str
    title: str
    research_question: str
    provider_type: str
    model_name: str
    dataset_path: str
    dataset_hash: str
    config_path: str
    config_hash: str
    git_commit: Optional[str] = None
    started_at: datetime
    completed_at: datetime
    total_cases: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExperimentSummary(MTBaseModel):
    title: str
    research_question: str
    run_id: Optional[str] = None
    run_label: Optional[str] = None
    benchmark_suite: Optional[str] = None
    model_names: List[str]
    total_cases: int
    aggregate_metrics: Dict[str, float]
    decision_summary: Dict[str, Any] = Field(default_factory=dict)
    category_breakdown: Dict[str, Dict[str, float]]
    scenario_breakdown: Dict[str, Dict[str, float]]
    benchmark_breakdown: Dict[str, Dict[str, float]]
    tripwire_summary: Dict[str, int]
    notable_failures: List[Dict[str, Any]]
    limitations: List[str]
    next_steps: List[str]
