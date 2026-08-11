import httpx
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.modules.scrapers.schemas import GovernmentJob
from app.core.logging import logger


class BaseScraper(ABC):
    """
    Abstract Base Scraper for all Government Job Source Plugins.
    Every scraper plugin MUST implement the 8 required lifecycle methods:
    1. initialize()
    2. health_check()
    3. fetch_jobs()
    4. fetch_notifications()
    5. normalize()
    6. validate()
    7. save()
    8. shutdown()
    """

    def __init__(
        self,
        source_code: str,
        source_name: str,
        base_url: str,
        category: str = "Central Government",
        priority: int = 1,
        schedule_interval_minutes: int = 30,
        is_enabled: bool = True
    ):
        self.source_code = source_code
        self.source_name = source_name
        self.base_url = base_url
        self.category = category
        self.priority = priority
        self.schedule_interval_minutes = schedule_interval_minutes
        self.is_enabled = is_enabled
        self.client: Optional[httpx.AsyncClient] = None
        self._is_initialized = False

    async def initialize(self) -> None:
        """1. Initializes Async HTTP Client and SSL/Proxy configurations."""
        if not self._is_initialized:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(30.0),
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                },
                follow_redirects=True
            )
            self._is_initialized = True
            logger.info(f"[{self.source_code}] Plugin initialized for base URL: {self.base_url}")

    async def health_check(self) -> bool:
        """2. Checks portal reachability and HTTP status."""
        if not self.client:
            await self.initialize()
        try:
            response = await self.client.get("/")
            is_healthy = response.status_code < 400
            logger.info(f"[{self.source_code}] Health check status: {response.status_code} ({is_healthy})")
            return is_healthy
        except Exception as e:
            logger.error(f"[{self.source_code}] Health check failed: {str(e)}")
            return False

    @abstractmethod
    async def fetch_jobs(self) -> List[Dict[str, Any]]:
        """3. Fetches raw job listing pages/APIs from official portal."""
        pass

    @abstractmethod
    async def fetch_notifications(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        """4. Fetches raw notification details, HTML payload, and PDF URL for a specific notice."""
        pass

    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> GovernmentJob:
        """5. Transforms raw portal JSON/HTML payload into unified GovernmentJob model."""
        pass

    def validate(self, job: GovernmentJob) -> bool:
        """6. Validates mandatory GovernmentJob fields."""
        if not job.title or not job.advt_number or not job.pdf_url:
            logger.warning(f"[{self.source_code}] Job validation failed: Missing title, advt_number, or pdf_url")
            return False
        if not job.last_date:
            logger.warning(f"[{self.source_code}] Job validation failed: Missing last_date")
            return False
        return True

    async def save(self, job: GovernmentJob) -> bool:
        """7. Lifecycle hook to handle custom plugin storage if needed."""
        logger.debug(f"[{self.source_code}] Validated job payload ready for engine persistence: {job.title}")
        return True

    async def shutdown(self) -> None:
        """8. Cleans up HTTP client sessions and connection pools."""
        if self.client and not self.client.is_closed:
            await self.client.aclose()
            self._is_initialized = False
            logger.info(f"[{self.source_code}] Plugin shutdown completed.")
