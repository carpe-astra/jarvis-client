"""The main web application definition"""

from fastapi import FastAPI

from app.api.v1.api import router as v1_router
from app.dashboards import router as dashboard_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(v1_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix="/dashboards")
