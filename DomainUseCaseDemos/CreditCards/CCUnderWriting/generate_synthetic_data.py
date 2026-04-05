"""
Synthetic Credit Card Application Data Generator
===============================================

This program generates synthetic credit card application data for educational purposes.
The data mimics real-world credit card applications with various customer attributes
and approval decisions based on realistic business logic.

Author: AI Assistant for Finance Course
Date: July 2025
"""

from faker import Faker
import pandas as pd
import numpy as np
import random
import argparse
import logging
from datetime import datetime, timedelta
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SyntheticCreditCardDataGenerator:
    """
    Generates synthetic credit card application data with configurable parameters.
    
    This class creates realistic credit card application datasets that can be used
    for machine learning demonstrations, particularly for credit underwriting models.
    """
    
    def __init__(self, 
                 size=10000,
                 locale='en_IN',
                 age_range=(21, 65),
                 income_range=(200000, 5000000),
                 approval_rate=0.7,
                 seed=42):
        """
        Initialize the data generator with configurable parameters.
        
        Parameters:
        -----------
        size : int
            Number of records to generate (default: 10000)
        locale : str
            Faker locale for generating names and addresses (default: 'en_IN')
        age_range : tuple
            Min and max age range (default: (21, 65))
        income_range : tuple
            Min and max annual income in INR (default: (200000, 5000000))
        approval_rate : float
            Target approval rate (0.0 to 1.0, default: 0.7)
        seed : int
            Random seed for reproducibility (default: 42)
        """
        try:
            self.size = size
            self.locale = locale
            self.age_range = age_range
            self.income_range = income_range
            self.approval_rate = approval_rate
            self.seed = seed
            
            # Initialize Faker and set seeds for reproducibility
            self.fake = Faker(locale)
            Faker.seed(seed)
            np.random.seed(seed)
            random.seed(seed)
            
            logger.info(f"Initialized generator for {size} records with locale {locale}")
            
        except Exception as e:
            logger.error(f"Error initializing generator: {e}")
            raise
    
    def _generate_customer_demographics(self):
        """Generate basic customer demographic information."""
        try:
            customer_ids = [f"CUST{i:08d}" for i in range(1, self.size + 1)]
            names = [self.fake.name() for _ in range(self.size)]
            ages = np.random.randint(self.age_range[0], self.age_range[1] + 1, self.size)
            genders = np.random.choice(['M', 'F'], self.size, p=[0.52, 0.48])
            
            return customer_ids, names, ages, genders
            
        except Exception as e:
            logger.error(f"Error generating demographics: {e}")
            raise
    
    def _generate_financial_data(self):
        """Generate financial information for customers."""
        try:
            # Annual income with log-normal distribution (more realistic)
            mu = np.log(800000)  # Median income around 8 lakhs
            sigma = 0.8
            incomes = np.random.lognormal(mu, sigma, self.size)
            incomes = np.clip(incomes, self.income_range[0], self.income_range[1])
            incomes = incomes.astype(int)
            
            # Employment status
            employment_statuses = np.random.choice(
                ['Salaried', 'Self-Employed', 'Business', 'Professional', 'Retired'],
                self.size,
                p=[0.6, 0.2, 0.1, 0.08, 0.02]
            )
            
            # Credit score (300-850 range, normal distribution)
            credit_scores = np.random.normal(680, 80, self.size)
            credit_scores = np.clip(credit_scores, 300, 850).astype(int)
            
            # Existing debt (correlated with income)
            debt_ratio = np.random.beta(2, 5, self.size)  # Most people have lower debt ratios
            existing_debts = (incomes * debt_ratio * np.random.uniform(0.1, 0.8, self.size)).astype(int)
            
            # Number of existing credit cards
            num_cards = np.random.poisson(1.5, self.size)
            num_cards = np.clip(num_cards, 0, 8)
            
            # Monthly salary (for salaried employees)
            monthly_salaries = (incomes / 12).astype(int)
            
            return incomes, employment_statuses, credit_scores, existing_debts, num_cards, monthly_salaries
            
        except Exception as e:
            logger.error(f"Error generating financial data: {e}")
            raise
    
    def _generate_application_data(self):
        """Generate credit card application specific data."""
        try:
            # Requested credit limit (typically 2-5x monthly income)
            monthly_incomes = np.array([inc/12 for inc in self._temp_incomes])
            multipliers = np.random.uniform(2, 8, self.size)
            requested_limits = (monthly_incomes * multipliers).astype(int)
            requested_limits = np.clip(requested_limits, 15000, 500000)
            
            # Application dates (last 2 years)
            start_date = datetime.now() - timedelta(days=730)
            end_date = datetime.now()
            application_dates = [
                self.fake.date_between(start_date=start_date, end_date=end_date)
                for _ in range(self.size)
            ]
            
            # Card type preference
            card_types = np.random.choice(
                ['Standard', 'Gold', 'Platinum', 'Premium'],
                self.size,
                p=[0.4, 0.3, 0.2, 0.1]
            )
            
            return requested_limits, application_dates, card_types
            
        except Exception as e:
            logger.error(f"Error generating application data: {e}")
            raise
    
    def _determine_approval_and_limit(self, credit_scores, incomes, existing_debts, requested_limits, ages, employment_statuses):
        """
        Determine approval status and credit limit based on underwriting rules.
        
        This method implements realistic credit underwriting logic:
        - Credit score is the primary factor
        - Income-to-debt ratio is considered
        - Age and employment status influence decisions
        - Requested limit vs. income ratio matters
        """
        try:
            approved_status = []
            approved_limits = []
            
            for i in range(self.size):
                score = credit_scores[i]
                income = incomes[i]
                debt = existing_debts[i]
                requested = requested_limits[i]
                age = ages[i]
                employment = employment_statuses[i]
                
                # Calculate debt-to-income ratio
                dti_ratio = debt / income if income > 0 else 1
                
                # Calculate approval probability based on multiple factors
                prob_approve = 0.0
                
                # Credit score factor (40% weight)
                if score >= 750:
                    prob_approve += 0.4
                elif score >= 700:
                    prob_approve += 0.32
                elif score >= 650:
                    prob_approve += 0.24
                elif score >= 600:
                    prob_approve += 0.16
                elif score >= 550:
                    prob_approve += 0.08
                
                # Income factor (25% weight)
                if income >= 1000000:
                    prob_approve += 0.25
                elif income >= 600000:
                    prob_approve += 0.20
                elif income >= 400000:
                    prob_approve += 0.15
                elif income >= 250000:
                    prob_approve += 0.10
                
                # Debt-to-income factor (20% weight)
                if dti_ratio <= 0.3:
                    prob_approve += 0.20
                elif dti_ratio <= 0.5:
                    prob_approve += 0.15
                elif dti_ratio <= 0.7:
                    prob_approve += 0.10
                
                # Employment factor (10% weight)
                if employment in ['Salaried', 'Professional']:
                    prob_approve += 0.10
                elif employment == 'Self-Employed':
                    prob_approve += 0.08
                elif employment == 'Business':
                    prob_approve += 0.06
                
                # Age factor (5% weight)
                if 25 <= age <= 55:
                    prob_approve += 0.05
                elif age > 55:
                    prob_approve += 0.03
                
                # Make approval decision
                if random.random() < prob_approve:
                    approved_status.append('Yes')
                    
                    # Determine approved limit (usually 70-100% of requested)
                    if score >= 750:
                        limit_ratio = random.uniform(0.85, 1.0)
                    elif score >= 700:
                        limit_ratio = random.uniform(0.75, 0.95)
                    elif score >= 650:
                        limit_ratio = random.uniform(0.65, 0.85)
                    else:
                        limit_ratio = random.uniform(0.50, 0.75)
                    
                    approved_limit = int(requested * limit_ratio)
                    
                    # Cap the limit based on income (max 3x monthly income)
                    max_limit = int(income / 12 * 3)
                    approved_limit = min(approved_limit, max_limit)
                    
                    approved_limits.append(approved_limit)
                else:
                    approved_status.append('No')
                    approved_limits.append(0)
            
            return approved_status, approved_limits
            
        except Exception as e:
            logger.error(f"Error determining approval status: {e}")
            raise
    
    def generate_dataset(self, output_file='syntheticdata.csv'):
        """
        Generate the complete synthetic dataset and save to CSV.
        
        Parameters:
        -----------
        output_file : str
            Output CSV filename (default: 'syntheticdata.csv')
            
        Returns:
        --------
        pandas.DataFrame
            Generated dataset
        """
        try:
            logger.info("Starting dataset generation...")
            
            # Generate all data components
            customer_ids, names, ages, genders = self._generate_customer_demographics()
            incomes, employment_statuses, credit_scores, existing_debts, num_cards, monthly_salaries = self._generate_financial_data()
            
            # Store incomes temporarily for application data generation
            self._temp_incomes = incomes
            requested_limits, application_dates, card_types = self._generate_application_data()
            
            # Determine approval and limits
            approved_status, approved_limits = self._determine_approval_and_limit(
                credit_scores, incomes, existing_debts, requested_limits, ages, employment_statuses
            )
            
            # Create DataFrame
            data = {
                'CustomerID': customer_ids,
                'Name': names,
                'Age': ages,
                'Gender': genders,
                'AnnualIncome': incomes,
                'MonthlySalary': monthly_salaries,
                'EmploymentStatus': employment_statuses,
                'CreditScore': credit_scores,
                'ExistingDebt': existing_debts,
                'NumCreditCards': num_cards,
                'RequestedCreditLimit': requested_limits,
                'CardType': card_types,
                'ApplicationDate': application_dates,
                'Approved': approved_status,
                'ApprovedCreditLimit': approved_limits
            }
            
            df = pd.DataFrame(data)
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            
            # Print summary statistics
            approval_rate = (df['Approved'] == 'Yes').mean()
            avg_approved_limit = df[df['Approved'] == 'Yes']['ApprovedCreditLimit'].mean()
            
            logger.info(f"Dataset generated successfully!")
            logger.info(f"Total records: {len(df)}")
            logger.info(f"Approval rate: {approval_rate:.2%}")
            logger.info(f"Average approved limit: ₹{avg_approved_limit:,.0f}")
            logger.info(f"Data saved to: {output_file}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating dataset: {e}")
            raise


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Generate synthetic credit card application data')
    parser.add_argument('--size', type=int, default=10000, help='Number of records to generate')
    parser.add_argument('--output', type=str, default='syntheticdata.csv', help='Output CSV filename')
    parser.add_argument('--locale', type=str, default='en_IN', help='Faker locale')
    parser.add_argument('--min-age', type=int, default=21, help='Minimum age')
    parser.add_argument('--max-age', type=int, default=65, help='Maximum age')
    parser.add_argument('--min-income', type=int, default=200000, help='Minimum annual income')
    parser.add_argument('--max-income', type=int, default=5000000, help='Maximum annual income')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    try:
        generator = SyntheticCreditCardDataGenerator(
            size=args.size,
            locale=args.locale,
            age_range=(args.min_age, args.max_age),
            income_range=(args.min_income, args.max_income),
            seed=args.seed
        )
        
        df = generator.generate_dataset(args.output)
        print(f"\nFirst 5 rows of generated data:")
        print(df.head())
        
    except Exception as e:
        logger.error(f"Failed to generate data: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
