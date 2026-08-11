from fastapi import APIRouter
from app.api.schemas.common import APIResponse

router = APIRouter(prefix="/version", tags=["System Information"])


@router.get("", response_model=APIResponse[dict])
def get_version():
    """Returns application version and environment metadata."""
    return APIResponse(
        data={
            "app_name": "GovtJob AI Agent Backend",
            "version": "1.0.0",
            "build": "production-foundation-v1"
        },
        message="Version metadata retrieved successfully"
    )
