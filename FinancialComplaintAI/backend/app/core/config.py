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
    api_key: str = "dev-secret-key-12345"

    @property
    def category_list(self) -> List[str]:
        return [c.strip() for c in self.categories.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()
