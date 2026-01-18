import os
from backend.embeddings import embed_texts
from backend.qdrant_conn import get_client

COLLECTION = os.getenv("QDRANT_COLLECTION")

def retrieve(query: str, top_k: int = 10):
    client = get_client()
    vector = embed_texts([query])[0]

    results = client.query_points(
        collection_name=COLLECTION,
        prefetch=[],
        query=vector,
        limit=top_k
    ).points

    return [
        {
            "text": r.payload["text"],
            "source": r.payload.get("source"),
            "title": r.payload.get("title"),
            "position": r.payload.get("position"),
        }
        for r in results
    ]
