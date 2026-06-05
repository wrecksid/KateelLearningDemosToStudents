# Banking Customer Segmentation Demo — OldBankCustomerSegmentation

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `DomainUseCaseDemos/Banking/OldBankCustomerSegmentation/`

An earlier customer segmentation implementation pairing **RFM analysis** with **K-Means clustering** on Faker-generated banking data. Useful as a reference alongside the `CustSeg` demo to compare design choices — notably the use of `pathlib.Path`, typed function signatures, and a leaner feature set focused on recency/frequency/monetary scores.

---

## What This Demo Does

| Step | Detail |
|------|--------|
| Data generation | `synthetic_data_generator.py` — `BankingDataGenerator` class; log-normal income, exponential balance, credit score 300–850; Faker-powered names/emails |
| Data loading | Validates required columns (`customer_id`, `annual_income`, `account_balance`, `monthly_transactions`, `credit_score`) |
| RFM analysis | `perform_rfm_analysis()` — quartile scoring on pre-generated `recency_score`, `frequency_score`, `monetary_score`; 8 segment labels |
| K-Means clustering | `perform_kmeans_clustering()` — auto-selects optimal k via elbow + silhouette + Calinski-Harabasz |
| Cluster analysis | `analyze_clusters()` — business labels (High-Value, Young Professionals, Long-term Loyal, Low-Engagement, Standard) |
| Visualisations | PCA scatter, income vs balance, age vs credit score, cluster size, average income, products vs transactions |
| Business insights | `generate_business_insights()` — text report saved to `customer_segmentation_insights.txt` with estimated annual revenue opportunity per segment |
| Export | `customer_segments.csv` with cluster ID and business label merged onto original records |

---

## Files

| File | Purpose |
|------|---------|
| `customer_segmentation.py` | Main pipeline — `CustomerSegmentation` class |
| `synthetic_data_generator.py` | Faker-based synthetic data generator (`BankingDataGenerator`) |
| `customer_segmentation.ipynb` | Notebook walkthrough of full pipeline |
| `synthetic_data_generator.ipynb` | Notebook walkthrough of data generation |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd DomainUseCaseDemos/Banking/OldBankCustomerSegmentation
pip install -r requirements.txt

# Generate synthetic data
python synthetic_data_generator.py --customers 2000 --output synthetic_bank_data.csv

# Run full segmentation pipeline
python customer_segmentation.py --data synthetic_bank_data.csv --clusters 4
```

**CLI options (customer_segmentation.py):**

| Flag | Default | Description |
|------|---------|-------------|
| `--data` | `synthetic_bank_data.csv` | Input CSV |
| `--clusters` | auto | K-Means cluster count (auto if omitted) |
| `--output` | `customer_segments.csv` | Result export filename |

**CLI options (synthetic_data_generator.py):**

| Flag | Default | Description |
|------|---------|-------------|
| `--customers` | configurable | Number of customers to generate |
| `--output` | `synthetic_bank_data.csv` | Output CSV filename |

---

## Expected Output

```
Loaded 2000 customer records from synthetic_bank_data.csv
RFM analysis completed successfully
Optimal number of clusters determined: 4
Number of clusters: 4 | Silhouette score: 0.298
Results saved to: customer_segments.csv
Business insights saved to: customer_segmentation_insights.txt
```

---

## How This Connects to Other Demos

- [`Banking/CustSeg`](../CustSeg/) — enhanced version with DBSCAN, 3D plots, and Indian ₹-denominated data
- [`TechUseCaseDemos/Clustering/demo001`](../../../TechUseCaseDemos/Clustering/demo001/) — foundational clustering techniques
- [`Banking/Marketing001`](../Marketing001/) — association rules for cross-sell / upsell

---

## Student Extensions

1. Compare cluster assignments between this demo and `CustSeg` on the same dataset.
2. Replace Faker's English locale with `en_IN` and observe how city/state names change.
3. Add **DBSCAN** to detect anomalous customer profiles that don't fit any cluster.
4. Build a **cluster migration dashboard** by running the pipeline on monthly snapshots.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../../ATTRIBUTION.md).
