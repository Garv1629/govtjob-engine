from app.modules.ai.providers.base import LLMProviderAdapter
from app.modules.ai.providers.openai_adapter import OpenAIAdapter
from app.modules.ai.providers.mock_adapter import MockLLMAdapter
from app.core.config import settings


class LLMProviderFactory:
    """Factory for instantiating LLM Providers seamlessly."""

    @staticmethod
    def get_provider(provider_name: str = "OpenAI", model_name: str = "gpt-4o") -> LLMProviderAdapter:
        name = provider_name.strip().upper()
        if name == "OPENAI":
            return OpenAIAdapter(model_name=model_name, api_key=settings.OPENAI_API_KEY)
        elif name in ["MOCK", "TEST", "OFFLINE"]:
            return MockLLMAdapter(model_name="mock-gpt-4")
        else:
            # Fallback to Mock Adapter
            return MockLLMAdapter(model_name="mock-fallback")


__all__ = ["LLMProviderAdapter", "OpenAIAdapter", "MockLLMAdapter", "LLMProviderFactory"]
