"""
High Frequency Trading (HFT) Demo
==================================

This demo illustrates a simple high-frequency trading strategy using:
- Synthetic market data generation (tick-level)
- Basic momentum and mean-reversion signals
- Transaction cost modeling
- Performance metrics (PnL, Sharpe ratio, max drawdown)

Dependencies:
    numpy, pandas, matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)


def generate_tick_data(n_points=5000, mu=0.0001, sigma=0.01):
    """Generate synthetic tick price data (random walk)."""
    dt = 1.0
    shocks = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt), size=n_points)
    prices = 100.0 + np.cumsum(shocks)
    timestamps = pd.date_range(start="2024-01-01", periods=n_points, freq="1min")
    return pd.DataFrame({"timestamp": timestamps, "price": prices})


def compute_momentum_signal(prices, short_win=5, long_win=20):
    """Compute a simple momentum signal: short MA vs long MA."""
    short_ma = prices.rolling(window=short_win).mean()
    long_ma = prices.rolling(window=long_win).mean()
    signal = np.where(short_ma > long_ma, 1, -1)
    return pd.Series(signal, index=prices.index)


def compute_mean_reversion_signal(prices, lookback=10, entry_z=1.0, exit_z=0.5):
    """Mean reversion: trade against recent deviations from a rolling mean."""
    rolling_mean = prices.rolling(window=lookback).mean()
    rolling_std = prices.rolling(window=lookback).std()
    z = (prices - rolling_mean) / rolling_std
    signal = np.where(z < -entry_z, 1, np.where(z > entry_z, -1, 0))
    exit_signal = np.where(np.abs(z) < exit_z, 0, signal)
    return pd.Series(exit_signal, index=prices.index)


def backtest_strategy(signal, prices, tc_bps=5):
    """
    Simple backtest with transaction costs.
    signal: pd.Series with values 1 (long), -1 (short), 0 (flat).
    tc_bps: basis points per side (e.g., 5 = 0.05%).
    """
    tc = tc_bps / 10000.0
    position = 0
    equity_curve = []
    cash = 0.0
    trades = []

    for t in range(len(signal)):
        target = int(signal.iloc[t])
        if target != position:
            p_enter = prices.iloc[t]
            prev_price = prices.iloc[t - 1] if t > 0 else p_enter
            pnl = position * (p_enter - prev_price)
            cash += pnl - abs(target - position) * p_enter * tc
            position = target
            action = "enter_long" if target == 1 else ("enter_short" if target == -1 else "exit")
            trades.append({"t": t, "action": action, "price": p_enter})
        equity_curve.append(cash + position * prices.iloc[t])

    equity = pd.Series(equity_curve, index=prices.index)
    ret = equity.pct_change().dropna()
    total_pnl = (equity.iloc[-1] - equity.iloc[0])
    sharpe = np.sqrt(252 * 6.5) * ret.mean() / ret.std() if ret.std() > 0 else 0.0
    max_dd = (equity.cummax() - equity).max()
    return {
        "equity": equity,
        "returns": ret,
        "total_pnl": total_pnl,
        "sharpe": sharpe,
        "max_drawdown": max_dd,
        "trades": pd.DataFrame(trades),
    }


def plot_results(prices, signal, results):
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    axes[0].plot(prices.index, prices.values, label="Price", color="black")
    axes[0].set_title("Price")
    axes[0].grid(True)
    axes[1].plot(signal.index, signal.values, label="Signal", drawstyle="steps-post", color="green")
    axes[1].set_ylabel("Signal")
    axes[1].set_yticks([-1, 0, 1])
    axes[1].grid(True)
    axes[2].plot(results["equity"].index, results["equity"].values, label="Equity", color="blue")
    axes[2].set_title(f"Equity (PnL={results['total_pnl']:.2f}, Sharpe={results['sharpe']:.2f})")
    axes[2].set_ylabel("Equity")
    axes[2].grid(True)
    plt.tight_layout()
    plt.savefig("hft_demo_results.png", dpi=120)
    plt.close()


def main():
    print("=== High Frequency Trading Demo ===\n")
    df = generate_tick_data(n_points=5000)
    prices = df["price"]
    timestamps = df["timestamp"]
    print(f"Generated {len(df)} ticks from {timestamps.iloc[0]} to {timestamps.iloc[-1]}")

    # Compute signals
    momentum = compute_momentum_signal(prices)
    mean_rev = compute_mean_reversion_signal(prices)
    combined = np.where(mean_rev != 0, mean_rev, momentum)
    combined_series = pd.Series(combined, index=prices.index)

    results = backtest_strategy(combined_series, prices, tc_bps=5)
    print(f"\nPerformance:")
    print(f"  Total PnL:        {results['total_pnl']:.4f}")
    print(f"  Annualized Sharpe: {results['sharpe']:.2f}")
    print(f"  Max Drawdown:      {results['max_drawdown']:.4f}")
    print(f"  Number of trades:  {len(results['trades'])}")
    print(f"  Last 5 trades:\n{results['trades'].tail().to_string(index=False)}")

    plot_results(prices, combined_series, results)
    print(f"\nChart saved to /tmp/hft_demo_results.png")
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
