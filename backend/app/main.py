from fastapi import FastAPI
from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.api.security import router as security_router
from backend.app.api.logs import router as logs_router
from fastapi import Request
from fastapi.responses import JSONResponse
from collections import defaultdict,deque
from datetime import datetime,timedelta
from backend.app.api.admin import router as admin_router
import os

app=FastAPI()

RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))
RATE_WINDOW = int(os.getenv("RATE_WINDOW", 60))
client_requests = defaultdict(deque)

app.include_router(security_router)
app.include_router(logs_router)
app.include_router(admin_router)

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

Base.metadata.create_all(bind=engine)


@app.get("/")

def root():
    return{"service":"Secura AI","status":"running"}

