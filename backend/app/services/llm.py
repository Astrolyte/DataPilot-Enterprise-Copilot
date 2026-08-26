from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


MODEL_NAME = "llama3.2:3b"


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)


prompt = ChatPromptTemplate(
    [
        (
            "system",
            """
You are DataPilot, an enterprise data assistant.

Answer questions ONLY using the provided context.

Rules:
1. Do not invent facts.
2. Do not use outside knowledge.
3. If the context does not contain enough information,
   say that the information is not available.
4. Give concise and direct answers.
5. Preserve important numbers, dates, and names.
6. Do not reveal information that is not present
   in the retrieved context.
            """,
        ),
        (
            "human",
            """
Question:{question}

Retrieved Context:{context}

Answer the question using only the retrieved context.
            """,
        ),
    ]
)


chain = prompt | llm


def generate_answer(question: str,context: str,):

    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return response.content