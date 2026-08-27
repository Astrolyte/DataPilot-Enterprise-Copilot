from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are the final answer generator for AcmeCloud DataPilot.

Answer the user's question using ONLY the supplied
database results and document context.

Rules:

- Do not invent information.
- Do not perform calculations that are not supported
  by the supplied data.
- Clearly distinguish structured database facts from
  document facts when useful.
- Give a concise, direct answer.
- Mention the relevant source/document when answering
  from contract or policy information.
""",
        ),
        (
            "human",
            """
User question:
{question}

Database results:
{database_results}

Document context:
{document_context}
""",
        ),
    ]
)


def generate_hybrid_answer(
    question: str,
    database_results,
    document_context,
):

    response = prompt.invoke(
        {
            "question": question,
            "database_results": database_results,
            "document_context": document_context,
        }
    )

    result = llm.invoke(response)

    return result.content.strip()