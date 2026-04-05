from collections import defaultdict

def apriori(transactions, min_support=0.01):
    """
    Find frequent itemsets using simplified Apriori algorithm.
    :param transactions: List of transactions (each as list of items)
    :param min_support: Minimum support threshold as a fraction
    :return: Dictionary of frequent itemsets and their support counts
    """
    item_counts = defaultdict(int)
    num_transactions = len(transactions)

    # Count support for individual items
    for transaction in transactions:
        for item in transaction:
            item_counts[frozenset([item])] += 1

    # Filter items by minimum support
    frequent_itemsets = {itemset: count for itemset, count in item_counts.items() if count / num_transactions >= min_support}
    current_frequent_itemsets = frequent_itemsets.copy()
    k = 2

    while current_frequent_itemsets:
        candidates = set()
        itemsets_list = list(current_frequent_itemsets.keys())
        for i in range(len(itemsets_list)):
            for j in range(i + 1, len(itemsets_list)):
                union_set = itemsets_list[i].union(itemsets_list[j])
                if len(union_set) == k:
                    candidates.add(union_set)

        candidate_counts = defaultdict(int)
        for transaction in transactions:
            transaction_set = set(transaction)
            for candidate in candidates:
                if candidate.issubset(transaction_set):
                    candidate_counts[candidate] += 1

        current_frequent_itemsets = {itemset: count for itemset, count in candidate_counts.items() if count / num_transactions >= min_support}
        frequent_itemsets.update(current_frequent_itemsets)
        k += 1

    return frequent_itemsets

# Assuming 'transactions' variable contains generated data from Part 1

# Run Apriori algorithm on generated data with min_support of 1%
frequent_itemsets = apriori(transactions, min_support=0.01)

# Display some frequent itemsets
print("\nFrequent Itemsets and Support Counts (showing first 20):")
for i, (itemset, count) in enumerate(frequent_itemsets.items()):
    print(f"{set(itemset)}: {count}")
    if i == 19:
        break
