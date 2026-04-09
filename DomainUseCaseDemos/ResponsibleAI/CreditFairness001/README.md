# Responsible AI: Credit Fairness Demo

## Overview

This demo introduces fairness and responsible-AI checks in a lending context using synthetic credit approval data. It shows how a model can appear accurate overall while producing different approval patterns across subgroups.

The goal is educational: help students connect credit decisioning, subgroup analysis, explainability thinking, and governance obligations in BFSI.

## Files in This Folder

- `generate_synthetic_data.py` creates synthetic lending application data
- `credit_fairness_demo.py` trains a simple model and reports subgroup fairness metrics
- `requirements.txt` local Python dependencies

## What Students Learn

- why fairness matters in financial AI
- demographic parity style differences in approval rates
- true-positive and false-positive comparisons across groups
- why strong overall accuracy is not enough in regulated decisions

## How To Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python generate_synthetic_data.py
python credit_fairness_demo.py
```

## Suggested Extensions

- compare multiple thresholds
- add explainability notes for the most important features
- compare fairness across more than one protected attribute
- propose a human-review workflow for borderline cases
