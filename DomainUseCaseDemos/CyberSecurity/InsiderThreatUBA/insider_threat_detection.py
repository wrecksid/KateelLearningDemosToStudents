#!/usr/bin/env python3
"""
Insider Threat Detection via User Behaviour Analytics (UBA)
===========================================================
Pipeline:
  1. Build a per-user baseline from the first 60 days of activity.
  2. Score the final 30 days against that baseline using Z-scores.
  3. Compute a composite risk score (weighted sum of anomaly indicators).
  4. Run Isolation Forest across all user-day feature vectors for a
     complementary unsupervised view.
  5. Produce a 2×3 dashboard: risk heatmap, timelines, and feature breakdowns.

Three embedded threats:
  user_003 — disgruntled: after-hours spikes + USB events
  user_017 — malicious:   data-download explosion + external email surge
  user_031 — compromised: login-hour shift + new-location logins
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "user_activity.csv")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "reports")

BEHAVIOUR_FEATURES = [
    "login_hour", "data_downloaded_mb", "external_emails_sent",
    "usb_events", "after_hours", "new_location_login", "files_accessed",
]
RISK_WEIGHTS = {
    "after_hours":          3.0,
    "new_location_login":   4.0,
    "usb_events":           2.5,
    "data_downloaded_mb":   2.0,
    "external_emails_sent": 1.5,
    "files_accessed":       1.0,
    "login_hour":           1.0,
}
THREAT_COLORS = {
    "normal":      "#4a9eff",
    "disgruntled": "#ff9f00",
    "malicious":   "#ff4a4a",
    "compromised": "#a855f7",
}


def _style(ax, title):
    ax.set_facecolor("#1a1a2e")
    ax.tick_params(colors="#aaaaaa", labelsize=7)
    for sp in ax.spines.values():
        sp.set_edgecolor("#2a2a4a")
    ax.set_title(title, color="white", fontsize=9, fontweight="bold", pad=6)
    ax.grid(True, color="#2a2a4a", linewidth=0.4, alpha=0.7)


def load(path):
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def build_baselines(df, baseline_days=60):
    """Compute per-user mean and std from first `baseline_days` calendar days."""
    cutoff = df["date"].min() + pd.Timedelta(days=baseline_days)
    base   = df[df["date"] < cutoff]
    stats  = base.groupby("user_id")[BEHAVIOUR_FEATURES].agg(["mean", "std"])
    stats.columns = ["_".join(c) for c in stats.columns]
    return stats, cutoff


def score_recent(df, stats, cutoff):
    """Z-score each behaviour feature for each user-day after the cutoff."""
    recent = df[df["date"] >= cutoff].copy()
    for feat in BEHAVIOUR_FEATURES:
        mu_col  = f"{feat}_mean"
        std_col = f"{feat}_std"
        mu   = recent["user_id"].map(stats[mu_col])
        sig  = recent["user_id"].map(stats[std_col]).fillna(1).clip(lower=0.5)
        recent[f"z_{feat}"] = (recent[feat] - mu) / sig

    z_cols = [f"z_{f}" for f in BEHAVIOUR_FEATURES]
    weights = np.array([RISK_WEIGHTS[f] for f in BEHAVIOUR_FEATURES])
    z_vals  = recent[z_cols].clip(lower=0).values
    recent["risk_score"] = (z_vals * weights).sum(axis=1)
    return recent


def run_isolation_forest(df):
    X  = df[BEHAVIOUR_FEATURES].values
    Xs = StandardScaler().fit_transform(X)
    clf = IsolationForest(contamination=0.06, random_state=42, n_estimators=100)
    clf.fit(Xs)
    df = df.copy()
    df["if_score"] = clf.decision_function(Xs)
    df["if_flag"]  = clf.predict(Xs) == -1
    return df


def dashboard(df_all, df_recent, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fig = plt.figure(figsize=(18, 11), facecolor="#0f0f1a")
    fig.suptitle("Insider Threat Detection — User Behaviour Analytics",
                 color="white", fontsize=15, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.48, wspace=0.38)

    # Plot 1 — Top 20 users by mean daily risk score (recent window)
    ax = fig.add_subplot(gs[0, 0])
    top20 = (df_recent.groupby(["user_id", "label"])["risk_score"]
             .mean().reset_index()
             .sort_values("risk_score", ascending=False).head(20))
    colors = [THREAT_COLORS.get(l, "#4a9eff") for l in top20["label"]]
    ax.barh(range(len(top20)), top20["risk_score"], color=colors, alpha=0.85)
    ax.set_yticks(range(len(top20)))
    ax.set_yticklabels(top20["user_id"], fontsize=6, color="#aaaaaa")
    ax.set_xlabel("Mean Daily Risk Score", color="#aaaaaa", fontsize=8)
    patches = [plt.Rectangle((0, 0), 1, 1, color=v, alpha=0.8)
               for v in THREAT_COLORS.values()]
    ax.legend(patches, list(THREAT_COLORS.keys()),
              fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Top 20 Users by Risk Score (Recent 30 Days)")

    # Plot 2 — Risk score timeline for top 3 threat users
    ax = fig.add_subplot(gs[0, 1])
    threat_users = ["user_003", "user_017", "user_031"]
    for uid in threat_users:
        sub = df_recent[df_recent["user_id"] == uid].sort_values("date")
        lbl = sub["label"].iloc[0] if len(sub) else "normal"
        ax.plot(sub["date"], sub["risk_score"],
                color=THREAT_COLORS.get(lbl, "#888"),
                linewidth=1.5, marker="o", markersize=3, label=f"{uid} ({lbl})")
    ax.set_xlabel("Date", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Risk Score", color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.7)
    ax.tick_params(axis="x", rotation=30)
    _style(ax, "Risk Score Timeline — Threat Users")

    # Plot 3 — Data downloaded MB over time for malicious user vs normal avg
    ax = fig.add_subplot(gs[0, 2])
    mal = df_all[df_all["user_id"] == "user_017"].sort_values("date")
    norm_avg = (df_all[~df_all["user_id"].isin(threat_users)]
                .groupby("date")["data_downloaded_mb"].mean().reset_index())
    ax.plot(mal["date"], mal["data_downloaded_mb"],
            color="#ff4a4a", linewidth=1.5, label="user_017 (malicious)")
    ax.plot(norm_avg["date"], norm_avg["data_downloaded_mb"],
            color="#4a9eff", linewidth=1, linestyle="--", label="Normal avg")
    ax.set_xlabel("Date", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Data Downloaded (MB)", color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.7)
    ax.tick_params(axis="x", rotation=30)
    _style(ax, "Data Exfiltration Signal — user_017")

    # Plot 4 — After-hours and USB events for disgruntled user
    ax = fig.add_subplot(gs[1, 0])
    dis = df_all[df_all["user_id"] == "user_003"].sort_values("date")
    ax2 = ax.twinx()
    ax.bar(dis["date"], dis["after_hours"], color="#ff9f00", alpha=0.6,
           label="After-hours", width=1)
    ax2.plot(dis["date"], dis["usb_events"], color="#a855f7", linewidth=1.5,
             marker="o", markersize=3, label="USB events")
    ax.set_ylabel("After-Hours (0/1)", color="#ff9f00", fontsize=8)
    ax2.set_ylabel("USB Events",       color="#a855f7",  fontsize=8)
    ax2.tick_params(colors="#a855f7", labelsize=7)
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labs1 + labs2,
              fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    ax.tick_params(axis="x", rotation=30, colors="#aaaaaa", labelsize=7)
    _style(ax, "Disgruntled Signals — user_003")

    # Plot 5 — Login hour distribution: compromised vs normal
    ax = fig.add_subplot(gs[1, 1])
    comp   = df_all[df_all["user_id"] == "user_031"]["login_hour"]
    normal = df_all[~df_all["user_id"].isin(threat_users)]["login_hour"]
    ax.hist(normal, bins=range(0, 25), alpha=0.6, color="#4a9eff",
            label="Normal users", density=True)
    ax.hist(comp,   bins=range(0, 25), alpha=0.7, color="#a855f7",
            label="user_031 (compromised)", density=True)
    ax.set_xlabel("Login Hour", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Density",    color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.7)
    _style(ax, "Login Hour Distribution — Compromised vs Normal")

    # Plot 6 — Isolation Forest flags by user
    ax = fig.add_subplot(gs[1, 2])
    if_by_user = (df_all.groupby(["user_id", "label"])["if_flag"]
                  .sum().reset_index()
                  .sort_values("if_flag", ascending=False).head(15))
    colors_if = [THREAT_COLORS.get(l, "#4a9eff") for l in if_by_user["label"]]
    ax.barh(range(len(if_by_user)), if_by_user["if_flag"],
            color=colors_if, alpha=0.85)
    ax.set_yticks(range(len(if_by_user)))
    ax.set_yticklabels(if_by_user["user_id"], fontsize=6, color="#aaaaaa")
    ax.set_xlabel("Days Flagged by Isolation Forest", color="#aaaaaa", fontsize=8)
    _style(ax, "Isolation Forest Flags per User")

    path = os.path.join(out_dir, "insider_threat_dashboard.png")
    plt.savefig(path, dpi=130, bbox_inches="tight", facecolor="#0f0f1a")
    plt.close()
    print(f"Dashboard  →  {path}")


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Data not found: {DATA_PATH}\nRun:  python syndata.py")
        sys.exit(1)

    print("Loading user activity …")
    df = load(DATA_PATH)
    print(f"  {len(df):,} records  |  {df['label'].value_counts().to_dict()}")

    print("Building per-user baselines …")
    stats, cutoff = build_baselines(df)
    print(f"  Baseline cutoff: {cutoff.date()}  |  {len(stats)} users profiled")

    print("Scoring recent behaviour …")
    df_recent = score_recent(df, stats, cutoff)

    print("Running Isolation Forest on full history …")
    df = run_isolation_forest(df)

    print("\n── Top 5 Highest-Risk Users (recent 30 days) ────────────")
    top5 = (df_recent.groupby(["user_id", "label"])["risk_score"]
            .mean().sort_values(ascending=False).head(5))
    for (uid, lbl), score in top5.items():
        print(f"  {uid:<12}  {lbl:<15}  risk_score={score:.1f}")

    print("\nBuilding dashboard …")
    dashboard(df, df_recent, OUT_DIR)
    print("\nDone.")

    return 1 if top5.iloc[0] > 10 else 0


if __name__ == "__main__":
    sys.exit(main())
