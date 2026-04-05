"""
Smoke tests for ecom_fulldemo pipeline
"""
from ecom_syndata import EcommerceSyntheticGenerator
from ecom_fulldemo import preprocess, run_apriori, run_fpgrowth


def run_smoke():
    gen = EcommerceSyntheticGenerator(orders=800, seed=123, fraud_rate=0.0)
    df = gen.generate()
    basket_bool = preprocess(df)

    apriori_items, apriori_rules = run_apriori(basket_bool, minsup=0.01)
    fpg_items, fpg_rules = run_fpgrowth(basket_bool, minsup=0.01)

    assert apriori_items is not None, 'Apriori returned None'
    assert fpg_items is not None, 'FP-Growth returned None'
    print('ecom fulldemo smoke test completed successfully')


if __name__ == '__main__':
    run_smoke()
