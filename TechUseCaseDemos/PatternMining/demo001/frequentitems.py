"""
Frequent item mining demo (market basket analysis).
"""

import numpy as np
import pandas as pd
from itertools import combinations
from collections import Counter

np.random.seed(42)

def generate_transactions(n=1000, n_items=20):
    items = [f"item_{i}" for i in range(n_items)]
    probs = np.random.dirichlet(np.ones(n_items))  # random item popularity
    transactions = []
    for _ in range(n):
        basket_size = np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.2, 0.07, 0.03])
        basket = list(np.random.choice(items, size=basket_size, replace=False, p=probs))
        transactions.append(basket)
    return transactions

def mine_frequent_items(transactions, min_support=0.02):
    counter = Counter()
    n = len(transactions)
    for t in transactions:
        for item in set(t):
            counter[item] += 1
    freq = {item: cnt / n for item, cnt in counter.items() if cnt / n >= min_support}
    pairs_counter = Counter()
    for t in transactions:
        for p in combinations(sorted(t), 2):
            pairs_counter[p] += 1
    pairs = {p: cnt / n for p, cnt in pairs_counter.items() if cnt / n >= min_support}
    return freq, pairs

def demo():
    transactions = generate_transactions(1000)
    freq, pairs = mine_frequent_items(transactions, min_support=0.01)
    print(f"Frequent items: {len(freq)}")
    print(f"Frequent pairs: {len(pairs)}")
    if freq:
        top = sorted(freq.items(), key=lambda x: -x[1])[:5]
        print("Top items:", top)
    print("Frequent items demo complete.")

if __name__ == "__main__":
    demo()
