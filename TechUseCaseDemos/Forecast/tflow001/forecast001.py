"""
Time series forecasting demo 001: univariate forecasting with simple moving average.
"""

import numpy as np
import pandas as pd
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

np.random.seed(42)

def generate_series(n=300):
    t = np.arange(n)
    base = 10 + 0.02 * t
    seasonal = 5 * np.sin(2 * np.pi * t / 30)
    noise = np.random.normal(0, 1, n)
    y = base + seasonal + noise
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n, freq="D")
    return pd.Series(y, index=dates)

def forecast_moving_average(series, window=7):
    return series.rolling(window=window).mean()

if __name__ == "__main__":
    s = generate_series(300)
    fc = forecast_moving_average(s)
    if HAS_MPL:
        plt.figure(figsize=(10, 4))
        plt.plot(s.index, s.values, label="Actual")
        plt.plot(fc.index, fc.values, label="MA Forecast", alpha=0.8)
        plt.legend(); plt.tight_layout()
        plt.savefig("/tmp/forecast001.png", dpi=120); plt.close()
    print("Forecast demo 001 complete. Plot saved to /tmp/forecast001.png")
