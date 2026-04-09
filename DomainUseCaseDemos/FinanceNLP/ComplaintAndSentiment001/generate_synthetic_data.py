import random
from pathlib import Path

import pandas as pd


PRODUCTS = ["Savings Account", "Credit Card", "Personal Loan", "Insurance", "UPI"]
CHANNELS = ["Branch", "Mobile App", "Call Center", "Email", "Website"]

COMPLAINT_LIBRARY = {
    "billing_issue": [
        "I was charged twice for the same credit card transaction and the extra amount is still not reversed.",
        "The bill shows a late fee even though I paid before the due date.",
        "The premium amount debited from my account does not match the policy schedule."
    ],
    "service_delay": [
        "My loan application has been pending for days and nobody is giving a clear update.",
        "The account opening request is still under review and the branch has not responded.",
        "I raised a support ticket for card replacement but the status has not changed."
    ],
    "fraud_alert": [
        "I noticed an unknown UPI transaction and need the bank to block further activity immediately.",
        "There are suspicious card transactions in a city I have never visited.",
        "I received a fraud alert after a payment and want to confirm whether my account is safe."
    ],
    "technical_issue": [
        "The mobile banking app crashes every time I try to transfer funds.",
        "The insurance portal fails during document upload and the claim cannot be submitted.",
        "The website login keeps timing out when I try to access my statements."
    ],
    "product_query": [
        "I need clarity on how the interest is calculated for the personal loan offer.",
        "Please explain the annual fee waiver condition on this card.",
        "I want to understand the difference between the savings variants before I upgrade."
    ],
}

SENTIMENT_SUFFIX = {
    "negative": [
        "This is very frustrating and I expect immediate action.",
        "I am unhappy with the service and do not want to repeat this complaint.",
        "The experience has been disappointing so far."
    ],
    "neutral": [
        "Please review the case and share the next steps.",
        "Kindly check and confirm the status.",
        "I am waiting for a proper update from the team."
    ],
    "positive": [
        "The branch staff was polite, but I still need a resolution.",
        "I appreciate the support so far and hope this can be fixed soon.",
        "Thank you for looking into this matter."
    ],
}


def main(rows: int = 600, output: str = "synthetic_complaints.csv") -> None:
    random.seed(42)
    records = []
    for idx in range(1, rows + 1):
        complaint_type = random.choice(list(COMPLAINT_LIBRARY))
        sentiment = random.choices(["negative", "neutral", "positive"], weights=[0.5, 0.35, 0.15])[0]
        product = random.choice(PRODUCTS)
        channel = random.choice(CHANNELS)
        text = f"{random.choice(COMPLAINT_LIBRARY[complaint_type])} {random.choice(SENTIMENT_SUFFIX[sentiment])}"
        escalation_needed = int(complaint_type in {"fraud_alert", "billing_issue"} and sentiment == "negative")

        records.append(
            {
                "complaint_id": f"CMP{idx:05d}",
                "product": product,
                "channel": channel,
                "complaint_type": complaint_type,
                "sentiment_label": sentiment,
                "escalation_needed": escalation_needed,
                "text": text,
            }
        )

    df = pd.DataFrame(records)
    out_path = Path(output)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} complaint rows to {out_path}")


if __name__ == "__main__":
    main()
