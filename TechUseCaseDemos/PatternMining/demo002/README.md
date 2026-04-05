Pattern Mining Demo (demo002)

This folder contains a credit-card transaction synthetic generator (`syndata.py`) and
an ecommerce-focused synthetic data generator (`ecom_syndata.py`). Both write
`syntheticdata.csv` in item-level format so the existing `fulldemo.py` can run without
modification.

Usage examples:
- python syndata.py --rows 5000
- python ecom_syndata.py --orders 2000
- python ecom_syndata.py --sample  # quick preview

Notes:
- `ecom_syndata.py` produces realistic product bundles (e.g., Electronics + Accessories,
  Clothing + Shoes, Groceries + Household) and repeated customers to make pattern
  mining examples more realistic.

New demo:
- `ecom_fulldemo.py` demonstrates frequent itemset mining with **Apriori** and **FP-Growth**
  using baskets created from orders (CustomerID + TransactionDate). Use `--minsup` and `--plot`.

Tests:
- `test_ecom_syndata.py` and `test_ecom_fulldemo.py` provide lightweight smoke tests.
