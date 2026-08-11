import pytest
from app.modules.notifications.telegram_bot import (
    TelegramSecurity,
    TelegramCardFormatter,
    TelegramBotCommandCenter
)
from app.modules.notifications.telegram import TelegramNotificationService
from app.core.config import settings


def test_telegram_security_authorization():
    # Test authorized user
    authorized_id = settings.TELEGRAM_ALLOWED_USER_IDS[0] if settings.TELEGRAM_ALLOWED_USER_IDS else "123456789"
    assert TelegramSecurity.is_authorized(authorized_id) is True

    # Test unauthorized user
    assert TelegramSecurity.is_authorized("unauthorized_user_999", username="fake_user") is False


def test_telegram_card_formatting():
    job_data = {
        "organization": "Staff Selection Commission",
        "job_title": "Combined Graduate Level Exam 2026",
        "advt_number": "SSC-CGL-2026",
        "total_vacancies": 12000,
        "salary_summary": "Pay Level 7 (₹44,900 - ₹1,42,400)",
        "qualifications": {"essential": ["Bachelor's Degree in any discipline"]},
        "min_age": 18,
        "max_age": 30,
        "last_date": "2026-08-31",
        "location": "All India",
        "fee_summary": "₹100 (UR/OBC), Exempted (SC/ST/Female)",
        "pdf_url": "https://ssc.gov.in/cgl.pdf",
        "website_url": "https://ssc.gov.in",
        "apply_url": "https://ssc.gov.in/apply"
    }

    eligibility = {"status": "ELIGIBLE", "score": 95.0}

    card_text = TelegramCardFormatter.format_job_notification_card(job_data, eligibility)
    assert "Staff Selection Commission" in card_text
    assert "Combined Graduate Level Exam 2026" in card_text
    assert "95.0%" in card_text
    assert "Download PDF" in card_text

    keyboard = TelegramCardFormatter.get_job_card_inline_keyboard("wf_123", job_data["pdf_url"], job_data["website_url"], job_data["apply_url"])
    assert len(keyboard) == 3
    assert keyboard[0][0]["text"] == "⚡ Apply"


@pytest.mark.asyncio
async def test_telegram_command_center_authorized_commands(db_session):
    cmd_center = TelegramBotCommandCenter(db_session=db_session)
    user_id = settings.TELEGRAM_ALLOWED_USER_IDS[0] if settings.TELEGRAM_ALLOWED_USER_IDS else "123456789"

    commands = ["start", "help", "profile", "documents", "jobs", "applications", "status", "logs", "settings", "restart", "health", "version"]
    for cmd in commands:
        res = await cmd_center.handle_command(cmd, user_id=user_id)
        assert res["status"] == "SUCCESS"
        assert len(res["text"]) > 0


@pytest.mark.asyncio
async def test_telegram_command_center_unauthorized_user(db_session):
    cmd_center = TelegramBotCommandCenter(db_session=db_session)
    res = await cmd_center.handle_command("profile", user_id="unauthorized_9999")
    assert res["status"] == "UNAUTHORIZED"
    assert "Access Denied" in res["text"]


@pytest.mark.asyncio
async def test_telegram_callback_buttons(db_session):
    cmd_center = TelegramBotCommandCenter(db_session=db_session)
    user_id = settings.TELEGRAM_ALLOWED_USER_IDS[0] if settings.TELEGRAM_ALLOWED_USER_IDS else "123456789"

    # Test APPLY callback
    res_apply = await cmd_center.handle_callback("btn_apply:wf_test_10", user_id=user_id)
    assert res_apply["status"] == "SUCCESS"
    assert res_apply["action"] == "APPLY"

    # Test IGNORE callback
    res_ignore = await cmd_center.handle_callback("btn_ignore:wf_test_10", user_id=user_id)
    assert res_ignore["status"] == "SUCCESS"
    assert res_ignore["action"] == "IGNORE"

    # Test RESUME callback
    res_resume = await cmd_center.handle_callback("btn_resume:wf_test_10", user_id=user_id)
    assert res_resume["status"] == "SUCCESS"
    assert res_resume["action"] == "RESUME"


def test_telegram_webhook_api(client):
    auth_user_id = settings.TELEGRAM_ALLOWED_USER_IDS[0] if settings.TELEGRAM_ALLOWED_USER_IDS else "123456789"
    webhook_payload = {
        "update_id": 10001,
        "message": {
            "message_id": 1,
            "from": {"id": int(auth_user_id) if str(auth_user_id).isdigit() else 123456789, "first_name": "Admin"},
            "text": "/health"
        }
    }

    response = client.post("/api/v1/telegram/webhook", json=webhook_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert "System Health" in data["text"]
