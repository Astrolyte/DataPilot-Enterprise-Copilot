from sqlalchemy import text

from app.core.database import engine

def log_audit_server(
    request_id:str,
    user_id: int| None,
    role: str | None,
    query_text: str | None,
    route: str | None,
    tables_used: list[str] | None = None,
    sources_used: list[str] | None = None,
    latency_ms: int | None = None,
    status: str = "SUCCESS",
):
    query = text(
        """
        INSERT INTO audit_logs (
            request_id,
            user_id,
            role,
            query_text,
            route,
            tables_used,
            sources_used,
            latency_ms,
            status
        )
        VALUES (
            :request_id,
            :user_id,
            :role,
            :query_text,
            :route,
            :tables_used,
            :sources_used,
            :latency_ms,
            :status
        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "request_id": request_id,
                "user_id": user_id,
                "role": role,
                "query_text": query_text,
                "route": route,
                "tables_used": tables_used,
                "sources_used": sources_used,
                "latency_ms": latency_ms,
                "status": status,
            },
        )