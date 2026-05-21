# Domain Use Case Demos

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana

This folder contains industry-vertical demos organised by domain. Each demo is designed
to be classroom-ready: all data is synthetic (no compliance concerns), each folder
includes a README with setup steps, expected outputs, and student extension ideas.

---

## Banking

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [BankQ](Banking/BankQ/) | Branch queue design and analysis | Synthetic queue data, Faker (en_IN), queue metrics and visualisation |
| [CustSeg](Banking/CustSeg/) | Customer segmentation | K-Means clustering, RFM analysis, RapidMiner templates |
| [IntRateRisk](Banking/IntRateRisk/) | Interest rate risk management | Sensitivity analysis on synthetic Indian financial data |
| [LiquidityMgmt](Banking/LiquidityMgmt/) | Liquidity management | Monte Carlo simulation, cash-flow variability, scenario analysis |
| [Marketing001](Banking/Marketing001/) | Upsell / cross-sell pattern mining | Apriori, FP-Growth, association rules on product ownership |
| [MesaLiquidity](Banking/MesaLiquidity/) | Agent-based liquidity simulation | Synthetic banking transactions, Mesa-ready data generation |

---

## Credit Cards

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [CCCustomerLTV](CreditCards/CCCustomerLTV/) | Customer lifetime value | CLV modelling, retention targeting, revenue forecasting |
| [CCUnderWriting](CreditCards/CCUnderWriting/) | Credit card underwriting | Supervised learning, business rules, approval threshold analysis |
| [CreditCardFraudOutlier002](CreditCards/CreditCardFraudOutlier002/) | Fraud via anomaly detection | Isolation Forest, Local Outlier Factor, Z-score |
| [CreditCardTxnFraud](CreditCards/CreditCardTxnFraud/) | Fraud via classification | Random Forest, Logistic Regression, precision/recall, class imbalance |

---

## Cyber Security

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [ServerLogIntrusion](CyberSecurity/ServerLogIntrusion/) | Intrusion detection from server logs | Apache access log parsing, SSH brute-force detection, firewall port-scan analysis, 7 detectors mapped to MITRE ATT&CK |

Logs are in standard formats (Apache Combined, Linux syslog, iptables) using RFC 5737
non-routable IP ranges — safe for classroom use with no real infrastructure exposure.

---

## Finance NLP

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [ComplaintAndSentiment001](FinanceNLP/ComplaintAndSentiment001/) | Complaint classification and sentiment | TF-IDF, logistic regression, sentiment scoring, escalation triage |

---

## Insurance

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [ClaimFraud001](Insurance/ClaimFraud001/) | Insurance claim fraud detection | Frequent itemset mining (Apriori, FP-Growth) on synthetic Indian claim data |

---

## Model Governance

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [DriftAndThresholds001](ModelGovernance/DriftAndThresholds001/) | Model drift and threshold monitoring | Baseline vs monitoring period comparison, feature drift, champion-challenger thinking |

---

## Responsible AI

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [CreditFairness001](ResponsibleAI/CreditFairness001/) | Fairness in credit decisioning | Demographic parity, subgroup approval-rate analysis, accuracy vs fairness trade-off |

---

## Wealth Management

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [NIFTYOpt](WealthMgmt/NIFTYOpt/) | Portfolio optimisation on real data | Modern Portfolio Theory, efficient frontier, Monte Carlo, NIFTY 50 tickers |
| [PortfolioOptSynSharpeRation](WealthMgmt/PortfolioOptSynSharpeRation/) | Portfolio optimisation (no live data) | Max Sharpe ratio, min-variance frontier, diversification analysis |

---

## BFSI Chatbot

| Folder | Topic | Key Techniques |
|--------|-------|----------------|
| [ProductFAQ001](BFSIChatbot/ProductFAQ001/) | Product FAQ retrieval chatbot | Retrieval-based matching, bridge to RAG and production support |

---

## Attribution Reminder

If you use any of these demos in a course, workshop, or project, the three mandatory
requirements in [ATTRIBUTION.md](../ATTRIBUTION.md) apply:

1. **Credit Professor Vinaya Sathyanarayana** in every presentation, handout, and published resource.
2. **Star the repository** at https://github.com/VinayaSharada/KateelLearningDemosToStudents
3. **Email vinallcontact@gmail.com** with a usage notification.
