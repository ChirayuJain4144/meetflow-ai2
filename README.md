# MeetFlow AI — Turn Meetings into Action

[![CI/CD Pipeline](https://github.com/chira/meetflow-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/chira/meetflow-ai)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/UI-Tailwind%20CSS-38B2AC.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Turn meetings into action."**  
> An enterprise-grade, production-minded meeting-to-execution AI agent that prevents critical decisions from being lost, maintains cross-meeting memory, detects conflicting commitments, and enforces human-in-the-loop task approval.

---

## 📌 Problem Statement: The Meeting-to-Execution Gap

In modern engineering and product teams:
1. **Decisions are Lost in the Fog:** Teams spend hours discussing timelines, architecture, and scope, but agreements vanish into meeting notes or chat histories.
2. **Commitments Contradict Without Warning:** A team agrees on a December 10 launch date in Sprint Planning. In a subsequent ad-hoc sync, someone proposes December 15, and the revision goes untracked, causing launch chaos.
3. **Action Items Lack Clear Ownership & Follow-up:** "Someone should deploy the app" results in nobody doing it.
4. **Lack of Human Oversight:** Many AI meeting summaries blindly post hallucinated tasks to Jira/Trello without review.

---

## 🌟 Key Differentiating Features

### 1. Cross-Meeting Institutional Memory & Conflict Detection (Core Innovation)
MeetFlow AI does **not** treat meetings as isolated islands. Every recorded decision is preserved in a permanent, version-controlled database. When a new meeting is processed:
- Relevant past baseline decisions are retrieved.
- The AI cross-evaluates new decisions against past decisions using category semantics and date parameter matching.
- **Contradictions (e.g. changed launch dates, divergent tech stacks, revised scope) trigger an instant Conflict Review Alert.**
- **Zero Silent Overwrites:** The previous baseline remains active until a human explicitly confirms or rejects the revision.

### 2. Mandatory Human-in-the-Loop Approval Workflow
Before any task is sent to an external integration (like Trello) or marked active:
- Action items are ingested in a **Pending Approval** state.
- Team leads can edit titles, descriptions, owners, deadlines, and priorities.
- Only approved tasks transition to the active execution board.

### 3. Speaker Attribution & Safe Extraction
- Supports transcripts formatted like `Rahul: I will complete the backend by 5 December.`
- Accurately attributes action items to their speaker.
- Parses explicit and relative calendar dates (e.g. "5 December", "next Friday").
- Never invents owners or deadlines if not stated.

### 4. Interactive Dual-View Task Tracker
- **Kanban Board** with drag/status progression: `Pending` ➔ `In Progress` ➔ `Completed` ➔ `Blocked`.
- **List View** with multi-select bulk approvals.
- Built-in tracker with optional **Trello board synchronization**.

### 5. Automated Background Deadline Reminders
- Standalone **APScheduler** background daemon running independently of browser sessions.
- Scans tasks due within 48 hours or overdue tasks, emitting in-app reminders and notifications with deduplication.

### 6. Weekly Execution Digest
- Per-member productivity breakdown (Rahul, Chirayu, Priya).
- Completion rates, pending commitments, overdue tasks, and key decisions.
- One-click **Markdown Export** to copy summaries directly into Slack or email.

---

## 🏗️ Architecture & Technology Stack

```
                              ┌────────────────────────────────────────┐
                              │             Web Browser UI             │
                              │   React 18 + Vite + Tailwind CSS       │
                              └──────────────────┬─────────────────────┘
                                                 │ HTTP / REST
                                                 ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FastAPI Backend (Python 3.11+)                              │
│                                                                                              │
│   ┌────────────────────┐     ┌─────────────────────┐     ┌───────────────────────────────┐   │
│   │    REST Routers    │     │      AI Engine      │     │    Cross-Meeting Memory       │   │
│   │  /meetings         │────▶│  OpenAI GPT-4o-mini │────▶│   Conflict Detection Engine   │   │
│   │  /decisions        │     │  Deterministic NLP  │     │   (Version Chaining & Diffs)  │   │
│   │  /conflicts        │     └─────────────────────┘     └───────────────┬───────────────┘   │
│   │  /tasks            │                                                 │                   │
│   │  /digest           │     ┌─────────────────────┐                     │                   │
│   │  /reminders        │     │ APScheduler Service │                     │                   │
│   └─────────┬──────────┘     │ Deadline Reminders  │                     │                   │
│             │                └──────────┬──────────┘                     │                   │
│             ▼                           ▼                                ▼                   │
│   ┌──────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        SQLAlchemy 2.x Database Abstraction                           │   │
│   │          SQLite (Local Dev)  /  PostgreSQL (Azure / Production Deploy Ready)          │   │
│   └──────────────────────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
                              ┌────────────────────────────────────────┐
                              │         External Integrations          │
                              │        Trello API / Webhooks           │
                              └────────────────────────────────────────┘
```

### Technology Highlights
- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons, Date-fns, Axios.
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.x, Pydantic v2, APScheduler, Requests, Httpx.
- **Database:** SQLite (local zero-config) with fully compatible PostgreSQL schema for production.
- **AI Engine:** Dual-mode: OpenAI API (`gpt-4o-mini`) + high-fidelity offline deterministic parser for 100% offline reliability.
- **DevOps:** Docker, Docker Compose, GitHub Actions CI/CD.

---

## 🗄️ Database Schema & Entity Relationships

| Model | Description |
| :--- | :--- |
| **Meeting** | Stores meeting title, date, transcript, executive summary, discussion points, and unresolved questions. |
| **Participant** | Team members identified in the transcript and linked to the meeting. |
| **Decision** | Persistent institutional commitments, categories (`launch_date`, `architecture`, `budget`, `scope`), confidence scores, and statuses (`active`, `superseded`, `in_review`). |
| **DecisionVersion** | Immutable historical version snapshots tracking previous texts, change reasons, and audit dates. |
| **Task** | Action items with title, description, owner, deadline, priority, status (`pending`, `in_progress`, `completed`, `blocked`), and approval status (`pending_approval`, `approved`, `published`). |
| **Conflict** | Discrepancies detected between new meetings and existing baseline decisions, holding the diff, AI explanation, and resolution state. |
| **Reminder** | Generated alerts for upcoming or overdue deadlines. |
| **Notification** | Real-time system activity alerts for users. |

---

## 🚀 Quickstart: Run Locally on Windows 11

### Prerequisites
- Python 3.10+ (tested on Python 3.11 & 3.13)
- Node.js 18+ (tested on Node v20 & v24)
- Git

### 1. Clone & Setup Repository
```powershell
git clone https://github.com/chira/meetflow-ai.git
cd meetflow-ai
```

### 2. Backend Setup
```powershell
# Create and activate virtual environment
python -m venv backend/venv
.\backend\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Run backend (starts on http://localhost:8000)
python backend/run.py
```
> Fast API interactive OpenAPI documentation will be live at: **http://localhost:8000/docs**

### 3. Frontend Setup (in a separate terminal)
```powershell
cd frontend
npm install
npm run dev
```
> Open your browser at: **http://localhost:5173**

---

## 🐳 Run with Docker & Docker Compose

MeetFlow AI is fully containerized with a production multi-stage build.

```bash
# Build and run containers
docker compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs

---

## 🎯 Sample Demo Scenario Walkthrough (Jury Evaluation)

A dedicated one-click demo loader is built into the UI (**"Run Judge Demo Scenario"** in the sidebar or banner). You can also run the seed script from the CLI:

```powershell
python seed_demo.py
```

### The Demonstration Flow:

#### Step 1: Ingest Meeting 1 (Launch Alignment)
```text
Rahul: I will complete the backend by 5 December.
Chirayu: I will deploy the application by 8 December.
Priya: I will prepare the presentation by 9 December.
Rahul: We agreed to launch the project on 10 December.
Chirayu: Yes, the launch date is 10 December.
```
- **Result:**
  - Tasks assigned to Rahul, Chirayu, and Priya with exact extracted deadlines.
  - Baseline decision established: *"The project launch date is 10 December."* (Category: `launch_date`, Status: `active`).

#### Step 2: Ingest Meeting 2 (Schedule Update)
```text
Rahul: The backend is completed.
Chirayu: The launch date should now be 15 December.
Priya: I will finish the presentation by 12 December.
```
- **Result:**
  - **Conflict Center Alert Triggered!**
  - MeetFlow AI detects that the launch date changed from `10 December` to `15 December`.
  - The previous decision is **not** overwritten automatically.
  - The user can click **"Confirm Change"**:
    - Marks December 10 as `superseded`.
    - Saves a historical record in `DecisionVersion`.
    - Activates December 15 as the new baseline.
  - Or click **"Keep Previous Decision"** to reject the change.

#### Step 3: Human Approval & Task Publishing
- Navigate to the **Task Tracker**.
- Newly extracted tasks are marked with an amber **"Pending Approval"** badge.
- Click **"Approve"** on Priya's presentation task.
- Click **"Publish Task"** to simulate publishing to Trello or the local board!

---

## 🧪 Running Automated Tests

MeetFlow AI includes comprehensive test coverage mocking LLM calls for 100% offline, cost-free validation:

```powershell
# Run backend test suite
.\backend\venv\Scripts\pytest.exe backend/tests -v
```

Test coverage includes:
- ✅ Meeting transcript processing & speaker attribution
- ✅ Explicit and relative date parsing
- ✅ Cross-meeting conflict detection
- ✅ Conflict resolution (confirm change vs keep previous)
- ✅ Mandatory task approval workflow
- ✅ Task CRUD & status transitions
- ✅ Background deadline reminder generation
- ✅ Weekly digest calculation

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory (refer to `.env.example`):

```ini
# Application
PROJECT_NAME="MeetFlow AI"
DEBUG=True
PORT=8000
HOST="0.0.0.0"

# Database
DATABASE_URL="sqlite:///./meetflow.db"

# LLM Provider (Optional - local fallback runs automatically if blank)
OPENAI_API_KEY=""
OPENAI_MODEL="gpt-4o-mini"

# Trello Task Integration (Optional)
TRELLO_API_KEY=""
TRELLO_TOKEN=""
TRELLO_LIST_ID=""

# Frontend
VITE_API_BASE_URL="http://localhost:8000/api"
```

---

## 🔮 Future Enhancements
- 🎙️ **Speech-to-Text & Diarization:** Direct audio file ingestion (`.mp3`, `.wav`) using OpenAI Whisper and PyAnnote audio diarization.
- 💬 **Slack / Microsoft Teams Bot:** Real-time reminders and conflict notifications delivered directly into team channels.
- ☁️ **Cloud Native Azure Deployment:** Terraform scripts for Azure App Service & Azure PostgreSQL Flexible Server.

---

## 🎓 Author & Presentation Details
- **Project:** MeetFlow AI — Complete AI Meeting-to-Execution Agent
- **Target:** B.Tech Computer Science AI Product Challenge
- **Architecture:** Decoupled, modular, enterprise-style micro-architecture with human-in-the-loop safety.
