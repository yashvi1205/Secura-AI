from fastapi import FastAPI
from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.api.security import router as security_router
from backend.app.api.logs import router as logs_router
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from collections import defaultdict,deque
from datetime import datetime,timedelta
from backend.app.api.admin import router as admin_router
from backend.app.api.catalog import router as catalog_router
from backend.app.api.bootstrap import router as bootstrap_router
from backend.app.api.console import router as console_router
from backend.app.api.ingest import router as ingest_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.core.config import settings

app=FastAPI()

RATE_LIMIT = settings.rate_limit
RATE_WINDOW = settings.rate_window_seconds
client_requests = defaultdict(deque)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_allow_origins.split(",")] if settings.cors_allow_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(security_router)
app.include_router(logs_router)
app.include_router(admin_router)
app.include_router(bootstrap_router)
app.include_router(catalog_router)
app.include_router(console_router)
app.include_router(ingest_router)

repo_root = Path(__file__).resolve().parents[2]  # backend/app/main.py -> project root
frontend_dir = repo_root / "frontend"
if frontend_dir.exists():
    @app.get("/ui")
    def redirect_ui():
        return RedirectResponse(url="/ui/", status_code=302)
    app.mount("/ui", StaticFiles(directory=str(frontend_dir), html=True), name="ui")

@app.middleware("http")
async def rate_limit_middleware(request:Request,call_next):
    client_ip= request.client.host
    now=datetime.now()
    client_requests[client_ip].append(now)

    window_start = now - timedelta(seconds=RATE_WINDOW)

    while client_requests[client_ip] and client_requests[client_ip][0] <= window_start:
        client_requests[client_ip].popleft()

    if len(client_requests[client_ip]) > RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"}
        )

    response = await call_next(request)
    return response


@app.get("/")
def root():
    return {"status": "Secura AI running"}

if settings.auto_create_schema:
    Base.metadata.create_all(bind=engine)

