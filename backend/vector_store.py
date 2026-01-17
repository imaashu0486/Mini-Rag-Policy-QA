import uuid
from qdrant_client.models import PointStruct
from backend.qdrant_conn import get_qdrant_client, ensure_collection
from backend.embeddings import embed_texts
from backend.config import settings


def upsert_chunks(chunks: list[dict]):
    texts = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    # Ensure collection exists with correct vector size
    ensure_collection(vector_size=len(vectors[0]))

    points = []
    for chunk, vector in zip(chunks, vectors):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),  # ✅ VALID QDRANT ID
                vector=vector,
                payload={
                    "text": chunk["text"],
                    **chunk["metadata"]
                }
            )
        )

    client = get_qdrant_client()
    client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points
    )
