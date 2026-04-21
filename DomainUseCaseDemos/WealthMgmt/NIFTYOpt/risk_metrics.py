"""
Risk metrics computation for portfolio returns.
"""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_returns(tickers, days=252):
    np.random.seed(42)
    mu = np.random.uniform(0.0001, 0.001, len(tickers))
    cov = np.random.uniform(0.5, 1.5, (len(tickers), len(tickers)))
    cov = (cov + cov.T) / 2
    np.fill_diagonal(cov, np.abs(np.diag(cov)) + 0.2)
    rets = np.random.multivariate_normal(mu, cov, days)
    return pd.DataFrame(rets, columns=tickers)


def compute_metrics(returns):
    metrics = {}
    metrics["annualized_return"] = returns.mean() * 252
    metrics["annualized_volatility"] = returns.std() * np.sqrt(252)
    metrics["sharpe_ratio"] = metrics["annualized_return"] / metrics["annualized_volatility"]
    metrics["max_drawdown"] = (returns / returns.cummax() - 1).min()
    metrics["var_95"] = returns.quantile(0.05)
    return pd.DataFrame(metrics)


if __name__ == "__main__":
    tickers = ["RELIANCE", "INFY", "HDFCBANK"]
    rets = generate_returns(tickers, 252)
    m = compute_metrics(rets)
    print("Risk metrics per asset:")
    print(m)
    print("Risk metrics demo complete.")
