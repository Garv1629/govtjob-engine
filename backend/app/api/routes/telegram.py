from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.notifications.telegram_bot import TelegramBotCommandCenter, TelegramSecurity
from app.modules.notifications.telegram import TelegramNotificationService
from app.core.logging import logger

router = APIRouter(prefix="/telegram", tags=["Telegram AI Command Center"])


@router.post("/webhook", response_model=Dict[str, Any])
async def handle_telegram_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Receives incoming Telegram updates (Command messages, inline callbacks, document uploads).
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    logger.info(f"[TelegramWebhook] Received update: {body}")
    cmd_center = TelegramBotCommandCenter(db_session=db)

    # 1. Callback Query Handling
    if "callback_query" in body:
        cb = body["callback_query"]
        user = cb.get("from", {})
        user_id = user.get("id")
        data = cb.get("data", "")
        res = await cmd_center.handle_callback(data, user_id)
        return res

    # 2. Text Message / Command Handling
    elif "message" in body:
        msg = body["message"]
        user = msg.get("from", {})
        user_id = user.get("id")
        text = msg.get("text", "")

        if text.startswith("/"):
            parts = text.split()
            command = parts[0]
            args = parts[1:]
            res = await cmd_center.handle_command(command, user_id, args)
            return res
        else:
            return {"status": "SUCCESS", "message": "Received standard message"}

    return {"status": "IGNORED"}


@router.post("/send-alert", response_model=Dict[str, Any])
async def send_manual_job_alert(
    job_id: str,
    title: str,
    organization: str,
    advt_number: str = "ADV-2026",
    vacancies: int = 1000,
    db: Session = Depends(get_db)
):
    """
    Triggers a formatted Telegram job notification card for testing or manual alert dispatch.
    """
    tg_service = TelegramNotificationService(db_session=db)
    job_data = {
        "job_title": title,
        "organization": organization,
        "advt_number": advt_number,
        "total_vacancies": vacancies,
        "pdf_url": "https://govjob.gov.in/sample.pdf",
        "website_url": "https://govjob.gov.in",
        "apply_url": "https://govjob.gov.in/apply"
    }
    eligibility = {"status": "ELIGIBLE", "score": 95.0}

    success = await tg_service.send_job_alert(job_data, eligibility, workflow_id=f"wf_{job_id}")
    return {"success": success, "job_id": job_id, "message": "Telegram alert dispatched"}


@router.get("/status", response_model=Dict[str, Any])
async def get_telegram_command_center_status():
    """
    Returns Telegram Command Center operational status and configuration metadata.
    """
    from app.core.config import settings
    return {
        "bot_enabled": settings.TELEGRAM_ENABLED,
        "bot_token_configured": bool(settings.TELEGRAM_BOT_TOKEN),
        "chat_id_configured": bool(settings.TELEGRAM_CHAT_ID),
        "authorized_users_count": len(settings.TELEGRAM_ALLOWED_USER_IDS),
        "status": "OPERATIONAL"
    }
