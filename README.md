# 📚 Mini RAG System – Policy Question Answering

A lightweight, production-style **Retrieval-Augmented Generation (RAG)** system for answering questions over policy documents with transparent retrieval, citations, and confidence estimation.

This project demonstrates a **real-world RAG pipeline** while remaining deployable on **free-tier cloud platforms**.

---

## 🔗 Live Demo

🌐 **Live Application**  
👉 https://mini-rag-policy-qa.onrender.com/ui/

> ⚠️ The live deployment runs in **Lite Mode** to remain memory-safe on free-tier hosting.

---

## 👤 Author

**Ashish Ranjan**  
- GitHub: https://github.com/imaashu0486  
- Resume: https://drive.google.com/file/d/1saJAWGx4y5ueEf-mXXW_Z-6jkaIHAnpP/view?usp=sharing  

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





# Mini RAG System – Policy Question Answering

## Overview
This project implements a minimal Retrieval-Augmented Generation (RAG) system for answering questions over policy documents.  
The system retrieves relevant document chunks, reranks them, and generates grounded answers with explicit citations.

The design prioritizes correctness, transparency, and alignment with real-world RAG workflows.

---

## Architecture
The end-to-end query flow is:

Query → Vector Retrieval → Reranking → Answer Generation → Citations

### Components
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector Database**: Qdrant
- **Retriever**: Top-K cosine similarity search
- **Reranker**: Cross-Encoder (`ms-marco-MiniLM-L-6-v2`)
- **Answering**: Context-grounded extractive answering
- **Backend**: FastAPI
- **Frontend**: Static HTML (served via FastAPI)

---

## Document Ingestion
- Documents are split into overlapping chunks before embedding
- Each chunk stores metadata:
  - Document title
  - Section name
  - Chunk index
- Chunks and embeddings are stored in Qdrant

---

## Retrieval & Reranking
1. A user query is embedded
2. Top-K relevant chunks are retrieved from Qdrant
3. Retrieved chunks are reranked using a cross-encoder
4. The highest-ranked chunks are used for answering

---

## Answer Generation
- Answers are generated strictly from retrieved context
- Each answer includes inline citations
- A confidence threshold is applied to handle no-answer cases
- If no relevant context is found, the system responds:
  > *No relevant information found in the provided documents.*

This prevents hallucination and ensures document grounding.

---

## API Endpoints

### Health Check

```bash
GET/health
```

- This endpoint verifies that the backend service is running and reachable.

### Ask a Question

```bash
POST /ask

- Answers are generated only from retrieved document context
- Citations map directly to the source document and chunk
- Latency is returned for transparency

## Frontend

- A lightweight web interface is provided for querying the system
- Features:
-      Question input box
-      Answer display panel
-      Explicit citations
-      Response latency
- The frontend is served directly by FastAPI at the root path (/)

## Running Locally

### Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant

### Start Backend

```bash
uvicorn backend.app:app --reload

- Open in browser:
```bash
http://127.0.0.1:8000

##Configuration

- Environment variables supported:
-         QDRANT_URL
-         QDRANT_COLLECTION
- Defaults are provided for local development

## Evaluation Queries (Examples)

- 1.How are interns evaluated?
- 2.Which document defines intern selection?
- 3.Is performance mentioned in the policy?
- 4.Are document sections preserved for citation?
- 5.What happens if the answer is not present in the documents?

## Notes

- Local Qdrant is used for development and testing
- The architecture follows a standard production-style RAG pipeline
- Design choices prioritize reliability, traceability, and grounded responses over speculative generation
