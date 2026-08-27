from fastapi import FastAPI
from app.api.routes.query import router

app = FastAPI(title="DataPilot Enterprise Copilot",version="1.0.0")

app.include_router(router)

@app.get("/health")
def health():
    return {
        "status":"healthy",
        "service":"datapilot"
    }
