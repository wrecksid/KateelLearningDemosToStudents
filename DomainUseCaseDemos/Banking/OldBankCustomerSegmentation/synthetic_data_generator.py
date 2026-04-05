"""
Synthetic Banking Customer Data Generator
========================================

This module generates realistic synthetic banking customer data for educational purposes.
Used for demonstrating customer segmentation techniques in banking.

Author: AI/ML Finance Course
Version: 1.0
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BankingDataGenerator:
    """
    A comprehensive synthetic banking data generator using realistic patterns
    and distributions commonly found in banking datasets.
    """
    
    def __init__(self, seed: int = 42):
        """
        Initialize the data generator with configurable parameters.
        
        Args:
            seed (int): Random seed for reproducible results
        """
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        self.fake = Faker()
        Faker.seed(seed)
        
        # Default parameters - can be modified by users
        self.params = {
            'age_range': (18, 80),
            'income_range': (20000, 200000),
            'account_balance_range': (100, 100000),
            'credit_score_range': (300, 850),
            'transaction_frequency_range': (1, 50),
            'products_range': (1, 8),
            'tenure_range': (1, 25),
            'income_distribution': 'lognormal',
            'balance_distribution': 'exponential',
            'geographic_concentration': 0.7  # 70% customers from major cities
        }
        
        # Product types available in the bank
        self.products = [
            'Savings Account', 'Checking Account', 'Credit Card', 
            'Personal Loan', 'Mortgage', 'Investment Account',
            'Certificate of Deposit', 'Business Account'
        ]
        
        # Major cities for geographic concentration
        self.major_cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata',
            'Hyderabad', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur'
        ]
    
    def update_parameters(self, new_params: Dict[str, Any]) -> None:
        """
        Update generation parameters.
        
        Args:
            new_params (Dict[str, Any]): Dictionary of parameters to update
        """
        try:
            self.params.update(new_params)
            logger.info(f"Parameters updated: {new_params}")
        except Exception as e:
            logger.error(f"Error updating parameters: {e}")
            raise
    
    def _generate_correlated_features(self, income: float, age: int) -> Dict[str, Any]:
        """
        Generate features that are realistically correlated with income and age.
        
        Args:
            income (float): Customer income
            age (int): Customer age
            
        Returns:
            Dict[str, Any]: Dictionary of correlated features
        """
        try:
            # Credit score correlation with income and age
            base_credit_score = 600 + (income / 1000) * 0.5 + (age - 18) * 2
            credit_score = int(np.clip(
                np.random.normal(base_credit_score, 50),
                self.params['credit_score_range'][0],
                self.params['credit_score_range'][1]
            ))
            
            # Account balance correlation with income
            balance_multiplier = np.random.exponential(0.1)
            account_balance = max(
                self.params['account_balance_range'][0],
                min(income * balance_multiplier, self.params['account_balance_range'][1])
            )
            
            # Transaction frequency based on age and income
            base_transactions = 10 + (income / 10000) + (40 - abs(age - 40)) / 10
            monthly_transactions = int(np.clip(
                np.random.poisson(base_transactions),
                self.params['transaction_frequency_range'][0],
                self.params['transaction_frequency_range'][1]
            ))
            
            # Number of products based on income and age
            base_products = 1 + (income / 50000) + (age / 20)
            num_products = int(np.clip(
                np.random.poisson(base_products),
                self.params['products_range'][0],
                self.params['products_range'][1]
            ))
            
            return {
                'credit_score': credit_score,
                'account_balance': round(account_balance, 2),
                'monthly_transactions': monthly_transactions,
                'num_products': num_products
            }
            
        except Exception as e:
            logger.error(f"Error generating correlated features: {e}")
            raise
    
    def _generate_income(self) -> float:
        """Generate income based on specified distribution."""
        try:
            min_income, max_income = self.params['income_range']
            
            if self.params['income_distribution'] == 'lognormal':
                # Log-normal distribution for realistic income distribution
                mu = np.log(50000)  # Median income
                sigma = 0.8
                income = np.random.lognormal(mu, sigma)
            else:
                # Uniform distribution fallback
                income = np.random.uniform(min_income, max_income)
            
            return np.clip(income, min_income, max_income)
            
        except Exception as e:
            logger.error(f"Error generating income: {e}")
            return 50000  # Default fallback
    
    def _generate_location(self) -> str:
        """Generate location with geographic concentration."""
        try:
            if random.random() < self.params['geographic_concentration']:
                return random.choice(self.major_cities)
            else:
                return self.fake.city()
        except Exception as e:
            logger.error(f"Error generating location: {e}")
            return "Mumbai"  # Default fallback
    
    def generate_customer_data(self, n_customers: int = 10000) -> pd.DataFrame:
        """
        Generate synthetic customer data.
        
        Args:
            n_customers (int): Number of customers to generate
            
        Returns:
            pd.DataFrame: Generated customer data
        """
        try:
            logger.info(f"Generating data for {n_customers} customers...")
            
            customers = []
            
            for i in range(n_customers):
                # Basic demographics
                age = random.randint(*self.params['age_range'])
                income = self._generate_income()
                
                # Correlated features
                correlated_features = self._generate_correlated_features(income, age)
                
                # Customer record
                customer = {
                    'customer_id': f"CUST_{i+1:06d}",
                    'name': self.fake.name(),
                    'age': age,
                    'gender': random.choice(['Male', 'Female']),
                    'location': self._generate_location(),
                    'annual_income': round(income, 2),
                    'account_balance': correlated_features['account_balance'],
                    'credit_score': correlated_features['credit_score'],
                    'monthly_transactions': correlated_features['monthly_transactions'],
                    'num_products': correlated_features['num_products'],
                    'tenure_years': random.randint(*self.params['tenure_range']),
                    'last_transaction_days': random.randint(1, 90),
                    'digital_engagement_score': random.randint(1, 10),
                    'complaint_count': np.random.poisson(0.3),  # Low complaint rate
                    'education_level': random.choice([
                        'High School', 'Bachelor', 'Master', 'PhD', 'Diploma'
                    ]),
                    'employment_type': random.choice([
                        'Salaried', 'Self-Employed', 'Business Owner', 'Retired'
                    ]),
                    'marital_status': random.choice(['Single', 'Married', 'Divorced']),
                }
                
                # Add some derived features for segmentation
                customer['avg_transaction_amount'] = round(
                    customer['account_balance'] / max(customer['monthly_transactions'], 1), 2
                )
                customer['income_to_balance_ratio'] = round(
                    customer['annual_income'] / max(customer['account_balance'], 1), 2
                )
                customer['recency_score'] = 10 - min(customer['last_transaction_days'] // 10, 9)
                customer['frequency_score'] = min(customer['monthly_transactions'] // 5, 10)
                customer['monetary_score'] = min(customer['account_balance'] // 10000, 10)
                
                customers.append(customer)
                
                # Progress indicator
                if (i + 1) % 1000 == 0:
                    logger.info(f"Generated {i + 1} customers...")
            
            df = pd.DataFrame(customers)
            logger.info(f"Successfully generated {len(df)} customer records")
            return df
            
        except Exception as e:
            logger.error(f"Error generating customer data: {e}")
            raise
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = "synthetic_bank_data.csv") -> None:
        """
        Save generated data to CSV file.
        
        Args:
            df (pd.DataFrame): Data to save
            filename (str): Output filename
        """
        try:
            output_path = Path(filename)
            df.to_csv(output_path, index=False)
            logger.info(f"Data saved to {output_path.absolute()}")
            
        except Exception as e:
            logger.error(f"Error saving data to CSV: {e}")
            raise

def main():
    """Main function to run the data generator from command line."""
    try:
        parser = argparse.ArgumentParser(
            description="Generate synthetic banking customer data"
        )
        parser.add_argument(
            '--size', type=int, default=10000,
            help='Number of customers to generate (default: 10000)'
        )
        parser.add_argument(
            '--output', type=str, default='synthetic_bank_data.csv',
            help='Output CSV filename (default: synthetic_bank_data.csv)'
        )
        parser.add_argument(
            '--seed', type=int, default=42,
            help='Random seed for reproducibility (default: 42)'
        )
        
        args = parser.parse_args()
        
        # Validate inputs
        if args.size <= 0:
            raise ValueError("Dataset size must be positive")
        
        # Generate data
        generator = BankingDataGenerator(seed=args.seed)
        data = generator.generate_customer_data(args.size)
        generator.save_to_csv(data, args.output)
        
        # Display summary statistics
        print("\n" + "="*50)
        print("DATA GENERATION SUMMARY")
        print("="*50)
        print(f"Total customers generated: {len(data)}")
        print(f"Output file: {args.output}")
        print(f"\nSample statistics:")
        print(f"Average income: ${data['annual_income'].mean():,.2f}")
        print(f"Average account balance: ${data['account_balance'].mean():,.2f}")
        print(f"Average credit score: {data['credit_score'].mean():.0f}")
        print(f"Age range: {data['age'].min()} - {data['age'].max()}")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
