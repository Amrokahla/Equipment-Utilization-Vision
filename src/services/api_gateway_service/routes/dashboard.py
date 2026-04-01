from __future__ import annotations

from fastapi import APIRouter, Depends

from ..deps import get_analytics_repo
from ..models import DashboardResponse, DashboardMachine
from ..repositories.analytics_repo import AnalyticsRepository

router = APIRouter(tags=["dashboard"])


@router.get("/api/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    repo: AnalyticsRepository = Depends(get_analytics_repo),
) -> DashboardResponse:
    rows = await repo.get_dashboard_summary()
    machines = [DashboardMachine(**r) for r in rows]
    return DashboardResponse(machine_count=len(machines), machines=machines)
