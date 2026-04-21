"""
Tests for ecom_fulldemo.
"""

import numpy as np
import pandas as pd
try:
    from mlxtend.frequent_patterns import apriori, association_rules
    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False

np.random.seed(42)

def test_ecom_demo():
    if not HAS_MLXTEND:
        print("mlxtend not installed; skipping test.")
        return
    from ecom_fulldemo import generate_ecom_data
    df = generate_ecom_data(200)
    assert len(df) > 0, "DataFrame should not be empty"
    basket = df.groupby(["transaction_id", "product"]).size().unstack(fill_value=0)
    basket_bin = (basket > 0).astype(int)
    freq = apriori(basket_bin, min_support=0.05, use_colnames=True)
    print(f"Test passed: {len(freq)} itemsets found")

if __name__ == "__main__":
    test_ecom_demo()
