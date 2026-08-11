import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logging import logger
from app.modules.notifications.telegram_bot import TelegramCardFormatter, TelegramBotCommandCenter, TelegramSecurity


class TelegramNotificationService:
    """
    Production-grade Telegram Notification Service supporting live status updates,
    rich job notification cards, manual action alerts, completion cards, and error alerts.
    """

    def __init__(self, db_session=None):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.formatter = TelegramCardFormatter()
        self.command_center = TelegramBotCommandCenter(db_session=db_session)
        self.base_url = f"https://api.telegram.org/bot{self.token}" if self.token else None

    async def send_job_alert(
        self,
        job_data: Dict[str, Any],
        eligibility: Optional[Dict[str, Any]] = None,
        workflow_id: str = "wf_demo_1"
    ) -> bool:
        """Sends rich job alert card with inline action buttons."""
        card_text = self.formatter.format_job_notification_card(job_data, eligibility)
        pdf_url = job_data.get("pdf_url", "https://govjob.gov.in/notification.pdf")
        website = job_data.get("website_url", "https://govjob.gov.in")
        apply_url = job_data.get("apply_url", "https://govjob.gov.in/apply")

        inline_keyboard = self.formatter.get_job_card_inline_keyboard(workflow_id, pdf_url, website, apply_url)
        return await self._send_telegram_message(self.chat_id, card_text, inline_keyboard)

    async def send_live_status_update(
        self,
        chat_id: str,
        message_id: str,
        workflow_id: str,
        status_text: str,
        step: str = ""
    ) -> bool:
        """Edits an existing Telegram message to show live progress."""
        text = self.formatter.format_live_status_card(workflow_id, status_text, step)
        logger.info(f"[TelegramService] Editing message '{message_id}' for workflow '{workflow_id}': {status_text}")
        if not self.base_url or not chat_id or not message_id:
            return True

        url = f"{self.base_url}/editMessageText"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"[TelegramService] Error editing live status: {str(e)}")
            return False

    async def send_manual_action_required(
        self,
        workflow_id: str,
        reason: str,
        screenshot_path: Optional[str] = None
    ) -> bool:
        """Sends manual intervention alert when workflow pauses for OTP/CAPTCHA/Payment."""
        text = self.formatter.format_manual_action_card(workflow_id, reason, screenshot_path)
        keyboard = self.formatter.get_manual_action_inline_keyboard(workflow_id)
        return await self._send_telegram_message(self.chat_id, text, keyboard)

    async def send_completion_alert(
        self,
        workflow_id: str,
        application_number: str,
        portal_name: str,
        receipt_path: Optional[str] = None,
        duration_seconds: float = 0.0
    ) -> bool:
        """Sends application submission completion card."""
        text = self.formatter.format_completion_card(
            workflow_id=workflow_id,
            application_number=application_number,
            portal_name=portal_name,
            receipt_path=receipt_path,
            duration_seconds=duration_seconds
        )
        return await self._send_telegram_message(self.chat_id, text)

    async def send_failure_alert(self, workflow_id: str, reason: str) -> bool:
        """Sends workflow failure card with recovery suggestions and retry button."""
        text = self.formatter.format_failure_card(workflow_id, reason)
        keyboard = [[{"text": "🔄 Retry Workflow", "callback_data": f"btn_retry:{workflow_id}"}]]
        return await self._send_telegram_message(self.chat_id, text, keyboard)

    async def _send_telegram_message(
        self,
        chat_id: str,
        text: str,
        reply_markup: Optional[List[List[Dict[str, str]]]] = None
    ) -> bool:
        """Internal helper sending text message via Telegram API or logging in dry-run mode."""
        logger.info(f"[TelegramService] Sending message to chat '{chat_id or self.chat_id}'")
        if not self.base_url or not (chat_id or self.chat_id):
            logger.info(f"[TelegramService] Dry-Run Mode (Token/Chat ID not configured):\n{text}")
            return True

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id or self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = {"inline_keyboard": reply_markup}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"[TelegramService] Error sending Telegram message: {str(e)}")
            return False
