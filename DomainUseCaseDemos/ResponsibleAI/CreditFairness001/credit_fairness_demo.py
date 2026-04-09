from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC = ["income", "credit_score", "debt_to_income", "delinquencies", "job_stability"]
CATEGORICAL = ["gender", "region"]


def subgroup_metrics(df: pd.DataFrame, group_col: str, score_col: str, pred_col: str, actual_col: str) -> pd.DataFrame:
    rows = []
    for group_value, group_df in df.groupby(group_col):
        tn, fp, fn, tp = confusion_matrix(group_df[actual_col], group_df[pred_col], labels=[0, 1]).ravel()
        rows.append(
            {
                "group": group_value,
                "count": len(group_df),
                "approval_rate": round(group_df[pred_col].mean(), 4),
                "avg_score": round(group_df[score_col].mean(), 4),
                "true_positive_rate": round(tp / max(tp + fn, 1), 4),
                "false_positive_rate": round(fp / max(fp + tn, 1), 4),
            }
        )
    return pd.DataFrame(rows).sort_values("group")


def main(data_file: str = "synthetic_credit_fairness.csv") -> None:
    path = Path(data_file)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run generate_synthetic_data.py first.")

    df = pd.read_csv(path)
    x = df[NUMERIC + CATEGORICAL]
    y = df["approved"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ]
    )

    model = Pipeline(
        [
            ("prep", preprocessor),
            ("clf", LogisticRegression(max_iter=500)),
        ]
    )
    model.fit(x_train, y_train)

    scores = model.predict_proba(x_test)[:, 1]
    preds = (scores >= 0.5).astype(int)
    eval_df = x_test.copy()
    eval_df["approved_actual"] = y_test.to_numpy()
    eval_df["approved_pred"] = preds
    eval_df["score"] = scores

    print("\nOverall AUC")
    print(round(roc_auc_score(y_test, scores), 4))

    print("\nFairness View by Gender")
    print(subgroup_metrics(eval_df, "gender", "score", "approved_pred", "approved_actual").to_string(index=False))

    print("\nFairness View by Region")
    print(subgroup_metrics(eval_df, "region", "score", "approved_pred", "approved_actual").to_string(index=False))

    approval_gap = (
        eval_df.groupby("gender")["approved_pred"].mean().max()
        - eval_df.groupby("gender")["approved_pred"].mean().min()
    )
    print("\nApproval Rate Gap Across Gender")
    print(round(float(approval_gap), 4))


if __name__ == "__main__":
    main()
