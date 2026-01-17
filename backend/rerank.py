from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_chunks(query, chunks, top_n=5):
    pairs = [(query, c["text"]) for c in chunks]
    scores = model.predict(pairs)

    for i, score in enumerate(scores):
        chunks[i]["score"] = float(score)

    ranked = sorted(chunks, key=lambda x: x["score"], reverse=True)
    return ranked[:top_n]
