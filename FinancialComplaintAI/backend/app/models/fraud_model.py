import joblib
import os
import hashlib
import numpy as np
from typing import Dict, Any

class FraudEnsemble:
    def __init__(self, model_path: str = None):
        self.model = None
        self.model_hash = None
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def load_model(self, path: str):
        # Integrity check
        with open(path, "rb") as f:
            self.model_hash = hashlib.sha256(f.read()).hexdigest()
        
        self.model = joblib.load(path)
        print(f"✅ Fraud model loaded. Hash: {self.model_hash}")

    def predict_proba(self, features: np.ndarray) -> float:
        if self.model is None:
            # Fallback/Mock logic for dev
            return float(np.random.uniform(0.01, 0.99))
        return self.model.predict_proba(features)[0][1]

    def get_risk_factors(self, features: np.ndarray) -> list:
        # Mock SHAP-like factors
        factors = ["High Velocity", "New Beneficiary", "Location Anomaly", "Large Amount", "Night Transaction"]
        return list(np.random.choice(factors, 3, replace=False))

def get_risk_level(prob: float) -> str:
    if prob > 0.8: return "CRITICAL"
    if prob > 0.5: return "HIGH"
    if prob > 0.2: return "MEDIUM"
    return "LOW"

def get_recommendation(risk_level: str) -> str:
    if risk_level in ("CRITICAL", "HIGH"): return "BLOCK & REVIEW"
    if risk_level == "MEDIUM": return "FLAG for SMS Verification"
    return "ALLOW"
