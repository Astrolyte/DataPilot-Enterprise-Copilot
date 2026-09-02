from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.query import router as query_router
from app.api.routes.auth import router as auth_router
from app.middleware.request_id import RequestIDMiddleware

app = FastAPI(title="DataPilot Enterprise Copilot", version="1.0.0")

# Addde RequestIDMiddleware first (so it executes last, after CORS)
app.add_middleware(RequestIDMiddleware)

#CORS middleware added last (so it executes first, before other middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
    expose_headers=["X-Request-ID"],
)

app.include_router(query_router)
app.include_router(auth_router)

@app.get("/health")
def health():
    return {
        "status":"healthy",
        "service":"datapilot"
    }
