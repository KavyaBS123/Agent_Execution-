from fastapi import FastAPI

from agent_platform.api.routes.health import router as health_router
from agent_platform.api.routes.ops import router as ops_router
from agent_platform.api.routes.tasks import router as tasks_router
from agent_platform.api.routes.workflows import router as workflows_router


app = FastAPI(title="AI Agent Execution Platform", version="0.1.0")

app.include_router(health_router)
app.include_router(workflows_router)
app.include_router(tasks_router)
app.include_router(ops_router)
