from abc import ABC, abstractmethod
from typing import Tuple
from app.modules.ai.schemas import StructuredJobExtraction


class LLMProviderAdapter(ABC):
    """
    Abstract Adapter Interface for LLM Providers.
    Ensures vendor-neutral abstraction allowing OpenAI, Gemini, Claude, Ollama, etc. to be swapped without changing business logic.
    """

    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    async def extract_structured_data(self, cleaned_text: str) -> Tuple[StructuredJobExtraction, float]:
        """
        Parses cleaned document text and returns structured extraction payload along with LLM execution latency (ms).
        """
        pass
