# Insurance Claim Fraud Detection Using Frequent Itemset Mining

## Overview

This project demonstrates the use of AI/ML methodology — specifically frequent pattern mining — to detect fraud in individual insurance claims. Using synthetic claim data, students learn how to discover common attribute patterns linked to fraudulent behavior.

---

## Folder Structure

- `generate_synthetic_data.py`: Generates synthetic insurance claim dataset resembling real Indian insurance data.
- `fraud_pattern_mining.py`: Loads synthetic data, applies pattern mining algorithms (Apriori, FP-Growth), generates association rules, plots results, and compares algorithms.
- `syntheticdata.csv`: Generated dataset with 10,000+ records (created by `generate_synthetic_data.py`).
- `requirements.txt`: Python dependencies.

---

## Usage Instructions

### Synthetic Data Generation

Run the script `generate_synthetic_data.py` to create a realistic synthetic dataset.

