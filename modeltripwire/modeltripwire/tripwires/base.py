from __future__ import annotations

from abc import ABC, abstractmethod

from modeltripwire.models.schemas import PromptCase, ProviderResponse, TripwireMatch


class Tripwire(ABC):
    def __init__(self, name: str, description: str, severity: int) -> None:
        self.name = name
        self.description = description
        self.severity = severity

    @abstractmethod
    def evaluate(self, prompt_case: PromptCase, response: ProviderResponse) -> TripwireMatch | None:
        raise NotImplementedError
