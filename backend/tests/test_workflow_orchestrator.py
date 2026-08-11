import pytest
from app.modules.workflow.orchestrator import WorkflowOrchestrator
from app.modules.workflow.enums import WorkflowState, UserDecision
from app.db.repositories import WorkflowInstanceRepository


@pytest.mark.asyncio
async def test_workflow_orchestrator_start_job_pipeline(db_session):
    orchestrator = WorkflowOrchestrator(db=db_session)
    job_payload = {
        "source_code": "SSC",
        "organization": "Staff Selection Commission",
        "advt_number": "SSC-CGL-2026",
        "job_title": "Combined Graduate Level Examination 2026",
        "total_vacancies": 12000,
        "pdf_url": "https://ssc.gov.in/notifications/cgl2026.pdf",
        "apply_url": "https://ssc.gov.in/apply"
    }

    res = await orchestrator.start_job_workflow(job_data=job_payload, user_id="user_test_99")

    assert res["workflow_id"] is not None
    assert res["current_state"] == WorkflowState.WAITING_FOR_USER.value
    assert res["eligibility_status"] in ["ELIGIBLE", "PARTIALLY_ELIGIBLE", "NOT_ELIGIBLE"]


@pytest.mark.asyncio
async def test_workflow_user_decision_ignore(db_session):
    orchestrator = WorkflowOrchestrator(db=db_session)
    job_payload = {
        "source_code": "UPSC",
        "organization": "Union Public Service Commission",
        "advt_number": "UPSC-CSE-2026",
        "job_title": "Civil Services Examination 2026",
        "total_vacancies": 1000,
        "pdf_url": "https://upsc.gov.in/notifications/cse2026.pdf",
        "apply_url": "https://upsc.gov.in/apply"
    }

    start_res = await orchestrator.start_job_workflow(job_data=job_payload, user_id="user_test_99")
    wf_id = start_res["workflow_id"]

    decision_res = await orchestrator.process_user_decision(
        workflow_id=wf_id,
        decision=UserDecision.IGNORE
    )

    assert decision_res["current_state"] == WorkflowState.CANCELLED.value
    assert decision_res["status"] == "STOPPED_AND_ARCHIVED"


@pytest.mark.asyncio
async def test_workflow_user_decision_apply_and_resume(db_session):
    orchestrator = WorkflowOrchestrator(db=db_session)
    job_payload = {
        "source_code": "SSC",
        "organization": "Staff Selection Commission",
        "advt_number": "SSC-CHSL-2026",
        "job_title": "Combined Higher Secondary Level 2026",
        "total_vacancies": 4500,
        "pdf_url": "https://ssc.gov.in/notifications/chsl2026.pdf",
        "apply_url": "https://ssc.gov.in/apply"
    }

    start_res = await orchestrator.start_job_workflow(job_data=job_payload, user_id="user_test_99")
    wf_id = start_res["workflow_id"]

    # 1. APPLY -> Browser Automation runs & pauses for payment/OTP
    apply_res = await orchestrator.process_user_decision(
        workflow_id=wf_id,
        decision=UserDecision.APPLY
    )

    assert apply_res["current_state"] == WorkflowState.WAITING_FOR_MANUAL_ACTION.value

    # 2. User confirms payment/OTP -> Resume workflow
    resume_res = await orchestrator.resume_manual_action(
        workflow_id=wf_id,
        confirmation_payload={"action_completed": True, "otp": "123456"}
    )

    assert resume_res["current_state"] == WorkflowState.COMPLETED.value
    assert resume_res["application_number"] is not None


def test_workflow_api_endpoints(client):
    # 1. Trigger API
    trigger_payload = {
        "user_id": "user_api_1",
        "source_code": "SSC",
        "organization": "Staff Selection Commission",
        "advt_number": "SSC-MTS-2026",
        "job_title": "Multi Tasking Staff 2026",
        "pdf_url": "https://ssc.gov.in/mts.pdf",
        "apply_url": "https://ssc.gov.in/apply_mts",
        "total_vacancies": 8000
    }

    response = client.post("/api/v1/workflow/trigger", json=trigger_payload)
    assert response.status_code == 201
    data = response.json()
    wf_id = data["workflow_id"]

    # 2. Status API
    status_resp = client.get(f"/api/v1/workflow/{wf_id}")
    assert status_resp.status_code == 200
    assert status_resp.json()["current_state"] == "WAITING_FOR_USER"

    # 3. Decision API (IGNORE)
    dec_resp = client.post(f"/api/v1/workflow/{wf_id}/decision", json={"decision": "IGNORE"})
    assert dec_resp.status_code == 200
    assert dec_resp.json()["current_state"] == "CANCELLED"

    # 4. Metrics API
    metrics_resp = client.get("/api/v1/workflow/metrics")
    assert metrics_resp.status_code == 200
    assert "current_workflows_count" in metrics_resp.json()
