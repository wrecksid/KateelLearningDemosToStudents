"""
Full ML classification pipeline: preprocessing, training, evaluation.
"""

import numpy as np
import pandas as pd
try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

np.random.seed(42)

def make_data(n=1000):
    X = np.random.randn(n, 8)
    y = (X[:, 0] + X[:, 1] - X[:, 2] > 0).astype(int)
    return X, y

def demo():
    if not HAS_SKLEARN:
        print("SKLearn not installed; skipping full classification demo.")
        return
    X, y = make_data(600)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_s, y_train)
    preds = clf.predict(X_test_s)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))
    print("Classification Report:\n", classification_report(y_test, preds))
    print("Full classification demo complete.")

if __name__ == "__main__":
    demo()
