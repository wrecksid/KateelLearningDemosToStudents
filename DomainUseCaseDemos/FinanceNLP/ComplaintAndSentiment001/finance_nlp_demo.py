"""
Finance NLP: complaint sentiment classification and topic detection.
"""

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_complaint_data(n=500):
    complaints = [
        ("Account locked, cannot login", "access_issue"),
        ("Charges not matching statement", "billing_dispute"),
        ("Interest rate seems too high", "rate_query"),
        ("Card declined at store", "transaction_issue"),
        ("How do I reset my password?", "access_issue"),
        ("Refund not received after 30 days", "billing_dispute"),
        ("APP keeps crashing", "technical_issue"),
        ("Can I get a credit limit increase?", "limit_request"),
        ("Why was my transaction flagged?", "transaction_issue"),
        ("My statement is wrong", "billing_dispute"),
    ] * (n // 10 + 1)
    texts, labels = zip(*complaints[:n])
    return pd.DataFrame({"complaint": texts, "category": labels})


def simple_sentiment(text):
    neg_words = ["wrong", "error", "issue", "declined", "cannot", "broken", "crash"]
    pos_words = ["increase", "raise", "good", "great", "resolved"]
    t = text.lower()
    score = sum(w in t for w in pos_words) - sum(w in t for w in neg_words)
    return "positive" if score > 0 else ("negative" if score < 0 else "neutral")


def demo_pipeline():
    if not HAS_SKLEARN:
        print("SKLearn not available; running lightweight demo.")
        df = generate_complaint_data(50)
        df["sentiment"] = df["complaint"].apply(simple_sentiment)
        print(df.head())
        return

    df = generate_complaint_data(200)
    pipe = make_pipeline(TfidfVectorizer(), MultinomialNB())
    pipe.fit(df["complaint"], df["category"])
    preds = pipe.predict(df["complaint"])
    df["predicted"] = preds
    acc = (df["predicted"] == df["category"]).mean()
    print(f"NLP classifier accuracy: {acc:.2f}")


if __name__ == "__main__":
    demo_pipeline()
    print("Finance NLP demo complete.")
