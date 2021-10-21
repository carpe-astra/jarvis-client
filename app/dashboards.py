"""API endpoints for dashboards"""

from fastapi import APIRouter, HTTPException, Request, status
from starlette.responses import RedirectResponse

from app.config import settings
from app.core._logging import logger

router = APIRouter()

# Endpoints
# ================================================================
@router.get("/schedule")
async def schedule_dashboard(request: Request):
    host = request.client.host
    port = settings.dashboard_port
    return RedirectResponse(url=f"http://{host}:{port}")
