# Finance NLP: Complaint Classification and Sentiment

## Overview

This demo introduces NLP in a BFSI context using synthetic customer complaints. It shows how text analytics can help classify complaint type, estimate sentiment, and identify which cases may need escalation.

The demo is designed to be lightweight and classroom-friendly. It uses synthetic data so students can explore text workflows without privacy or compliance concerns.

## Files in This Folder

- `generate_synthetic_data.py` creates a synthetic complaint dataset
- `finance_nlp_demo.py` runs complaint classification and sentiment analysis
- `requirements.txt` local Python dependencies

## What Students Learn

- how text data differs from tabular BFSI data
- complaint classification using TF-IDF and logistic regression
- basic sentiment scoring for operational triage
- how NLP can support service quality and complaint operations

## How To Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python generate_synthetic_data.py
python finance_nlp_demo.py
```

## Suggested Extensions

- add more complaint categories
- compare logistic regression with Naive Bayes
- add multilingual complaint templates
- add a simple dashboard for escalation review
