from vector_store import upsert_chunks

def chunk_text(text: str, metadata: dict):
    words = text.split()
    chunks = []

    target_words = 4500
    overlap_words = 600

    start = 0
    idx = 0
    total_words = len(words)

    while start < total_words:
        end = min(start + target_words, total_words)

        chunks.append({
            "text": " ".join(words[start:end]),
            "metadata": {
                **metadata,
                "chunk_index": idx,
                "word_range": f"{start}-{end}"
            }
        })

        idx += 1
        if end == total_words:
            break
        start = end - overlap_words

    return chunks


if __name__ == "__main__":
    print("Starting full ingestion...")

    text = "This policy defines how interns are evaluated and selected. " * 100
    meta = {
        "doc_id": "policy_001",
        "doc_title": "Intern Evaluation Policy",
        "section": "Overview"
    }

    chunks = chunk_text(text, meta)
    upsert_chunks(chunks)

    print("✅ Ingestion + vector upsert completed")
