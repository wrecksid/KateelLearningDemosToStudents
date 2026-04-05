"""
ecom_syndata.py
Synthetic Ecommerce Order Data Generator (Item-level rows)
Author: GitHub Copilot (based on Vinaya Sathyanarayana work)

Generates synthetic ecommerce transactions composed of realistic product bundles.
Each order may contain multiple items; the output is an item-level CSV with the
same columns used by the demo: so the demo can run unchanged.

Output columns (CSV):
- CustomerID, Age, Gender, Income, TransactionAmount, TransactionDate,
  MerchantCategory, TransactionType, CardType, FraudFlag, RewardPoints

Usage:
python ecom_syndata.py --orders 2000 --seed 42
python ecom_syndata.py --sample

"""

import argparse
import random
from datetime import timedelta
from faker import Faker
import pandas as pd
import numpy as np


BUNDLE_TEMPLATES = {
    # primary : [(co_item, probability), ...]
    'Electronics': [('Accessories', 0.6), ('Gaming', 0.2), ('Home Office', 0.15)],
    'Clothing': [('Shoes', 0.5), ('Accessories', 0.4), ('Beauty', 0.1)],
    'Groceries': [('Household', 0.4), ('Personal Care', 0.2)],
    'Books': [('Stationery', 0.3), ('Electronics', 0.05)],
    'Home Decor': [('Furniture', 0.25), ('Bedding', 0.15)],
    'Sports': [('Fitness', 0.4), ('Accessories', 0.3)],
    'Toys': [('Baby', 0.2), ('Games', 0.3)],
    'Pet Supplies': [('Pet Food', 0.6)],
    'Beauty': [('Health', 0.25), ('Clothing', 0.1)],
    'Gaming': [('Electronics', 0.5), ('Accessories', 0.4)],
}

# Typical price ranges by category (min, max)
PRICE_RANGES = {
    'Electronics': (1500, 120000),
    'Accessories': (100, 5000),
    'Clothing': (300, 6000),
    'Shoes': (500, 15000),
    'Groceries': (20, 2000),
    'Household': (50, 5000),
    'Personal Care': (50, 3000),
    'Books': (100, 2000),
    'Stationery': (20, 500),
    'Home Decor': (200, 40000),
    'Furniture': (2000, 200000),
    'Bedding': (500, 30000),
    'Sports': (500, 50000),
    'Fitness': (1000, 80000),
    'Toys': (100, 15000),
    'Baby': (200, 10000),
    'Games': (500, 5000),
    'Pet Supplies': (100, 5000),
    'Pet Food': (50, 3000),
    'Beauty': (100, 8000),
    'Health': (50, 10000),
    'Gaming': (800, 150000),
    'Home Office': (500, 50000),
    'Electronics Accessories': (100, 7000),
}

ALL_CATEGORIES = sorted(list(set(list(PRICE_RANGES.keys()) + list(BUNDLE_TEMPLATES.keys()))))


class EcommerceSyntheticGenerator:
    def __init__(self, orders=2000, locale='en_IN', seed=None, fraud_rate=0.01, avg_items=2.2):
        self.orders = orders
        self.locale = locale
        self.seed = seed
        self.fraud_rate = fraud_rate
        self.avg_items = avg_items
        self.fake = Faker(locale)
        if seed is not None:
            random.seed(seed)
            Faker.seed(seed)
            np.random.seed(seed)

    def _choose_bundle(self, primary_cat):
        items = [primary_cat]
        if primary_cat in BUNDLE_TEMPLATES:
            for co_cat, prob in BUNDLE_TEMPLATES[primary_cat]:
                if random.random() < prob:
                    items.append(co_cat)
        # Occasionally add random extra item
        if random.random() < 0.05:
            items.append(random.choice(ALL_CATEGORIES))
        return items

    def _price_for(self, category):
        r = PRICE_RANGES.get(category)
        if r:
            return round(random.uniform(r[0], r[1]), 2)
        # fallback
        return round(random.uniform(50, 5000), 2)

    def generate(self):
        rows = []
        # Create a pool of customers so customers repeat realistically
        unique_customers = max(250, int(self.orders * 0.4))
        customers = []
        for _ in range(unique_customers):
            cust = {
                'CustomerID': self.fake.unique.random_int(min=100000, max=999999),
                'Age': random.randint(18, 70),
                'Gender': random.choices(['Male', 'Female', 'Other'], weights=[0.49, 0.49, 0.02])[0],
                'Income': round(random.uniform(15000, 300000), 2)
            }
            customers.append(cust)

        start_date = self.fake.date_between(start_date='-2y', end_date='-1y')
        for order_idx in range(self.orders):
            cust = random.choice(customers)
            # jitter date across range
            order_date = (start_date + timedelta(days=random.randint(0, 720))).strftime('%Y-%m-%d')
            # number of items drawn from Poisson-like distribution (min 1)
            num_items = max(1, int(np.random.poisson(self.avg_items)))

            # choose primary category and build bundle
            primary = random.choices(list(BUNDLE_TEMPLATES.keys()) + ['Groceries', 'Books', 'Clothing'],
                                     weights=[3,3,2,2,2,1,1,1,1,1,5,3,3], k=1)[0]
            bundle_items = self._choose_bundle(primary)

            # ensure num_items honored; expand or trim bundle
            if len(bundle_items) < num_items:
                while len(bundle_items) < num_items:
                    bundle_items.append(random.choice(ALL_CATEGORIES))
            elif len(bundle_items) > num_items:
                bundle_items = bundle_items[:num_items]

            card_type = random.choices(['Credit', 'Debit', 'Prepaid'], weights=[0.6, 0.35, 0.05])[0]
            transaction_type = 'Purchase'
            fraud_flag = 1 if random.random() < self.fraud_rate else 0

            for cat in bundle_items:
                merchant = self.fake.company()
                amt = self._price_for(cat)
                reward_points = int(amt // 20)
                rows.append([
                    cust['CustomerID'], cust['Age'], cust['Gender'], cust['Income'],
                    amt, order_date, cat, transaction_type, card_type, fraud_flag, reward_points
                ])

        df = pd.DataFrame(rows, columns=[
            'CustomerID', 'Age', 'Gender', 'Income', 'TransactionAmount', 'TransactionDate',
            'MerchantCategory', 'TransactionType', 'CardType', 'FraudFlag', 'RewardPoints'
        ])
        # shuffle rows
        df = df.sample(frac=1, random_state=self.seed).reset_index(drop=True)
        return df

    def save(self, df, filename='syntheticdata.csv'):
        df.to_csv(filename, index=False)
        print(f"Saved ecommerce synthetic data to {filename} with {len(df)} rows ({self.orders} orders).")


def main():
    parser = argparse.ArgumentParser(description='Ecommerce synthetic order data generator')
    parser.add_argument('--orders', type=int, default=2000, help='Number of orders to generate (default: 2000)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')
    parser.add_argument('--locale', type=str, default='en_IN', help='Locale for faker (default en_IN)')
    parser.add_argument('--fraud_rate', type=float, default=0.01, help='Fraction of fraudulent orders (default 0.01)')
    parser.add_argument('--sample', action='store_true', help='Generate a small sample and print a preview')
    args = parser.parse_args()

    orders = 10 if args.sample else args.orders
    gen = EcommerceSyntheticGenerator(orders=orders, locale=args.locale, seed=args.seed, fraud_rate=args.fraud_rate)
    df = gen.generate()
    gen.save(df)

    if args.sample:
        print(df.head(20).to_string(index=False))


if __name__ == '__main__':
    main()
