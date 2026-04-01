from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Database
from .kafka_consumers import KafkaConsumerManager
from .websocket_manager import WebSocketManager
from .routes import health, machines, dashboard, ws

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("gateway")

# ---------------------------------------------------------------------------
# Database schema (idempotent — safe to run on every startup)
# ---------------------------------------------------------------------------

_SCHEMA_STATEMENTS: list[str] = [
    """
    CREATE TABLE IF NOT EXISTS machines (
        machine_id       TEXT PRIMARY KEY,
        machine_type     TEXT,
        first_seen       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        last_seen        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        current_state    TEXT DEFAULT 'UNKNOWN',
        current_activity TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS machine_utilization (
        id              SERIAL PRIMARY KEY,
        machine_id      TEXT NOT NULL REFERENCES machines(machine_id),
        timestamp       TIMESTAMPTZ NOT NULL,
        active_time_s   DOUBLE PRECISION NOT NULL DEFAULT 0,
        idle_time_s     DOUBLE PRECISION NOT NULL DEFAULT 0,
        utilization_pct DOUBLE PRECISION NOT NULL DEFAULT 0,
        activity_breakdown JSONB,
        created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS machine_activities (
        id         SERIAL PRIMARY KEY,
        machine_id TEXT NOT NULL REFERENCES machines(machine_id),
        timestamp  TIMESTAMPTZ NOT NULL,
        state      TEXT NOT NULL,
        activity   TEXT,
        duration_s DOUBLE PRECISION,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_utilization_machine_ts
        ON machine_utilization (machine_id, timestamp DESC)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_activities_machine_ts
        ON machine_activities (machine_id, timestamp DESC)
    """,
]


async def _ensure_schema(db: Database) -> None:
    """Run CREATE IF NOT EXISTS for all required tables."""
    for stmt in _SCHEMA_STATEMENTS:
        await db.execute(stmt)
    logger.info("Database schema verified")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Database = app.state.db
    kafka: KafkaConsumerManager = app.state.kafka_consumer

    await db.connect(settings.database_url)
    await _ensure_schema(db)
    kafka.start(asyncio.get_running_loop())
    logger.info("API Gateway ready (port %s)", settings.gateway_port)

    yield

    kafka.stop()
    await db.disconnect()
    logger.info("API Gateway stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Eaglevision API Gateway",
        version="0.1.0",
        lifespan=lifespan,
    )

    # shared state
    app.state.db = Database()
    app.state.ws_manager = WebSocketManager()
    app.state.kafka_consumer = KafkaConsumerManager(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        ws_manager=app.state.ws_manager,
    )

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # routers
    app.include_router(health.router)
    app.include_router(machines.router)
    app.include_router(dashboard.router)
    app.include_router(ws.router)

    return app


app = create_app()
