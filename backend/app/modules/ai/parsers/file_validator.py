import io
from typing import Dict, Any, Tuple
from pypdf import PdfReader
from app.core.logging import logger


class FileValidatorAndFormatDetector:
    """
    Validates document payloads and detects format types:
    NATIVE_PDF, SCANNED_PDF, ENCRYPTED_PDF, BLANK_PDF, CORRUPTED_PDF, HTML_PAGE, IMAGE.
    """

    @staticmethod
    def inspect_bytes(file_bytes: bytes, file_name: str = "document.pdf") -> Tuple[str, Dict[str, Any]]:
        """Inspects binary payload and returns detected format & metadata."""
        if not file_bytes or len(file_bytes) == 0:
            return "BLANK_PDF", {"error": "Empty or zero-byte document payload."}

        # Check if HTML payload
        snippet = file_bytes[:500].decode("utf-8", errors="ignore").lower()
        if "<html" in snippet or "<!doctype html" in snippet or "<body" in snippet:
            return "HTML_PAGE", {"size_bytes": len(file_bytes), "is_html": True}

        # Attempt PDF parsing via PyPDF
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            
            # Check Encryption
            if reader.is_encrypted:
                logger.warning(f"File {file_name} is password protected or encrypted.")
                return "ENCRYPTED_PDF", {"error": "Password protected / encrypted PDF document."}

            total_pages = len(reader.pages)
            if total_pages == 0:
                return "BLANK_PDF", {"error": "PDF has 0 pages."}

            # Check for scanned vs native text pages
            text_char_count = 0
            for i in range(min(total_pages, 5)):
                page_text = reader.pages[i].extract_text() or ""
                text_char_count += len(page_text.strip())

            avg_chars_per_page = text_char_count / min(total_pages, 5)
            
            if avg_chars_per_page < 30:
                # Scanned PDF detected (page contains minimal or no extractable text characters)
                logger.info(f"File {file_name} detected as SCANNED_PDF (Avg chars/page: {avg_chars_per_page:.1f})")
                return "SCANNED_PDF", {
                    "total_pages": total_pages,
                    "avg_chars_per_page": avg_chars_per_page,
                    "requires_ocr": True
                }

            logger.info(f"File {file_name} detected as NATIVE_PDF (Avg chars/page: {avg_chars_per_page:.1f})")
            return "NATIVE_PDF", {
                "total_pages": total_pages,
                "avg_chars_per_page": avg_chars_per_page,
                "requires_ocr": False
            }

        except Exception as e:
            logger.error(f"Corrupted PDF or invalid binary stream for {file_name}: {str(e)}")
            return "CORRUPTED_PDF", {"error": f"Failed to parse binary PDF header: {str(e)}"}
