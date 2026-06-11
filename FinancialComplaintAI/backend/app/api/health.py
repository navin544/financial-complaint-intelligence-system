from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok" if rag_service.is_ready else "initializing",
        llm_ready=rag_service.is_ready,
        index_loaded=rag_service.vectorstore is not None,
        total_documents=rag_service.doc_count,
    )
