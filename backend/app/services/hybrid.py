from sqlalchemy import text

from app.core.database import engine

from app.services.hybrid_answer import generate_hybrid_answer

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


def get_customer_revenue(customer_id: int):
    """
    Calculate completed revenue for a customer.
    """

    query = text(
        """
        SELECT
            COALESCE(
                SUM(total_amount),
                0
            ) AS completed_revenue
        FROM orders
        WHERE customer_id = :customer_id
          AND status = 'completed'
        """
    )

    with engine.connect() as connection:

        row = connection.execute(
            query,
            {
                "customer_id": customer_id,
            },
        ).mappings().first()

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


def ask_hybrid(
    company_name: str,
    question: str,
):
    """
    Execute a hybrid query using:

    PostgreSQL:
        - customer lookup
        - contract metadata
        - completed revenue

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
    # 3. Get completed revenue
    # --------------------------------------------------

    revenue = get_customer_revenue(
        customer_id
    )

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
            "revenue": revenue,
        },
        document_context=document_context,
    )

    return {
        "answer": answer,
        "customer": customer,
        "contract": contract,
        "revenue": revenue,
        "document_id": contract["document_id"],
        "document_context": document_context,
    }