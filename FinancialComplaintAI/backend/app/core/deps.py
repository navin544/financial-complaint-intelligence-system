from fastapi import Request, HTTPException
from app.services.rag_service import rag_service

def get_fraud_model(request: Request):
    model = getattr(request.app.state, "fraud_model", None)
    if model is None:
        raise HTTPException(status_code=503, detail="Fraud model not loaded")
    return model

def get_rag_service():
    if not rag_service.is_ready:
        raise HTTPException(status_code=503, detail="RAG service initializing")
    return rag_service
