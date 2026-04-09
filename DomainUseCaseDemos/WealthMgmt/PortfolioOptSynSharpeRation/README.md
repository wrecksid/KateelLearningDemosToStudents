# Portfolio Optimization with Synthetic Data

## Overview

This folder contains a synthetic-data-driven portfolio optimization demo based on Modern Portfolio Theory. It is useful when you want a reproducible wealth-management example without depending on live market data.

The demo covers efficient frontier thinking, risk-return trade-offs, and Sharpe-ratio-based portfolio selection in a classroom-friendly way.

## Files in This Folder

- `generate_synthetic_data.py` creates synthetic return data
- `portfolio_optimization_demo.py` runs the main optimization workflow
- `portfolio_optimization_demo.ipynb` interactive notebook walkthrough
- `portfolio_data_generator.ipynb` notebook for synthetic data generation
- `requirements.txt` local dependencies
- `setup_venv.bat` and `setup_venv.sh` local environment setup helpers
- sample output images such as `efficient_frontier.png`

## How To Run

### 1. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate synthetic portfolio data

```powershell
python generate_synthetic_data.py
```

### 3. Run the optimization demo

```powershell
python portfolio_optimization_demo.py
```

You can also open the notebooks for a more guided walkthrough.

## What Students Learn

- efficient frontier construction
- minimum variance vs maximum Sharpe portfolios
- role of covariance and diversification
- how synthetic data can support controlled experimentation

## Course Relevance

This demo is a strong companion for:

- wealth management
- robo-advisory thinking
- asset allocation
- risk-return trade-off discussions

## Suggested Student Extensions

- change the risk-free rate and compare the resulting allocation
- add practical constraints such as max weight per asset
- compare synthetic-data results with the live-data `NIFTYOpt` demo
- add customer suitability notes for different portfolio choices
