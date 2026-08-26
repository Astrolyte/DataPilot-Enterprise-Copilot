import re
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIRS = (Path("data/documents"), Path("data/contracts"))
COLLECTION_NAME = "datapilot_documents"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384  # bge-small's output size

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer(EMBEDDING_MODEL)

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100,
    separators=[
        "\n\n","\n",". "," ",""
    ]
)


def parse_header(text: str):
    """Pull [key: value] metadata lines from the top of a doc into a dict."""
    metadata = {}
    body_lines = []
    for line in text.splitlines():
        match = re.match(r"\[(\w+):\s*(.+)\]", line)
        if match:
            key, value = match.groups()
            metadata[key] = value
        elif line.strip():
            body_lines.append(line)
    return metadata, "\n".join(body_lines)


def chunk_text(body: str):
    """Performing Recursive Character Splitting"""
    return splitter.split_text(body)


def main():
    # Recreate the collection fresh each run — safe during development
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
    )

    points = []
    point_id = 0
    total_documents = 0

    for docs_root in DOCS_DIRS:
        for file_path in docs_root.rglob("*.txt"):
            total_documents += 1
            raw_text = file_path.read_text(encoding="utf-8")
            metadata, body = parse_header(raw_text)
            document_id = metadata.get("document_id")
            if not document_id:
                document_id = file_path.stem
            chunks = chunk_text(body)

            for chunk_index, chunk in enumerate(chunks):
                embedding = model.encode(chunk,normalize_embeddings=True).tolist()
                
                
                payload = {
                    **metadata,
                    "document_id": document_id,
                    "allowed_roles": metadata.get("allowed_roles", "").split(","),
                    "chunk_index": chunk_index,
                    "chunk_text": chunk,
                    "source_file": str(file_path.relative_to(docs_root)),
                }

                points.append(
                    PointStruct(id=point_id, vector=embedding, payload=payload)
                )
                point_id += 1

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Ingested {len(points)} chunks from {total_documents} documents.")


if __name__ == "__main__":
    main()