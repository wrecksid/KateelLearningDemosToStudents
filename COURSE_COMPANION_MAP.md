# Course Companion Map

This file maps the repository to the BITS Financial AI / ML course so students can quickly find practical demos after each session.

## How To Use This Map

- use the "best current demos" first
- use the "use with extension" items when the mapping is approximate
- treat the "recommended additions" as the next repo growth backlog

## Session Mapping

| Session | Topic | Best Current Demos | Notes |
|---|---|---|---|
| 01 | Introduction to AI in Financial Services | `DomainUseCaseDemos\Banking\BankQ`, `ecomm001` | Good for showing end-to-end analytics thinking and operational decision support. |
| 02 | ML Basics in Financial Contexts | `TechUseCaseDemos\Classification\demo001`, `TechUseCaseDemos\Clustering\demo001`, `TechUseCaseDemos\PatternMining\demo002` | Good for introducing supervised vs unsupervised vs pattern mining workflows. |
| 03 | Supervised Learning for Credit Risk / Underwriting | `DomainUseCaseDemos\CreditCards\CCUnderWriting` | Strong direct fit. Can be expanded with calibration, reject inference, and explainability. |
| 04 | Fraud Detection in Financial Transactions | `DomainUseCaseDemos\CreditCards\CreditCardFraud`, `DomainUseCaseDemos\CreditCards\CreditCardTxnFraud`, `DomainUseCaseDemos\Insurance\ClaimFraud001` | Strong fit across classification and pattern-based fraud detection. |
| 05 | Unsupervised Learning and Segmentation | `DomainUseCaseDemos\Banking\CustSeg`, `DomainUseCaseDemos\Banking\OldBankCustomerSegmentation` | Strong fit for clustering and customer profiling. |
| 06 | NLP in Finance | No direct demo yet | Recommended addition: sentiment, complaint classification, document summarization, or policy Q&A. |
| 07 | Chatbots and Virtual Assistants in BFSI | No direct demo yet | Recommended addition: retrieval + FAQ assistant over product or policy documents. |
| 08 | AI in Payments and Digital Transactions | `DomainUseCaseDemos\CreditCards\CreditCardTxnFraud` | Useful starting point, but a payments-specific transaction monitoring demo would improve coverage. |
| 09 | Mid-Term Case Discussion | `DomainUseCaseDemos\LearningExercise001.md`, `DomainUseCaseDemos\LearningExercise002.md` | Good seeds for assignment-style work. |
| 10 | AI in Wealth Management / Robo Advisory | `DomainUseCaseDemos\WealthMgmt\NIFTYOpt`, `DomainUseCaseDemos\WealthMgmt\PortfolioOptSynSharpeRation` | Strong fit for portfolio construction and advisory framing. |
| 11 | AI in Insurance | `DomainUseCaseDemos\Insurance\ClaimFraud001` | Good start; can be expanded into pricing, claims triage, or underwriting. |
| 12 | Algorithmic / High-Frequency Trading | No direct demo yet | Recommended addition: market microstructure, signal simulation, backtesting, and risk controls. |
| 13 | Regulatory Compliance and Model Governance | `DomainUseCaseDemos\Banking\LiquidityMgmt`, `DomainUseCaseDemos\Banking\IntRateRisk` | Partial fit from a regulated-risk perspective; a model monitoring demo would be better. |
| 14 | Ethics and Fairness in Financial AI | No direct demo yet | Recommended addition: bias checks, threshold trade-offs, subgroup metrics, explainability. |
| 15 | Future Trends: AutoML, RL, and Disruption | No direct demo yet | Recommended addition: simple AutoML comparison and toy RL allocation or pricing example. |
| 16 | Final Case Study: AI Strategy in FinTech | `ecomm001`, `DomainUseCaseDemos\LearningExercise001.md`, `DomainUseCaseDemos\LearningExercise002.md` | Good for combining analytics, business framing, and communication. |

## Best Current Demo Paths

- credit underwriting: `DomainUseCaseDemos\CreditCards\CCUnderWriting`
- card fraud classification: `DomainUseCaseDemos\CreditCards\CreditCardFraud`
- card transaction fraud: `DomainUseCaseDemos\CreditCards\CreditCardTxnFraud`
- insurance claim fraud: `DomainUseCaseDemos\Insurance\ClaimFraud001`
- customer segmentation: `DomainUseCaseDemos\Banking\CustSeg`
- queue analytics: `DomainUseCaseDemos\Banking\BankQ`
- liquidity management: `DomainUseCaseDemos\Banking\LiquidityMgmt`
- interest rate risk: `DomainUseCaseDemos\Banking\IntRateRisk`
- wealth optimization: `DomainUseCaseDemos\WealthMgmt\NIFTYOpt`
- pattern mining: `TechUseCaseDemos\PatternMining\demo002`

## High-Value Enhancements

The following additions would most improve the repo as a super companion repo:

1. `DomainUseCaseDemos\FinanceNLP\...`
2. `DomainUseCaseDemos\BFSIChatbot\...`
3. `DomainUseCaseDemos\ModelGovernance\...`
4. `DomainUseCaseDemos\ResponsibleAI\...`
5. `DomainUseCaseDemos\Payments\...`
6. `DomainUseCaseDemos\Trading\...`
7. `Assignments\SessionXX\...`

## Suggested Demo Contract

Each demo should ideally contain:

- `README.md`
- `requirements.txt` or `pyproject.toml`
- `generate_synthetic_data.py` when applicable
- `main.py` or a clearly named runnable script
- notebook for teaching walkthrough
- expected outputs or screenshots
- "what to try next" section for students
