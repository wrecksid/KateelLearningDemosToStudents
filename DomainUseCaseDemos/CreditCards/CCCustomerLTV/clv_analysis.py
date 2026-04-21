"""
Customer Lifetime Value (CLV) analysis for credit card customers.
Estimates long-term customer value using transaction history and demographics.
"""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_credit_card_data(n=2000):
    data = {
        "customer_id": [f"CC_{i:05d}" for i in range(n)],
        "age": np.random.randint(22, 65, n),
        "income_k": np.random.lognormal(10.2, 0.8, n).round(2),
        "avg_monthly_spend": np.random.gamma(shape=2, scale=800, size=n).round(2),
        "num_transactions": np.random.poisson(12, n),
        "tenure_months": np.random.randint(1, 60, n),
        "credit_limit": np.random.gamma(shape=3, scale=2000, size=n).round(2),
        "default_flag": np.random.choice([0, 1], n, p=[0.88, 0.12]),
    }
    return pd.DataFrame(data)


def estimate_clv(transactions, tenure_months, retention_rate=0.92, margin_pct=0.035):
    avg_monthly_spend = transactions / max(tenure_months, 1)
    clv = (avg_monthly_spend * margin_pct * retention_rate) / max((0.01 + retention_rate - 1), 0.99)
    return clv


if __name__ == "__main__":
    df = generate_credit_card_data(300)
    df["estimated_clv"] = estimate_clv(df["avg_monthly_spend"], df["tenure_months"])
    df.to_csv("cc_ltv_data.csv", index=False)
    print(f"Generated {len(df)} CC customer records with CLV -> cc_ltv_data.csv")
