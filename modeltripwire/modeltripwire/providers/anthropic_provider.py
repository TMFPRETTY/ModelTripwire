from __future__ import annotations

import time

import httpx

from modeltripwire.models.schemas import ProviderRequest, ProviderResponse
from modeltripwire.providers.base import BaseProvider


class AnthropicProvider(BaseProvider):
    provider_type = "anthropic"

    def __init__(self, model_name: str, api_key: str, base_url: str = "https://api.anthropic.com/v1") -> None:
        super().__init__(model_name=model_name)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        start = time.perf_counter()
        payload = {
            "model": self.model_name,
            "max_tokens": 512,
            "messages": [{"role": "user", "content": request.prompt}],
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        with httpx.Client(timeout=60.0) as client:
            response = client.post(f"{self.base_url}/messages", headers=headers, json=payload)
            response.raise_for_status()
            raw = response.json()
        content = "".join(block.get("text", "") for block in raw.get("content", []) if block.get("type") == "text")
        latency_ms = int((time.perf_counter() - start) * 1000)
        return ProviderResponse(model_name=self.model_name, content=content, raw=raw, latency_ms=latency_ms)
