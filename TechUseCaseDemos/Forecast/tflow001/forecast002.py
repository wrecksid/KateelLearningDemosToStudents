"""
Time series forecasting demo 002: exponential smoothing.
"""

import numpy as np
import pandas as pd

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    HAS_STATS = True
except ImportError:
    HAS_STATS = False

np.random.seed(42)

def generate_series(n=365):
    t = np.arange(n)
    level = 100 + 0.05 * t
    seasonal = 10 * np.sin(2 * np.pi * t / 30)
    noise = np.random.normal(0, 2, n)
    return pd.Series(level + seasonal + noise, index=pd.date_range(end=pd.Timestamp.today(), periods=n, freq="D"))

def forecast_holt_winters(series):
    if not HAS_STATS:
        return series.ewm(alpha=0.3).mean()
    model = ExponentialSmoothing(series, trend="add", seasonal="add", seasonal_periods=30)
    fit = model.fit()
    return fit.fittedvalues

if __name__ == "__main__":
    s = generate_series(365)
    fc = forecast_holt_winters(s)
    print("Forecast demo 002 complete (Holt-Winters fitted).")
