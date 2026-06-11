import pandas as pd
import numpy as np
import joblib
import os
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def generate_synthetic_data(n_samples=5000):
    np.random.seed(42)
    # Features: amount, is_new_beneficiary, device_changed, location_anomaly
    
    # Normal transactions
    normal_amount = np.random.lognormal(mean=5, sigma=1, size=n_samples)
    normal_new_ben = np.random.choice([0, 1], p=[0.9, 0.1], size=n_samples)
    normal_dev_chg = np.random.choice([0, 1], p=[0.98, 0.02], size=n_samples)
    normal_loc_anom = np.random.choice([0, 1], p=[0.95, 0.05], size=n_samples)
    
    # Fraud transactions (about 5% of data)
    n_fraud = int(n_samples * 0.05)
    fraud_amount = np.random.lognormal(mean=8, sigma=1.5, size=n_fraud)
    fraud_new_ben = np.random.choice([0, 1], p=[0.2, 0.8], size=n_fraud)
    fraud_dev_chg = np.random.choice([0, 1], p=[0.4, 0.6], size=n_fraud)
    fraud_loc_anom = np.random.choice([0, 1], p=[0.3, 0.7], size=n_fraud)
    
    X_normal = np.column_stack((normal_amount, normal_new_ben, normal_dev_chg, normal_loc_anom))
    y_normal = np.zeros(n_samples)
    
    X_fraud = np.column_stack((fraud_amount, fraud_new_ben, fraud_dev_chg, fraud_loc_anom))
    y_fraud = np.ones(n_fraud)
    
    X = np.vstack((X_normal, X_fraud))
    y = np.concatenate((y_normal, y_fraud))
    
    return X, y

def train_and_save_model():
    print("Generating synthetic fraud data...")
    X, y = generate_synthetic_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    print("Training XGBoost classifier...")
    # Fix for XGBClassifier: handle 5% fraud imbalance with scale_pos_weight=19
    model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, scale_pos_weight=19, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))
    
    os.makedirs("data", exist_ok=True)
    model_path = os.path.join("data", "fraud_model.pkl")
    joblib.dump(model, model_path)
    print(f"✅ Model saved successfully to {model_path}")

if __name__ == "__main__":
    # Run from the backend root directory
    train_and_save_model()
