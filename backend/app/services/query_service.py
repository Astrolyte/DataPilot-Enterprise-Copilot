from app.services.router import route_question
from app.services.sql import ask_sql
from app.services.rag import ask as ask_rag
from app.services.hybrid import ask_hybrid
from app.services.entity_extractor import extract_company_name


def process_question(question: str,user_role: str = "admin",company_name: str | None = None):

    route = route_question(question)

    if route == "SQL":

        result = ask_sql(question)

        return {
            "route": "SQL",
            "result": result,
        }

    if route == "RAG":

        result = ask_rag(question=question,user_role=user_role)

        return {
            "route": "RAG",
            "result": result,
        }

    if route == "HYBRID":

        company_name = extract_company_name(question)
        if not company_name:
            raise ValueError("NO Customer/Company was found in the question")

        result = ask_hybrid(company_name=company_name,question=question,)

        return {"route": "HYBRID","result": result,}

    raise ValueError(
        f"Unsupported route: {route}"
    )