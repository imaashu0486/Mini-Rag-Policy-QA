import os
from backend.config import USE_LOCAL_EMBEDDINGS

# ---------- FULL MODE (LOCAL MODEL) ----------
if USE_LOCAL_EMBEDDINGS:
    from sentence_transformers import SentenceTransformer

    _model = None

    def get_model():
        global _model
        if _model is None:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model

    def embed_texts(texts: list[str]) -> list[list[float]]:
        return get_model().encode(
            texts,
            normalize_embeddings=True
        ).tolist()

# ---------- LITE MODE (GROQ EMBEDDINGS) ----------
else:
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def embed_texts(texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            model="nomic-embed-text",
            input=texts
        )
        return [d.embedding for d in response.data]
