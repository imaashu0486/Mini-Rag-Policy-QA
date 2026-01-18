import uuid
from qdrant_client.models import PointStruct
from backend.qdrant_conn import get_client, ensure_collection
from backend.embeddings import embed_texts
import os

COLLECTION = os.getenv("QDRANT_COLLECTION")

def upsert_chunks(chunks: list[dict]):
    ensure_collection()
    client = get_client()

    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    points = []
    for chunk, vector in zip(chunks, vectors):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk["metadata"] | {"text": chunk["text"]}
            )
        )

    client.upsert(collection_name=COLLECTION, points=points)
