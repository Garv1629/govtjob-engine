import os
import sys

# Auto-add DLL search paths for Windows Python installations
if sys.platform == "win32":
    py_base = os.path.dirname(sys.executable)
    dll_paths = [
        os.path.join(py_base, "DLLs"),
        os.path.join(os.path.dirname(py_base), "DLLs"),
        r"C:\Users\GARV\AppData\Local\Programs\Python\Python314\DLLs"
    ]
    for p in dll_paths:
        if os.path.exists(p):
            try:
                os.add_dll_directory(p)
            except Exception:
                pass
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.api.router import api_router
from app.api.middleware.security import SecurityAndLoggingMiddleware
from app.db.base import Base
from app.db.session import engine
from app.modules.scheduler.manager import initialize_scheduler
from app.modules.notifications.telegram_poller import start_telegram_poller, stop_telegram_poller


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application Lifespan Events (Startup & Shutdown)."""
    logger.info("Initializing Database Tables...")
    Base.metadata.create_all(bind=engine)

    logger.info("Starting Background Scheduler...")
    sched = initialize_scheduler()

    logger.info("Starting Telegram Bot Poller Worker...")
    poller_task = asyncio.create_task(start_telegram_poller())

    logger.info(f"{settings.APP_NAME} started successfully on environment '{settings.APP_ENV}'")
    yield

    logger.info("Stopping Telegram Bot Poller Worker...")
    stop_telegram_poller()
    poller_task.cancel()

    logger.info("Shutting down Background Scheduler...")
    if sched.running:
        sched.shutdown()
    logger.info("GovtJob AI Agent Backend shut down successfully.")


def create_application() -> FastAPI:
    """Application Factory for initializing production FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan
    )

    # Add Middleware
    app.add_middleware(SecurityAndLoggingMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API Router
    app.include_router(api_router)

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
