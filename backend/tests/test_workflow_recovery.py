import pytest
from app.modules.workflow.recovery import WorkflowRecovery
from app.db.repositories import WorkflowInstanceRepository
from app.modules.workflow.enums import WorkflowState, WorkflowStep


@pytest.mark.asyncio
async def test_exponential_backoff_calculation(db_session):
    recovery = WorkflowRecovery(db_session)
    d1 = await recovery.calculate_retry_delay(1)
    d2 = await recovery.calculate_retry_delay(2)
    d3 = await recovery.calculate_retry_delay(3)

    assert d1 > 0
    assert d2 > d1
    assert d3 > d2


def test_checkpoint_saving_and_retrieval(db_session):
    recovery = WorkflowRecovery(db_session)
    inst_repo = WorkflowInstanceRepository(db_session)

    # Create dummy workflow instance
    inst = inst_repo.create({
        "id": "wf_rec_test",
        "current_state": WorkflowState.PROCESSING.value,
        "current_step": WorkflowStep.EXTRACT_NOTIFICATION.value
    })

    cp = recovery.save_checkpoint(
        workflow_id="wf_rec_test",
        step_name=WorkflowStep.EXTRACT_NOTIFICATION.value,
        state=WorkflowState.PROCESSING.value,
        checkpoint_data={"extracted_fields": 10}
    )

    assert cp.id is not None
    assert cp.workflow_id == "wf_rec_test"

    latest = recovery.get_last_checkpoint("wf_rec_test")
    assert latest is not None
    assert latest.step_name == WorkflowStep.EXTRACT_NOTIFICATION.value
    assert latest.checkpoint_data["extracted_fields"] == 10


def test_retry_count_and_threshold_handling(db_session):
    recovery = WorkflowRecovery(db_session)
    inst_repo = WorkflowInstanceRepository(db_session)

    inst_repo.create({
        "id": "wf_retry_test",
        "current_state": WorkflowState.PROCESSING.value,
        "current_step": WorkflowStep.ELIGIBILITY_CHECK.value,
        "retry_count": 0
    })

    should_retry, count1 = recovery.handle_step_failure("wf_retry_test", "Network timeout", WorkflowStep.ELIGIBILITY_CHECK.value)
    assert should_retry is True
    assert count1 == 1

    should_retry2, count2 = recovery.handle_step_failure("wf_retry_test", "Network timeout", WorkflowStep.ELIGIBILITY_CHECK.value)
    assert should_retry2 is True
    assert count2 == 2

    should_retry3, count3 = recovery.handle_step_failure("wf_retry_test", "Network timeout", WorkflowStep.ELIGIBILITY_CHECK.value)
    assert should_retry3 is True
    assert count3 == 3

    # Exceeding max retries (settings.WORKFLOW_MAX_RETRIES = 3)
    should_retry4, count4 = recovery.handle_step_failure("wf_retry_test", "Network timeout", WorkflowStep.ELIGIBILITY_CHECK.value)
    assert should_retry4 is False
    assert count4 == 4


def test_crash_recovery_execution(db_session):
    recovery = WorkflowRecovery(db_session)
    inst_repo = WorkflowInstanceRepository(db_session)

    inst_repo.create({
        "id": "wf_crash_1",
        "current_state": WorkflowState.PROCESSING.value,
        "current_step": WorkflowStep.DOWNLOAD_NOTIFICATION.value
    })

    recovered_info = recovery.perform_crash_recovery()
    assert len(recovered_info) >= 1
    target = [r for r in recovered_info if r["workflow_id"] == "wf_crash_1"][0]
    assert target["status"] in ["RESTORED_TO_CHECKPOINT", "MARKED_FAILED"]
