from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    text: str
    source: str
    title: Optional[str] = None

class AskRequest(BaseModel):
    question: str

class Citation(BaseModel):
    id: int
    source: str
    section: str
    chunk_index: int

class AskResponse(BaseModel):
    question: str
    answer: str
    citations: List[Citation]
    latency_ms: int
