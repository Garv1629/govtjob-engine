import time
import json
from typing import Tuple
from openai import AsyncOpenAI
from app.modules.ai.providers.base import LLMProviderAdapter
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class OpenAIAdapter(LLMProviderAdapter):
    """OpenAI API Provider Adapter implementing structured JSON extraction."""

    def __init__(self, model_name: str = "gpt-4o", api_key: str = ""):
        super().__init__(model_name, api_key)
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def extract_structured_data(self, cleaned_text: str) -> Tuple[StructuredJobExtraction, float]:
        start_time = time.time()
        
        if not self.client or self.api_key == "mock-openai-key":
            logger.warning("OpenAI API key not set or mock key detected. Using deterministic OpenAI fallback parser.")
            from app.modules.ai.providers.mock_adapter import MockLLMAdapter
            mock = MockLLMAdapter()
            return await mock.extract_structured_data(cleaned_text)

        prompt = f"""
        You are an expert Government Job Notification Extractor. Extract all details from the provided document into a clean, valid JSON object matching the requested schema exactly.
        
        Document Content:
        {cleaned_text[:12000]}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You extract structured data from official government job notification PDFs and web pages."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )

            raw_json_str = response.choices[0].message.content
            parsed_dict = json.loads(raw_json_str)
            extraction = StructuredJobExtraction.model_validate(parsed_dict)
            
            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"OpenAI extraction completed in {elapsed_ms:.2f}ms using {self.model_name}")
            return extraction, elapsed_ms

        except Exception as e:
            logger.error(f"OpenAI extraction error: {str(e)}")
            raise e
