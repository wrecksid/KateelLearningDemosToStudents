"""
Full clustering demo: generate data, cluster, visualize.
"""

import numpy as np
import pandas as pd
try:
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.decomposition import PCA
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

np.random.seed(42)

def generate_cluster_data(n=300):
    np.random.seed(42)
    c1 = np.random.randn(n // 3, 2) * 0.5 + np.array([2, 2])
    c2 = np.random.randn(n // 3, 2) * 0.5 + np.array([-2, -2])
    c3 = np.random.randn(n // 3, 2) * 0.5 + np.array([2, -2])
    X = np.vstack([c1, c2, c3])
    labels = np.array([0] * (n // 3) + [1] * (n // 3) + [2] * (n // 3))
    return X, labels

def demo():
    if not HAS_SKLEARN:
        print("SKLearn not installed; skipping clustering demo.")
        return
    X, true_labels = generate_cluster_data(300)
    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    preds = km.fit_predict(X)
    acc = (preds == true_labels).mean()
    print(f"KMeans clustering accuracy: {acc:.3f}")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    print(f"PCA 2D explained variance: {pca.explained_variance_ratio_.sum():.3f}")
    dbscan = DBSCAN(eps=0.6, min_samples=5)
    dpreds = dbscan.fit_predict(X)
    n_clusters = len(set(dpreds)) - (1 if -1 in dpreds else 0)
    print(f"DBSCAN found {n_clusters} clusters.")
    print("Clustering demo complete.")

if __name__ == "__main__":
    demo()
