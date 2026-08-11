from fastapi import APIRouter
from app.api.routes import (
    health_router,
    jobs_router,
    applications_router,
    scrapers_router,
    eligibility_router,
    workflow_router,
    telegram_router,
    metrics_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(jobs_router)
api_router.include_router(applications_router)
api_router.include_router(scrapers_router)
api_router.include_router(eligibility_router)
api_router.include_router(workflow_router)
api_router.include_router(telegram_router)
api_router.include_router(metrics_router)
