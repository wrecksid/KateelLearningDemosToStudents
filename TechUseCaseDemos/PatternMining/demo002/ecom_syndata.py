"""
E-commerce synthetic data generator.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

def generate(n=500):
    products = [f"prod_{i}" for i in range(20)]
    rows = []
    for tid in range(n):
        for item in np.random.choice(products, size=np.random.randint(1, 5), replace=False):
            rows.append({"transaction_id": tid, "product": item})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate(500)
    df.to_csv("ecom_syndata.csv", index=False)
    print(f"Generated {len(df)} rows -> ecom_syndata.csv")
