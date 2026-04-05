#!/usr/bin/env python3
"""
Synthetic Financial Transaction Data Generator for Liquidity Management Simulations

This script generates synthetic financial transaction data that mimics real-world banking
datasets for use in agent-based liquidity management simulations using Mesa library.

Author: Finance Analytics Course
Purpose: Educational demonstration of liquidity management concepts
Locale: en_IN (English - India)
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import argparse
import sys
import os
from typing import Dict, List, Optional, Tuple
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialDataGenerator:
    """
    A comprehensive synthetic financial data generator for banking and liquidity simulations.
    
    This class generates realistic financial transaction data including:
    - Customer accounts and profiles
    - Transaction histories
    - Account balances and movements
    - Liquidity metrics
    - Risk indicators
    """
    
    def __init__(self, locale: str = 'en_IN', seed: Optional[int] = None):
        """
        Initialize the financial data generator.
        
        Args:
            locale (str): Faker locale for generating location-specific data
            seed (int, optional): Random seed for reproducible data generation
        """
        self.fake = Faker(locale)
        if seed:
            Faker.seed(seed)
            np.random.seed(seed)
            random.seed(seed)
        
        # Financial constants and parameters
        self.ACCOUNT_TYPES = ['savings', 'current', 'fixed_deposit', 'loan', 'credit_card']
        self.TRANSACTION_TYPES = ['deposit', 'withdrawal', 'transfer', 'payment', 'interest']
        self.CUSTOMER_SEGMENTS = ['retail', 'corporate', 'sme', 'hni']
        self.CHANNELS = ['atm', 'branch', 'online', 'mobile', 'pos']
        self.CURRENCIES = ['INR', 'USD', 'EUR', 'GBP']
        
        # Realistic parameter ranges
        self.BALANCE_RANGES = {
            'savings': (1000, 500000),
            'current': (5000, 10000000),
            'fixed_deposit': (10000, 5000000),
            'loan': (-1000000, -10000),
            'credit_card': (-100000, 50000)
        }
        
        self.TRANSACTION_AMOUNT_RANGES = {
            'retail': (100, 50000),
            'corporate': (10000, 10000000),
            'sme': (1000, 1000000),
            'hni': (5000, 2000000)
        }
        
    def generate_customers(self, num_customers: int) -> pd.DataFrame:
        """
        Generate synthetic customer data.
        
        Args:
            num_customers (int): Number of customers to generate
            
        Returns:
            pd.DataFrame: Customer data with demographics and risk profiles
        """
        try:
            logger.info(f"Generating {num_customers} customer records...")
            
            customers = []
            for i in range(num_customers):
                customer = {
                    'customer_id': f"CUST_{i+1:06d}",
                    'name': self.fake.name(),
                    'email': self.fake.email(),
                    'phone': self.fake.phone_number(),
                    'address': self.fake.address().replace('\n', ', '),
                    'city': self.fake.city(),
                    'state': self.fake.state(),
                    'pincode': self.fake.postcode(),
                    'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                    'gender': random.choice(['M', 'F', 'O']),
                    'occupation': self.fake.job(),
                    'annual_income': np.random.lognormal(11, 0.8),  # Log-normal distribution for income
                    'customer_segment': np.random.choice(
                        self.CUSTOMER_SEGMENTS, 
                        p=[0.6, 0.2, 0.15, 0.05]  # Realistic distribution
                    ),
                    'risk_score': np.random.normal(500, 100),  # Credit score like distribution
                    'customer_since': self.fake.date_between(start_date='-10y', end_date='today'),
                    'kyc_status': np.random.choice(['verified', 'pending', 'incomplete'], p=[0.85, 0.1, 0.05]),
                    'is_active': np.random.choice([True, False], p=[0.9, 0.1])
                }
                customers.append(customer)
                
            df = pd.DataFrame(customers)
            logger.info("Customer data generated successfully")
            return df
            
        except Exception as e:
            logger.error(f"Error generating customer data: {str(e)}")
            raise
    
    def generate_accounts(self, customers_df: pd.DataFrame, accounts_per_customer: int = 2) -> pd.DataFrame:
        """
        Generate synthetic account data linked to customers.
        
        Args:
            customers_df (pd.DataFrame): Customer data
            accounts_per_customer (int): Average number of accounts per customer
            
        Returns:
            pd.DataFrame: Account data with balances and account details
        """
        try:
            accounts = []
            account_counter = 1
            
            logger.info(f"Generating accounts for {len(customers_df)} customers...")
            
            for _, customer in customers_df.iterrows():
                # Number of accounts varies by customer segment
                segment_multiplier = {
                    'retail': 1, 'sme': 2, 'corporate': 3, 'hni': 4
                }
                num_accounts = np.random.poisson(
                    accounts_per_customer * segment_multiplier[customer['customer_segment']]
                )
                num_accounts = max(1, min(num_accounts, 6))  # Between 1-6 accounts
                
                for _ in range(num_accounts):
                    account_type = np.random.choice(self.ACCOUNT_TYPES)
                    min_bal, max_bal = self.BALANCE_RANGES[account_type]
                    
                    account = {
                        'account_id': f"ACC_{account_counter:08d}",
                        'customer_id': customer['customer_id'],
                        'account_type': account_type,
                        'account_number': self.fake.bban(),
                        'ifsc_code': f"BANK{random.randint(100000, 999999)}",
                        'branch_code': f"BR{random.randint(1000, 9999)}",
                        'currency': np.random.choice(self.CURRENCIES, p=[0.8, 0.1, 0.05, 0.05]),
                        'opening_date': self.fake.date_between(
                            start_date=customer['customer_since'], 
                            end_date='today'
                        ),
                        'current_balance': np.random.uniform(min_bal, max_bal),
                        'available_balance': 0,  # Will be calculated
                        'minimum_balance': min_bal * 0.1 if account_type in ['savings', 'current'] else 0,
                        'interest_rate': self._get_interest_rate(account_type),
                        'is_active': np.random.choice([True, False], p=[0.95, 0.05]),
                        'last_transaction_date': self.fake.date_between(start_date='-30d', end_date='today')
                    }
                    
                    # Calculate available balance (current balance minus holds/freezes)
                    hold_percentage = np.random.uniform(0, 0.1)  # 0-10% on hold
                    account['available_balance'] = account['current_balance'] * (1 - hold_percentage)
                    
                    accounts.append(account)
                    account_counter += 1
            
            df = pd.DataFrame(accounts)
            logger.info(f"Generated {len(df)} accounts")
            return df
            
        except Exception as e:
            logger.error(f"Error generating account data: {str(e)}")
            raise
    
    def generate_transactions(self, accounts_df: pd.DataFrame, num_transactions: int) -> pd.DataFrame:
        """
        Generate synthetic transaction data.
        
        Args:
            accounts_df (pd.DataFrame): Account data
            num_transactions (int): Number of transactions to generate
            
        Returns:
            pd.DataFrame: Transaction data with realistic patterns
        """
        try:
            logger.info(f"Generating {num_transactions} transactions...")
            
            transactions = []
            active_accounts = accounts_df[accounts_df['is_active'] == True]['account_id'].tolist()
            
            for i in range(num_transactions):
                account_id = random.choice(active_accounts)
                account_info = accounts_df[accounts_df['account_id'] == account_id].iloc[0]
                
                transaction = {
                    'transaction_id': f"TXN_{i+1:010d}",
                    'account_id': account_id,
                    'transaction_type': np.random.choice(self.TRANSACTION_TYPES),
                    'transaction_date': self.fake.date_time_between(start_date='-90d', end_date='now'),
                    'amount': self._generate_transaction_amount(account_info),
                    'currency': account_info['currency'],
                    'channel': np.random.choice(self.CHANNELS),
                    'description': self._generate_transaction_description(),
                    'reference_number': self.fake.uuid4(),
                    'status': np.random.choice(['completed', 'pending', 'failed'], p=[0.9, 0.05, 0.05]),
                    'fees': 0,  # Will be calculated
                    'exchange_rate': 1.0 if account_info['currency'] == 'INR' else np.random.uniform(70, 90),
                    'merchant_category': self._get_merchant_category(),
                    'location': f"{self.fake.city()}, {self.fake.state()}",
                    'device_id': self.fake.uuid4() if random.random() > 0.5 else None
                }
                
                # Calculate fees based on transaction type and amount
                transaction['fees'] = self._calculate_transaction_fees(
                    transaction['transaction_type'], 
                    transaction['amount'],
                    transaction['channel']
                )
                
                transactions.append(transaction)
            
            df = pd.DataFrame(transactions)
            df = df.sort_values('transaction_date').reset_index(drop=True)
            logger.info("Transaction data generated successfully")
            return df
            
        except Exception as e:
            logger.error(f"Error generating transaction data: {str(e)}")
            raise
    
    def generate_liquidity_metrics(self, accounts_df: pd.DataFrame, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate liquidity-specific metrics for the simulation.
        
        Args:
            accounts_df (pd.DataFrame): Account data
            transactions_df (pd.DataFrame): Transaction data
            
        Returns:
            pd.DataFrame: Liquidity metrics by account
        """
        try:
            logger.info("Calculating liquidity metrics...")
            
            metrics = []
            
            for _, account in accounts_df.iterrows():
                account_txns = transactions_df[
                    transactions_df['account_id'] == account['account_id']
                ]
                
                # Calculate various liquidity metrics
                metric = {
                    'account_id': account['account_id'],
                    'customer_id': account['customer_id'],
                    'current_balance': account['current_balance'],
                    'available_balance': account['available_balance'],
                    'avg_daily_balance': account_txns['amount'].mean() if not account_txns.empty else account['current_balance'],
                    'transaction_velocity': len(account_txns) / 90,  # Transactions per day over 90 days
                    'largest_withdrawal': account_txns[account_txns['transaction_type'] == 'withdrawal']['amount'].max() if not account_txns.empty else 0,
                    'withdrawal_frequency': len(account_txns[account_txns['transaction_type'] == 'withdrawal']) / 90,
                    'deposit_frequency': len(account_txns[account_txns['transaction_type'] == 'deposit']) / 90,
                    'balance_volatility': account_txns['amount'].std() if not account_txns.empty else 0,
                    'liquidity_ratio': account['available_balance'] / max(account['current_balance'], 1),
                    'cash_conversion_cycle': np.random.uniform(10, 60),  # Days
                    'credit_utilization': np.random.uniform(0, 0.8) if account['account_type'] == 'credit_card' else 0,
                    'liquidity_risk_score': np.random.normal(50, 15),  # 0-100 scale
                    'stress_test_survival_days': np.random.uniform(30, 180)  # Days the account can survive stress
                }
                
                metrics.append(metric)
            
            df = pd.DataFrame(metrics)
            logger.info("Liquidity metrics calculated successfully")
            return df
            
        except Exception as e:
            logger.error(f"Error calculating liquidity metrics: {str(e)}")
            raise
    
    def _get_interest_rate(self, account_type: str) -> float:
        """Get realistic interest rates by account type."""
        rates = {
            'savings': np.random.uniform(3.0, 6.0),
            'current': 0.0,
            'fixed_deposit': np.random.uniform(6.0, 8.5),
            'loan': np.random.uniform(8.0, 15.0),
            'credit_card': np.random.uniform(18.0, 45.0)
        }
        return round(rates.get(account_type, 4.0), 2)
    
    def _generate_transaction_amount(self, account_info: dict) -> float:
        """Generate realistic transaction amounts based on account and customer profile."""
        # Get customer segment from account info to determine amount range
        segment = 'retail'  # Default
        min_amount, max_amount = self.TRANSACTION_AMOUNT_RANGES[segment]
        
        # Adjust based on account type
        if account_info['account_type'] == 'loan':
            return np.random.uniform(1000, 50000)  # Loan payments
        elif account_info['account_type'] == 'credit_card':
            return np.random.uniform(500, 25000)  # Credit card transactions
        else:
            return np.random.uniform(min_amount, max_amount)
    
    def _generate_transaction_description(self) -> str:
        """Generate realistic transaction descriptions."""
        descriptions = [
            "ATM Withdrawal", "Online Transfer", "Salary Credit", "Bill Payment",
            "Merchant Payment", "Interest Credit", "Service Charges", "Cash Deposit",
            "Cheque Clearance", "Mobile Payment", "UPI Transfer", "NEFT Transfer",
            "RTGS Transfer", "Standing Instruction", "Dividend Credit"
        ]
        return random.choice(descriptions)
    
    def _get_merchant_category(self) -> str:
        """Get merchant category codes."""
        categories = [
            "Grocery", "Fuel", "Restaurants", "Shopping", "Healthcare",
            "Education", "Entertainment", "Travel", "Utilities", "Insurance",
            "Investment", "Loan", "Other"
        ]
        return random.choice(categories)
    
    def _calculate_transaction_fees(self, txn_type: str, amount: float, channel: str) -> float:
        """Calculate realistic transaction fees."""
        base_fees = {
            'atm': 20, 'branch': 0, 'online': 5, 'mobile': 0, 'pos': 0
        }
        
        fee = base_fees.get(channel, 0)
        
        # Additional fees for high-value transactions
        if amount > 200000:
            fee += amount * 0.001  # 0.1% fee for high-value transactions
            
        return round(fee, 2)

def main():
    """
    Main function to generate synthetic financial data with command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Generate synthetic financial transaction data for liquidity management simulations"
    )
    parser.add_argument(
        '--customers', type=int, default=1000,
        help='Number of customers to generate (default: 1000)'
    )
    parser.add_argument(
        '--transactions', type=int, default=10000,
        help='Number of transactions to generate (default: 10000)'
    )
    parser.add_argument(
        '--output-dir', type=str, default='sample_data',
        help='Output directory for generated data (default: sample_data)'
    )
    parser.add_argument(
        '--seed', type=int, default=42,
        help='Random seed for reproducible data generation (default: 42)'
    )
    parser.add_argument(
        '--locale', type=str, default='en_IN',
        help='Faker locale for data generation (default: en_IN)'
    )
    parser.add_argument(
        '--accounts-per-customer', type=int, default=2,
        help='Average number of accounts per customer (default: 2)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Initialize data generator
        generator = FinancialDataGenerator(locale=args.locale, seed=args.seed)
        
        # Generate data
        logger.info("Starting synthetic financial data generation...")
        
        # Generate customers
        customers_df = generator.generate_customers(args.customers)
        customers_file = os.path.join(args.output_dir, 'customers.csv')
        customers_df.to_csv(customers_file, index=False)
        logger.info(f"Customer data saved to {customers_file}")
        
        # Generate accounts
        accounts_df = generator.generate_accounts(customers_df, args.accounts_per_customer)
        accounts_file = os.path.join(args.output_dir, 'accounts.csv')
        accounts_df.to_csv(accounts_file, index=False)
        logger.info(f"Account data saved to {accounts_file}")
        
        # Generate transactions
        transactions_df = generator.generate_transactions(accounts_df, args.transactions)
        transactions_file = os.path.join(args.output_dir, 'transactions.csv')
        transactions_df.to_csv(transactions_file, index=False)
        logger.info(f"Transaction data saved to {transactions_file}")
        
        # Generate liquidity metrics
        liquidity_df = generator.generate_liquidity_metrics(accounts_df, transactions_df)
        liquidity_file = os.path.join(args.output_dir, 'liquidity_metrics.csv')
        liquidity_df.to_csv(liquidity_file, index=False)
        logger.info(f"Liquidity metrics saved to {liquidity_file}")
        
        # Generate summary statistics
        summary = {
            'generation_timestamp': datetime.now().isoformat(),
            'parameters': vars(args),
            'summary_statistics': {
                'total_customers': len(customers_df),
                'total_accounts': len(accounts_df),
                'total_transactions': len(transactions_df),
                'total_transaction_value': float(transactions_df['amount'].sum()),
                'average_account_balance': float(accounts_df['current_balance'].mean()),
                'data_quality_score': 95.5  # Placeholder for data quality metrics
            }
        }
        
        summary_file = os.path.join(args.output_dir, 'generation_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info("="*60)
        logger.info("SYNTHETIC DATA GENERATION COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        logger.info(f"Generated {len(customers_df)} customers")
        logger.info(f"Generated {len(accounts_df)} accounts")
        logger.info(f"Generated {len(transactions_df)} transactions")
        logger.info(f"Total transaction value: ₹{transactions_df['amount'].sum():,.2f}")
        logger.info(f"Data saved to: {args.output_dir}")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Error in data generation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# This code is designed to be run as a script, generating synthetic financial data for simulations.
# It can be customized via command-line arguments for flexibility in data generation.