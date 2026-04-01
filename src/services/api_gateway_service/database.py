from __future__ import annotations

import logging
from typing import Any

import asyncpg

logger = logging.getLogger(__name__)


class Database:
    """Thin async wrapper around an asyncpg connection pool."""

    def __init__(self) -> None:
        self._pool: asyncpg.Pool | None = None

    async def connect(self, dsn: str, *, min_size: int = 2, max_size: int = 10) -> None:
        self._pool = await asyncpg.create_pool(dsn, min_size=min_size, max_size=max_size)
        logger.info("PostgreSQL connection pool created")

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("PostgreSQL connection pool closed")

    @property
    def pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError("Database is not connected")
        return self._pool

    # ----- convenience helpers -----

    async def fetch(self, query: str, *args: Any) -> list[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(r) for r in rows]

    async def fetchrow(self, query: str, *args: Any) -> dict | None:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None

    async def fetchval(self, query: str, *args: Any) -> Any:
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def execute(self, query: str, *args: Any) -> str:
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def is_healthy(self) -> bool:
        try:
            await self.fetchval("SELECT 1")
            return True
        except Exception:
            return False
