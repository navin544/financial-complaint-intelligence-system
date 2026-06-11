import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "llm_ready" in data

def test_unauthorized_access():
    response = client.post("/api/v1/classify", json={"text": "test complaint"})
    assert response.status_code == 403 # Missing API Key
