from __future__ import annotations

import time

import httpx

from modeltripwire.models.schemas import ProviderRequest, ProviderResponse
from modeltripwire.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    provider_type = "openai"

    def __init__(self, model_name: str, api_key: str, base_url: str = "https://api.openai.com/v1") -> None:
        super().__init__(model_name=model_name)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        start = time.perf_counter()
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": request.prompt}],
        }
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            raw = response.json()
        content = raw["choices"][0]["message"]["content"]
        latency_ms = int((time.perf_counter() - start) * 1000)
        return ProviderResponse(model_name=self.model_name, content=content, raw=raw, latency_ms=latency_ms)
