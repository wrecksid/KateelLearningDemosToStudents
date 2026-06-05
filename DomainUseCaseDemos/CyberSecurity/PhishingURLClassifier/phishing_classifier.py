#!/usr/bin/env python3
"""
Phishing URL Classifier
=======================
Trains and compares three classifiers on URL-derived feature vectors:
  - Logistic Regression  (linear baseline, interpretable)
  - Random Forest        (ensemble, feature importance)
  - Gradient Boosting    (typically best AUC)

Outputs a 2×3 dashboard to reports/phishing_dashboard.png.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (auc, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "url_features.csv")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "reports")

FEATURE_COLS = [
    "url_length", "num_dots", "num_hyphens", "num_underscores",
    "num_slashes", "num_at", "num_digits", "has_ip_address",
    "num_subdomains", "domain_length", "tld_is_common", "has_https",
    "num_query_params", "url_entropy", "num_suspicious_words",
    "has_redirect", "path_length", "brand_in_subdomain",
]

MODEL_COLORS = {
    "Logistic Regression": "#4a9eff",
    "Random Forest":       "#10b981",
    "Gradient Boosting":   "#a855f7",
}


def _style(ax, title):
    ax.set_facecolor("#1a1a2e")
    ax.tick_params(colors="#aaaaaa", labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor("#2a2a4a")
    ax.set_title(title, color="white", fontsize=9, fontweight="bold", pad=6)
    ax.grid(True, color="#2a2a4a", linewidth=0.4, alpha=0.7)


def load_data(path):
    df = pd.read_csv(path)
    X  = df[FEATURE_COLS].values
    y  = df["label"].values
    return df, X, y


def train_and_evaluate(X_train, X_test, y_train, y_test):
    scaler = StandardScaler()
    Xtr_sc = scaler.fit_transform(X_train)
    Xte_sc = scaler.transform(X_test)

    specs = {
        "Logistic Regression": (LogisticRegression(max_iter=500, random_state=42),
                                Xtr_sc, Xte_sc),
        "Random Forest":       (RandomForestClassifier(n_estimators=100, random_state=42),
                                X_train, X_test),
        "Gradient Boosting":   (GradientBoostingClassifier(n_estimators=100, random_state=42),
                                X_train, X_test),
    }

    results = {}
    for name, (clf, Xtr, Xte) in specs.items():
        clf.fit(Xtr, y_train)
        y_pred = clf.predict(Xte)
        y_prob = clf.predict_proba(Xte)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        results[name] = dict(
            clf=clf, y_pred=y_pred, y_prob=y_prob,
            fpr=fpr, tpr=tpr, auc=auc(fpr, tpr),
            cm=confusion_matrix(y_test, y_pred),
            precision=precision_score(y_test, y_pred),
            recall=recall_score(y_test, y_pred),
            f1=f1_score(y_test, y_pred),
        )
        print(f"\n  {name}  (AUC={results[name]['auc']:.4f})")
        print(classification_report(y_test, y_pred,
                                    target_names=["Benign", "Phishing"], indent=4))
    return results


def dashboard(results, df_full, y_full, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    names = list(results.keys())

    fig = plt.figure(figsize=(18, 11), facecolor="#0f0f1a")
    fig.suptitle("Phishing URL Classifier — Model Comparison",
                 color="white", fontsize=15, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.46, wspace=0.38)

    # Plot 1 — ROC curves
    ax = fig.add_subplot(gs[0, 0])
    for name, res in results.items():
        ax.plot(res["fpr"], res["tpr"], color=MODEL_COLORS[name], linewidth=2,
                label=f"{name}  AUC={res['auc']:.3f}")
    ax.plot([0, 1], [0, 1], "w--", alpha=0.3, linewidth=1)
    ax.set_xlabel("False Positive Rate", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("True Positive Rate",  color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.7)
    _style(ax, "ROC Curves — All Models")

    # Plot 2 — Random Forest feature importance
    ax = fig.add_subplot(gs[0, 1])
    imp = results["Random Forest"]["clf"].feature_importances_
    idx = np.argsort(imp)
    ax.barh(range(len(idx)), imp[idx],
            color=["#ff4a4a" if imp[i] > np.median(imp) else "#4a9eff" for i in idx],
            alpha=0.85)
    ax.set_yticks(range(len(idx)))
    ax.set_yticklabels([FEATURE_COLS[i] for i in idx], fontsize=6, color="#aaaaaa")
    ax.set_xlabel("Importance", color="#aaaaaa", fontsize=8)
    ax.grid(axis="x", color="#2a2a4a", linewidth=0.4)
    _style(ax, "Feature Importance (Random Forest)")

    # Plot 3 — Confusion matrix of best-AUC model
    ax  = fig.add_subplot(gs[0, 2])
    best = max(results, key=lambda k: results[k]["auc"])
    cm   = results[best]["cm"]
    ax.imshow(cm, cmap="Blues", aspect="auto")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white", fontsize=16, fontweight="bold")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["Benign", "Phishing"], color="#aaaaaa")
    ax.set_yticklabels(["Benign", "Phishing"], color="#aaaaaa")
    ax.set_xlabel("Predicted", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Actual",    color="#aaaaaa", fontsize=8)
    _style(ax, f"Confusion Matrix — {best}")

    # Plot 4 — AUC bar chart
    ax = fig.add_subplot(gs[1, 0])
    aucs = [results[n]["auc"] for n in names]
    bars = ax.bar(range(len(names)), aucs,
                  color=[MODEL_COLORS[n] for n in names], alpha=0.85, width=0.5)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([n.replace(" ", "\n") for n in names], color="#aaaaaa", fontsize=8)
    ax.set_ylim(0.85, 1.0); ax.set_ylabel("AUC", color="#aaaaaa", fontsize=8)
    for bar, val in zip(bars, aucs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                f"{val:.4f}", ha="center", va="bottom", color="white", fontsize=9)
    _style(ax, "AUC Comparison")

    # Plot 5 — Precision / Recall / F1 grouped bar
    ax = fig.add_subplot(gs[1, 1])
    x = np.arange(len(names)); w = 0.25
    ax.bar(x - w, [results[n]["precision"] for n in names], w,
           label="Precision", color="#4a9eff", alpha=0.85)
    ax.bar(x,     [results[n]["recall"]    for n in names], w,
           label="Recall",    color="#10b981", alpha=0.85)
    ax.bar(x + w, [results[n]["f1"]        for n in names], w,
           label="F1",        color="#a855f7", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace(" ", "\n") for n in names], color="#aaaaaa", fontsize=8)
    ax.set_ylim(0.85, 1.0); ax.set_ylabel("Score", color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=7, facecolor="#1a1a2e", labelcolor="white", framealpha=0.7)
    _style(ax, "Precision / Recall / F1")

    # Plot 6 — URL length distribution by class
    ax = fig.add_subplot(gs[1, 2])
    ax.hist(df_full[y_full == 0]["url_length"], bins=40, alpha=0.6,
            color="#4a9eff", label="Benign",   density=True)
    ax.hist(df_full[y_full == 1]["url_length"], bins=40, alpha=0.6,
            color="#ff4a4a", label="Phishing", density=True)
    ax.set_xlabel("URL Length", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Density",    color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=7, facecolor="#1a1a2e", labelcolor="white", framealpha=0.7)
    _style(ax, "URL Length Distribution by Class")

    path = os.path.join(out_dir, "phishing_dashboard.png")
    plt.savefig(path, dpi=130, bbox_inches="tight", facecolor="#0f0f1a")
    plt.close()
    print(f"Dashboard  →  {path}")


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Data not found: {DATA_PATH}\nRun:  python syndata.py")
        sys.exit(1)

    print("Loading URL feature data …")
    df, X, y = load_data(DATA_PATH)
    print(f"  {len(df):,} records  |  benign: {(y==0).sum()}, phishing: {(y==1).sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)

    print("\nTraining and evaluating models …")
    results = train_and_evaluate(X_train, X_test, y_train, y_test)

    print("\nBuilding dashboard …")
    dashboard(results, df, y, OUT_DIR)
    print("\nDone.")


if __name__ == "__main__":
    main()
