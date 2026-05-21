# Technical Use Case Demos

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana

This folder contains technique-first ML and data-science demos. Where
[DomainUseCaseDemos](../DomainUseCaseDemos/) leads with an industry problem,
these demos lead with a method — showing how a technique works on realistic synthetic
data, then connecting it to business applications.

---

## Blockchain

| Folder | Demo | Description |
|--------|------|-------------|
| [Blockchain](Blockchain/) | Blockchain Finance Suite | Five self-contained demos: PoW ledger with chain validation, 3-party smart contract escrow, Merkle tree integrity proofs, PoW vs PoS consensus comparison, off-chain payment channel. Zero external dependencies — standard Python library only. |

**Learning goals:** blockchain data structures, mining mechanics, tamper detection,
off-chain scaling patterns, smart contract state transitions.

---

## Classification

| Folder | Demo | Description |
|--------|------|-------------|
| [Classification/demo001](Classification/demo001/) | Ensemble Classifiers | Random Forest, Gradient Boosting, and Logistic Regression compared on synthetic tabular data. Includes feature importance, confusion matrices, and ROC curves. |

**Learning goals:** ensemble methods, bias-variance trade-off, model selection,
interpretability vs performance.

---

## Clustering

| Folder | Demo | Description |
|--------|------|-------------|
| [Clustering/demo002](Clustering/demo002/) | Customer Clustering Techniques | K-Means, DBSCAN, and Agglomerative clustering on synthetic customer data. Includes elbow method, silhouette analysis, and cluster profiling. |

**Learning goals:** unsupervised learning, distance metrics, hyperparameter sensitivity,
business interpretation of clusters.

---

## Forecasting

| Folder | Demo | Description |
|--------|------|-------------|
| [Forecast/tsdemo001](Forecast/tsdemo001/) | LSTM Time Series Forecasting | Full pipeline: synthetic series generation → windowing → LSTM training → forecast evaluation. Outputs training history plot, forecast plot, and saved `.h5` model. |
| [Forecast/tflow001](Forecast/tflow001/) | TensorFlow Forecast Variants | Alternative LSTM architectures and training configurations for time series. |

**Learning goals:** sequence modelling, sliding-window preparation, vanishing gradients,
LSTM architecture choices.

---

## High-Frequency Trading

| Folder | Demo | Description |
|--------|------|-------------|
| [HFT](HFT/) | HFT Simulation | Synthetic high-frequency order book and trade data for latency and market microstructure exploration. |

**Learning goals:** market microstructure, order book dynamics, tick data patterns.

---

## Outlier Detection

| Folder | Demo | Description |
|--------|------|-------------|
| [Outlier/demo001](Outlier/demo001/) | Outlier Detection Methods | Z-score, IQR, Isolation Forest, and Local Outlier Factor compared on the same synthetic dataset. Includes visualisation of decision boundaries. |

**Learning goals:** when to use statistical vs ML outlier methods, contamination parameter,
precision/recall for rare events.

---

## Pattern Mining

| Folder | Demo | Description |
|--------|------|-------------|
| [PatternMining/demo001](PatternMining/demo001/) | Frequent Itemset Basics | Apriori fundamentals on simple synthetic transaction data. |
| [PatternMining/demo002](PatternMining/demo002/) | Credit Card & E-Commerce Mining | Apriori and FP-Growth on two synthetic datasets: credit card product ownership and e-commerce baskets. Includes confidence/lift/support interpretation. |
| [PatternMining/demo003](PatternMining/demo003/) | Sequential Pattern Mining (SPMF) | Setup guide and integration for the SPMF Java framework via Python subprocess. CM-SPADE algorithm for sequential patterns. |

**Learning goals:** support/confidence/lift, Apriori vs FP-Growth efficiency, sequential
patterns vs itemsets, Python-Java interop.

---

## How These Demos Connect to Domain Use Cases

Each technique demo here has a direct counterpart in [DomainUseCaseDemos](../DomainUseCaseDemos/):

| Technique Demo | Domain Counterpart |
|----------------|--------------------|
| Classification/demo001 | CreditCards/CCUnderWriting, CreditCards/CreditCardTxnFraud |
| Clustering/demo002 | Banking/CustSeg |
| Forecast/tsdemo001 | Banking/LiquidityMgmt |
| Outlier/demo001 | CreditCards/CreditCardFraudOutlier002 |
| PatternMining/demo002 | Banking/Marketing001, Insurance/ClaimFraud001 |

---

## Attribution Reminder

If you use any of these demos in a course, workshop, or project, the three mandatory
requirements in [ATTRIBUTION.md](../ATTRIBUTION.md) apply:

1. **Credit Professor Vinaya Sathyanarayana** in every presentation, handout, and published resource.
2. **Star the repository** at https://github.com/VinayaSharada/KateelLearningDemosToStudents
3. **Email vinallcontact@gmail.com** with a usage notification.
