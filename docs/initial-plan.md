# Equipment Utilization & Activity Classification System

## Initial Architecture Plan

---

# 1. Overview

This document defines the initial architecture plan for the Equipment Monitoring System. The system processes construction site videos, detects equipment, determines machine activity states, calculates dwell time, and streams analytics through a distributed microservice architecture.

Key system goals:

* Real‑time equipment monitoring
* Accurate idle (dwell) time calculation
* Persistent machine identification
* Scalable event-driven architecture
* Microservice isolation

The architecture follows an event-driven pipeline built around Apache Kafka.

---

# 2. Technology Stack

## Backend

| Component        | Technology               |
| ---------------- | ------------------------ |
| Language         | Python 3.10              |
| Web framework    | FastAPI                  |
| Object detection | YOLOv8                   |
| Object tracking  | DeepSORT                 |
| Computer vision  | OpenCV                   |
| Event streaming  | Apache Kafka             |
| Kafka client     | confluent-kafka-python   |
| Database         | PostgreSQL / TimescaleDB |
| Data validation  | Pydantic                 |
| Serialization    | JSON                     |

## Frontend

| Component          | Technology          |
| ------------------ | ------------------- |
| Framework          | Next.js             |
| Data visualization | Recharts / Chart.js |
| State updates      | WebSockets          |

## Infrastructure

| Component           | Technology                |
| ------------------- | ------------------------- |
| Containers          | Docker                    |
| Local orchestration | Docker Compose            |
| Message broker      | Apache Kafka (KRaft mode) |

---

# 3. Ubuntu Environment Setup

## System Dependencies

```
sudo apt update
sudo apt install -y \
    build-essential \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    curl \
    make
```

## Python Environment

```
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## Core Python Dependencies

```
pip install \
    fastapi \
    uvicorn \
    pydantic \
    opencv-python \
    torch \
    ultralytics \
    numpy \
    confluent-kafka \
    psycopg2-binary
```

## Docker

```
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

---

# 4. High Level Codebase Architecture

```
root
│
├── src
│   ├── common
│   ├── services
│   ├── cmd
│   ├── tools
│   ├── dev
│   ├── docs
│   └── scripts
│
├── app
│   └── (Next.js frontend)
│
├── Makefile
├── README.md
└── features.md
```

---

# 5. Backend Codebase Detailed Structure

## src/common

Shared components used across services.

```
common/
    config/
    logging/
    kafka/
    models/
    database/
    tracking/
    utils/
```

Responsibilities:

* configuration loading
* shared schemas
* kafka producers/consumers
* logging configuration
* database connectors

---

## src/services

Contains independent microservices.

```
services/

    video_ingestion_service/

    cv_processing_service/

    state_manager_service/

    analytics_service/

    api_gateway_service/
```

### video_ingestion_service

Responsibilities:

* read video files
* stream frames
* publish frames to processing service

---

### cv_processing_service

Responsibilities:

* equipment detection
* machine tracking
* activity classification
* motion detection

Pipeline:

```
frame
→ detection
→ tracking
→ activity classification
→ state estimation
→ kafka event
```

---

### state_manager_service

Responsibilities:

* maintain machine state
* compute dwell time
* track active vs idle states

This service maintains persistent machine identity.

---

### analytics_service

Responsibilities:

* aggregate utilization metrics
* compute statistics
* persist to database

---

### api_gateway_service

Responsibilities:

* expose APIs for frontend
* serve analytics queries
* provide machine state

---

# 6. Command Layer

## src/cmd

Command-line entrypoints.

Example:

```
cmd/
    run_cv_service.py
    run_ingestion_service.py
    run_analytics_service.py
```

Each command launches a microservice.

---

# 7. Development Infrastructure

## src/dev

```
dev/
    docker/
    docker-compose.yml
    kafka/
    postgres/
```

This directory contains infrastructure definitions for development.

---

# 8. Tools Directory

## src/tools

Internal development tools.

Examples:

* dataset preparation
* model evaluation
* benchmarking scripts

---

# 9. Scripts Directory

Utility scripts used during development.

Examples:

```
scripts/
    setup_env.sh
    download_models.sh
    run_local_pipeline.sh
```

---

# 10. Data Flow Architecture

```
Video Source

↓

Video Ingestion Service

↓

Kafka Topic: raw_frames

↓

CV Processing Service

↓

Kafka Topic: machine_events

↓

State Manager Service

↓

Kafka Topic: machine_state

↓

Analytics Service

↓

PostgreSQL / TimescaleDB

↓

API Gateway

↓

Next.js Dashboard
```

---

# 11. Kafka Role in the System

Apache Kafka acts as the event streaming backbone.

Primary responsibilities:

* decouple microservices
* provide fault tolerance
* enable asynchronous processing
* support event replay

## Topics

```
raw_frames
machine_events
machine_state
analytics_updates
```

### raw_frames

Produced by:

video_ingestion_service

Consumed by:

cv_processing_service

---

### machine_events

Produced by:

cv_processing_service

Contains:

* machine_id
* bounding_box
* activity
* state
* timestamp

Consumed by:

state_manager_service

---

### machine_state

Produced by:

state_manager_service

Contains:

* machine_id
* active_time
* idle_time
* dwell_time

Consumed by:

analytics_service

---

### analytics_updates

Produced by:

analytics_service

Consumed by:

api_gateway_service

---

# 12. Database Schema (Initial)

```
machines

machine_id
first_seen
last_seen

machine_activity

machine_id
timestamp
activity
state

machine_utilization

machine_id
active_time
idle_time
utilization
```

---

# 13. Development Workflow

```
1 initialize environment
2 start docker infrastructure
3 run ingestion service
4 run cv processing service
5 run state manager
6 run analytics service
7 run frontend
```

---

# 14. Future Extensions

Possible improvements:

* distributed model inference
* GPU acceleration
* multi-camera support
* advanced activity recognition
* long-term analytics

---

# End of Initial Architecture Plan
