from __future__ import annotations

from modeltripwire.models.schemas import ProviderRequest
from modeltripwire.providers.base import BaseProvider


class UnsafeAgent:
    def __init__(self, provider: BaseProvider) -> None:
        self.provider = provider

    def handle(self, user_input: str) -> str:
        request = ProviderRequest(prompt=user_input, model_name=self.provider.model_name)
        response = self.provider.generate(request)
        return response.content
