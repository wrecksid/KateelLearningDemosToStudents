"""
Fraud detection demo using outlier detection methods.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope

np.random.seed(42)


def generate_fraud_data(n=5000, fraud_ratio=0.02):
    n_fraud = int(n * fraud_ratio)
    n_normal = n - n_fraud

    normal = {
        "amount": np.random.exponential(50, n_normal).round(2),
        "hour": np.random.randint(6, 22, n_normal),
        "days_since_last": np.random.exponential(2, n_normal).round(2),
        "location_score": np.random.normal(0.5, 0.15, n_normal).clip(0, 1),
        "is_fraud": 0,
    }

    fraud = {
        "amount": np.concatenate([
            np.random.exponential(300, n_fraud // 2),
            np.random.exponential(800, n_fraud - n_fraud // 2),
        ]).round(2),
        "hour": np.concatenate([
            np.random.randint(2, 5, n_fraud // 2),
            np.random.randint(22, 5, n_fraud - n_fraud // 2),
        ]),
        "days_since_last": np.random.exponential(0.1, n_fraud).round(2),
        "location_score": np.random.normal(0.1, 0.05, n_fraud).clip(0, 1),
        "is_fraud": 1,
    }

    df = pd.DataFrame({**normal, **fraud})
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def detect_outliers(df, method="isolation_forest"):
    features = ["amount", "hour", "days_since_last", "location_score"]
    X = df[features].values

    if method == "isolation_forest":
        model = IsolationForest(contamination=0.02, random_state=42)
    else:
        model = EllipticEnvelope(contamination=0.02, random_state=42)

    df["anomaly_score"] = model.fit_predict(X)
    df["predicted_fraud"] = np.where(df["anomaly_score"] == -1, 1, 0)
    return df


if __name__ == "__main__":
    data = generate_fraud_data(3000)
    result = detect_outliers(data, method="isolation_forest")
    result.to_csv("fraud_outlier_predictions.csv", index=False)
    true_pos = ((result["is_fraud"] == 1) & (result["predicted_fraud"] == 1)).sum()
    print(f"Fraud detection demo complete. Results -> fraud_outlier_predictions.csv")
    print(f"True fraud cases detected: {true_pos}/{result['is_fraud'].sum()}")
