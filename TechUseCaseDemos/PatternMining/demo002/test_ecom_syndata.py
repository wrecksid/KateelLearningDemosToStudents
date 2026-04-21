"""
Tests for ecom_syndata.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

def test_syndata():
    from ecom_syndata import generate
    df = generate(400)
    assert len(df) > 0, "Syndata should not be empty"
    assert "transaction_id" in df.columns
    assert "product" in df.columns
    print(f"Test passed: {len(df)} rows generated")

if __name__ == "__main__":
    test_syndata()
