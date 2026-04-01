from __future__ import annotations

from ..database import Database


class AnalyticsRepository:
    """Read-only queries for utilization and activity data."""

    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_latest_utilization(self, machine_id: str) -> dict | None:
        return await self._db.fetchrow("""
            SELECT machine_id, active_time_s, idle_time_s,
                   utilization_pct, activity_breakdown, timestamp
            FROM machine_utilization
            WHERE machine_id = $1
            ORDER BY timestamp DESC
            LIMIT 1
        """, machine_id)

    async def get_activities(
        self, machine_id: str, *, limit: int = 50, offset: int = 0
    ) -> list[dict]:
        return await self._db.fetch("""
            SELECT id, machine_id, timestamp, state, activity, duration_s
            FROM machine_activities
            WHERE machine_id = $1
            ORDER BY timestamp DESC
            LIMIT $2 OFFSET $3
        """, machine_id, limit, offset)

    async def get_dashboard_summary(self) -> list[dict]:
        return await self._db.fetch("""
            SELECT
                m.machine_id,
                m.machine_type,
                m.current_state,
                m.current_activity,
                COALESCE(u.active_time_s, 0)   AS active_time_s,
                COALESCE(u.idle_time_s, 0)     AS idle_time_s,
                COALESCE(u.utilization_pct, 0) AS utilization_pct
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
