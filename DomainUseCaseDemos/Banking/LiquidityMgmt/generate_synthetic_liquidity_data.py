#!/usr/bin/env python3
"""
Synthetic Liquidity Management Data Generator

This script generates realistic synthetic financial transaction data 
for liquidity management analysis using Monte Carlo simulations.

Author: Financial Analytics Course
Version: 1.0
"""

import csv
import random
import argparse
import sys
import os
from datetime import datetime, timedelta
from typing import Optional

try:
    from faker import Faker
except ImportError:
    print("Error: faker library not found. Please install requirements using: pip install -r requirements.txt")
    sys.exit(1)


class LiquidityDataGenerator:
    """
    A class to generate synthetic liquidity management data for financial analysis.
    
    This generator creates realistic transaction data including:
    - Transaction IDs, dates, types (inflow/outflow)
    - Counterparty information
    - Transaction amounts in INR
    - Business descriptions
    """
    
    def __init__(self, locale: str = 'en_IN', seed: Optional[int] = None):
        """
        Initialize the data generator.
        
        Args:
            locale (str): Locale for faker data generation
            seed (int, optional): Random seed for reproducibility
        """
        self.locale = locale
        if seed is not None:
            random.seed(seed)
            Faker.seed(seed)
        
        try:
            self.fake = Faker(locale)
        except AttributeError:
            print(f"Warning: Locale {locale} not supported, using default")
            self.fake = Faker()
    
    def generate_transaction_type(self) -> str:
        """
        Generate transaction type with realistic distribution.
        
        Returns:
            str: 'inflow' or 'outflow'
        """
        # 45% inflows, 55% outflows (realistic business scenario)
        return random.choices(['inflow', 'outflow'], weights=[45, 55])[0]
    
    def generate_amount(self, transaction_type: str, mean: float, stddev: float) -> float:
        """
        Generate transaction amount based on type and parameters.
        
        Args:
            transaction_type (str): Type of transaction
            mean (float): Mean amount
            stddev (float): Standard deviation
            
        Returns:
            float: Transaction amount
        """
        try:
            # Adjust mean based on transaction type
            if transaction_type == 'inflow':
                adjusted_mean = mean * 1.2  # Inflows tend to be larger
            else:
                adjusted_mean = mean * 0.8  # Outflows tend to be smaller
            
            # Generate amount using normal distribution
            amount = abs(random.gauss(adjusted_mean, stddev))
            
            # Set minimum amount to 1000 INR
            amount = max(amount, 1000)
            
            return round(amount, 2)
            
        except Exception as e:
            print(f"Error generating amount: {e}")
            return 10000.0  # Default fallback
    
    def generate_counterparty(self, transaction_type: str) -> str:
        """
        Generate realistic counterparty names based on transaction type.
        
        Args:
            transaction_type (str): Type of transaction
            
        Returns:
            str: Counterparty name
        """
        try:
            if transaction_type == 'inflow':
                # For inflows: customers, clients, investors
                prefixes = ['', 'M/s ', 'Shri ', 'Smt ']
                return random.choice(prefixes) + self.fake.company()
            else:
                # For outflows: suppliers, vendors, employees
                types = ['suppliers', 'vendors', 'employees']
                chosen_type = random.choice(types)
                
                if chosen_type == 'employees':
                    return self.fake.name()
                else:
                    return self.fake.company()
                    
        except Exception as e:
            print(f"Error generating counterparty: {e}")
            return "Unknown Counterparty"
    
    def generate_description(self, transaction_type: str) -> str:
        """
        Generate realistic transaction descriptions.
        
        Args:
            transaction_type (str): Type of transaction
            
        Returns:
            str: Transaction description
        """
        try:
            if transaction_type == 'inflow':
                descriptions = [
                    "Revenue from operations",
                    "Customer payment received",
                    "Investment income",
                    "Interest income",
                    "Sales proceeds",
                    "Service charges received",
                    "Commission income"
                ]
            else:
                descriptions = [
                    "Supplier payment",
                    "Salary disbursement",
                    "Utility bills payment",
                    "Rent payment",
                    "Equipment purchase",
                    "Professional fees",
                    "Marketing expenses",
                    "Office supplies",
                    "Travel expenses"
                ]
            
            return random.choice(descriptions)
            
        except Exception as e:
            print(f"Error generating description: {e}")
            return "Financial transaction"
    
    def generate_data(self, num_rows: int, amount_mean: float, amount_stddev: float, 
                     output_file: str, start_date: str = '-2y', end_date: str = 'today') -> bool:
        """
        Generate synthetic liquidity data and save to CSV.
        
        Args:
            num_rows (int): Number of rows to generate
            amount_mean (float): Mean transaction amount
            amount_stddev (float): Standard deviation for amounts
            output_file (str): Output CSV file path
            start_date (str): Start date for transactions
            end_date (str): End date for transactions
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate inputs
            if num_rows <= 0:
                raise ValueError("Number of rows must be positive")
            if amount_mean <= 0:
                raise ValueError("Amount mean must be positive")
            if amount_stddev < 0:
                raise ValueError("Amount standard deviation must be non-negative")
            
            print(f"Generating {num_rows} synthetic liquidity management records...")
            
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header
                header = [
                    'transaction_id', 'transaction_date', 'transaction_type',
                    'counterparty', 'amount_inr', 'description', 'currency',
                    'business_unit', 'account_type'
                ]
                writer.writerow(header)
                
                # Generate data rows
                for i in range(1, num_rows + 1):
                    try:
                        transaction_id = f'TXN{i:08d}'
                        transaction_date = self.fake.date_between(start_date=start_date, end_date=end_date)
                        transaction_type = self.generate_transaction_type()
                        counterparty = self.generate_counterparty(transaction_type)
                        amount = self.generate_amount(transaction_type, amount_mean, amount_stddev)
                        description = self.generate_description(transaction_type)
                        currency = 'INR'
                        business_unit = random.choice(['Corporate Banking', 'Retail Banking', 'Investment Banking', 'Treasury'])
                        account_type = random.choice(['Current Account', 'Savings Account', 'Fixed Deposit', 'Call Money'])
                        
                        writer.writerow([
                            transaction_id, transaction_date, transaction_type,
                            counterparty, amount, description, currency,
                            business_unit, account_type
                        ])
                        
                        # Progress indicator
                        if i % 1000 == 0:
                            print(f"Generated {i} records...")
                            
                    except Exception as e:
                        print(f"Error generating row {i}: {e}")
                        continue
            
            print(f"Successfully generated {num_rows} synthetic records in '{output_file}'")
            print(f"File size: {os.path.getsize(output_file)} bytes")
            return True
            
        except Exception as e:
            print(f"Error generating synthetic data: {e}")
            return False


def main():
    """Main function to handle command line execution."""
    parser = argparse.ArgumentParser(
        description='Generate synthetic liquidity management financial data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_synthetic_liquidity_data.py --rows 5000
  python generate_synthetic_liquidity_data.py --rows 10000 --mean 750000 --stddev 300000
  python generate_synthetic_liquidity_data.py --locale en_US --seed 42
        """
    )
    
    parser.add_argument('--rows', type=int, default=10000,
                       help='Number of rows to generate (default: 10000)')
    parser.add_argument('--locale', type=str, default='en_IN',
                       help='Locale for data generation (default: en_IN)')
    parser.add_argument('--mean', type=float, default=500000,
                       help='Mean transaction amount in INR (default: 500000)')
    parser.add_argument('--stddev', type=float, default=200000,
                       help='Standard deviation of transaction amounts (default: 200000)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility (default: None)')
    parser.add_argument('--output', type=str, default='synthetic_liquidity_data.csv',
                       help='Output CSV file name (default: synthetic_liquidity_data.csv)')
    
    args = parser.parse_args()
    
    try:
        # Create data generator
        generator = LiquidityDataGenerator(locale=args.locale, seed=args.seed)
        
        # Generate data
        success = generator.generate_data(
            num_rows=args.rows,
            amount_mean=args.mean,
            amount_stddev=args.stddev,
            output_file=args.output
        )
        
        if success:
            print("\n✅ Data generation completed successfully!")
        else:
            print("\n❌ Data generation failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Data generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
