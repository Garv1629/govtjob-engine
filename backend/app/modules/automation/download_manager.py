import os
from typing import Any
from app.core.logging import logger

try:
    from playwright.async_api import Download
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Download = Any


class DownloadManager:
    """Manages application receipt downloads and payment acknowledgment PDFs."""

    def __init__(self, output_dir: str = "artifacts/receipts"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def save_download(self, download: Any, custom_filename: str = "receipt.pdf") -> str:
        if not PLAYWRIGHT_AVAILABLE or not download:
            return ""
        target_path = os.path.join(self.output_dir, custom_filename)
        await download.save_as(target_path)
        logger.info(f"Saved downloaded application receipt to: {target_path}")
        return target_path
