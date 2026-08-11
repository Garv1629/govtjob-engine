import io
from pypdf import PdfReader
from app.core.logging import logger


class NativePDFParser:
    """Extracts raw text content from multi-page native PDFs."""

    @staticmethod
    def extract_text(pdf_bytes: bytes) -> str:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_pages = []
        
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            extracted_pages.append(f"--- PAGE {idx + 1} ---\n" + page_text)

        full_text = "\n\n".join(extracted_pages)
        logger.info(f"Extracted {len(full_text)} characters from {len(reader.pages)} PDF pages.")
        return full_text
