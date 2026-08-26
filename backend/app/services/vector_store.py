from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url = "http://localhost:6333")

VECTOR_SIZE = 384 
# no of dimensions of that model

COLLECTION_NAME = "datapilot_documents"

def create_collections():
    
    existing_collections = [
        collection.name
        for collection in client.get_collections().collections
    ]
    
    if COLLECTION_NAME in existing_collections:
        
        print(f"Collections {COLLECTION_NAME} already exists")
        return
    
    client.create_collection(
        collection_name = COLLECTION_NAME,
        vectors_config = VectorParams(
            size = VECTOR_SIZE,
            distance = Distance.COSINE
        )
    )

    print(f"collection created {COLLECTION_NAME}")