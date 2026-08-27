from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(model="llama3.2:3b",temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You extract customer/company names from AcmeCloud
DataPilot questions.

Return ONLY the company name mentioned in the question.

Rules:

- Return the exact company name as written by the user.
- Do not add explanations.
- Do not add quotes.
- If no company/customer is mentioned, return:
  NONE

Examples:

Question:
What is Price LLC's refund window?

Answer:
Price LLC

Question:
How much revenue did Austin, Day and Johnson generate?

Answer:
Austin, Day and Johnson

Question:
Which customer generated the most revenue?

Answer:
NONE
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


chain = prompt | llm


def extract_company_name(question: str) -> str | None:

    response = chain.invoke(
        {
            "question": question,
        }
    )

    company_name = response.content.strip()

    if company_name.upper() == "NONE":
        return None

    return company_name