from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.models.schemas import ComplaintRequest, ClassificationResponse
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
