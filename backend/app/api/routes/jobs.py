from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.repositories import JobRepository
from app.api.schemas.job import JobResponse
from app.api.schemas.common import APIResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=APIResponse[List[JobResponse]])
def list_jobs(db: Session = Depends(get_db)):
    """Retrieves all active government jobs discovered by the Job Source Engine."""
    repo = JobRepository(db)
    jobs = repo.get_all()
    return APIResponse(
        data=[JobResponse.model_validate(j) for j in jobs],
        message="Discovered government jobs retrieved successfully"
    )
