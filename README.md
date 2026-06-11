# 🏦 Financial Complaint Intelligence System (FCIS)

**Android App + FastAPI Backend + Llama 3 + LangChain + FAISS**

---

## 🏗️ Architecture

```
Android App (Kotlin + Jetpack Compose)
        │  Retrofit HTTP
        ▼
FastAPI Backend (Python)
  ├── /api/v1/classify    → Llama 3 via Ollama
  ├── /api/v1/summarize   → Llama 3 via Ollama
  └── /api/v1/chat        → LangChain RAG → FAISS → Llama 3
```

```
Tech Stack
├── LLM          : Llama 3 (via Ollama — runs locally, free)
├── Orchestration: LangChain 0.2
├── Vector DB    : FAISS (CPU)
├── Embeddings   : sentence-transformers/all-MiniLM-L6-v2
├── API Server   : FastAPI + Uvicorn
└── Android      : Kotlin · Jetpack Compose · Hilt · Retrofit
```

---

## 📋 Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Java JDK | 17+ | https://adoptium.net/ |
| Python | 3.9+ | https://python.org/ |
| Git | Any | https://git-scm.com/ |
| Android Studio | Hedgehog+ | https://developer.android.com/studio |
| Ollama | Latest | https://ollama.ai/ |

---

## 🚀 Quick Start (3 Steps)

### Step 1 — Install Ollama + Llama 3

```bash
# Download Ollama from https://ollama.ai/
# Then pull Llama 3:
ollama pull llama3
# Verify it works:
ollama run llama3 "Hello"
```

### Step 2 — Run the Backend

```bash
# Clone / extract this project, then:
cd FinancialComplaintAI/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add pydantic-settings (required by config)
pip install pydantic-settings

# Create sample data
cd ..
python setup_sample_data.py backend/data
cd backend

# Build FAISS index (one-time)
python -m app.services.index_builder

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ API docs at: http://localhost:8000/docs

### Step 3 — Run Android App

```bash
# Open Android Studio
# File → Open → select FinancialComplaintAI/android/
# Wait for Gradle sync (first time downloads ~500MB)
# Run on emulator (emulator uses 10.0.2.2 for localhost)
# OR for real device: edit NetworkModule.kt → set BASE_URL to your PC's IP
```

---

## 📁 Project Structure

```
FinancialComplaintAI/
├── BUILD_PROJECT.bat          ← Windows one-click builder
├── generate_backend.py        ← Generates all backend files
├── generate_android.py        ← Generates all Android files
├── setup_sample_data.py       ← Creates sample complaints CSV
│
├── backend/
│   ├── requirements.txt
│   ├── .env
│   └── app/
│       ├── main.py            ← FastAPI app entry
│       ├── core/config.py     ← Settings
│       ├── models/schemas.py  ← Pydantic models
│       ├── api/
│       │   ├── classify.py    ← POST /api/v1/classify
│       │   ├── summarize.py   ← POST /api/v1/summarize
│       │   ├── chat.py        ← POST /api/v1/chat
│       │   └── health.py      ← GET  /api/v1/health
│       └── services/
│           ├── rag_service.py ← Core: FAISS + LangChain + Ollama
│           └── index_builder.py ← One-time FAISS index creation
│
└── android/
    └── app/src/main/
        ├── AndroidManifest.xml
        └── java/com/fcis/app/
            ├── MainActivity.kt
            ├── FCISApplication.kt
            ├── ui/
            │   ├── FCISApp.kt           ← Navigation
            │   ├── theme/Theme.kt       ← Material 3 colors
            │   └── screens/
            │       ├── HomeScreen.kt
            │       ├── ClassifyScreen.kt
            │       ├── SummarizeScreen.kt
            │       └── ChatScreen.kt
            ├── viewmodel/
            │   ├── ClassifyViewModel.kt
            │   ├── SummarizeViewModel.kt
            │   └── ChatViewModel.kt
            └── data/
                ├── model/ApiModels.kt
                ├── network/ApiService.kt
                ├── network/NetworkModule.kt
                └── repository/ComplaintRepository.kt
```

---

## 🔌 API Reference

### Classify a Complaint
```http
POST /api/v1/classify
{"text": "I was charged a $35 fee even though I paid on time..."}

Response:
{
  "category": "Credit Card",
  "confidence": 0.92,
  "reasoning": "Complaint involves unauthorized fee on a credit card account.",
  "processing_time_ms": 1840.5
}
```

### Summarize a Complaint
```http
POST /api/v1/summarize
{"text": "My mortgage servicer applied my payment to the wrong account..."}

Response:
{
  "summary": "Customer's mortgage payment was misapplied...",
  "key_issues": ["Payment misapplication", "Credit bureau error"],
  "sentiment": "Very Negative",
  "urgency_level": "High",
  "processing_time_ms": 2100.3
}
```

### RAG Chat
```http
POST /api/v1/chat
{"query": "What are the most common credit card issues?", "history": []}

Response:
{
  "answer": "Based on the complaint database, the most common credit card issues include...",
  "sources": ["CC-001", "CC-002", "CC-003"],
  "processing_time_ms": 3200.7
}
```

---

## 🔧 Configuration

Edit `backend/.env` to change:
- `LLM_MODEL` — swap to `llama3:70b`, `mistral`, `gemma2`, etc.
- `EMBEDDING_MODEL` — change embeddings model
- `OLLAMA_BASE_URL` — if Ollama runs on a different host
- `CATEGORIES` — add/remove complaint categories

---

## 📱 Android Network Config

| Environment | BASE_URL in NetworkModule.kt |
|-------------|------------------------------|
| Emulator    | `http://10.0.2.2:8000/`      |
| Real Device | `http://YOUR_PC_LAN_IP:8000/`|
| Production  | `https://your-domain.com/`   |

---

## 🛠️ Troubleshooting

**"FAISS index not found"** → Run `python -m app.services.index_builder` first

**"Service initializing"** → Wait 30–60 seconds for models to load on first start

**Ollama connection refused** → Make sure `ollama serve` is running

**Android can't connect** → Check firewall, use correct IP, ensure `usesCleartextTraffic=true` is in manifest

**Slow responses** → Normal for CPU inference; Llama 3 8B takes 5–30s on CPU. Use GPU or llama3:instruct for speed.
