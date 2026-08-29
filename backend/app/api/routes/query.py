from fastapi import APIRouter, HTTPException, Depends, Request
import time
from app.api.schemas.query import (QueryRequest,QueryResponse)

from app.services.query_service import process_question
from app.api.dependencies import get_current_user
from app.services.audit_service import log_audit_server

router = APIRouter(prefix="/query",tags = ["Query"])

@router.post("",response_model=QueryResponse)
def query(request: Request, query_request: QueryRequest, current_user: dict = Depends(get_current_user)):
    start_time = time.perf_counter()
    
    try:
        result = process_question(question = query_request.question,user_role = current_user["role"].lower())
        print("\n========== QUERY METRICS ==========")
        print(result.get("metrics"))
        print("===================================\n")
        route = result["route"]
        data = result["result"]
        
        latency_ms = int((time.perf_counter() - start_time)*1000)
        if route == "SQL":
            log_audit_server(request_id = request.state.request_id,
                            user_id=int(current_user["user_id"]),
                            role=current_user["role"],
                            query_text=query_request.question,
                            route="SQL",
                            tables_used=[],
                            sources_used=[],
                            latency_ms=latency_ms,
                            status="SUCCESS",)
            
            return QueryResponse(route="SQL",answer=None,sql=data["sql"],rows=data["rows"])
        
        if route == "RAG":
            sources = data["sources"]
            
            source_ids = [source.get("document_id")
                          for source in sources
                          if source.get("document_id")
                          ]
            log_audit_server(
                request_id=request.state.request_id,
                user_id=int(current_user["user_id"]),
                role=current_user["role"],
                query_text=query_request.question,
                route="RAG",
                tables_used=[],
                sources_used=source_ids,
                latency_ms=latency_ms,
                status="SUCCESS",
            )
            return QueryResponse(route = "RAG",answer=data["answer"],sources = data["sources"])
        
        if route == "HYBRID":
            document_id = data["document_id"]
            contract_type = data.get("contract", {}).get("contract_type", "Contract")

            log_audit_server(
                request_id=request.state.request_id,
                user_id=int(current_user["user_id"]),
                role=current_user["role"],
                query_text=query_request.question,
                route="HYBRID",
                tables_used=[
                    "customers",
                    "customer_contracts",
                    "orders",
                ],
                sources_used=[
                    document_id
                ],
                latency_ms=latency_ms,
                status="SUCCESS",
            )

            return QueryResponse(
                route="HYBRID",
                answer=data["answer"],
                sources=[{
                    "document_id": data["document_id"],
                    "type": contract_type,
                    "name": f"Contract - {contract_type}"
                }]
            )
        
        raise HTTPException(status_code=500,detail="Unknown Query Route.")
    except ValueError as e:
        latency_ms = int(
            (time.perf_counter() - start_time) * 1000
        )
        log_audit_server(
                    request_id=request.state.request_id,
                    user_id=int(current_user["user_id"]),
                    role=current_user["role"],
                    query_text=query_request.question,
                    route="UNKNOWN",
                    tables_used=[],
                    sources_used=[],
                    latency_ms=latency_ms,
                    status="VALIDATION_ERROR",
                )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        latency_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        log_audit_server(
            request_id=request.state.request_id,
            user_id=int(current_user["user_id"]),
            role=current_user["role"],
            query_text=query_request.question,
            route="UNKNOWN",
            tables_used=[],
            sources_used=[],
            latency_ms=latency_ms,
            status="ERROR",
        )
        raise HTTPException(status_code=500,detail = str(e))
    
