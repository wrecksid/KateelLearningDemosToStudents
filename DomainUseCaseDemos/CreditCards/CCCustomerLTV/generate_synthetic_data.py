"""
Credit Card Customer Synthetic Data Generator
============================================

This program generates synthetic credit card customer data for Lifetime Value analysis.
The data includes customer demographics, account information, transaction patterns,
and payment behavior suitable for CLV modeling.

Author: AI Assistant for Financial Analytics Course
Date: July 2025
"""

import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import BaseProvider
import random
import argparse
import logging
from datetime import datetime, timedelta
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreditCardProvider(BaseProvider):
    """Custom provider for credit card specific data"""
    
    card_types = ['Gold', 'Platinum', 'Silver', 'Premium', 'Classic']
    card_networks = ['Visa', 'Mastercard', 'RuPay']
    employment_types = ['Salaried', 'Self-Employed', 'Business Owner', 'Professional', 'Retired']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad', 
              'Kolkata', 'Jaipur', 'Lucknow', 'Indore', 'Nagpur', 'Surat', 'Vadodara']
    
    def card_type(self):
        return self.random_element(self.card_types)
    
    def card_network(self):
        return self.random_element(self.card_networks)
    
    def employment_type(self):
        return self.random_element(self.employment_types)
    
    def indian_city(self):
        return self.random_element(self.cities)

def generate_synthetic_data(num_records=10000, seed=42, **kwargs):
    """
    Generate synthetic credit card customer data
    
    Parameters:
    -----------
    num_records : int
        Number of records to generate (default: 10000)
    seed : int
        Random seed for reproducibility (default: 42)
    **kwargs : dict
        Additional parameters for data generation:
        - min_age : int (default: 18)
        - max_age : int (default: 75)
        - min_income : int (default: 200000)
        - max_income : int (default: 2000000)
        - min_tenure : int (default: 1)
        - max_tenure : int (default: 120)
        - churn_rate : float (default: 0.15)
    
    Returns:
    --------
    pd.DataFrame
        Synthetic customer data
    """
    
    # Set random seeds for reproducibility
    random.seed(seed)
    np.random.seed(seed)
    
    # Initialize Faker with Indian locale
    fake = Faker('en_IN')
    fake.add_provider(CreditCardProvider)
    Faker.seed(seed)
    
    # Extract parameters with defaults
    min_age = kwargs.get('min_age', 18)
    max_age = kwargs.get('max_age', 75)
    min_income = kwargs.get('min_income', 200000)
    max_income = kwargs.get('max_income', 2000000)
    min_tenure = kwargs.get('min_tenure', 1)
    max_tenure = kwargs.get('max_tenure', 120)
    churn_rate = kwargs.get('churn_rate', 0.15)
    
    logger.info(f"Generating {num_records} synthetic records with parameters:")
    logger.info(f"Age range: {min_age}-{max_age}, Income range: {min_income}-{max_income}")
    logger.info(f"Tenure range: {min_tenure}-{max_tenure} months, Churn rate: {churn_rate}")
    
    try:
        data = []
        
        for i in range(num_records):
            if i % 1000 == 0:
                logger.info(f"Generated {i} records...")
            
            # Basic demographics
            age = random.randint(min_age, max_age)
            gender = random.choice(['Male', 'Female'])
            city = fake.indian_city()
            annual_income = random.randint(min_income, max_income)
            employment_type = fake.employment_type()
            
            # Account information
            tenure_months = random.randint(min_tenure, max_tenure)
            card_type = fake.card_type()
            card_network = fake.card_network()
            
            # Credit limit based on income and profile
            income_multiplier = random.uniform(0.3, 2.0)
            if card_type in ['Platinum', 'Premium']:
                income_multiplier *= random.uniform(1.2, 2.5)
            credit_limit = min(int(annual_income * income_multiplier / 12), 500000)
            
            # Usage patterns
            avg_monthly_spend = random.uniform(0.1, 0.8) * credit_limit
            utilization_rate = avg_monthly_spend / credit_limit
            transactions_per_month = max(1, int(np.random.poisson(15) * (avg_monthly_spend / 10000)))
            
            # Payment behavior
            payment_ratio = random.uniform(0.05, 1.0)  # Fraction of balance paid
            if payment_ratio < 0.1:  # Minimum payment customers
                payment_ratio = random.uniform(0.05, 0.15)
            
            late_payments_12m = max(0, int(np.random.poisson(1.5) * (1 - payment_ratio)))
            
            # Current balance
            current_balance = avg_monthly_spend * random.uniform(0.5, 2.0)
            current_balance = min(current_balance, credit_limit)
            
            # Customer status
            is_active = random.random() > churn_rate
            
            # Revenue components (monthly)
            interchange_revenue = avg_monthly_spend * random.uniform(0.015, 0.025)  # 1.5-2.5%
            interest_revenue = current_balance * random.uniform(0.015, 0.035) if payment_ratio < 0.9 else 0
            annual_fee = random.choice([0, 500, 1500, 3000, 5000]) if card_type != 'Classic' else 0
            monthly_fee_revenue = annual_fee / 12
            
            total_monthly_revenue = interchange_revenue + interest_revenue + monthly_fee_revenue
            
            # Costs (monthly)
            acquisition_cost = random.uniform(2000, 8000) / tenure_months  # Amortized
            servicing_cost = random.uniform(100, 300)
            default_risk_cost = current_balance * random.uniform(0.001, 0.01) * (late_payments_12m / 12)
            
            total_monthly_cost = acquisition_cost + servicing_cost + default_risk_cost
            
            # Monthly profit
            monthly_profit = total_monthly_revenue - total_monthly_cost
            
            record = {
                'customer_id': f'CC_{i+1:06d}',
                'age': age,
                'gender': gender,
                'city': city,
                'annual_income': annual_income,
                'employment_type': employment_type,
                'tenure_months': tenure_months,
                'card_type': card_type,
                'card_network': card_network,
                'credit_limit': int(credit_limit),
                'current_balance': round(current_balance, 2),
                'utilization_rate': round(utilization_rate, 3),
                'avg_monthly_spend': round(avg_monthly_spend, 2),
                'transactions_per_month': transactions_per_month,
                'payment_ratio': round(payment_ratio, 3),
                'late_payments_12m': late_payments_12m,
                'is_active': is_active,
                'interchange_revenue': round(interchange_revenue, 2),
                'interest_revenue': round(interest_revenue, 2),
                'annual_fee': annual_fee,
                'monthly_revenue': round(total_monthly_revenue, 2),
                'monthly_cost': round(total_monthly_cost, 2),
                'monthly_profit': round(monthly_profit, 2),
                'last_transaction_date': fake.date_between(start_date='-3M', end_date='today'),
                'account_opening_date': fake.date_between(start_date=f'-{tenure_months+12}M', end_date=f'-{tenure_months}M')
            }
            
            data.append(record)
        
        df = pd.DataFrame(data)
        logger.info(f"Successfully generated {len(df)} records")
        return df
        
    except Exception as e:
        logger.error(f"Error generating synthetic data: {str(e)}")
        raise

def save_to_csv(df, filename='syntheticdata.csv'):
    """Save DataFrame to CSV file"""
    try:
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
        logger.info(f"File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
    except Exception as e:
        logger.error(f"Error saving to CSV: {str(e)}")
        raise

def print_data_summary(df):
    """Print summary statistics of generated data"""
    print("\n" + "="*60)
    print("SYNTHETIC DATA SUMMARY")
    print("="*60)
    print(f"Total Records: {len(df):,}")
    print(f"Total Features: {len(df.columns)}")
    print("\nData Types:")
    print(df.dtypes.value_counts())
    
    print("\nKey Statistics:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe())
    
    print("\nCategorical Distributions:")
    categorical_cols = ['gender', 'card_type', 'employment_type', 'is_active']
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n{col}:")
            print(df[col].value_counts())

def main():
    """Main function to handle command line arguments and generate data"""
    parser = argparse.ArgumentParser(description='Generate synthetic credit card customer data for CLV analysis')
    parser.add_argument('--records', type=int, default=10000, help='Number of records to generate (default: 10000)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility (default: 42)')
    parser.add_argument('--filename', type=str, default='syntheticdata.csv', help='Output filename (default: syntheticdata.csv)')
    parser.add_argument('--min-age', type=int, default=18, help='Minimum age (default: 18)')
    parser.add_argument('--max-age', type=int, default=75, help='Maximum age (default: 75)')
    parser.add_argument('--min-income', type=int, default=200000, help='Minimum annual income (default: 200000)')
    parser.add_argument('--max-income', type=int, default=2000000, help='Maximum annual income (default: 2000000)')
    parser.add_argument('--min-tenure', type=int, default=1, help='Minimum tenure in months (default: 1)')
    parser.add_argument('--max-tenure', type=int, default=120, help='Maximum tenure in months (default: 120)')
    parser.add_argument('--churn-rate', type=float, default=0.15, help='Customer churn rate (default: 0.15)')
    parser.add_argument('--summary', action='store_true', help='Print data summary')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.records <= 0:
        logger.error("Number of records must be positive")
        sys.exit(1)
    
    if not (0 <= args.churn_rate <= 1):
        logger.error("Churn rate must be between 0 and 1")
        sys.exit(1)
    
    try:
        # Generate synthetic data
        df = generate_synthetic_data(
            num_records=args.records,
            seed=args.seed,
            min_age=args.min_age,
            max_age=args.max_age,
            min_income=args.min_income,
            max_income=args.max_income,
            min_tenure=args.min_tenure,
            max_tenure=args.max_tenure,
            churn_rate=args.churn_rate
        )
        
        # Save to CSV
        save_to_csv(df, args.filename)
        
        # Print summary if requested
        if args.summary:
            print_data_summary(df)
        
        print(f"\n✅ Successfully generated {len(df):,} records and saved to {args.filename}")
        
    except Exception as e:
        logger.error(f"Failed to generate data: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
