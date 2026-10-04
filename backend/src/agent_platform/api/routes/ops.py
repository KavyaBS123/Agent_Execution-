from fastapi import APIRouter

router = APIRouter(tags=["ops"])


@router.get("/workers")
async def list_workers() -> dict[str, list[dict]]:
    return {"workers": []}


@router.get("/queues")
async def list_queues() -> dict[str, list[dict]]:
    return {"queues": []}
