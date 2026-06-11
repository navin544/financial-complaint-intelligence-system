import joblib
import os
import hashlib
import numpy as np
import shap
from typing import Dict, Any

class FraudEnsemble:
    def __init__(self, model_path: str = None):
        self.model = None
        self.model_hash = None
        self.explainer = None
        self.feature_names = ["Amount", "New Beneficiary", "Device Changed", "Location Anomaly"]
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)

    def load_model(self, path: str):
        # Integrity check
        with open(path, "rb") as f:
            self.model_hash = hashlib.sha256(f.read()).hexdigest()
        
        self.model = joblib.load(path)
        
        # Initialize SHAP explainer
        try:
            self.explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            print(f"Warning: Could not initialize SHAP explainer: {e}")
            
        print(f"✅ Fraud model loaded. Hash: {self.model_hash}")

    def predict_proba(self, features: np.ndarray) -> float:
        if self.model is None:
            # Fallback/Mock logic for dev
            return float(np.random.uniform(0.01, 0.99))
        return self.model.predict_proba(features)[0][1]

    def get_risk_factors(self, features: np.ndarray) -> list:
        if self.explainer is None:
            return ["Model Explainability Unavailable"]
            
        try:
            # Calculate SHAP values for the single instance
            shap_values = self.explainer.shap_values(features)
            
            # For XGBoost, shap_values might be a list (for multiclass) or array
            if isinstance(shap_values, list):
                shap_vals = shap_values[1][0] # Get values for positive class
            else:
                shap_vals = shap_values[0]
                
            # Pair feature names with their absolute SHAP values to find biggest contributors
            feature_importance = list(zip(self.feature_names, shap_vals))
            
            # Sort by absolute SHAP value (impact magnitude) descending
            feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
            
            # Return the names of the top 3 contributing factors
            return [name for name, val in feature_importance[:3] if abs(val) > 0.01]
            
        except Exception as e:
            print(f"SHAP Error: {e}")
            return ["Analysis Error"]

def get_risk_level(prob: float) -> str:
    if prob > 0.8: return "CRITICAL"
    if prob > 0.5: return "HIGH"
    if prob > 0.2: return "MEDIUM"
    return "LOW"

def get_recommendation(risk_level: str) -> str:
    if risk_level in ("CRITICAL", "HIGH"): return "BLOCK & REVIEW"
    if risk_level == "MEDIUM": return "FLAG for SMS Verification"
    return "ALLOW"
