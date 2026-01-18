import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer(question: str, contexts: list[dict]) -> str:
    """
    contexts = [
      {"id": 1, "text": "...", "source": "..."}
    ]
    """

    if not GROQ_API_KEY:
        return "LLM not configured."

    client = Groq(api_key=GROQ_API_KEY)

    context_block = "\n\n".join(
        f"[{c['id']}] {c['text']}" for c in contexts
    )

    system_prompt = (
        "Answer ONLY using the provided context.\n"
        "If the answer is not present, say 'I don't know'.\n"
        "Use inline citations like [1], [2]."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context_block}\n\nQuestion:\n{question}"
            },
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
