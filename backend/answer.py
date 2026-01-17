from backend.retrieve import retrieve_chunks
from backend.rerank import rerank_chunks
from backend.context_builder import build_context
from backend.answer_generator import generate_answer


def get_relevant_context(query: str):
    retrieved = retrieve_chunks(query, top_k=10)
    reranked = rerank_chunks(query, retrieved, top_n=5)
    return reranked


if __name__ == "__main__":
    query = "How are interns evaluated?"

    chunks = get_relevant_context(query)
    context_text, citations = build_context(chunks)
    answer = generate_answer(query, context_text, max_sentences=2)

    print("\nANSWER:\n")
    print(answer)

    print("\nCITATIONS:\n")
    for c in citations:
        print(
            f"[{c['id']}] {c['source']} – "
            f"Section: {c['section']} – "
            f"Chunk {c['chunk_index']}"
        )
