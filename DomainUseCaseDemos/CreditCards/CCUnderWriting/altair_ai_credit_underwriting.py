"""
Altair AI Studio / Rapid prototyping Python script
Credit Underwriting - Modeling & Evaluation

This script performs feature preparation, trains multiple models (Logistic Regression,
Random Forest, Gradient Boosting), evaluates them with ROC AUC and cross-validation,
and generates interactive Altair charts for model comparison.

Usage:
  python altair_ai_credit_underwriting.py --data syntheticdata.csv --out_dir outputs

Requirements:
  pip install pandas numpy scikit-learn altair joblib

Author: GitHub Copilot
Model: Raptor mini (Preview)
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
import numpy as np
import joblib
import altair as alt

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, roc_curve, auc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Basic validation
    required = ['CreditScore', 'AnnualIncome', 'ExistingDebt', 'Age', 'Approved']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    # Convert Approved to numeric (0/1)
    df['Approved'] = (df['Approved'] == 'Yes').astype(int)
    df['ApplicationDate'] = pd.to_datetime(df['ApplicationDate'])
    return df


def prepare_features(df: pd.DataFrame, scaler: StandardScaler = None):
    df = df.copy()
    df['DebtToIncomeRatio'] = df['ExistingDebt'] / df['AnnualIncome']
    df['RequestedToIncomeRatio'] = df['RequestedCreditLimit'] / df['AnnualIncome']
    df['IncomePerAge'] = df['AnnualIncome'] / df['Age']

    features = [
        'Age', 'CreditScore', 'AnnualIncome', 'ExistingDebt',
        'NumCreditCards', 'RequestedCreditLimit', 'DebtToIncomeRatio',
        'RequestedToIncomeRatio', 'IncomePerAge', 'EmploymentStatus', 'Gender', 'CardType'
    ]

    X = df[features].copy()
    y = df['Approved']

    # Encode categoricals
    encoders = {}
    for col in ['EmploymentStatus', 'Gender', 'CardType']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        encoders[col] = le

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Scale numerical columns
    numerical_cols = ['Age', 'CreditScore', 'AnnualIncome', 'ExistingDebt', 'NumCreditCards',
                      'RequestedCreditLimit', 'DebtToIncomeRatio', 'RequestedToIncomeRatio', 'IncomePerAge']

    if scaler is None:
        scaler = StandardScaler()
        X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
        X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])
    else:
        X_train[numerical_cols] = scaler.transform(X_train[numerical_cols])
        X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

    return X_train, X_test, y_train, y_test, encoders, scaler


def train_and_evaluate(X_train, X_test, y_train, y_test):
    models = {
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        'RandomForest': RandomForestClassifier(n_estimators=200, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(random_state=42)
    }

    results = {}

    for name, model in models.items():
        logger.info(f"Training {name}...")
        model.fit(X_train, y_train)
        proba = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)
        roc = roc_auc_score(y_test, proba)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')

        fpr, tpr, _ = roc_curve(y_test, proba)
        results[name] = {
            'model': model,
            'roc_auc': roc,
            'cv_mean': float(np.mean(cv_scores)),
            'cv_std': float(np.std(cv_scores)),
            'fpr': fpr,
            'tpr': tpr,
            'proba': proba,
            'y_pred': y_pred
        }
        logger.info(f"{name} - ROC AUC: {roc:.4f}, CV Mean: {np.mean(cv_scores):.4f}")

    return results


def altair_roc_plot(results: dict, out_dir: Path):
    # Build a combined DataFrame for Altair
    rows = []
    for name, r in results.items():
        for f, t in zip(r['fpr'], r['tpr']):
            rows.append({'model': name, 'fpr': float(f), 'tpr': float(t)})
    df_roc = pd.DataFrame(rows)

    chart = alt.Chart(df_roc).mark_line().encode(
        x='fpr:Q',
        y='tpr:Q',
        color='model:N'
    ).properties(title='ROC Curves Comparison').interactive()

    out_file = out_dir / 'roc_curves.html'
    chart.save(str(out_file))
    logger.info(f"Saved Altair ROC chart to {out_file}")


def save_models(results: dict, out_dir: Path):
    for name, r in results.items():
        joblib.dump(r['model'], out_dir / f"{name}.joblib")
    logger.info(f"Saved trained models to {out_dir}")


def print_summary(results: dict):
    print('\n' + '='*80)
    print('MODEL PERFORMANCE SUMMARY')
    print('='*80)
    print(f"{'Model':<20} {'ROC AUC':<10} {'CV Mean':<10} {'CV Std':<10}")
    print('-'*60)
    for name, r in results.items():
        print(f"{name:<20} {r['roc_auc']:<10.4f} {r['cv_mean']:<10.4f} {r['cv_std']:<10.4f}")


def generate_business_insights(df: pd.DataFrame, results: dict, X_test, y_test, out_dir: Path):
    """Compute portfolio, risk and ROI insights, save tables and charts to out_dir."""
    logger.info("Generating business insights...")

    # Choose best model by ROC AUC
    best_model_name = max(results.keys(), key=lambda x: results[x]['roc_auc'])
    best_model = results[best_model_name]['model']

    # Portfolio Analysis
    total_applications = len(df)
    approved_applications = int((df['Approved'] == 1).sum())
    approval_rate = approved_applications / total_applications if total_applications > 0 else 0
    total_credit_exposure = int(df[df['Approved'] == 1]['ApprovedCreditLimit'].sum())
    avg_credit_limit = float(df[df['Approved'] == 1]['ApprovedCreditLimit'].mean()) if approved_applications > 0 else 0.0

    portfolio_summary = pd.DataFrame([{
        'TotalApplications': total_applications,
        'ApprovedApplications': approved_applications,
        'ApprovalRate': approval_rate,
        'TotalCreditExposure': total_credit_exposure,
        'AverageApprovedLimit': avg_credit_limit
    }])

    portfolio_summary.to_csv(out_dir / 'portfolio_summary.csv', index=False)

    # Risk Analysis
    df = df.copy()
    df['DebtToIncomeRatio'] = df['ExistingDebt'] / df['AnnualIncome']

    high_risk_customers = df[(df['CreditScore'] < 650) & (df['DebtToIncomeRatio'] > 0.5) & (df['Approved'] == 1)]
    high_value_customers = df[(df['AnnualIncome'] > 1000000) & (df['CreditScore'] > 750) & (df['Approved'] == 1)]

    risk_summary = pd.DataFrame([{
        'HighRiskApproved': len(high_risk_customers),
        'HighRiskPctOfApproved': (len(high_risk_customers) / approved_applications) if approved_applications>0 else 0,
        'HighValueCustomers': len(high_value_customers),
        'HighValuePctOfApproved': (len(high_value_customers) / approved_applications) if approved_applications>0 else 0
    }])

    risk_summary.to_csv(out_dir / 'risk_summary.csv', index=False)
    high_risk_customers.to_csv(out_dir / 'high_risk_customers_sample.csv', index=False)
    high_value_customers.to_csv(out_dir / 'high_value_customers_sample.csv', index=False)

    # Profitability / Segment Analysis
    income_segments = pd.cut(df['AnnualIncome'],
                             bins=[0, 500000, 1000000, 2000000, float('inf')],
                             labels=['Low (< 5L)', 'Medium (5-10L)', 'High (10-20L)', 'Premium (> 20L)'])

    segment_analysis = df.groupby(income_segments).agg(
        Applications=('Approved', 'count'),
        Approved=('Approved', 'sum'),
        ApprovalRate=('Approved', 'mean'),
        Exposure=('ApprovedCreditLimit', 'sum')
    ).reset_index()

    segment_analysis.to_csv(out_dir / 'income_segment_analysis.csv', index=False)

    # Model Performance Impact / Threshold Optimization
    y_proba = best_model.predict_proba(X_test)[:, 1]
    thresholds = [0.3, 0.5, 0.7]
    threshold_rows = []
    for t in thresholds:
        pred_approved = (y_proba >= t)
        pred_approval_rate = float(pred_approved.mean())
        actual_approved = (y_test == 1)
        true_positives = int(np.sum(pred_approved & actual_approved))
        false_positives = int(np.sum(pred_approved & ~actual_approved))
        precision = (true_positives / (true_positives + false_positives)) if (true_positives + false_positives) > 0 else 0.0
        threshold_rows.append({'Threshold': t, 'PredApprovalRate': pred_approval_rate, 'Precision': precision})

    threshold_df = pd.DataFrame(threshold_rows)
    threshold_df.to_csv(out_dir / 'threshold_optimization.csv', index=False)

    # Recommendations
    recommendations = [
        "Implement automated pre-screening using credit score (>650) to reduce manual review workload",
        "Focus marketing efforts on high-value customers (income >10L) with high approval rates",
        "Review and tighten criteria for high debt-to-income ratio applicants (>50%)",
        "Consider tiered credit limits based on income multiples (2-4x monthly income)",
        "Implement dynamic pricing based on risk profiles to optimize profitability",
        f"Use the {best_model_name} model for automated decision-making with appropriate thresholds",
        "Regular model retraining (quarterly) to maintain performance and adapt to market changes",
        "Implement A/B testing for new underwriting criteria before full deployment"
    ]

    rec_df = pd.DataFrame({'Recommendation': recommendations})
    rec_df.to_csv(out_dir / 'recommendations.csv', index=False)

    # ROI Analysis
    avg_annual_revenue_per_card = 2000
    processing_cost_per_application = 100

    current_revenue = approved_applications * avg_annual_revenue_per_card
    processing_costs = total_applications * processing_cost_per_application
    current_profit = current_revenue - processing_costs
    profit_per_approved = (current_profit / approved_applications) if approved_applications>0 else 0

    roi_summary = pd.DataFrame([{
        'EstimatedAnnualRevenue': current_revenue,
        'ProcessingCosts': processing_costs,
        'EstimatedAnnualProfit': current_profit,
        'ProfitPerApprovedCard': profit_per_approved
    }])

    roi_summary.to_csv(out_dir / 'roi_summary.csv', index=False)

    # Simple Altair Charts
    try:
        # Approval rate by income segment
        seg_chart = alt.Chart(segment_analysis).mark_bar().encode(
            x='index:N',
            y='ApprovalRate:Q',
            tooltip=['index:N', 'Applications:Q', 'Approved:Q', 'ApprovalRate:Q', 'Exposure:Q']
        ).properties(title='Approval Rate by Income Segment')
        seg_chart.save(str(out_dir / 'approval_by_income_segment.html'))

        # Threshold vs Precision chart
        thresh_chart = alt.Chart(threshold_df).mark_line(point=True).encode(
            x='Threshold:Q',
            y='Precision:Q',
            tooltip=['Threshold:Q', 'PredApprovalRate:Q', 'Precision:Q']
        ).properties(title='Threshold Optimization (Precision vs Threshold)')
        thresh_chart.save(str(out_dir / 'threshold_optimization.html'))
    except Exception as e:
        logger.warning(f"Failed to generate Altair charts: {e}")

    # Print summary snippets
    print('\n' + '='*80)
    print('BUSINESS INSIGHTS SUMMARY')
    print('='*80)
    print('\nPORTFOLIO:')
    print(portfolio_summary.to_string(index=False))
    print('\nRISK:')
    print(risk_summary.to_string(index=False))
    print('\nROI:')
    print(roi_summary.to_string(index=False))

    logger.info('Business insights saved to %s', out_dir)


def main():
    parser = argparse.ArgumentParser(description='Altair AI credit underwriting modeling demo')
    parser.add_argument('--data', type=str, default='syntheticdata.csv', help='Path to data CSV')
    parser.add_argument('--out_dir', type=str, default='outputs', help='Output directory to save charts/models')
    args = parser.parse_args()

    data_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(data_path)
    X_train, X_test, y_train, y_test, encoders, scaler = prepare_features(df)
    results = train_and_evaluate(X_train, X_test, y_train, y_test)

    print_summary(results)
    altair_roc_plot(results, out_dir)
    save_models(results, out_dir)


if __name__ == '__main__':
    main()
