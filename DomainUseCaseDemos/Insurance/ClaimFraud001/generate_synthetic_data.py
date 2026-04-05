"""
Synthetic Insurance Claim Data Generator
Author: Vinaya Sathyanarayana

Generates synthetic insurance claims data to simulate real-life datasets.
Uses Faker with 'en_IN' locale for realistic data generation in Indian context.

Features:
- Default dataset size: 10,000 rows (modifiable)
- Parameter tuning: dataset size, max claim amount, fraud probability
- Outputs CSV file 'syntheticdata.csv' in working directory

Instructions for students:
- Adjust parameters in main() to explore data scale and fraud incidence effects
- Use the generated 'syntheticdata.csv' as input for fraud detection algorithms

Instructions for banks:
- Use to simulate claim data to test and tune fraud detection models before deploying in production
- Tune fraud_probability and claim amount ranges to mimic organization-specific patterns

Error Handling:
- Handles invalid parameter inputs and file write errors gracefully
"""

import pandas as pd
import random
import sys

try:
    from faker import Faker
except ImportError:
    print("Faker library not found. Please install dependencies using 'pip install -r requirements.txt'")
    sys.exit(1)


def generate_synthetic_insurance_claim_data(
        num_rows=10000,
        locale='en_IN',
        seed=42,
        max_claim_amount=1000000,
        fraud_probability=0.05
):
    """
    Generate synthetic insurance claims dataset.

    Args:
    - num_rows (int): number of records to generate.
    - locale (str): Faker locale, default 'en_IN' for Indian English.
    - seed (int): random seed for reproducibility.
    - max_claim_amount (float): max claim amount value.
    - fraud_probability (float): base probability (0-1) that a claim is fraudulent.

    Returns:
    - pd.DataFrame: generated dataset.
    """
    if not (0 <= fraud_probability <= 1):
        raise ValueError("fraud_probability must be between 0 and 1")
    if num_rows <= 0:
        raise ValueError("num_rows must be positive")
    if max_claim_amount <= 0:
        raise ValueError("max_claim_amount must be positive")

    fake = Faker(locale)
    Faker.seed(seed)

    claim_types = ['Accident', 'Health', 'Theft', 'Fire', 'Natural Disaster', 'Other']
    claim_status = ['Approved', 'Rejected', 'Under Review']
    fraud_flags = [0, 1]  # 0 = Not Fraud, 1 = Fraud

    data = []

    for _ in range(num_rows):
        policy_id = fake.bothify(text='????-########')  # Alphanumeric policy ID
        customer_id = fake.random_int(min=100000, max=999999)  # Removed .unique to avoid duplicates
        date_of_claim = fake.date_between(start_date='-2y', end_date='today')
        claim_type = random.choices(claim_types, weights=[0.3, 0.25, 0.15, 0.10, 0.10, 0.10])[0]
        claim_amount = round(random.uniform(1000, max_claim_amount), 2)

        # Fraud chance modification based on patterns
        fraud_chance = fraud_probability
        if claim_type in ['Theft', 'Fire'] and claim_amount > 500000:
            fraud_chance = min(1.0, fraud_probability * 4)
        elif claim_type == 'Health' and claim_amount > 700000:
            fraud_chance = min(1.0, fraud_probability * 3)

        fraud_flag = random.choices(fraud_flags, weights=[1 - fraud_chance, fraud_chance])[0]
        adjuster_id = fake.random_int(min=1000, max=9999)  # Removed .unique for same reason
        claim_status_choice = random.choices(claim_status, weights=[0.7, 0.2, 0.1])[0]

        data.append([
            policy_id,
            customer_id,
            date_of_claim,
            claim_type,
            claim_amount,
            claim_status_choice,
            fraud_flag,
            adjuster_id
        ])

    df = pd.DataFrame(data, columns=[
        'PolicyID', 'CustomerID', 'DateOfClaim',
        'ClaimType', 'ClaimAmount', 'ClaimStatus',
        'FraudFlag', 'AdjusterID'
    ])

    try:
        df.to_csv('syntheticdata.csv', index=False)
        print(f"Synthetic dataset generated and saved as 'syntheticdata.csv' with {num_rows} rows.")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

    return df


if __name__ == '__main__':
    # Run with default params; students can modify here or call function externally
    generate_synthetic_insurance_claim_data()
