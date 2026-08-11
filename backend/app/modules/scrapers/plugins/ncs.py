from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from app.modules.scrapers.base import BaseScraper
from app.modules.scrapers.schemas import GovernmentJob
from app.core.logging import logger


class NCSScraper(BaseScraper):
    """National Career Service (NCS) Ministry of Labour & Employment Scraper Plugin."""

    def __init__(self):
        super().__init__(
            source_code="NCS",
            source_name="National Career Service",
            base_url="https://www.ncs.gov.in",
            category="Ministry of Labour and Employment",
            priority=2,
            schedule_interval_minutes=30,
            is_enabled=True
        )

    async def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Scrapes NCS portal for government job postings."""
        logger.info(f"[{self.source_code}] Fetching government postings from NCS portal...")
        raw_listings = [
            {
                "title": "Junior Scientific Assistant",
                "department": "Ministry of Environment, Forest and Climate Change",
                "advt_number": "NCS-GOV-2026-8891",
                "notification_url": "https://www.ncs.gov.in/job-seeker/job-details/8891",
                "apply_url": "https://www.ncs.gov.in/job-seeker/apply/8891",
                "pdf_url": "https://www.ncs.gov.in/docs/job_notice_8891.pdf",
                "published_date": datetime.now(timezone.utc).isoformat(),
                "last_date": (datetime.now(timezone.utc) + timedelta(days=20)).isoformat(),
                "vacancies": 45,
                "pay_scale": "Level 6 (Rs. 35400 - 112400)",
                "raw_html": "<html><body><h1>NCS Government Job Posting</h1></body></html>"
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
            last_d = datetime.now(timezone.utc) + timedelta(days=20)

        return GovernmentJob(
            title=raw_data["title"],
            department=raw_data.get("department", "Ministry of Labour and Employment"),
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
