from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


FEATURES = ["income", "credit_score", "debt_to_income", "delinquency_count", "stable_income_flag"]


def psi(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    breakpoints = np.linspace(0, 1, bins + 1)
    quantiles = np.unique(np.quantile(expected, breakpoints))
    if len(quantiles) < 3:
        return 0.0
    expected_bins = pd.cut(expected, bins=quantiles, include_lowest=True)
    actual_bins = pd.cut(actual, bins=quantiles, include_lowest=True)
    expected_dist = expected_bins.value_counts(normalize=True, sort=False) + 1e-6
    actual_dist = actual_bins.value_counts(normalize=True, sort=False) + 1e-6
    return float(((actual_dist - expected_dist) * np.log(actual_dist / expected_dist)).sum())


def evaluate_period(model, df: pd.DataFrame, threshold: float) -> dict:
    probs = model.predict_proba(df[FEATURES])[:, 1]
    preds = (probs >= threshold).astype(int)
    return {
        "auc": roc_auc_score(df["approved"], probs),
        "approval_rate": preds.mean(),
        "avg_score": probs.mean(),
    }


def main():
    data_dir = Path("data")
    train = pd.read_csv(data_dir / "train.csv")
    baseline = pd.read_csv(data_dir / "baseline.csv")
    monitoring = pd.read_csv(data_dir / "monitoring.csv")

    model = LogisticRegression(max_iter=500)
    model.fit(train[FEATURES], train["approved"])

    print("\nFeature Drift (PSI)")
    psi_rows = []
    for feature in FEATURES:
        value = psi(baseline[feature], monitoring[feature])
        psi_rows.append({"feature": feature, "psi": round(value, 4)})
    psi_df = pd.DataFrame(psi_rows).sort_values("psi", ascending=False)
    print(psi_df.to_string(index=False))

    print("\nThreshold Comparison")
    thresholds = [0.4, 0.5, 0.6]
    rows = []
    for threshold in thresholds:
        base_metrics = evaluate_period(model, baseline, threshold)
        mon_metrics = evaluate_period(model, monitoring, threshold)
        rows.append(
            {
                "threshold": threshold,
                "baseline_auc": round(base_metrics["auc"], 4),
                "monitoring_auc": round(mon_metrics["auc"], 4),
                "baseline_approval_rate": round(base_metrics["approval_rate"], 4),
                "monitoring_approval_rate": round(mon_metrics["approval_rate"], 4),
                "score_shift": round(mon_metrics["avg_score"] - base_metrics["avg_score"], 4),
            }
        )
    report = pd.DataFrame(rows)
    print(report.to_string(index=False))

    alerts = psi_df[psi_df["psi"] >= 0.1]
    if alerts.empty:
        print("\nNo PSI alerts above 0.1")
    else:
        print("\nPSI Alerts")
        print(alerts.to_string(index=False))


if __name__ == "__main__":
    main()
