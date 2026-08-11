import re
from typing import List
from app.core.logging import logger


class TextCleanerAndChunker:
    """Cleans document text, strips repetitive header/footer boilerplate, and builds LLM context chunks."""

    @staticmethod
    def clean_text(raw_text: str) -> str:
        if not raw_text:
            return ""

        # Remove repetitive page headers/footers
        text = re.sub(r"--- PAGE \d+ ---", "\n", raw_text)
        text = re.sub(r"Page \d+ of \d+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"www\.[a-zA-Z0-9\.\-]+\.(gov|nic|in)", "", text, flags=re.IGNORECASE)

        # Normalize whitespace and multiple newlines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned = "\n".join(lines)
        
        logger.debug(f"Cleaned raw text from {len(raw_text)} to {len(cleaned)} characters.")
        return cleaned

    @staticmethod
    def generate_chunks(cleaned_text: str, max_chunk_tokens: int = 4000) -> List[str]:
        """Splits long document text into processing chunks if PDF exceeds single LLM context window."""
        max_chars = max_chunk_tokens * 4
        if len(cleaned_text) <= max_chars:
            return [cleaned_text]

        chunks = []
        start = 0
        while start < len(cleaned_text):
            end = min(start + max_chars, len(cleaned_text))
            chunks.append(cleaned_text[start:end])
            start += max_chars - 500  # 500 chars overlap
            
        logger.info(f"Split document into {len(chunks)} context chunks.")
        return chunks
