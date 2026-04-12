from __future__ import annotations

from abc import ABC, abstractmethod

from modeltripwire.models.schemas import ProviderRequest, ProviderResponse


class BaseProvider(ABC):
    provider_type: str = "base"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @abstractmethod
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        raise NotImplementedError
