from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time

from backend.retrieve import retrieve_chunks
from backend.rerank import rerank_chunks
from backend.context_builder import build_context
from backend.answer_generator import generate_answer

app = FastAPI(title="Mini RAG")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

import os

@app.post("/ask")
def ask_question(req: QueryRequest):
    start = time.time()

    # 🔒 Free-tier / hosted guard
    if os.getenv("RENDER_DEPLOY") == "true":
        return {
            "question": req.question,
            "answer": "Hosted demo runs in lightweight mode due to free-tier memory limits. Full RAG pipeline runs locally.",
            "citations": [],
            "latency_ms": 0,
        }

    try:
        retrieved = retrieve_chunks(req.question, top_k=10)
        reranked = rerank_chunks(req.question, retrieved, top_n=5)

        if (
            not reranked
            or not isinstance(reranked, list)
            or "score" not in reranked[0]
            or reranked[0]["score"] < 3.0
        ):
            return {
                "question": req.question,
                "answer": "No relevant information found in the provided documents.",
                "citations": [],
                "latency_ms": int((time.time() - start) * 1000),
            }

        context_text, citations = build_context(reranked)

        if not context_text:
            return {
                "question": req.question,
                "answer": "No relevant information found in the provided documents.",
                "citations": [],
                "latency_ms": int((time.time() - start) * 1000),
            }

        answer = generate_answer(req.question, context_text, max_sentences=2)

        return {
            "question": req.question,
            "answer": answer,
            "citations": citations,
            "latency_ms": int((time.time() - start) * 1000),
        }

    except Exception:
        return {
            "question": req.question,
            "answer": "Internal processing error.",
            "citations": [],
            "latency_ms": int((time.time() - start) * 1000),
        }

@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ STATIC FILES MUST BE LAST
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")
