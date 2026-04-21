"""
NIFTY 50 constituent tickers and metadata.
"""

NIFTY50_TICKERS = [
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

INDICES = {
    "NIFTY 50": {
        "tickers": NIFTY50_TICKERS,
        "base_date": "1996-01-01",
        "free_float_factor": 0.75,
    },
}
