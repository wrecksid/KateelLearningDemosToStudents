"""
Credit Card Fraud Detection - Machine Learning Demo
=================================================

This module demonstrates credit card fraud detection using various
machine learning algorithms with comprehensive analysis and visualization.

Author: Educational Demo
Course: Masters in Finance - AI/ML Applications
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import (classification_report, confusion_matrix, roc_auc_score, 
                           roc_curve, precision_recall_curve, f1_score)
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

import argparse
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CreditCardFraudDetector:
    """
    Comprehensive credit card fraud detection system with multiple ML algorithms
    and extensive analysis capabilities.
    """
    
    def __init__(self, data_file=None):
        """
        Initialize the fraud detector.
        
        Args:
            data_file (str): Path to the CSV data file
        """
        self.data_file = data_file
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.models = {}
        self.results = {}
        
        logger.info("Initialized CreditCardFraudDetector")
    
    def load_data(self, file_path=None):
        """
        Load credit card transaction data from CSV file.
        
        Args:
            file_path (str): Path to CSV file. If None, uses self.data_file
        """
        try:
            file_path = file_path or self.data_file
            if not file_path or not os.path.exists(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            self.df = pd.read_csv(file_path)
            logger.info(f"Loaded data: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            
            # Convert timestamp if present
            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            # Basic data validation
            if 'is_fraud' not in self.df.columns:
                raise ValueError("Target column 'is_fraud' not found in data")
            
            self._print_data_summary()
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _print_data_summary(self):
        """Print comprehensive data summary."""
        print("\n" + "="*60)
        print("CREDIT CARD FRAUD DETECTION - DATA SUMMARY")
        print("="*60)
        print(f"Dataset shape: {self.df.shape}")
        print(f"Total transactions: {len(self.df):,}")
        print(f"Fraudulent transactions: {self.df['is_fraud'].sum():,}")
        print(f"Fraud rate: {self.df['is_fraud'].mean()*100:.3f}%")
        print(f"Date range: {self.df['timestamp'].min()} to {self.df['timestamp'].max()}")
        
        print(f"\nMissing values:")
        missing = self.df.isnull().sum()
        if missing.any():
            print(missing[missing > 0])
        else:
            print("No missing values found")
        
        print(f"\nAmount statistics:")
        print(f"Min: ₹{self.df['amount'].min():.2f}")
        print(f"Max: ₹{self.df['amount'].max():.2f}")
        print(f"Mean: ₹{self.df['amount'].mean():.2f}")
        print(f"Median: ₹{self.df['amount'].median():.2f}")
    
    def exploratory_data_analysis(self):
        """
        Perform comprehensive exploratory data analysis with visualizations.
        """
        logger.info("Performing exploratory data analysis...")
        
        # Set up the plotting area
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Credit Card Fraud Detection - Exploratory Data Analysis', fontsize=16)
        
        # 1. Fraud distribution
        fraud_counts = self.df['is_fraud'].value_counts()
        axes[0,0].pie(fraud_counts.values, labels=['Normal', 'Fraud'], autopct='%1.2f%%', 
                     colors=['lightblue', 'red'])
        axes[0,0].set_title('Transaction Distribution')
        
        # 2. Amount distribution by fraud status
        self.df.boxplot(column='amount', by='is_fraud', ax=axes[0,1])
        axes[0,1].set_title('Amount Distribution by Fraud Status')
        axes[0,1].set_xlabel('Fraud Status (0=Normal, 1=Fraud)')
        
        # 3. Fraud by hour of day
        fraud_by_hour = self.df.groupby('hour_of_day')['is_fraud'].mean()
        axes[0,2].bar(fraud_by_hour.index, fraud_by_hour.values, color='orange')
        axes[0,2].set_title('Fraud Rate by Hour of Day')
        axes[0,2].set_xlabel('Hour')
        axes[0,2].set_ylabel('Fraud Rate')
        
        # 4. Fraud by merchant category
        fraud_by_category = self.df.groupby('merchant_category')['is_fraud'].mean().sort_values(ascending=False)
        axes[1,0].barh(fraud_by_category.index, fraud_by_category.values, color='green')
        axes[1,0].set_title('Fraud Rate by Merchant Category')
        axes[1,0].set_xlabel('Fraud Rate')
        
        # 5. Amount vs Age scatter (colored by fraud)
        normal_data = self.df[self.df['is_fraud'] == 0].sample(n=min(1000, len(self.df[self.df['is_fraud'] == 0])))
        fraud_data = self.df[self.df['is_fraud'] == 1]
        
        axes[1,1].scatter(normal_data['customer_age'], normal_data['amount'], 
                         alpha=0.6, label='Normal', s=10)
        axes[1,1].scatter(fraud_data['customer_age'], fraud_data['amount'], 
                         alpha=0.8, label='Fraud', s=10, color='red')
        axes[1,1].set_xlabel('Customer Age')
        axes[1,1].set_ylabel('Amount')
        axes[1,1].set_title('Amount vs Age (Sample)')
        axes[1,1].legend()
        
        # 6. Correlation heatmap for numerical features
        numerical_cols = ['amount', 'customer_age', 'hour_of_day', 'amount_to_income_ratio', 
                         'amount_to_limit_ratio', 'is_fraud']
        correlation_matrix = self.df[numerical_cols].corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                   ax=axes[1,2], fmt='.2f')
        axes[1,2].set_title('Feature Correlation Matrix')
        
        plt.tight_layout()
        plt.show()
        
        # Additional interactive plot using Plotly
        self._create_interactive_plots()
    
    def _create_interactive_plots(self):
        """Create interactive plots using Plotly."""
        logger.info("Creating interactive visualizations...")
        
        # Interactive time series plot
        daily_stats = self.df.groupby(self.df['timestamp'].dt.date).agg({
            'is_fraud': ['count', 'sum', 'mean'],
            'amount': 'mean'
        }).round(4)
        
        daily_stats.columns = ['total_transactions', 'fraud_count', 'fraud_rate', 'avg_amount']
        daily_stats = daily_stats.reset_index()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Daily Fraud Rate', 'Daily Transaction Volume', 
                          'Daily Average Amount', 'Fraud vs Normal Amount Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Daily fraud rate
        fig.add_trace(
            go.Scatter(x=daily_stats['timestamp'], y=daily_stats['fraud_rate'],
                      name='Fraud Rate', line=dict(color='red')),
            row=1, col=1
        )
        
        # Daily transaction volume
        fig.add_trace(
            go.Bar(x=daily_stats['timestamp'], y=daily_stats['total_transactions'],
                  name='Transaction Count', marker_color='blue'),
            row=1, col=2
        )
        
        # Daily average amount
        fig.add_trace(
            go.Scatter(x=daily_stats['timestamp'], y=daily_stats['avg_amount'],
                      name='Avg Amount', line=dict(color='green')),
            row=2, col=1
        )
        
        # Amount distribution
        fig.add_trace(
            go.Histogram(x=self.df[self.df['is_fraud']==0]['amount'], 
                        name='Normal', opacity=0.7, nbinsx=50),
            row=2, col=2
        )
        fig.add_trace(
            go.Histogram(x=self.df[self.df['is_fraud']==1]['amount'], 
                        name='Fraud', opacity=0.7, nbinsx=50),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Credit Card Fraud Analysis Dashboard")
        fig.show()
    
    def prepare_features(self, test_size=0.2, random_state=42, apply_smote=True):
        """
        Prepare features for machine learning models.
        
        Args:
            test_size (float): Proportion of data for testing
            random_state (int): Random state for reproducibility
            apply_smote (bool): Whether to apply SMOTE for balancing
        """
        logger.info("Preparing features for machine learning...")
        
        # Select features (exclude non-predictive columns)
        feature_columns = [col for col in self.df.columns if col not in 
                          ['transaction_id', 'customer_id', 'timestamp', 'is_fraud',
                           'customer_city', 'transaction_city']]
        
        # Handle categorical variables
        df_processed = self.df.copy()
        
        # One-hot encode categorical variables
        categorical_cols = ['merchant_category']
        df_processed = pd.get_dummies(df_processed, columns=categorical_cols, prefix=categorical_cols)
        
        # Update feature columns after encoding
        feature_columns = [col for col in df_processed.columns if col not in 
                          ['transaction_id', 'customer_id', 'timestamp', 'is_fraud',
                           'customer_city', 'transaction_city']]
        
        X = df_processed[feature_columns]
        y = df_processed['is_fraud']
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale the features
        self.scaler = RobustScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Apply SMOTE to handle class imbalance
        if apply_smote:
            logger.info("Applying SMOTE for class balancing...")
            smote = SMOTE(random_state=random_state, sampling_strategy=0.1)  # 10% fraud ratio
            self.X_train_balanced, self.y_train_balanced = smote.fit_resample(
                self.X_train_scaled, self.y_train
            )
        else:
            self.X_train_balanced = self.X_train_scaled
            self.y_train_balanced = self.y_train
        
        print(f"\nFeature preparation complete:")
        print(f"Training set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")
        print(f"Features: {self.X_train.shape[1]}")
        print(f"Original fraud rate in training: {self.y_train.mean()*100:.2f}%")
        if apply_smote:
            print(f"Balanced fraud rate in training: {self.y_train_balanced.mean()*100:.2f}%")
    
    def train_models(self):
        """Train multiple machine learning models for fraud detection."""
        logger.info("Training machine learning models...")
        
        # Define models
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, 
                                                   class_weight='balanced'),
            'Isolation Forest': IsolationForest(contamination=0.02, random_state=42)
        }
        
        self.models = {}
        self.results = {}
        
        for name, model in models.items():
            logger.info(f"Training {name}...")
            
            try:
                if name == 'Isolation Forest':
                    # Isolation Forest is unsupervised
                    model.fit(self.X_train_scaled)
                    
                    # Predict on test set (-1 for outliers, 1 for inliers)
                    predictions = model.predict(self.X_test_scaled)
                    # Convert to binary (1 for fraud, 0 for normal)
                    y_pred = np.where(predictions == -1, 1, 0)
                    y_pred_proba = model.decision_function(self.X_test_scaled)
                    # Normalize scores to [0,1] range
                    y_pred_proba = (y_pred_proba - y_pred_proba.min()) / (y_pred_proba.max() - y_pred_proba.min())
                    
                else:
                    # Supervised models
                    model.fit(self.X_train_balanced, self.y_train_balanced)
                    y_pred = model.predict(self.X_test_scaled)
                    y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
                
                # Calculate metrics
                accuracy = (y_pred == self.y_test).mean()
                precision = (y_pred * self.y_test).sum() / (y_pred.sum() + 1e-8)
                recall = (y_pred * self.y_test).sum() / (self.y_test.sum() + 1e-8)
                f1 = 2 * (precision * recall) / (precision + recall + 1e-8)
                
                try:
                    auc_score = roc_auc_score(self.y_test, y_pred_proba)
                except:
                    auc_score = 0.5
                
                self.models[name] = model
                self.results[name] = {
                    'model': model,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba,
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'auc_score': auc_score
                }
                
                logger.info(f"{name} - AUC: {auc_score:.3f}, F1: {f1:.3f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {str(e)}")
                continue
        
        self._print_model_comparison()
    
    def _print_model_comparison(self):
        """Print comparison of model performances."""
        print("\n" + "="*80)
        print("MODEL PERFORMANCE COMPARISON")
        print("="*80)
        print(f"{'Model':<20} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'AUC':<10}")
        print("-" * 80)
        
        for name, result in self.results.items():
            print(f"{name:<20} {result['accuracy']:<10.3f} {result['precision']:<10.3f} "
                  f"{result['recall']:<10.3f} {result['f1_score']:<10.3f} {result['auc_score']:<10.3f}")
    
    def visualize_results(self):
        """Create comprehensive visualizations of model results."""
        logger.info("Creating result visualizations...")
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Credit Card Fraud Detection - Model Results', fontsize=16)
        
        # 1. Model Performance Comparison
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'auc_score']
        model_names = list(self.results.keys())
        
        x = np.arange(len(model_names))
        width = 0.15
        
        for i, metric in enumerate(metrics):
            values = [self.results[name][metric] for name in model_names]
            axes[0,0].bar(x + i*width, values, width, label=metric.replace('_', ' ').title())
        
        axes[0,0].set_xlabel('Models')
        axes[0,0].set_ylabel('Score')
        axes[0,0].set_title('Model Performance Comparison')
        axes[0,0].set_xticks(x + width * 2)
        axes[0,0].set_xticklabels(model_names, rotation=45)
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. ROC Curves
        for name, result in self.results.items():
            try:
                fpr, tpr, _ = roc_curve(self.y_test, result['probabilities'])
                axes[0,1].plot(fpr, tpr, label=f"{name} (AUC = {result['auc_score']:.3f})")
            except:
                continue
        
        axes[0,1].plot([0, 1], [0, 1], 'k--', label='Random')
        axes[0,1].set_xlabel('False Positive Rate')
        axes[0,1].set_ylabel('True Positive Rate')
        axes[0,1].set_title('ROC Curves')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Precision-Recall Curves
        for name, result in self.results.items():
            try:
                precision, recall, _ = precision_recall_curve(self.y_test, result['probabilities'])
                axes[0,2].plot(recall, precision, label=f"{name}")
            except:
                continue
        
        axes[0,2].set_xlabel('Recall')
        axes[0,2].set_ylabel('Precision')
        axes[0,2].set_title('Precision-Recall Curves')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
        
        # 4. Confusion Matrix for best model (highest F1-score)
        best_model_name = max(self.results.keys(), key=lambda k: self.results[k]['f1_score'])
        best_result = self.results[best_model_name]
        
        cm = confusion_matrix(self.y_test, best_result['predictions'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1,0])
        axes[1,0].set_title(f'Confusion Matrix - {best_model_name}')
        axes[1,0].set_xlabel('Predicted')
        axes[1,0].set_ylabel('Actual')
        
        # 5. Feature Importance (for Random Forest)
        if 'Random Forest' in self.results:
            rf_model = self.models['Random Forest']
            feature_importance = rf_model.feature_importances_
            feature_names = self.X_train.columns
            
            # Get top 10 features
            top_indices = np.argsort(feature_importance)[-10:]
            top_features = [feature_names[i] for i in top_indices]
            top_importance = feature_importance[top_indices]
            
            axes[1,1].barh(top_features, top_importance, color='skyblue')
            axes[1,1].set_title('Top 10 Feature Importance (Random Forest)')
            axes[1,1].set_xlabel('Importance')
        
        # 6. Fraud Detection Rate by Amount Range
        amount_ranges = pd.cut(self.df['amount'], bins=10)
        fraud_by_amount = self.df.groupby(amount_ranges)['is_fraud'].agg(['count', 'sum', 'mean'])
        
        axes[1,2].bar(range(len(fraud_by_amount)), fraud_by_amount['mean'], color='coral')
        axes[1,2].set_title('Fraud Rate by Amount Range')
        axes[1,2].set_xlabel('Amount Range (Low to High)')
        axes[1,2].set_ylabel('Fraud Rate')
        axes[1,2].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def generate_business_insights(self):
        """Generate business insights and recommendations."""
        print("\n" + "="*80)
        print("BUSINESS INSIGHTS AND RECOMMENDATIONS")
        print("="*80)
        
        # Find best performing model
        best_model_name = max(self.results.keys(), key=lambda k: self.results[k]['f1_score'])
        best_result = self.results[best_model_name]
        
        print(f"\n🏆 BEST PERFORMING MODEL: {best_model_name}")
        print(f"   - F1-Score: {best_result['f1_score']:.3f}")
        print(f"   - Precision: {best_result['precision']:.3f}")
        print(f"   - Recall: {best_result['recall']:.3f}")
        print(f"   - AUC: {best_result['auc_score']:.3f}")
        
        # Calculate financial impact
        total_fraud_amount = self.df[self.df['is_fraud'] == 1]['amount'].sum()
        avg_fraud_amount = self.df[self.df['is_fraud'] == 1]['amount'].mean()
        
        # Estimate detection savings with best model
        detected_frauds = int(best_result['recall'] * self.y_test.sum())
        prevented_loss = detected_frauds * avg_fraud_amount
        
        print(f"\n💰 FINANCIAL IMPACT ANALYSIS:")
        print(f"   - Total fraud amount in dataset: ₹{total_fraud_amount:,.2f}")
        print(f"   - Average fraud transaction: ₹{avg_fraud_amount:,.2f}")
        print(f"   - Estimated frauds detected by best model: {detected_frauds}")
        print(f"   - Estimated prevented loss: ₹{prevented_loss:,.2f}")
        
        # Risk patterns
        print(f"\n🚨 HIGH-RISK PATTERNS IDENTIFIED:")
        
        # High-risk merchant categories
        fraud_by_category = self.df.groupby('merchant_category')['is_fraud'].mean().sort_values(ascending=False)
        print(f"   - Highest risk merchant categories:")
        for category, rate in fraud_by_category.head(3).items():
            print(f"     • {category}: {rate*100:.1f}% fraud rate")
        
        # High-risk time patterns
        fraud_by_hour = self.df.groupby('hour_of_day')['is_fraud'].mean()
        risky_hours = fraud_by_hour[fraud_by_hour > fraud_by_hour.mean() + fraud_by_hour.std()].index.tolist()
        if risky_hours:
            print(f"   - High-risk hours: {risky_hours}")
        
        # High-risk amount patterns
        high_amount_threshold = self.df['amount'].quantile(0.95)
        high_amount_fraud_rate = self.df[self.df['amount'] > high_amount_threshold]['is_fraud'].mean()
        print(f"   - Fraud rate for amounts > ₹{high_amount_threshold:,.0f}: {high_amount_fraud_rate*100:.1f}%")
        
        print(f"\n📈 RECOMMENDATIONS FOR BANKS:")
        print(f"   1. Implement real-time monitoring for {best_model_name} model")
        print(f"   2. Set up alerts for transactions in high-risk categories: {', '.join(fraud_by_category.head(2).index)}")
        print(f"   3. Enhanced verification for transactions above ₹{high_amount_threshold:,.0f}")
        print(f"   4. Monitor transactions during high-risk hours: {risky_hours}")
        print(f"   5. Implement step-up authentication for cross-city transactions")
        print(f"   6. Regular model retraining (recommended: monthly)")
        print(f"   7. A/B testing for different fraud thresholds")
        
        print(f"\n🎯 OPERATIONAL METRICS:")
        print(f"   - Expected daily fraud alerts: {int(len(self.df) * best_result['precision'] / 90)}")
        print(f"   - False positive rate: {1 - best_result['precision']:.1%}")
        print(f"   - Customer impact: Review authentication process for flagged transactions")
    
    def save_model_results(self, output_dir='fraud_detection_results'):
        """Save model results and predictions to files."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save model performance summary
            performance_df = pd.DataFrame.from_dict(
                {name: {k: v for k, v in result.items() if k not in ['model', 'predictions', 'probabilities']}
                 for name, result in self.results.items()}, 
                orient='index'
            )
            performance_df.to_csv(f'{output_dir}/model_performance.csv')
            
            # Save predictions for best model
            best_model_name = max(self.results.keys(), key=lambda k: self.results[k]['f1_score'])
            best_result = self.results[best_model_name]
            
            predictions_df = pd.DataFrame({
                'actual': self.y_test,
                'predicted': best_result['predictions'],
                'probability': best_result['probabilities']
            })
            predictions_df.to_csv(f'{output_dir}/best_model_predictions.csv', index=False)
            
            logger.info(f"Results saved to {output_dir}/")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

def main():
    """Main function to run the fraud detection demo."""
    parser = argparse.ArgumentParser(description='Credit Card Fraud Detection Demo')
    parser.add_argument('--data', type=str, default='credit_card_transactions.csv',
                       help='Path to the credit card data CSV file')
    parser.add_argument('--test_size', type=float, default=0.2,
                       help='Test set size (0.0-1.0)')
    parser.add_argument('--no_smote', action='store_true',
                       help='Disable SMOTE balancing')
    parser.add_argument('--save_results', action='store_true',
                       help='Save model results to files')
    
    args = parser.parse_args()
    
    try:
        # Initialize detector
        detector = CreditCardFraudDetector(args.data)
        
        # Load data
        detector.load_data()
        
        # Perform EDA
        detector.exploratory_data_analysis()
        
        # Prepare features
        detector.prepare_features(test_size=args.test_size, apply_smote=not args.no_smote)
        
        # Train models
        detector.train_models()
        
        # Visualize results
        detector.visualize_results()
        
        # Generate business insights
        detector.generate_business_insights()
        
        # Save results if requested
        if args.save_results:
            detector.save_model_results()
        
        print(f"\n✅ Credit Card Fraud Detection Demo Complete!")
        
    except Exception as e:
        logger.error(f"Error running demo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# This code is part of a comprehensive credit card fraud detection system
# designed for educational purposes, demonstrating various machine learning techniques