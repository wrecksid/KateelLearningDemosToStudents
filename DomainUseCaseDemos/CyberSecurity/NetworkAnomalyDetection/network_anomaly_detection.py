#!/usr/bin/env python3
"""
Network Anomaly Detection
=========================
Detects four attack types in synthetic NetFlow data using a combination of
unsupervised ML and rule-based detectors:

  1. Isolation Forest       — general anomaly scoring on flow features
  2. Z-score (bytes_out)    — statistical exfiltration flag (z > 4)
  3. Port-scan rule         — src_ip with >20 unique dst_ports in 10-min window
  4. Beaconing detection    — (src, dst) pairs with suspiciously low inter-arrival CV

Outputs a 2×3 matplotlib dashboard to reports/network_anomaly_dashboard.png
and exits with code 1 if any critical anomalies are found.
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

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "network_flows.csv")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "reports")

FEATURES = ["bytes_out", "bytes_in", "pkts_out", "pkt_rate", "duration_ms", "bytes_ratio"]

COLORS = {
    "normal":       "#4a9eff",
    "exfiltration": "#ff4a4a",
    "port_scan":    "#ff9f00",
    "beaconing":    "#a855f7",
    "ddos":         "#ff6b35",
}


# ── helpers ──────────────────────────────────────────────────────────────────

def _style(ax, title):
    ax.set_facecolor("#1a1a2e")
    ax.tick_params(colors="#aaaaaa", labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor("#2a2a4a")
    ax.set_title(title, color="white", fontsize=9, fontweight="bold", pad=6)
    ax.grid(True, color="#2a2a4a", linewidth=0.4, alpha=0.7)


# ── 1. load & feature-engineer ───────────────────────────────────────────────

def load(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df["hour"]         = df["timestamp"].dt.hour
    df["bytes_ratio"]  = df["bytes_out"] / (df["bytes_in"] + 1)
    df["pkt_rate"]     = (df["pkts_out"] + df["pkts_in"]) / (df["duration_ms"] / 1000 + 0.001)
    df["bytes_per_pkt"]= df["bytes_out"] / (df["pkts_out"] + 1)
    return df


# ── 2. Isolation Forest ───────────────────────────────────────────────────────

def isolation_forest(df, contamination=0.05):
    X = df[FEATURES].copy()
    for col in ["bytes_out", "bytes_in", "pkts_out", "pkt_rate"]:
        X[col] = np.log1p(X[col])
    Xs = StandardScaler().fit_transform(X)
    clf = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
    clf.fit(Xs)
    df = df.copy()
    df["if_score"] = clf.decision_function(Xs)
    df["if_flag"]  = clf.predict(Xs) == -1
    return df


# ── 3. Z-score exfiltration ───────────────────────────────────────────────────

def zscore_exfil(df, threshold=4.0):
    df = df.copy()
    mu, sigma = df["bytes_out"].mean(), df["bytes_out"].std()
    df["z_bytes"]    = (df["bytes_out"] - mu) / (sigma + 1e-9)
    df["zscore_flag"] = df["z_bytes"] > threshold
    return df


# ── 4. Port-scan detection ────────────────────────────────────────────────────

def port_scan(df, window="10min", threshold=20):
    df = df.copy()
    df["tbin"] = df["timestamp"].dt.floor(window)
    grp = (df.groupby(["src_ip", "tbin"])["dst_port"]
             .nunique()
             .reset_index(name="unique_dst_ports"))
    flagged = set(zip(grp[grp["unique_dst_ports"] >= threshold]["src_ip"],
                      grp[grp["unique_dst_ports"] >= threshold]["tbin"]))
    df["portscan_flag"] = [
        (r.src_ip, r.tbin) in flagged for r in df.itertuples()
    ]
    return df, grp


# ── 5. Beaconing detection ────────────────────────────────────────────────────

def beaconing(df, min_conn=10, max_cv=0.05):
    df = df.copy()
    pairs = set()
    for (src, dst), g in df.groupby(["src_ip", "dst_ip"]):
        if len(g) < min_conn:
            continue
        intervals = g["timestamp"].sort_values().diff().dt.total_seconds().dropna()
        if len(intervals) < min_conn - 1:
            continue
        cv = intervals.std() / (intervals.mean() + 1e-9)
        if cv < max_cv:
            pairs.add((src, dst))
    df["beacon_flag"] = [(r.src_ip, r.dst_ip) in pairs for r in df.itertuples()]
    return df, pairs


# ── 6. Dashboard ──────────────────────────────────────────────────────────────

def dashboard(df, grp, beacon_pairs, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fig = plt.figure(figsize=(18, 11), facecolor="#0f0f1a")
    fig.suptitle("Network Anomaly Detection Dashboard",
                 color="white", fontsize=15, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.46, wspace=0.35)

    # Plot 1 — hourly flow volume stacked by type
    ax = fig.add_subplot(gs[0, 0])
    hourly = df.groupby(["hour", "label"]).size().unstack(fill_value=0)
    bottom = np.zeros(24)
    for lbl in hourly.columns:
        vals = hourly[lbl].reindex(range(24), fill_value=0).values
        ax.bar(range(24), vals, bottom=bottom,
               color=COLORS.get(lbl, "#888"), alpha=0.85, label=lbl, width=0.8)
        bottom += vals
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    ax.set_xlabel("Hour of Day", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Flow Count",  color="#aaaaaa", fontsize=8)
    _style(ax, "Hourly Flow Volume by Type")

    # Plot 2 — bytes_out distribution (log scale) by type
    ax = fig.add_subplot(gs[0, 1])
    for lbl in df["label"].unique():
        vals = df[df["label"] == lbl]["bytes_out"].clip(lower=1)
        ax.hist(np.log10(vals), bins=40, alpha=0.55, density=True,
                color=COLORS.get(lbl, "#888"), label=lbl)
    ax.set_xlabel("log₁₀(Bytes Out)", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Density",          color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Bytes-Out Distribution (log scale)")

    # Plot 3 — Isolation Forest score histogram
    ax = fig.add_subplot(gs[0, 2])
    ax.hist(df[~df["if_flag"]]["if_score"], bins=50, alpha=0.7,
            color="#4a9eff", label="Normal", density=True)
    ax.hist(df[df["if_flag"]]["if_score"],  bins=50, alpha=0.8,
            color="#ff4a4a", label="Flagged", density=True)
    ax.axvline(0, color="white", linewidth=1, linestyle="--", alpha=0.5)
    ax.set_xlabel("IF Anomaly Score", color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Density",          color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=7, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Isolation Forest Score Distribution")

    # Plot 4 — port scan: top source IPs by unique dst_ports
    ax = fig.add_subplot(gs[1, 0])
    top = grp.sort_values("unique_dst_ports", ascending=False).head(15)
    colors_ps = ["#ff4a4a" if p >= 20 else "#4a9eff"
                 for p in top["unique_dst_ports"]]
    ax.barh(range(len(top)), top["unique_dst_ports"], color=colors_ps, alpha=0.85)
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(
        [f"{r.src_ip}  {r.tbin.strftime('%H:%M')}" for r in top.itertuples()],
        fontsize=6, color="#aaaaaa")
    ax.axvline(20, color="#ff4a4a", linestyle="--", linewidth=1,
               label="Threshold (20 ports)")
    ax.set_xlabel("Unique Dst Ports / 10-min window", color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Port-Scan Detection (Top Source IPs)")

    # Plot 5 — beaconing: inter-arrival coefficient of variation
    ax = fig.add_subplot(gs[1, 1])
    pair_cvs, pair_beacons = [], []
    for (src, dst), g in df.groupby(["src_ip", "dst_ip"]):
        if len(g) < 5:
            continue
        ivs = g["timestamp"].sort_values().diff().dt.total_seconds().dropna()
        if len(ivs) == 0:
            continue
        cv = ivs.std() / (ivs.mean() + 1e-9)
        pair_cvs.append(min(cv, 5))
        pair_beacons.append((src, dst) in beacon_pairs)
    if pair_cvs:
        normal_cv  = [c for c, b in zip(pair_cvs, pair_beacons) if not b]
        beacon_cv  = [c for c, b in zip(pair_cvs, pair_beacons) if b]
        ax.scatter(range(len(normal_cv)), normal_cv,
                   color="#4a9eff", s=8, alpha=0.5, label="Normal pairs")
        if beacon_cv:
            ax.scatter(range(len(normal_cv), len(normal_cv) + len(beacon_cv)),
                       beacon_cv, color="#a855f7", s=30, alpha=0.9, label="Beaconing")
        ax.axhline(0.05, color="#ff9f00", linestyle="--", linewidth=1,
                   label="CV threshold (0.05)")
    ax.set_xlabel("(src, dst) Pair Index",         color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Inter-Arrival CV",              color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Beaconing Detection (Inter-Arrival Regularity)")

    # Plot 6 — summary: flagged counts per detector
    ax = fig.add_subplot(gs[1, 2])
    det_names   = ["Isolation\nForest", "Z-score\n(bytes)", "Port\nScan", "Beaconing"]
    det_counts  = [int(df["if_flag"].sum()), int(df["zscore_flag"].sum()),
                   int(df["portscan_flag"].sum()), int(df["beacon_flag"].sum())]
    bar_colors  = ["#ff4a4a", "#ff9f00", "#a855f7", "#10b981"]
    bars = ax.bar(range(4), det_counts, color=bar_colors, alpha=0.85, width=0.5)
    ax.set_xticks(range(4))
    ax.set_xticklabels(det_names, color="#aaaaaa", fontsize=8)
    ax.set_ylabel("Flows Flagged", color="#aaaaaa", fontsize=8)
    for bar, val in zip(bars, det_counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                str(val), ha="center", va="bottom", color="white", fontsize=9)
    _style(ax, "Flows Flagged per Detector")

    path = os.path.join(out_dir, "network_anomaly_dashboard.png")
    plt.savefig(path, dpi=130, bbox_inches="tight", facecolor="#0f0f1a")
    plt.close()
    print(f"Dashboard  →  {path}")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(DATA_PATH):
        print(f"Data not found: {DATA_PATH}\nRun:  python syndata.py")
        sys.exit(1)

    print("Loading flows …")
    df = load(DATA_PATH)
    print(f"  {len(df):,} flows  |  {df['label'].value_counts().to_dict()}")

    print("Isolation Forest …")
    df = isolation_forest(df)
    print("Z-score exfiltration detector …")
    df = zscore_exfil(df)
    print("Port-scan detector …")
    df, grp = port_scan(df)
    print("Beaconing detector …")
    df, beacon_pairs = beaconing(df)

    gt_anomalies = int((df["label"] != "normal").sum())
    print("\n── Detection Summary ─────────────────────────────────")
    print(f"  Isolation Forest flagged : {df['if_flag'].sum():>5}")
    print(f"  Z-score flagged          : {df['zscore_flag'].sum():>5}")
    print(f"  Port-scan flagged        : {df['portscan_flag'].sum():>5}")
    print(f"  Beaconing flagged        : {df['beacon_flag'].sum():>5}")
    print(f"  Ground-truth anomalies   : {gt_anomalies:>5}")
    if df["if_flag"].sum() > 0:
        prec = (df[df["if_flag"]]["label"] != "normal").mean()
        print(f"  IF precision (vs label)  : {prec:.1%}")

    print("\nBuilding dashboard …")
    dashboard(df, grp, beacon_pairs, OUT_DIR)

    critical = any([df["if_flag"].sum(), df["portscan_flag"].sum(),
                    df["beacon_flag"].sum(), df["zscore_flag"].sum()])
    print("\nCRITICAL anomalies detected — review dashboard." if critical
          else "\nNo anomalies detected.")
    return 1 if critical else 0


if __name__ == "__main__":
    sys.exit(main())
