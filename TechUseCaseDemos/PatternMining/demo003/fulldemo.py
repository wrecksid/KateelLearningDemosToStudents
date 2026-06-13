"""
fulldemo.py
Pattern Mining Demo on Synthetic Credit Card Transactions for Finance Domain
Author: Vinaya Sathyanarayana

Demonstrates:
- Apriori and FP-Growth via mlxtend (frequent itemsets and association rules)
- PrefixSpan for sequential pattern mining (prefixspan package)
- SPAM sequential pattern mining (sequence-mining package)
- Placeholder and integration example for advanced SPMF algorithms via Java CLI
- Robust error handling, verbose/quiet modes
- Detailed explanations and visualization of results

Note:
Many advanced algorithms (GSP, SPADE, ClaSP, BIDE+, MaxSP, etc.) are implemented in
the open-source SPMF Java tool. This demo shows how to prepare data, run SPMF algorithms,
and parse outputs, essential for mastering pattern mining in finance.

Dependencies:
- pandas, numpy, matplotlib, mlxtend, prefixspan, sequence-mining
- Java runtime environment and spmf.jar from https://github.com/philippe-fournier/spmf/

Usage:
python fulldemo.py [--minsup 0.001] [-q]

"""

import pandas as pd
import numpy as np
import argparse
import sys
import time
import subprocess
import os
import tempfile
import math
import json
import matplotlib.pyplot as plt

# MLxtend imports for Apriori and FP-Growth
try:
    from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
except ImportError:
    print("Error: Please install mlxtend (pip install mlxtend)")
    sys.exit(1)

# PrefixSpan module
try:
    from prefixspan import PrefixSpan
except ImportError:
    PrefixSpan = None

# sequence-mining package for SPAM demonstration
try:
    from sequence_mining.spam import SpamAlgo
except ImportError:
    SpamAlgo = None

# ------------------------
# Utility functions
# ------------------------

def load_data(filename, verbose=True):
    if verbose:
        print(f"\nLoading synthetic data from {filename}")
    try:
        df = pd.read_csv(filename)
        if verbose:
            print(f"Data shape: {df.shape}")
            print(df.head())
        return df
    except Exception as e:
        print(f"Error loading {filename}: {e}", file=sys.stderr)
        sys.exit(1)

def preprocess_for_apriori_fp(df, verbose=True):
    """
    Prepare basket (boolean) dataframe with 'Category' as items for Apriori/FP-Growth.
    """
    if verbose:
        print("\nPreprocessing data for Apriori and FP-Growth...")

    df['Item'] = df['Category']
    df['TransactionID'] = df['TransactionDate'].astype(str) + '_' + df['CardHolderName']
    basket = df.groupby(['TransactionID', 'Item']).size().unstack(fill_value=0)
    basket_bool = basket.astype(bool)
    if verbose:
        print(f"Prepared basket dataframe with shape: {basket_bool.shape}")
        print(basket_bool.head())
    return basket_bool

def run_apriori(basket, minsup=0.001, verbose=True):
    if verbose:
        print("\nRunning Apriori...")
    start = time.time()
    try:
        frequent_items = apriori(basket, min_support=minsup, use_colnames=True, verbose=verbose)
        if frequent_items.empty:
            if verbose:
                print("Apriori found no frequent itemsets")
            return None, None, 0
        rules = association_rules(frequent_items, metric="confidence", min_threshold=0.5)
    except Exception as e:
        print(f"Apriori error: {e}", file=sys.stderr)
        return None, None, 0
    duration = time.time() - start
    if verbose:
        print(f"Apriori took {duration:.2f}s found {len(frequent_items)} itemsets")
        print(frequent_items.head())
        print(rules.head())
    return frequent_items, rules, duration

def run_fpgrowth(basket, minsup=0.001, verbose=True):
    if verbose:
        print("\nRunning FP-Growth...")
    start = time.time()
    try:
        frequent_items = fpgrowth(basket, min_support=minsup, use_colnames=True, verbose=verbose)
        if frequent_items.empty:
            if verbose:
                print("FP-Growth found no frequent itemsets")
            return None, None, 0
        rules = association_rules(frequent_items, metric="confidence", min_threshold=0.5)
    except Exception as e:
        print(f"FP-Growth error: {e}", file=sys.stderr)
        return None, None, 0
    duration = time.time() - start
    if verbose:
        print(f"FP-Growth took {duration:.2f}s found {len(frequent_items)} itemsets")
        print(frequent_items.head())
        print(rules.head())
    return frequent_items, rules, duration

def preprocess_for_prefixspan(df, verbose=True):
    if verbose:
        print("\nPreprocessing data for PrefixSpan...")
    df_sorted = df.sort_values(['CardHolderName', 'TransactionDate'])
    df_sorted['Item'] = df_sorted['Category']
    sequences = []
    current_holder = None
    current_seq = []
    for _, row in df_sorted.iterrows():
        if row['CardHolderName'] != current_holder:
            if current_seq:
                sequences.append(current_seq)
            current_seq = []
            current_holder = row['CardHolderName']
        current_seq.append(str(row['Item']))
    if current_seq:
        sequences.append(current_seq)
    if verbose:
        print(f"Prepared {len(sequences)} sequences for PrefixSpan")
        if sequences:
            print("Sample sequence:", sequences[0])
    return sequences

def run_prefixspan(sequences, minsup=0.001, maxlen=5, verbose=True):
    if PrefixSpan is None:
        if verbose:
            print("prefixspan not installed, skipping PrefixSpan demo")
        return None

    if verbose:
        print("\nRunning PrefixSpan...")

    try:
        ps = PrefixSpan(sequences)

        min_support_count = max(1, int(len(sequences) * minsup))

        raw_patterns = ps.frequent(min_support_count)

        patterns = []

        for support, pattern in raw_patterns:
            if len(pattern) <= maxlen:
                patterns.append((pattern, support))

        if verbose:
            print(f"PrefixSpan found {len(patterns)} patterns")

            for pattern, support in patterns[:5]:
                print(
                    f"Pattern: {' -> '.join(map(str, pattern))} | Support: {support}"
                )

        return patterns

    except Exception as e:
        print(f"PrefixSpan error: {e}", file=sys.stderr)
        return None

def run_spam(sequences, minsup, verbose=True):
    if SpamAlgo is None:
        if verbose:
            print("sequence-mining (SPAM) library not installed, skipping SPAM demo")
        return None
    if verbose:
        print("\nRunning SPAM algorithm...")
    try:
        spam = SpamAlgo(sequences)
        min_support_count = max(1, int(len(sequences) * minsup))
        results = spam.run(min_support_count)
        if verbose:
            print(f"SPAM found {len(results)} patterns")
            for pattern in results[:5]:
                pat_str = ' -> '.join(['{' + ','.join(map(str, itemset)) + '}' for itemset in pattern[0]])
                print(f"Pattern: {pat_str} Support: {pattern[1]}")
        return results
    except Exception as e:
        print(f"SPAM error: {e}", file=sys.stderr)
        return None

def write_spmf_input(sequences, filepath):
    """
    Write sequences to SPMF format.
    """
    mapping = {}
    next_id = 1

    with open(filepath, 'w') as f:
        for seq in sequences:

            for item in seq:

                key = str(item)

                if key not in mapping:
                    mapping[key] = next_id
                    next_id += 1

                f.write(f"{mapping[key]} -1 ")

            f.write("-2\n")

    return mapping

def run_spmf_algorithm(algorithm_name, input_file, output_file, minsup_percent, spmf_jar_path='spmf.jar', verbose=True):
    """
    Run an SPMF Java algorithm via subprocess using given input file.
    """
    if verbose:
        print(f"\nRunning SPMF algorithm {algorithm_name} with min support {minsup_percent}%...")
    try:
        cmd = ['java', '-jar', spmf_jar_path, 'run', algorithm_name, input_file, output_file, str(minsup_percent)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"SPMF execution failed: {result.stderr}", file=sys.stderr)
            return False
        if verbose:
            print(f"SPMF output saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error running SPMF: {e}", file=sys.stderr)
        return False

def parse_spmf_output(output_file, verbose=True):
    """
    Parse SPMF output file containing sequences to list of (pattern, support).
    """
    patterns = []
    try:
        with open(output_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(' -1 ')
                if len(parts) < 2:
                    continue
                # Last is -2 support separated by space
                seq_parts = parts[:-1]
                # support may be in the trailing part after -2 and #SUP:
                try:
                    support = int(parts[-1].split('#SUP:')[-1])
                except Exception:
                    # fallback parse
                    tail = parts[-1].strip()
                    support = int(''.join(ch for ch in tail if ch.isdigit()) or 0)
                pattern = [list(map(int, itemset.split())) for itemset in seq_parts]
                patterns.append((pattern, support))
        if verbose:
            print(f"Parsed {len(patterns)} patterns from SPMF output")
        return patterns
    except Exception as e:
        print(f"Error parsing SPMF output: {e}", file=sys.stderr)
        return []


def translate_spmf_patterns(patterns, mapping):
    """
    Translate numeric patterns from SPMF output back to original item strings using mapping.
    mapping: dict from item_str -> id
    """
    inv = {v: k for k, v in mapping.items()}
    translated = []
    for pat, sup in patterns:
        newpat = []
        for itemset in pat:
            new_itemset = [inv.get(int(item), str(item)) for item in itemset]
            newpat.append(new_itemset)
        translated.append((newpat, sup))
    return translated

def main():
    parser = argparse.ArgumentParser(description='Pattern Mining Demo for Finance Data by Vinaya Sathyanarayana')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode suppress verbose output')
    parser.add_argument('--minsup', type=float, default=0.001, help='Minimum support as fraction (e.g., 0.001)')
    parser.add_argument('--maxlen', type=int, default=5, help='Max pattern length for sequential patterns')
    parser.add_argument('--spmf', type=str, default='spmf.jar', help='Path to spmf.jar for advanced algorithms')
    args = parser.parse_args()

    verbose = not args.quiet

    df = load_data('syntheticdata.csv', verbose)

    basket = preprocess_for_apriori_fp(df, verbose)

    apriori_itemsets, apriori_rules, apriori_time = run_apriori(basket, args.minsup, verbose)

    fpgrowth_itemsets, fpgrowth_rules, fpgrowth_time = run_fpgrowth(basket, args.minsup, verbose)

    sequences = preprocess_for_prefixspan(df, verbose)

    prefixspan_patterns = run_prefixspan(sequences, args.minsup, args.maxlen, verbose)

    spam_patterns = run_spam(sequences, args.minsup, verbose)

    # Run an example advanced algorithm (e.g. CM-SPADE) from SPMF if jar present
    if os.path.exists(args.spmf):
        if verbose:
            print(f"\nPreparing SPMF input file for advanced algorithms...")
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_input, \
             tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_output:
            mapping = write_spmf_input(sequences, tmp_input.name)
            tmp_input.flush()

            # Save mapping to a sidecar JSON for later translation
            mapping_path = tmp_input.name + '.map.json'
            with open(mapping_path, 'w') as mf:
                json.dump(mapping, mf)

            algo = 'CM-SPADE'  # Example advanced algorithm name supported by SPMF
            minsup_percent = max(1, int(math.ceil(args.minsup * 100)))  # Ensure at least 1%

            success = run_spmf_algorithm(algo, tmp_input.name, tmp_output.name, minsup_percent, args.spmf, verbose)
            if success:
                spmf_raw_patterns = parse_spmf_output(tmp_output.name, verbose)
                spmf_patterns = translate_spmf_patterns(spmf_raw_patterns, mapping)
            else:
                spmf_patterns = None
    else:
        if verbose:
            print(f"SPMF jar '{args.spmf}' not found; skipping advanced algorithms.")
        spmf_patterns = None

    # Visualization and summary (example)
    if verbose:
        import matplotlib.pyplot as plt
        labels = ['Apriori', 'FP-Growth']
        counts = [
            apriori_itemsets.shape[0] if apriori_itemsets is not None else 0,
            fpgrowth_itemsets.shape[0] if fpgrowth_itemsets is not None else 0,
        ]
        times = [
            apriori_time,
            fpgrowth_time,
        ]
        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Frequent Itemsets', color=color)
        ax1.bar(labels, counts, color=color, alpha=0.6)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Time (s)', color=color)
        ax2.plot(labels, times, color=color, marker='o')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title('Apriori vs FP-Growth Performance')
        plt.show()

        print("\nSummary:")
        print(f"Apriori: {counts[0]} itemsets in {times[0]:.2f}s" if apriori_itemsets is not None else "Apriori failed")
        print(f"FP-Growth: {counts[1]} itemsets in {times[1]:.2f}s" if fpgrowth_itemsets is not None else "FP-Growth failed")
        if prefixspan_patterns is not None:
            print(f"PrefixSpan patterns found: {len(prefixspan_patterns)}")
        if spam_patterns is not None:
            print(f"SPAM patterns found: {len(spam_patterns)}")
        if spmf_patterns is not None:
            print(f"SPMF (CM-SPADE) patterns found: {len(spmf_patterns)}")

    print("\nDemo complete. For other listed algorithms, consider integrating with SPMF or implement as research projects.")

if __name__ == '__main__':
    main()
