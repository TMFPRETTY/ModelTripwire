from __future__ import annotations

import logging

from modeltripwire.agents.filters import is_input_allowed, is_output_allowed
from modeltripwire.models.schemas import ProviderRequest
from modeltripwire.providers.base import BaseProvider


class SafeAgent:
    def __init__(self, provider: BaseProvider, logger: logging.Logger | None = None) -> None:
        self.provider = provider
        self.logger = logger or logging.getLogger("modeltripwire.safe_agent")

    def handle(self, user_input: str) -> str:
        if not is_input_allowed(user_input):
            self.logger.warning("Blocked unsafe input", extra={"user_input": user_input})
            return "Request blocked by input safety policy."

        request = ProviderRequest(prompt=user_input, model_name=self.provider.model_name)
        response = self.provider.generate(request)

        if not is_output_allowed(response.content):
            self.logger.warning("Blocked unsafe output", extra={"output": response.content})
            return "Model output blocked by output safety policy."

        self.logger.info("SafeAgent completed request")
        return response.content
