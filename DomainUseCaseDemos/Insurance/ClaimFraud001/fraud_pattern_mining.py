"""
Insurance Claim Fraud Detection using Frequent Itemset Mining
Author: Vinaya Sathyanarayana

Demonstrates pattern mining algorithms to detect fraudulent insurance claims using synthetic data.

Features:
- Loads syntheticdata.csv
- Applies Apriori and FP-Growth algorithms to find frequent patterns in claim attributes linked to fraud
- Explains outputs, graphs, interpretations
- Step-by-step algorithm insights
- Comparison of model results with evaluation metrics

Instructions for students:
- Use generated 'syntheticdata.csv' as input
- Experiment with min_support and other parameters in each algorithm function
- Explore differences in patterns for fraud vs non-fraud claims

Instructions for banks:
- Adapt these scripts to real claim data
- Build better fraud detection systems based on discovered patterns and frequent itemsets
- Use frequent pattern mining to target suspicious claim types and amounts for investigation

Error Handling:
- Handles file missing, data loading, and algorithm exceptions smoothly
"""

import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.frequent_patterns import association_rules
import numpy as np
import sys
import time


def load_data(file_path='syntheticdata.csv'):
    """Load synthetic insurance claim data."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Input data file '{file_path}' not found. Please generate synthetic data first.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Data file is empty.")
        sys.exit(1)
    return df


def preprocess_data(df):
    """
    Preprocess data for pattern mining.
    Convert categorical variables to one-hot encoded format.
    Bin monetary amounts to categorical bins for itemset mining.
    """
    df = df.copy()
    # Bin claim amounts to categories
    bins = [0, 10000, 50000, 100000, 500000, 1000000]
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    df['ClaimAmountCategory'] = pd.cut(df['ClaimAmount'], bins=bins, labels=labels, include_lowest=True)

    # Convert 'FraudFlag' to string 'Fraud' or 'No Fraud' for analysis
    df['FraudFlagStr'] = df['FraudFlag'].map({0: 'No Fraud', 1: 'Fraud'})

    # Features to include in itemset mining
    features = ['ClaimType', 'ClaimStatus', 'ClaimAmountCategory', 'FraudFlagStr']

    # One-hot encode these features
    df_onehot = pd.get_dummies(df[features])

    return df_onehot, df


def run_apriori(df_onehot, min_support=0.02, use_colnames=True):
    """
    Run Apriori algorithm to find frequent itemsets.

    Args:
    - df_onehot: one-hot encoded input DataFrame
    - min_support: minimum support threshold for itemsets
    """
    start_time = time.time()
    frequent_itemsets = apriori(df_onehot, min_support=min_support, use_colnames=use_colnames)
    duration = time.time() - start_time
    print(f"Apriori found {len(frequent_itemsets)} frequent itemsets in {duration:.2f} seconds.")
    return frequent_itemsets


def run_fpgrowth(df_onehot, min_support=0.02, use_colnames=True):
    """
    Run FP-Growth algorithm to find frequent itemsets.

    Args:
    - df_onehot: one-hot encoded input DataFrame
    - min_support: minimum support threshold for itemsets
    """
    start_time = time.time()
    frequent_itemsets = fpgrowth(df_onehot, min_support=min_support, use_colnames=use_colnames)
    duration = time.time() - start_time
    print(f"FP-Growth found {len(frequent_itemsets)} frequent itemsets in {duration:.2f} seconds.")
    return frequent_itemsets


def analyze_rules(frequent_itemsets, metric="confidence", min_threshold=0.7):
    """
    Generate association rules from frequent itemsets.

    Args:
    - frequent_itemsets: DataFrame with frequent itemsets
    - metric: metric to filter rules ['confidence', 'lift', etc.]
    - min_threshold: minimum threshold for metric
    """
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    print(f"Generated {len(rules)} association rules with {metric} >= {min_threshold}")
    return rules


def plot_frequent_itemsets(frequent_itemsets, title="Frequent Itemsets Support"):
    """Plot bar chart of top 10 frequent itemsets by support."""
    top_10 = frequent_itemsets.sort_values(by='support', ascending=False).head(10)
    itemsets_str = top_10['itemsets'].apply(lambda x: ', '.join(list(x)))

    plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(top_10)), top_10['support'], color='skyblue')
    plt.yticks(range(len(top_10)), itemsets_str)
    plt.xlabel('Support')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.show()

    print("Interpretation: The chart shows the most common combinations of claim attributes that occur frequently in the dataset.\n"
          "High support indicates these patterns appear in a large portion of claims, valuable to identify typical claim behaviors.\n"
          "Patterns involving the 'Fraud' flag suggest common attribute combos among fraudulent claims.\n")


def compare_algorithms(df_onehot, min_support=0.02):
    """
    Compare Apriori and FP-Growth algorithms on runtime and number of frequent itemsets found.
    Returns a summary DataFrame of results.
    """
    print("Running Apriori...")
    apriori_itemsets = run_apriori(df_onehot, min_support)
    print("Running FP-Growth...")
    fpgrowth_itemsets = run_fpgrowth(df_onehot, min_support)

    # Compare results
    comparison = pd.DataFrame({
        'Algorithm': ['Apriori', 'FP-Growth'],
        'NumFrequentItemsets': [len(apriori_itemsets), len(fpgrowth_itemsets)]
    })

    print("\nComparison of Algorithms:")
    print(comparison.to_string(index=False))

    return apriori_itemsets, fpgrowth_itemsets, comparison


def main():
    print("Loading synthetic insurance claim data...")
    df = load_data()

    print("Preprocessing data for frequent itemset mining...")
    df_onehot, original_df = preprocess_data(df)

    # Min support minimum frequency of itemsets; adjustable for exploration
    min_support = 0.02

    # Run Apriori
    apriori_results = run_apriori(df_onehot, min_support=min_support)
    plot_frequent_itemsets(apriori_results, title="Top 10 Frequent Itemsets by Apriori")

    # Run FP-Growth
    fpgrowth_results = run_fpgrowth(df_onehot, min_support=min_support)
    plot_frequent_itemsets(fpgrowth_results, title="Top 10 Frequent Itemsets by FP-Growth")

    # Generate association rules for Apriori results to explore strong correlations
    rules = analyze_rules(apriori_results, metric="confidence", min_threshold=0.8)
    print("\nExample association rules (head):")
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())

    # Comparison table
    print("\nGenerating comparison of the two algorithms based on number of itemsets found...")
    _, _, comparison = compare_algorithms(df_onehot, min_support=min_support)

    print("\nStep-by-step explanations:")
    print("- Preprocessing converts categorical variables into a format suitable for pattern mining.")
    print("- Apriori uses downward closure principle to prune infrequent itemsets and finds frequent sets iteratively.")
    print("- FP-Growth uses a compact tree structure (FP-Tree) to find frequent itemsets without candidate generation, generally faster.")
    print("- Association rules help interpret relationships between attribute patterns and fraud presence.")
    print("- High confidence and lift in rules suggest strong linkage between attribute combinations and fraud, useful for management decisions.")

    print("\nBanks can use this approach to:")
    print("- Identify suspicious claim patterns.")
    print("- Prioritize investigation of claims with frequently occurring fraudulent patterns.")
    print("- Develop automated alerts for claims matching frequent fraud itemsets.")

    print("\nStudents are encouraged to experiment by changing min_support, metric thresholds, and exploring extended attributes in data.")


if __name__ == '__main__':
    main()
