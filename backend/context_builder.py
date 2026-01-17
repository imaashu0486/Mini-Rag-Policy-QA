def build_context(chunks: list[dict]) -> tuple[str, list[dict]]:
    """
    Build context text and citation map
    """
    context_blocks = []
    citations = []

    for idx, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"[{idx}] {chunk['text']}"
        )
        citations.append({
            "id": idx,
            "source": chunk["metadata"].get("doc_title", "Unknown"),
            "section": chunk["metadata"].get("section", "N/A"),
            "chunk_index": chunk["metadata"].get("chunk_index")
        })

    return "\n\n".join(context_blocks), citations
