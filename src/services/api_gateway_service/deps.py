"""FastAPI dependency factories for the gateway."""

from __future__ import annotations

from fastapi import Request

from .database import Database
from .repositories.machine_repo import MachineRepository
from .repositories.analytics_repo import AnalyticsRepository
from .websocket_manager import WebSocketManager


def get_db(request: Request) -> Database:
    return request.app.state.db


def get_ws_manager(request: Request) -> WebSocketManager:
    return request.app.state.ws_manager


def get_machine_repo(request: Request) -> MachineRepository:
    return MachineRepository(request.app.state.db)


def get_analytics_repo(request: Request) -> AnalyticsRepository:
    return AnalyticsRepository(request.app.state.db)
