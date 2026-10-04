from __future__ import annotations

from agent_platform.domain.enums import TaskStatus, WorkflowStatus


class InvalidStateTransition(ValueError):
    pass


TASK_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.PENDING: {TaskStatus.QUEUED, TaskStatus.BLOCKED, TaskStatus.CANCELLED},
    TaskStatus.BLOCKED: {TaskStatus.QUEUED, TaskStatus.CANCELLED},
    TaskStatus.QUEUED: {TaskStatus.RUNNING, TaskStatus.CANCELLED},
    TaskStatus.RUNNING: {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.RETRYING, TaskStatus.CANCELLED},
    TaskStatus.RETRYING: {TaskStatus.QUEUED, TaskStatus.CANCELLED, TaskStatus.DEAD_LETTER},
    TaskStatus.FAILED: {TaskStatus.RETRYING, TaskStatus.DEAD_LETTER},
    TaskStatus.COMPLETED: set(),
    TaskStatus.CANCELLED: set(),
    TaskStatus.DEAD_LETTER: set(),
}

WORKFLOW_TRANSITIONS: dict[WorkflowStatus, set[WorkflowStatus]] = {
    WorkflowStatus.PENDING: {WorkflowStatus.RUNNING, WorkflowStatus.CANCELLED},
    WorkflowStatus.RUNNING: {WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED},
    WorkflowStatus.COMPLETED: set(),
    WorkflowStatus.FAILED: set(),
    WorkflowStatus.CANCELLED: set(),
}


def transition_task(current: TaskStatus, target: TaskStatus) -> TaskStatus:
    allowed = TASK_TRANSITIONS[current]
    if target not in allowed:
        raise InvalidStateTransition(f"Task cannot transition from {current} to {target}")
    return target


def transition_workflow(current: WorkflowStatus, target: WorkflowStatus) -> WorkflowStatus:
    allowed = WORKFLOW_TRANSITIONS[current]
    if target not in allowed:
        raise InvalidStateTransition(f"Workflow cannot transition from {current} to {target}")
    return target
