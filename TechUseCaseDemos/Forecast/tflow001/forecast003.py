"""
Time series forecasting demo 003: ARIMA-style linear trend + seasonality.
"""

import numpy as np
import pandas as pd

try:
    from statsmodels.tsa.arima.model import ARIMA
    HAS_STATS = True
except ImportError:
    HAS_STATS = False

np.random.seed(42)

def generate_series(n=365):
    t = np.arange(n)
    y = 50 + 0.1 * t + 8 * np.sin(2 * np.pi * t / 30) + np.random.normal(0, 1.5, n)
    return pd.Series(y, index=pd.date_range(end=pd.Timestamp.today(), periods=n, freq="D"))

def forecast_arima_like(series):
    if not HAS_STATS:
        return series.rolling(7).mean()
    model = ARIMA(series, order=(1, 1, 1))
    fit = model.fit()
    return fit.fittedvalues

if __name__ == "__main__":
    s = generate_series(365)
    fc = forecast_arima_like(s)
    print("Forecast demo 003 complete (ARIMA-like fitted).")
