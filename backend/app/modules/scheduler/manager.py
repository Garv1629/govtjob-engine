from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.logging import logger

scheduler = AsyncIOScheduler()


def initialize_scheduler() -> AsyncIOScheduler:
    """Initializes cron and periodic background scraping schedules."""
    if not scheduler.running:
        logger.info("Initializing APScheduler background jobs manager...")
        scheduler.start()
    return scheduler
