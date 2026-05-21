#!/usr/bin/env python3
"""
Generate 7 days of synthetic SIEM alerts with 3 embedded attack campaigns.

Campaign 1 — Phishing → Credential Theft → Lateral Movement → Exfiltration
Campaign 2 — SSH Brute Force → Successful Login → Persistence → Crypto-miner
Campaign 3 — Web App Attack (SQLi) → RCE → C2 Beacon → Data Staged

Background noise: authentication failures, port scans, AV detections, policy violations.
"""
import argparse
import os
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

COLS = [
    "alert_id", "timestamp", "severity", "category",
    "rule_name", "src_ip", "dst_ip", "affected_host",
    "mitre_tactic", "campaign_id", "label",
]

SEVERITIES   = ["Critical", "High", "Medium", "Low", "Informational"]
SEV_WEIGHTS  = [0.05, 0.15, 0.35, 0.30, 0.15]

BACKGROUND_RULES = [
    ("Low",           "network",        "Port Scan Detected",          "Reconnaissance"),
    ("Low",           "authentication", "Failed Login Attempt",        "Credential Access"),
    ("Medium",        "authentication", "Multiple Failed Logins",      "Credential Access"),
    ("Informational", "endpoint",       "USB Device Connected",        "Collection"),
    ("Low",           "application",    "Suspicious File Download",    "Initial Access"),
    ("Medium",        "network",        "DNS Query to Known Bad Domain","Command and Control"),
    ("Low",           "endpoint",       "AV Alert — PUA Detected",    "Defense Evasion"),
    ("Informational", "application",    "Policy Violation — Torrent",  "Exfiltration"),
    ("Medium",        "network",        "Outbound Connection on High Port","Command and Control"),
    ("Low",           "authentication", "Account Locked Out",          "Credential Access"),
]

INTERNAL = [f"10.1.{b}.{h}" for b in range(1, 4) for h in range(10, 30)]
EXTERNAL = ["192.0.2.50", "198.51.100.12", "203.0.113.88",
            "93.184.216.34", "151.101.1.140"]


def _aid():
    return str(uuid.uuid4())[:8].upper()


def _ts(base, rng, spread_s):
    return base + timedelta(seconds=float(rng.uniform(0, spread_s)))


def gen_background(n_per_day, base, rng):
    rows = []
    for d in range(7):
        day = base + timedelta(days=d)
        for _ in range(n_per_day):
            sev, cat, rule, tactic = rng.choice(BACKGROUND_RULES)
            src = rng.choice(INTERNAL + EXTERNAL[:3])
            dst = rng.choice(INTERNAL)
            rows.append([
                _aid(), _ts(day, rng, 86400), sev, cat, rule,
                src, dst, rng.choice(INTERNAL),
                tactic, None, "background",
            ])
    return rows


def gen_campaign1(base, rng):
    """Phishing → cred theft → lateral movement → data exfiltration (days 1–4)."""
    cid  = "C1"
    attk = "192.0.2.50"
    vic1 = "10.1.1.15"   # phishing victim
    vic2 = "10.1.2.22"   # lateral movement target
    rows = []
    sequence = [
        (0,  8,  "High",     "email",          "Phishing Email Opened",             attk, vic1, vic1, "Initial Access"),
        (0, 10,  "High",     "endpoint",       "Credential Harvesting Tool Detected",attk, vic1, vic1, "Credential Access"),
        (1,  9,  "Critical", "authentication", "Successful Login — Unusual Time",   vic1, vic2, vic2, "Lateral Movement"),
        (1, 11,  "High",     "network",        "Internal Port Scan",                vic1, vic2, vic2, "Discovery"),
        (2, 14,  "Critical", "endpoint",       "Scheduled Task Created",            vic1, vic2, vic2, "Persistence"),
        (3, 22,  "Critical", "network",        "Large Outbound Transfer",           vic2, attk, vic2, "Exfiltration"),
        (4,  1,  "High",     "network",        "C2 Beacon Detected",                vic2, attk, vic2, "Command and Control"),
    ]
    for day_off, hr, sev, cat, rule, src, dst, host, tactic in sequence:
        ts = base + timedelta(days=day_off, hours=hr,
                              minutes=int(rng.integers(0, 30)))
        rows.append([_aid(), ts, sev, cat, rule, src, dst, host, tactic, cid, "campaign"])
    return rows


def gen_campaign2(base, rng):
    """SSH brute force → successful login → persistence → crypto-miner (days 2–5)."""
    cid  = "C2"
    attk = "198.51.100.12"
    tgt  = "10.1.1.5"
    rows = []
    # brute force: 50 rapid failures
    ts = base + timedelta(days=2, hours=3)
    for _ in range(50):
        ts += timedelta(seconds=float(rng.uniform(1, 8)))
        rows.append([_aid(), ts, "Medium", "authentication",
                     "SSH Failed Login", attk, tgt, tgt,
                     "Credential Access", cid, "campaign"])
    # success
    ts += timedelta(seconds=5)
    rows.append([_aid(), ts, "Critical", "authentication",
                 "SSH Successful Login After Brute Force", attk, tgt, tgt,
                 "Initial Access", cid, "campaign"])
    # persistence
    ts += timedelta(hours=1)
    rows.append([_aid(), ts, "High", "endpoint",
                 "Crontab Modified by Non-Root", attk, tgt, tgt,
                 "Persistence", cid, "campaign"])
    # crypto-miner
    ts += timedelta(hours=2)
    rows.append([_aid(), ts, "High", "endpoint",
                 "Crypto-Miner Process Detected", attk, tgt, tgt,
                 "Impact", cid, "campaign"])
    rows.append([_aid(), ts + timedelta(minutes=10), "High", "network",
                 "Outbound Mining Pool Traffic", tgt, "203.0.113.88", tgt,
                 "Command and Control", cid, "campaign"])
    return rows


def gen_campaign3(base, rng):
    """SQLi on web server → RCE → C2 beaconing → staged data (days 4–6)."""
    cid  = "C3"
    attk = "203.0.113.88"
    web  = "10.1.3.10"
    db   = "10.1.3.11"
    rows = []
    sequence = [
        (4,  9, "High",     "application",    "SQL Injection Attempt Detected",   attk, web, web, "Initial Access"),
        (4, 10, "Critical", "application",    "Web Shell Uploaded",               attk, web, web, "Execution"),
        (4, 11, "High",     "network",        "Unexpected Outbound Connection",   web,  attk, web, "Command and Control"),
        (5,  2, "Critical", "network",        "C2 Beacon — Regular Interval",     web,  attk, web, "Command and Control"),
        (5,  8, "High",     "endpoint",       "DB Dump Command Executed",         web,  db,  db,  "Collection"),
        (6, 23, "Critical", "network",        "Large Encrypted Upload to C2",     web,  attk, web, "Exfiltration"),
    ]
    for day_off, hr, sev, cat, rule, src, dst, host, tactic in sequence:
        ts = base + timedelta(days=day_off, hours=hr,
                              minutes=int(rng.integers(0, 20)))
        rows.append([_aid(), ts, sev, cat, rule, src, dst, host, tactic, cid, "campaign"])
    return rows


def main():
    ap = argparse.ArgumentParser(description="Generate synthetic SIEM alerts")
    ap.add_argument("--seed",       type=int, default=42)
    ap.add_argument("--bg-per-day", type=int, default=200,
                    help="background alerts per day (default 200)")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "data", "siem_alerts.csv"))
    args = ap.parse_args()

    rng  = np.random.default_rng(args.seed)
    base = datetime(2026, 5, 15, 0, 0, 0)

    rows = (gen_background(args.bg_per_day, base, rng) +
            gen_campaign1(base, rng) +
            gen_campaign2(base, rng) +
            gen_campaign3(base, rng))

    df = (pd.DataFrame(rows, columns=COLS)
            .sort_values("timestamp")
            .reset_index(drop=True))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, index=False)

    print(f"Generated {len(df):,} alerts  →  {args.out}")
    vc = df["label"].value_counts()
    print(f"  background : {vc.get('background', 0):>5}")
    print(f"  campaign   : {vc.get('campaign',   0):>5}")
    print(f"  campaigns  : {df[df['campaign_id'].notna()]['campaign_id'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
