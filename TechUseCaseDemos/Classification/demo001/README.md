# Classification Demo 001

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `TechUseCaseDemos/Classification/`

A focused classification pipeline demo covering preprocessing, training, and evaluation
on synthetic tabular data — designed as a starting point for understanding supervised
learning before applying it to domain-specific datasets.

---

## What This Demo Does

Generates a synthetic 8-feature binary classification dataset and runs a full
end-to-end pipeline:

| Step | Detail |
|------|--------|
| Data generation | 600 samples, 8 numeric features, linearly separable boundary |
| Preprocessing | `StandardScaler` feature normalisation |
| Model | `RandomForestClassifier` (100 trees) |
| Evaluation | Accuracy, confusion matrix, full classification report |

---

## Files

| File | Purpose |
|------|---------|
| `full_classification_demo.py` | Main pipeline — generates data, trains, evaluates |
| `classificationdemo.py` | Simplified single-model variant for in-class walkthrough |
| `ensemble_classifiers_demo.py` | Extended version comparing multiple ensemble methods |
| `generatesyntheticdata.py` | Standalone data generator with configurable parameters |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd TechUseCaseDemos/Classification/demo001
pip install -r requirements.txt
python full_classification_demo.py
```

---

## Expected Output

```
Accuracy: ~0.93
Confusion Matrix: [[TN FP] [FN TP]]
Classification Report: precision / recall / f1 per class
Full classification demo complete.
```

---

## How This Connects to Domain Demos

This technique demo is the foundation for:
- [`DomainUseCaseDemos/CreditCards/CCUnderWriting`](../../DomainUseCaseDemos/CreditCards/CCUnderWriting/) — credit approval classification
- [`DomainUseCaseDemos/CreditCards/CreditCardTxnFraud`](../../DomainUseCaseDemos/CreditCards/CreditCardTxnFraud/) — fraud classification

---

## Student Extensions

1. Replace `RandomForest` with `GradientBoostingClassifier` or `XGBoost` and compare accuracy.
2. Add cross-validation (`cross_val_score`) to get a more stable performance estimate.
3. Plot feature importances to understand which of the 8 features matter most.
4. Introduce class imbalance (95% class 0, 5% class 1) and apply SMOTE to balance.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md).
