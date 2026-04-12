from modeltripwire.models.schemas import ProviderRequest, ProviderResponse
from modeltripwire.providers.base import BaseProvider
from modeltripwire.providers.reliable import ReliableProvider, RetryPolicy


class FlakyProvider(BaseProvider):
    provider_type = "flaky"

    def __init__(self, failures_before_success: int) -> None:
        super().__init__(model_name="flaky-model")
        self.failures_before_success = failures_before_success
        self.calls = 0

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        if self.calls <= self.failures_before_success:
            raise RuntimeError("transient failure")
        return ProviderResponse(model_name=self.model_name, content="safe refusal", raw={"source": "flaky"}, latency_ms=1)


def test_reliable_provider_retries_until_success() -> None:
    provider = FlakyProvider(failures_before_success=2)
    reliable = ReliableProvider(
        provider,
        retry_policy=RetryPolicy(max_attempts=3, initial_backoff_seconds=0.0, backoff_multiplier=1.0, retry_on=(RuntimeError,)),
        sleep_fn=lambda _: None,
    )

    response = reliable.generate(ProviderRequest(prompt="test", model_name="flaky-model"))
    assert response.content == "safe refusal"
    assert response.raw["retry_attempts"] == 3
    assert provider.calls == 3


def test_reliable_provider_raises_after_exhausting_retries() -> None:
    provider = FlakyProvider(failures_before_success=5)
    reliable = ReliableProvider(
        provider,
        retry_policy=RetryPolicy(max_attempts=3, initial_backoff_seconds=0.0, backoff_multiplier=1.0, retry_on=(RuntimeError,)),
        sleep_fn=lambda _: None,
    )

    try:
        reliable.generate(ProviderRequest(prompt="test", model_name="flaky-model"))
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass

    assert provider.calls == 3
