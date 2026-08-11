from typing import Dict, Any
from app.core.logging import logger

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any


class FormEngine:
    """
    Intelligent Form Engine for auto-detecting input fields, matching candidate profile attributes,
    selecting dropdowns, radios, checkboxes, and date pickers.
    """

    @staticmethod
    async def fill_input(page: Any, selector: str, value: str, field_name: str = "field"):
        if not PLAYWRIGHT_AVAILABLE or not page or not value:
            return
        try:
            await page.wait_for_selector(selector, timeout=5000)
            await page.fill(selector, str(value))
            logger.info(f"FormEngine: Filled '{field_name}' with value '{value}' at selector '{selector}'")
        except Exception as e:
            logger.warning(f"FormEngine: Failed to fill '{field_name}' ({selector}): {str(e)}")

    @staticmethod
    async def select_dropdown(page: Any, selector: str, value: str, field_name: str = "dropdown"):
        if not PLAYWRIGHT_AVAILABLE or not page or not value:
            return
        try:
            await page.wait_for_selector(selector, timeout=5000)
            await page.select_option(selector, label=value)
            logger.info(f"FormEngine: Selected option '{value}' in '{field_name}'")
        except Exception:
            try:
                await page.select_option(selector, value=value)
            except Exception as e:
                logger.warning(f"FormEngine: Could not select dropdown '{field_name}': {str(e)}")

    @staticmethod
    async def click_radio_or_checkbox(page: Any, selector: str, field_name: str = "control"):
        if not PLAYWRIGHT_AVAILABLE or not page:
            return
        try:
            await page.wait_for_selector(selector, timeout=5000)
            await page.check(selector)
            logger.info(f"FormEngine: Checked control '{field_name}'")
        except Exception as e:
            logger.warning(f"FormEngine: Could not check control '{field_name}': {str(e)}")
