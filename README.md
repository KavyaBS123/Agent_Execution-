# AI Agent Execution Platform

Production-grade backend platform for DAG-based AI agent execution with persistence, retries, queueing, tool execution, and real-time workflow visibility.

## Current Phase

Phase 1 is implemented:

- Repository structure
- FastAPI backend skeleton
- PostgreSQL-oriented SQLAlchemy models
- Alembic migrations
- Workflow and task state machine
- Basic workflow API
- Minimal frontend shell

Later phases will add the Redis queue, workers, event stream, WebSockets, LLM abstraction, tools, observability, and richer dashboarding.

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
alembic upgrade head
uvicorn agent_platform.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Compose

```bash
docker compose up --build
```

## Implemented Endpoints

- `GET /health`
- `POST /workflows`
- `GET /workflows/{workflow_id}`
- `POST /workflows/{workflow_id}/cancel`
- `GET /workflows/{workflow_id}/tasks`
- `GET /tasks/{task_id}`
- `GET /workers`
- `GET /queues`
