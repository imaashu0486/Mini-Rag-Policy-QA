def generate_answer(question: str, context: str, max_sentences: int = 3) -> str:
    """
    Generate a concise, grounded answer by extracting
    and deduplicating relevant sentences from context.
    """

    sentences = []
    seen = set()

    # Split context into sentences
    for block in context.split("\n\n"):
        for sent in block.split("."):
            sent = sent.strip()
            if len(sent) < 20:
                continue

            key = sent.lower()
            if key not in seen:
                seen.add(key)
                sentences.append(sent)

            if len(sentences) >= max_sentences:
                break
        if len(sentences) >= max_sentences:
            break

    if not sentences:
        return (
            "The provided documents do not contain enough information "
            "to answer this question confidently."
        )

    return ". ".join(sentences) + "."
