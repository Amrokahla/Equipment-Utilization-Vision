from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..models import DashboardMachine

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/live")
async def websocket_live(websocket: WebSocket) -> None:
    ws_manager = websocket.app.state.ws_manager
    db = websocket.app.state.db

    await ws_manager.connect(websocket)

    try:
        snapshot = await _build_snapshot(db)
        await websocket.send_text(json.dumps(snapshot, default=str))
    except Exception:
        logger.exception("Failed to send initial snapshot")

    try:
        while True:
            # keep connection alive; could handle client commands here later
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        ws_manager.disconnect(websocket)


async def _build_snapshot(db) -> dict:  # noqa: ANN001
    """Build a full snapshot of current machine state for new WS clients."""
    rows = await db.fetch("""
        SELECT
            m.machine_id,
            m.machine_type,
            m.current_state,
            m.current_activity,
            COALESCE(u.active_time_s, 0)    AS active_time_s,
            COALESCE(u.idle_time_s, 0)      AS idle_time_s,
            COALESCE(u.utilization_pct, 0)  AS utilization_pct
        FROM machines m
        LEFT JOIN LATERAL (
            SELECT active_time_s, idle_time_s, utilization_pct
            FROM machine_utilization
            WHERE machine_id = m.machine_id
            ORDER BY timestamp DESC
            LIMIT 1
        ) u ON true
        ORDER BY m.last_seen DESC
    """)

    machines = [DashboardMachine(**r).model_dump(mode="json") for r in rows]
    return {
        "type": "snapshot",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {"machine_count": len(machines), "machines": machines},
    }
