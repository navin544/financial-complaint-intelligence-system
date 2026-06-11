import pandas as pd
import numpy as np

def engineer_features(data: dict) -> np.ndarray:
    """
    Center for feature engineering. 
    Input is a single transaction dict. 
    Output is a numpy array ready for the ensemble model.
    """
    df = pd.DataFrame([data])
    
    # Bug fix: Ensure location_anomaly is handled correctly
    df['location_anomaly'] = df.get('location_anomaly', pd.Series(0, index=df.index))
    
    # Feature selection matching the model's expectations
    # In a real system, this would match the training pipeline exactly
    features = [
        df.get('amount', pd.Series(0.0, index=df.index)).iloc[0],
        df.get('is_new_beneficiary', pd.Series(0, index=df.index)).iloc[0],
        df.get('device_changed', pd.Series(0, index=df.index)).iloc[0],
        df.get('location_anomaly', pd.Series(0, index=df.index)).iloc[0]
    ]
    
    return np.array([features])
