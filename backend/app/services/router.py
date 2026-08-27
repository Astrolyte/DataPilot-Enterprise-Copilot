from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(model="llama3.2:3b",temperature=0,)


router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the query router for AcmeCloud DataPilot.

Classify the user's question into exactly ONE route:

SQL
RAG
HYBRID

Use these rules:

SQL:
Use SQL when the question can be answered entirely
from structured PostgreSQL data.

Examples:
- How many customers do we have?
- Which customer generated the most revenue?
- How many orders were completed?
- What is the total revenue?

RAG:
Use RAG when the question can be answered entirely
from company documents, policies, or contracts.

Examples:
- What is the refund policy?
- How much PTO do employees receive?
- What is the enterprise SLA?
- What is Price LLC's refund window?

HYBRID:
Use HYBRID when the question requires both structured
database information and document information.

Example:
- What is Price LLC's refund window and how much revenue
  has Price LLC generated?

Rules:
- Return ONLY one word.
- Valid outputs are exactly:
  SQL
  RAG
  HYBRID
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


router_chain = router_prompt | llm


def route_question(question: str) -> str:

    response = router_chain.invoke(
        {
            "question": question,
        }
    )

    route = response.content.strip().upper()

    if route not in {
        "SQL",
        "RAG",
        "HYBRID",
    }:
        raise ValueError(
            f"Invalid route returned by LLM: {route}"
        )

    return route