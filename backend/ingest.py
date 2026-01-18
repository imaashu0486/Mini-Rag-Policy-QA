global LAST_DOCUMENT
LAST_DOCUMENT = {
    "title": req.title,
    "source": req.source,
    "text": req.text
}


from backend.embeddings import embed_texts
from backend.qdrant_conn import get_qdrant_client
from backend.config import settings
from uuid import uuid4
import re

CHUNK_SIZE = 800
OVERLAP = 120


def chunk_text(text: str):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - OVERLAP

    return chunks


def ingest_document(
    text: str,
    source: str,
    title: str | None = None
):
    client = get_qdrant_client()

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append({
            "id": str(uuid4()),
            "vector": vector,
            "payload": {
                "source": source,
                "title": title or source,
                "section": "N/A",
                "chunk_index": i,
                "text": chunk,
            },
        })

    client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points,
    )

    return len(points)
