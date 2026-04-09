# Kateel Learning Demos To Students

This repository is a companion workspace for applied AI, machine learning, analytics, and BFSI domain learning. It is designed to help students move from classroom concepts to runnable demos, synthetic data generation, analysis notebooks, and small end-to-end mini projects.

The strongest current coverage is in banking, credit cards, insurance, wealth management, segmentation, fraud, underwriting, portfolio optimization, and pattern mining. It is especially useful as a practical companion for the BITS Financial AI / ML course materials.

## What This Repo Should Help Students Do

- understand a concept through a runnable example
- generate synthetic datasets when real data is not available
- compare a notebook-based workflow with a script-based workflow
- connect technical methods to BFSI business use cases
- extend starter demos into assignments, mini projects, and case discussions

## Quick Start

### 1. Clone the repository

```powershell
git clone https://github.com/VinayaSharada/KateelLearningDemosToStudents.git
cd KateelLearningDemosToStudents
```

### 2. Pick one demo folder

Examples:

- `DomainUseCaseDemos\CreditCards\CreditCardFraud`
- `DomainUseCaseDemos\CreditCards\CCUnderWriting`
- `DomainUseCaseDemos\Banking\CustSeg`
- `DomainUseCaseDemos\WealthMgmt\NIFTYOpt`
- `TechUseCaseDemos\PatternMining\demo002`

### 3. Install dependencies for that folder

Many folders include a local `requirements.txt`, plus setup scripts such as `setup_venv.bat` or `setup_venv.sh`.

Example:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the generator first if synthetic data is needed

Many demos follow this pattern:

- generate synthetic data
- run analysis or modeling script
- optionally open the notebook for step-by-step exploration

## Repository Structure

### `DomainUseCaseDemos`

Business-oriented BFSI demos. These are the best starting point for course alignment.

Representative topics:

- banking queue analytics
- customer segmentation
- liquidity management
- interest rate risk
- credit card fraud
- credit underwriting
- customer lifetime value
- insurance claim fraud
- wealth management and portfolio optimization

### `TechUseCaseDemos`

Method-oriented demos that focus more on the technique than the business domain.

Representative topics:

- classification
- clustering
- outlier detection
- forecasting
- pattern mining

### `ecomm001`

A more complete mini-project that demonstrates a polished end-to-end workflow with synthetic data, notebook analysis, automated reporting, and dashboard-oriented presentation.

## Demo Index

A quick curated inventory of high-value demos lives in [DEMO_INDEX.md](D:\Todel\nodeapps\KateelLearningDemosToStudents\DEMO_INDEX.md).

## Recommended Student Workflow

1. Read the local README in the chosen demo folder.
2. Run the synthetic data generator if one exists.
3. Run the Python demo script to see the baseline output.
4. Open the notebook to understand the steps in detail.
5. Change one parameter, distribution, threshold, or model choice.
6. Record what changed in both the metrics and the business interpretation.

## Financial AI / ML Course Companion Map

This repo already supports many parts of the course. A dedicated mapping lives in [COURSE_COMPANION_MAP.md](D:\Todel\nodeapps\KateelLearningDemosToStudents\COURSE_COMPANION_MAP.md).

Suggested starting demos by topic:

- credit risk and underwriting: `DomainUseCaseDemos\CreditCards\CCUnderWriting`
- fraud detection: `DomainUseCaseDemos\CreditCards\CreditCardFraud`, `DomainUseCaseDemos\Insurance\ClaimFraud001`
- segmentation: `DomainUseCaseDemos\Banking\CustSeg`
- wealth management: `DomainUseCaseDemos\WealthMgmt\NIFTYOpt`
- pattern mining: `TechUseCaseDemos\PatternMining\demo002`

## Current Gaps To Fill Over Time

To become a stronger super companion repo for the course, the next additions should include:

- NLP for financial text
- chatbot / assistant demos for BFSI
- model governance and monitoring
- explainability and fairness
- AI strategy and operating model case demos
- course-wise assignments and rubrics

The recommended additions are listed in more detail in [ADDITIONAL_DEMOS.md](D:\Todel\nodeapps\KateelLearningDemosToStudents\ADDITIONAL_DEMOS.md).

## Assignments

A starter assignment structure now lives under [Assignments](D:\Todel\nodeapps\KateelLearningDemosToStudents\Assignments). This is intended to help convert demos into guided coursework, labs, mini-projects, and evaluation tasks.

## Contribution Style

When adding or updating a demo, please try to include:

- a clear `README.md`
- a reproducible way to install dependencies
- a synthetic data generator when real data is not available
- a runnable Python script
- a notebook for interactive learning where helpful
- a short explanation of business meaning, not only technical outputs

See [CONTRIBUTING.md](D:\Todel\nodeapps\KateelLearningDemosToStudents\CONTRIBUTING.md) for the preferred structure.

## Notes

- This repository contains student-facing educational material and experiments at different maturity levels.
- Some folders are more polished than others; the intent is to improve consistency over time.
- If a demo folder is missing documentation, treat it as a good candidate for cleanup and standardization.

## Copyright

Copyright Professor Vinaya Sathyanarayana. All rights reserved.
