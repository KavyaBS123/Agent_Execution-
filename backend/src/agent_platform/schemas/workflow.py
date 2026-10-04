from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from agent_platform.domain.enums import TaskStatus, WorkflowStatus


class TaskCreate(BaseModel):
    task_key: str = Field(min_length=1, max_length=120)
    task_type: str = Field(min_length=1, max_length=120)
    input: dict = Field(default_factory=dict)
    dependencies: list[str] = Field(default_factory=list)
    max_retries: int = Field(default=3, ge=0)
    timeout_seconds: int = Field(default=300, ge=1)
    priority: int = Field(default=0)
    idempotency_key: str = Field(min_length=1, max_length=255)


class WorkflowCreate(BaseModel):
    user_request: str = Field(min_length=1)
    tasks: list[TaskCreate]
    metadata: dict = Field(default_factory=dict)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workflow_id: UUID
    task_key: str
    task_type: str
    status: TaskStatus
    input: dict
    output: dict | None
    retry_count: int
    max_retries: int
    timeout_seconds: int
    priority: int
    idempotency_key: str
    started_at: datetime | None
    completed_at: datetime | None
    error: dict | None
    dependencies: list[UUID] = Field(default_factory=list)


class WorkflowRead(BaseModel):
    id: UUID
    user_request: str
    status: WorkflowStatus
    metadata: dict
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    error: dict | None
    tasks: list[TaskRead] = Field(default_factory=list)


class WorkflowCancelResponse(BaseModel):
    workflow_id: UUID
    status: WorkflowStatus
