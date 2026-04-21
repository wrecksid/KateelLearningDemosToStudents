"""
NIFTY 50 data fetcher and preprocessor for portfolio optimization.
"""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_nifty_tickers():
    """Returns a representative subset of NIFTY 50 tickers."""
    return [
        "RELIANCE", "INFY", "HDFCBANK", "SBIN", "ITC",
        "TCS", "KOTAKBANK", "HCLTECH", "TITAN", "ASIANPAINT",
        "BAJFINANCE", "MARUTI", "ULTRACEMCO", "LT", "BHARTIARTL",
        "ADANIPORTS", "HEROMOTOCO", "M&M", "GRASIM", "POWERGRID",
        "BPCL", "VEDL", "ICICIBANK", "HDFCLIFE", "DIVISLAB",
        "SUNPHARMA", "DRREDDY", "TATAMOTORS", "EICHERMOT", "HDFC",
        "BAJAJ-AUTO", "GAIL", "JSWSTEEL", "APOLLOHOSP", "BAJAJFINSV",
        "ONGC", "SBILIFE", "ADANIENT", "UPL", "NTPC",
        "COALINDIA", "HINDUNILVR", "INDUSINDBK", "PFC", "WIPRO",
    ]


def generate_mock_prices(tickers, days=252):
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days, freq="B")
    data = {}
    for t in tickers:
        drift = np.random.uniform(-0.0003, 0.0008)
        vol = np.random.uniform(0.008, 0.025)
        rets = np.random.normal(drift, vol, days)
        price = 100 * np.exp(np.cumsum(rets))
        data[t] = np.round(price, 2)
    return pd.DataFrame(data, index=dates)


if __name__ == "__main__":
    tickers = generate_nifty_tickers()
    df = generate_mock_prices(tickers, 252)
    df.to_csv("nifty50_mock_prices.csv")
    print(f"Generated mock NIFTY 50 prices for {len(tickers)} tickers -> nifty50_mock_prices.csv")
