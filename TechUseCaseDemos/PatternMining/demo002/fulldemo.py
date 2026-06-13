"""
Full pattern mining demo.
"""

import numpy as np
import pandas as pd
from pathlib import Path

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
        basket = list(
            np.random.choice(
                products,
                size=np.random.randint(1, 6),
                replace=False
            )
        )

        for p in basket:
            data.append({
                "tid": tid,
                "product": p
            })

    return pd.DataFrame(data)


def demo():

    if not HAS_MLXTEND:
        print("mlxtend not installed; skipping fulldemo.")
        return

    try:
        df = generate_data(500)

        basket = (
            df.groupby(["tid", "product"])
            .size()
            .unstack(fill_value=0)
        )

        # mlxtend prefers bool values
        basket_bin = (basket > 0)

        freq = apriori(
            basket_bin,
            min_support=0.04,
            use_colnames=True
        )

        rules = pd.DataFrame()

        if not freq.empty:

            # Fix mlxtend/numpy compatibility issue
            freq["itemsets"] = freq["itemsets"].apply(
                lambda x: frozenset(str(item) for item in x)
            )

            try:
                rules = association_rules(
                    freq,
                    metric="confidence",
                    min_threshold=0.45
                )
            except Exception as e:
                print(f"association_rules warning: {e}")
                rules = pd.DataFrame()

        print(f"Demo 002: {len(freq)} itemsets, {len(rules)} rules")

        output_file = Path("pattern_frequent.csv")
        freq.to_csv(output_file, index=False)

        print(f"Saved {output_file.resolve()}")

    except Exception as e:
        print(f"Demo failed: {e}")


if __name__ == "__main__":
    demo()