"""
Synthetic data generator for clustering demo 002.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

def generate_data(n=300):
    c1 = np.random.randn(n // 3, 2) * 0.5 + np.array([2, 2])
    c2 = np.random.randn(n // 3, 2) * 0.5 + np.array([-2, -2])
    c3 = np.random.randn(n // 3, 2) * 0.5 + np.array([2, -2])
    X = np.vstack([c1, c2, c3])
    labels = np.array([0] * (n // 3) + [1] * (n // 3) + [2] * (n // 3))
    df = pd.DataFrame(X, columns=["f1", "f2"])
    df["label"] = labels
    return df

if __name__ == "__main__":
    df = generate_data(300)
    df.to_csv("syndata_clustering_demo02.csv", index=False)
    print(f"Generated {len(df)} rows -> syndata_clustering_demo02.csv")
