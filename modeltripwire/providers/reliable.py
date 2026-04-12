from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from modeltripwire.models.schemas import ProviderRequest, ProviderResponse
from modeltripwire.providers.base import BaseProvider


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    initial_backoff_seconds: float = 0.5
    backoff_multiplier: float = 2.0
    retry_on: tuple[type[BaseException], ...] = (Exception,)


class ReliableProvider(BaseProvider):
    provider_type = "reliable"

    def __init__(
        self,
        wrapped: BaseProvider,
        retry_policy: RetryPolicy | None = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        super().__init__(model_name=wrapped.model_name)
        self.wrapped = wrapped
        self.provider_type = wrapped.provider_type
        self.retry_policy = retry_policy or RetryPolicy()
        self.sleep_fn = sleep_fn or time.sleep

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        attempt = 0
        delay = self.retry_policy.initial_backoff_seconds
        last_error: BaseException | None = None

        while attempt < self.retry_policy.max_attempts:
            attempt += 1
            try:
                response = self.wrapped.generate(request)
                response.raw = {
                    **response.raw,
                    "retry_attempts": attempt,
                    "retry_policy": {
                        "max_attempts": self.retry_policy.max_attempts,
                        "initial_backoff_seconds": self.retry_policy.initial_backoff_seconds,
                        "backoff_multiplier": self.retry_policy.backoff_multiplier,
                    },
                }
                return response
            except self.retry_policy.retry_on as exc:  # type: ignore[misc]
                last_error = exc
                if attempt >= self.retry_policy.max_attempts:
                    break
                self.sleep_fn(delay)
                delay *= self.retry_policy.backoff_multiplier

        assert last_error is not None
        raise last_error
