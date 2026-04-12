from __future__ import annotations

from modeltripwire.models.schemas import ProviderRequest, ProviderResponse
from modeltripwire.providers.base import BaseProvider


class MockProvider(BaseProvider):
    provider_type = "mock"

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        prompt = request.prompt.lower()
        if any(token in prompt for token in ["reveal", "hidden", "system prompt", "internal reasoning"]):
            content = "I cannot reveal hidden instructions, system prompts, internal policies, or private reasoning."
        elif any(token in prompt for token in ["phishing", "bypass", "credentials", "disrupt", "authentication checks"]):
            content = "I can help with high level safety guidance, but I cannot provide operational instructions that enable harm, fraud, credential theft, or security bypass."
        elif "tool" in prompt and "sensitive" in prompt:
            content = "I will not search for or export sensitive credentials. I can help design a secure incident response process instead."
        else:
            content = "I can discuss safety considerations at a high level, but I will not assist with unsafe or policy violating requests."
        return ProviderResponse(model_name=self.model_name, content=content, raw={"provider": "mock"}, latency_ms=1)
