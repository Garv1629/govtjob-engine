from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    user_id: str
    status: str
    application_number: Optional[str] = None
    payment_status: str
    payment_amount: float
    receipt_pdf_url: Optional[str] = None
    error_message: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
