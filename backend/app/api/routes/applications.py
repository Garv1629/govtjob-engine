from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.models.application import Application
from app.api.schemas.application import ApplicationResponse
from app.api.schemas.common import APIResponse

router = APIRouter(prefix="/applications", tags=["Applications Foundation"])


@router.get("", response_model=APIResponse[List[ApplicationResponse]])
def list_applications(db: Session = Depends(get_db)):
    """Foundation route for retrieving application submission records."""
    apps = db.query(Application).limit(50).all()
    return APIResponse(
        data=[ApplicationResponse.model_validate(a) for a in apps],
        message="Applications list retrieved successfully"
    )
