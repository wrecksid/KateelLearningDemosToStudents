"""
Visualization utilities for portfolio and time series.
"""

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

import numpy as np
import pandas as pd


def plot_returns(returns_df, title="Returns", save_path="/tmp/returns_plot.png"):
    if not HAS_MPL:
        print("Matplotlib not available; skipping plot.")
        return
    plt.figure(figsize=(10, 4))
    for col in returns_df.columns:
        plt.plot(returns_df.index, returns_df[col].cumsum(), label=col)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close()
    print(f"Saved plot to {save_path}")


if __name__ == "__main__":
    dates = pd.date_range(end="2024-12-31", periods=252, freq="B")
    rets = pd.DataFrame(np.random.randn(252, 3), columns=["A", "B", "C"], index=dates)
    plot_returns(rets, title="Cumulative Returns")
    print("Visualization demo complete.")
