#!/usr/bin/env python3
"""
Generate 90 days of synthetic daily user-behaviour records for 50 employees.

Three insider threat profiles are embedded:
  - user_003  disgruntled   — after-hours access and USB events spike in final 3 weeks
  - user_017  malicious     — sudden large data downloads and high external email volume
  - user_031  compromised   — login hour shifts dramatically; new-location logins appear

All other users follow stable, role-consistent behavioural baselines.
"""
import argparse
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

COLS = [
    "date", "user_id", "dept", "login_hour", "logout_hour",
    "files_accessed", "data_downloaded_mb", "emails_sent",
    "external_emails_sent", "usb_events", "after_hours",
    "new_location_login", "label",
]

DEPTS = ["Engineering", "Finance", "HR", "Sales", "Operations"]
DEPT_PROFILES = {
    "Engineering":  dict(files=(20, 5),  dl=(50, 15),  emails=(8,  2), ext=(1, 0.5)),
    "Finance":      dict(files=(15, 4),  dl=(30, 10),  emails=(12, 3), ext=(2, 0.8)),
    "HR":           dict(files=(10, 3),  dl=(20,  8),  emails=(15, 4), ext=(3, 1.0)),
    "Sales":        dict(files=(12, 4),  dl=(25, 10),  emails=(20, 5), ext=(8, 2.0)),
    "Operations":   dict(files=(18, 5),  dl=(40, 12),  emails=(10, 3), ext=(2, 0.8)),
}


def _clip_int(rng, mu, sigma, lo=0, hi=None):
    v = int(round(rng.normal(mu, sigma)))
    v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return v


def gen_user(uid, dept, days, rng, threat=None):
    p     = DEPT_PROFILES[dept]
    start = date(2026, 2, 20)
    rows  = []
    for d in range(days):
        cur = start + timedelta(days=d)
        if cur.weekday() >= 5:          # skip weekends
            continue
        is_last3w = d >= days - 21      # flag final 3-week window

        login  = _clip_int(rng, 9, 1, 7, 11)
        logout = _clip_int(rng, 17, 1, 15, 20)
        files  = _clip_int(rng, *p["files"], 1)
        dl     = max(0.0, round(rng.normal(*p["dl"]), 1))
        emails = _clip_int(rng, *p["emails"], 0)
        ext    = _clip_int(rng, *p["ext"], 0)
        usb    = 0
        after  = 0
        newloc = 0
        lbl    = "normal"

        if threat == "disgruntled" and is_last3w:
            after  = int(rng.random() < 0.6)
            usb    = _clip_int(rng, 2, 1, 0, 8)
            logout = _clip_int(rng, 20, 1, 18, 23)
            lbl    = "disgruntled"

        elif threat == "malicious" and is_last3w:
            dl     = max(0.0, round(rng.normal(500, 80), 1))  # ~500 MB/day
            ext    = _clip_int(rng, 25, 5, 10)
            files  = _clip_int(rng, 80, 10, 20)
            lbl    = "malicious"

        elif threat == "compromised" and is_last3w:
            login  = _clip_int(rng, 2, 1, 0, 5)   # unusual 02:xx logins
            newloc = int(rng.random() < 0.5)
            files  = _clip_int(rng, 60, 10, 10)
            lbl    = "compromised"

        rows.append([cur, uid, dept, login, logout, files, dl,
                     emails, ext, usb, after, newloc, lbl])
    return rows


def main():
    ap = argparse.ArgumentParser(description="Generate insider threat UBA dataset")
    ap.add_argument("--seed",  type=int, default=42)
    ap.add_argument("--days",  type=int, default=90)
    ap.add_argument("--users", type=int, default=50)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "data", "user_activity.csv"))
    args = ap.parse_args()

    rng      = np.random.default_rng(args.seed)
    threats  = {3: "disgruntled", 17: "malicious", 31: "compromised"}
    rows     = []

    for uid in range(1, args.users + 1):
        dept  = DEPTS[uid % len(DEPTS)]
        label = threats.get(uid)
        rows += gen_user(f"user_{uid:03d}", dept, args.days, rng, threat=label)

    df = pd.DataFrame(rows, columns=COLS)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, index=False)

    vc = df["label"].value_counts()
    print(f"Generated {len(df):,} daily records  →  {args.out}")
    for lbl, cnt in vc.items():
        tag = "⚠" if lbl != "normal" else " "
        print(f"  {tag} {lbl:<15} {cnt:>5}")


if __name__ == "__main__":
    main()
