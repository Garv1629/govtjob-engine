from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.dependencies import get_db
from app.api.schemas.common import APIResponse
from app.modules.automation import AutomationRunner
from app.modules.eligibility.schemas import CandidateProfileInput
from app.db.repositories import AutomationSessionRepository

router = APIRouter(prefix="/automation", tags=["Browser Automation Engine"])


class StartAutomationRequestPayload(BaseModel):
    application_id: str
    job_id: str
    user_id: str
    credentials: Dict[str, str] = Field(default_factory=dict)
    documents_map: Dict[str, str] = Field(default_factory=dict)
    pause_for_payment: bool = Field(True, description="Pause for manual OTP / Payment verification")
    profile: CandidateProfileInput


class ResumeAutomationRequestPayload(BaseModel):
    confirmation_payload: Dict[str, Any] = Field(default_factory=dict)


@router.post("/start", response_model=APIResponse[dict])
async def start_automation(payload: StartAutomationRequestPayload, db: Session = Depends(get_db)):
    """Initiates automated job application workflow with safe manual pause hooks."""
    runner = AutomationRunner(db=db)
    try:
        res = await runner.execute_application_workflow(
            application_id=payload.application_id,
            job_id=payload.job_id,
            user_id=payload.user_id,
            profile=payload.profile,
            credentials=payload.credentials,
            documents_map=payload.documents_map,
            pause_for_payment=payload.pause_for_payment
        )
        return APIResponse(data=res, message="Automation workflow initiated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation error: {str(e)}")


@router.post("/{session_id}/resume", response_model=APIResponse[dict])
async def resume_automation(session_id: str, payload: ResumeAutomationRequestPayload, db: Session = Depends(get_db)):
    """Resumes paused automation session post OTP/payment completion."""
    runner = AutomationRunner(db=db)
    try:
        res = await runner.resume_workflow(
            session_id=session_id,
            confirmation_payload=payload.confirmation_payload
        )
        return APIResponse(data=res, message="Automation workflow resumed and completed successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume error: {str(e)}")


@router.get("/{session_id}/status", response_model=APIResponse[dict])
def get_automation_status(session_id: str, db: Session = Depends(get_db)):
    """Retrieves session state, screenshot path, and audit log events."""
    repo = AutomationSessionRepository(db)
    rec = repo.get_by_id(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    payload = {
        "id": rec.id,
        "application_id": rec.application_id,
        "job_id": rec.job_id,
        "user_id": rec.user_id,
        "source_code": rec.source_code,
        "current_state": rec.current_state,
        "manual_action_reason": rec.manual_action_reason,
        "latest_screenshot_path": rec.latest_screenshot_path,
        "receipt_path": rec.receipt_path,
        "audit_logs": rec.audit_logs,
        "created_at": rec.created_at,
        "updated_at": rec.updated_at
    }
    return APIResponse(data=payload, message="Automation status retrieved successfully")
