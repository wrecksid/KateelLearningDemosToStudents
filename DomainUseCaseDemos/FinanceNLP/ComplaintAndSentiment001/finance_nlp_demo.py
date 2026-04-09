from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


POSITIVE_WORDS = {"appreciate", "thank", "polite", "fixed", "support"}
NEGATIVE_WORDS = {"frustrating", "unhappy", "disappointing", "suspicious", "crashes", "timeout"}


def simple_sentiment(text: str) -> str:
    tokens = {token.strip(".,!?").lower() for token in text.split()}
    score = len(tokens & POSITIVE_WORDS) - len(tokens & NEGATIVE_WORDS)
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def main(data_file: str = "synthetic_complaints.csv") -> None:
    data_path = Path(data_file)
    if not data_path.exists():
        raise FileNotFoundError(f"{data_path} not found. Run generate_synthetic_data.py first.")

    df = pd.read_csv(data_path)
    x_train, x_test, y_train, y_test = train_test_split(
        df["text"], df["complaint_type"], test_size=0.25, random_state=42, stratify=df["complaint_type"]
    )

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
            ("clf", LogisticRegression(max_iter=500)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    print("\nComplaint Type Classification Report")
    print(classification_report(y_test, predictions))

    df["predicted_sentiment"] = df["text"].apply(simple_sentiment)
    sentiment_summary = pd.crosstab(df["sentiment_label"], df["predicted_sentiment"])
    print("\nSentiment Label vs Simple Sentiment Heuristic")
    print(sentiment_summary)

    escalation_view = (
        df.groupby(["complaint_type", "predicted_sentiment"])["escalation_needed"]
        .mean()
        .reset_index()
        .sort_values(["escalation_needed", "complaint_type"], ascending=[False, True])
    )
    print("\nEscalation Patterns")
    print(escalation_view.to_string(index=False))


if __name__ == "__main__":
    main()
