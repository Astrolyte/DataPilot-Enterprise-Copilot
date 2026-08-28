from fastapi import FastAPI
from app.api.routes.query import router as query_router
from app.api.routes.auth import router as auth_router
app = FastAPI(title="DataPilot Enterprise Copilot",version="1.0.0")

app.include_router(query_router)
app.include_router(auth_router)

@app.get("/health")
def health():
    return {
        "status":"healthy",
        "service":"datapilot"
    }
