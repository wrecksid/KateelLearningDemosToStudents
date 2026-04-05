"""
Author: Vinaya Sathyanarayana

Synthetic Data Generator for Financial Clustering Demos

This program generates synthetic financial customer data 
with tunable parameters and realistic patterns primarily 
for clustering algorithm demonstrations in finance.

Features:
- Uses Faker with locale 'en_IN' for Indian context data
- Tunable parameters for income, age, transaction amount
- Generates customers with fields including demographics, accounts, transactions, risk score, and segments
- Outputs CSV file named 'syntheticdata.csv'
- Default size 10000 rows, user can specify size and tuning params
- Well documented with error handling

Instructions for students:
- Install dependencies using `pip install -r requirements.txt`
- Run this script directly, optionally specify size and tuning dict on initialization
- Explore data fields to understand typical financial customer attributes
- Modify tuning parameters to see how data distribution changes

Instructions for banks:
- Use this script as a blueprint to synthesize customer data for model prototyping and training without exposing real customer data
- Adjust tuning parameters to mimic your customer base distribution
- Use the data with clustering models to segment customers based on risk and transaction behaviors

"""

import sys
import traceback
from faker import Faker
import pandas as pd
import numpy as np

class SyntheticDataGenerator:
    def __init__(self, size=10000, locale='en_IN', seed=None):
        """
        Initializes the generator.
        :param size: Number of rows to generate (default 10000)
        :param locale: Faker locale (default 'en_IN')
        :param seed: Random seed for reproducibility (default None)
        """
        self.size = size
        self.locale = locale
        self.seed = seed
        try:
            self.faker = Faker(self.locale)
            if seed is not None:
                Faker.seed(seed)
                np.random.seed(seed)
        except Exception as e:
            print("Error initializing Faker:", e)
            sys.exit(1)

    def generate_data(self, tune_params=None):
        """
        Generate synthetic data.
        :param tune_params: dict with optional tuning parameters:
                'income_mean', 'income_std', 'age_mean', 'age_std',
                'transaction_amount_mean', 'transaction_amount_std'
        :return: Pandas DataFrame with synthetic data
        """
        try:
            if tune_params is None:
                tune_params = {}
            income_mean = tune_params.get('income_mean', 70000)
            income_std = tune_params.get('income_std', 30000)
            age_mean = tune_params.get('age_mean', 40)
            age_std = tune_params.get('age_std', 10)
            transaction_amount_mean = tune_params.get('transaction_amount_mean', 5000)
            transaction_amount_std = tune_params.get('transaction_amount_std', 2000)

            data = []
            for _ in range(self.size):
                # Customer Information
                name = self.faker.name()
                age = int(np.clip(np.random.normal(age_mean, age_std), 18, 100))
                gender = self.faker.random_element(elements=('Male', 'Female', 'Other'))
                city = self.faker.city()
                state = self.faker.state()
                income = np.clip(np.random.normal(income_mean, income_std), 10000, None)  # INR income
                
                # Account Information
                account_id = self.faker.unique.bban()
                account_type = self.faker.random_element(elements=('Savings', 'Current', 'Salary', 'Fixed Deposit'))
                account_open_date = self.faker.date_between(start_date='-10y', end_date='today')

                # Transaction Information
                transaction_date = self.faker.date_between(start_date=account_open_date, end_date='today')
                transaction_type = self.faker.random_element(elements=('Debit', 'Credit', 'Transfer'))
                transaction_amount = np.clip(np.random.normal(transaction_amount_mean, transaction_amount_std), 10, None)

                # Customer risk score and latent segment (for clustering)
                risk_score = np.clip(np.random.beta(2, 5) * 100, 0, 100)

                # Define segments based on income and risk score
                if income > 100000 and risk_score < 30:
                    segment = 'Premium Low Risk'
                elif income <= 100000 and 30 <= risk_score < 70:
                    segment = 'Mid Risk Mid Income'
                else:
                    segment = 'High Risk Low Income'

                # Feedback sentiment (categorical text data)
                feedback = self.faker.random_element(elements=("Positive", "Neutral", "Negative"))

                # Time-series-like data: monthly transactions and volume (synthetic)
                monthly_transactions = np.random.poisson(5 if segment == 'Premium Low Risk' else 3 if segment == 'Mid Risk Mid Income' else 1)
                monthly_volume = monthly_transactions * transaction_amount

                row = {
                    'Name': name,
                    'Age': age,
                    'Gender': gender,
                    'City': city,
                    'State': state,
                    'Income_INR': round(income, 2),
                    'Account_ID': account_id,
                    'Account_Type': account_type,
                    'Account_Open_Date': account_open_date,
                    'Transaction_Date': transaction_date,
                    'Transaction_Type': transaction_type,
                    'Transaction_Amount_INR': round(transaction_amount, 2),
                    'Risk_Score': round(risk_score, 2),
                    'Segment': segment,
                    'Feedback': feedback,
                    'Monthly_Transactions': monthly_transactions,
                    'Monthly_Volume_INR': round(monthly_volume, 2)
                }
                data.append(row)

            df = pd.DataFrame(data)
            df.to_csv('syntheticdata.csv', index=False)
            print(f"Generated synthetic data saved to syntheticdata.csv ({self.size} rows).")
            return df
        except Exception as e:
            print("Error during data generation:", e)
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    # Default generate and save synthetic data
    generator = SyntheticDataGenerator()
    generator.generate_data()

