"""
Synthetic Credit Card Transaction Data Generator
Author: Vinaya Sathyanarayana

Generates synthetic credit card transaction data with fraud labels.
Allows tuning of dataset size and saves output as syntheticdata.csv.

Usage:
    python synthetic_data_generator.py [size]

    size: optional integer to specify number of rows (default 10000)

Outputs:
    syntheticdata.csv file with generated data

Features:
- transaction_id, customer_id (UUID)
- transaction_date (datetime within current year)
- merchant_category (various categories)
- transaction_amount (10 to 5000 INR)
- transaction_currency (INR)
- card_type (Credit, Debit, Prepaid)
- card_issuer (HDFC, SBI, ICICI, Axis, Kotak)
- is_fraud (binary label with ~2% fraud cases)

Students can customize merchant categories, card types, and fraud percentages in code.

"""

import sys
from faker import Faker
import pandas as pd
import random


class SyntheticDataGenerator:
    def __init__(self, size=10000, locale='en_IN'):
        if size <= 0:
            raise ValueError("Size must be a positive integer.")
        self.size = size
        self.fake = Faker(locale)
        self.data = None

    def generate(self):
        data = {
            'transaction_id': [self.fake.uuid4() for _ in range(self.size)],
            'customer_id': [self.fake.uuid4() for _ in range(self.size)],
            'transaction_date': [self.fake.date_time_this_year() for _ in range(self.size)],
            'merchant_category': [self.fake.random_element(elements=(
                'Grocery', 'Travel', 'Restaurant', 'Electronics',
                'Clothing', 'Health', 'Entertainment', 'Utilities')) for _ in range(self.size)],
            'transaction_amount': [round(random.uniform(10, 5000), 2) for _ in range(self.size)],
            'transaction_currency': ['INR'] * self.size,
            'card_type': [self.fake.random_element(elements=('Credit', 'Debit', 'Prepaid')) for _ in range(self.size)],
            'card_issuer': [self.fake.random_element(elements=('HDFC', 'SBI', 'ICICI', 'Axis', 'Kotak')) for _ in range(self.size)],
            'is_fraud': [self._generate_fraud_label() for _ in range(self.size)],
        }
        self.data = pd.DataFrame(data)
        return self.data

    def _generate_fraud_label(self):
        # Approx 2% fraud rate
        return 1 if random.random() < 0.02 else 0

    def save_to_csv(self, filename='syntheticdata.csv'):
        if self.data is None:
            raise ValueError("Data not generated yet. Call generate() first.")
        self.data.to_csv(filename, index=False)


def main():
    try:
        size = 10000
        if len(sys.argv) > 1:
            size = int(sys.argv[1])
        generator = SyntheticDataGenerator(size=size)
        df = generator.generate()
        generator.save_to_csv()
        print(f"Synthetic data generated with {size} rows and saved to syntheticdata.csv")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
