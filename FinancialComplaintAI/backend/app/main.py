from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import complaints, fraud
from app.core.config import settings
from app.core.logging import logger
from app.core.limiter import limiter
from contextlib import asynccontextmanager
from app.db.database import engine, Base
from app.models.fraud_model import FraudEnsemble
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize RAG
    from app.services.rag_service import rag_service
    await rag_service.initialize()
    logger.info("✅ RAG service loaded.")
    
    # Initialize Fraud Model
    model_path = os.path.join("data", "fraud_model.pkl")
    app.state.fraud_model = FraudEnsemble(model_path)
    logger.info("✅ Fraud ensemble loaded (or using dev mock).")
    
    yield
    app.state.fraud_model = None

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UPI Intelligence Platform",
    description="Unified Fraud Detection + Financial Complaint Analysis",
    version="2.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.0.2.2",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fraud.router,      prefix="/api/v1/fraud",      tags=["Fraud Detection"])
app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["Complaint Intelligence"])
