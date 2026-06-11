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
