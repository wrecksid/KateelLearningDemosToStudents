# syndata.py
# Synthetic Credit Card Transaction Data Generator for Finance Domain
# Author: Vinaya Sathyanarayana

"""
Program Description:
This program generates synthetic credit card transaction data that mimics real-life datasets 
commonly used in finance, especially for credit card transaction analysis, fraud detection, 
and pattern mining.

Features:
- Generates customizable number of rows (default 10,000).
- Uses locale 'en_IN' for English (India) as default for realistic names, locations, and companies.
- Includes fields: transaction date, cardholder info, card details, transaction category,
  merchant name, transaction amount, city, state, country, fraud flag.
- Fraud transactions randomly flagged (~2% by default).
- Supports random seed for reproducibility.
- Verbose progress mode (default) with option for quiet mode (-q/--quiet).
- Outputs data in CSV format called 'syntheticdata.csv'.

Usage Examples:
$ python syndata.py              # Generates 10,000 rows with verbose output
$ python syndata.py --size 5000  # Generates 5,000 rows
$ python syndata.py -q           # Quiet mode: no progress shown
$ python syndata.py --seed 42    # Fixes random seed for repeatable results
$ python syndata.py --sample     # Generate a small sample and preview

Instructions for students:
Explore by varying --size and --seed parameters. Examine the generated data fields, 
noting the diversity in transaction categories, merchants, and location data.
Use this dataset for applying pattern mining and fraud detection algorithms.

Bank usage scenario:
Banks can use synthetic data like this for training and testing AI/ML fraud detection, 
transaction pattern analysis, and risk assessment models without compromising real customer data.

"""

import pandas as pd
import argparse
from faker import Faker
import random
import sys

def generate_synthetic_data(num_rows=10000, locale='en_IN', seed=None, include_geo=True):
    if seed is not None:
        random.seed(seed)

    fake = Faker(locale)
    Faker.seed(seed)

    data = []

    # Transaction categories to simulate real-life spending behavior
    categories = [
        'Groceries', 'Electronics', 'Clothing', 'Restaurants', 'Travel', 'Gas',
        'Entertainment', 'Healthcare', 'Utilities', 'Education'
    ]

    for _ in range(num_rows):
        transaction_amount = round(random.uniform(10, 5000), 2)  # Amount between 10 and 5000
        category = random.choice(categories)
        transaction_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        merchant = fake.company()
        card_holder_name = fake.name()
        card_number = fake.credit_card_number(card_type='visa')
        card_expiry = fake.credit_card_expire()
        card_cvv = fake.credit_card_security_code()
        city = fake.city() if include_geo else ''
        state = fake.state() if include_geo else ''
        country = fake.country() if include_geo else ''

        # 2% transactions flagged as fraudulent randomly
        is_fraud = 1 if random.random() < 0.02 else 0

        data.append([
            transaction_date, card_holder_name, card_number, card_expiry, card_cvv,
            category, merchant, transaction_amount, city, state, country, is_fraud
        ])

    df = pd.DataFrame(data, columns=[
        'TransactionDate', 'CardHolderName', 'CardNumber', 'CardExpiry', 'CardCVV',
        'Category', 'Merchant', 'TransactionAmount', 'City', 'State', 'Country', 'IsFraud'
    ])

    return df

def main():
    parser = argparse.ArgumentParser(description='Synthetic Credit Card Transaction Data Generator')
    parser.add_argument('--size', type=int, default=10000, help='Number of rows to generate (default: 10000)')
    parser.add_argument('--locale', type=str, default='en_IN', help='Locale for data generation (default: en_IN)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode, suppress progress output')
    parser.add_argument('--sample', action='store_true', help='Generate a small sample (10 rows) and preview')
    args = parser.parse_args()

    # If sample flag set, override size and enable verbose preview
    if args.sample:
        args.size = 10
        args.quiet = False

    try:
        if not args.quiet:
            print(f"Starting synthetic data generation for {args.size} rows using locale '{args.locale}'...")

        df = generate_synthetic_data(num_rows=args.size, locale=args.locale, seed=args.seed)

        output_file = 'syntheticdata.csv'
        df.to_csv(output_file, index=False)

        if not args.quiet:
            print(f"Synthetic data successfully written to '{output_file}'.")
            print("Sample data preview:")
            print(df.head(5))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
