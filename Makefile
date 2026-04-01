# Eaglevision — Docker backend + Next.js app
# Run `make help` for targets.

SHELL := /bin/bash
COMPOSE := docker compose

# Infra + Python services (no Next.js container — use `make app` for local dev, or `make dev-app` for all-in-Docker)
BACKEND_SERVICES := kafka postgres kafka-init video-ingestion cv-processing state-manager analytics api-gateway

.PHONY: help env dev dev-app app dev-app-local stop dev-stop app-stop ps logs build rebuild rebuild-dev rebuild-app install-app clean

.DEFAULT_GOAL := help

help:
	@echo "Eaglevision Makefile"
	@echo ""
	@echo "  make env            Create .env from .env.example if missing"
	@echo "  make dev            Start Kafka, Postgres, kafka-init, and backend service containers (no app container)"
	@echo "  make app            Run Next.js dev server locally (cd app && npm run dev)"
	@echo "  make dev-app        Start full stack in Docker (includes Next.js container on port APP_PORT)"
	@echo "  make dev-app-local  Same as: make dev, then open a second terminal: make app"
	@echo ""
	@echo "  make stop           docker compose down (stop and remove project containers)"
	@echo "  make dev-stop       Stop only backend/infra containers (not the Next.js Docker app)"
	@echo "  make app-stop       Stop only the eaglevision-app container (when started with dev-app)"
	@echo ""
	@echo "  make ps             docker compose ps -a"
	@echo "  make logs           Follow logs for all services"
	@echo "  make logs-SERVICE   e.g. make logs-kafka"
	@echo ""
	@echo "  make build          Build all images"
	@echo "  make build-SERVICE  e.g. make build-api-gateway, make build-app"
	@echo "  make rebuild-dev    Rebuild + recreate Python backend services (picks up Dockerfile/code changes)"
	@echo "  make rebuild-app    Rebuild + recreate only the Next.js Docker image"
	@echo "  make rebuild        rebuild-dev + rebuild-app"
	@echo ""
	@echo "  make install-app    npm install in app/ (for local make app)"
	@echo "  make clean          docker compose down -v (removes volumes — destructive)"
	@echo ""

env:
	@test -f .env || (cp .env.example .env && echo "Created .env from .env.example")

dev: env
	$(COMPOSE) up -d $(BACKEND_SERVICES)

# Full stack with Next.js running inside Docker (profile "app")
dev-app: env
	$(COMPOSE) --profile app up -d

# Hint: typical local workflow is `make dev` in one terminal, `make app` in another
dev-app-local:
	@echo "Run in terminal 1: make dev"
	@echo "Run in terminal 2: make app"

app: install-app
	cd app && npm run dev

install-app:
	@test -d app/node_modules || (cd app && npm install)

stop:
	$(COMPOSE) --profile app down

dev-stop:
	$(COMPOSE) stop $(BACKEND_SERVICES)

app-stop:
	-$(COMPOSE) --profile app stop app

ps:
	$(COMPOSE) ps -a

logs:
	$(COMPOSE) logs -f

logs-%:
	$(COMPOSE) logs -f $*

build:
	$(COMPOSE) build

build-%:
	$(COMPOSE) build $*

rebuild-dev:
	$(COMPOSE) build video-ingestion cv-processing state-manager analytics api-gateway
	$(COMPOSE) up -d --force-recreate video-ingestion cv-processing state-manager analytics api-gateway

rebuild-app:
	$(COMPOSE) build app
	$(COMPOSE) --profile app up -d --force-recreate app

rebuild: rebuild-dev rebuild-app

clean:
	$(COMPOSE) --profile app down -v
