# Liquidity Management Demo

## Overview

This folder contains a synthetic-data-based liquidity management demo for banking and treasury learning. It helps students understand how inflows, outflows, transaction timing, and operating variability affect liquidity position and managerial decision-making.

The demo is useful for courses covering BFSI operations, treasury analytics, risk awareness, and AI-assisted financial analysis.

## Files in This Folder

- `generate_synthetic_liquidity_data.py` generates transaction-level liquidity data
- `liquidity_monte_carlo_simulation.py` runs the main analysis and simulation workflow
- `generate_synthetic_liquidity_data.ipynb` notebook version of data generation
- `liquidity_monte_carlo_simulation.ipynb` notebook version of analysis
- `requirements.txt` local dependencies
- `setup_env.sh` environment setup helper
- `liquidity_analysis_report.txt` sample output report

## What Students Learn

- inflow and outflow behavior in a banking context
- cash-flow variability and stress thinking
- scenario analysis using simulation
- how treasury-style analytics can support decision-making

## How To Run

### 1. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate synthetic data

```powershell
python generate_synthetic_liquidity_data.py
```

### 3. Run the simulation / analysis

```powershell
python liquidity_monte_carlo_simulation.py
```

You can also explore the notebook files for a step-by-step walkthrough.

## Course Relevance

This demo is a strong companion for:

- financial operations analytics
- risk and regulation discussions
- treasury and liquidity management concepts
- model governance conversations where decision support and assumptions matter

## Suggested Student Extensions

- change transaction distributions and compare the liquidity profile
- add early warning thresholds for low-liquidity days
- compare normal conditions with stressed market conditions
- add a dashboard or daily monitoring summary
- extend the model to include funding cost or regulatory limits
