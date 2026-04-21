"""
Synthetic data generator for outlier detection demo.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

def generate_data(n=500):
    normal = np.random.randn(n - 10, 2) * 0.5
    anomalies = np.random.uniform(low=-6, high=6, size=(10, 2))
    X = np.vstack([normal, anomalies])
    np.random.shuffle(X)
    df = pd.DataFrame(X, columns=["x", "y"])
    return df

if __name__ == "__main__":
    df = generate_data(500)
    df.to_csv("syndata_outlier.csv", index=False)
    print(f"Generated {len(df)} outlier samples -> syndata_outlier.csv")
