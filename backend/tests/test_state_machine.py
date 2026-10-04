from agent_platform.domain.enums import TaskStatus, WorkflowStatus
from agent_platform.domain.state_machine import InvalidStateTransition, transition_task, transition_workflow


def test_task_transition_allows_pending_to_queued() -> None:
    assert transition_task(TaskStatus.PENDING, TaskStatus.QUEUED) == TaskStatus.QUEUED


def test_task_transition_rejects_invalid_jump() -> None:
    try:
        transition_task(TaskStatus.COMPLETED, TaskStatus.RUNNING)
    except InvalidStateTransition:
        return
    raise AssertionError("Expected InvalidStateTransition")


def test_workflow_transition_allows_running_to_completed() -> None:
    assert transition_workflow(WorkflowStatus.RUNNING, WorkflowStatus.COMPLETED) == WorkflowStatus.COMPLETED
