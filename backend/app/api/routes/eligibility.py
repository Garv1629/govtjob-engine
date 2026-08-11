from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.modules.eligibility import EligibilityEvaluatorEngine, CandidateProfileInput, EligibilityEvaluationOutput
from app.modules.ai import AIService
from app.db.repositories import JobRepository, EligibilityRepository

router = APIRouter(prefix="/eligibility", tags=["AI Eligibility Engine"])


class EvaluationRequestPayload(BaseModel):
    job_id: str
    profile: CandidateProfileInput


@router.post("/evaluate", response_model=APIResponse[EligibilityEvaluationOutput])
async def evaluate_eligibility(payload: EvaluationRequestPayload, db: Session = Depends(get_db)):
    """Evaluates candidate profile against specified Government Job using multi-checker rules."""
    job_repo = JobRepository(db)
    job_record = job_repo.get_by_id(payload.job_id)
    if not job_record:
        raise HTTPException(status_code=404, detail=f"Job record '{payload.job_id}' not found.")

    # Extract or retrieve AI structured job details
    ai_service = AIService(db=db)
    extraction_res = await ai_service.extract_job_details(job_id=payload.job_id, provider="Mock")
    job_data = extraction_res.data

    evaluator = EligibilityEvaluatorEngine(db=db)
    result = evaluator.evaluate(job_id=payload.job_id, profile=payload.profile, job=job_data)
    
    return APIResponse(data=result, message="Eligibility evaluation completed successfully")


@router.get("/results/{job_id}/{user_id}", response_model=APIResponse[dict])
def get_eligibility_results(job_id: str, user_id: str, db: Session = Depends(get_db)):
    """Retrieves stored eligibility evaluation result for job and user."""
    repo = EligibilityRepository(db)
    res = repo.get_by_job_and_user(job_id=job_id, user_id=user_id)
    if not res:
        raise HTTPException(status_code=404, detail="No eligibility result found for specified job and user.")

    payload = {
        "id": res.id,
        "job_id": res.job_id,
        "user_id": res.user_id,
        "status": res.status,
        "overall_score": res.overall_score,
        "scores": res.scores,
        "reasons": res.reasons,
        "matched_rules": res.matched_rules,
        "failed_rules": res.failed_rules,
        "missing_documents": res.missing_documents,
        "recommendations": res.recommendations,
        "evaluated_at": res.evaluated_at
    }
    return APIResponse(data=payload, message="Eligibility result retrieved successfully")
