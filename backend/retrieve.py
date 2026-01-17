from backend.qdrant_conn import get_qdrant_client
from backend.embeddings import embed_texts
from backend.config import settings


def retrieve_chunks(query: str, top_k: int = 10):
    """
    Universal Qdrant retrieval (works across all client versions)
    """
    client = get_qdrant_client()
    query_vector = embed_texts([query])[0]

    response = client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        prefetch=[],
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    chunks = []
    for point in response.points:
        chunks.append({
            "text": point.payload["text"],
            "score": point.score,
            "metadata": {
                k: v for k, v in point.payload.items() if k != "text"
            }
        })

    return chunks
