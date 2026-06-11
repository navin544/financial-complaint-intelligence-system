from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not rag_service.is_ready:
        raise HTTPException(503, "Service initializing, please retry.")
    answer, sources, ms = rag_service.chat(req.query, req.history)
    return ChatResponse(answer=answer, sources=sources, processing_time_ms=ms)
