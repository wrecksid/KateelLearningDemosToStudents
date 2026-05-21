# Clustering Demo 002 — K-Means and DBSCAN Comparison

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `TechUseCaseDemos/Clustering/`

A lightweight, self-contained clustering demo that generates synthetic 2D cluster
data and compares K-Means against DBSCAN — highlighting where each algorithm
succeeds and where it fails.

---

## What This Demo Does

| Step | Detail |
|------|--------|
| Data generation | 300 points in 3 well-separated Gaussian clusters |
| K-Means | Assigns all points; fast; assumes spherical clusters |
| DBSCAN | Density-based; finds clusters without specifying `k`; handles noise |
| PCA | Verifies 2D representation explains most variance |

---

## Files

| File | Purpose |
|------|---------|
| `fulldemo.py` | Main demo — generates data, runs both algorithms, prints metrics |
| `main.py` | Entry-point wrapper |
| `syndata.py` | Standalone data generator for external use |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd TechUseCaseDemos/Clustering/demo002
pip install -r requirements.txt
python fulldemo.py
```

---

## Expected Output

```
KMeans clustering accuracy: ~0.98
PCA 2D explained variance: ~0.99
DBSCAN found 3 clusters.
Clustering demo complete.
```

---

## Student Extensions

1. Try DBSCAN with `eps=0.3` and `eps=1.0` — observe how cluster membership and noise points change.
2. Add **Agglomerative Clustering** with Ward linkage and compare the dendrogram to K-Means boundaries.
3. Introduce elongated clusters (use `np.random.randn(100, 2) @ [[3, 1], [0, 0.5]]`) and see how K-Means breaks down while DBSCAN adapts.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md).
