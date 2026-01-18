from sentence_transformers import CrossEncoder

# Lazy load to avoid startup crash
_model = None

def get_model():
    global _model
    if _model is None:
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _model


def rerank_chunks(query: str, chunks: list[dict], top_n: int = 5):
    if not chunks:
        return []

    pairs = [(query, c["text"]) for c in chunks]
    scores = get_model().predict(pairs)

    for c, score in zip(chunks, scores):
        c["score"] = float(score)

    chunks.sort(key=lambda x: x["score"], reverse=True)
    return chunks[:top_n]
