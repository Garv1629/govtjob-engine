import pytest
from app.modules.automation import AutomationStateMachine, AutomationState, DocumentUploader, PortalAdapterRegistry, AutomationRunner
from app.modules.eligibility.schemas import CandidateProfileInput
from app.db.repositories import JobRepository, AutomationSessionRepository


def test_automation_state_machine():
    sm = AutomationStateMachine(AutomationState.INITIALIZED)
    assert sm.current_state == AutomationState.INITIALIZED

    # Valid transition INITIALIZED -> LOGGED_IN
    assert sm.transition_to(AutomationState.LOGGED_IN) is True
    assert sm.current_state == AutomationState.LOGGED_IN

    # Valid transition LOGGED_IN -> FORM_IN_PROGRESS
    assert sm.transition_to(AutomationState.FORM_IN_PROGRESS) is True

    # Valid transition FORM_IN_PROGRESS -> WAITING_FOR_MANUAL_ACTION
    assert sm.transition_to(AutomationState.WAITING_FOR_MANUAL_ACTION) is True

    # Invalid transition check (WAITING_FOR_MANUAL_ACTION cannot jump directly to INITIALIZED)
    with pytest.raises(ValueError):
        sm.transition_to(AutomationState.INITIALIZED)


def test_document_uploader_validation(tmp_path):
    # Test non-existent file
    valid, msg = DocumentUploader.validate_file("invalid_path/file.pdf")
    assert valid is False

    # Test invalid extension file
    bad_ext_file = tmp_path / "test.exe"
    bad_ext_file.write_bytes(b"dummy exe content")
    valid_ext, msg_ext = DocumentUploader.validate_file(str(bad_ext_file))
    assert valid_ext is False
    assert "Invalid extension" in msg_ext

    # Test valid image file
    good_file = tmp_path / "photo.jpg"
    good_file.write_bytes(b"dummy photo content")
    valid_good, msg_good = DocumentUploader.validate_file(str(good_file))
    assert valid_good is True


@pytest.mark.asyncio
async def test_automation_runner_pause_and_resume(db_session):
    # Setup test job in DB
    job_repo = JobRepository(db_session)
    job = job_repo.create({
        "source_code": "SSC",
        "title": "SSC CGL 2026 Assistant Section Officer",
        "organization": "SSC",
        "advt_number": "HQ-CGL/2026/01",
        "notification_url": "https://ssc.gov.in/cgl",
        "apply_url": "https://ssc.gov.in/apply",
        "pdf_url": "https://ssc.gov.in/cgl.pdf",
        "last_date": "2026-09-15T18:00:00Z",
        "content_hash": "hash_auto_998877"
    })

    profile = CandidateProfileInput(
        user_id="user_auto_1",
        full_name="Ankit Sharma",
        dob="1998-04-12",
        category="GENERAL",
        degree="B.Tech"
    )

    runner = AutomationRunner(db_session)
    
    # 1. Execute Application (Pause for Payment = True)
    start_res = await runner.execute_application_workflow(
        application_id="app_12345",
        job_id=job.id,
        user_id="user_auto_1",
        profile=profile,
        credentials={"registration_number": "REG123456", "password": "pass"},
        documents_map={"PHOTO": "artifacts/photo.jpg"},
        pause_for_payment=True
    )

    assert start_res["status"] == "WAITING_FOR_MANUAL_ACTION"
    assert start_res["manual_action_reason"] == "PAYMENT_AND_OTP_VERIFICATION"
    session_id = start_res["session_id"]

    # Verify session recorded in DB
    session_repo = AutomationSessionRepository(db_session)
    session_db = session_repo.get_by_id(session_id)
    assert session_db is not None
    assert session_db.current_state == "WAITING_FOR_MANUAL_ACTION"

    # 2. Resume Workflow after Manual Payment Confirmation
    resume_res = await runner.resume_workflow(
        session_id=session_id,
        confirmation_payload={"payment_status": "SUCCESS", "transaction_ref": "TXN99887766"}
    )

    assert resume_res["status"] == "SUBMITTED"
    assert "receipt_path" in resume_res
    
    # Verify final DB update
    updated_session = session_repo.get_by_id(session_id)
    assert updated_session.current_state == "SUBMITTED"


def test_automation_api_endpoints(client, db_session):
    job_repo = JobRepository(db_session)
    job = job_repo.create({
        "source_code": "UPSC",
        "title": "UPSC IAS 2026",
        "organization": "UPSC",
        "advt_number": "05/2026-CSP",
        "notification_url": "https://upsc.gov.in/ias",
        "apply_url": "https://upsc.gov.in/apply",
        "pdf_url": "https://upsc.gov.in/ias.pdf",
        "last_date": "2026-08-28T18:00:00Z",
        "content_hash": "hash_upsc_auto_5544"
    })

    # Start Automation API
    start_resp = client.post("/api/v1/automation/start", json={
        "application_id": "app_api_555",
        "job_id": job.id,
        "user_id": "user_api_555",
        "pause_for_payment": True,
        "credentials": {"registration_number": "RID998877"},
        "profile": {
            "user_id": "user_api_555",
            "full_name": "Siddharth Malhotra",
            "dob": "1997-09-21",
            "category": "GENERAL",
            "degree": "B.Sc"
        }
    })

    assert start_resp.status_code == 200
    res_data = start_resp.json()
    assert res_data["success"] is True
    session_id = res_data["data"]["session_id"]
    assert res_data["data"]["status"] == "WAITING_FOR_MANUAL_ACTION"

    # Status API
    status_resp = client.get(f"/api/v1/automation/{session_id}/status")
    assert status_resp.status_code == 200
    stat_json = status_resp.json()
    assert stat_json["data"]["current_state"] == "WAITING_FOR_MANUAL_ACTION"

    # Resume API
    resume_resp = client.post(f"/api/v1/automation/{session_id}/resume", json={
        "confirmation_payload": {"otp_verified": True}
    })
    assert resume_resp.status_code == 200
    res_res_json = resume_resp.json()
    assert res_res_json["data"]["status"] == "SUBMITTED"
