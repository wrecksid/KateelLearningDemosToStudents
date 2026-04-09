from pathlib import Path

import numpy as np
import pandas as pd


def make_data(rows: int = 1500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    gender = rng.choice(["Female", "Male"], size=rows, p=[0.42, 0.58])
    region = rng.choice(["Metro", "Urban", "SemiUrban"], size=rows, p=[0.35, 0.4, 0.25])
    income = rng.normal(720000, 160000, size=rows)
    credit_score = rng.normal(715, 55, size=rows)
    debt_to_income = np.clip(rng.normal(0.36, 0.09, size=rows), 0.05, 0.9)
    delinquencies = rng.poisson(0.55, size=rows)
    job_stability = np.clip(rng.normal(72, 12, size=rows), 20, 100)

    # Small subgroup shifts to make fairness analysis educational.
    score_adjust = np.where(gender == "Female", 8, -3) + np.where(region == "Metro", 5, 0)
    effective_score = credit_score + score_adjust

    logit = (
        (effective_score - 690) / 38
        + (income - 600000) / 180000
        - 4.0 * debt_to_income
        - 0.8 * delinquencies
        + (job_stability - 65) / 20
    )
    approval_prob = 1 / (1 + np.exp(-logit))
    approved = rng.binomial(1, approval_prob)

    return pd.DataFrame(
        {
            "income": income.round(0),
            "credit_score": credit_score.round(0),
            "debt_to_income": debt_to_income.round(3),
            "delinquencies": delinquencies,
            "job_stability": job_stability.round(1),
            "gender": gender,
            "region": region,
            "approved": approved,
        }
    )


def main() -> None:
    df = make_data()
    out = Path("synthetic_credit_fairness.csv")
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} rows to {out}")


if __name__ == "__main__":
    main()
