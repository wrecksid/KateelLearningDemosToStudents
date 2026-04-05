"""
Synthetic Data Generator for Banking Product Ownership
Author: Vinaya Sathyanarayana

Generates synthetic data simulating customers and their owned financial products for 
marketing upsell and cross sell pattern mining use case.

Features:
- Configurable dataset size (default 10,000 rows)
- Locale support (default en_IN for Indian customers)
- Outputs CSV file named 'syntheticdata.csv'
- Generates customer demographics and multiple banking product ownership flags
"""

import pandas as pd
from faker import Faker
import random

class SyntheticDataGenerator:
    def __init__(self, size=10000, locale='en_IN'):
        self.size = size
        self.fake = Faker(locale)
        self.locale = locale
        self.data = None

    def generate_customer_data(self):
        """Generates synthetic banking product ownership data."""
        data = []

        products = [
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

        for _ in range(self.size):
            customer_id = self.fake.unique.random_int(min=100000, max=999999)
            age = random.randint(21, 70)
            gender = random.choice(['Male', 'Female', 'Other'])
            income = round(random.gauss(50000, 15000), 2)  # Monthly income INR
            if income < 10000:
                income = 10000
            tenure_years = random.randint(0, 20)  # Years as bank customer

            owns_products = {product: (random.random() < 0.3) for product in products}

            # Ensure at least one product is owned
            if not any(owns_products.values()):
                owns_products[random.choice(products)] = True

            row = {
                'CustomerID': customer_id,
                'Age': age,
                'Gender': gender,
                'MonthlyIncomeINR': income,
                'BankTenureYears': tenure_years,
            }
            row.update(owns_products)
            data.append(row)

        self.data = pd.DataFrame(data)
        return self.data

    def save_to_csv(self, filename='syntheticdata.csv'):
        if self.data is None:
            raise ValueError("Data not generated yet. Call generate_customer_data() first.")
        self.data.to_csv(filename, index=False)
        return filename

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate synthetic banking data for upsell/cross sell pattern mining.")
    parser.add_argument('--size', type=int, default=10000, help='Number of records to generate (default 10000)')
    parser.add_argument('--locale', type=str, default='en_IN', help='Locale for faker data (default en_IN)')
    parser.add_argument('--output', type=str, default='syntheticdata.csv', help='CSV output filename (default syntheticdata.csv)')

    args = parser.parse_args()

    try:
        gen = SyntheticDataGenerator(size=args.size, locale=args.locale)
        gen.generate_customer_data()
        file = gen.save_to_csv(filename=args.output)
        print(f"Synthetic data generated and saved to {file}")
    except Exception as e:
        print(f"Error during data generation: {e}")

if __name__ == '__main__':
    main()
