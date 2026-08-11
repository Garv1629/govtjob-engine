from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.modules.ai.service import AIService
from app.modules.ai.schemas import ExtractionRequest, ExtractionResponse
from app.db.repositories import JobExtractionRepository

router = APIRouter(prefix="/ai", tags=["AI Job Intelligence Engine"])


@router.post("/extract", response_model=APIResponse[ExtractionResponse])
async def extract_job(req: ExtractionRequest, db: Session = Depends(get_db)):
    """Triggers 12-step AI Extraction Pipeline on job PDF / text."""
    service = AIService(db=db)
    try:
        res = await service.extract_job_details(
            job_id=req.job_id,
            pdf_url=req.pdf_url,
            raw_text_override=req.raw_text,
            provider=req.provider or "OpenAI"
        )
        return APIResponse(data=res, message="AI Job Extraction completed successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Extraction error: {str(e)}")


@router.get("/results/{job_id}", response_model=APIResponse[dict])
def get_extraction_results(job_id: str, db: Session = Depends(get_db)):
    """Retrieves saved structured JSON extraction result and confidence score."""
    repo = JobExtractionRepository(db)
    result = repo.get_by_job_id(job_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No extraction results found for job ID '{job_id}'.")
    
    payload = {
        "id": result.id,
        "job_id": result.job_id,
        "extraction_version": result.extraction_version,
        "llm_provider": result.llm_provider,
        "llm_model_used": result.llm_model_used,
        "confidence_score": result.confidence_score,
        "processing_time_ms": result.processing_time_ms,
        "ocr_time_ms": result.ocr_time_ms,
        "llm_time_ms": result.llm_time_ms,
        "data": result.extracted_json,
        "created_at": result.created_at
    }
    return APIResponse(data=payload, message="Extraction result retrieved successfully")
