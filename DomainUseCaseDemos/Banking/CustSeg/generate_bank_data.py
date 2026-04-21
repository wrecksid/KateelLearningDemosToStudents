"""
Synthetic bank customer data generator for Customer Segmentation demo.
Generates customer profiles with demographics, account balances, and transaction history.
"""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_bank_customers(n=1000):
    data = {
        "customer_id": [f"CUST_{i:05d}" for i in range(n)],
        "age": np.random.randint(18, 75, n),
        "income_k": np.random.lognormal(10.5, 0.7, n).round(2),
        "balance": np.random.lognormal(8.0, 1.2, n).round(2),
        "num_accounts": np.random.choice([1, 2, 3, 4, 5], n, p=[0.4, 0.3, 0.15, 0.1, 0.05]),
        "region": np.random.choice(['North', 'South', 'East', 'West'], n),
        "churn_risk": np.random.choice([0, 1], n, p=[0.85, 0.15]),
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_bank_customers(500)
    df.to_csv("bank_customers.csv", index=False)
    print(f"Generated {len(df)} customer records -> bank_customers.csv")
