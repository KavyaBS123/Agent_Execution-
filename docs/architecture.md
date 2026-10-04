# Proposed Architecture

## System Overview

Client
-> FastAPI API
-> Workflow Orchestrator
-> PostgreSQL for workflow and task state
-> Redis queue for dispatch
-> Worker pool
-> Task executor
-> LLM / tools / MCP
-> Event bus
-> WebSocket gateway
-> Frontend

The platform is split into clear layers so orchestration, execution, persistence, and UI streaming stay independent.

## Directory Structure

```text
agent-os/
  backend/
    src/agent_platform/
      api/
      core/
      db/
      domain/
      models/
      schemas/
      services/
      main.py
    migrations/
    tests/
    pyproject.toml
  frontend/
    src/
    package.json
  docs/
    architecture.md
  docker-compose.yml
  .env.example
  README.md
```

## Database Schema

Core tables:

- `users`
- `workflows`
- `tasks`
- `task_dependencies`
- `events`
- `task_attempts`
- `workers`
- `tool_executions`
- `llm_executions`

Notes:

- Use relational rows for state, not a single JSON document.
- Use JSONB only for structured payload fields that are naturally flexible.
- Index workflow/task status and foreign keys for fast orchestration queries.

## Workflow Execution Lifecycle

1. User submits a workflow request.
2. API persists workflow and task graph.
3. Orchestrator identifies root tasks with no unmet dependencies.
4. Root tasks transition to `QUEUED` and are published to Redis.
5. Workers claim tasks, transition them to `RUNNING`, and record attempts.
6. Task executor runs an agent, Python function, or tool chain.
7. Completion persists output and emits `TASK_COMPLETED`.
8. Orchestrator unlocks downstream tasks when all dependencies are satisfied.
9. Failure triggers retry with exponential backoff until retry budget is exhausted.
10. Exhausted tasks move to `DEAD_LETTER` and workflows can fail or continue based on policy.

## Task State Machine

Allowed states:

- `PENDING`
- `QUEUED`
- `RUNNING`
- `COMPLETED`
- `FAILED`
- `RETRYING`
- `CANCELLED`
- `BLOCKED`
- `DEAD_LETTER`

Guiding rules:

- `PENDING -> QUEUED | BLOCKED | CANCELLED`
- `BLOCKED -> QUEUED | CANCELLED`
- `QUEUED -> RUNNING | CANCELLED`
- `RUNNING -> COMPLETED | FAILED | RETRYING | CANCELLED`
- `RETRYING -> QUEUED | CANCELLED | DEAD_LETTER`
- `FAILED -> RETRYING | DEAD_LETTER`
- terminal states cannot move forward

## Redis Queue Design

Planned queues:

- `workflow:ready` for newly unblocked tasks
- `workflow:retry` for delayed retry requeueing
- `workflow:dead-letter` for permanently failed tasks
- `workflow:events` for event fanout to the WebSocket gateway

Queue items should contain task identifiers, idempotency keys, and execution metadata, not the entire task payload.

## Worker Architecture

Workers should:

- claim work atomically
- re-check persistent task state before running
- enforce timeouts and idempotency
- persist attempts and result metadata
- publish completion/failure events
- release downstream tasks after transactionally recording success

Workers remain stateless; PostgreSQL is the source of truth.

## Implementation Phases

1. Repository structure, FastAPI, PostgreSQL models, migrations, and basic API.
2. DAG engine, dependency resolution, and state transitions.
3. Redis queue, workers, and asynchronous execution.
4. Retries, backoff, idempotency, timeout, cancellation, dead-letter handling.
5. Event system and WebSocket streaming.
6. LLM abstraction, agents, tools, and MCP compatibility.
7. Observability and structured logging.
8. React dashboard and DAG visualization.
9. Testing, Docker hardening, and documentation.
