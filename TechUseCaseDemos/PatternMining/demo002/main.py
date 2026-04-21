"""
Main pattern mining pipeline.
"""

import numpy as np
import pandas as pd
try:
    from mlxtend.frequent_patterns import apriori, association_rules
    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False

np.random.seed(42)

def demo():
    if not HAS_MLXTEND:
        print("mlxtend missing; main demo skipped.")
        return
    products = [f"p_{i}" for i in range(25)]
    data = []
    for tid in range(600):
        basket = list(np.random.choice(products, size=np.random.randint(1, 5), replace=False))
        for p in basket:
            data.append({"tid": tid, "product": p})
    df = pd.DataFrame(data)
    basket_df = df.groupby(["tid", "product"]).size().unstack(fill_value=0)
    basket_bin = (basket_df > 0).astype(int)
    freq = apriori(basket_bin, min_support=0.05, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=0.5) if len(freq) > 0 else pd.DataFrame()
    print(f"Main demo: {len(freq)} itemsets, {len(rules)} rules")

if __name__ == "__main__":
    demo()
