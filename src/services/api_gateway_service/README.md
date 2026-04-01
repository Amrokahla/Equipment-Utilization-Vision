# `api_gateway_service`

The API Gateway is the **browser-facing entrypoint** for Eaglevision and a **first-class Kafka participant**. It bridges the event backbone to the frontend via HTTP REST and WebSocket.

## Responsibilities

- **Consume** Kafka topics (`machine_events`, `machine_state`, `analytics_updates`) and push live updates to connected WebSocket clients
- **Serve REST** endpoints for machine lists, utilization stats, activity history, and dashboard snapshots (backed by PostgreSQL)
- **Expose WebSocket** at `/ws/live` with a typed envelope format (`{type, timestamp, payload}`)
- **CORS** configured via `CORS_ORIGINS` env var
- **Schema bootstrap** — creates database tables on startup if they don't exist

## Endpoints

| Path | Method | Purpose |
| --- | --- | --- |
| `/api/health` | GET | Liveness check (Kafka, Postgres, WS client count) |
| `/api/machines` | GET | List all tracked machines |
| `/api/machines/{id}` | GET | Single machine details |
| `/api/machines/{id}/utilization` | GET | Latest utilization stats |
| `/api/machines/{id}/activities` | GET | Activity history (paginated) |
| `/api/dashboard` | GET | Dashboard snapshot for all machines |
| `/ws/live` | WS | Live event stream (snapshot on connect, then incremental updates) |

## Environment variables

| Variable | Default |
| --- | --- |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:29092` |
| `DATABASE_URL` | `postgresql://eaglevision:eaglevision@postgres:5432/eaglevision` |
| `GATEWAY_PORT` | `8000` |
| `CORS_ORIGINS` | `http://localhost:3000` |

## Running

The gateway runs inside Docker Compose (see root `docker-compose.yml`). Build context is `./src` so the shared `common/` library is available.

```bash
make dev          # starts all backend services including the gateway
# Gateway available at http://localhost:8000
```
