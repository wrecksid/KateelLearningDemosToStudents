"""
Credit Card Underwriting Demo
============================

This program demonstrates machine learning techniques for credit card underwriting
using synthetic data. It includes data analysis, model training, evaluation,
and business insights for management decision-making.

Author: AI Assistant for Finance Course
Date: July 2025
"""

# CLI options (use with `python cc_underwriting_demo.py [options]`):
# --data-file PATH        Path to CSV file (default: 'syntheticdata.csv')
# --data PATH             Alias for --data-file (also accepted by the script)
# --output-dir PATH       Directory to save outputs (default: 'outputs/')
# --models LIST           Comma-separated models to train: logistic,rf,gb,all (default: 'all')
# --test-size FLOAT       Test set fraction (default: 0.2)
# --random-seed INT       Random seed (default: 42)
# --no-plots              Skip generating plots
# --save-models           Save trained models to <output-dir>/models
# --demo / --full-demo    Run the complete demo end-to-end, printing progress and visualizations
# --verbose               Enable debug logging (overrides logging level)
# --help                  Show help and exit

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
import logging
import argparse
import sys
from datetime import datetime

# Configure warnings and logging
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure console stdout uses UTF-8 and provide a safe print fallback that replaces non-encodable characters
import builtins
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def _safe_print(*args, **kwargs):
    try:
        builtins.print(*args, **kwargs)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, 'encoding', None) or 'utf-8'
        safe_args = []
        for a in args:
            s = str(a)
            try:
                s.encode(encoding)
                safe_args.append(s)
            except UnicodeEncodeError:
                safe_args.append(s.encode(encoding, errors='replace').decode(encoding))
        builtins.print(*safe_args, **kwargs)

# Replace built-in print with the safe version so all prints fall back safely
builtins.print = _safe_print

class CreditCardUnderwritingDemo:
    """
    Demonstrates credit card underwriting using machine learning techniques.
    
    This class provides comprehensive analysis and modeling capabilities for
    credit card approval decisions, including data exploration, model training,
    evaluation, and business insights.
    """
    
    def __init__(self, data_file='syntheticdata.csv'):
        """
        Initialize the demo with data loading and preprocessing.
        
        Parameters:
        -----------
        data_file : str
            Path to the CSV data file
        """
        try:
            self.data_file = data_file
            self.df = None
            self.X_train = None
            self.X_test = None
            self.y_train = None
            self.y_test = None
            self.models = {}
            self.scaler = StandardScaler()
            self.label_encoders = {}
            
            self._load_data()
            logger.info("CreditCardUnderwritingDemo initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing demo: {e}")
            raise
    
    def _load_data(self):
        """Load and perform initial data validation."""
        try:
            self.df = pd.read_csv(self.data_file)
            logger.info(f"Loaded {len(self.df)} records from {self.data_file}")
            
            # Basic data validation
            required_columns = ['CreditScore', 'AnnualIncome', 'ExistingDebt', 'Age', 'Approved']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert data types
            self.df['ApplicationDate'] = pd.to_datetime(self.df['ApplicationDate'])
            self.df['Approved'] = (self.df['Approved'] == 'Yes').astype(int)
            
            logger.info("Data loaded and validated successfully")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def exploratory_data_analysis(self):
        """
        Perform comprehensive exploratory data analysis.
        
        This method generates various visualizations and statistics to understand
        the data distribution and relationships between variables.
        """
        try:
            logger.info("Starting exploratory data analysis...")
            
            # Set up the plotting style
            plt.style.use('seaborn-v0_8')
            fig = plt.figure(figsize=(20, 15))
            
            # 1. Approval rate overview
            plt.subplot(3, 4, 1)
            approval_counts = self.df['Approved'].value_counts()
            plt.pie([approval_counts[0], approval_counts[1]], labels=['Rejected', 'Approved'], 
                   autopct='%1.1f%%', startangle=90)
            plt.title('Credit Card Approval Rate')
            
            # 2. Credit score distribution
            plt.subplot(3, 4, 2)
            plt.hist(self.df['CreditScore'], bins=30, alpha=0.7, edgecolor='black')
            plt.xlabel('Credit Score')
            plt.ylabel('Frequency')
            plt.title('Credit Score Distribution')
            
            # 3. Income distribution
            plt.subplot(3, 4, 3)
            plt.hist(self.df['AnnualIncome']/100000, bins=30, alpha=0.7, edgecolor='black')
            plt.xlabel('Annual Income (Lakhs)')
            plt.ylabel('Frequency')
            plt.title('Annual Income Distribution')
            
            # 4. Age distribution
            plt.subplot(3, 4, 4)
            plt.hist(self.df['Age'], bins=20, alpha=0.7, edgecolor='black')
            plt.xlabel('Age')
            plt.ylabel('Frequency')
            plt.title('Age Distribution')
            
            # 5. Approval rate by credit score ranges
            plt.subplot(3, 4, 5)
            score_bins = pd.cut(self.df['CreditScore'], bins=5)
            approval_by_score = self.df.groupby(score_bins)['Approved'].mean()
            approval_by_score.plot(kind='bar', rot=45)
            plt.xlabel('Credit Score Range')
            plt.ylabel('Approval Rate')
            plt.title('Approval Rate by Credit Score')
            
            # 6. Approval rate by income ranges
            plt.subplot(3, 4, 6)
            income_bins = pd.cut(self.df['AnnualIncome'], bins=5)
            approval_by_income = self.df.groupby(income_bins)['Approved'].mean()
            approval_by_income.plot(kind='bar', rot=45)
            plt.xlabel('Income Range')
            plt.ylabel('Approval Rate')
            plt.title('Approval Rate by Income')
            
            # 7. Debt to income ratio analysis
            plt.subplot(3, 4, 7)
            self.df['DebtToIncomeRatio'] = self.df['ExistingDebt'] / self.df['AnnualIncome']
            dti_bins = pd.cut(self.df['DebtToIncomeRatio'], bins=5)
            approval_by_dti = self.df.groupby(dti_bins)['Approved'].mean()
            approval_by_dti.plot(kind='bar', rot=45)
            plt.xlabel('Debt-to-Income Ratio')
            plt.ylabel('Approval Rate')
            plt.title('Approval Rate by DTI Ratio')
            
            # 8. Employment status analysis
            plt.subplot(3, 4, 8)
            emp_approval = self.df.groupby('EmploymentStatus')['Approved'].mean()
            emp_approval.plot(kind='bar', rot=45)
            plt.xlabel('Employment Status')
            plt.ylabel('Approval Rate')
            plt.title('Approval Rate by Employment')
            
            # 9. Correlation heatmap
            plt.subplot(3, 4, 9)
            numeric_cols = ['Age', 'AnnualIncome', 'CreditScore', 'ExistingDebt', 
                          'NumCreditCards', 'RequestedCreditLimit', 'Approved']
            correlation_matrix = self.df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Feature Correlation Matrix')
            
            # 10. Approved credit limit distribution
            plt.subplot(3, 4, 10)
            approved_df = self.df[self.df['Approved'] == 1]
            plt.hist(approved_df['ApprovedCreditLimit']/1000, bins=30, alpha=0.7, edgecolor='black')
            plt.xlabel('Approved Credit Limit (Thousands)')
            plt.ylabel('Frequency')
            plt.title('Approved Credit Limit Distribution')
            
            # 11. Monthly trend of applications
            plt.subplot(3, 4, 11)
            monthly_apps = self.df.groupby(self.df['ApplicationDate'].dt.to_period('M')).size()
            monthly_apps.plot()
            plt.xlabel('Month')
            plt.ylabel('Number of Applications')
            plt.title('Monthly Application Trend')
            plt.xticks(rotation=45)
            
            # 12. Card type preference
            plt.subplot(3, 4, 12)
            card_type_counts = self.df['CardType'].value_counts()
            card_type_counts.plot(kind='bar')
            plt.xlabel('Card Type')
            plt.ylabel('Number of Applications')
            plt.title('Card Type Preferences')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.show()
            
            # Print summary statistics
            print("\n" + "="*60)
            print("EXPLORATORY DATA ANALYSIS SUMMARY")
            print("="*60)
            
            print(f"\n1. BASIC STATISTICS:")
            print(f"   Total Applications: {len(self.df):,}")
            print(f"   Approved Applications: {self.df['Approved'].sum():,}")
            print(f"   Overall Approval Rate: {self.df['Approved'].mean():.2%}")
            
            print(f"\n2. CREDIT SCORE INSIGHTS:")
            print(f"   Average Credit Score: {self.df['CreditScore'].mean():.0f}")
            print(f"   Credit Score Range: {self.df['CreditScore'].min()} - {self.df['CreditScore'].max()}")
            
            print(f"\n3. INCOME INSIGHTS:")
            print(f"   Average Annual Income: ₹{self.df['AnnualIncome'].mean():,.0f}")
            print(f"   Median Annual Income: ₹{self.df['AnnualIncome'].median():,.0f}")
            
            print(f"\n4. RISK INDICATORS:")
            avg_dti = self.df['DebtToIncomeRatio'].mean()
            print(f"   Average Debt-to-Income Ratio: {avg_dti:.2%}")
            high_risk_pct = (self.df['DebtToIncomeRatio'] > 0.5).mean()
            print(f"   High Risk Applicants (DTI > 50%): {high_risk_pct:.2%}")
            
            logger.info("Exploratory data analysis completed")
            
        except Exception as e:
            logger.error(f"Error in exploratory data analysis: {e}")
            raise
    
    def prepare_features(self):
        """
        Prepare features for machine learning models.
        
        This method handles feature engineering, encoding categorical variables,
        and splitting data into training and testing sets.
        """
        try:
            logger.info("Preparing features for modeling...")
            
            # Create feature engineering
            self.df['DebtToIncomeRatio'] = self.df['ExistingDebt'] / self.df['AnnualIncome']
            self.df['RequestedToIncomeRatio'] = self.df['RequestedCreditLimit'] / self.df['AnnualIncome']
            self.df['IncomePerAge'] = self.df['AnnualIncome'] / self.df['Age']
            
            # Select features for modeling
            feature_columns = [
                'Age', 'CreditScore', 'AnnualIncome', 'ExistingDebt', 
                'NumCreditCards', 'RequestedCreditLimit', 'DebtToIncomeRatio',
                'RequestedToIncomeRatio', 'IncomePerAge', 'EmploymentStatus', 
                'Gender', 'CardType'
            ]
            
            # Persist feature column order for prediction consistency
            self.feature_columns = feature_columns
            
            X = self.df[self.feature_columns].copy()
            y = self.df['Approved']
            
            # Encode categorical variables
            categorical_columns = ['EmploymentStatus', 'Gender', 'CardType']
            
            for col in categorical_columns:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
                self.label_encoders[col] = le
            
            # Split the data
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale numerical features
            numerical_columns = ['Age', 'CreditScore', 'AnnualIncome', 'ExistingDebt', 
                               'NumCreditCards', 'RequestedCreditLimit', 'DebtToIncomeRatio',
                               'RequestedToIncomeRatio', 'IncomePerAge']
            
            self.X_train[numerical_columns] = self.scaler.fit_transform(self.X_train[numerical_columns])
            self.X_test[numerical_columns] = self.scaler.transform(self.X_test[numerical_columns])
            
            logger.info(f"Features prepared: {len(feature_columns)} features")
            logger.info(f"Training set: {len(self.X_train)} samples")
            logger.info(f"Test set: {len(self.X_test)} samples")
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            raise
    
    def train_models(self):
        """
        Train multiple machine learning models for credit card underwriting.
        
        This method trains and compares different algorithms to find the best
        performing model for credit approval prediction.
        """
        try:
            logger.info("Training machine learning models...")
            
            # Define models to train
            models_to_train = {
                'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
                'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
                'Gradient Boosting': GradientBoostingClassifier(random_state=42)
            }
            
            # Train and evaluate each model
            results = {}
            
            for name, model in models_to_train.items():
                logger.info(f"Training {name}...")
                
                # Train the model
                model.fit(self.X_train, self.y_train)
                
                # Make predictions
                y_pred = model.predict(self.X_test)
                y_pred_proba = model.predict_proba(self.X_test)[:, 1]
                
                # Calculate metrics
                roc_auc = roc_auc_score(self.y_test, y_pred_proba)
                cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='roc_auc')
                
                # Store results
                results[name] = {
                    'model': model,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba,
                    'roc_auc': roc_auc,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std()
                }
                
                self.models[name] = model
                
                logger.info(f"{name} - ROC AUC: {roc_auc:.4f}, CV Score: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
            
            # Display results comparison
            print("\n" + "="*80)
            print("MODEL PERFORMANCE COMPARISON")
            print("="*80)
            
            print(f"{'Model':<20} {'ROC AUC':<10} {'CV Mean':<12} {'CV Std':<10}")
            print("-" * 52)
            
            for name, result in results.items():
                print(f"{name:<20} {result['roc_auc']:<10.4f} {result['cv_mean']:<12.4f} {result['cv_std']:<10.4f}")
            
            # Find best model
            best_model_name = max(results.keys(), key=lambda x: results[x]['roc_auc'])
            self.best_model = results[best_model_name]['model']
            self.best_model_name = best_model_name
            
            print(f"\nBest Model: {best_model_name}")
            
            # Plot model comparison
            self._plot_model_comparison(results)
            
            logger.info("Model training completed")
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            raise
    
    def _plot_model_comparison(self, results):
        """Plot model performance comparison."""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # ROC Curves
            ax1.plot([0, 1], [0, 1], 'k--', alpha=0.6)
            for name, result in results.items():
                fpr, tpr, _ = roc_curve(self.y_test, result['probabilities'])
                ax1.plot(fpr, tpr, label=f"{name} (AUC = {result['roc_auc']:.3f})")
            
            ax1.set_xlabel('False Positive Rate')
            ax1.set_ylabel('True Positive Rate')
            ax1.set_title('ROC Curves Comparison')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Model Performance Bar Chart
            model_names = list(results.keys())
            roc_scores = [results[name]['roc_auc'] for name in model_names]
            
            bars = ax2.bar(model_names, roc_scores, alpha=0.7)
            ax2.set_ylabel('ROC AUC Score')
            ax2.set_title('Model Performance Comparison')
            ax2.set_ylim(0.5, 1.0)
            
            # Add value labels on bars
            for bar, score in zip(bars, roc_scores):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{score:.3f}', ha='center', va='bottom')
            
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            
            # Confusion Matrix for Best Model
            best_result = results[self.best_model_name]
            cm = confusion_matrix(self.y_test, best_result['predictions'])
            
            sns.heatmap(cm, annot=True, fmt='d', ax=ax3, cmap='Blues',
                       xticklabels=['Rejected', 'Approved'],
                       yticklabels=['Rejected', 'Approved'])
            ax3.set_xlabel('Predicted')
            ax3.set_ylabel('Actual')
            ax3.set_title(f'Confusion Matrix - {self.best_model_name}')
            
            # Feature Importance (for tree-based models)
            if hasattr(self.best_model, 'feature_importances_'):
                feature_names = self.X_train.columns
                importances = self.best_model.feature_importances_
                indices = np.argsort(importances)[::-1][:10]  # Top 10 features
                
                ax4.bar(range(len(indices)), importances[indices])
                ax4.set_xlabel('Features')
                ax4.set_ylabel('Importance')
                ax4.set_title(f'Top 10 Feature Importances - {self.best_model_name}')
                ax4.set_xticks(range(len(indices)))
                ax4.set_xticklabels([feature_names[i] for i in indices], rotation=45, ha='right')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            logger.error(f"Error plotting model comparison: {e}")
            raise
    
    def business_insights(self):
        """
        Generate business insights and recommendations for management.
        
        This method provides actionable insights that can be used for
        business decision-making in credit card underwriting.
        """
        try:
            logger.info("Generating business insights...")
            
            print("\n" + "="*80)
            print("BUSINESS INSIGHTS FOR CREDIT CARD UNDERWRITING")
            print("="*80)
            
            # 1. Portfolio Analysis
            print("\n1. PORTFOLIO ANALYSIS:")
            print("-" * 25)
            
            total_applications = len(self.df)
            approved_applications = self.df['Approved'].sum()
            approval_rate = approved_applications / total_applications
            
            total_credit_exposure = self.df[self.df['Approved'] == 1]['ApprovedCreditLimit'].sum()
            avg_credit_limit = self.df[self.df['Approved'] == 1]['ApprovedCreditLimit'].mean()
            
            print(f"   • Total Applications Processed: {total_applications:,}")
            print(f"   • Applications Approved: {approved_applications:,}")
            print(f"   • Overall Approval Rate: {approval_rate:.2%}")
            print(f"   • Total Credit Exposure: ₹{total_credit_exposure:,.0f}")
            print(f"   • Average Credit Limit: ₹{avg_credit_limit:,.0f}")
            
            # 2. Risk Analysis
            print("\n2. RISK ANALYSIS:")
            print("-" * 20)
            
            high_risk_customers = self.df[
                (self.df['CreditScore'] < 650) & 
                (self.df['DebtToIncomeRatio'] > 0.5) & 
                (self.df['Approved'] == 1)
            ]
            
            high_value_customers = self.df[
                (self.df['AnnualIncome'] > 1000000) & 
                (self.df['CreditScore'] > 750) & 
                (self.df['Approved'] == 1)
            ]
            
            print(f"   • High-Risk Approved Customers: {len(high_risk_customers)} ({len(high_risk_customers)/approved_applications:.1%})")
            print(f"   • High-Value Customers: {len(high_value_customers)} ({len(high_value_customers)/approved_applications:.1%})")
            
            # 3. Profitability Insights
            print("\n3. PROFITABILITY INSIGHTS:")
            print("-" * 30)
            
            # Segment analysis by income
            income_segments = pd.cut(self.df['AnnualIncome'], 
                                   bins=[0, 500000, 1000000, 2000000, float('inf')],
                                   labels=['Low (< 5L)', 'Medium (5-10L)', 'High (10-20L)', 'Premium (> 20L)'])
            
            segment_analysis = self.df.groupby(income_segments).agg({
                'Approved': ['count', 'sum', 'mean'],
                'ApprovedCreditLimit': 'sum'
            }).round(3)
            
            print("   Income Segment Analysis:")
            for segment in segment_analysis.index:
                apps = segment_analysis.loc[segment, ('Approved', 'count')]
                approved = segment_analysis.loc[segment, ('Approved', 'sum')]
                rate = segment_analysis.loc[segment, ('Approved', 'mean')]
                exposure = segment_analysis.loc[segment, ('ApprovedCreditLimit', 'sum')]
                
                print(f"     {segment}: {apps:,} apps, {rate:.1%} approval, ₹{exposure:,.0f} exposure")
            
            # 4. Model Performance Impact
            print("\n4. MODEL PERFORMANCE IMPACT:")
            print("-" * 35)
            
            if hasattr(self, 'best_model'):
                # Calculate potential improvements
                current_approval_rate = self.df['Approved'].mean()
                
                # Simulate model-based decisions
                y_pred_proba = self.best_model.predict_proba(self.X_test)[:, 1]
                
                # Different threshold scenarios
                thresholds = [0.3, 0.5, 0.7]
                
                print("   Threshold Optimization Analysis:")
                for threshold in thresholds:
                    pred_approved = (y_pred_proba >= threshold)
                    pred_approval_rate = pred_approved.mean()
                    
                    # Calculate metrics on test set
                    actual_approved = (self.y_test == 1)
                    true_positives = np.sum(pred_approved & actual_approved)
                    false_positives = np.sum(pred_approved & ~actual_approved)
                    
                    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
                    
                    print(f"     Threshold {threshold}: {pred_approval_rate:.1%} approval rate, {precision:.1%} precision")
            
            # 5. Recommendations
            print("\n5. MANAGEMENT RECOMMENDATIONS:")
            print("-" * 35)
            
            recommendations = [
                "• Implement automated pre-screening using credit score (>650) to reduce manual review workload",
                "• Focus marketing efforts on high-value customers (income >10L) with approval rates >80%",
                "• Review and tighten criteria for high debt-to-income ratio applicants (>50%)",
                "• Consider tiered credit limits based on income multiples (2-4x monthly income)",
                "• Implement dynamic pricing based on risk profiles to optimize profitability",
                f"• Use the {self.best_model_name} model for automated decision-making with appropriate thresholds",
                "• Regular model retraining (quarterly) to maintain performance and adapt to market changes",
                "• Implement A/B testing for new underwriting criteria before full deployment"
            ]
            
            for rec in recommendations:
                print(f"   {rec}")
            
            # 6. ROI Analysis
            print("\n6. ESTIMATED ROI IMPACT:")
            print("-" * 28)
            
            # Simplified ROI calculation
            avg_annual_revenue_per_card = 2000  # Assumption: ₹2000 per card per year
            processing_cost_per_application = 100  # Assumption: ₹100 per application
            
            current_revenue = approved_applications * avg_annual_revenue_per_card
            processing_costs = total_applications * processing_cost_per_application
            current_profit = current_revenue - processing_costs
            
            print(f"   • Estimated Annual Revenue: ₹{current_revenue:,.0f}")
            print(f"   • Processing Costs: ₹{processing_costs:,.0f}")
            print(f"   • Estimated Annual Profit: ₹{current_profit:,.0f}")
            print(f"   • Profit per Approved Card: ₹{current_profit/approved_applications:,.0f}")
            
            logger.info("Business insights generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating business insights: {e}")
            raise
    
    def predict_new_application(self, customer_data):
        """
        Predict approval for a new credit card application.
        
        Parameters:
        -----------
        customer_data : dict
            Dictionary containing customer information
            
        Returns:
        --------
        dict
            Prediction results with probability and recommended limit
        """
        try:
            if not hasattr(self, 'best_model'):
                raise ValueError("Models not trained yet. Please run train_models() first.")
            
            # Convert input to DataFrame
            input_df = pd.DataFrame([customer_data]).copy()
            
            # Feature engineering (safe defaults if keys missing)
            input_df['DebtToIncomeRatio'] = input_df.get('ExistingDebt', 0) / input_df.get('AnnualIncome', 1)
            input_df['RequestedToIncomeRatio'] = input_df.get('RequestedCreditLimit', 0) / input_df.get('AnnualIncome', 1)
            input_df['IncomePerAge'] = input_df.get('AnnualIncome', 0) / input_df.get('Age', 1)
            
            # Ensure all expected feature columns exist and fill missing values with sensible defaults
            if hasattr(self, 'feature_columns'):
                for col in self.feature_columns:
                    if col not in input_df.columns:
                        if col in self.label_encoders:  # categorical -> use mode
                            input_df[col] = self.df[col].mode()[0]
                        else:  # numerical -> use median
                            input_df[col] = self.df[col].median()
            
            # Encode categorical variables with safe handling for unseen categories
            for col, encoder in self.label_encoders.items():
                if col in input_df.columns:
                    val = input_df.at[0, col]
                    if val in encoder.classes_:
                        input_df[col] = encoder.transform(input_df[col])
                    else:
                        logger.warning(f"Unseen category '{val}' for '{col}'; using mode '{encoder.classes_[0]}'")
                        input_df[col] = encoder.transform([encoder.classes_[0]])
            
            # Scale numerical features (ensure columns exist)
            numerical_columns = ['Age', 'CreditScore', 'AnnualIncome', 'ExistingDebt', 
                               'NumCreditCards', 'RequestedCreditLimit', 'DebtToIncomeRatio',
                               'RequestedToIncomeRatio', 'IncomePerAge']
            for col in numerical_columns:
                if col not in input_df.columns:
                    input_df[col] = self.df[col].median()
            input_df[numerical_columns] = self.scaler.transform(input_df[numerical_columns])
            
            # Reindex to the same feature column order used in training
            if hasattr(self, 'feature_columns'):
                input_df = input_df[self.feature_columns]
            else:
                logger.warning("Feature column order not found; proceeding with inferred order")
            
            # Make prediction
            approval_probability = self.best_model.predict_proba(input_df)[0, 1]
            approval_decision = approval_probability >= 0.5
            
            # Calculate recommended credit limit
            if approval_decision:
                monthly_income = customer_data['AnnualIncome'] / 12
                if customer_data['CreditScore'] >= 750:
                    recommended_limit = int(monthly_income * 4)
                elif customer_data['CreditScore'] >= 700:
                    recommended_limit = int(monthly_income * 3)
                elif customer_data['CreditScore'] >= 650:
                    recommended_limit = int(monthly_income * 2.5)
                else:
                    recommended_limit = int(monthly_income * 2)
                
                # Cap at requested amount
                recommended_limit = min(recommended_limit, customer_data['RequestedCreditLimit'])
            else:
                recommended_limit = 0
            
            return {
                'approval_decision': 'Approved' if approval_decision else 'Rejected',
                'approval_probability': approval_probability,
                'recommended_credit_limit': recommended_limit,
                'risk_level': 'Low' if approval_probability > 0.8 else 'Medium' if approval_probability > 0.5 else 'High'
            }
            
        except Exception as e:
            logger.error(f"Error predicting new application: {e}")
            raise
    
    def run_complete_demo(self):
        """Run the complete demonstration workflow."""
        try:
            print("\n" + "="*80)
            print("CREDIT CARD UNDERWRITING MACHINE LEARNING DEMO")
            print("="*80)
            
            # Step 1: Exploratory Data Analysis
            print("\nStep 1: Performing Exploratory Data Analysis...")
            self.exploratory_data_analysis()
            
            # Step 2: Feature Preparation
            print("\nStep 2: Preparing Features for Machine Learning...")
            self.prepare_features()
            
            # Step 3: Model Training
            print("\nStep 3: Training Machine Learning Models...")
            self.train_models()
            
            # Step 4: Business Insights
            print("\nStep 4: Generating Business Insights...")
            self.business_insights()
            
            # Step 5: Sample Prediction
            print("\nStep 5: Sample Prediction Example...")
            sample_customer = {
                'Age': 35,
                'CreditScore': 720,
                'AnnualIncome': 800000,
                'ExistingDebt': 200000,
                'NumCreditCards': 2,
                'RequestedCreditLimit': 100000,
                'EmploymentStatus': 'Salaried',
                'Gender': 'M',
                'CardType': 'Gold'
            }
            
            prediction = self.predict_new_application(sample_customer)
            
            print(f"\nSample Customer Profile:")
            for key, value in sample_customer.items():
                print(f"   {key}: {value}")
            
            print(f"\nPrediction Results:")
            print(f"   Decision: {prediction['approval_decision']}")
            print(f"   Probability: {prediction['approval_probability']:.2%}")
            print(f"   Recommended Limit: ₹{prediction['recommended_credit_limit']:,}")
            print(f"   Risk Level: {prediction['risk_level']}")
            
            print("\n" + "="*80)
            print("DEMO COMPLETED SUCCESSFULLY!")
            print("="*80)
            
        except Exception as e:
            logger.error(f"Error running complete demo: {e}")
            raise


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Credit Card Underwriting ML Demo')
    parser.add_argument('--data', '--data-file', type=str, default='syntheticdata.csv', help='Path to data file')
    parser.add_argument('--demo', action='store_true', help='Run complete demo (short alias)')
    parser.add_argument('--full-demo', dest='demo', action='store_true', help='Alias for --demo: Run the complete demo end-to-end, printing progress and visualizations')
    
    args = parser.parse_args()
    
    try:
        demo = CreditCardUnderwritingDemo(args.data)
        
        if args.demo:
            demo.run_complete_demo()
        else:
            # Interactive mode
            print("Credit Card Underwriting Demo initialized.")
            print("Available methods:")
            print("- demo.exploratory_data_analysis()")
            print("- demo.prepare_features()")
            print("- demo.train_models()")
            print("- demo.business_insights()")
            print("- demo.run_complete_demo()")
            print("\nRun with --demo or --full-demo to execute the full end-to-end demo and generate outputs.")
            
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
