# synthetic_data_generator.py
"""
Synthetic Data Generator for Bank Queue Management Demo
Author: Financial Analytics Course Team
Locale: English (India) - en_IN

Usage:
- Run directly or import the generate_synthetic_data function.
- Customize size and parameters for synthetic dataset.
- Output CSV: 'syntheticdata.csv'

Generated fields:
- customer_id: Unique ID
- name: Full name
- age: Customer age (18-85)
- gender: Male/Female/Other with tunable distribution
- city: Indian city
- transaction_type: Transaction purpose (e.g., Deposit, Withdrawal, Loan Inquiry)
- transaction_amount: Amount involved in transaction
- arrival_time: Timestamp in banking hours during workday
- service_start_time: Timestamp when service started (simulating queue delay)
- service_duration_sec: Duration of transaction processing in seconds

Notes:
- Arrival and service times are generated with realistic patterns for queuing modeling.
- Tunable parameters control demographics and transaction characteristics.
- Error handling included.
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import argparse
import sys

def generate_synthetic_data(
        num_records=10000,
        output_file='syntheticdata.csv',
        locale='en_IN',
        gender_dist=None,
        transaction_types=None,
        work_start_hour=9,
        work_end_hour=17,
        avg_service_time_sec=300,  # 5 minutes avg service time
        service_time_std_dev=120   # Std dev in seconds
    ):
    """
    Generate synthetic bank queue dataset.

    Parameters:
        num_records (int): Number of rows to generate.
        output_file (str): CSV output filename.
        locale (str): Faker locale.
        gender_dist (dict): Distribution of genders, e.g., {'Male':0.5, 'Female':0.48, 'Other':0.02}
        transaction_types (dict): Transaction types and probabilities.
        work_start_hour (int): Bank opening hour (24h format).
        work_end_hour (int): Bank closing hour.
        avg_service_time_sec (int): Average duration of service.
        service_time_std_dev (int): Std deviation of service time.

    Returns:
        None (writes CSV file)
    """
    try:
        fake = Faker(locale)
        Faker.seed(42)
        random.seed(42)

        if gender_dist is None:
            gender_dist = {'Male': 0.49, 'Female': 0.49, 'Other': 0.02}
        if transaction_types is None:
            transaction_types = {
                'Cash Deposit': 0.3,
                'Cash Withdrawal': 0.3,
                'Loan Inquiry': 0.1,
                'Account Opening': 0.1,
                'Cheque Deposit': 0.1,
                'Others': 0.1
            }

        gender_choices = list(gender_dist.keys())
        gender_probs = list(gender_dist.values())
        transaction_type_choices = list(transaction_types.keys())
        transaction_type_probs = list(transaction_types.values())

        # Create header
        header = [
            'customer_id', 'name', 'age', 'gender', 'city',
            'transaction_type', 'transaction_amount',
            'arrival_time', 'service_start_time', 'service_duration_sec'
        ]

        # Bank day reference date
        base_date = datetime.now().date()
        
        # Collect data
        data = []
        last_service_end = None

        for i in range(num_records):
            customer_id = i + 1

            name = fake.name()
            age = random.randint(18, 85)
            gender = random.choices(gender_choices, gender_probs)[0]
            city = fake.city()

            transaction_type = random.choices(transaction_type_choices, transaction_type_probs)[0]
            # Transaction amount logic: vary by type
            if transaction_type in ['Cash Deposit', 'Cash Withdrawal', 'Cheque Deposit']:
                transaction_amount = round(random.uniform(100, 50000), 2)
            elif transaction_type == 'Loan Inquiry':
                transaction_amount = 0.0  # No immediate transaction amount
            elif transaction_type == 'Account Opening':
                transaction_amount = round(random.uniform(1000, 10000), 2)
            else:
                transaction_amount = round(random.uniform(100, 20000), 2)

            # Generate arrival time randomly within bank hours
            arrival_hour = random.randint(work_start_hour, work_end_hour - 1)
            arrival_minute = random.randint(0, 59)
            arrival_second = random.randint(0, 59)
            arrival_time = datetime.combine(
                base_date,
                datetime.min.time()
            ) + timedelta(hours=arrival_hour, minutes=arrival_minute, seconds=arrival_second)

            # Calculate service start time ensuring queue effect
            if last_service_end is None or arrival_time > last_service_end:
                service_start_time = arrival_time
            else:
                service_start_time = last_service_end

            # Service duration sampled from normal dist, clipped at 1 min minimum
            service_duration_sec = max(60, int(random.gauss(avg_service_time_sec, service_time_std_dev)))

            # Update last_service_end time
            last_service_end = service_start_time + timedelta(seconds=service_duration_sec)

            data.append([
                customer_id,
                name,
                age,
                gender,
                city,
                transaction_type,
                transaction_amount,
                arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                service_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                service_duration_sec
            ])

        # Write to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

        print(f"Generated {num_records} records and saved to '{output_file}'")

    except Exception as e:
        print(f"Error generating synthetic data: {e}", file=sys.stderr)
        raise

# Command line interface to allow running standalone
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synthetic Data Generator for Bank Queue Management")
    parser.add_argument('--num_records', type=int, default=10000, help="Number of synthetic records to generate (default 10000)")
    parser.add_argument('--output_file', type=str, default='syntheticdata.csv', help="Output CSV filename (default 'syntheticdata.csv')")
    args = parser.parse_args()

    generate_synthetic_data(num_records=args.num_records, output_file=args.output_file)
