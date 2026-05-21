#!/usr/bin/env python3
"""
Generate synthetic phishing URL feature vectors.

Each row represents features extracted from one URL (benign or phishing).
Feature definitions mirror what real URL-analysis tools extract:
  url_length, num_dots, num_hyphens, num_underscores, num_slashes,
  num_at, num_digits, has_ip_address, num_subdomains, domain_length,
  tld_is_common, has_https, num_query_params, url_entropy,
  num_suspicious_words, has_redirect, path_length, brand_in_subdomain
"""
import argparse
import os
import numpy as np
import pandas as pd

COLS = [
    "url_length", "num_dots", "num_hyphens", "num_underscores",
    "num_slashes", "num_at", "num_digits", "has_ip_address",
    "num_subdomains", "domain_length", "tld_is_common", "has_https",
    "num_query_params", "url_entropy", "num_suspicious_words",
    "has_redirect", "path_length", "brand_in_subdomain", "label",
]


def _entropy(rng, mu, sigma):
    return round(float(np.clip(rng.normal(mu, sigma), 1.0, 5.0)), 3)


def gen_benign(n, rng):
    rows = []
    for _ in range(n):
        rows.append([
            int(rng.integers(20,  80)),   # url_length
            int(rng.integers(2,   5)),    # num_dots
            int(rng.integers(0,   2)),    # num_hyphens
            0,                            # num_underscores
            int(rng.integers(1,   4)),    # num_slashes
            0,                            # num_at
            int(rng.integers(0,   5)),    # num_digits
            0,                            # has_ip_address
            int(rng.integers(1,   3)),    # num_subdomains
            int(rng.integers(5,  20)),    # domain_length
            1,                            # tld_is_common (.com/.org/.edu)
            1,                            # has_https
            int(rng.integers(0,   3)),    # num_query_params
            _entropy(rng, 3.0, 0.4),      # url_entropy
            0,                            # num_suspicious_words
            0,                            # has_redirect
            int(rng.integers(0,  30)),    # path_length
            0,                            # brand_in_subdomain
            0,                            # label: 0 = benign
        ])
    return rows


def gen_phishing(n, rng):
    rows = []
    for _ in range(n):
        has_ip   = int(rng.random() < 0.25)
        tld_ok   = int(rng.random() < 0.30)   # less common TLDs
        https    = int(rng.random() < 0.18)    # phishing often skips HTTPS
        brand    = int(rng.random() < 0.35)    # paypal.attacker.xyz
        redirect = int(rng.random() < 0.30)
        rows.append([
            int(rng.integers(60, 200)),   # url_length — longer
            int(rng.integers(3,   9)),    # num_dots — deeper nesting
            int(rng.integers(1,   6)),    # num_hyphens — more hyphens
            int(rng.integers(0,   3)),    # num_underscores
            int(rng.integers(2,   7)),    # num_slashes
            int(rng.random() < 0.15),    # num_at
            int(rng.integers(3,  16)),    # num_digits — more digits
            has_ip,
            int(rng.integers(2,   7)),    # num_subdomains
            int(rng.integers(8,  40)),    # domain_length
            tld_ok,
            https,
            int(rng.integers(1,   8)),    # num_query_params
            _entropy(rng, 3.9, 0.4),      # url_entropy — higher
            int(rng.integers(1,   5)),    # num_suspicious_words (login/verify/secure…)
            redirect,
            int(rng.integers(15, 90)),    # path_length
            brand,
            1,                            # label: 1 = phishing
        ])
    return rows


def main():
    ap = argparse.ArgumentParser(description="Generate synthetic URL feature vectors")
    ap.add_argument("--seed",     type=int, default=42)
    ap.add_argument("--benign",   type=int, default=3000)
    ap.add_argument("--phishing", type=int, default=1500)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "data", "url_features.csv"))
    args = ap.parse_args()

    rng  = np.random.default_rng(args.seed)
    rows = gen_benign(args.benign, rng) + gen_phishing(args.phishing, rng)
    idx  = rng.permutation(len(rows))
    df   = pd.DataFrame([rows[i] for i in idx], columns=COLS)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, index=False)

    vc = df["label"].value_counts()
    print(f"Generated {len(df):,} URL records  →  {args.out}")
    print(f"  benign:   {vc.get(0, 0):>5}")
    print(f"  phishing: {vc.get(1, 0):>5}")


if __name__ == "__main__":
    main()
