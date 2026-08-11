from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.modules.automation.state_machine import AutomationStateMachine, AutomationState
from app.modules.automation.browser_manager import BrowserManager
from app.modules.automation.session_manager import SessionManager
from app.modules.automation.registry import PortalAdapterRegistry
from app.modules.automation.audit_logger import AutomationAuditLogger
from app.modules.eligibility.schemas import CandidateProfileInput
from app.db.repositories import AutomationSessionRepository, JobRepository
from app.core.logging import logger


class AutomationRunner:
    """
    High-level Browser Automation Runner executing full application workflows.
    Safely pauses at CAPTCHA / OTP / Payment manual intervention points and resumes state.
    """

    def __init__(self, db: Session):
        self.db = db
        self.session_repo = AutomationSessionRepository(db)
        self.job_repo = JobRepository(db)
        self.audit = AutomationAuditLogger()

    async def execute_application_workflow(
        self,
        application_id: str,
        job_id: str,
        user_id: str,
        profile: CandidateProfileInput,
        credentials: Dict[str, str],
        documents_map: Dict[str, str],
        pause_for_payment: bool = True
    ) -> Dict[str, Any]:
        job_record = self.job_repo.get_by_id(job_id)
        source_code = job_record.source_code if job_record else "SSC"

        state_machine = AutomationStateMachine(AutomationState.INITIALIZED)
        self.audit.log_event("STATE_CHANGE", f"State transitioned to {state_machine.current_state}")

        bm = BrowserManager(headless=True)
        page = await bm.new_page()
        adapter = PortalAdapterRegistry.get_adapter(source_code, page)

        try:
            # 1. Initialize
            await adapter.initialize()
            
            # 2. Login
            await adapter.login(credentials)
            state_machine.transition_to(AutomationState.LOGGED_IN)
            self.audit.log_event("STATE_CHANGE", "Logged in to recruitment portal successfully")

            # 3. Open Form
            await adapter.open_application(job_record.advt_number if job_record else "2026/01")
            state_machine.transition_to(AutomationState.FORM_IN_PROGRESS)

            # 4. Fill Sections
            await adapter.fill_profile(profile)
            self.audit.log_event("FORM_FILL", "Candidate personal details filled")

            await adapter.fill_education(profile)
            self.audit.log_event("FORM_FILL", "Education details filled")

            await adapter.fill_experience(profile)
            self.audit.log_event("FORM_FILL", "Experience details filled")

            # 5. Upload Documents
            await adapter.upload_documents(documents_map)
            self.audit.log_event("DOCUMENT_UPLOAD", "Candidate documents uploaded to portal")

            # 6. Review Page
            await adapter.review_application()
            state_machine.transition_to(AutomationState.READY_TO_SUBMIT)

            # 7. Check for Manual Step (Payment / OTP)
            if pause_for_payment:
                state_machine.transition_to(AutomationState.WAITING_FOR_MANUAL_ACTION)
                pause_info = await adapter.pause_for_manual_step("PAYMENT_AND_OTP_VERIFICATION")
                screenshot_path = await adapter.capture_screenshot("payment_pause")

                # Save state to Database
                session_record = self.session_repo.create({
                    "application_id": application_id,
                    "job_id": job_id,
                    "user_id": user_id,
                    "source_code": source_code,
                    "current_state": AutomationState.WAITING_FOR_MANUAL_ACTION.value,
                    "manual_action_reason": "PAYMENT_AND_OTP_VERIFICATION",
                    "latest_screenshot_path": screenshot_path,
                    "state_payload": {"advt_number": job_record.advt_number if job_record else ""},
                    "audit_logs": self.audit.logs
                })

                await bm.shutdown()
                return {
                    "session_id": session_record.id,
                    "application_id": application_id,
                    "status": "WAITING_FOR_MANUAL_ACTION",
                    "manual_action_reason": "PAYMENT_AND_OTP_VERIFICATION",
                    "screenshot_path": screenshot_path,
                    "message": "Application filled and ready for submission. Paused for payment/OTP confirmation."
                }

            # 8. Submit Application (If auto-submit enabled)
            submit_res = await adapter.submit(Completing=True)
            state_machine.transition_to(AutomationState.SUBMITTED)
            receipt_path = await adapter.download_receipt()

            session_record = self.session_repo.create({
                "application_id": application_id,
                "job_id": job_id,
                "user_id": user_id,
                "source_code": source_code,
                "current_state": AutomationState.SUBMITTED.value,
                "receipt_path": receipt_path,
                "audit_logs": self.audit.logs
            })

            await bm.shutdown()
            return {
                "session_id": session_record.id,
                "application_id": application_id,
                "status": "SUBMITTED",
                "receipt_path": receipt_path,
                "submission_result": submit_res
            }

        except Exception as e:
            logger.error(f"AutomationRunner workflow error: {str(e)}")
            state_machine.current_state = AutomationState.FAILED
            self.audit.log_event("ERROR", f"Workflow execution failed: {str(e)}")
            await bm.shutdown()
            raise e

    async def resume_workflow(self, session_id: str, confirmation_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Resumes paused workflow after candidate completes payment or OTP confirmation."""
        session_record = self.session_repo.get_by_id(session_id)
        if not session_record or session_record.current_state != AutomationState.WAITING_FOR_MANUAL_ACTION.value:
            raise ValueError(f"Invalid session '{session_id}' or state is not WAITING_FOR_MANUAL_ACTION")

        self.audit.log_event("RESUME", f"Resuming workflow for session ID '{session_id}'")

        bm = BrowserManager(headless=True)
        page = await bm.new_page()
        adapter = PortalAdapterRegistry.get_adapter(session_record.source_code, page)

        await adapter.initialize()
        await adapter.resume_after_confirmation(confirmation_payload)

        # Submit
        submit_res = await adapter.submit(Completing=True)
        receipt_path = await adapter.download_receipt()

        self.session_repo.update(session_id, {
            "current_state": AutomationState.SUBMITTED.value,
            "receipt_path": receipt_path,
            "manual_action_reason": None,
            "audit_logs": session_record.audit_logs + self.audit.logs
        })

        await bm.shutdown()

        return {
            "session_id": session_id,
            "application_id": session_record.application_id,
            "status": "SUBMITTED",
            "receipt_path": receipt_path,
            "submission_result": submit_res
        }
