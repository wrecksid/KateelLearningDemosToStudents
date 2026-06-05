# High-Frequency Trading (HFT) Demo

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `TechUseCaseDemos/HFT/`

An educational simulation of high-frequency trading strategies on synthetic tick data,
covering momentum and mean-reversion signals, transaction cost modelling, and
performance metrics — without any real market connectivity.

---

## What This Demo Does

| Component | Detail |
|-----------|--------|
| Data | 5,000 synthetic tick prices (random walk, 1-min bars) |
| Momentum signal | Short MA (5) vs Long MA (20) crossover |
| Mean-reversion signal | Z-score of price vs rolling mean; entry at ±1σ |
| Transaction costs | Configurable basis-points per side (default 5 bps) |
| Performance metrics | P&L curve, Sharpe ratio, maximum drawdown |

---

## Files

| File | Purpose |
|------|---------|
| `hft_demo.py` | Full demo — data generation, signals, backtest, metrics |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd TechUseCaseDemos/HFT
pip install -r requirements.txt
python hft_demo.py
```

---

## Key Concepts Illustrated

- **Market microstructure** — tick price simulation as a random walk with drift
- **Signal generation** — how simple technical indicators create trading signals
- **Transaction cost drag** — how 5 bps per side erodes strategy returns at high frequency
- **Sharpe ratio** — risk-adjusted return comparison between strategies
- **Max drawdown** — peak-to-trough loss as a risk measure

---

## Student Extensions

1. Increase transaction costs to 20 bps and observe how the momentum strategy degrades.
2. Add a **limit order book** simulation with bid-ask spread.
3. Compare the Sharpe ratio of momentum vs mean-reversion over different market regimes (trending vs ranging).
4. Implement a **volatility filter** — only trade when rolling volatility is below a threshold.
5. Connect to `DomainUseCaseDemos/WealthMgmt/NIFTYOpt` to apply HFT signals on real NIFTY 50 data.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../ATTRIBUTION.md).
