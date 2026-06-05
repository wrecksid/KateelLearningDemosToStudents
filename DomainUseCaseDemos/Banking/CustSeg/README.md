# Banking Customer Segmentation Demo — CustSeg

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `DomainUseCaseDemos/Banking/CustSeg/`

A comprehensive bank customer segmentation pipeline combining **K-Means clustering**, **DBSCAN**, **RFM analysis**, and **PCA visualisation** on synthetic Indian banking data. Produces actionable segment profiles (High-Value, Young Professionals, Long-term Loyal, Low-Engagement) with business recommendations and churn risk scoring for each segment.

---

## What This Demo Does

| Step | Detail |
|------|--------|
| Data generation | `generate_bank_data.py` — synthetic customers with income, balance, credit score, tenure, products, CLV (₹-denominated) |
| Preprocessing | Missing-value imputation, feature engineering (income-to-balance ratio, CLV/year, products/tenure) |
| K-Means segmentation | `n_clusters=4` with elbow + silhouette selection; cluster profiles with churn rate per segment |
| RFM analysis | Recency / Frequency / Monetary scoring (1–5 quartiles), segment labels: Champions → Lost Customers |
| Optimal clusters | `find_optimal_clusters()` — inertia, silhouette score, Calinski-Harabasz index plotted together |
| Visualisations | 2×3 matplotlib grid + 3D scatter (income × balance × credit score) saved as PNG |
| Business insights | Per-segment strategy recommendations, revenue opportunity estimates, risk levels |
| Export | `segmentation_results.csv` with cluster + segment labels merged back onto original records |

---

## Files

| File | Purpose |
|------|---------|
| `customer_segmentation.py` | Main pipeline — `CustomerSegmentation` class with K-Means, RFM, insights |
| `generate_bank_data.py` | Synthetic data generator for Indian banking customers |
| `data_generation.ipynb` | Notebook walkthrough of data generation |
| `customer_segmentation.ipynb` | Notebook walkthrough of full segmentation pipeline |
| `rmp_scripts/` | RapidMiner process files for K-Means and RFM workflows |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd DomainUseCaseDemos/Banking/CustSeg
pip install -r requirements.txt

# Generate synthetic data first
python generate_bank_data.py

# Run segmentation (K-Means + RFM)
python customer_segmentation.py --data bank_customer_data.csv --method both --clusters 4
```

**CLI options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--data` | `bank_customer_data.csv` | Input CSV |
| `--method` | `both` | `kmeans`, `rfm`, or `both` |
| `--clusters` | `4` | K-Means cluster count |
| `--output` | `segmentation_results.csv` | Result export filename |

---

## Expected Output

```
Preprocessed 2000 customer records
Optimal clusters: 4
K-Means completed - Silhouette Score: 0.312
RFM completed - 8 segments identified
Segmentation results exported to segmentation_results.csv
```

Plots saved: `kmeans_segmentation_analysis.png`, `rfm_segmentation_analysis.png`, `kmeans_3d_clusters.png`

---

## Segment Examples

| Segment | Profile | Strategy |
|---------|---------|----------|
| High-Value | Income > ₹8L, Balance > ₹5L | Premium services, wealth management |
| Young Professionals | Age < 35, Income < ₹5L | Digital banking, career-building products |
| Long-term Loyal | Tenure > 15 years | Retention programs, loyalty rewards |
| Low-Engagement | < 5 transactions/month | Activation campaigns, simplified products |

---

## How This Connects to Other Demos

- [`Banking/OldBankCustomerSegmentation`](../OldBankCustomerSegmentation/) — alternative RFM + K-Means pipeline with Faker-generated data
- [`TechUseCaseDemos/Clustering/demo001`](../../../TechUseCaseDemos/Clustering/demo001/) — foundational clustering techniques
- [`Banking/Marketing001`](../Marketing001/) — association rules for cross-sell / upsell

---

## Student Extensions

1. Try `n_clusters` from 3 to 8 — observe how silhouette and business coherence change.
2. Add **Gaussian Mixture Models (GMM)** and compare soft-cluster assignments with K-Means hard labels.
3. Introduce a **real churn dataset** (e.g., UCI Bank Marketing) in place of synthetic data.
4. Add **cluster migration analysis** — track which segment a customer moves to month-over-month.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
