from app.services.retriever import retrieve
from app.services.context import build_context
from app.services.llm import chain


def ask(question: str,user_role: str,top_k: int = 3):

    # 1. Retrieve authorized documents
    results = retrieve(query=question,user_role=user_role,top_k=top_k)

    # 2. Build LLM context
    context = build_context(results)

    # 3. Generate answer
    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return {
        "answer": response.content,
        "context":context,
        "sources": results,
    }