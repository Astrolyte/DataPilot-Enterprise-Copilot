from app.services.retriever import retrieve
from app.services.context import build_context
from app.services.llm import chain
import time

def ask(question: str,user_role: str,top_k: int = 3):
    
    total_start = time.perf_counter()
    # 1. Retrieve authorized documents
    retrieval_start = time.perf_counter()
    results = retrieve(query=question,user_role=user_role,top_k=top_k)
    retrieval_ms = int((time.perf_counter() - retrieval_start) * 1000)
    
    # 2. Build LLM context
    context_start = time.perf_counter()
    
    context = build_context(results)

    context_ms = int((time.perf_counter() - context_start) * 1000)

    # 3. Generate answer
    llm_start = time.perf_counter()
    
    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )
    llm_ms = int((time.perf_counter() - llm_start) * 1000)


    total_ms = int(
        (time.perf_counter() - total_start) * 1000
    )

    metrics = {
        "retrieval_ms": retrieval_ms,
        "context_ms": context_ms,
        "llm_ms": llm_ms,
        "total_ms": total_ms,
    }
    
    print("\n========== RAG METRICS ==========")
    print(metrics)
    print("=================================\n")
    
    
    return {
        "answer": response.content,
        "context":context,
        "sources": results,
        "metrics":metrics
    }