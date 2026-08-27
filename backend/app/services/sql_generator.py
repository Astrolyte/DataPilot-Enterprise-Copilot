from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
)


sql_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a PostgreSQL SQL generation assistant for AcmeCloud.

Your job is to convert a user's natural language question
into a PostgreSQL SELECT query.

Database schema:

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

users(
    user_id,
    username,
    password_hash,
    role,
    employee_id,
    created_at
)

audit_logs(
    log_id,
    request_id,
    user_id,
    role,
    query_text,
    route,
    tables_used,
    sources_used,
    latency_ms,
    status,
    created_at
)

Rules:

1. Generate ONLY SELECT statements.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, GRANT, or REVOKE.
3. Never access password_hash.
4. Use PostgreSQL syntax.
5. Use table aliases for joins.
6. Return ONLY the SQL query.
7. Do not wrap the query in markdown.
8. Translate every explicit condition in the user's question into
   the SQL WHERE clause.

9. If the question asks about "completed orders" or
   "completed revenue", always include:
   WHERE status = 'completed'

10. Do not invent column names. Only use columns explicitly listed
    in the schema above.
            """,
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


sql_chain = sql_prompt | llm


def generate_sql(question: str) -> str:

    response = sql_chain.invoke(
        {
            "question": question,
        }
    )

    sql = response.content.strip()

    # Remove markdown fences if the model ignores the instruction
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

    return sql