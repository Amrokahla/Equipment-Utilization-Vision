-- Eaglevision database bootstrap
-- Mounted into postgres /docker-entrypoint-initdb.d/ and executed on first start.
-- The gateway also runs CREATE IF NOT EXISTS on every startup, so these
-- statements serve as a safety net / single source of truth for the schema.

CREATE TABLE IF NOT EXISTS machines (
    machine_id       TEXT PRIMARY KEY,
    machine_type     TEXT,
    first_seen       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    current_state    TEXT DEFAULT 'UNKNOWN',
    current_activity TEXT
);

CREATE TABLE IF NOT EXISTS machine_utilization (
    id              SERIAL PRIMARY KEY,
    machine_id      TEXT NOT NULL REFERENCES machines(machine_id),
    timestamp       TIMESTAMPTZ NOT NULL,
    active_time_s   DOUBLE PRECISION NOT NULL DEFAULT 0,
    idle_time_s     DOUBLE PRECISION NOT NULL DEFAULT 0,
    utilization_pct DOUBLE PRECISION NOT NULL DEFAULT 0,
    activity_breakdown JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS machine_activities (
    id         SERIAL PRIMARY KEY,
    machine_id TEXT NOT NULL REFERENCES machines(machine_id),
    timestamp  TIMESTAMPTZ NOT NULL,
    state      TEXT NOT NULL,
    activity   TEXT,
    duration_s DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_utilization_machine_ts
    ON machine_utilization (machine_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_activities_machine_ts
    ON machine_activities (machine_id, timestamp DESC);
