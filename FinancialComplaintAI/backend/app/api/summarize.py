from fastapi import APIRouter, HTTPException
from app.models.schemas import ComplaintRequest, SummaryResponse
from app.services.rag_service import rag_service
import uuid

router = APIRouter()

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_complaint(req: ComplaintRequest):
    if not rag_service.is_ready:
        raise HTTPException(503, "Service initializing, please retry.")
    if not req.text.strip():
        raise HTTPException(400, "Complaint text is empty.")
    data, ms = rag_service.summarize(req.text)
    return SummaryResponse(
        complaint_id=req.complaint_id or str(uuid.uuid4())[:8],
        original_length=len(req.text),
        summary=data.get("summary", "Summary unavailable."),
        key_issues=data.get("key_issues", []),
        sentiment=data.get("sentiment", "Unknown"),
        urgency_level=data.get("urgency_level", "Medium"),
        processing_time_ms=ms,
    )
