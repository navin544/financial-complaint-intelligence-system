from fastapi import APIRouter, HTTPException
from app.models.schemas import ComplaintRequest, ClassificationResponse
from app.services.rag_service import rag_service
import uuid

router = APIRouter()

@router.post("/classify", response_model=ClassificationResponse)
async def classify_complaint(req: ComplaintRequest):
    if not rag_service.is_ready:
        raise HTTPException(503, "Service initializing, please retry.")
    if not req.text.strip():
        raise HTTPException(400, "Complaint text is empty.")
    category, confidence, reasoning, ms = rag_service.classify(req.text)
    return ClassificationResponse(
        complaint_id=req.complaint_id or str(uuid.uuid4())[:8],
        category=category,
        confidence=confidence,
        reasoning=reasoning,
        processing_time_ms=ms,
    )
