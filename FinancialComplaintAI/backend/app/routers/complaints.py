from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.schemas import ComplaintRequest, ClassificationResponse, SummaryResponse, ChatRequest, ChatResponse, HealthResponse
from app.services.rag_service import rag_service
from app.core.auth import verify_api_key
from app.core.limiter import limiter
from app.db.database import get_db
from app.db.models import ComplaintRecord
import uuid

router = APIRouter()

@router.post("/classify", response_model=ClassificationResponse)
@limiter.limit("10/minute")
async def classify_complaint(
    req: ComplaintRequest, 
    request: Request,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    if not rag_service.is_ready:
        raise HTTPException(503, "Service initializing, please retry.")
    if not req.text.strip():
        raise HTTPException(400, "Complaint text is empty.")
    
    category, confidence, reasoning, ms = await rag_service.classify(req.text)
    complaint_id = req.complaint_id or str(uuid.uuid4())[:8]
    
    # Save to DB
    record = ComplaintRecord(
        complaint_id=complaint_id,
        text=req.text,
        category=category,
        confidence=confidence
    )
    db.add(record)
    db.commit()
    
    return ClassificationResponse(
        complaint_id=complaint_id,
        category=category,
        confidence=confidence,
        reasoning=reasoning,
        processing_time_ms=ms,
    )

@router.post("/summarize", response_model=SummaryResponse)
@limiter.limit("10/minute")
async def summarize_complaint(
    req: ComplaintRequest, 
    request: Request,
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    if not rag_service.is_ready:
        raise HTTPException(503, "Service initializing, please retry.")
    if not req.text.strip():
        raise HTTPException(400, "Complaint text is empty.")
    
    data, ms = await rag_service.summarize(req.text)
    complaint_id = req.complaint_id or str(uuid.uuid4())[:8]
    
    # Save to DB
    record = ComplaintRecord(
        complaint_id=complaint_id,
        text=req.text,
        summary=data.get("summary"),
        sentiment=data.get("sentiment"),
        urgency=data.get("urgency_level")
    )
    db.add(record)
    db.commit()
    
    return SummaryResponse(
        complaint_id=complaint_id,
        original_length=len(req.text),
        summary=data.get("summary", "Summary unavailable."),
        key_issues=data.get("key_issues", []),
        sentiment=data.get("sentiment", "Unknown"),
        urgency_level=data.get("urgency_level", "Medium"),
        processing_time_ms=ms,
    )

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat(
    req: ChatRequest, 
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    if not rag_service.is_ready:
        raise HTTPException(503, "Service initializing, please retry.")
    answer, sources, ms = await rag_service.chat(req.query, req.history)
    return ChatResponse(answer=answer, sources=sources, processing_time_ms=ms)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok" if rag_service.is_ready else "initializing",
        llm_ready=rag_service.is_ready,
        index_loaded=rag_service.vectorstore is not None,
        total_documents=rag_service.doc_count,
    )
