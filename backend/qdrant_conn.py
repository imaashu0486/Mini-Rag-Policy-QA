from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from backend.config import settings

def get_qdrant_client():
    return QdrantClient(url=settings.QDRANT_URL)

def ensure_collection(vector_size: int):
    client = get_qdrant_client()
    collections = [c.name for c in client.get_collections().collections]

    if settings.QDRANT_COLLECTION not in collections:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )
