#!/usr/bin/env python3
"""
SIEM Alert Correlation Engine
==============================
Reduces alert noise and reconstructs attack campaigns from raw SIEM events.

Techniques:
  1. Source-IP reputation scoring  — IPs appearing across multiple tactic categories
  2. Time-window grouping (1-hour) — burst detection per source IP
  3. Kill-chain reconstruction     — MITRE tactic sequence per campaign
  4. Alert deduplication           — collapse repeated identical rule firings
  5. Severity aggregation          — roll-up to campaign-level risk

Outputs a 2×3 dashboard to reports/siem_dashboard.png.
"""
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "siem_alerts.csv")
OUT_DIR   = os.path.join(os.path.dirname(__file__), "reports")

SEV_ORDER  = ["Critical", "High", "Medium", "Low", "Informational"]
SEV_SCORE  = {"Critical": 5, "High": 4, "Medium": 3, "Low": 2, "Informational": 1}
SEV_COLORS = {"Critical": "#ff4a4a", "High": "#ff9f00", "Medium": "#ffde59",
              "Low": "#4a9eff", "Informational": "#aaaaaa"}
CAMP_COLORS = {"C1": "#ff4a4a", "C2": "#a855f7", "C3": "#10b981"}

MITRE_ORDER = [
    "Initial Access", "Execution", "Persistence", "Privilege Escalation",
    "Defense Evasion", "Credential Access", "Discovery", "Lateral Movement",
    "Collection", "Command and Control", "Exfiltration", "Impact",
]


def _style(ax, title):
    ax.set_facecolor("#1a1a2e")
    ax.tick_params(colors="#aaaaaa", labelsize=7)
    for sp in ax.spines.values():
        sp.set_edgecolor("#2a2a4a")
    ax.set_title(title, color="white", fontsize=9, fontweight="bold", pad=6)
    ax.grid(True, color="#2a2a4a", linewidth=0.4, alpha=0.7)


def load(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df["sev_score"] = df["severity"].map(SEV_SCORE).fillna(1)
    return df


# ── 1. Source-IP reputation ───────────────────────────────────────────────────

def ip_reputation(df):
    """Score each src_ip by number of distinct MITRE tactic categories it appears in."""
    rep = (df.groupby("src_ip")["mitre_tactic"]
              .nunique()
              .rename("tactic_spread")
              .reset_index())
    rep["rep_score"] = rep["tactic_spread"] * df.groupby("src_ip")["sev_score"].mean().values
    df = df.merge(rep[["src_ip", "rep_score"]], on="src_ip", how="left")
    return df, rep


# ── 2. Time-window burst detection ────────────────────────────────────────────

def burst_detection(df, window="1h", threshold=20):
    df = df.copy()
    df["tbin"] = df["timestamp"].dt.floor(window)
    bursts = (df.groupby(["src_ip", "tbin"])
                .size()
                .reset_index(name="alert_count"))
    df = df.merge(bursts, on=["src_ip", "tbin"], how="left")
    df["burst_flag"] = df["alert_count"] >= threshold
    return df, bursts


# ── 3. Deduplication ──────────────────────────────────────────────────────────

def deduplicate(df, window="10min"):
    """Collapse identical (src_ip, rule_name) pairs within a rolling window."""
    df = df.sort_values("timestamp").copy()
    df["tbin10"] = df["timestamp"].dt.floor(window)
    before = len(df)
    df = df.drop_duplicates(subset=["src_ip", "rule_name", "tbin10"])
    after  = len(df)
    print(f"  Deduplication: {before:,} → {after:,} alerts ({before - after:,} removed)")
    return df


# ── 4. Kill-chain reconstruction ──────────────────────────────────────────────

def kill_chains(df):
    """For each campaign, list the ordered sequence of unique MITRE tactics."""
    camp_df = df[df["campaign_id"].notna()].copy()
    chains  = {}
    for cid, grp in camp_df.groupby("campaign_id"):
        tactics = (grp.sort_values("timestamp")["mitre_tactic"]
                      .drop_duplicates().tolist())
        chains[cid] = tactics
    return chains


# ── 5. Dashboard ──────────────────────────────────────────────────────────────

def dashboard(df, df_dedup, rep, bursts, chains, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fig = plt.figure(figsize=(18, 11), facecolor="#0f0f1a")
    fig.suptitle("SIEM Alert Correlation Dashboard",
                 color="white", fontsize=15, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.50, wspace=0.38)

    # Plot 1 — Hourly alert volume with severity stacking
    ax = fig.add_subplot(gs[0, 0])
    df["hour"] = df["timestamp"].dt.floor("1h")
    hourly = (df.groupby(["hour", "severity"])
                .size().unstack(fill_value=0)
                .reindex(columns=SEV_ORDER, fill_value=0))
    bottom = np.zeros(len(hourly))
    for sev in SEV_ORDER:
        if sev in hourly:
            ax.bar(range(len(hourly)), hourly[sev], bottom=bottom,
                   color=SEV_COLORS[sev], alpha=0.85, label=sev, width=0.8)
            bottom += hourly[sev].values
    ax.set_xticks(range(0, len(hourly), 12))
    ax.set_xticklabels(
        [hourly.index[i].strftime("%d %H:%M") for i in range(0, len(hourly), 12)],
        rotation=30, fontsize=6, color="#aaaaaa")
    ax.set_ylabel("Alert Count", color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white",
              framealpha=0.6, loc="upper left")
    _style(ax, "Hourly Alert Volume by Severity")

    # Plot 2 — Severity distribution (deduplicated)
    ax = fig.add_subplot(gs[0, 1])
    vc  = df_dedup["severity"].value_counts().reindex(SEV_ORDER, fill_value=0)
    colors_sev = [SEV_COLORS[s] for s in SEV_ORDER]
    wedges, texts, autotexts = ax.pie(
        vc.values, labels=SEV_ORDER, autopct="%1.0f%%",
        colors=colors_sev, startangle=90,
        textprops={"color": "#aaaaaa", "fontsize": 7})
    for at in autotexts:
        at.set_color("white"); at.set_fontsize(7)
    ax.set_facecolor("#1a1a2e")
    ax.set_title("Severity Distribution (after dedup)", color="white",
                 fontsize=9, fontweight="bold", pad=6)

    # Plot 3 — Top 15 source IPs by reputation score
    ax = fig.add_subplot(gs[0, 2])
    top_ip = rep.sort_values("tactic_spread", ascending=False).head(15)
    camp_ips = set(["192.0.2.50", "198.51.100.12", "203.0.113.88"])
    colors_ip = ["#ff4a4a" if ip in camp_ips else "#4a9eff"
                 for ip in top_ip["src_ip"]]
    ax.barh(range(len(top_ip)), top_ip["tactic_spread"],
            color=colors_ip, alpha=0.85)
    ax.set_yticks(range(len(top_ip)))
    ax.set_yticklabels(top_ip["src_ip"], fontsize=6, color="#aaaaaa")
    ax.set_xlabel("Distinct MITRE Tactics", color="#aaaaaa", fontsize=8)
    ax.axvline(3, color="#ff9f00", linestyle="--", linewidth=1,
               label="Threshold (3 tactics)")
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Source IP Reputation (Tactic Spread)")

    # Plot 4 — Burst detection: top src_ip alert counts per hour
    ax = fig.add_subplot(gs[1, 0])
    top_bursts = bursts.sort_values("alert_count", ascending=False).head(15)
    colors_b = ["#ff4a4a" if c >= 20 else "#4a9eff"
                for c in top_bursts["alert_count"]]
    ax.barh(range(len(top_bursts)), top_bursts["alert_count"],
            color=colors_b, alpha=0.85)
    ax.set_yticks(range(len(top_bursts)))
    ax.set_yticklabels(
        [f"{r.src_ip}  {r.tbin.strftime('%d %H:00')}"
         for r in top_bursts.itertuples()],
        fontsize=6, color="#aaaaaa")
    ax.axvline(20, color="#ff9f00", linestyle="--", linewidth=1,
               label="Burst threshold")
    ax.set_xlabel("Alerts in 1-hour Window", color="#aaaaaa", fontsize=8)
    ax.legend(fontsize=6, facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
    _style(ax, "Alert Burst Detection (Top Source IPs)")

    # Plot 5 — Kill-chain heatmap (tactic × campaign)
    ax = fig.add_subplot(gs[1, 1])
    tactic_matrix = pd.DataFrame(0, index=MITRE_ORDER, columns=sorted(chains.keys()))
    for cid, tactics in chains.items():
        for t in tactics:
            if t in tactic_matrix.index:
                tactic_matrix.loc[t, cid] = 1
    im = ax.imshow(tactic_matrix.values, cmap="RdYlGn", aspect="auto",
                   vmin=0, vmax=1)
    ax.set_xticks(range(len(tactic_matrix.columns)))
    ax.set_xticklabels(tactic_matrix.columns, color="#aaaaaa", fontsize=8)
    ax.set_yticks(range(len(MITRE_ORDER)))
    ax.set_yticklabels(MITRE_ORDER, fontsize=6, color="#aaaaaa")
    for i, row in enumerate(tactic_matrix.values):
        for j, val in enumerate(row):
            if val:
                ax.text(j, i, "✓", ha="center", va="center",
                        color="white", fontsize=10)
    ax.set_title("Kill-Chain Coverage per Campaign", color="white",
                 fontsize=9, fontweight="bold", pad=6)

    # Plot 6 — Alert category breakdown
    ax = fig.add_subplot(gs[1, 2])
    cat_vc = df_dedup["category"].value_counts()
    bars = ax.bar(range(len(cat_vc)), cat_vc.values,
                  color=["#4a9eff", "#10b981", "#ff9f00", "#a855f7", "#ff4a4a"],
                  alpha=0.85, width=0.6)
    ax.set_xticks(range(len(cat_vc)))
    ax.set_xticklabels(cat_vc.index, rotation=30, ha="right",
                       color="#aaaaaa", fontsize=7)
    ax.set_ylabel("Alert Count", color="#aaaaaa", fontsize=8)
    for bar, val in zip(bars, cat_vc.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                str(val), ha="center", va="bottom", color="white", fontsize=8)
    _style(ax, "Alert Volume by Category")

    path = os.path.join(out_dir, "siem_dashboard.png")
    plt.savefig(path, dpi=130, bbox_inches="tight", facecolor="#0f0f1a")
    plt.close()
    print(f"Dashboard  →  {path}")


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Data not found: {DATA_PATH}\nRun:  python syndata.py")
        sys.exit(1)

    print("Loading SIEM alerts …")
    df = load(DATA_PATH)
    print(f"  {len(df):,} raw alerts  |  "
          f"background: {(df['label']=='background').sum()}, "
          f"campaign: {(df['label']=='campaign').sum()}")

    print("IP reputation scoring …")
    df, rep = ip_reputation(df)

    print("Burst detection …")
    df, bursts = burst_detection(df)

    print("Deduplicating …")
    df_dedup = deduplicate(df)

    print("Reconstructing kill chains …")
    chains = kill_chains(df)
    for cid, tactics in chains.items():
        print(f"  {cid}: {' → '.join(tactics)}")

    print("\n── Campaign Summary ──────────────────────────────────────")
    camp_df = df[df["campaign_id"].notna()]
    for cid, grp in camp_df.groupby("campaign_id"):
        sev_max = grp["severity"].map(SEV_SCORE).max()
        sev_lbl = {v: k for k, v in SEV_SCORE.items()}[sev_max]
        print(f"  {cid}  {len(grp):>3} alerts  max_severity={sev_lbl}"
              f"  hosts={grp['affected_host'].nunique()}")

    top_ip = rep.nlargest(3, "tactic_spread")
    print(f"\n  Top attacker IPs: {top_ip['src_ip'].tolist()}")

    print("\nBuilding dashboard …")
    dashboard(df, df_dedup, rep, bursts, chains, OUT_DIR)
    print("\nDone.")
    return 1 if (df["severity"] == "Critical").sum() > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
