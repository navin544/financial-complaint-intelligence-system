"""
generate_backend.py
Generates all FastAPI + RAG + FAISS backend files for the Financial Complaint Intelligence System.
Usage: python generate_backend.py <output_dir>
"""

import os, sys, textwrap

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip())
    print(f"  + {path}")

def generate(root):

    # ── requirements.txt ───────────────────────────────────────────────────────
    write(f"{root}/requirements.txt", """
        fastapi==0.111.0
        uvicorn[standard]==0.30.1
        langchain==0.2.5
        langchain-community==0.2.5
        langchain-huggingface==0.0.3
        faiss-cpu==1.8.0
        sentence-transformers==3.0.1
        transformers==4.41.2
        torch==2.3.1
        huggingface-hub==0.23.4
        pydantic==2.7.4
        python-multipart==0.0.9
        pandas==2.2.2
        numpy==1.26.4
        python-dotenv==1.0.1
        httpx==0.27.0
        ollama==0.2.1
    """)

    # ── .env ──────────────────────────────────────────────────────────────────
    write(f"{root}/.env", """
        # Backend Config
        APP_HOST=0.0.0.0
        APP_PORT=8000
        DEBUG=True

        # Model Config  (Ollama runs locally — no API key needed)
        OLLAMA_BASE_URL=http://localhost:11434
        LLM_MODEL=llama3

        # Embedding Model (downloaded from HuggingFace automatically)
        EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

        # FAISS Index
        FAISS_INDEX_PATH=data/faiss_index
        COMPLAINTS_CSV=data/complaints.csv

        # Classification Labels
        CATEGORIES=Credit Card,Mortgage,Student Loan,Bank Account,Debt Collection,Credit Reporting,Money Transfer,Payday Loan,Vehicle Loan
    """)

    # ── app/__init__.py ───────────────────────────────────────────────────────
    write(f"{root}/app/__init__.py", "")

    # ── app/main.py ───────────────────────────────────────────────────────────
    write(f"{root}/app/main.py", '''
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
    ''')

    # ── app/core/config.py ────────────────────────────────────────────────────
    write(f"{root}/app/core/config.py", '''
        from pydantic_settings import BaseSettings
        from typing import List

        class Settings(BaseSettings):
            app_host: str = "0.0.0.0"
            app_port: int = 8000
            debug: bool = True
            ollama_base_url: str = "http://localhost:11434"
            llm_model: str = "llama3"
            embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
            faiss_index_path: str = "data/faiss_index"
            complaints_csv: str = "data/complaints.csv"
            categories: str = (
                "Credit Card,Mortgage,Student Loan,Bank Account,"
                "Debt Collection,Credit Reporting,Money Transfer,"
                "Payday Loan,Vehicle Loan"
            )

            @property
            def category_list(self) -> List[str]:
                return [c.strip() for c in self.categories.split(",")]

            class Config:
                env_file = ".env"

        settings = Settings()
    ''')

    # ── app/models/schemas.py ─────────────────────────────────────────────────
    write(f"{root}/app/models/schemas.py", '''
        from pydantic import BaseModel
        from typing import Optional, List

        class ComplaintRequest(BaseModel):
            text: str
            complaint_id: Optional[str] = None

        class ClassificationResponse(BaseModel):
            complaint_id: Optional[str]
            category: str
            confidence: float
            reasoning: str
            processing_time_ms: float

        class SummaryResponse(BaseModel):
            complaint_id: Optional[str]
            original_length: int
            summary: str
            key_issues: List[str]
            sentiment: str
            urgency_level: str
            processing_time_ms: float

        class ChatMessage(BaseModel):
            role: str
            content: str

        class ChatRequest(BaseModel):
            query: str
            history: Optional[List[ChatMessage]] = []

        class ChatResponse(BaseModel):
            answer: str
            sources: List[str]
            processing_time_ms: float

        class HealthResponse(BaseModel):
            status: str
            llm_ready: bool
            index_loaded: bool
            total_documents: int
    ''')

    # ── app/services/rag_service.py ───────────────────────────────────────────
    write(f"{root}/app/services/rag_service.py", '''
        """
        Core RAG service: loads FAISS index, runs LLM via Ollama/LangChain.
        Handles classification, summarization, and chat.
        """
        import time, os, asyncio
        from typing import List, Tuple
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.llms import Ollama
        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        from app.core.config import settings

        CLASSIFY_PROMPT = PromptTemplate(
            input_variables=["complaint", "categories"],
            template="""
        You are a financial complaint classifier.

        Complaint:
        {complaint}

        Available categories: {categories}

        Respond ONLY with valid JSON (no markdown):
        {{
          "category": "<one of the categories above>",
          "confidence": <0.0-1.0>,
          "reasoning": "<one sentence>"
        }}
        """
        )

        SUMMARIZE_PROMPT = PromptTemplate(
            input_variables=["complaint"],
            template="""
        You are a financial analyst. Analyze this complaint and respond ONLY with valid JSON:

        Complaint:
        {complaint}

        {{
          "summary": "<2-3 sentence summary>",
          "key_issues": ["<issue1>", "<issue2>"],
          "sentiment": "Positive|Neutral|Negative|Very Negative",
          "urgency_level": "Low|Medium|High|Critical"
        }}
        """
        )

        RAG_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template="""
        You are a helpful financial complaint analyst.
        Use the following complaint records to answer the question.

        Context:
        {context}

        Question: {question}

        Provide a clear, helpful answer based on the complaint data.
        """
        )


        class RAGService:
            def __init__(self):
                self.vectorstore = None
                self.embeddings = None
                self.llm = None
                self.qa_chain = None
                self._ready = False

            async def initialize(self):
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self._load_sync)

            def _load_sync(self):
                print("⏳  Loading embedding model...")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=settings.embedding_model,
                    model_kwargs={"device": "cpu"},
                )

                index_path = settings.faiss_index_path
                if os.path.exists(index_path):
                    print("⏳  Loading FAISS index from disk...")
                    self.vectorstore = FAISS.load_local(
                        index_path, self.embeddings, allow_dangerous_deserialization=True
                    )
                else:
                    print("⚠️   FAISS index not found — run index_builder.py first")
                    return

                print("⏳  Connecting to Ollama (llama3)...")
                self.llm = Ollama(
                    base_url=settings.ollama_base_url,
                    model=settings.llm_model,
                    temperature=0.1,
                )

                retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=retriever,
                    chain_type_kwargs={"prompt": RAG_PROMPT},
                    return_source_documents=True,
                )
                self._ready = True
                print("✅  RAG service ready.")

            @property
            def is_ready(self) -> bool:
                return self._ready

            @property
            def doc_count(self) -> int:
                if self.vectorstore:
                    return self.vectorstore.index.ntotal
                return 0

            def classify(self, text: str) -> Tuple[str, float, str, float]:
                t0 = time.time()
                prompt = CLASSIFY_PROMPT.format(
                    complaint=text[:2000],
                    categories=", ".join(settings.category_list),
                )
                raw = self.llm(prompt)
                import json, re
                try:
                    m = re.search(r"\\{.*\\}", raw, re.DOTALL)
                    data = json.loads(m.group()) if m else {}
                except Exception:
                    data = {}
                return (
                    data.get("category", "Unknown"),
                    float(data.get("confidence", 0.5)),
                    data.get("reasoning", ""),
                    (time.time() - t0) * 1000,
                )

            def summarize(self, text: str) -> Tuple[dict, float]:
                t0 = time.time()
                prompt = SUMMARIZE_PROMPT.format(complaint=text[:3000])
                raw = self.llm(prompt)
                import json, re
                try:
                    m = re.search(r"\\{.*\\}", raw, re.DOTALL)
                    data = json.loads(m.group()) if m else {}
                except Exception:
                    data = {}
                return data, (time.time() - t0) * 1000

            def chat(self, query: str, history: list) -> Tuple[str, List[str], float]:
                t0 = time.time()
                result = self.qa_chain({"query": query})
                answer = result.get("result", "I could not find relevant information.")
                sources = [
                    doc.metadata.get("complaint_id", "N/A")
                    for doc in result.get("source_documents", [])
                ]
                return answer, sources, (time.time() - t0) * 1000


        rag_service = RAGService()
    ''')

    # ── app/services/index_builder.py ─────────────────────────────────────────
    write(f"{root}/app/services/index_builder.py", '''
        """
        Build FAISS index from complaints CSV.
        Run once: python -m app.services.index_builder
        """
        import pandas as pd
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain.docstore.document import Document
        from app.core.config import settings
        import os

        def build_index():
            csv = settings.complaints_csv
            if not os.path.exists(csv):
                print(f"❌  CSV not found: {csv}")
                return

            print(f"📂  Loading {csv}...")
            df = pd.read_csv(csv).fillna("")
            print(f"   {len(df)} complaints loaded.")

            docs = []
            for _, row in df.iterrows():
                content = row.get("complaint_text", row.get("Consumer complaint narrative", ""))
                if not content.strip():
                    continue
                docs.append(Document(
                    page_content=content[:1000],
                    metadata={
                        "complaint_id": str(row.get("Complaint ID", row.name)),
                        "product": row.get("Product", "Unknown"),
                        "issue": row.get("Issue", ""),
                        "state": row.get("State", ""),
                    }
                ))

            print(f"⏳  Building FAISS index for {len(docs)} documents...")
            embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model,
                model_kwargs={"device": "cpu"},
            )
            vectorstore = FAISS.from_documents(docs, embeddings)
            vectorstore.save_local(settings.faiss_index_path)
            print(f"✅  Index saved to {settings.faiss_index_path}")

        if __name__ == "__main__":
            build_index()
    ''')

    # ── app/api/health.py ─────────────────────────────────────────────────────
    write(f"{root}/app/api/health.py", '''
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
    ''')

    # ── app/api/classify.py ───────────────────────────────────────────────────
    write(f"{root}/app/api/classify.py", '''
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
    ''')

    # ── app/api/summarize.py ──────────────────────────────────────────────────
    write(f"{root}/app/api/summarize.py", '''
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
    ''')

    # ── app/api/chat.py ───────────────────────────────────────────────────────
    write(f"{root}/app/api/chat.py", '''
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
    ''')

    # ── app/api/__init__.py ───────────────────────────────────────────────────
    write(f"{root}/app/api/__init__.py", "")

    print(f"\\n✅  Backend files written to {root}/")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "backend"
    generate(root)
