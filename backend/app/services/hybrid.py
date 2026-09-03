import sqlglot
from sqlglot import exp
from sqlalchemy import text

from app.core.database import engine

from app.services.hybrid_answer import generate_hybrid_answer
from app.services.sql import ask_sql

from qdrant_client import QdrantClient
from qdrant_client.models import (Filter,FieldCondition,MatchValue,)


qdrant_client = QdrantClient(host="localhost",port=6333)

COLLECTION_NAME = "datapilot_documents"


def find_customer(company_name: str):
    """
    Resolve a company name to its PostgreSQL customer record.
    """

    query = text(
        """
        SELECT
            customer_id,
            company_name
        FROM customers
        WHERE company_name ILIKE :company_name
        LIMIT 1
        """
    )

    with engine.connect() as connection:

        row = connection.execute(
            query,
            {
                "company_name": company_name,
            },
        ).mappings().first()

    if not row:
        return None

    return dict(row)


def get_customer_contract(customer_id: int):
    """
    Get the contract metadata associated with a customer.
    """

    query = text(
        """
        SELECT
            contract_id,
            customer_id,
            contract_type,
            refund_window_days,
            document_id,
            signed_date,
            annual_value
        FROM customer_contracts
        WHERE customer_id = :customer_id
        LIMIT 1
        """
    )

    with engine.connect() as connection:

        row = connection.execute(
            query,
            {
                "customer_id": customer_id,
            },
        ).mappings().first()

    if not row:
        return None

    return dict(row)


def get_contract_document(document_id: str):
    """
    Retrieve the exact contract document from Qdrant
    using its document_id.
    """

    results = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id
                    ),
                )
            ]
        ),
        limit=10,
    )[0]

    return [
        {
            "document_id": point.payload.get(
                "document_id"
            ),
            "chunk_index": point.payload.get(
                "chunk_index"
            ),
            "chunk_text": point.payload.get(
                "chunk_text"
            ),
            "source_file": point.payload.get(
                "source_file"
            ),
        }
        for point in results
    ]


def _tables_in_sql(sql: str) -> list[str]:
    """Return the tables referenced by a validated SQL query."""
    tables = []
    for table in sqlglot.parse_one(sql, read="postgres").find_all(exp.Table):
        table_name = table.name.lower()
        if table_name not in tables:
            tables.append(table_name)
    return tables


def ask_hybrid(
    company_name: str,
    question: str,
):
    """
    Execute a hybrid query using:

    PostgreSQL:
        - the existing Text-to-SQL pipeline for structured facts
        - customer lookup and contract metadata for document resolution

    Qdrant:
        - exact contract document

    LLM:
        - final answer synthesis
    """

    # --------------------------------------------------
    # 1. Resolve customer
    # --------------------------------------------------

    customer = find_customer(
        company_name
    )

    if not customer:
        raise ValueError(
            f"Customer '{company_name}' not found."
        )

    customer_id = customer["customer_id"]

    # --------------------------------------------------
    # 2. Get contract metadata
    # --------------------------------------------------

    contract = get_customer_contract(
        customer_id
    )

    if not contract:
        raise ValueError(
            f"No contract found for "
            f"'{company_name}'."
        )

    # --------------------------------------------------
    # 3. Run the structured part through the same guarded SQL pipeline
    #    used by normal SQL queries. This keeps retrieval driven by the
    #    question instead of always fetching revenue.
    # --------------------------------------------------
    sql_result = ask_sql(question)

    # --------------------------------------------------
    # 4. Retrieve exact contract document
    # --------------------------------------------------

    document = get_contract_document(
        contract["document_id"]
    )

    if not document:
        raise ValueError(
            f"Contract document "
            f"'{contract['document_id']}' "
            f"not found in Qdrant."
        )

    # Combine document chunks
    document_context = "\n\n".join(
        chunk["chunk_text"]
        for chunk in document
    )

    # --------------------------------------------------
    # 5. Generate final answer
    # --------------------------------------------------

    answer = generate_hybrid_answer(
        question=question,
        database_results={
            "customer": customer,
            "contract": contract,
            "sql": sql_result["sql"],
            "rows": sql_result["rows"],
        },
        document_context=document_context,
    )

    tables_used = ["customers", "customer_contracts"]
    for table in _tables_in_sql(sql_result["sql"]):
        if table not in tables_used:
            tables_used.append(table)

    return {
        "answer": answer,
        "customer": customer,
        "contract": contract,
        "sql": sql_result["sql"],
        "rows": sql_result["rows"],
        "attempts": sql_result["attempts"],
        "tables_used": tables_used,
        "document_id": contract["document_id"],
        "document_context": document_context,
    }