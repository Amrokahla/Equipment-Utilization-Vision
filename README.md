# Eaglevision

Eaglevision is an equipment utilization and activity classification system for processing construction-site video streams into machine events, state transitions, analytics, and dashboard views.

The repository includes a **Next.js** app under `app/` (App Router, TypeScript, Tailwind) and placeholder backend service containers. Backend service logic is still to be implemented.

## Documents

- [`docs/00-ARCHTICUTRE.md`](docs/00-ARCHTICUTRE.md) — high-level architecture, communication, and data flow
- [`docs/initial-plan.md`](docs/initial-plan.md) — initial architecture and system flow
- [`docs/plans/01-codebase-building.md`](docs/plans/01-codebase-building.md) — codebase layout and tech stack setup plan

## Requirements

- Docker
- Docker Compose
- Python 3.10 (optional local editor tooling / virtualenv)
- Node.js 20+ (for local `npm run dev` in `app/`; Docker builds the app image without a host install)

## Local setup

### 1. Copy environment file

```bash
cp .env.example .env
```

### 2. Build all containers

```bash
docker compose build
```

### 3. Start the stack

```bash
docker compose up
```

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
