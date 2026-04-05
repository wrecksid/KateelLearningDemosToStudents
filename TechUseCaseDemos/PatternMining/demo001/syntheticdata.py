import random

def generate_transactions(num_transactions=10000):
    """
    Generate synthetic transaction data.
    Each transaction contains a random number of items chosen from a fixed item pool.
    """
    item_pool = ['milk', 'bread', 'apple', 'banana', 'egg', 'cheese', 'butter', 'orange', 'grape', 'water']
    transactions = []
    for _ in range(num_transactions):
        transaction_size = random.randint(1, 5)  # Each transaction has 1 to 5 items
        transaction = random.sample(item_pool, transaction_size)
        transactions.append(transaction)
    return transactions

# Generate 10,000 transactions
transactions = generate_transactions(10000)

# Example: Print first 5 transactions
for i in range(5):
    print(f"Transaction {i+1}: {transactions[i]}")
