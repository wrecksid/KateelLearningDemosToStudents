"""
Credit underwriting demo with risk scoring and approval workflow.
"""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_application_data(n=1500):
    df = {
        "applicant_id": [f"APP_{i:05d}" for i in range(n)],
        "age": np.random.randint(20, 70, n),
        "income_k": np.random.lognormal(10.0, 0.9, n).round(2),
        "employment_years": np.random.exponential(5, n).round(1),
        "credit_score": np.random.normal(680, 70, n).clip(300, 850).astype(int),
        "dti_ratio": np.random.beta(2, 5, n).round(3),
        "loan_amount": np.random.gamma(shape=3, scale=5000, size=n).round(2),
        "existing_debt": np.random.gamma(shape=2, scale=3000, size=n).round(2),
    }
    return pd.DataFrame(df)


def risk_score(row):
    score = 500
    if row["credit_score"] > 720:
        score += 100
    elif row["credit_score"] < 620:
        score -= 80
    score -= int(row["dti_ratio"] * 1000)
    if row["employment_years"] > 3:
        score += 30
    return min(max(score, 300), 850)


def approve_loan(row, threshold=600):
    return "Approved" if risk_score(row) >= threshold else "Declined"


if __name__ == "__main__":
    apps = generate_application_data(200)
    apps["risk_score"] = apps.apply(risk_score, axis=1)
    apps["decision"] = apps.apply(approve_loan, axis=1)
    apps.to_csv("credit_applications_decisions.csv", index=False)
    approval_rate = (apps["decision"] == "Approved").mean()
    print(f"Processed {len(apps)} applications, approval rate: {approval_rate:.1%}")
    print("Output -> credit_applications_decisions.csv")
