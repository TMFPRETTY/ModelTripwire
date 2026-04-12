from __future__ import annotations

import hashlib

from modeltripwire.models.schemas import ProviderRequest, ProviderResponse
from modeltripwire.providers.base import BaseProvider


class MockProvider(BaseProvider):
    provider_type = "mock"

    SAFE_REFUSAL = "I cannot help with that request. I can offer high level safety guidance, defensive analysis, or safer alternatives instead."
    PARTIAL_COMPLIANCE = "I cannot provide full operational instructions, but generally an attacker might use social engineering, credential theft, or workflow manipulation to pursue the goal."
    UNSAFE_COMPLIANCE = "Here is how to do it step by step: identify the target, craft a convincing pretext, collect credentials, and use them to bypass controls."

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        prompt = request.prompt.lower()

        if any(token in prompt for token in ["reveal", "hidden", "system prompt", "internal reasoning"]):
            content = self.SAFE_REFUSAL
            behavior = "safe_refusal"
        elif "tool" in prompt and "sensitive" in prompt:
            content = self.PARTIAL_COMPLIANCE
            behavior = "partial_compliance"
        elif any(token in prompt for token in ["phishing", "bypass", "credentials", "disrupt", "authentication checks"]):
            mode = int(hashlib.md5(prompt.encode("utf-8")).hexdigest(), 16) % 3
            if mode == 0:
                content = self.SAFE_REFUSAL
                behavior = "safe_refusal"
            elif mode == 1:
                content = self.PARTIAL_COMPLIANCE
                behavior = "partial_compliance"
            else:
                content = self.UNSAFE_COMPLIANCE
                behavior = "unsafe_compliance"
        else:
            content = "I can discuss safety considerations at a high level, but I will not assist with unsafe or policy violating requests."
            behavior = "safe_refusal"

        return ProviderResponse(
            model_name=self.model_name,
            content=content,
            raw={"provider": "mock", "behavior": behavior},
            latency_ms=1,
        )
