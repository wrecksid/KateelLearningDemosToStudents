"""
Synthetic Financial Data Generator
Author: Vinaya Sathyanarayana

This program generates synthetic financial dataset for classification tasks, simulating bank customers with attributes relevant for credit risk prediction (default or no default).

Features include:
- Age, Annual Income
- Credit Card ownership, Loan status (binary features)
- Gender, Occupation, State (categorical features)
- Target variable: Default (0=No, 1=Yes)

Students can tune:
- Number of rows (default 10000)
- Income range, Age range
- Probability of Credit Card and Loan ownership
- Probability of Default base rate

Generated data is saved to 'syntheticdata.csv' in CSV format.

Usage:
- Run as a script to generate data.
- Modify parameters in main or call function from Jupyter Notebook/other scripts.

Bank use case:
- Generate realistic customer population data.
- Simulate default based on risk factors for credit risk modeling.
- Data can be used for classification algorithm training/testing and management decisions.

"""

import pandas as pd
import random
import sys

try:
    from faker import Faker
except ImportError as e:
    print("Error: Faker library is not installed. Please install it using 'pip install Faker'.")
    sys.exit(1)


def generate_synthetic_financial_data(
        num_rows=10000,
        locale='en_IN',
        income_min=10000,
        income_max=200000,
        age_min=18,
        age_max=75,
        credit_card_prob=0.6,
        loan_prob=0.3,
        default_prob=0.1):
    """
    Generate synthetic financial customer data for classification.

    Args:
        num_rows (int): Number of rows of data to generate. Default is 10000.
        locale (str): Locale setting for Faker (default 'en_IN' for English India).
        income_min (float): Minimum annual income.
        income_max (float): Maximum annual income.
        age_min (int): Minimum age.
        age_max (int): Maximum age.
        credit_card_prob (float): Probability customer owns a credit card.
        loan_prob (float): Probability customer has an active loan.
        default_prob (float): Base probability of default.

    Returns:
        pd.DataFrame: DataFrame containing the synthetic dataset.
    """

    try:
        fake = Faker(locale)
        Faker.seed(42)
    except Exception as e:
        print(f"Error initializing Faker with locale {locale}: {e}")
        sys.exit(1)

    data = []

    for _ in range(num_rows):
        age = random.randint(age_min, age_max)
        income = round(random.uniform(income_min, income_max), 2)
        credit_card = 1 if random.random() < credit_card_prob else 0
        loan = 1 if random.random() < loan_prob else 0

        # Compute base default risk influenced by presence of loan, credit card and low income
        base_default_prob = default_prob
        if loan == 1:
            base_default_prob += 0.1
        if credit_card == 1:
            base_default_prob += 0.05
        if income < 50000:
            base_default_prob += 0.05

        default_risk = 1 if random.random() < base_default_prob else 0

        gender = random.choice(['Male', 'Female'])
        occupation = random.choice(['Salaried', 'Self-employed', 'Student', 'Retired'])

        state = random.choice(['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Gujarat', 'West Bengal'])

        data.append([age, income, credit_card, loan, default_risk, gender, occupation, state])

    df = pd.DataFrame(data, columns=['Age', 'Annual_Income', 'Credit_Card', 'Loan', 'Default', 'Gender', 'Occupation', 'State'])

    try:
        df.to_csv('syntheticdata.csv', index=False)
        print("Synthetic dataset generated and saved as 'syntheticdata.csv'")
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        sys.exit(1)

    return df


if __name__ == "__main__":
    # Default generation with 10k rows, tunable by editing the parameters below or calling the function externally
    generate_synthetic_financial_data()
