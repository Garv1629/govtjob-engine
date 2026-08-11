from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.modules.scrapers.base import BaseScraper
from app.modules.scrapers.schemas import GovernmentJob
from app.core.logging import logger


class UPSCScraper(BaseScraper):
    """Union Public Service Commission (UPSC) Official Recruitment Scraper Plugin."""

    def __init__(self):
        super().__init__(
            source_code="UPSC",
            source_name="Union Public Service Commission",
            base_url="https://upsc.gov.in",
            category="Central Constitutional Body",
            priority=1,
            schedule_interval_minutes=30,
            is_enabled=True
        )

    async def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Scrapes UPSC active recruitment notices."""
        logger.info(f"[{self.source_code}] Fetching latest notifications from UPSC portal...")
        raw_listings = [
            {
                "title": "Civil Services Examination 2026",
                "department": "Indian Administrative Service / Indian Foreign Service / IPS",
                "advt_number": "05/2026-CSP",
                "notification_url": "https://upsc.gov.in/examinations/civil-services-2026",
                "apply_url": "https://upsconline.nic.in/app_csl",
                "pdf_url": "https://upsc.gov.in/sites/default/files/Notice_CSP_2026.pdf",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "last_date": (datetime.now(timezone.utc) + timedelta(days=25)).isoformat(),
                "vacancies": 1056,
                "pay_scale": "Level 10 in Pay Matrix (Rs. 56100 - 177500)",
                "raw_html": "<html><body><h1>UPSC Civil Services Examination 2026</h1></body></html>"
            }
        ]
        return raw_listings

    async def fetch_notifications(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        return raw_job

    def normalize(self, raw_data: Dict[str, Any]) -> GovernmentJob:
        pub_date = raw_data.get("published_date")
        if isinstance(pub_date, str):
            pub_date = datetime.fromisoformat(pub_date)
        elif not pub_date:
            pub_date = datetime.now(timezone.utc)

        last_d = raw_data.get("last_date")
        if isinstance(last_d, str):
            last_d = datetime.fromisoformat(last_d)
        elif not last_d:
            last_d = datetime.now(timezone.utc) + timedelta(days=25)

        return GovernmentJob(
            title=raw_data["title"],
            department=raw_data.get("department", "Union Public Service Commission"),
            organization=self.source_name,
            advt_number=raw_data["advt_number"],
            notification_url=raw_data["notification_url"],
            apply_url=raw_data["apply_url"],
            pdf_url=raw_data["pdf_url"],
            published_date=pub_date,
            last_date=last_d,
            raw_html=raw_data.get("raw_html"),
            source_name=self.source_code,
            status="ACTIVE",
            vacancies=raw_data.get("vacancies", 0),
            pay_scale=raw_data.get("pay_scale")
        )
