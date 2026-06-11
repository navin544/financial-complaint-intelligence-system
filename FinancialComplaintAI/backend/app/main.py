from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import classify, summarize, chat, health
from app.core.config import settings

app = FastAPI(
    title="Financial Complaint Intelligence API",
    description="RAG-powered complaint classification, summarization and chat",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,   prefix="/api/v1", tags=["Health"])
app.include_router(classify.router, prefix="/api/v1", tags=["Classification"])
app.include_router(summarize.router,prefix="/api/v1", tags=["Summarization"])
app.include_router(chat.router,     prefix="/api/v1", tags=["RAG Chat"])

@app.on_event("startup")
async def startup():
    from app.services.rag_service import rag_service
    await rag_service.initialize()
    print("✅  FAISS index loaded. Server ready.")
