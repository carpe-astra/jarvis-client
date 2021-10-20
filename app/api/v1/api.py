from fastapi import APIRouter

from app.api.v1.endpoints import modules, tasks

router = APIRouter()

router.include_router(router=modules.router, prefix="/modules", tags=["Modules"])
router.include_router(router=tasks.router, prefix="/tasks", tags=["Tasks"])
