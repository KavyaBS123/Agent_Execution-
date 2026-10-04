from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from agent_platform.domain.enums import TaskStatus, WorkflowStatus
from agent_platform.domain.state_machine import InvalidStateTransition, transition_workflow
from agent_platform.models.workflow import Task, TaskDependency, Workflow
from agent_platform.schemas.workflow import TaskCreate, WorkflowCreate


class WorkflowService:
    async def create_workflow(self, session: AsyncSession, payload: WorkflowCreate) -> Workflow:
        workflow = Workflow(user_request=payload.user_request, workflow_metadata=payload.metadata, status=WorkflowStatus.PENDING)
        task_lookup: dict[str, Task] = {}

        for task_input in payload.tasks:
            task = Task(
                workflow=workflow,
                task_key=task_input.task_key,
                task_type=task_input.task_type,
                input=task_input.input,
                status=TaskStatus.PENDING,
                max_retries=task_input.max_retries,
                timeout_seconds=task_input.timeout_seconds,
                priority=task_input.priority,
                idempotency_key=task_input.idempotency_key,
            )
            task_lookup[task.task_key] = task

        session.add(workflow)
        await session.flush()

        dependencies: list[TaskDependency] = []

        for task_input in payload.tasks:
            for dependency_key in task_input.dependencies:
                dependency_task = task_lookup.get(dependency_key)
                if dependency_task is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Unknown dependency '{dependency_key}' for task '{task_input.task_key}'",
                    )
                dependencies.append(
                    TaskDependency(
                        workflow_id=workflow.id,
                        task_id=task_lookup[task_input.task_key].id,
                        depends_on_task_id=dependency_task.id,
                    )
                )

        session.add_all(dependencies)
        await session.commit()
        return await self.get_workflow(session, workflow.id)

    async def get_workflow(self, session: AsyncSession, workflow_id: UUID) -> Workflow:
        workflow = await session.scalar(
            select(Workflow)
            .where(Workflow.id == workflow_id)
            .options(selectinload(Workflow.tasks).selectinload(Task.outgoing_dependencies))
        )
        if workflow is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
        return workflow

    async def cancel_workflow(self, session: AsyncSession, workflow_id: UUID) -> Workflow:
        workflow = await self.get_workflow(session, workflow_id)
        try:
            workflow.status = transition_workflow(workflow.status, WorkflowStatus.CANCELLED)
        except InvalidStateTransition as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

        workflow.completed_at = datetime.now(timezone.utc)
        for task in workflow.tasks:
            if task.status not in {TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.DEAD_LETTER}:
                task.status = TaskStatus.CANCELLED
        await session.commit()
        return workflow

    async def list_workflow_tasks(self, session: AsyncSession, workflow_id: UUID) -> list[Task]:
        workflow = await self.get_workflow(session, workflow_id)
        return list(workflow.tasks)

    async def get_task(self, session: AsyncSession, task_id: UUID) -> Task:
        task = await session.scalar(select(Task).where(Task.id == task_id).options(selectinload(Task.outgoing_dependencies)))
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task
