from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ..deps import get_machine_repo, get_analytics_repo
from ..models import MachineResponse, UtilizationResponse, ActivityRecord
from ..repositories.machine_repo import MachineRepository
from ..repositories.analytics_repo import AnalyticsRepository

router = APIRouter(prefix="/api/machines", tags=["machines"])


@router.get("", response_model=list[MachineResponse])
async def list_machines(
    repo: MachineRepository = Depends(get_machine_repo),
) -> list[MachineResponse]:
    rows = await repo.list_machines()
    return [MachineResponse(**r) for r in rows]


@router.get("/{machine_id}", response_model=MachineResponse)
async def get_machine(
    machine_id: str,
    repo: MachineRepository = Depends(get_machine_repo),
) -> MachineResponse:
    row = await repo.get_machine(machine_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return MachineResponse(**row)


@router.get("/{machine_id}/utilization", response_model=UtilizationResponse)
async def get_utilization(
    machine_id: str,
    repo: AnalyticsRepository = Depends(get_analytics_repo),
) -> UtilizationResponse:
    row = await repo.get_latest_utilization(machine_id)
    if row is None:
        raise HTTPException(
            status_code=404, detail="No utilization data for this machine"
        )
    return UtilizationResponse(**row)


@router.get("/{machine_id}/activities", response_model=list[ActivityRecord])
async def get_activities(
    machine_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    repo: AnalyticsRepository = Depends(get_analytics_repo),
) -> list[ActivityRecord]:
    rows = await repo.get_activities(machine_id, limit=limit, offset=offset)
    return [ActivityRecord(**r) for r in rows]
