from pydantic import BaseModel
from typing import Optional, List

class ComplaintRequest(BaseModel):
    text: str
    complaint_id: Optional[str] = None

class ClassificationResponse(BaseModel):
    complaint_id: Optional[str]
    category: str
    confidence: float
    reasoning: str
    processing_time_ms: float

class SummaryResponse(BaseModel):
    complaint_id: Optional[str]
    original_length: int
    summary: str
    key_issues: List[str]
    sentiment: str
    urgency_level: str
    processing_time_ms: float

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    llm_ready: bool
    index_loaded: bool
    total_documents: int
