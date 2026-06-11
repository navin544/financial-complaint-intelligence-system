from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
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
    api_key: str = Field(..., description="API_KEY must be set in .env")

    @field_validator('api_key')
    @classmethod
    def check_api_key(cls, v):
        if not v or v == "your_secure_api_key_here":
            raise ValueError("Invalid or missing API_KEY. Please set a real API_KEY in the .env file.")
        return v

    @property
    def category_list(self) -> List[str]:
        return [c.strip() for c in self.categories.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()
