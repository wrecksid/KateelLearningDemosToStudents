# Credit Card Underwriting Demo

## Overview

This folder contains a credit card underwriting demo built on synthetic applicant data. It is one of the strongest current companion demos for supervised learning in BFSI because it combines business rules, data generation, analysis, and model-based approval thinking.

The workflow helps students connect lending concepts such as applicant quality, approval criteria, and explainable decisions with practical machine learning.

## Files in This Folder

- `generate_synthetic_data.py` creates synthetic underwriting application data
- `cc_underwriting_demo.py` runs the main underwriting analysis and ML demo
- `altair_ai_credit_underwriting.py` alternate implementation for analysis / visualization
- `rmp_validator.py` validates RapidMiner process files
- `cc_underwriting_rapidminer_process.rmp` and related `.rmp` files provide RapidMiner artifacts
- `requirements.txt` local Python dependencies
- setup helpers: `setup_venv.bat`, `setup_venv.sh`, `activate_env.bat`

## Recommended Run Flow

### 1. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate synthetic data

```powershell
python generate_synthetic_data.py
```

### 3. Run the demo

```powershell
python cc_underwriting_demo.py --help
python cc_underwriting_demo.py --demo
```

If you want the full script output with generated artifacts:

```powershell
python cc_underwriting_demo.py --full-demo --save-models
```

## What Students Learn

- supervised learning in a lending context
- features commonly used in underwriting
- approval vs rejection decision framing
- business interpretation of credit risk outputs
- how model results should support, not replace, underwriting policy

## Course Relevance

This folder maps directly to:

- credit risk and underwriting sessions
- supervised learning in finance
- model evaluation and decision threshold discussions
- business-rule plus model hybrid workflows

## Suggested Student Extensions

- compare logistic regression vs tree-based models
- add approval threshold analysis and reject-rate trade-offs
- test fairness across demographic slices where appropriate
- add explainability outputs such as feature importance or SHAP
- compare pure rules, pure model, and hybrid approval strategies
