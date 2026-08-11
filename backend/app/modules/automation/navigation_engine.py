from typing import Any
from app.core.logging import logger

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any


class NavigationEngine:
    """Handles multi-step form navigation, page readiness wait hooks, and dynamic validation messages."""

    @staticmethod
    async def navigate_to(page: Any, url: str, wait_until: str = "networkidle"):
        if not PLAYWRIGHT_AVAILABLE or not page:
            return
        logger.info(f"NavigationEngine: Opening URL: {url}")
        await page.goto(url, wait_until=wait_until, timeout=30000)

    @staticmethod
    async def click_next_or_submit(page: Any, selector: str, step_name: str = "Step"):
        if not PLAYWRIGHT_AVAILABLE or not page:
            return
        logger.info(f"NavigationEngine: Clicking next button for {step_name} at selector '{selector}'")
        await page.wait_for_selector(selector, timeout=5000)
        await page.click(selector)
        await page.wait_for_load_state("networkidle")
