"""
Frequent Item Set Mining Demo for Banking Marketing Upsell / Cross sell
Author: Vinaya Sathyanarayana

This script demonstrates multiple frequent pattern mining algorithms on synthetic banking product ownership data.
It shows step-by-step explanations, visualizations, and model comparisons with examples.

Usage:
- Run this script after generating syntheticdata.csv using synthetic_data_generator.py
- Explore outputs and graphs to understand frequent product bundles customers own
- See how these patterns can inform upsell and cross sell campaigns in banks
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules, fpmax
import numpy as np

import warnings
warnings.filterwarnings("ignore")

AUTHOR = "Vinaya Sathyanarayana"

def load_data(filename='syntheticdata.csv'):
    try:
        data = pd.read_csv(filename)
        print(f"Loaded data with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to load data file {filename}: {e}")

def preprocess_data(df):
    # Extract only product ownership columns (boolean)
    product_cols = [
        'Savings Account',
        'Current Account',
        'Fixed Deposit',
        'Recurring Deposit',
        'Credit Card',
        'Personal Loan',
        'Home Loan',
        'Car Loan',
        'Mutual Funds',
        'Insurance'
    ]
    # Ensure all product columns exist
    for col in product_cols:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in data.")

    # Convert ownership columns to boolean True/False
    products_df = df[product_cols].astype(bool)
    return products_df

def plot_frequency(products_df):
    counts = products_df.sum().sort_values(ascending=False)
    plt.figure(figsize=(10,6))
    sns.barplot(x=counts.index, y=counts.values, palette='viridis')
    plt.xticks(rotation=45)
    plt.title('Product Ownership Frequency')
    plt.ylabel('Number of Customers Owning Product')
    plt.xlabel('Product')
    plt.tight_layout()
    plt.show()

    print("Interpretation: This bar chart shows the count of customers owning each financial product. \nMarketing teams can identify the most popular products and target cross sell on less owned ones or upsell enhancements for popular products.")

def run_apriori(products_df, min_support=0.05):
    print("\nRunning Apriori algorithm with minimum support:", min_support)
    freq_itemsets = apriori(products_df, min_support=min_support, use_colnames=True)
    freq_itemsets['length'] = freq_itemsets['itemsets'].apply(lambda x: len(x))

    print(f"Found {len(freq_itemsets)} frequent itemsets.")
    return freq_itemsets

def run_fpgrowth(products_df, min_support=0.05):
    print("\nRunning FP-Growth algorithm with minimum support:", min_support)
    freq_itemsets = fpgrowth(products_df, min_support=min_support, use_colnames=True)
    freq_itemsets['length'] = freq_itemsets['itemsets'].apply(lambda x: len(x))

    print(f"Found {len(freq_itemsets)} frequent itemsets.")
    return freq_itemsets

def find_closed_itemsets(frequent_itemsets):
    """
    Identify closed frequent itemsets from the DataFrame of frequent itemsets.
    A frequent itemset is closed if none of its supersets have the same support.

    Parameters:
        frequent_itemsets (pd.DataFrame): DataFrame with 'itemsets' (frozenset) and 'support' columns

    Returns:
        pd.DataFrame: DataFrame of closed itemsets with columns 'itemsets' and 'support'
    """
    closed_itemsets = []
    # Sort descending by support to optimize checks
    frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False).reset_index(drop=True)

    for i, row_i in frequent_itemsets.iterrows():
        is_closed = True
        for j, row_j in frequent_itemsets.iterrows():
            if i != j:
                if row_i['itemsets'].issubset(row_j['itemsets']) and row_i['support'] == row_j['support']:
                    is_closed = False
                    break
        if is_closed:
            closed_itemsets.append(row_i)

    return pd.DataFrame(closed_itemsets)

def run_closed_itemsets(products_df, min_support=0.05):
    print("\nMining closed frequent itemsets with minimum support:", min_support)
    try:
        freq_itemsets = apriori(products_df, min_support=min_support, use_colnames=True)
        closed_sets = find_closed_itemsets(freq_itemsets)
        closed_sets['length'] = closed_sets['itemsets'].apply(lambda x: len(x))
        print(f"Found {len(closed_sets)} closed frequent itemsets.")
        return closed_sets
    except Exception as e:
        print("Error mining closed itemsets:", e)
        return pd.DataFrame()

def run_fpmax(products_df, min_support=0.05):
    print("\nMining maximal frequent itemsets with minimum support:", min_support)
    try:
        max_sets = fpmax(products_df, min_support=min_support)
        max_sets['length'] = max_sets['itemsets'].apply(lambda x: len(x))
        print(f"Found {len(max_sets)} maximal frequent itemsets.")
        return max_sets
    except Exception as e:
        print("Error mining maximal itemsets:", e)
        return pd.DataFrame()

def plot_itemset_lengths(freq_itemsets, title='Frequent Itemset Length Distribution'):
    count_len = freq_itemsets['length'].value_counts().sort_index()
    plt.figure(figsize=(8,5))
    sns.barplot(x=count_len.index, y=count_len.values, palette='magma')
    plt.title(title)
    plt.xlabel('Itemset Length (Number of Products)')
    plt.ylabel('Count of Itemsets')
    plt.tight_layout()
    plt.show()

    print(f"Interpretation: This chart shows how many frequent itemsets were found for each itemset size.\n"
          f"For marketing, larger itemsets indicate common bundles of multiple products customers own together, useful for targeted campaigns.")

def compare_model_support_sets(*args):
    """Compare lengths and count of frequent sets detected by algorithms."""
    import pandas as pd
    results = []
    for (name, df) in args:
        if df is not None and not df.empty:
            max_len = df['length'].max()
            num_sets = len(df)
            avg_len = df['length'].mean()
            results.append({
                'Algorithm': name,
                'Number of Frequent Itemsets': num_sets,
                'Max Itemset Length': max_len,
                'Average Itemset Length': round(avg_len, 2)
            })
    return pd.DataFrame(results)

def plot_association_rules(rules):
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=rules, x='support', y='confidence', hue='lift', palette='coolwarm', edgecolor='k')
    plt.title('Association Rules Support vs Confidence (colored by Lift)')
    plt.xlabel('Support')
    plt.ylabel('Confidence')
    plt.legend(title='Lift')
    plt.tight_layout()
    plt.show()

    print("Interpretation: Scatter plot of association rules showing the tradeoff between support and confidence.\n"
          "Rules with high lift are most interesting for marketing (high relevance and strong association).")

def main():
    print(f"Author: {AUTHOR}")
    try:
        df = load_data()
        products_df = preprocess_data(df)
        plot_frequency(products_df)

        min_support = 0.05

        apriori_sets = run_apriori(products_df, min_support)
        fpgrowth_sets = run_fpgrowth(products_df, min_support)
        closed_sets = run_closed_itemsets(products_df, min_support)
        maximal_sets = run_fpmax(products_df, min_support)

        plot_itemset_lengths(apriori_sets, 'Apriori Frequent Itemset Length Distribution')
        plot_itemset_lengths(fpgrowth_sets, 'FP-Growth Frequent Itemset Length Distribution')

        # Compare model outputs
        comparison_df = compare_model_support_sets(
            ('Apriori', apriori_sets),
            ('FP-Growth', fpgrowth_sets),
            ('Closed Patterns', closed_sets),
            ('Maximal Patterns', maximal_sets)
        )
        print("\nComparison of Frequent Pattern Mining Algorithms:")
        print(comparison_df.to_string(index=False))

        # Generate association rules from Apriori frequent itemsets
        print("\nGenerating association rules from Apriori frequent itemsets...")
        rules = association_rules(apriori_sets, metric="confidence", min_threshold=0.6)
        print(f"Generated {len(rules)} rules with confidence >= 0.6.")

        if not rules.empty:
            # Show top 10 rules sorted by lift
            top_rules = rules.sort_values(by='lift', ascending=False).head(10)
            print("\nTop 10 Association Rules (by Lift):")
            for i, row in top_rules.iterrows():
                antecedents = ', '.join(list(row['antecedents']))
                consequents = ', '.join(list(row['consequents']))
                print(f"Rule: If a customer owns [{antecedents}] then likely owns [{consequents}] "
                      f"(support={row['support']:.3f}, confidence={row['confidence']:.3f}, lift={row['lift']:.3f})")

            plot_association_rules(top_rules)

        else:
            print("No strong association rules found at the given confidence threshold.")

        print("\nInstructions for students:")
        print("- Modify min_support parameter to see how frequent patterns vary.")
        print("- Experiment with association_rules parameters such as metric and confidence threshold.")
        print("- Try running on data subsets filtered by demographics (age, gender) to observe differences.")

        print("\nBank use case notes:")
        print("- Banks can use frequent itemset mining to identify common product bundles owned by customers.")
        print("- Association rules inform upsell/cross sell strategies by identifying likely products to market next.")
        print("- Closed and maximal patterns help reduce redundancy and focus on most significant bundles.")

    except Exception as e:
        print(f"Error in pattern mining demo: {e}")

if __name__ == '__main__':
    main()
