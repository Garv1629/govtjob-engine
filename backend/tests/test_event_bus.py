import pytest
import asyncio
from app.modules.workflow.event_bus import EventBus
from app.modules.workflow.event_dispatcher import EventDispatcher
from app.modules.workflow.events import (
    JobDiscoveredEvent,
    EligibilityCompletedEvent,
    ApplicationSubmittedEvent
)


@pytest.mark.asyncio
async def test_event_bus_subscribe_and_publish():
    bus = EventBus()
    received_events = []

    async def handle_job_discovered(event):
        received_events.append(event)

    bus.subscribe("JobDiscovered", handle_job_discovered)

    event = JobDiscoveredEvent(
        workflow_id="wf_test_1",
        job_id="job_1",
        source_code="SSC",
        title="SSC CGL 2026",
        url="https://ssc.gov.in"
    )

    await bus.publish(event)

    assert len(received_events) == 1
    assert received_events[0].workflow_id == "wf_test_1"
    assert received_events[0].title == "SSC CGL 2026"


@pytest.mark.asyncio
async def test_event_bus_wildcard_listener():
    bus = EventBus()
    all_events = []

    def wildcard_handler(event):
        all_events.append(event)

    bus.subscribe("*", wildcard_handler)

    e1 = JobDiscoveredEvent(workflow_id="wf_1", job_id="j1", source_code="SSC", title="Job 1", url="http://example.com")
    e2 = EligibilityCompletedEvent(workflow_id="wf_1", user_id="u1", status="ELIGIBLE", overall_score=92.0)

    await bus.publish(e1)
    await bus.publish(e2)

    assert len(all_events) == 2


@pytest.mark.asyncio
async def test_event_dispatcher_metrics():
    bus = EventBus()
    dispatcher = EventDispatcher(bus=bus)

    async def sample_listener(event):
        pass

    dispatcher.register_listener("ApplicationSubmitted", sample_listener)

    event = ApplicationSubmittedEvent(
        workflow_id="wf_2",
        application_id="app_123",
        application_number="SSC-1002"
    )

    await dispatcher.dispatch(event)
    stats = dispatcher.get_stats()

    assert stats["total_dispatched"] == 1
    assert stats["total_failures"] == 0
