"""
Author: Vinaya Sathyanarayana
Synthetic Credit Card Transactions Data Generator

Generates a synthetic dataset for credit card transactions including fraud labels.
Designed to mimic realistic distributions and allow parameter tuning.

Usage:
- Default: generates 10,000 rows with 2% fraud ratio
- Parameters can be modified by changing function arguments or command line options (if extended)

Outputs:
- CSV file named 'syntheticdata.csv' in current folder
"""

import sys
import argparse
from faker import Faker
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def generate_synthetic_credit_card_data(rows=10000, fraud_ratio=0.02, locale='en_IN', filename='syntheticdata.csv'):
    """
    Generate synthetic credit card transaction data with class imbalance for fraud detection.

    Args:
        rows (int): Number of rows to generate (default 10000)
        fraud_ratio (float): Fraction of fraudulent transactions (default 0.02)
        locale (str): Faker locale (default 'en_IN' for English - India)
        filename (str): Output CSV filename (default 'syntheticdata.csv')

    Returns:
        None: Saves the generated data as CSV file.
    """

    try:
        if rows <= 0:
            raise ValueError("Number of rows must be positive.")
        if not (0 <= fraud_ratio < 1):
            raise ValueError("Fraud ratio must be between 0 (inclusive) and 1 (exclusive).")

        fake = Faker(locale)
        Faker.seed(1234)
        np.random.seed(1234)

        # Define categories and cities - representative of Indian context
        merchant_categories = [
            'Grocery', 'Electronics', 'Clothing', 'Restaurants', 'Travel', 'Online',
            'Utilities', 'Gas Station', 'Pharmacy'
        ]

        cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad'
        ]

        num_fraud = int(rows * fraud_ratio)
        num_non_fraud = rows - num_fraud

        data_rows = []

        # Generate non-fraudulent transactions
        for _ in range(num_non_fraud):
            data_rows.append({
                'TransactionID': fake.uuid4(),
                'CardNumber': fake.credit_card_number(card_type='mastercard'),
                'CardHolderName': fake.name(),
                'TransactionAmount': round(np.random.exponential(scale=1000), 2),  # right skewed amounts
                'MerchantCategory': np.random.choice(merchant_categories, p=[0.2,0.1,0.1,0.15,0.1,0.15,0.05,0.1,0.05]),
                'TransactionDate': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
                'TransactionTime': fake.time(pattern='%H:%M:%S'),
                'TransactionCity': np.random.choice(cities),
                'IsFraud': 0
            })

        # Generate fraudulent transactions with different patterns
        for _ in range(num_fraud):
            data_rows.append({
                'TransactionID': fake.uuid4(),
                'CardNumber': fake.credit_card_number(card_type='mastercard'),
                'CardHolderName': fake.name(),
                'TransactionAmount': round(np.random.uniform(2000, 20000), 2),  # higher amounts
                'MerchantCategory': np.random.choice(merchant_categories, p=[0.05,0.15,0.1,0.1,0.15,0.15,0.1,0.1,0.1]),
                'TransactionDate': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
                'TransactionTime': fake.time(pattern='%H:%M:%S'),
                'TransactionCity': np.random.choice(cities),
                'IsFraud': 1
            })

        # Shuffle the dataset
        df = pd.DataFrame(data_rows)
        df = df.sample(frac=1, random_state=1234).reset_index(drop=True)

        df.to_csv(filename, index=False)
        logging.info(f"Synthetic dataset generated with {rows} rows ({num_fraud} frauds). Saved as {filename}")

    except Exception as e:
        logging.error(f"Error in data generation: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate synthetic credit card transaction dataset with fraud labels.")
    parser.add_argument('--rows', type=int, default=10000, help='Number of rows of data to generate (default 10000)')
    parser.add_argument('--fraud_ratio', type=float, default=0.02, help='Ratio of fraudulent transactions (default 0.02)')
    parser.add_argument('--locale', type=str, default='en_IN', help='Locale for Faker library (default en_IN)')
    parser.add_argument('--output', type=str, default='syntheticdata.csv', help='Output CSV file name (default syntheticdata.csv)')

    args = parser.parse_args()
    generate_synthetic_credit_card_data(rows=args.rows, fraud_ratio=args.fraud_ratio, locale=args.locale, filename=args.output)
