"""API response models for the gateway endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    kafka: str
    postgres: str
    websocket_clients: int


class MachineResponse(BaseModel):
    machine_id: str
    machine_type: str | None = None
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    current_state: str | None = None
    current_activity: str | None = None


class UtilizationResponse(BaseModel):
    machine_id: str
    active_time_s: float
    idle_time_s: float
    utilization_pct: float
    activity_breakdown: dict[str, float] | None = None
    timestamp: datetime | None = None


class ActivityRecord(BaseModel):
    id: int
    machine_id: str
    timestamp: datetime
    state: str
    activity: str | None = None
    duration_s: float | None = None


class DashboardMachine(BaseModel):
    machine_id: str
    machine_type: str | None = None
    current_state: str | None = None
    current_activity: str | None = None
    active_time_s: float = 0.0
    idle_time_s: float = 0.0
    utilization_pct: float = 0.0


class DashboardResponse(BaseModel):
    machine_count: int
    machines: list[DashboardMachine]


class WSEnvelope(BaseModel):
    type: str
    timestamp: str
    payload: dict[str, Any]
