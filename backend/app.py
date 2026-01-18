from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uuid
import time

from backend.chunking import chunk_text
from backend.vector_store import upsert_chunks
from backend.retrieve import retrieve
from backend.rerank import rerank_chunks
from backend.answer_generator import generate_answer

app = FastAPI(title="Mini RAG")

LAST_DOCUMENT = {}

# ---------- HELPERS ----------

def extract_supporting_sentence(answer: str, text: str):
    for sentence in text.split("."):
        s = sentence.strip()
        if s and s.lower() in answer.lower():
            return s
    return None

# ---------- MIDDLEWARE ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- MODELS ----------

class IngestRequest(BaseModel):
    text: str
    source: str
    title: str

class QueryRequest(BaseModel):
    question: str

# ---------- INGEST ----------

@app.post("/ingest")
def ingest(req: IngestRequest):
    global LAST_DOCUMENT

    doc_id = str(uuid.uuid4())

    LAST_DOCUMENT = {
        "title": req.title,
        "source": req.source,
        "text": req.text
    }

    chunks = chunk_text(
        text=req.text,
        metadata={
            "doc_id": doc_id,
            "source": req.source,
            "title": req.title,
        },
    )

    upsert_chunks(chunks)

    return {
        "status": "ingested",
        "doc_id": doc_id,
        "chunks_created": len(chunks),
    }

# ---------- QUERY (FULL METRICS + HIGHLIGHT + CONFIDENCE) ----------

@app.post("/query")
def query(req: QueryRequest):
    start_total = time.time()

    # ---- Retrieval ----
    t1 = time.time()
    retrieved = retrieve(req.question)
    t2 = time.time()

    # ---- Rerank ----
    reranked = rerank_chunks(req.question, retrieved)
    t3 = time.time()

    # ---- Build contexts ----
    contexts = []
    for i, c in enumerate(reranked):
        contexts.append({
            "id": i + 1,
            "text": c["text"],
            "title": c.get("title"),
            "source": c.get("source"),
            "position": c.get("position"),
            "used_in_answer": False,
            "highlight": None
        })

    # ---- LLM ----
    answer = generate_answer(req.question, contexts)
    t4 = time.time()

    # ---- Citation + sentence highlight (explicit citations) ----
    for c in contexts:
        if f"[{c['id']}]" in answer:
            c["used_in_answer"] = True
            c["highlight"] = extract_supporting_sentence(answer, c["text"])

    # ---- Fallback: sentence-level grounding across all chunks ----
    if not any(c["used_in_answer"] for c in contexts):
        for c in contexts:
            for sentence in c["text"].split("."):
                s = sentence.strip()
                if s and s.lower() in answer.lower():
                    c["used_in_answer"] = True
                    c["highlight"] = s
                    break
            if c["used_in_answer"]:
                break

    # ---- Confidence ----
    if "i don't know" in answer.lower():
        confidence = "None"
    elif any(c["used_in_answer"] for c in contexts):
        confidence = "High"
    else:
        confidence = "Low"

    # ---- Metrics ----
    metrics = {
        "retrieval_ms": int((t2 - t1) * 1000),
        "rerank_ms": int((t3 - t2) * 1000),
        "llm_ms": int((t4 - t3) * 1000),
        "total_ms": int((t4 - start_total) * 1000),
        "retrieved_chunks": len(retrieved),
        "reranked_chunks": len(contexts),
        "cited_chunks": sum(1 for c in contexts if c["used_in_answer"])
    }

    return {
        "answer": answer,
        "confidence": confidence,
        "metrics": metrics,
        "sources": contexts,
        "retrieved_chunks": contexts
    }

# ---------- UTILS ----------

@app.get("/document")
def get_document():
    return LAST_DOCUMENT

@app.get("/")
def root():
    return RedirectResponse(url="/ui")

# ---------- FRONTEND ----------

app.mount("/ui", StaticFiles(directory="backend/static", html=True), name="static")
