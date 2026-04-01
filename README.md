# Eaglevision

Eaglevision is an equipment utilization and activity classification system for processing construction-site video streams into machine events, state transitions, analytics, and dashboard views.

The repository includes a **Next.js** app under `app/` (App Router, TypeScript, Tailwind) and placeholder backend service containers. Backend service logic is still to be implemented.

## Documents

- [`docs/00-PROJECT-OVERVIEW.md`](docs/00-PROJECT-OVERVIEW.md) — project overview, problem statement, and goals (from the technical assessment)
- [`docs/01-ARCHTICUTRE.md`](docs/01-ARCHTICUTRE.md) — high-level architecture, communication, and data flow
- [`docs/02-KAFKA.md`](docs/02-KAFKA.md) — Kafka topics, flows, and how services (and the API Gateway) use the broker

Local-only planning files may live under `docs/plans/` (ignored by git).

## Requirements

- Docker
- Docker Compose
- Python 3.10 (optional local editor tooling / virtualenv)
- Node.js 20+ (for local `npm run dev` in `app/`; Docker builds the app image without a host install)

## Makefile (shortcuts)

| Target | What it does |
| ------ | -------------- |
| `make help` | List all targets |
| `make dev` | Start Kafka, Postgres, topic init, and Python backend containers (no Next.js container) |
| `make app` | Run Next.js locally (`npm run dev` in `app/`) — use with `make dev` in another terminal for full local dev |
| `make dev-app` | Start everything in Docker, including the Next.js container (`docker compose --profile app`) |
| `make stop` / `make dev-stop` / `make app-stop` | Stop all / backend only / Next container only |
| `make build` / `make build-<service>` | Build all or one image (e.g. `make build-api-gateway`) |
| `make rebuild-dev` | Rebuild and recreate Python backend services after Dockerfile or code changes |
| `make rebuild-app` | Rebuild and recreate the Next.js Docker image |

Run `make help` for the full list.

## Local setup

### Option A — Makefile

```bash
make env          # optional: copy .env.example → .env
make dev          # backend + infra
make app          # in a second terminal: Next.js dev server
```

Or all in Docker (Next.js in a container):

```bash
make dev-app
```

### Option B — Docker Compose only

1. Copy environment file: `cp .env.example .env`
2. Build: `docker compose build`
3. Backend only: `docker compose up -d` (Next.js container is behind profile `app`; it is **not** started by default)
4. Include Next.js in Docker: `docker compose --profile app up -d`

The **app** image runs a real Next.js production build. Python services are still placeholders (`sleep`-style) until implemented.

## Default ports

| Component | Host port |
| --------- | --------- |
| Kafka | `9092` |
| PostgreSQL | `5432` |
| Next.js (app) | `3000` |

## Notes

- Kafka runs as **`apache/kafka:3.8.1`** (KRaft). Other services use `kafka:29092` on the Compose network; the host maps broker port `9092` by default.
- Kafka topics are bootstrapped from `src/dev/kafka/topics.txt` by the one-shot `kafka-init` service.
- PostgreSQL initialization files can be placed in `docker/postgres/init/`.
- Shared Python package structure lives under `src/`.
