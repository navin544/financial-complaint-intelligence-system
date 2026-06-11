from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service
from app.core.auth import verify_api_key
from app.core.limiter import limiter

router = APIRouter()

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
