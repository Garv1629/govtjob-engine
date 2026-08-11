from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.core.dependencies import get_db
from app.api.schemas.common import HealthCheckResponse, APIResponse
from app.core.self_healing import self_healing_manager

router = APIRouter(prefix="/health", tags=["System Health"])


@router.get("", response_model=APIResponse[HealthCheckResponse])
def check_health(db: Session = Depends(get_db)):
    """System health check verifying API and Database status."""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"

    return APIResponse(
        data=HealthCheckResponse(
            status="healthy" if db_status == "connected" else "degraded",
            environment=settings.APP_ENV,
            version="1.0.0",
            database=db_status
        ),
        message="Health status retrieved successfully"
    )


@router.post("/self-heal")
async def trigger_self_healing():
    """Triggers self-healing audit across database, scheduler, telegram, workflows, and browser engine."""
    healing_report = await self_healing_manager.check_and_heal_all()
    return APIResponse(
        data=healing_report,
        message="Self-healing routine executed successfully"
    )
