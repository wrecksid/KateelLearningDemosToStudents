"""
Full Classification Demo with Synthetic Financial Data
Author: Vinaya Sathyanarayana

This program demonstrates a wide range of classification algorithms on synthetic financial data ('syntheticdata.csv').
It includes:
- Base classifiers: Decision Tree, Rule-based, KNN, Naive Bayes, SVM, Neural Net, Logistic Regression
- Ensemble classifiers: Random Forest, AdaBoost

Outputs include:
- Loading and preprocessing steps with explanations
- Model training progress and error handling
- Classification reports with detailed metrics
- Confusion matrix plots with interpretation
- ROC curve plots with interpretation
- Final comparative performance table saved as CSV

Instructions for students:
- Explore changes by tuning hyperparameters below and observe their influence on results.
- Modify synthetic data generator inputs to see effects of different dataset distributions.
- Use plots to interpret model performance beyond accuracy, focusing on recall and precision in credit risk.

Bank use case:
- Use extensive evaluation to select robust and interpretable models for credit default prediction.
- Ensemble methods show improvements and reduce overfitting risks.
- Visualizations assist management understanding and decision-making for credit policies.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, roc_curve, auc
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

warnings.filterwarnings('ignore')

def load_data(filepath='syntheticdata.csv'):
    """
    Load synthetic dataset from CSV, with error handling.
    """
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found. Please generate synthetic data first using the provided generator.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        sys.exit(1)


def preprocess_data(df):
    """
    Preprocess dataset:
    - Encode categorical features to numeric.
    - Scale continuous features (Age, Annual_Income).
    - Split features and target variable.
    Returns transformed features, labels.
    """
    try:
        df_enc = df.copy()
        for col in ['Gender', 'Occupation', 'State']:
            le = LabelEncoder()
            df_enc[col] = le.fit_transform(df_enc[col])

        X = df_enc.drop(columns=['Default'])
        y = df_enc['Default']

        scaler = StandardScaler()
        X[['Age', 'Annual_Income']] = scaler.fit_transform(X[['Age', 'Annual_Income']])

        print("Preprocessing done: Categorical features encoded, continuous features scaled.")
        return X, y
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        sys.exit(1)

def plot_confusion_matrix(cm, labels, title='Confusion Matrix'):
    """
    Plot confusion matrix using seaborn heatmap.
    """
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(title)
    plt.show()

def plot_roc_curve(fpr, tpr, roc_auc, model_name):
    """
    Plot ROC curve with AUC annotation.
    Explanation: ROC curve shows trade-off between true positive rate and false positive rate.
    AUC close to 1 indicates excellent model.
    """
    plt.figure()
    plt.plot(fpr, tpr, color='blue',
             lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--', label='Random guess')
    plt.xlim([-0.01, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc="lower right")
    plt.show()

def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    """
    Train model, evaluate on test set with metrics and plots.
    Prints:
    - Accuracy score
    - Classification report (precision, recall, f1-score)
    - Confusion matrix plot and explanation
    - ROC curve plot and explanation
    Returns dictionary with accuracy and AUC for comparison.
    """
    print(f"\nTraining model: {name}")
    try:
        model.fit(X_train, y_train)
        print(f"Model '{name}' trained successfully.")
    except Exception as e:
        print(f"Training error for {name}: {e}")
        return None

    try:
        y_pred = model.predict(X_test)

        # For ROC curve probability or decision_function needed
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:,1]
        elif hasattr(model, "decision_function"):
            y_prob_raw = model.decision_function(X_test)
            # Scale decision_function output to [0,1] for ROC
            y_prob = (y_prob_raw - y_prob_raw.min()) / (y_prob_raw.max() - y_prob_raw.min())
        else:
            y_prob = None

        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")

        print("Classification Report:\n", classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        plot_confusion_matrix(cm, labels=['No Default (0)', 'Default (1)'], title=f"Confusion Matrix - {name}")
        print("Confusion matrix interpretation:")
        print("  - Diagonal elements are correct predictions.")
        print("  - Off-diagonal elements represent misclassifications, important in credit risk to minimize false negatives (missed defaults).")

        if y_prob is not None:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            plot_roc_curve(fpr, tpr, roc_auc, name)
        else:
            roc_auc = None
            print("ROC curve not available for this model.")

        return {'Model': name, 'Accuracy': acc, 'AUC': roc_auc}

    except Exception as e:
        print(f"Error during model evaluation for {name}: {e}")
        return None

def main():
    print("Starting Full Classification Demo...")

    df = load_data()
    X, y = preprocess_data(df)

    # Train-test split: 70% train, 30% test with reproducibility
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Define models
    base_classifiers = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Rule-based (Decision Tree max_depth=2)': DecisionTreeClassifier(max_depth=2, random_state=42),
        'Nearest Neighbor (KNN)': KNeighborsClassifier(),
        'Naive Bayes': GaussianNB(),
        'Support Vector Machine': SVC(probability=True, random_state=42),
        'Neural Network (MLP)': MLPClassifier(max_iter=300, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=200, random_state=42)
    }

    ensemble_classifiers = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'AdaBoost': AdaBoostClassifier(n_estimators=50, random_state=42)
    }

    all_classifiers = {**base_classifiers, **ensemble_classifiers}

    results = []

    print("\nEvaluating Base Classifiers...")
    for clf_name, clf_model in base_classifiers.items():
        res = evaluate_model(clf_name, clf_model, X_train, X_test, y_train, y_test)
        if res is not None:
            results.append(res)

    print("\nEvaluating Ensemble Classifiers...")
    for clf_name, clf_model in ensemble_classifiers.items():
        res = evaluate_model(clf_name, clf_model, X_train, X_test, y_train, y_test)
        if res is not None:
            results.append(res)

    # Results comparison table
    print("\nFinal Model Comparison Table:")
    results_df = pd.DataFrame(results)
    results_df_sorted = results_df.sort_values(by='Accuracy', ascending=False).reset_index(drop=True)
    print(results_df_sorted)

    # Save comparison to CSV for exploration
    results_df_sorted.to_csv('full_model_comparison.csv', index=False)
    print("\nSaved model comparison table as 'full_model_comparison.csv'")

    print("\nDemo complete. Students are encouraged to tune parameters and explore further!")

if __name__ == "__main__":
    main()
