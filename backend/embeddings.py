import hashlib
from backend.config import USE_LOCAL_EMBEDDINGS

# ---------- FULL MODE (LOCAL / REAL) ----------
if USE_LOCAL_EMBEDDINGS:
    from sentence_transformers import SentenceTransformer

    _model = None

    def get_model():
        global _model
        if _model is None:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model

    def embed_texts(texts: list[str]) -> list[list[float]]:
        return get_model().encode(texts, normalize_embeddings=True).tolist()

# ---------- LITE MODE (MOCK EMBEDDINGS) ----------
else:
    def fake_embedding(text: str, dim: int = 384):
        h = hashlib.sha256(text.encode()).digest()
        return [(b / 255.0) for b in h[:dim]]

    def embed_texts(texts: list[str]) -> list[list[float]]:
        return [fake_embedding(t) for t in texts]
