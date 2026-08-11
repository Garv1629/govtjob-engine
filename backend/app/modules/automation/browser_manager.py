import os
from typing import Optional, Any
from app.core.logging import logger

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    async_playwright = None
    Browser = Any
    BrowserContext = Any
    Page = Any


class BrowserManager:
    """Manages Playwright browser instances, headless modes, context configurations, and cleanup."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Any] = None
        self.context: Optional[Any] = None

    async def initialize(self) -> Any:
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright is not available in current environment. Returning mock context.")
            return None

        logger.info(f"Initializing Playwright Browser (Headless={self.headless})...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            accept_downloads=True
        )
        return self.context

    async def new_page(self) -> Any:
        if not PLAYWRIGHT_AVAILABLE:
            return None
        if not self.context:
            await self.initialize()
        return await self.context.new_page() if self.context else None

    async def shutdown(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Playwright Browser Manager shut down successfully.")
