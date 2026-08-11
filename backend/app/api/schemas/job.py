from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    id: str
    source_code: str
    organization: str
    department: Optional[str] = None
    advt_number: str
    job_title: str
    total_vacancies: int
    pay_level: Optional[str] = None
    grade_pay: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    last_date: datetime
    pdf_url: str
    apply_url: str
    content_hash: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
