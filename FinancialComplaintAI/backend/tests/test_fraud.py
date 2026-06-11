import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
API_KEY = "dev-secret-key-12345"
HEADERS = {"X-API-Key": API_KEY}

def test_predict_fraud_success():
    payload = {
        "amount": 500.0,
        "sender_id": "test@upi",
        "receiver_id": "merchant@upi"
    }
    response = client.post("/api/v1/fraud/predict", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_probability" in data
    assert "risk_level" in data
    assert "top_risk_factors" in data

def test_predict_invalid_amount():
    payload = {
        "amount": -10.0,
        "sender_id": "test@upi"
    }
    response = client.post("/api/v1/fraud/predict", json=payload, headers=HEADERS)
    assert response.status_code == 422 # Validation Error

def test_predict_with_context():
    payload = {
        "amount": 10000.0,
        "sender_id": "victim@upi",
        "receiver_id": "scammer@upi"
    }
    response = client.post("/api/v1/fraud/predict-with-context", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "related_complaints" in data
