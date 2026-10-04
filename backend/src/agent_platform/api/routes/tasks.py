from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agent_platform.api.dependencies import get_session
from agent_platform.schemas.workflow import TaskRead
from agent_platform.services.workflow_service import WorkflowService

router = APIRouter(prefix="/tasks", tags=["tasks"])
service = WorkflowService()


def _to_task_read(task) -> TaskRead:
    return TaskRead.model_validate(
        {
            "id": task.id,
            "workflow_id": task.workflow_id,
            "task_key": task.task_key,
            "task_type": task.task_type,
            "status": task.status,
            "input": task.input,
            "output": task.output,
            "retry_count": task.retry_count,
            "max_retries": task.max_retries,
            "timeout_seconds": task.timeout_seconds,
            "priority": task.priority,
            "idempotency_key": task.idempotency_key,
            "started_at": task.started_at,
            "completed_at": task.completed_at,
            "error": task.error,
            "dependencies": [dependency.depends_on_task_id for dependency in task.outgoing_dependencies],
        }
    )


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: UUID, session: AsyncSession = Depends(get_session)) -> TaskRead:
    task = await service.get_task(session, task_id)
    return _to_task_read(task)
