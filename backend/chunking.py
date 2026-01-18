from typing import List
import tiktoken

ENC = tiktoken.get_encoding("cl100k_base")

def chunk_text(
    text: str,
    metadata: dict,
    chunk_size: int = 900,
    overlap: int = 150
) -> List[dict]:
    tokens = ENC.encode(text)
    chunks = []

    start = 0
    position = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = ENC.decode(chunk_tokens)

        chunks.append({
            "text": chunk_text,
            "metadata": {
                **metadata,
                "position": position
            }
        })

        position += 1
        start += chunk_size - overlap

    return chunks
