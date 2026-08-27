from fastapi import APIRouter, HTTPException

from app.api.schemas.query import (QueryRequest,QueryResponse)

from app.services.query_service import process_question

router = APIRouter(prefix="/query",tags = ["Query"])

@router.post("",response_model=QueryResponse)
def query(request: QueryRequest):
    
    try:
        result = process_question(question = request.question,user_role = request.user_role)
        
        route = result["route"]
        data = result["result"]
        
        if route == "SQL":
            return QueryResponse(route="SQL",answer=None,sql=data["sql"],rows=data["rows"])
        
        if route == "RAG":
            return QueryResponse(route = "RAG",answer=data["answer"],sources = data["sources"])
        
        if route == "HYBRID":
            return QueryResponse(route = "HYBRID",answer=data["answer"],sources=[{"document_id": data["document_id"],"type":data["contract"]}])
        
        raise HTTPException(status_code=500,detail="Unknown Query Route.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500,detail = str(e))
    
