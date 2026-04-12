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
    description: str
    prompt_text: str
    expected_risk_type: str


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
    notes: List[str] = Field(default_factory=list)


class TripwireMatch(MTBaseModel):
    name: str
    description: str
    severity: int
    evidence: str


class EvaluationResult(MTBaseModel):
    prompt_case: PromptCase
    provider_type: str
    provider_response: ProviderResponse
    scorecard: ScoreCard
    tripwires_triggered: List[TripwireMatch] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def tripwire_count(self) -> int:
        return len(self.tripwires_triggered)

    @property
    def max_severity(self) -> int:
        return max((match.severity for match in self.tripwires_triggered), default=0)


class ExperimentSummary(MTBaseModel):
    title: str
    research_question: str
    model_names: List[str]
    total_cases: int
    aggregate_metrics: Dict[str, float]
    category_breakdown: Dict[str, Dict[str, float]]
    tripwire_summary: Dict[str, int]
    notable_failures: List[Dict[str, Any]]
    limitations: List[str]
    next_steps: List[str]
