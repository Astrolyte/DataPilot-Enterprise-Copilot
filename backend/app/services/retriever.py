from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

COLLECTION_NAME = "datapilot_documents"


def retrieve(query: str, user_role: str, top_k: int = 5):
    query_vector = model.encode(query).tolist()

    role_filter = Filter(
        must=[
            FieldCondition(
                key="allowed_roles",
                match=MatchAny(any=[user_role]),
            )
        ]
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=role_filter,
        limit=top_k,
    ).points

    return [
        {
            "score": r.score,
            "source_file": r.payload.get("source_file"),
            "chunk_text": r.payload.get("chunk_text"),
            "allowed_roles": r.payload.get("allowed_roles"),
            "customer_id": r.payload.get("customer_id"),
            "document_id":r.payload.get("document_id")
        }
        for r in results
    ]