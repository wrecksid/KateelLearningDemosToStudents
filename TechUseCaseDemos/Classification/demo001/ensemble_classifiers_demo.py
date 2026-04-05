"""
Ensemble Classifiers Demo with Synthetic Financial Data
Author: Vinaya Sathyanarayana

This program demonstrates ensemble classification techniques using the synthetic financial dataset 'syntheticdata.csv'.
It focuses on:
- Random Forest
- AdaBoost

Outputs include:
- Training progress
- Accuracy, classification reports
- Confusion matrices
- ROC curves
- Explanations with each plot

Bank usage:
- Assess how ensemble methods improve prediction accuracy and stability over base classifiers.
- Help select ensemble methods for credit risk modeling.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

import warnings
warnings.filterwarnings('ignore')

def load_data(filepath='syntheticdata.csv'):
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found. Please generate synthetic data first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def preprocess_data(df):
    try:
        df_enc = df.copy()
        for col in ['Gender', 'Occupation', 'State']:
            le = LabelEncoder()
            df_enc[col] = le.fit_transform(df_enc[col])

        X = df_enc.drop(columns=['Default'])
        y = df_enc['Default']

        scaler = StandardScaler()
        X[['Age', 'Annual_Income']] = scaler.fit_transform(X[['Age', 'Annual_Income']])

        return X, y
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)

def plot_confusion_matrix(cm, labels, title='Confusion Matrix'):
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(title)
    plt.show()

def plot_roc_curve(fpr, tpr, roc_auc, model_name):
    plt.figure()
    plt.plot(fpr, tpr, color='green',
             lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlim([-0.01, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Receiver Operating Characteristic - {model_name}')
    plt.legend(loc="lower right")
    plt.show()

def evaluate_ensemble(name, model, X_train, X_test, y_train, y_test):
    print(f"\nTraining {name} ensemble classifier...")
    try:
        model.fit(X_train, y_train)
        print(f"Model {name} trained successfully.")
    except Exception as e:
        print(f"Error training {name}: {e}")
        return None

    try:
        y_pred = model.predict(X_test)
        y_prob = None
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:,1]
        elif hasattr(model, "decision_function"):
            y_prob = model.decision_function(X_test)
            y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min())  

        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy of {name}: {acc:.4f}")

        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        plot_confusion_matrix(cm, labels=['No_Default', 'Default'], title=f'Confusion Matrix - {name}')

        if y_prob is not None:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_auc = auc(fpr, tpr)
            plot_roc_curve(fpr, tpr, roc_auc, name)
        else:
            roc_auc = None

        return {'model': name, 'accuracy': acc, 'auc': roc_auc}
    except Exception as e:
        print(f"Error during evaluation of {name}: {e}")
        return None


def main():
    df = load_data()
    X, y = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    results = []

    ensemble_classifiers = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'AdaBoost': AdaBoostClassifier(n_estimators=50, random_state=42)
    }

    for name, model in ensemble_classifiers.items():
        res = evaluate_ensemble(name, model, X_train, X_test, y_train, y_test)
        if res:
            results.append(res)

    # Comparison table
    print("\nEnsemble Model Performance Comparison:")
    comp_df = pd.DataFrame(results)
    comp_df = comp_df[['model', 'accuracy', 'auc']].sort_values(by='accuracy', ascending=False).reset_index(drop=True)
    print(comp_df)

    comp_df.to_csv('ensemble_model_comparison.csv', index=False)
    print("\nComparison table saved as 'ensemble_model_comparison.csv'")

if __name__ == "__main__":
    main()
