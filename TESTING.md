# Secura AI – How to Run, Test & Flow

## 1. Run the Application

```powershell
cd c:\Users\winuser\Desktop\secura-ai
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --reload
```

Then open in your browser: **http://127.0.0.1:8000/ui/** (use the trailing slash).

---

## 2. Software Flow (Architecture)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SECURA AI FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐     HTTP      ┌──────────────────────────────────────────┐
  │   Browser    │ ◄──────────►  │         FastAPI Backend (port 8000)        │
  │   (UI)       │               │                                            │
  │              │               │  • Serves UI at /ui/ (StaticFiles)         │
  │  /ui/        │               │  • API: /secure, /logs, /admin/*,          │
  │  - Home      │               │    /console/*, /ingest/events             │
  │  - Downloads │               │                                            │
  │  - Console   │               │  ┌─────────────┐  ┌─────────────────────┐  │
  │  - Analyzer  │               │  │ SQLAlchemy  │  │ Redis + RQ (async)  │  │
  └──────────────┘               │  │ SQLite/     │  │ (detection workers) │  │
        │                        │  │ Postgres    │  └─────────────────────┘  │
        │                        │  └─────────────┘                            │
        │                        └──────────────────────────────────────────┘
        │
        │  API calls use:
        │  • API Base = window.location.origin (same host when served from backend)
        │  • X-Secura-Key header for console endpoints (after bootstrap)
        │
        ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  REQUEST FLOW                                                             │
  │                                                                           │
  │  1. Legacy Analyzer:  POST /secure  →  analyze_prompt()  →  ThreatLog      │
  │  2. Console (Overview/Events/Detections/Incidents):                       │
  │     GET /console/*  →  require_api_key  →  query Event/Detection/Incident │
  │  3. Ingest (agents/SDK):  POST /ingest/events  →  enqueue  →  worker       │
  │     →  Detection + Incident                                                │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. How to Test

### A. No setup (works immediately)

| Test | Steps | Expected |
|------|-------|----------|
| **Health** | Open http://127.0.0.1:8000/ | `{"status": "Secura AI running"}` |
| **Home** | Open http://127.0.0.1:8000/ui/ | Hero, feature cards, no errors |
| **Downloads** | Click "Downloads" | Platform cards from `downloads.json` |
| **Legacy Analyzer** | Click "Legacy Analyzer" → enter prompt → "Analyze & Log" | Risk level, score, reasons |

### B. Console (needs bootstrap)

1. Create `.env` in project root:
   ```
   BOOTSTRAP_TOKEN=test-token-123
   AUTO_CREATE_SCHEMA=true
   ```

2. Restart uvicorn, then bootstrap:
   ```powershell
   curl -X POST http://127.0.0.1:8000/admin/bootstrap -H "X-Bootstrap-Token: test-token-123" -H "Content-Type: application/json" -d "{\"org_name\": \"Test\"}"
   ```

3. Copy the `api_key` from the response.

4. In the UI: **Settings** → paste key into **X-Secura-Key** → **Save settings**.

5. Use **Overview**, **Live Events**, **Detections**, **Incidents** – they should load.

---

## 4. UI ↔ Backend Connection

| UI Element | Backend Endpoint | Auth |
|------------|------------------|------|
| Home, Downloads, Pricing, Docs | Static (no API) | — |
| Legacy Analyzer | `POST /secure` | None |
| Overview | `GET /console/overview` | X-Secura-Key |
| Live Events | `GET /console/events` | X-Secura-Key |
| Detections | `GET /console/detections` | X-Secura-Key |
| Incidents | `GET /console/incidents` | X-Secura-Key |
| Settings | Saves API base + key to `localStorage` | — |

**API Base** is set automatically to `window.location.origin` when the UI is served from the backend, so requests go to the same host.
