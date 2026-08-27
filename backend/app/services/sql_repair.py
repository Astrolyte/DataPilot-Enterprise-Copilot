from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)


repair_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a PostgreSQL SQL repair assistant.

You are given:
1. A user's original question.
2. SQL generated for that question.
3. The PostgreSQL error produced when executing that SQL.

Fix the SQL so that it correctly answers the user's question.

Use ONLY the following schema:

employees(
    employee_id,
    name,
    department,
    region,
    role,
    email
)

customers(
    customer_id,
    company_name,
    industry,
    country,
    customer_segment,
    account_manager_id,
    created_at
)

products(
    product_id,
    product_name,
    category,
    price
)

orders(
    order_id,
    customer_id,
    order_date,
    status,
    total_amount
)

order_items(
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price
)

transactions(
    transaction_id,
    customer_id,
    amount,
    transaction_type,
    date,
    status
)

customer_contracts(
    contract_id,
    customer_id,
    contract_type,
    refund_window_days,
    document_id,
    signed_date,
    annual_value
)

Rules:

- Return ONLY the corrected SQL.
- Only SELECT queries are allowed.
- Never use columns that do not exist.
- Never invent tables or columns.
- Preserve the original intent of the question.
- PostgreSQL syntax only.
""",
        ),
        (
            "human",
            """
Original question:
{question}

Generated SQL:
{sql}

PostgreSQL error:
{error}
""",
        ),
    ]
)


repair_chain = repair_prompt | llm


def repair_sql(
    question: str,
    sql: str,
    error: str,
) -> str:

    response = repair_chain.invoke(
        {
            "question": question,
            "sql": sql,
            "error": error,
        }
    )

    repaired_sql = response.content.strip()

    if repaired_sql.startswith("```"):
        repaired_sql = repaired_sql.replace(
            "```sql",
            "",
        )
        repaired_sql = repaired_sql.replace(
            "```",
            "",
        )
        repaired_sql = repaired_sql.strip()

    return repaired_sql