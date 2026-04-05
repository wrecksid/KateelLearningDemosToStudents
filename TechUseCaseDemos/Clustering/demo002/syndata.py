"""
syndata.py
Author: Vinaya Sathyanarayana

This program generates synthetic credit card customer data for clustering demonstrations in finance.
It uses the Faker library to simulate realistic data with locale en_IN for Indian context.

Features include:
- CustomerID, Name, Age, Gender, Income, CreditScore, CardType, CardLimit,
  NumTransactions, AvgTransactionAmount, FraudFlag
- Dataset size adjustable by user with default 10,000 rows
- Outputs CSV file named syntheticdata.csv by default

Instructions for Students:
- Run the script with default settings or specify number of rows and output CSV filename
- Explore how changing size and data distribution affects clustering performance

Instructions for Banks:
- Simulated data models customer segments for targeted marketing, risk, and fraud control
- Parameters can be tuned for different synthetic populations

Error handling and documentation included.
"""

from faker import Faker
import pandas as pd
import numpy as np
import random

class SyntheticDataGenerator:
    def __init__(self, num_rows=10000, locale='en_IN'):
        self.num_rows = num_rows
        self.locale = locale
        self.fake = Faker(locale)
        # Seed for reproducibility
        Faker.seed(42)
        np.random.seed(42)
        random.seed(42)

    def generate_data(self):
        # Generate credit card customer features:
        # CustomerID, Name, Age, Gender, Income, CreditScore, CardType, CardLimit,
        # NumTransactions, AvgTransactionAmount, FraudFlag

        data = {
            'CustomerID': [self.fake.unique.random_int(min=100000, max=999999) for _ in range(self.num_rows)],
            'Name': [self.fake.name() for _ in range(self.num_rows)],
            'Age': np.random.randint(18, 75, size=self.num_rows),
            'Gender': np.random.choice(['M', 'F'], size=self.num_rows, p=[0.55, 0.45]),
            'Income': np.random.normal(loc=700000, scale=200000, size=self.num_rows).astype(int),
            'CreditScore': np.random.normal(loc=650, scale=70, size=self.num_rows).astype(int),
            'CardType': np.random.choice(['Silver', 'Gold', 'Platinum', 'Titanium'], size=self.num_rows, p=[0.4, 0.3, 0.2, 0.1]),
            'CardLimit': np.random.normal(loc=150000, scale=50000, size=self.num_rows).astype(int),
            'NumTransactions': np.random.poisson(lam=30, size=self.num_rows),
            'AvgTransactionAmount': np.random.normal(loc=5000, scale=2000, size=self.num_rows).astype(int),
            'FraudFlag': np.random.choice([0, 1], size=self.num_rows, p=[0.98, 0.02])
        }
        df = pd.DataFrame(data)

        # Clean Income, CardLimit, AvgTransactionAmount from negatives and set sensible bounds
        df['Income'] = df['Income'].apply(lambda x: max(abs(x), 10000))
        df['CreditScore'] = df['CreditScore'].apply(lambda x: min(max(x, 300), 850))  # Credit score range 300-850
        df['CardLimit'] = df['CardLimit'].apply(lambda x: max(abs(x), 5000))
        df['AvgTransactionAmount'] = df['AvgTransactionAmount'].apply(lambda x: max(abs(x), 100))

        return df

    def save_to_csv(self, filename='syntheticdata.csv'):
        try:
            df = self.generate_data()
            df.to_csv(filename, index=False)
            print(f"Synthetic data saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate Synthetic Credit Card Customer Data')
    parser.add_argument('--rows', type=int, default=10000, help='Number of rows of synthetic data to generate (default: 10000)')
    parser.add_argument('--output', type=str, default='syntheticdata.csv', help='Output CSV file name (default: syntheticdata.csv)')
    args = parser.parse_args()

    try:
        generator = SyntheticDataGenerator(num_rows=args.rows)
        generator.save_to_csv(args.output)
    except Exception as e:
        print(f"Error occurred: {e}")
