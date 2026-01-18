# 📚 Mini RAG System – Policy Question Answering

A lightweight, production-style **Retrieval-Augmented Generation (RAG)** system for answering questions over policy documents with transparent retrieval, citations, and confidence estimation.

This project demonstrates a **real-world RAG pipeline** while remaining deployable on **free-tier cloud platforms**.

---

## 🔗 Live Demo

🌐 **Live Application**  
👉 https://mini-rag-policy-qa.onrender.com/ui/

> ⚠️ The live deployment runs in **Lite Mode** to remain memory-safe on free-tier hosting.

---

## 🧠 Project Overview

This system allows users to:
- Ingest policy documents
- Ask natural language questions
- Retrieve relevant document chunks
- View supporting evidence with citations
- See confidence estimation for each answer

The design focuses on **correctness, transparency, and deployment realism** rather than black-box generation.

---

## 🏗️ System Architecture
User Query
->
Embedding
->
Qdrant Vector Search
->
Reranking (Full Mode)
->
Context Selection
->
Answer Generation
->
Citations + Confidence


---

## ⚙️ Core Components

### Backend
- **Framework**: FastAPI
- **Vector Database**: Qdrant
- **Chunking**: Overlapping text chunks
- **Retrieval**: Cosine similarity search
- **Reranking**: Cross-Encoder (local mode)
- **Answering**: Context-grounded generation

### Frontend
- Static HTML served via FastAPI
- Features:
  - Document ingestion
  - Question answering
  - Retrieved chunk viewer
  - Highlighted supporting sentences
  - Confidence indicator

---

## 📄 Document Ingestion

- Documents are split into overlapping chunks
- Each chunk stores metadata:
  - Document title
  - Source
  - Chunk position
- Embeddings are generated and stored in Qdrant
- Ingestion is available via the `/ingest` endpoint

---

## 🔍 Retrieval & Answer Generation

1. User query is embedded
2. Top-K chunks are retrieved from Qdrant
3. Chunks are reranked (Full Mode only)
4. Answer is generated **only from retrieved context**
5. Inline citations are detected
6. Confidence is computed:
   - **High** → Answer grounded in retrieved chunks
   - **Low** → Weak grounding
   - **None** → No relevant information found

This prevents hallucination and ensures explainability.

---

## 🚦 Deployment Modes

### ✅ Full Mode (Local / Development)

- Uses `sentence-transformers`
- Uses cross-encoder reranker
- Best answer quality
- Recommended for local testing

```env
DEPLOYMENT_MODE=full
```
### Lite Mode (Production / Free Tier)

- Uses deterministic mock embeddings
- No heavy ML models loaded
- Memory-safe for Render / Vercel
- Preserves full RAG workflow logic

```env
DEPLOYMENT_MODE=full
```
- Lite mode exists intentionally to handle real-world cloud constraints.

## 🌐 API Endpoints

| Method | Endpoint  | Description     |
| ------ | --------- | --------------- |
| GET    | `/health` | Health check    |
| POST   | `/ingest` | Ingest document |
| POST   | `/query`  | Ask a question  |
| GET    | `/ui/`    | Web interface   |

## 🧪 Example Queries

- How are interns evaluated?
- Which document defines the selection policy?
- Is performance mentioned in the policy?
- What happens if the answer is not present?


## 🧯 Safety & Reliability

- Prevents hallucinations by refusing unsupported answers
- Ensures vector dimension consistency
- Handles empty or weak retrieval gracefully
- Avoids API quota failures in production

## 🚀 Running Locally

# 1️⃣ Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```
# 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
# 3️⃣ Run Backend
'''bash
uvicorn backend.app:app --reload
```
Open in browser:
```bash
http://127.0.0.1:8000/ui/
```

## 📌 Design Decisions

- Explicit separation of Full vs Lite execution
- Fixed embedding dimension to prevent schema mismatch
- Explainability prioritized over speculative generation
- Built for clarity and robustness, not shortcuts

## ⚠️ Known Limitations

- Lite mode uses mock embeddings (deployment trade-off)
- No authentication layer (out of scope)
- Single collection assumed per deployment

These trade-offs are intentional and documented

## 👤 Author

**Ashish Ranjan**  
- GitHub: https://github.com/imaashu0486  
- Resume: https://drive.google.com/file/d/1saJAWGx4y5ueEf-mXXW_Z-6jkaIHAnpP/view?usp=sharing  


