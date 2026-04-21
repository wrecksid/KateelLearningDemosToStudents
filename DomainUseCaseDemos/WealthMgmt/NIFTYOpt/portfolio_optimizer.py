"""
Portfolio optimization demo using efficient frontier and risk parity.
"""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_mock_returns(tickers, days=252):
    np.random.seed(42)
    drift = np.random.uniform(-0.0002, 0.0006, len(tickers))
    cov = np.random.uniform(0.5, 1.5, (len(tickers), len(tickers)))
    cov = (cov + cov.T) / 2
    np.fill_diagonal(cov, np.abs(np.diag(cov)) + 0.2)
    rets = np.random.multivariate_normal(drift, cov, days)
    return pd.DataFrame(rets, columns=tickers)


def compute_efficient_frontier(returns):
    mu = returns.mean().values
    S = returns.cov().values
    n = len(mu)
    targets = np.linspace(mu.min(), mu.max(), 20)
    weights = []
    for t in targets:
        ones = np.ones(n)
        A = np.vstack([mu, ones])
        b = np.array([t, 1.0])
        w = np.linalg.lstsq(A, b, rcond=None)[0]
        w = np.clip(w, 0, 1)
        w /= w.sum()
        weights.append(w)
    port_rets = np.array([w @ mu for w in weights])
    port_risks = [np.sqrt(w @ S @ w) for w in weights]
    sharpe = port_rets / port_risks
    best_idx = np.argmax(sharpe)
    return weights[best_idx], port_rets[best_idx], port_risks[best_idx], sharpe[best_idx]


if __name__ == "__main__":
    tickers = ["RELIANCE", "INFY", "HDFCBANK", "SBIN", "ITC"]
    rets = generate_mock_returns(tickers, 252)
    w, ret, risk, sharpe = compute_efficient_frontier(rets)
    print(f"Optimal portfolio return: {ret:.3f}, risk: {risk:.3f}, Sharpe: {sharpe:.3f}")
    print(f"Weights: {dict(zip(tickers, np.round(w, 4)))}")
    print("Optimization demo complete.")
