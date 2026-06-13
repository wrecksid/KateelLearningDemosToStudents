"""
Outlier detection full demo with visualization.
"""

import numpy as np
import pandas as pd
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

np.random.seed(42)

def generate_data(n=500):
    normal = np.random.randn(n - 10, 2) * 0.5
    anomalies = np.random.uniform(low=-6, high=6, size=(10, 2))
    X = np.vstack([normal, anomalies])
    np.random.shuffle(X)
    return pd.DataFrame(X, columns=["x", "y"])

def demo():
    if not HAS_SKLEARN or not HAS_MPL:
        print("Required libraries missing; skipping outlier demo.")
        return
    df = generate_data(500)
    model = IsolationForest(contamination=0.02, random_state=42)
    df["outlier"] = model.fit_predict(df[["x", "y"]])
    inliers = df[df["outlier"] == 1]
    outliers = df[df["outlier"] == -1]
    print(f"Detected {len(outliers)} outliers out of {len(df)} points.")
    plt.figure(figsize=(6, 6))
    plt.scatter(inliers["x"], inliers["y"], c="blue", s=10, label="inlier", alpha=0.6)
    plt.scatter(outliers["x"], outliers["y"], c="red", s=40, label="outlier")
    plt.legend(); plt.tight_layout()
    plt.savefig("outlier_demo.png", dpi=120); plt.close()
    print("Outlier demo complete. Plot -> outlier_demo.png")

if __name__ == "__main__":
    demo()
