from app.api.routes.health import health_router
from app.api.routes.jobs import jobs_router
from app.api.routes.applications import applications_router
from app.api.routes.scrapers import scrapers_router
from app.api.routes.eligibility import eligibility_router
from app.api.routes.workflow import workflow_router
from app.api.routes.telegram import telegram_router
from app.api.routes.metrics import metrics_router

__all__ = [
    "health_router",
    "jobs_router",
    "applications_router",
    "scrapers_router",
    "eligibility_router",
    "workflow_router",
    "telegram_router",
    "metrics_router",
]
