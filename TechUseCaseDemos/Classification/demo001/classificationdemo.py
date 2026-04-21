"""
Classification Demo with Synthetic Financial Data
Author: Vinaya Sathyanarayana

This program demonstrates classification techniques and algorithms using the synthetic financial dataset 'syntheticdata.csv'.
It implements base classifiers and ensemble classifiers for predicting customer default risk.

Algorithms included:
- Decision Tree
- Rule-based (using Decision Tree with max_depth=2 for interpretability)
- Nearest Neighbor (K-Nearest Neighbors)
- Naïve Bayes
- Support Vector Machine (SVM)
- Neural Network (MLPClassifier)
- Logistic Regression
- Ensemble methods: Random Forest, AdaBoost

The program outputs:
- Model training progress
- Accuracy scores and classification reports
- Confusion matrices
- ROC curves
- Comparative evaluation table

Instructions for students:
- Change model parameters and dataset size in the synthetic data generator.
- Experiment with feature selection and hyperparameters.
- Understand model strengths/weaknesses from metrics and visualizations.

How a bank can use this program:
- Train models on customer data for default prediction.
- Use model comparisons to choose best algorithm for credit risk.
- Visualizations help interpret model performance for management decisions.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
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
    # Convert categorical columns to numeric using Label Encoding
    try:
        df_enc = df.copy()
        label_encoders = {}
        for col in ['Gender', 'State']:
            le = LabelEncoder()
            df_enc[col] = le.fit_transform(df_enc[col])
            label_encoders[col] = le

        # Features and target
        X = df_enc.drop(columns=["IsFraud"])
        y = df_enc["IsFraud"]

        # Scale continuous variables (Age, Annual_Income)
        scaler = StandardScaler()
        X[['Age', 'Annual_Income']] = scaler.fit_transform(X[['Age', 'Annual_Income']])

        return X, y, label_encoders, scaler
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
    plt.plot(fpr, tpr, color='darkorange',
             lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([-0.01, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Receiver Operating Characteristic - {model_name}')
    plt.legend(loc="lower right")
    plt.show()

def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    print(f"\nTraining {name}...")
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
            y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min()) # scale to 0-1 for ROC

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
    X, y, label_encoders, scaler = preprocess_data(df)

    # Split into train and test 70:30 split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    results = []

    # Base classifiers
    base_classifiers = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Rule-based (Decision Tree max_depth=2)': DecisionTreeClassifier(max_depth=2, random_state=42),
        'Nearest Neighbor (KNN)': KNeighborsClassifier(),
        'Naive Bayes': GaussianNB(),
        'Support Vector Machine': SVC(probability=True, random_state=42),
        'Neural Network (MLP)': MLPClassifier(max_iter=300, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=200, random_state=42)
    }

    print("\n--- Base Classifiers ---")
    for name, model in base_classifiers.items():
        res = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        if res:
            results.append(res)

    # Ensemble classifiers
    ensemble_classifiers = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'AdaBoost': AdaBoostClassifier(n_estimators=50, random_state=42)
    }

    print("\n--- Ensemble Classifiers ---")
    for name, model in ensemble_classifiers.items():
        res = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        if res:
            results.append(res)

    # Create comparison table
    print("\nModel Performance Comparison:")
    comp_df = pd.DataFrame(results)
    comp_df = comp_df[['model', 'accuracy', 'auc']].sort_values(by='accuracy', ascending=False).reset_index(drop=True)
    print(comp_df)

    # Save comparison to CSV for students to explore if desired
    comp_df.to_csv('model_comparison.csv', index=False)
    print("\nComparison table saved as 'model_comparison.csv'")

if __name__ == "__main__":
    main()
