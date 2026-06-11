from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from app.models.fraud_model import FraudEnsemble, get_risk_level, get_recommendation
from app.core.deps import get_fraud_model, get_rag_service
from app.core.auth import verify_api_key
from app.core.limiter import limiter
from app.db.database import get_db
from app.db.models import TransactionRecord
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import json

router = APIRouter()

class TransactionRequest(BaseModel):
    transaction_id: str | None = None
    amount: float = Field(..., gt=0, lt=10000000)
    sender_id: str = Field(..., min_length=3)
    receiver_id: str | None = None
    is_new_beneficiary: int = 0
    device_changed: int = 0
    location_anomaly: int = 0

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

class FraudResponse(BaseModel):
    transaction_id: str
    fraud_probability: float
    risk_level: str
    recommendation: str
    is_fraud: bool
    timestamp: str
    top_risk_factors: list[str] = []

class FraudResponseWithContext(FraudResponse):
    related_complaints: list[str] = []

@router.post("/predict", response_model=FraudResponse)
@limiter.limit("30/minute")
async def predict(
    txn: TransactionRequest, 
    request: Request,
    api_key: str = Depends(verify_api_key),
    model: FraudEnsemble = Depends(get_fraud_model),
    db: Session = Depends(get_db)
):
    # Simulated feature engineering
    features = [txn.amount, txn.is_new_beneficiary, txn.device_changed, txn.location_anomaly]
    
    prob = model.predict_proba(features)
    risk_level = get_risk_level(prob)
    recommendation = get_recommendation(risk_level)
    factors = model.get_risk_factors(features)
    is_fraud = prob > 0.5
    
    tid = txn.transaction_id or f"TXN_{uuid.uuid4().hex[:8].upper()}"
    
    # Save to DB
    record = TransactionRecord(
        id=tid,
        sender_id=txn.sender_id,
        receiver_id=txn.receiver_id or "UNKNOWN",
        amount=txn.amount,
        risk_level=risk_level,
        fraud_probability=prob,
        is_fraud=is_fraud,
        risk_factors=json.dumps(factors)
    )
    db.add(record)
    db.commit()
    
    return FraudResponse(
        transaction_id=tid,
        fraud_probability=prob,
        risk_level=risk_level,
        recommendation=recommendation,
        is_fraud=is_fraud,
        timestamp=datetime.utcnow().isoformat(),
        top_risk_factors=factors
    )

@router.post("/predict-with-context", response_model=FraudResponseWithContext)
@limiter.limit("20/minute")
async def predict_with_context(
    txn: TransactionRequest,
    request: Request,
    api_key: str = Depends(verify_api_key),
    model: FraudEnsemble = Depends(get_fraud_model),
    rag = Depends(get_rag_service),
    db: Session = Depends(get_db)
):
    # Basic prediction
    res = await predict(txn, request, api_key, model, db)
    
    complaint_context = []
    if res.risk_level in ("CRITICAL", "HIGH", "MEDIUM"):
        # Query RAG for related complaints
        query = f"UPI fraud complaints involving {txn.sender_id} or {txn.receiver_id or 'unknown'}"
        answer, sources, _ = await rag.chat(query, [])
        complaint_context = [f"Context from RAG: {answer[:200]}..."]
        
    return FraudResponseWithContext(
        **res.model_dump(),
        related_complaints=complaint_context
    )
