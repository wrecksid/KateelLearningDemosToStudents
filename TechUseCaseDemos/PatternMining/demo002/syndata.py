"""
syndata.py
Author: Vinaya Sathyanarayana

This program generates synthetic credit card customer transaction data
using the Faker library (locale: en_IN). The synthetic dataset simulates
realistic transaction details useful for demonstrating pattern mining algorithms
in finance. The output is saved as 'syntheticdata.csv'.

Features:
- Default dataset size of 10,000 rows, customizable by the user
- Ability to tune parameters like fraud rate, income range, etc.
- Synthetic fields include CustomerID, Age, Gender, Income, TransactionAmount,
  TransactionDate, MerchantCategory, TransactionType, CardType, FraudFlag, RewardPoints

Instructions:
Run this script directly. Use command-line parameter --rows to set dataset size.
Example: python syndata.py --rows 5000

A bank may use this data to simulate and analyze transaction patterns, fraud detection,
and customer profiling for credit card management decisions.
"""

import argparse
import random
import pandas as pd
from faker import Faker
import numpy as np


class SyntheticDataGenerator:
    def __init__(self, n=10000, locale='en_IN', fraud_rate=0.02, income_min=20000, income_max=2000000, seed=42):
        self.n = n
        self.locale = locale
        self.fraud_rate = fraud_rate
        self.income_min = income_min
        self.income_max = income_max
        self.faker = Faker(locale)
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    def generate_credit_card_transactions(self) -> pd.DataFrame:
        data = []
        for _ in range(self.n):
            customer_id = self.faker.unique.random_int(min=100000, max=999999)
            age = random.randint(18, 75)
            gender = random.choices(['Male', 'Female', 'Other'], weights=[0.48, 0.5, 0.02])[0]
            income = round(random.uniform(self.income_min, self.income_max), 2)  # Annual income in INR
            transaction_amount = round(random.uniform(10, 100000), 2)  # INR
            transaction_date = self.faker.date_between(start_date='-2y', end_date='today')
            merchant_category = random.choice([
                'Groceries', 'Travel', 'Entertainment', 'Utilities', 'Dining',
                'Healthcare', 'Electronics', 'Education', 'Clothing', 'Fuel', 'Online Shopping'
            ])
            transaction_type = random.choice(['Purchase', 'Cash Withdrawal', 'Payment', 'Refund'])
            card_type = random.choice(['Credit', 'Debit', 'Prepaid'])
            fraud_flag = random.choices([0, 1], weights=[1 - self.fraud_rate, self.fraud_rate])[0]
            reward_points = int(transaction_amount // 10)  # Simplified points system

            data.append([
                customer_id, age, gender, income, transaction_amount, transaction_date,
                merchant_category, transaction_type, card_type, fraud_flag, reward_points
            ])

        df = pd.DataFrame(data, columns=[
            'CustomerID', 'Age', 'Gender', 'Income', 'TransactionAmount', 'TransactionDate',
            'MerchantCategory', 'TransactionType', 'CardType', 'FraudFlag', 'RewardPoints'
        ])
        return df

    def save_to_csv(self, df: pd.DataFrame, filename='syntheticdata.csv'):
        df.to_csv(filename, index=False)
        print(f"Saved synthetic data to {filename} with {len(df)} rows.")


def main():
    parser = argparse.ArgumentParser(description="Synthetic Credit Card Transaction Data Generator")
    parser.add_argument('--rows', type=int, default=10000,
                        help='Number of synthetic data rows to generate (default 10000)')
    parser.add_argument('--fraud_rate', type=float, default=0.02,
                        help='Ratio of fraudulent transactions (default 0.02)')
    args = parser.parse_args()

    generator = SyntheticDataGenerator(n=args.rows, fraud_rate=args.fraud_rate)
    df = generator.generate_credit_card_transactions()
    generator.save_to_csv(df)


if __name__ == "__main__":
    main()
