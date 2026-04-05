"""
Credit Card Fraud Detection Demo
Author: Vinaya Sathyanarayana

This program demonstrates fraud detection classification techniques on synthetic credit card transaction data.

Features:
- Loads syntheticdata.csv (generated from synthetic_data_generator.py)
- Preprocesses data with feature encoding and scaling
- Applies multiple classification algorithms representing:
    - Statistical Parametric: Logistic Regression
    - Statistical Nonparametric: k-Nearest Neighbors
    - Proximity-based: also k-NN
    - Reconstruction-based: Autoencoder (using keras)
    - Clustering and Classification: Decision Tree, Random Forest
- Provides step-by-step explanations
- Visualizes results with graphs and interpretation
- Outputs a comparison table of model performance (accuracy, precision, recall, F1-score)
- Well documented with error handling
- Includes instructions for students and banking use-case

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import warnings
warnings.filterwarnings("ignore")

try:
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense
    from tensorflow.keras import regularizers
except ImportError:
    print("Warning: Tensorflow/Keras not found. Autoencoder part will be skipped.")


def load_and_preprocess_data(file_path='syntheticdata.csv'):
    """
    Load synthetic data and preprocess features for classification.

    Returns:
        X_train, X_test, y_train, y_test, feature_names (list)
    """
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded. Sample records:")
        print(df.head())

        # Drop card number and expiry as they do not help for fraud detection (or anonymize)
        df = df.drop(['CardNumber', 'ExpiryDate', 'MerchantName', 'TransactionDate'], axis=1)

        # Encode categorical variables: CardType, MerchantCategory, Location
        for col in ['CardType', 'MerchantCategory', 'Location']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])

        y = df['IsFraud']
        X = df.drop('IsFraud', axis=1)

        # Scale features (amount especially)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

        feature_names = X.columns.tolist()

        print(f"Data preprocessing complete. Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")

        return X_train, X_test, y_train, y_test, feature_names

    except Exception as e:
        print(f"Error in load_and_preprocess_data: {e}")
        traceback.print_exc()
        return None, None, None, None, None


def train_and_evaluate_model(model, model_name, X_train, y_train, X_test, y_test):
    """
    Train a classification model and evaluate with classification metrics.

    Returns:
        Dictionary of metrics
    """
    print(f"\nTraining model: {model_name}")
    try:
        model.fit(X_train, y_train)
        print("Training complete.")

        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        print(f"Evaluation Metrics for {model_name}:")
        print(classification_report(y_test, y_pred, zero_division=0))

        # Confusion matrix visualization with interpretation
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Fraud', 'Fraud'], yticklabels=['Not Fraud', 'Fraud'])
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.show()
        print(f"Interpretation: \nTP: {cm[1,1]}, TN: {cm[0,0]}, FP (Type I error): {cm[0,1]}, FN (Type II error): {cm[1,0]}")
        print("High false negatives mean missed frauds; high false positives mean unnecessary alerts.\n")

        return {'Model': model_name, 'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1-Score': f1}

    except Exception as e:
        print(f"Error training {model_name}: {e}")
        traceback.print_exc()
        return {'Model': model_name, 'Accuracy': 0, 'Precision': 0, 'Recall': 0, 'F1-Score': 0}


def build_autoencoder(input_dim):
    """
    Builds an autoencoder model for reconstruction-based anomaly detection.
    """
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(14, activation='relu', activity_regularizer=regularizers.l1(10e-5))(input_layer)
    encoded = Dense(7, activation='relu')(encoded)

    decoded = Dense(14, activation='relu')(encoded)
    decoded = Dense(input_dim, activation='linear')(decoded)

    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer='adam', loss='mse')

    return autoencoder


def autoencoder_anomaly_detection(X_train, X_test, y_test):
    """
    Train an autoencoder on non-fraud data and detect anomalies on test data.

    Returns:
        Dictionary of metrics
    """
    try:
        # Train only on non-fraud samples (label=0)
        X_train_nf = X_train[y_train == 0]

        input_dim = X_train.shape[1]
        autoencoder = build_autoencoder(input_dim)

        print("Training Autoencoder on non-fraud transactions...")
        history = autoencoder.fit(X_train_nf, X_train_nf,
                                  epochs=50,
                                  batch_size=32,
                                  shuffle=True,
                                  validation_data=(X_test, X_test),
                                  verbose=0)

        # Predict reconstruction error
        X_test_pred = autoencoder.predict(X_test)
        mse = np.mean(np.power(X_test - X_test_pred, 2), axis=1)

        # Set threshold as 95th percentile mse on train non-fraud (more robust thresholding can be explored)
        X_train_pred = autoencoder.predict(X_train_nf)
        mse_train = np.mean(np.power(X_train_nf - X_train_pred, 2), axis=1)
        threshold = np.percentile(mse_train, 95)

        print(f"Anomaly detection threshold (95th percentile mse): {threshold:.5f}")

        y_pred = (mse > threshold).astype(int)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        print("Evaluation Metrics for Reconstruction-based Approach (Autoencoder):")
        print(classification_report(y_test, y_pred, zero_division=0))

        # Plot mse distribution with threshold and fraud/non-fraud
        plt.figure(figsize=(8, 5))
        plt.hist(mse[y_test==0], bins=50, alpha=0.7, label='Non-Fraud')
        plt.hist(mse[y_test==1], bins=50, alpha=0.7, label='Fraud')
        plt.axvline(threshold, color='red', linestyle='--', label='Threshold')
        plt.title('Reconstruction Error (MSE) Distribution')
        plt.xlabel('MSE')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

        print("Interpretation:\nHigher reconstruction error indicates potential fraud transaction (anomaly).\nThreshold chosen to balance false positives and false negatives.\n")

        return {'Model': 'Autoencoder', 'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1-Score': f1}

    except Exception as e:
        print(f"Error in Autoencoder anomaly detection: {e}")
        traceback.print_exc()
        return {'Model': 'Autoencoder', 'Accuracy': 0, 'Precision': 0, 'Recall': 0, 'F1-Score': 0}


if __name__ == '__main__':
    import sys

    print("Credit Card Fraud Detection Demo - Starting...\n")

    # Load and preprocess data
    X_train, X_test, y_train, y_test, features = load_and_preprocess_data()

    if X_train is None:
        sys.exit("Data loading failed. Exiting.")

    results = []

    # Logistic Regression (Statistical Parametric)
    lr = LogisticRegression()
    results.append(train_and_evaluate_model(lr, "Logistic Regression", X_train, y_train, X_test, y_test))

    # k-Nearest Neighbors (Statistical Nonparametric & Proximity-based)
    knn = KNeighborsClassifier(n_neighbors=5)
    results.append(train_and_evaluate_model(knn, "k-Nearest Neighbors", X_train, y_train, X_test, y_test))

    # Decision Tree (Clustering and Classification-Based)
    dt = DecisionTreeClassifier(random_state=42)
    results.append(train_and_evaluate_model(dt, "Decision Tree", X_train, y_train, X_test, y_test))

    # Random Forest (Ensemble, Classification-Based)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    results.append(train_and_evaluate_model(rf, "Random Forest", X_train, y_train, X_test, y_test))

    # Reconstruction-based: Autoencoder (if tensorflow/keras available)
    try:
        if 'tensorflow' in sys.modules:
            results.append(autoencoder_anomaly_detection(X_train, X_test, y_test))
        else:
            print("Skipping Autoencoder model - tensorflow/keras not installed.")
    except NameError:
        print("Skipping Autoencoder model - tensorflow/keras not installed.")

    # Summary Table of Results
    results_df = pd.DataFrame(results)
    print("\nModel Performance Comparison:")
    print(results_df)

    # Plot comparison bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Model', y='Recall', data=results_df)
    plt.title('Model Recall Comparison - Important for Fraud Detection')
    plt.ylabel('Recall (Sensitivity)')
    plt.show()

    print("""
    Interpretation:
    - Recall is crucial in fraud detection to catch most fraudulent transactions (minimize false negatives).
    - Precision indicates correctness of flagged frauds (minimize false positives).
    - F1-Score balances recall and precision, useful for overall model comparison.
    - Banks must weigh recall vs. precision trade-offs based on operational priorities.
    """)

    print("Demo completed. Students are encouraged to modify parameters, add models, and explore the dataset and algorithms further.")
