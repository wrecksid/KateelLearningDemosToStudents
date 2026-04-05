"""
Synthetic Credit Card Transactions Data Generator
Author: Vinaya Sathyanarayana

Generates synthetic credit card transaction data for fraud detection use.
The CSV output file is 'syntheticdata.csv' by default.

Features:
- Tunable dataset size (default 10,000 rows)
- Tunable fraud transaction ratio (default 2%)
- Locale: en_IN (English - India)
- Fraud transactions have distinct anomalies (high amounts, suspicious categories and locations)
- Robust error handling and reproducible seeding
"""

import pandas as pd
import random
from faker import Faker
import numpy as np


def generate_synthetic_data(num_rows=10000, fraud_ratio=0.02, seed=42, output_filename='syntheticdata.csv'):
    """
    Generate synthetic credit card transaction dataset with fraud labels.

    Args:
        num_rows (int): Number of samples to generate.
        fraud_ratio (float): Fraction of fraudulent transactions.
        seed (int): Random seed for reproducibility.
        output_filename (str): CSV output filename.

    Returns:
        pd.DataFrame: generated dataset
    """
    try:
        faker = Faker('en_IN')
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)

        data = []
        for _ in range(num_rows):
            card_num = faker.credit_card_number(card_type=None)
            card_expiry = faker.credit_card_expire()
            card_type = faker.credit_card_provider()
            transaction_amount = round(random.uniform(10.0, 50000.0), 2)
            transaction_date = faker.date_time_this_year()
            merchant_name = faker.company()
            merchant_category = random.choice(['Grocery', 'Electronics', 'Online Shopping', 'Travel', 'Restaurant',
                                              'Fuel', 'Utilities', 'Healthcare', 'Entertainment', 'Clothing'])
            location = f"{faker.city()}, {faker.state()}"
            is_fraud = 0

            if random.random() < fraud_ratio:
                is_fraud = 1
                transaction_amount = round(random.uniform(50000, 100000), 2)
                merchant_category = random.choice(['Online Shopping', 'Electronics', 'Travel'])
                location = random.choice(['Delhi, Delhi', 'Mumbai, Maharashtra', 'Bengaluru, Karnataka', 'Hyderabad, Telangana'])

            data.append([card_num, card_expiry, card_type, transaction_amount, transaction_date, merchant_name,
                         merchant_category, location, is_fraud])

        df = pd.DataFrame(data, columns=['CardNumber', 'ExpiryDate', 'CardType', 'TransactionAmount', 'TransactionDate',
                                         'MerchantName', 'MerchantCategory', 'Location', 'IsFraud'])
        df.to_csv(output_filename, index=False)
        print(f"Synthetic data generated and saved to {output_filename} with {num_rows} rows and fraud ratio {fraud_ratio}")
        return df

    except Exception as e:
        print(f"Error generating synthetic data: {e}")
        return None


if __name__ == "__main__":
    generate_synthetic_data()
