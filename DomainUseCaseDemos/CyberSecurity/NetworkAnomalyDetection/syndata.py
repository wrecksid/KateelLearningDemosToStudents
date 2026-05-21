#!/usr/bin/env python3
"""
Generate synthetic NetFlow-style network flow records with embedded attack scenarios.

Scenarios embedded:
  normal       - web, DNS, SSH, email traffic from internal hosts
  exfiltration - large nightly uploads from one host to a C2 server
  port_scan    - TCP SYN scan across 200 ports from an external attacker
  beaconing    - regular 5-min heartbeat from an implanted host to C2
  ddos         - high-rate UDP flood from an internal host
"""
import argparse
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

INTERNAL = [f"10.0.{b}.{h}" for b in range(1, 5) for h in range(1, 21)]
EXTERNAL = ["93.184.216.34", "151.101.1.140", "216.58.214.206", "172.217.16.142",
            "104.244.42.65", "13.107.42.14",  "23.215.0.138",  "199.232.28.140"]
ATTACKER = ["192.0.2.15", "198.51.100.99", "203.0.113.77"]   # RFC 5737

COLS = ["timestamp", "src_ip", "dst_ip", "src_port", "dst_port", "protocol",
        "bytes_out", "bytes_in", "pkts_out", "pkts_in", "duration_ms", "label"]


def _t(base, rng, spread_s):
    return base + timedelta(seconds=float(rng.uniform(0, spread_s)))


def gen_normal(n, base, rng):
    rows = []
    for _ in range(n):
        src   = rng.choice(INTERNAL)
        dst   = rng.choice(EXTERNAL if rng.random() < 0.7 else INTERNAL[:8])
        proto = "TCP" if rng.random() < 0.82 else "UDP"
        dport = int(rng.choice([80, 443, 443, 443, 22, 53, 25, 587, 8080]))
        bo    = int(rng.lognormal(8.0, 1.5))
        bi    = int(rng.lognormal(10.0, 1.5))
        rows.append([_t(base, rng, 86400), src, dst,
                     int(rng.integers(49152, 65535)), dport, proto,
                     bo, bi, max(1, bo // 1400), max(1, bi // 1400),
                     max(1, int(rng.lognormal(6, 2))), "normal"])
    return rows


def gen_exfiltration(base, rng):
    """500 KB–2 MB chunks uploaded to C2 between 01:00 and 02:30."""
    src  = "10.0.2.15"
    dst  = ATTACKER[0]
    ts   = base.replace(hour=1, minute=0, second=0)
    rows = []
    for i in range(45):
        ts += timedelta(minutes=2, seconds=float(rng.uniform(0, 20)))
        bo  = int(rng.uniform(400_000, 2_000_000))
        rows.append([ts, src, dst, int(rng.integers(49152, 65535)), 443, "TCP",
                     bo, int(rng.uniform(100, 400)),
                     bo // 1400 + 1, 1, 20000 + int(rng.integers(0, 8000)),
                     "exfiltration"])
    return rows


def gen_port_scan(base, rng):
    """TCP SYN to 200 distinct ports on one target in ~30 seconds."""
    src  = ATTACKER[1]
    tgt  = "10.0.1.5"
    ts   = base.replace(hour=14) + timedelta(minutes=int(rng.integers(0, 30)))
    rows = []
    for port in rng.choice(range(1, 10001), size=200, replace=False):
        ts += timedelta(milliseconds=float(rng.uniform(50, 200)))
        rows.append([ts, src, tgt, int(rng.integers(49152, 65535)), int(port), "TCP",
                     60, 0, 1, 0, int(rng.uniform(40, 150)), "port_scan"])
    return rows


def gen_beaconing(base, rng):
    """C2 implant heartbeat every 300 s ± 5 s, all day."""
    src  = "10.0.3.22"
    dst  = ATTACKER[2]
    ts   = base.replace(hour=8, minute=0, second=0)
    rows = []
    for _ in range(96):
        ts += timedelta(seconds=300 + float(rng.uniform(-5, 5)))
        rows.append([ts, src, dst, int(rng.integers(49152, 65535)), 443, "TCP",
                     int(rng.uniform(80, 250)), int(rng.uniform(60, 180)),
                     1, 1, int(rng.uniform(80, 350)), "beaconing"])
    return rows


def gen_ddos(base, rng):
    """High-rate UDP flood burst — 500 packets in ~8 seconds."""
    src  = "10.0.4.9"
    dst  = EXTERNAL[0]
    ts   = base.replace(hour=21)
    rows = []
    for _ in range(500):
        ts += timedelta(milliseconds=float(rng.uniform(1, 16)))
        rows.append([ts, src, dst, int(rng.integers(49152, 65535)), 80, "UDP",
                     int(rng.uniform(60, 120)), 0, 1, 0,
                     int(rng.uniform(1, 12)), "ddos"])
    return rows


def main():
    ap = argparse.ArgumentParser(description="Generate synthetic network flow data")
    ap.add_argument("--seed",   type=int, default=42)
    ap.add_argument("--normal", type=int, default=5000,
                    help="number of normal flows (default 5000)")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "data", "network_flows.csv"))
    args = ap.parse_args()

    rng  = np.random.default_rng(args.seed)
    base = datetime(2026, 5, 21)

    rows = (gen_normal(args.normal, base, rng) +
            gen_exfiltration(base, rng) +
            gen_port_scan(base, rng) +
            gen_beaconing(base, rng) +
            gen_ddos(base, rng))

    df = (pd.DataFrame(rows, columns=COLS)
            .sort_values("timestamp")
            .reset_index(drop=True))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, index=False)

    print(f"Generated {len(df):,} flows  →  {args.out}")
    for lbl, cnt in df["label"].value_counts().items():
        tag = "⚠" if lbl != "normal" else " "
        print(f"  {tag} {lbl:<15} {cnt:>5}")


if __name__ == "__main__":
    main()
