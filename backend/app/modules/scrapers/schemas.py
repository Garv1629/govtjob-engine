from typing import Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


class GovernmentJob(BaseModel):
    """
    Unified Output Schema for every recruitment scraper plugin.
    Never exposes source-specific fields.
    """
    title: str = Field(..., description="Job Title / Post Name")
    department: Optional[str] = Field(None, description="Government Department or Ministry")
    organization: str = Field(..., description="Recruitment Body e.g. SSC, UPSC, NCS")
    advt_number: str = Field(..., description="Official Advertisement / Notification Number")
    
    notification_url: str = Field(..., description="Official Notification Landing Page URL")
    apply_url: str = Field(..., description="Direct Online Application Portal URL")
    pdf_url: str = Field(..., description="Direct Link to Official Notification PDF")
    
    published_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_date: datetime = Field(..., description="Application Submission Deadline")
    
    raw_html: Optional[str] = Field(None, description="Raw HTML Content captured from notification landing page")
    raw_pdf_bytes: Optional[bytes] = Field(None, description="Raw PDF binary payload if fetched")
    
    source_name: str = Field(..., description="Scraper Plugin Source Identifier")
    status: str = Field("ACTIVE", description="ACTIVE, UPDATED, WITHDRAWN")
    
    vacancies: Optional[int] = Field(0, description="Total Vacancies Announced")
    pay_scale: Optional[str] = Field(None, description="Pay Level or Salary Range")

    model_config = ConfigDict(arbitrary_types_allowed=True)
