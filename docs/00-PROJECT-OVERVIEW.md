# Eaglevision — Project overview

This document is the **numbered `00` entry point** for the Eaglevision repository. It captures the **project context**, **problem being solved**, and **goals**, aligned with the technical assessment that defines the prototype scope.

**Source:** [`Technical Assessment_file-F.pdf`](Technical%20Assessment_file-F.pdf) — *Technical Assessment: Equipment Utilization & Activity Classification Prototype*.

---

## 1. What this project is

Eaglevision is a **scaled-down prototype** that demonstrates:

- **Computer vision** applied to **construction equipment** in video
- A **distributed, microservices-style backend** with **Apache Kafka** as the main communication spine
- **Streaming results** to operators through a **web user interface**

The assessment frames this as a **technical evaluation**: show CV depth, sound architecture, and a runnable system—not a full production product.

---

## 2. Problem statement

Construction sites rely on **heavy equipment** (excavators, dump trucks, and similar assets). Stakeholders need to understand **how that equipment is actually used**, not only whether it appears on camera.

Concrete pain points the prototype addresses:

- **Utilization is ambiguous in video** — a machine may be “present” but **idle**, **moving**, or **working** in different ways.
- **Partial motion is easy to misread** — for example, an **excavator arm** can be **digging** while the **tracks stay still**. Treating the whole frame as one rigid blob leads to wrong **ACTIVE vs INACTIVE** calls.
- **Activity matters for operations** — not just “moving / not moving,” but **what kind of work** is happening (digging, loading, dumping, waiting).
- **Time adds up** — teams need **working time**, **idle time**, and **utilization percentage** over the period the equipment is tracked.
- **Insights must reach users** — analysis results should flow through a **message broker** to a **UI**, not stop inside a single script.

Eaglevision exists to **make utilization and activity visible, measurable, and streamable** in a way that matches this problem.

---

## 3. Goals

### 3.1 Product and technical goals (from the assessment)

| Area | Goal |
| --- | --- |
| **Pipeline** | Build a **real-time**, **microservices-based** pipeline that processes **video clips** of construction equipment. |
| **State** | Track utilization states: **ACTIVE** (working, moving) vs **INACTIVE** (stationary), with correct handling where **only part of the machine** moves. |
| **Activity** | Classify **specific work activities**, including (as specified in the assessment): **Digging**, **Swinging/Loading**, **Dumping**, and **Waiting**. |
| **Metrics** | Compute **working vs idling** time and **utilization percentage** (**Total Active Time / Total Tracked Time**). |
| **Streaming** | Stream outcomes through **Kafka** toward a **simple user interface**. |
| **Persistence** | Land analysis results in a **data sink**: **PostgreSQL** or **TimescaleDB**. |

### 3.2 User-facing goals (what the UI should convey)

The assessment asks for a **simple** front end (examples given: Streamlit, Gradio, or a basic web app). In Eaglevision we use **Next.js**, but the **intent** is the same:

- **Processed video** (or equivalent view) with **bounding boxes** on equipment.
- **Live status** per machine: **ACTIVE / INACTIVE** and **current activity**.
- **Utilization dashboard**: running view of **total working time**, **total idle time**, and **utilization percentage** per detected machine.

### 3.3 Engineering goals (how we build it)

- **Clean, documented Python** for microservices, with explicit dependencies (`requirements.txt` / packaging as the repo evolves).
- **Docker Compose** (or equivalent) so **Kafka**, **services**, and supporting infra **spin up predictably**.
- **README** and **architecture docs** (this `00` doc, [`01-ARCHTICUTRE.md`](01-ARCHTICUTRE.md), [`02-KAFKA.md`](02-KAFKA.md)) so others can run and reason about the system.
- A path to a **technical write-up** and **demo** (video/GIF) as required by the assessment—tracked as deliverables, not necessarily in this file.

---

## 4. Core technical requirements (summary)

### 4.1 Computer vision (Component A)

- **Equipment utilization tracking** — motion analysis to label equipment as **ACTIVE** or **INACTIVE**.
- **Articulated motion** — detect **ACTIVE** when only a **part** of the machine moves (e.g. arm digging, tracks still). Acceptable approaches include **region-based motion**, **keypoint tracking**, or **instance segmentation** (assessment allows these directions).
- **Activity classification** — **Digging**, **Swinging/Loading**, **Dumping**, **Waiting**.
- **Working vs idle time** — overall **utilization percentage** from tracked time.
- **Data path** — stream analysis into **PostgreSQL / TimescaleDB** as well as through **Kafka** toward the UI.

### 4.2 Analytics backend and UI (Component B)

- Backend services support **aggregation**, **persistence**, and **streaming** consistent with the CV outputs.
- UI exposes **video with boxes**, **live machine state and activity**, and **utilization metrics** as described above.

### 4.3 Kafka payload (Component contract)

The assessment specifies that the **CV microservice** should publish **JSON** to Kafka in a shape that supports **state**, **activity**, and **time** analysis (see section **“Expected Kafka Payload Format”** in the PDF). The exact schema should be treated as the **integration contract** between CV and downstream services; implement it explicitly in code and in [`02-KAFKA.md`](02-KAFKA.md) as the project matures.

---

## 5. Submission expectations (from the assessment)

The assessment lists the following **submission** items. They define what “complete” means for the evaluation:

1. **Source code** — clean, documented Python (and other languages as used), with dependency manifests for all microservices.
2. **Architecture and setup** — `docker-compose.yml` (or similar), README with setup and **architecture overview**.
3. **Technical write-up** — design decisions and trade-offs, especially **articulated equipment** (e.g. arm-only motion) and **how activities are classified**.
4. **Demo** — video or GIF showing the solution **updating in real time** as video is processed.

---

## 6. How this document fits the doc set

| Doc | Role |
| --- | --- |
| **`00-PROJECT-OVERVIEW.md` (this file)** | **Why** the project exists, **what problem** it solves, **what goals** and assessment scope apply. |
| [`01-ARCHTICUTRE.md`](01-ARCHTICUTRE.md) | **How** the system is structured: layers, services, communication, data flow. |
| [`02-KAFKA.md`](02-KAFKA.md) | **How Kafka** is used: topics, flows, local broker, gateway bridge. |
| [`initial-plan.md`](initial-plan.md) | Earlier internal architecture notes and stack choices. |
| [`plans/01-codebase-building.md`](plans/01-codebase-building.md) | Repository layout and Docker-first bootstrap plan. |

---

## 7. Summary

- **Problem:** Equipment utilization and activity are hard to infer from video, especially with **partial/articulated motion**; operators need **clear states**, **activities**, **time metrics**, and **live visibility**.
- **Goal:** A **Kafka-backed**, **microservices-oriented** prototype with **CV + persistence + UI**, meeting the **Technical Assessment** scope.
- **Next read:** [`01-ARCHTICUTRE.md`](01-ARCHTICUTRE.md) for system architecture, then [`02-KAFKA.md`](02-KAFKA.md) for streaming details.

**Primary reference:** [`Technical Assessment_file-F.pdf`](Technical%20Assessment_file-F.pdf)
