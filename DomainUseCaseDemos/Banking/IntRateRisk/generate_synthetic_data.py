# generate_synthetic_data.py
import csv
import sys
from faker import Faker
import random
import datetime
from typing import Optional

class SyntheticDataGenerator:
    def __init__(self, num_rows: int = 10000, locale: str = 'en_IN', seed: Optional[int] = None):
        """
        Initialize the data generator.
        :param num_rows: Number of rows to generate (default 10,000)
        :param locale: Faker locale string (default 'en_IN')
        :param seed: Optional seed for reproducibility
        """
        self.num_rows = num_rows
        self.locale = locale
        self.fake = Faker(locale)
        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)

    def _random_account_type(self):
        return random.choice(['Savings', 'Current', 'Fixed Deposit', 'Recurring Deposit'])

    def _random_interest_rate(self, account_type: str) -> float:
        """
        Returns interest rate based on account type, approximating Indian banking rates.
        """
        if account_type == 'Savings':
            return round(random.uniform(3.0, 4.0), 2)
        elif account_type == 'Current':
            return round(random.uniform(0.1, 0.5), 2)
        elif account_type == 'Fixed Deposit':
            return round(random.uniform(5.5, 7.0), 2)
        elif account_type == 'Recurring Deposit':
            return round(random.uniform(5.0, 6.5), 2)
        else:
            return round(random.uniform(3.0, 7.0), 2)

    def _random_balance(self, account_type: str) -> float:
        """
        Generates realistic account balance based on account type.
        """
        if account_type == 'Savings':
            return round(random.uniform(1000, 5_00_000), 2)
        elif account_type == 'Current':
            return round(random.uniform(10_000, 1_00_00_000), 2)
        elif account_type == 'Fixed Deposit':
            return round(random.uniform(50_000, 5_00_00_000), 2)
        elif account_type == 'Recurring Deposit':
            return round(random.uniform(500, 10_00_000), 2)
        else:
            return round(random.uniform(1000, 5_00_000), 2)

    def _random_date_within_years(self, years_back: int = 5):
        """
        Generate a random past date within given years from today.
        """
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=365 * years_back)
        return self.fake.date_between(start_date=start_date, end_date=end_date)

    def generate(self, output_file: str = 'syntheticdata.csv'):
        """
        Generates synthetic dataset and writes to the CSV file.
        """
        try:
            with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'CustomerID', 'Name', 'Gender', 'Age', 'Email', 'PhoneNumber',
                    'Address', 'AccountNumber', 'AccountType', 'AccountOpenDate',
                    'Balance', 'InterestRate', 'LastTransactionDate'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for i in range(1, self.num_rows + 1):
                    name = self.fake.name()
                    gender = random.choice(['Male', 'Female', 'Other'])
                    birthdate = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
                    age = (datetime.date.today() - birthdate).days // 365
                    email = self.fake.email()
                    phone = self.fake.phone_number()
                    address = self.fake.address().replace("\n", ", ")
                    account_type = self._random_account_type()
                    account_open_date = self._random_date_within_years(years_back=15)
                    balance = self._random_balance(account_type)
                    interest_rate = self._random_interest_rate(account_type)
                    last_transaction_date = self._random_date_within_years(years_back=1)

                    writer.writerow({
                        'CustomerID': i,
                        'Name': name,
                        'Gender': gender,
                        'Age': age,
                        'Email': email,
                        'PhoneNumber': phone,
                        'Address': address,
                        'AccountNumber': f"{random.randint(10**9, 10**10 - 1)}",
                        'AccountType': account_type,
                        'AccountOpenDate': account_open_date,
                        'Balance': balance,
                        'InterestRate': interest_rate,
                        'LastTransactionDate': last_transaction_date
                    })
            print(f"Successfully generated {self.num_rows} rows to {output_file}")
        except Exception as e:
            print(f"Error generating synthetic data: {e}", file=sys.stderr)
            raise

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate synthetic finance data as CSV.')
    parser.add_argument('-n', '--num_rows', type=int, default=10000, help='Number of rows to generate')
    parser.add_argument('-o', '--output', type=str, default='syntheticdata.csv', help='Output CSV filename')
    parser.add_argument('-s', '--seed', type=int, default=None, help='Random seed (optional)')
    args = parser.parse_args()

    generator = SyntheticDataGenerator(num_rows=args.num_rows, seed=args.seed)
    generator.generate(output_file=args.output)

if __name__ == '__main__':
    main()
