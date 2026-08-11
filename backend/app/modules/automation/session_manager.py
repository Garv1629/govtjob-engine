import json
from typing import Dict, Any, List
from app.core.logging import logger

try:
    from playwright.async_api import BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    BrowserContext = Any


class SessionManager:
    """Handles session reuse, cookie persistence, and browser state restoration."""

    @staticmethod
    async def export_cookies(context: Any) -> List[Dict[str, Any]]:
        if not PLAYWRIGHT_AVAILABLE or not context:
            return []
        cookies = await context.cookies()
        logger.info(f"Exported {len(cookies)} session cookies.")
        return cookies

    @staticmethod
    async def import_cookies(context: Any, cookies: List[Dict[str, Any]]):
        if not PLAYWRIGHT_AVAILABLE or not context:
            return
        if cookies:
            await context.add_cookies(cookies)
            logger.info(f"Restored {len(cookies)} session cookies into browser context.")
