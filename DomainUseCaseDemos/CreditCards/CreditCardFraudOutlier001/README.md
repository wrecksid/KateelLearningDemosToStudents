# Credit Card Fraud Detection Using Outlier Methods

## Overview

This folder demonstrates fraud detection using anomaly and outlier detection methods instead of standard supervised classification. It is a useful teaching example because many fraud problems involve rare events, class imbalance, and incomplete labels.

## Files in This Folder

- `synthetic_data_generator.py` creates synthetic transaction data with fraud labels
- `frauddetect.py` runs multiple outlier-style fraud detection techniques
- `requirements.txt` local Python dependencies

## Methods Demonstrated

- statistical anomaly detection using z-scores
- Local Outlier Factor
- Isolation Forest

## How To Run

### 1. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate synthetic data

```powershell
python synthetic_data_generator.py
```

You can also pass a row count:

```powershell
python synthetic_data_generator.py 20000
```

### 3. Run the fraud detection demo

```powershell
python frauddetect.py
```

## What Students Learn

- why anomaly detection is relevant in fraud use cases
- the difference between supervised fraud detection and unsupervised / semi-supervised detection
- why precision and recall matter more than raw accuracy
- how contamination assumptions affect flagged cases

## Course Relevance

This folder is a good companion for:

- fraud detection
- outlier detection
- operational alerting trade-offs
- discussions of rare-event modeling in finance

## Suggested Student Extensions

- tune contamination levels and compare output behavior
- add transaction velocity or customer-history features
- compare this folder with the classification-based fraud demo
- document when outlier methods are more useful than labeled classification
