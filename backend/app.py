from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time

from backend.retrieve import retrieve_chunks
from backend.rerank import rerank_chunks
from backend.context_builder import build_context
from backend.answer_generator import generate_answer

# Create app
app = FastAPI(title="Mini RAG")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve frontend
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QueryRequest):
    start = time.time()

    retrieved = retrieve_chunks(req.question, top_k=10)
    reranked = rerank_chunks(req.question, retrieved, top_n=5)

    # No-answer handling
    if not reranked or reranked[0]["score"] < 3.0:
        return {
            "question": req.question,
            "answer": "No relevant information found in the provided documents.",
            "citations": [],
            "latency_ms": int((time.time() - start) * 1000)
        }

    context_text, citations = build_context(reranked)
    answer = generate_answer(req.question, context_text, max_sentences=2)

    return {
        "question": req.question,
        "answer": answer,
        "citations": citations,
        "latency_ms": int((time.time() - start) * 1000)
    }

@app.get("/health")
def health():
    return {"status": "ok"}
