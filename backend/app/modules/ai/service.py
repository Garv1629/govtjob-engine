from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.modules.ai.pipeline import AIJobIntelligencePipeline
from app.modules.ai.schemas import ExtractionResponse, StructuredJobExtraction
from app.core.config import settings
from app.core.logging import logger


class AIService:
    """High-level AIService interface foundation for AI Job Intelligence System."""

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    async def extract_job_details(
        self,
        job_id: str,
        pdf_url: Optional[str] = None,
        raw_text_override: Optional[str] = None,
        provider: str = "OpenAI"
    ) -> ExtractionResponse:
        """Executes full 12-step AI extraction pipeline."""
        logger.info(f"AI Service triggering extraction for job ID: {job_id} using provider: {provider}")
        pipeline = AIJobIntelligencePipeline(
            db=self.db,
            provider_name=provider,
            model_name=self.model
        )
        return await pipeline.execute_pipeline(
            job_id=job_id,
            pdf_url=pdf_url,
            raw_text_override=raw_text_override
        )
