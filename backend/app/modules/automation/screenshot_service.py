import os
import uuid
from typing import Any
from app.core.logging import logger

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any


class ScreenshotService:
    """Captures page screenshots and saves them for user visual verification during manual pauses or audits."""

    def __init__(self, output_dir: str = "artifacts/screenshots"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def capture(self, page: Any, name_prefix: str = "step") -> str:
        if not PLAYWRIGHT_AVAILABLE or not page:
            return ""
        filename = f"{name_prefix}_{uuid.uuid4().hex[:8]}.png"
        path = os.path.join(self.output_dir, filename)
        
        try:
            await page.screenshot(path=path, full_page=True)
            logger.info(f"Captured full page screenshot: {path}")
            return path
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            return ""
