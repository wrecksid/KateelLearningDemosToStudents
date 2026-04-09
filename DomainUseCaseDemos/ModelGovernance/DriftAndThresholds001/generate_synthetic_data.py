from pathlib import Path

import numpy as np
import pandas as pd


def make_dataset(rows: int, shift: bool = False, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    income = rng.normal(700000 if not shift else 620000, 120000, rows)
    credit_score = rng.normal(735 if not shift else 690, 45, rows)
    dti = rng.normal(0.32 if not shift else 0.41, 0.08, rows)
    delinquency = rng.poisson(0.4 if not shift else 0.8, rows)
    stable_income = rng.binomial(1, 0.82 if not shift else 0.72, rows)

    approval_logit = (
        (credit_score - 680) / 35
        + (income - 600000) / 175000
        - 4.5 * dti
        - 0.7 * delinquency
        + 0.8 * stable_income
    )
    approval_prob = 1 / (1 + np.exp(-approval_logit))
    approved = rng.binomial(1, approval_prob)

    return pd.DataFrame(
        {
            "income": income.round(0),
            "credit_score": credit_score.round(0),
            "debt_to_income": np.clip(dti, 0.05, 0.9).round(3),
            "delinquency_count": delinquency,
            "stable_income_flag": stable_income,
            "approved": approved,
        }
    )


def main():
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    make_dataset(1200, shift=False, seed=42).to_csv(out_dir / "train.csv", index=False)
    make_dataset(600, shift=False, seed=43).to_csv(out_dir / "baseline.csv", index=False)
    make_dataset(600, shift=True, seed=44).to_csv(out_dir / "monitoring.csv", index=False)
    print(f"Wrote monitoring datasets to {out_dir.resolve()}")


if __name__ == "__main__":
    main()
