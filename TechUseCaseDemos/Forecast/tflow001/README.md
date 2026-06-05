# Time Series Forecast Demo — Moving Average (tflow001)

**Repository:** [KateelLearningDemosToStudents](https://github.com/VinayaSharada/KateelLearningDemosToStudents)
**Author:** Professor Vinaya Sathyanarayana
**Section:** `TechUseCaseDemos/Forecast/`

A lightweight entry-level forecasting demo using a rolling moving-average model on
synthetic time series data. Intended as a conceptual stepping stone before the
LSTM-based `tsdemo001`.

---

## What This Demo Does

| Step | Detail |
|------|--------|
| Data generation | 300-day synthetic series with trend + 30-day seasonality + noise |
| Model | 7-day rolling moving average |
| Output | Actual vs forecast overlay plot saved to `/tmp/forecast001.png` |

---

## Files

| File | Purpose |
|------|---------|
| `forecast001.py` | Main demo — generate series, compute MA forecast, save plot |
| `forecast002.py` | Variant with different window sizes |
| `forecast003.py` | Extended variant with multiple MA horizons |
| `requirements.txt` | Python dependencies |

---

## Setup & Run

```bash
cd TechUseCaseDemos/Forecast/tflow001
pip install -r requirements.txt
python forecast001.py
```

Output: `forecast001.png` saved to `/tmp/` (or current directory on Windows).

---

## How This Relates to tsdemo001

This demo shows the **simplest possible forecast baseline** (moving average).
[`tsdemo001`](../tsdemo001/) replaces the moving average with an **LSTM neural network**
for a direct comparison of classical vs deep-learning forecasting.

---

## Student Extensions

1. Compare window sizes (3, 7, 14, 30 days) by computing MAE for each.
2. Add an **Exponential Moving Average (EWM)** using `pandas.Series.ewm()` and compare.
3. Implement a **seasonal naive baseline** (forecast = value from same day last period).
4. Connect to `tsdemo001` to compare MA vs LSTM on the same synthetic series.

---

## Attribution

If you use this demo in a course or project, see [ATTRIBUTION.md](../../../ATTRIBUTION.md).
