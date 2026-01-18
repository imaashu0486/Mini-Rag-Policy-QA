import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION = os.getenv("QDRANT_COLLECTION")

VECTOR_SIZE = 384  # match embedding model

def get_client():
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

from qdrant_client.http.exceptions import UnexpectedResponse

def ensure_collection():
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION not in collections:
        try:
            client.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
        except UnexpectedResponse:
            pass  # collection already exists
