from __future__ import annotations

from agent_platform.domain.enums import WorkflowStatus


async def test_health(client) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_and_fetch_workflow(client) -> None:
    payload = {
        "user_request": "Research the latest multimodal RAG papers",
        "tasks": [
            {
                "task_key": "research_a",
                "task_type": "research",
                "input": {"query": "paper A"},
                "dependencies": [],
                "idempotency_key": "workflow-1-research-a",
            },
            {
                "task_key": "analysis",
                "task_type": "analysis",
                "input": {"query": "compare results"},
                "dependencies": ["research_a"],
                "idempotency_key": "workflow-1-analysis",
            },
        ],
        "metadata": {"source": "test"},
    }

    response = await client.post("/workflows", json=payload)
    assert response.status_code == 201
    workflow = response.json()
    assert workflow["status"] == WorkflowStatus.PENDING.value
    assert len(workflow["tasks"]) == 2
    assert workflow["tasks"][1]["dependencies"] == [workflow["tasks"][0]["id"]]

    workflow_id = workflow["id"]
    details = await client.get(f"/workflows/{workflow_id}")
    assert details.status_code == 200
    assert details.json()["user_request"] == payload["user_request"]

    tasks = await client.get(f"/workflows/{workflow_id}/tasks")
    assert tasks.status_code == 200
    assert len(tasks.json()) == 2


async def test_cancel_workflow(client) -> None:
    payload = {
        "user_request": "Do something cancelable",
        "tasks": [
            {
                "task_key": "one",
                "task_type": "research",
                "input": {},
                "dependencies": [],
                "idempotency_key": "workflow-2-one",
            }
        ],
    }
    workflow = (await client.post("/workflows", json=payload)).json()

    cancel = await client.post(f"/workflows/{workflow['id']}/cancel")
    assert cancel.status_code == 200
    assert cancel.json()["status"] == WorkflowStatus.CANCELLED.value
