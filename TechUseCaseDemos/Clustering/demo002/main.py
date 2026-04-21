"""
Main clustering pipeline demo.
"""

import numpy as np
import pandas as pd
try:
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

np.random.seed(42)

def demo():
    if not HAS_SKLEARN:
        print("SKLearn not installed.")
        return
    data = np.random.randn(300, 2) * np.array([1.0, 0.5])
    data[:100] += np.array([2, 2])
    data[100:200] += np.array([-2, -2])
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data)
    score = silhouette_score(data, labels)
    print(f"Clustering silhouette score: {score:.3f}")
    df = pd.DataFrame(data, columns=["x", "y"])
    df["cluster"] = labels
    df.to_csv("clustering_output.csv", index=False)
    print("Saved clustering_output.csv")
    print("Main clustering demo complete.")

if __name__ == "__main__":
    demo()
