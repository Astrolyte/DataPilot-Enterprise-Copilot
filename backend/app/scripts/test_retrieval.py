from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


COLLECTION_NAME = "datapilot_documents"

client = QdrantClient(host="localhost",port=6333,)

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def search(query: str, top_k: int = 5):

    query_vector = model.encode(query,normalize_embeddings=True,).tolist()

    results = client.query_points(collection_name=COLLECTION_NAME,query=query_vector,
                                  limit=top_k,
    ).points

    print(f"\nQuery: {query}")

    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")

        print(f"Score: {result.score:.4f}")

        print(f"Document: "f"{result.payload.get('document_id')}")

        print(f"Source: "f"{result.payload.get('source_file')}")

        print(f"Department: "f"{result.payload.get('department')}")

        print(f"Customer ID: "f"{result.payload.get('customer_id')}")

        print(f"\nText:\n"f"{result.payload.get('chunk_text')}")


if __name__ == "__main__":

    search("What were our highest-value customers last quarter?")