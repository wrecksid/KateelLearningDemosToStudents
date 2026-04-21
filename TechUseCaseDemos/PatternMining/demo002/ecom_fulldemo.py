"""
E-commerce pattern mining full demo.
"""

import numpy as np
import pandas as pd
try:
    from mlxtend.frequent_patterns import apriori, association_rules
    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False

np.random.seed(42)

def generate_ecom_data(n=500):
    products = [f"prod_{i}" for i in range(20)]
    data = []
    for _ in range(n):
        basket = list(np.random.choice(products, size=np.random.randint(1, 5), replace=False))
        for p in basket:
            data.append({"transaction_id": _ , "product": p})
    return pd.DataFrame(data)

def demo():
    if not HAS_MLXTEND:
        print("mlxtend not installed; skipping ecom demo.")
        return
    df = generate_ecom_data(300)
    basket = df.groupby(["transaction_id", "product"]).size().unstack(fill_value=0)
    basket_bin = (basket > 0).astype(int)
    frequent = apriori(basket_bin, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent, metric="confidence", min_threshold=0.5) if len(frequent) > 0 else pd.DataFrame()
    print(f"E-commerce demo: {len(frequent)} itemsets, {len(rules)} rules")
    frequent.to_csv("/tmp/ecom_frequent.csv", index=False)
    print("Saved /tmp/ecom_frequent.csv")

if __name__ == "__main__":
    demo()
