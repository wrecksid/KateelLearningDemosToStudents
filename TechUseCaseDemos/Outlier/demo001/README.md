# Outlier Detection Demo 001

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `TechUseCaseDemos/Outlier/`

Detects outliers in synthetic 2D data using Isolation Forest, with a scatter plot
clearly showing flagged anomalies — a visual introduction to unsupervised anomaly
detection before applying it to financial fraud or network security data.

---

## What This Demo Does

| Step | Detail |
|------|--------|
| Data generation | 490 normal points (Gaussian) + 10 injected anomalies (uniform noise) |
| Model | `IsolationForest` with `contamination=0.02` |
| Output | Scatter plot (blue = inlier, red = outlier) saved to `/tmp/outlier_demo.png` |

---

## Files

| File | Purpose |
|------|---------|
| `fulldemo.py` | Main demo — generates data, fits Isolation Forest, plots results |
| `syndata.py` | Standalone data generator |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd TechUseCaseDemos/Outlier/demo001
pip install -r requirements.txt
python fulldemo.py
```

---

## Expected Output

```
Detected 10 outliers out of 500 points.
Outlier demo complete. Plot -> /tmp/outlier_demo.png
```

---

## How This Connects to Domain Demos

- [`CreditCards/CreditCardFraudOutlier001`](../../DomainUseCaseDemos/CreditCards/CreditCardFraudOutlier001/) — Isolation Forest on transaction data
- [`CreditCards/CreditCardFraudOutlier002`](../../DomainUseCaseDemos/CreditCards/CreditCardFraudOutlier002/) — LOF + Z-score anomaly detection
- [`CyberSecurity/NetworkAnomalyDetection`](../../DomainUseCaseDemos/CyberSecurity/NetworkAnomalyDetection/) — IF on network flows

---

## Student Extensions

1. Vary `contamination` from 0.01 to 0.10 and count how the number of flagged points changes.
2. Add **Local Outlier Factor (LOF)** and compare which points each method flags differently.
3. Replace the Gaussian normal data with a **t-distribution** (heavier tails) and observe how precision changes.
4. Extend to 8 features and use PCA to visualise the outlier detection in 2D.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md).
