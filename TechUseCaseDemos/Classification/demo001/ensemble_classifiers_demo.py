"""
Ensemble classifiers comparison demo.
"""

import numpy as np
import pandas as pd
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.model_selection import cross_val_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

np.random.seed(42)

def make_data(n=1000):
    X = np.random.randn(n, 10)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    return X, y

def demo():
    if not HAS_SKLEARN:
        print("SKLearn not installed; skipping ensemble demo.")
        return
    X, y = make_data(500)
    clfs = [
        ("rf", RandomForestClassifier(n_estimators=50, random_state=42)),
        ("gb", GradientBoostingClassifier(n_estimators=50, random_state=42)),
        ("lr", LogisticRegression(max_iter=1000)),
        ("svc", SVC(probability=True)),
    ]
    for name, m in clfs:
        scores = cross_val_score(m, X, y, cv=3)
        print(f"{name}: {scores.mean():.3f} (+/- {scores.std():.3f})")
    # Voting ensemble
    voting = VotingClassifier(estimators=[(n, m) for n, m in clfs], voting="soft")
    vscores = cross_val_score(voting, X, y, cv=3)
    print(f"VotingEnsemble: {vscores.mean():.3f} (+/- {vscores.std():.3f})")
    print("Ensemble classifiers demo complete.")

if __name__ == "__main__":
    demo()
