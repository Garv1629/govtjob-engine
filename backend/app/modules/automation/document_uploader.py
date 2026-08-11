import os
from typing import Dict, Any, Tuple
from app.core.logging import logger

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any


class DocumentUploader:
    """Validates file types, dimensions, and sizes before executing browser file uploads."""

    MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024 # 5 MB

    @staticmethod
    def validate_file(file_path: str, allowed_extensions: tuple = (".jpg", ".jpeg", ".png", ".pdf")) -> Tuple[bool, str]:
        if not os.path.exists(file_path):
            return False, f"File does not exist at path '{file_path}'"

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_extensions:
            return False, f"Invalid extension '{ext}'. Allowed: {allowed_extensions}"

        size = os.path.getsize(file_path)
        if size > DocumentUploader.MAX_FILE_SIZE_BYTES:
            return False, f"File size ({size/1024:.1f} KB) exceeds maximum limit of 5 MB."

        return True, "File validation successful."

    @staticmethod
    async def upload_file(page: Any, selector: str, file_path: str, doc_name: str = "document") -> bool:
        if not PLAYWRIGHT_AVAILABLE or not page:
            return False
        valid, msg = DocumentUploader.validate_file(file_path)
        if not valid:
            logger.error(f"DocumentUploader: Validation failed for '{doc_name}': {msg}")
            return False

        try:
            await page.wait_for_selector(selector, timeout=5000)
            await page.set_input_files(selector, file_path)
            logger.info(f"DocumentUploader: Successfully uploaded '{doc_name}' ({file_path})")
            return True
        except Exception as e:
            logger.error(f"DocumentUploader: Upload error for '{doc_name}': {str(e)}")
            return False
