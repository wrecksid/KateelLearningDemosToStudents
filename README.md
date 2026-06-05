# KateelLearningDemosToStudents

**Author:** Professor Vinaya Sathyanarayana
**GitHub:** [VinayaSharada](https://github.com/VinayaSharada)
**Contact:** vinallcontact@gmail.com

A curated, actively maintained collection of AI/ML demos, data-science walkthroughs, and
in-browser Small Language Model applications built for students, faculty, and practitioners.
Topics span finance, cybersecurity, NLP, forecasting, clustering, edge AI, blockchain,
and responsible AI — all with synthetic data so every demo runs without compliance concerns.

---

## About the Author

**Professor Vinaya Sathyanarayana** is an AI/ML practitioner and educator with extensive
experience in financial analytics, data science, and applied machine learning. This
repository grew out of real course delivery and is continuously expanded to reflect current
industry practices and emerging techniques. All demos are designed to be classroom-ready:
runnable in minutes, business-contextualised, and extensible for deeper student exploration.

---

## Repository Structure

| Section | Description |
|---------|-------------|
| [🤖 Browser-AI-Demos](🤖%20Browser-AI-Demos/) | Zero-dependency in-browser SLM apps — no server, no API key, runs offline |
| [DomainUseCaseDemos](DomainUseCaseDemos/) | Industry vertical demos across BFSI, cybersecurity, NLP, wealth management |
| [TechUseCaseDemos](TechUseCaseDemos/) | Technique-first ML demos: classification, clustering, forecasting, pattern mining |
| [Assignments](Assignments/) | Course-ready assignment scaffolds mapped to specific demos |
| [ecomm001](ecomm001/) | End-to-end e-commerce analytics pipeline with 900k+ synthetic orders |

---

## Demo Catalog

### 🤖 In-Browser AI — Zero Cloud, Zero Server

All seven demos run 100% locally in the browser using **Transformers.js v3**.
No API keys. No server. No data leaves the device.
Open any `index.html` in Chrome 113+ or Edge 113+ (WebGPU enabled).

| # | Demo | Model | Approx. Size |
|---|------|-------|-------------|
| 1 | [Local Chat Advisor](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/1-local-chat-advisor/) | SmolLM2-135M-Instruct | ~135 MB |
| 2 | [Smart Ticket Tagger](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/2-customer-support-tagger/) | DistilBERT + DeBERTa | ~140 MB |
| 3 | [Privacy Notebook](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/3-privacy-notebook/) | T5-Small | ~60 MB |
| 4 | [Whisper Voice Transcriber](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/4-whisper-voice-transcriber/) | Whisper Tiny EN | ~39 MB |
| 5 | [Named Entity Tagger](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/5-entity-tagger/) | BERT-NER | ~110 MB |
| 6 | [Semantic Search Engine](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/6-semantic-search/) | all-MiniLM-L6-v2 | ~23 MB |
| 7 | [SYNAPSE — Semantic Word Game](🤖%20Browser-AI-Demos/Browser-AI-Product-Demos/semantic-game/) | mxbai-embed-xsmall-v1 | ~25 MB |

---

### 🏦 Domain Use Case Demos

#### Banking

| Demo | Topic |
|------|-------|
| [Customer Segmentation](DomainUseCaseDemos/Banking/CustSeg/) | K-Means clustering of bank customers by behaviour |
| [Interest Rate Risk](DomainUseCaseDemos/Banking/IntRateRisk/) | Sensitivity analysis on synthetic financial data |
| [Liquidity Management](DomainUseCaseDemos/Banking/LiquidityMgmt/) | Monte Carlo simulation for cash-flow variability |
| [Branch Queue Management](DomainUseCaseDemos/Banking/BankQ/) | Queue analytics for branch operations optimisation |
| [Marketing Pattern Mining](DomainUseCaseDemos/Banking/Marketing001/) | Apriori / FP-Growth for upsell and cross-sell targeting |
| [Mesa Liquidity Simulation](DomainUseCaseDemos/Banking/MesaLiquidity/) | Agent-based synthetic banking transaction data |

#### Credit Cards

| Demo | Topic |
|------|-------|
| [Credit Card Underwriting](DomainUseCaseDemos/CreditCards/CCUnderWriting/) | Supervised learning for credit approval decisions |
| [Customer Lifetime Value](DomainUseCaseDemos/CreditCards/CCCustomerLTV/) | CLV prediction and retention targeting |
| [Fraud Classification](DomainUseCaseDemos/CreditCards/CreditCardTxnFraud/) | Multi-model supervised fraud detection |
| [Fraud Outlier Detection](DomainUseCaseDemos/CreditCards/CreditCardFraudOutlier002/) | Isolation Forest, LOF, and Z-score anomaly methods |

#### Other Verticals

| Demo | Topic |
|------|-------|
| [BFSI FAQ Chatbot](DomainUseCaseDemos/BFSIChatbot/ProductFAQ001/) | Retrieval-based FAQ assistant — bridge to RAG |
| [Finance NLP](DomainUseCaseDemos/FinanceNLP/ComplaintAndSentiment001/) | Customer complaint classification and sentiment scoring |
| [Insurance Claim Fraud](DomainUseCaseDemos/Insurance/ClaimFraud001/) | Frequent itemset mining on claim attribute patterns |
| [Cyber Security — Intrusion Detection](DomainUseCaseDemos/CyberSecurity/ServerLogIntrusion/) | Apache / SSH / firewall log analysis with 7 detectors |
| [Portfolio Optimisation — NIFTY 50](DomainUseCaseDemos/WealthMgmt/NIFTYOpt/) | Efficient frontier using real NIFTY 50 market data |
| [Portfolio Optimisation — Synthetic](DomainUseCaseDemos/WealthMgmt/PortfolioOptSynSharpeRation/) | Max Sharpe / min-variance without live data dependency |
| [Credit Fairness](DomainUseCaseDemos/ResponsibleAI/CreditFairness001/) | Demographic parity and fairness metrics in lending models |
| [Model Drift & Governance](DomainUseCaseDemos/ModelGovernance/DriftAndThresholds001/) | Post-deployment monitoring, concept drift, champion-challenger |

---

### ⚙️ Technical ML Demos

| Demo | Technique |
|------|-----------|
| [Blockchain Finance](TechUseCaseDemos/Blockchain/) | PoW ledger, Merkle trees, smart contract escrow, payment channels |
| [Ensemble Classification](TechUseCaseDemos/Classification/demo001/) | Random Forest, Gradient Boosting, Logistic Regression |
| [Customer Clustering](TechUseCaseDemos/Clustering/demo002/) | K-Means, DBSCAN, Agglomerative with synthetic data |
| [Time Series Forecasting](TechUseCaseDemos/Forecast/tsdemo001/) | LSTM forecasting pipeline on synthetic time series |
| [Outlier Detection](TechUseCaseDemos/Outlier/demo001/) | Statistical and ML-based anomaly methods |
| [Frequent Pattern Mining](TechUseCaseDemos/PatternMining/demo002/) | Apriori and FP-Growth on transaction baskets |

---

## ⚠️ Mandatory Attribution & Usage Requirements

These requirements apply to **everyone** — faculty, students, researchers, and practitioners.
Failure to comply violates the spirit of open educational resources and academic integrity norms.

### 1. Credit in Every Presentation

Include this statement on **every** slide deck, handout, lab sheet, or published resource
that uses or derives from this material:

> *"Demos and course material adapted from the **KateelLearningDemosToStudents** repository*
> *by Professor Vinaya Sathyanarayana (GitHub: VinayaSharada).*
> *https://github.com/VinayaSharada/KateelLearningDemosToStudents"*

This credit must appear in presentation slides, lecture notes, lab sheets, course syllabi,
recorded video descriptions, and any published reports or notebooks.

### 2. Star the Repository ⭐

[**Star the repo here**](https://github.com/VinayaSharada/KateelLearningDemosToStudents/stargazers)
before or at the point of first use.

### 3. Send a Usage Notification Email 📧

Email **vinallcontact@gmail.com** with subject:

```
[KateelLearningDemos] Usage Notification — <Your Name / Institution>
```

Include: your name and role, institution or organisation, course / project name,
approximate start date, and a public link (if available).

This is required the first time you use the material, and again each time you begin
a new course, cohort, or project.

> Full policy: [ATTRIBUTION.md](ATTRIBUTION.md)

---

## Self-Register Your Usage

Once you have emailed and starred the repo, add yourself to the
**[Usage Registry](https://github.com/VinayaSharada/KateelLearningDemosToStudents/wiki/Usage-Registry)**
— it takes under a minute and shows the global reach of this work.

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening
a pull request. Key principles:

- Use synthetic data — never commit real-world sensitive datasets
- Every demo needs a README, `requirements.txt`, and a runnable main script
- Explain both the technical method and its business relevance
- Write for students who may be encountering the topic for the first time

---

## Quick Start

Most Python demos follow the same three-step pattern:

```bash
cd <demo-folder>
pip install -r requirements.txt
python <main_script>.py
```

Browser AI demos need no installation — open `index.html` directly in Chrome 113+
or Edge 113+ (WebGPU support required, enabled by default in modern versions).

---

*This repository is actively maintained by Professor Vinaya Sathyanarayana.*
*Star it to stay notified of new demos and updates.*
