from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/paraphrase-MiniLM-L3-v2"
        )
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    ).tolist()
