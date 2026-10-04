from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agent_platform.api.dependencies import get_session
from agent_platform.schemas.workflow import TaskRead, WorkflowCancelResponse, WorkflowCreate, WorkflowRead
from agent_platform.services.workflow_service import WorkflowService

router = APIRouter(prefix="/workflows", tags=["workflows"])
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


def _to_workflow_read(workflow) -> WorkflowRead:
    return WorkflowRead.model_validate(
        {
            "id": workflow.id,
            "user_request": workflow.user_request,
            "status": workflow.status,
            "metadata": workflow.workflow_metadata,
            "created_at": workflow.created_at,
            "updated_at": workflow.updated_at,
            "started_at": workflow.started_at,
            "completed_at": workflow.completed_at,
            "error": workflow.error,
            "tasks": [_to_task_read(task) for task in workflow.tasks],
        }
    )


@router.post("", response_model=WorkflowRead, status_code=201)
async def create_workflow(payload: WorkflowCreate, session: AsyncSession = Depends(get_session)) -> WorkflowRead:
    workflow = await service.create_workflow(session, payload)
    return _to_workflow_read(workflow)


@router.get("/{workflow_id}", response_model=WorkflowRead)
async def get_workflow(workflow_id: UUID, session: AsyncSession = Depends(get_session)) -> WorkflowRead:
    workflow = await service.get_workflow(session, workflow_id)
    return _to_workflow_read(workflow)


@router.post("/{workflow_id}/cancel", response_model=WorkflowCancelResponse)
async def cancel_workflow(workflow_id: UUID, session: AsyncSession = Depends(get_session)) -> WorkflowCancelResponse:
    workflow = await service.cancel_workflow(session, workflow_id)
    return WorkflowCancelResponse(workflow_id=workflow.id, status=workflow.status)


@router.get("/{workflow_id}/tasks", response_model=list[TaskRead])
async def list_workflow_tasks(workflow_id: UUID, session: AsyncSession = Depends(get_session)) -> list[TaskRead]:
    tasks = await service.list_workflow_tasks(session, workflow_id)
    return [_to_task_read(task) for task in tasks]
