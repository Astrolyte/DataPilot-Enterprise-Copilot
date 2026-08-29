from app.services.router import route_question
from app.services.sql import ask_sql
from app.services.rag import ask as ask_rag
from app.services.hybrid import ask_hybrid
from app.services.entity_extractor import extract_company_name
import time

def process_question(question: str,user_role: str = "admin",company_name: str | None = None):

    total_start = time.perf_counter()
    
    ##ROUTING ---------
    
    routing_start = time.perf_counter()
    
    route = route_question(question)
    
    routing_ms = int((time.perf_counter()-routing_start)*1000)
    
    if route == "SQL":

        sql_start = time.perf_counter()
        result = ask_sql(question)
        sql_ms = int((time.perf_counter()-sql_start)*1000)
        total_ms = int((time.perf_counter() - total_start) * 1000)
        
        return {
            "route": "SQL",
            "result": result,
            "metrics": {
                "routing_ms": routing_ms,
                "sql_ms": sql_ms,
                "total_ms": total_ms,
            },
        }

    if route == "RAG":

        rag_start = time.perf_counter()
        
        result = ask_rag(question=question,user_role=user_role)

        rag_ms = int((time.perf_counter() - rag_start)*1000)
        
        total_ms = int((time.perf_counter() - total_start) * 1000)
        
        return {
            "route": "RAG",
            "result": result,
            "metrics":{
                "routing_ms":routing_ms,
                "rag_ms": rag_ms,
                "total_ms": total_ms,
            }
        }

    if route == "HYBRID":

        extraction_start = time.perf_counter()
        
        company_name = extract_company_name(question)
        
        extraction_ms = int((time.perf_counter() - extraction_start)*1000)
        if not company_name:
            raise ValueError("NO Customer/Company was found in the question")

        hybrid_start = time.perf_counter()
        
        result = ask_hybrid(company_name=company_name,question=question,)

        hybrid_ms = int((time.perf_counter()-hybrid_start)*1000)
        
        total_ms = int((time.perf_counter() - total_start) * 1000)
        return {"route": "HYBRID","result": result, "metrics": {
                "routing_ms": routing_ms,
                "entity_extraction_ms": extraction_ms,
                "hybrid_ms": hybrid_ms,
                "total_ms": total_ms,
            },}

    raise ValueError(
        f"Unsupported route: {route}"
    )