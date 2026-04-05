"""
syntdata.py

Synthetic Data Generator for AI/ML Finance Demos
Author: Vinaya Sathyanarayana

This program generates synthetic credit card transaction data with various features to demonstrate
outlier detection algorithms in a finance context.

Features:
- Transaction ID, datetime, cardholder name, card number
- Merchant name, category, transaction amount, currency, location
- Fraud flag to introduce outlier transactions

Usage:
  python syntdata.py [-n NUM_ROWS] [-q]

  -n, --num_rows   Number of rows to generate (default 10000)
  -q, --quiet      Quiet mode - minimal console output (default verbose)

Output:
  syntheticdata.csv in current directory
"""

import csv
import argparse
import random
import logging
from faker import Faker


class SyntheticDataGenerator:
    def __init__(self, locale='en_IN', num_records=10000, verbose=True):
        try:
            self.faker = Faker(locale)
            self.num_records = num_records
            self.verbose = verbose
            self.filename = 'syntheticdata.csv'
            self.currency = 'INR'
        except Exception as e:
            logging.error(f"Error initializing the synthetic data generator: {str(e)}")
            raise

    def generate_transaction_amount(self):
        try:
            # Typical transactions between 10 and 50000 INR
            base_amount = self.faker.pyfloat(
                left_digits=6,  # adjusted to fit max_value digits
                right_digits=2,
                positive=True,
                min_value=10,
                max_value=50000
            )
            # Add rare large spikes as outliers
            if random.random() < 0.01:
                outlier_amount = self.faker.pyfloat(
                    left_digits=7,  # adjusted for up to 1,000,000
                    right_digits=2,
                    positive=True,
                    min_value=100000,
                    max_value=1000000
                )
                if self.verbose:
                    logging.info(f"Generated outlier transaction amount: {outlier_amount}")
                return round(outlier_amount, 2)
            return round(base_amount, 2)
        except Exception as e:
            logging.error(f"Error generating transaction amount: {str(e)}")
            return None

    def generate_date(self):
        try:
            return self.faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logging.error(f"Error generating transaction date: {str(e)}")
            return None

    def generate_category(self):
        try:
            categories = [
                'Groceries', 'Electronics', 'Utilities', 'Clothing', 'Restaurants',
                'Travel', 'Fuel', 'Healthcare', 'Entertainment', 'Miscellaneous'
            ]
            # Rare outlier category
            if random.random() < 0.01:
                return 'Luxury'
            return random.choice(categories)
        except Exception as e:
            logging.error(f"Error generating transaction category: {str(e)}")
            return 'Miscellaneous'

    def generate_location(self):
        try:
            return self.faker.city()
        except Exception as e:
            logging.error(f"Error generating location: {str(e)}")
            return 'Unknown'

    def generate_merchant(self):
        try:
            merchants = [
                'Amazon', 'Flipkart', 'Reliance', 'Big Bazaar', 'Myntra',
                'Swiggy', 'Zomato', 'Ola', 'Uber', 'BookMyShow',
                'Healthify', 'PVR', 'Dominos', 'Cafe Coffee Day', 'Local Store'
            ]
            return random.choice(merchants)
        except Exception as e:
            logging.error(f"Error generating merchant: {str(e)}")
            return 'Unknown'

    def generate_record(self):
        try:
            record = {
                'transaction_id': self.faker.uuid4(),
                'transaction_datetime': self.generate_date(),
                'card_holder_name': self.faker.name(),
                'card_number': self.faker.credit_card_number(card_type=None),
                'merchant_name': self.generate_merchant(),
                'merchant_category': self.generate_category(),
                'transaction_amount': self.generate_transaction_amount(),
                'transaction_currency': self.currency,
                'transaction_location': self.generate_location(),
                'is_fraud': 0
            }
            # Insert some fraud/outlier transactions (1%)
            if random.random() < 0.01:
                record['is_fraud'] = 1
                record['transaction_amount'] = round(record['transaction_amount'] * random.uniform(5, 10), 2)
                record['merchant_category'] = 'Fraudulent'
            return record
        except Exception as e:
            logging.error(f"Error generating record: {str(e)}")
            return None

    def generate_dataset(self):
        try:
            data = []
            for i in range(self.num_records):
                if self.verbose and i > 0 and i % 1000 == 0:
                    logging.info(f"Generated {i} records so far...")
                record = self.generate_record()
                if record:
                    data.append(record)
            if self.verbose:
                logging.info(f"Finished generating {len(data)} records.")
            return data
        except Exception as e:
            logging.error(f"Error generating dataset: {str(e)}")
            return []

    def save_to_csv(self, data):
        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            if self.verbose:
                logging.info(f"Saved synthetic dataset to {self.filename}")
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='Synthetic Data Generator for AI/ML Finance Demos by Vinaya Sathyanarayana')
    parser.add_argument('-n', '--num_rows', type=int, default=10000, help='Number of rows to generate (default=10000)')
    parser.add_argument('-q', '--quiet', action='store_true', help='Run in quiet mode with minimal on-screen output')

    args = parser.parse_args()

    verbose_mode = not args.quiet

    if verbose_mode:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.ERROR)

    try:
        generator = SyntheticDataGenerator(num_records=args.num_rows, verbose=verbose_mode)
        dataset = generator.generate_dataset()
        if dataset:
            generator.save_to_csv(dataset)
        else:
            if verbose_mode:
                logging.warning("No data was generated.")
    except Exception as e:
        logging.error(f"Fatal error in generating synthetic data: {str(e)}")


if __name__ == '__main__':
    main()
