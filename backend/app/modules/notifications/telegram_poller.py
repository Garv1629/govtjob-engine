import asyncio
import httpx
from app.core.config import settings
from app.core.logging import logger
from app.db.session import SessionLocal
from app.modules.notifications.telegram_bot import TelegramBotCommandCenter

poller_task: asyncio.Task | None = None
is_polling: bool = False

async def start_telegram_poller():
    """
    Background worker long-polling Telegram API for updates in local development mode.
    Enables instant responses to /start, /help, /jobs, /profile without public webhooks.
    """
    global is_polling
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("[TelegramPoller] No TELEGRAM_BOT_TOKEN set, skipping poller.")
        return

    is_polling = True
    offset = 0
    base_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"
    cmd_center = TelegramBotCommandCenter()

    logger.info("[TelegramPoller] Starting background Telegram long-poller worker...")

    async with httpx.AsyncClient(timeout=15.0) as client:
        while is_polling:
            try:
                url = f"{base_url}/getUpdates?offset={offset}&timeout=5"
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1

                        # Process Callback Queries (Buttons)
                        if "callback_query" in update:
                            cb = update["callback_query"]
                            cb_id = cb.get("id")
                            user = cb.get("from", {})
                            user_id = user.get("id")
                            cb_data = cb.get("data", "")
                            
                            db = SessionLocal()
                            try:
                                cmd_center = TelegramBotCommandCenter(db_session=db)
                                res = await cmd_center.handle_callback(cb_data, user_id)
                            finally:
                                db.close()
                            
                            # Answer Callback & Send Message
                            await client.post(f"{base_url}/answerCallbackQuery", json={"callback_query_id": cb_id})
                            if res.get("text"):
                                chat_id = cb.get("message", {}).get("chat", {}).get("id", user_id)
                                await client.post(f"{base_url}/sendMessage", json={"chat_id": chat_id, "text": res["text"], "parse_mode": "HTML"})

                        # Process Text Messages & Commands
                        elif "message" in update:
                            msg = update["message"]
                            user = msg.get("from", {})
                            user_id = user.get("id")
                            chat_id = msg.get("chat", {}).get("id")
                            text = msg.get("text", "").strip()

                            if text:
                                command = text.split()[0].lower()
                                if not command.startswith("/"):
                                    command = "/" + command
                                
                                args = text.split()[1:]
                                
                                db = SessionLocal()
                                try:
                                    cmd_center = TelegramBotCommandCenter(db_session=db)
                                    res = await cmd_center.handle_command(command, user_id, args)
                                finally:
                                    db.close()
                                
                                if res.get("text"):
                                    await client.post(f"{base_url}/sendMessage", json={"chat_id": chat_id, "text": res["text"], "parse_mode": "HTML"})
            except Exception as e:
                logger.error(f"[TelegramPoller] Error during update polling: {str(e)}")
                await asyncio.sleep(3.0)

            await asyncio.sleep(0.5)

def stop_telegram_poller():
    global is_polling
    is_polling = False
    logger.info("[TelegramPoller] Stopped background Telegram poller.")
