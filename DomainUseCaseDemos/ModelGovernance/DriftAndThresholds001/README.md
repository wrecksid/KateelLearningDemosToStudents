# Model Governance: Drift and Threshold Monitoring

## Overview

This demo introduces a simple model governance workflow for BFSI. It trains a baseline approval model, compares baseline and monitoring periods, and highlights data drift, prediction-rate drift, and threshold-sensitive business metrics.

It is intended as an educational starting point for model monitoring and governance conversations.

## Files in This Folder

- `generate_synthetic_data.py` creates training, baseline, and monitoring datasets
- `drift_monitoring_demo.py` trains a model and compares model behavior across time periods
- `requirements.txt` local dependencies

## What Students Learn

- why production monitoring matters after model deployment
- how feature drift can appear even when code does not change
- how approval thresholds change business outcomes
- how to think about champion-challenger and monitoring dashboards

## How To Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python generate_synthetic_data.py
python drift_monitoring_demo.py
```

## Suggested Extensions

- add PSI bands for alert severity
- simulate fairness drift across groups
- compare more than one threshold
- add a simple monitoring dashboard export
