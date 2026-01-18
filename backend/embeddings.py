import os
from backend.config import USE_LOCAL_EMBEDDINGS

# ---------- FULL MODE ----------
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

# ---------- LITE MODE ----------
else:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_texts(texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [d.embedding for d in response.data]
