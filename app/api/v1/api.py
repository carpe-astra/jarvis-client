from fastapi import APIRouter

from app.api.v1.endpoints import tasks

router = APIRouter()

router.include_router(router=tasks.router, prefix="/tasks", tags=["Tasks"])
