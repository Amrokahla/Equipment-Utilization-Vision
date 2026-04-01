from __future__ import annotations

from fastapi import APIRouter, Request

from ..models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/api/health", response_model=HealthResponse)
async def health_check(request: Request) -> HealthResponse:
    db = request.app.state.db
    kafka = request.app.state.kafka_consumer
    ws = request.app.state.ws_manager

    pg_ok = await db.is_healthy()

    return HealthResponse(
        status="ok" if pg_ok and kafka.is_running else "degraded",
        kafka="connected" if kafka.is_running else "disconnected",
        postgres="connected" if pg_ok else "disconnected",
        websocket_clients=ws.client_count,
    )
