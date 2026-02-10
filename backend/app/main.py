from fastapi import FastAPI
from backend.app.db.session import engine
from backend.app.db.base import Base
from backend.app.api.security import router as security_router
from backend.app.api.logs import router as logs_router


app=FastAPI()


app.include_router(security_router)
app.include_router(logs_router)

@app.get("/")
def root():
    return {"status": "Secura AI running"}

Base.metadata.create_all(bind=engine)


@app.get("/")

def root():
    return{"service":"Secura AI","status":"running"}

