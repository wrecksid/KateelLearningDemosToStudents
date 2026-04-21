"""
Synthetic transaction data generator for frequent items demo.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

def generate_transactions(n=1000, n_items=20):
    items = [f"item_{i}" for i in range(n_items)]
    probs = np.random.dirichlet(np.ones(n_items))
    rows = []
    for tid in range(n):
        basket = list(np.random.choice(items, size=np.random.choice([1,2,3,4,5]), replace=False, p=probs))
        rows.append({"transaction_id": tid, "item": item} for item in basket)
    flat = [r for rows in rows for r in rows]
    df = pd.DataFrame(flat)
    return df

if __name__ == "__main__":
    df = generate_transactions(1000)
    df.to_csv("synthetic_transactions.csv", index=False)
    print(f"Generated {len(df)} transactions -> synthetic_transactions.csv")
