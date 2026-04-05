"""
Bank Customer Data Generator
==========================

This module generates synthetic bank customer data for machine learning demonstrations.
Designed for educational purposes in AI/ML Finance courses.

Author: AI Assistant
License: MIT
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
import argparse
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BankDataGenerator:
    """
    A class to generate synthetic bank customer data with realistic patterns.
    
    This generator creates data that mimics real banking customer profiles
    including demographics, account information, transaction patterns, and
    financial behaviors suitable for customer segmentation analysis.
    """
    
    def __init__(self, locale='en_IN', seed=42):
        """
        Initialize the data generator.
        
        Args:
            locale (str): Faker locale for generating region-specific data
            seed (int): Random seed for reproducibility
        """
        try:
            self.fake = Faker(locale)
            Faker.seed(seed)
            np.random.seed(seed)
            random.seed(seed)
            logger.info(f"Initialized BankDataGenerator with locale: {locale}")
        except Exception as e:
            logger.error(f"Error initializing generator: {str(e)}")
            raise
    
    def generate_customer_data(self, 
                             num_records=10000,
                             min_age=18,
                             max_age=80,
                             min_income=150000,
                             max_income=5000000,
                             min_account_balance=1000,
                             max_account_balance=10000000,
                             churn_rate=0.15):
        """
        Generate synthetic bank customer data.
        
        Args:
            num_records (int): Number of customer records to generate
            min_age (int): Minimum customer age
            max_age (int): Maximum customer age
            min_income (int): Minimum annual income in INR
            max_income (int): Maximum annual income in INR
            min_account_balance (int): Minimum account balance in INR
            max_account_balance (int): Maximum account balance in INR
            churn_rate (float): Proportion of customers who have churned
            
        Returns:
            pd.DataFrame: Generated customer data
        """
        try:
            logger.info(f"Generating {num_records} customer records...")
            
            # Validate parameters
            self._validate_parameters(num_records, min_age, max_age, min_income, 
                                    max_income, min_account_balance, max_account_balance, churn_rate)
            
            data = []
            
            for i in range(num_records):
                if i % 1000 == 0:
                    logger.info(f"Generated {i} records...")
                
                # Basic demographics
                age = np.random.randint(min_age, max_age + 1)
                gender = random.choice(['Male', 'Female', 'Other'])
                
                # Income correlation with age (peak earning years 35-55)
                if 25 <= age <= 35:
                    income_multiplier = np.random.uniform(0.6, 1.2)
                elif 35 <= age <= 55:
                    income_multiplier = np.random.uniform(1.0, 2.0)
                else:
                    income_multiplier = np.random.uniform(0.4, 1.0)
                
                annual_income = np.random.uniform(min_income, max_income) * income_multiplier
                annual_income = max(min_income, min(max_income, annual_income))
                
                # Account balance correlated with income
                balance_ratio = np.random.lognormal(0, 1) * 0.1
                account_balance = annual_income * balance_ratio
                account_balance = max(min_account_balance, min(max_account_balance, account_balance))
                
                # Credit score (300-850 scale, correlated with income and age)
                base_credit_score = 300 + (annual_income / max_income) * 400 + (age / max_age) * 150
                credit_score = max(300, min(850, base_credit_score + np.random.normal(0, 50)))
                
                # Products owned
                num_products = np.random.poisson(2) + 1
                num_products = min(6, max(1, num_products))
                
                # Tenure with bank (years)
                tenure = max(0, np.random.exponential(5))
                
                # Monthly transactions
                monthly_transactions = max(1, np.random.poisson(15))
                
                # Digital engagement score (0-100)
                digital_score = np.random.beta(2, 2) * 100
                
                # Customer lifetime value (CLV)
                clv = (annual_income * 0.02 * tenure) + (account_balance * 0.01)
                
                # Churn status
                churn_probability = self._calculate_churn_probability(
                    age, annual_income, account_balance, credit_score, 
                    tenure, num_products, digital_score
                )
                is_churned = random.random() < churn_rate * churn_probability
                
                # Location data
                city = self.fake.city()
                state = self.fake.state()
                
                record = {
                    'customer_id': f'CUST_{i+1:06d}',
                    'name': self.fake.name(),
                    'age': int(age),
                    'gender': gender,
                    'city': city,
                    'state': state,
                    'annual_income': round(annual_income, 2),
                    'account_balance': round(account_balance, 2),
                    'credit_score': int(credit_score),
                    'num_products': int(num_products),
                    'tenure_years': round(tenure, 1),
                    'monthly_transactions': int(monthly_transactions),
                    'digital_engagement_score': round(digital_score, 1),
                    'customer_lifetime_value': round(clv, 2),
                    'is_churned': is_churned,
                    'account_type': random.choice(['Savings', 'Current', 'Salary']),
                    'marital_status': random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
                    'education': random.choice(['High School', 'Graduate', 'Post Graduate', 'Professional']),
                    'employment_status': random.choice(['Employed', 'Self-Employed', 'Unemployed', 'Retired']),
                    'created_date': self.fake.date_between(start_date='-10y', end_date='today')
                }
                
                data.append(record)
            
            df = pd.DataFrame(data)
            logger.info(f"Successfully generated {len(df)} customer records")
            return df
            
        except Exception as e:
            logger.error(f"Error generating customer data: {str(e)}")
            raise
    
    def _validate_parameters(self, num_records, min_age, max_age, min_income, 
                           max_income, min_account_balance, max_account_balance, churn_rate):
        """Validate input parameters."""
        if num_records <= 0:
            raise ValueError("Number of records must be positive")
        if min_age >= max_age:
            raise ValueError("Minimum age must be less than maximum age")
        if min_income >= max_income:
            raise ValueError("Minimum income must be less than maximum income")
        if min_account_balance >= max_account_balance:
            raise ValueError("Minimum balance must be less than maximum balance")
        if not 0 <= churn_rate <= 1:
            raise ValueError("Churn rate must be between 0 and 1")
    
    def _calculate_churn_probability(self, age, income, balance, credit_score, 
                                   tenure, num_products, digital_score):
        """Calculate churn probability based on customer characteristics."""
        try:
            # Younger customers more likely to churn
            age_factor = 1.5 if age < 30 else 0.8 if age > 50 else 1.0
            
            # Lower income customers more likely to churn
            income_factor = 1.3 if income < 300000 else 0.7
            
            # Lower balance customers more likely to churn
            balance_factor = 1.2 if balance < 50000 else 0.8
            
            # Lower credit score customers more likely to churn
            credit_factor = 1.4 if credit_score < 650 else 0.6
            
            # Shorter tenure customers more likely to churn
            tenure_factor = 1.5 if tenure < 2 else 0.7
            
            # Fewer products means higher churn probability
            product_factor = 1.3 if num_products < 2 else 0.6
            
            # Lower digital engagement means higher churn
            digital_factor = 1.2 if digital_score < 50 else 0.8
            
            churn_prob = (age_factor * income_factor * balance_factor * 
                         credit_factor * tenure_factor * product_factor * digital_factor) / 7
            
            return min(2.0, max(0.1, churn_prob))
            
        except Exception as e:
            logger.warning(f"Error calculating churn probability: {str(e)}")
            return 1.0
    
    def save_to_csv(self, df, filename='bank_customer_data.csv'):
        """
        Save DataFrame to CSV file.
        
        Args:
            df (pd.DataFrame): Customer data
            filename (str): Output filename
        """
        try:
            df.to_csv(filename, index=False)
            logger.info(f"Data saved to {filename}")
            print(f"✅ Successfully saved {len(df)} records to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            raise

def main():
    """Main function to run the data generator."""
    parser = argparse.ArgumentParser(description='Generate synthetic bank customer data')
    parser.add_argument('--records', type=int, default=10000, help='Number of records to generate')
    parser.add_argument('--output', type=str, default='bank_customer_data.csv', help='Output filename')
    parser.add_argument('--min-age', type=int, default=18, help='Minimum customer age')
    parser.add_argument('--max-age', type=int, default=80, help='Maximum customer age')
    parser.add_argument('--min-income', type=int, default=150000, help='Minimum annual income')
    parser.add_argument('--max-income', type=int, default=5000000, help='Maximum annual income')
    parser.add_argument('--churn-rate', type=float, default=0.15, help='Churn rate (0-1)')
    
    args = parser.parse_args()
    
    try:
        print("🏦 Bank Customer Data Generator")
        print("=" * 40)
        
        generator = BankDataGenerator(locale='en_IN')
        
        df = generator.generate_customer_data(
            num_records=args.records,
            min_age=args.min_age,
            max_age=args.max_age,
            min_income=args.min_income,
            max_income=args.max_income,
            churn_rate=args.churn_rate
        )
        
        generator.save_to_csv(df, args.output)
        
        print("\n📊 Data Summary:")
        print(f"Total Records: {len(df)}")
        print(f"Churned Customers: {df['is_churned'].sum()}")
        print(f"Average Age: {df['age'].mean():.1f}")
        print(f"Average Income: ₹{df['annual_income'].mean():,.0f}")
        print(f"Average Balance: ₹{df['account_balance'].mean():,.0f}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
