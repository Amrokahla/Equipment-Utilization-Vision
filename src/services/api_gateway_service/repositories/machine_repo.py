from __future__ import annotations

from ..database import Database


class MachineRepository:
    """Read-only queries against the ``machines`` table."""

    def __init__(self, db: Database) -> None:
        self._db = db

    async def list_machines(self) -> list[dict]:
        return await self._db.fetch("""
            SELECT machine_id, machine_type, first_seen, last_seen,
                   current_state, current_activity
            FROM machines
            ORDER BY last_seen DESC
        """)

    async def get_machine(self, machine_id: str) -> dict | None:
        return await self._db.fetchrow("""
            SELECT machine_id, machine_type, first_seen, last_seen,
                   current_state, current_activity
            FROM machines
            WHERE machine_id = $1
        """, machine_id)
