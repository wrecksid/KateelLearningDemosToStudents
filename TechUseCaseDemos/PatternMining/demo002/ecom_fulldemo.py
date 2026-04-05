"""
ecom_fulldemo.py
Ecommerce Pattern Mining Demo (frequent itemsets & association rules)
Author: GitHub Copilot (based on existing demo002 work)

This demo expects an item-level CSV `syntheticdata.csv` with columns:
CustomerID, Age, Gender, Income, TransactionAmount, TransactionDate,
MerchantCategory, TransactionType, CardType, FraudFlag, RewardPoints

It groups rows into orders (CustomerID + TransactionDate) to create baskets
and runs Apriori and FP-Growth (mlxtend) to extract frequent itemsets and
association rules. Results are printed and optionally plotted.

Usage:
  python ecom_fulldemo.py --minsup 0.01
"""

import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules


def load_or_generate(filename='syntheticdata.csv', generate_if_missing=True, sample_orders=200):
    if not os.path.exists(filename):
        if not generate_if_missing:
            raise FileNotFoundError(f"{filename} not found")
        try:
            print(f"{filename} not found. Generating sample ecommerce data...")
            from ecom_syndata import EcommerceSyntheticGenerator
            gen = EcommerceSyntheticGenerator(orders=sample_orders, seed=42)
            df = gen.generate()
            gen.save(df, filename)
            return df
        except Exception as e:
            print(f"Error generating data: {e}")
            raise
    df = pd.read_csv(filename)
    return df


def preprocess(df):
    # Create synthetic OrderID (Customer + Date)
    df = df.copy()
    # If there are multiple orders in same date per customer, give each a sequence id
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    df['OrderID'] = df['CustomerID'].astype(str) + '_' + df['TransactionDate'].dt.strftime('%Y%m%d')

    # Basket: one row per order, columns are MerchantCategory
    basket = df.groupby(['OrderID', 'MerchantCategory'])['TransactionAmount'].sum().unstack(fill_value=0)
    basket_bool = basket > 0
    return basket_bool


def run_apriori(basket_bool, minsup=0.01, top_n=20):
    print(f"Running Apriori with min_support={minsup}...")
    freq = apriori(basket_bool, min_support=minsup, use_colnames=True)
    if freq.empty:
        print("No frequent itemsets found by Apriori")
        return freq, pd.DataFrame()
    freq = freq.sort_values('support', ascending=False).reset_index(drop=True)
    print(f"Apriori found {len(freq)} itemsets. Top {min(top_n, len(freq))} shown:")
    print(freq.head(top_n))
    # rules
    rules = association_rules(freq, metric='confidence', min_threshold=0.5)
    if not rules.empty:
        rules = rules.sort_values(['confidence', 'lift'], ascending=False)
        print("Top association rules:\n", rules.head(10))
    return freq, rules


def run_fpgrowth(basket_bool, minsup=0.01, top_n=20):
    print(f"Running FP-Growth with min_support={minsup}...")
    freq = fpgrowth(basket_bool, min_support=minsup, use_colnames=True)
    if freq.empty:
        print("No frequent itemsets found by FP-Growth")
        return freq, pd.DataFrame()
    freq = freq.sort_values('support', ascending=False).reset_index(drop=True)
    print(f"FP-Growth found {len(freq)} itemsets. Top {min(top_n, len(freq))} shown:")
    print(freq.head(top_n))
    rules = association_rules(freq, metric='confidence', min_threshold=0.5)
    if not rules.empty:
        rules = rules.sort_values(['confidence', 'lift'], ascending=False)
        print("Top association rules:\n", rules.head(10))
    return freq, rules


def plot_top_itemsets(freq_items, title="Top Frequent Itemsets", top_n=10):
    if freq_items is None or freq_items.empty:
        print("No itemsets to plot")
        return
    top = freq_items.sort_values('support', ascending=False).head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='support', y=top['itemsets'].apply(lambda s: ', '.join(list(s))), data=top)
    plt.title(title)
    plt.xlabel('Support')
    plt.ylabel('Itemset')
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Ecommerce Pattern Mining Demo')
    parser.add_argument('--data', type=str, default='syntheticdata.csv')
    parser.add_argument('--minsup', type=float, default=0.01)
    parser.add_argument('--plot', action='store_true')
    parser.add_argument('--sample', action='store_true', help='Generate sample data if missing')
    args = parser.parse_args()

    df = load_or_generate(args.data, generate_if_missing=args.sample)
    basket_bool = preprocess(df)

    apriori_items, apriori_rules = run_apriori(basket_bool, minsup=args.minsup)
    fpg_items, fpg_rules = run_fpgrowth(basket_bool, minsup=args.minsup)

    if args.plot:
        plot_top_itemsets(apriori_items, "Apriori - Top Itemsets")
        plot_top_itemsets(fpg_items, "FP-Growth - Top Itemsets")

    print('\nDemo complete.')


if __name__ == '__main__':
    main()
