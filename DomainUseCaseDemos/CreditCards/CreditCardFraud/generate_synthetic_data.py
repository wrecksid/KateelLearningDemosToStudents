"""
Credit Card Fraud Detection - Synthetic Data Generator
=====================================================

This module generates realistic synthetic credit card transaction data
for educational purposes in fraud detection machine learning.

Author: Educational Demo
Course: Masters in Finance - AI/ML Applications
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
import argparse
import logging
from datetime import datetime, timedelta
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreditCardDataGenerator:
    """
    Generates synthetic credit card transaction data with realistic patterns.
    
    This class creates datasets that mimic real-world credit card transactions
    including normal and fraudulent patterns, suitable for machine learning
    fraud detection models.
    """
    
    def __init__(self, locale='en_IN', seed=42):
        """
        Initialize the data generator.
        
        Args:
            locale (str): Faker locale for generating realistic data
            seed (int): Random seed for reproducibility
        """
        self.fake = Faker(locale)
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
        
        logger.info(f"Initialized CreditCardDataGenerator with locale: {locale}")
        
    def generate_merchant_categories(self):
        """Generate realistic merchant categories and their risk profiles."""
        return {
            'grocery_stores': {'risk_score': 0.1, 'avg_amount': 2500, 'std_amount': 1200},
            'gas_stations': {'risk_score': 0.15, 'avg_amount': 1800, 'std_amount': 800},
            'restaurants': {'risk_score': 0.2, 'avg_amount': 1200, 'std_amount': 600},
            'online_retail': {'risk_score': 0.3, 'avg_amount': 3500, 'std_amount': 2000},
            'atm_withdrawals': {'risk_score': 0.25, 'avg_amount': 5000, 'std_amount': 2500},
            'electronics': {'risk_score': 0.4, 'avg_amount': 15000, 'std_amount': 10000},
            'jewelry': {'risk_score': 0.6, 'avg_amount': 25000, 'std_amount': 20000},
            'travel_booking': {'risk_score': 0.35, 'avg_amount': 12000, 'std_amount': 8000},
            'medical_services': {'risk_score': 0.1, 'avg_amount': 3000, 'std_amount': 2000},
            'entertainment': {'risk_score': 0.25, 'avg_amount': 2000, 'std_amount': 1000}
        }
    
    def generate_customer_profiles(self, num_customers):
        """
        Generate customer profiles with realistic Indian demographic data.
        
        Args:
            num_customers (int): Number of customer profiles to generate
            
        Returns:
            dict: Dictionary of customer profiles
        """
        logger.info(f"Generating {num_customers} customer profiles...")
        
        customers = {}
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 
                 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
        
        for i in range(num_customers):
            customer_id = f"CUST_{i+1:06d}"
            
            # Generate age and income correlation
            age = np.random.normal(35, 12)
            age = max(18, min(80, int(age)))
            
            # Income roughly correlates with age (peak earning years)
            base_income = 300000 + (age - 25) * 15000 if age > 25 else 200000
            income = max(150000, np.random.normal(base_income, base_income * 0.3))
            
            customers[customer_id] = {
                'name': self.fake.name(),
                'age': age,
                'city': random.choice(cities),
                'annual_income': int(income),
                'credit_limit': int(income * random.uniform(2, 5)),
                'account_age_months': random.randint(6, 120),
                'risk_profile': 'low' if income > 500000 else 'medium' if income > 300000 else 'high'
            }
        
        logger.info("Customer profiles generated successfully")
        return customers
    
    def generate_transactions(self, num_transactions, fraud_rate=0.02, 
                            amount_range=(100, 50000), time_range_days=90):
        """
        Generate realistic credit card transactions.
        
        Args:
            num_transactions (int): Number of transactions to generate
            fraud_rate (float): Percentage of fraudulent transactions (0.0-1.0)
            amount_range (tuple): Min and max transaction amounts in INR
            time_range_days (int): Number of days to spread transactions across
            
        Returns:
            pandas.DataFrame: Generated transaction data
        """
        logger.info(f"Generating {num_transactions} transactions with {fraud_rate*100:.1f}% fraud rate...")
        
        # Generate customers (10% of transaction count for realistic distribution)
        num_customers = max(100, num_transactions // 10)
        customers = self.generate_customer_profiles(num_customers)
        customer_ids = list(customers.keys())
        
        merchant_categories = self.generate_merchant_categories()
        category_names = list(merchant_categories.keys())
        
        transactions = []
        start_date = datetime.now() - timedelta(days=time_range_days)
        
        # Determine fraud transactions
        num_fraud = int(num_transactions * fraud_rate)
        fraud_indices = set(random.sample(range(num_transactions), num_fraud))
        
        for i in range(num_transactions):
            customer_id = random.choice(customer_ids)
            customer = customers[customer_id]
            category = random.choice(category_names)
            cat_info = merchant_categories[category]
            
            # Generate transaction timestamp
            random_days = random.uniform(0, time_range_days)
            transaction_time = start_date + timedelta(days=random_days)
            
            # Determine if this is a fraudulent transaction
            is_fraud = i in fraud_indices
            
            # Generate amount based on category and fraud status
            if is_fraud:
                # Fraudulent transactions tend to be higher amounts or unusual patterns
                if random.random() < 0.4:  # 40% high-value fraud
                    amount = np.random.lognormal(np.log(cat_info['avg_amount'] * 3), 0.8)
                else:  # 60% regular amount fraud (harder to detect)
                    amount = np.random.normal(cat_info['avg_amount'], cat_info['std_amount'])
            else:
                # Normal transaction
                amount = np.random.normal(cat_info['avg_amount'], cat_info['std_amount'])
            
            amount = max(amount_range[0], min(amount_range[1], abs(amount)))
            
            # Generate location (fraud might be in different city)
            if is_fraud and random.random() < 0.3:  # 30% of fraud from different city
                cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
                transaction_city = random.choice([c for c in cities if c != customer['city']])
            else:
                transaction_city = customer['city']
            
            # Generate time-based features
            hour = transaction_time.hour
            is_weekend = transaction_time.weekday() >= 5
            
            # Fraud patterns: unusual hours, weekends
            if is_fraud and random.random() < 0.4:
                hour = random.choice([2, 3, 4, 5, 22, 23])  # Unusual hours
            
            # Calculate derived features
            amount_to_income_ratio = amount / customer['annual_income'] * 12
            amount_to_limit_ratio = amount / customer['credit_limit']
            
            transaction = {
                'transaction_id': f"TXN_{i+1:08d}",
                'customer_id': customer_id,
                'timestamp': transaction_time.isoformat(),
                'amount': round(amount, 2),
                'merchant_category': category,
                'transaction_city': transaction_city,
                'customer_city': customer['city'],
                'hour_of_day': hour,
                'day_of_week': transaction_time.weekday(),
                'is_weekend': is_weekend,
                'customer_age': customer['age'],
                'customer_income': customer['annual_income'],
                'credit_limit': customer['credit_limit'],
                'account_age_months': customer['account_age_months'],
                'amount_to_income_ratio': amount_to_income_ratio,
                'amount_to_limit_ratio': amount_to_limit_ratio,
                'city_mismatch': transaction_city != customer['city'],
                'is_fraud': 1 if is_fraud else 0
            }
            
            transactions.append(transaction)
        
        df = pd.DataFrame(transactions)
        
        # Add some PCA-like anonymized features (V1-V10) similar to real fraud datasets
        np.random.seed(self.seed)
        for i in range(1, 11):
            if i <= 3:  # First few components capture most variance
                df[f'V{i}'] = np.random.normal(0, 2, len(df)) + df['is_fraud'] * np.random.normal(0, 1, len(df))
            else:
                df[f'V{i}'] = np.random.normal(0, 1, len(df))
        
        logger.info(f"Generated {len(df)} transactions ({df['is_fraud'].sum()} fraudulent)")
        return df
    
    def save_to_csv(self, df, filename='credit_card_transactions.csv'):
        """
        Save the generated dataset to CSV file.
        
        Args:
            df (pandas.DataFrame): Transaction data
            filename (str): Output filename
        """
        try:
            df.to_csv(filename, index=False)
            logger.info(f"Dataset saved to {filename}")
            logger.info(f"Dataset shape: {df.shape}")
            logger.info(f"Fraud rate: {df['is_fraud'].mean()*100:.2f}%")
        except Exception as e:
            logger.error(f"Error saving dataset: {str(e)}")
            raise

def main():
    """Main function to run the synthetic data generator."""
    parser = argparse.ArgumentParser(description='Generate synthetic credit card fraud data')
    parser.add_argument('--size', type=int, default=10000, 
                       help='Number of transactions to generate (default: 10000)')
    parser.add_argument('--fraud_rate', type=float, default=0.02,
                       help='Fraud rate (0.0-1.0, default: 0.02)')
    parser.add_argument('--output', type=str, default='credit_card_transactions.csv',
                       help='Output CSV filename')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility')
    parser.add_argument('--min_amount', type=int, default=100,
                       help='Minimum transaction amount in INR')
    parser.add_argument('--max_amount', type=int, default=50000,
                       help='Maximum transaction amount in INR')
    parser.add_argument('--days', type=int, default=90,
                       help='Number of days to spread transactions across')
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.size <= 0:
        logger.error("Size must be positive")
        sys.exit(1)
    
    if not 0 <= args.fraud_rate <= 1:
        logger.error("Fraud rate must be between 0 and 1")
        sys.exit(1)
    
    try:
        # Generate data
        generator = CreditCardDataGenerator(seed=args.seed)
        df = generator.generate_transactions(
            num_transactions=args.size,
            fraud_rate=args.fraud_rate,
            amount_range=(args.min_amount, args.max_amount),
            time_range_days=args.days
        )
        
        # Save to CSV
        generator.save_to_csv(df, args.output)
        
        # Print summary statistics
        print("\n" + "="*50)
        print("SYNTHETIC DATA GENERATION COMPLETE")
        print("="*50)
        print(f"Dataset size: {len(df):,} transactions")
        print(f"Fraud transactions: {df['is_fraud'].sum():,} ({df['is_fraud'].mean()*100:.2f}%)")
        print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print(f"Amount range: ₹{df['amount'].min():.2f} to ₹{df['amount'].max():.2f}")
        print(f"Average amount: ₹{df['amount'].mean():.2f}")
        print(f"Output file: {args.output}")
        print("\nTop merchant categories:")
        print(df['merchant_category'].value_counts().head())
        
    except Exception as e:
        logger.error(f"Error generating data: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
