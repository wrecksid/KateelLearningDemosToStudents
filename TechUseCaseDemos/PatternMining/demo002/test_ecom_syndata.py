"""
Simple smoke test for ecom_syndata.py
Run it manually: python test_ecom_syndata.py
"""
from ecom_syndata import EcommerceSyntheticGenerator


def run_smoke():
    gen = EcommerceSyntheticGenerator(orders=5, seed=123, fraud_rate=0.0)
    df = gen.generate()
    assert not df.empty, "Generated DataFrame is empty"
    expected = {'CustomerID', 'Age', 'Gender', 'Income', 'TransactionAmount', 'TransactionDate',
                'MerchantCategory', 'TransactionType', 'CardType', 'FraudFlag', 'RewardPoints'}
    assert expected.issubset(set(df.columns)), f"Missing columns: {expected - set(df.columns)}"
    print('Smoke test passed: generated', len(df), 'rows')


if __name__ == '__main__':
    run_smoke()
