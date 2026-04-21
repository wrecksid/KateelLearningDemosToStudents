"""
Full pattern mining demo.
"""

import numpy as np
import pandas as pd
try:
    from mlxtend.frequent_patterns import apriori, association_rules
    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False

np.random.seed(42)

def generate_data(n=500):
    products = [f"prod_{i}" for i in range(30)]
    data = []
    for tid in range(n):
        basket = list(np.random.choice(products, size=np.random.randint(1, 6), replace=False))
        for p in basket:
            data.append({"tid": tid, "product": p})
    return pd.DataFrame(data)

def demo():
    if not HAS_MLXTEND:
        print("mlxtend not installed; skipping fulldemo.")
        return
    df = generate_data(500)
    basket = df.groupby(["tid", "product"]).size().unstack(fill_value=0)
    basket_bin = (basket > 0).astype(int)
    freq = apriori(basket_bin, min_support=0.04, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=0.45) if len(freq) > 0 else pd.DataFrame()
    print(f"Demo 002: {len(freq)} itemsets, {len(rules)} rules")
    freq.to_csv("/tmp/pattern_frequent.csv", index=False)
    print("Saved /tmp/pattern_frequent.csv")

if __name__ == "__main__":
    demo()
