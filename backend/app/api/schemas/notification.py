from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    id: str
    job_id: str
    eligibility_status: str
    confidence_score: float
    user_action: str
    sent_at: datetime

    model_config = ConfigDict(from_attributes=True)
