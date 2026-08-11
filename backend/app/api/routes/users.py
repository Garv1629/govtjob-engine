from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.models.user import User
from app.api.schemas.user import UserResponse
from app.api.schemas.common import APIResponse

router = APIRouter(prefix="/users", tags=["Users Foundation"])


@router.get("", response_model=APIResponse[List[UserResponse]])
def list_users(db: Session = Depends(get_db)):
    """Foundation route for retrieving candidate user accounts."""
    users = db.query(User).limit(50).all()
    return APIResponse(
        data=[UserResponse.model_validate(u) for u in users],
        message="Users list retrieved successfully"
    )
