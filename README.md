# Eaglevision

Eaglevision is an equipment utilization and activity classification system for processing construction-site video streams into machine events, state transitions, analytics, and dashboard views.

This repository currently contains the initial codebase skeleton only. The goal of this stage is to establish the project layout, container structure, and development infrastructure before implementing any service logic.

## Documents

- [`docs/00-ARCHTICUTRE.md`](docs/00-ARCHTICUTRE.md) — high-level architecture, communication, and data flow
- [`docs/initial-plan.md`](docs/initial-plan.md) — initial architecture and system flow
- [`docs/plans/01-codebase-building.md`](docs/plans/01-codebase-building.md) — codebase layout and tech stack setup plan

## Requirements

- Docker
- Docker Compose
- Python 3.10 (optional local editor tooling / virtualenv)
- Node.js (only needed once the Next.js app is scaffolded)

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

At this stage, service and app containers are placeholders so the repository can boot with a complete structure. They will be replaced with real implementations in later milestones.

## Default ports

| Component | Host port |
| --------- | --------- |
| Kafka | `9092` |
| PostgreSQL | `5432` |
| App placeholder | `3000` |

## Notes

- Kafka topics are bootstrapped from `src/dev/kafka/topics.txt`.
- PostgreSQL initialization files can be placed in `docker/postgres/init/`.
- Shared Python package structure lives under `src/`.
