"""
Credit Card Customer Lifetime Value Analysis
===========================================

This program demonstrates Customer Lifetime Value (CLV) analysis for credit card customers.
It includes various CLV models, customer segmentation, and actionable insights for
bank management decisions.

Author: AI Assistant for Financial Analytics Course
Date: July 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
import logging
import argparse
import sys
import os

# Configure plotting and warnings
plt.style.use('seaborn-v0_8')
warnings.filterwarnings('ignore')
sns.set_palette("husl")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CLVAnalyzer:
    """Customer Lifetime Value Analyzer for Credit Card Customers"""
    
    def __init__(self, data_file='syntheticdata.csv'):
        """
        Initialize the CLV Analyzer
        
        Parameters:
        -----------
        data_file : str
            Path to the synthetic data CSV file
        """
        self.data_file = data_file
        self.df = None
        self.clv_df = None
        self.segments = None
        self.models = {}
        
    def load_data(self):
        """Load and validate the synthetic data"""
        try:
            # If the provided path does not exist, try resolving common alternative locations
            if not os.path.exists(self.data_file):
                # 1) same folder as this script
                alt1 = os.path.join(os.path.dirname(__file__), os.path.basename(self.data_file))
                # 2) attempt a limited search for the filename to avoid scanning entire repo
                alt2 = None
                try:
                    filename = os.path.basename(self.data_file)
                    max_depth = 3
                    found = None
                    for root_dir, dirs, files in os.walk('.', topdown=True):
                        # compute depth relative to current directory
                        depth = root_dir.count(os.sep)
                        if depth > max_depth:
                            # prevent descending into very deep folders
                            dirs.clear()
                            continue
                        if filename in files:
                            found = os.path.join(root_dir, filename)
                            break
                    alt2 = found
                except Exception:
                    alt2 = None

                candidates = [alt for alt in (alt1, alt2) if alt and os.path.exists(alt)]
                if candidates:
                    self.data_file = candidates[0]
                    logger.info(f"Resolved data file to: {self.data_file}")
                else:
                    raise FileNotFoundError(f"Data file {self.data_file} not found. Please run generate_synthetic_data.py first.")

            self.df = pd.read_csv(self.data_file)
            logger.info(f"Loaded data with {len(self.df)} records and {len(self.df.columns)} features")
            
            # Validate required columns
            required_cols = ['customer_id', 'monthly_revenue', 'monthly_cost', 'tenure_months', 'is_active']
            missing_cols = [col for col in required_cols if col not in self.df.columns]
            
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Convert date columns
            date_cols = ['last_transaction_date', 'account_opening_date']
            for col in date_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_datetime(self.df[col])
            
            logger.info("✅ Data loaded and validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def calculate_clv_metrics(self, discount_rate=0.1, prediction_months=36):
        """
        Calculate Customer Lifetime Value using multiple approaches
        
        Parameters:
        -----------
        discount_rate : float
            Monthly discount rate for NPV calculation (default: 0.1/12)
        prediction_months : int
            Number of months to predict CLV for (default: 36)
        """
        try:
            logger.info(f"Calculating CLV metrics with {prediction_months} months prediction period")
            
            # Convert annual discount rate to monthly
            monthly_discount_rate = discount_rate / 12
            
            # 1. Historical CLV (based on tenure)
            self.df['historical_clv'] = self.df['monthly_profit'] * self.df['tenure_months']
            
            # 2. Simple CLV (current monthly profit * predicted lifetime)
            # Estimate customer lifetime based on churn probability
            self.df['churn_probability'] = self.estimate_churn_probability()
            self.df['estimated_lifetime_months'] = 1 / (self.df['churn_probability'] + 0.001)  # Avoid division by zero
            self.df['estimated_lifetime_months'] = np.clip(self.df['estimated_lifetime_months'], 1, 120)
            
            self.df['simple_clv'] = self.df['monthly_profit'] * self.df['estimated_lifetime_months']
            
            # 3. NPV-based CLV
            self.df['npv_clv'] = self.calculate_npv_clv(monthly_discount_rate, prediction_months)
            
            # 4. Predictive CLV using features
            self.df['predictive_clv'] = self.calculate_predictive_clv()
            
            # Create CLV summary dataframe
            # Include key metrics and supporting features required for segmentation and reporting
            clv_columns = ['customer_id', 'historical_clv', 'simple_clv', 'npv_clv', 'predictive_clv',
                          'monthly_profit', 'avg_monthly_spend', 'tenure_months', 'is_active', 'churn_probability']
            self.clv_df = self.df[clv_columns].copy()
            
            logger.info("✅ CLV metrics calculated successfully")
            
        except Exception as e:
            logger.error(f"Error calculating CLV metrics: {str(e)}")
            raise
    
    def estimate_churn_probability(self):
        """Estimate churn probability based on customer characteristics"""
        # Simple heuristic-based churn probability
        churn_prob = 0.1  # Base churn rate
        
        # Increase churn probability based on risk factors
        churn_factors = (
            (self.df['utilization_rate'] > 0.9) * 0.3 +  # High utilization
            (self.df['late_payments_12m'] > 6) * 0.4 +    # Frequent late payments
            (self.df['payment_ratio'] < 0.2) * 0.2 +      # Low payment ratio
            (self.df['monthly_profit'] <= 0) * 0.5 +      # Unprofitable customers
            (~self.df['is_active']) * 0.8                 # Inactive customers
        )
        
        churn_probability = np.clip(churn_prob + churn_factors, 0.01, 0.95)
        return churn_probability
    
    def calculate_npv_clv(self, discount_rate, prediction_months):
        """Calculate NPV-based CLV"""
        # Ensure arrays are numeric and handle NaNs
        monthly_cashflows = self.df['monthly_profit'].fillna(0).astype(float).values  # shape (n_customers,)
        churn = self.df['churn_probability'].fillna(0.0).astype(float).values  # shape (n_customers,)

        # months array
        months = np.arange(1, prediction_months + 1)  # shape (prediction_months,)

        # survival_rates: shape (prediction_months, n_customers)
        survival_rates = (1 - churn)[None, :] ** months[:, None]

        # discount_factors: shape (prediction_months, 1)
        discount_factors = (1 + discount_rate) ** (-months)[:, None]

        # Calculate NPV for each customer (sum over months)
        npv_clv = np.sum(monthly_cashflows[None, :] * survival_rates * discount_factors, axis=0)

        return npv_clv
    
    def calculate_predictive_clv(self):
        """Calculate predictive CLV using machine learning"""
        try:
            # Features for CLV prediction
            feature_cols = ['age', 'annual_income', 'tenure_months', 'credit_limit', 'avg_monthly_spend',
                           'utilization_rate', 'payment_ratio', 'late_payments_12m', 'monthly_revenue']
            
            # Prepare features
            X = self.df[feature_cols].copy()
            
            # Handle categorical variables
            if 'card_type' in self.df.columns:
                card_type_dummies = pd.get_dummies(self.df['card_type'], prefix='card_type')
                X = pd.concat([X, card_type_dummies], axis=1)
            
            # Target variable (using simple CLV as proxy)
            y = self.df['monthly_profit'] * 24  # 2 years as baseline
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train Random Forest model
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X_train, y_train)
            
            # Store model for later use
            self.models['clv_predictor'] = rf_model
            
            # Predict CLV for all customers
            predictive_clv = rf_model.predict(X)
            
            # Evaluate model
            y_pred_test = rf_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred_test)
            r2 = r2_score(y_test, y_pred_test)
            
            logger.info(f"CLV Prediction Model - MSE: {mse:.2f}, R²: {r2:.3f}")
            
            return predictive_clv
            
        except Exception as e:
            logger.error(f"Error in predictive CLV calculation: {str(e)}")
            # Return simple CLV as fallback
            return self.df['monthly_profit'] * 24
    
    def perform_customer_segmentation(self, n_segments=5):
        """Perform customer segmentation based on CLV and other factors"""
        try:
            logger.info(f"Performing customer segmentation into {n_segments} segments")
            
            # Features for segmentation
            segmentation_features = ['simple_clv', 'monthly_profit', 'avg_monthly_spend', 
                                   'tenure_months', 'churn_probability']
            
            # Prepare data for clustering
            X_segment = self.clv_df[segmentation_features].copy()
            
            # Standardize features
            logger.info('Segmentation: checking feature completeness and NaNs')
            missing_counts = X_segment.isna().sum()
            logger.info(f'Missing values by feature:\n{missing_counts.to_dict()}')

            # Fill small number of missing values (if any) with column median
            if X_segment.isna().any().any():
                logger.info('Filling missing values in segmentation features with column medians')
                X_segment = X_segment.fillna(X_segment.median())

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_segment)

            # Perform K-means clustering
            try:
                kmeans = KMeans(n_clusters=n_segments, random_state=42, n_init=10)
                segments = kmeans.fit_predict(X_scaled)
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                logger.error(f'KMeans fit_predict failed: {e}\n{tb}')
                raise

            # Add segments to dataframe
            self.clv_df['segment'] = segments

            # Create segment labels based on characteristics
            segment_summary = self.clv_df.groupby('segment').agg({
                'simple_clv': 'mean',
                'monthly_profit': 'mean',
                'churn_probability': 'mean',
                'customer_id': 'count'
            }).round(2)
            
            segment_summary.columns = ['avg_clv', 'avg_monthly_profit', 'avg_churn_prob', 'customer_count']
            logger.info(f"Segment summary computed for {len(segment_summary)} segments")

            # Safe assignment of meaningful names to segments
            segment_names = {}
            try:
                if 'avg_clv' in segment_summary.columns:
                    segment_names[segment_summary['avg_clv'].idxmax()] = 'Champions'
                if 'avg_monthly_profit' in segment_summary.columns:
                    segment_names[segment_summary['avg_monthly_profit'].idxmax()] = 'High Value'
                if 'avg_churn_prob' in segment_summary.columns:
                    segment_names[segment_summary['avg_churn_prob'].idxmax()] = 'At Risk'

                counts_sorted = segment_summary['customer_count'].sort_values()
                if len(counts_sorted) >= 2:
                    loyal_idx = counts_sorted.index[-2]
                    potential_idx = counts_sorted.index[-1]
                    segment_names[loyal_idx] = 'Loyal Customers'
                    segment_names[potential_idx] = 'Potential Loyalists'
                elif len(counts_sorted) == 1:
                    only_idx = counts_sorted.index[0]
                    segment_names[only_idx] = 'Loyal Customers'
            except Exception as inner_e:
                logger.warning(f"Could not assign some segment names automatically: {inner_e}")

            # Ensure all segments have names (fill defaults)
            for seg in segment_summary.index:
                if seg not in segment_names:
                    segment_names[seg] = f'Segment_{int(seg)+1}'

            self.clv_df['segment_name'] = self.clv_df['segment'].map(segment_names)
            self.segments = segment_summary

            logger.info("✅ Customer segmentation completed")

        except Exception as e:
            logger.error(f"Error in customer segmentation: {e}")
            # Remove partial segmentation to keep pipeline consistent
            self.segments = None
            if 'segment' in self.clv_df.columns:
                del self.clv_df['segment']
            if 'segment_name' in self.clv_df.columns:
                del self.clv_df['segment_name']
            raise
    
    def generate_visualizations(self, save_plots=True):
        """Generate comprehensive visualizations for CLV analysis"""
        try:
            logger.info("Generating visualizations...")
            
            # Set up the plotting environment
            plt.rcParams['figure.figsize'] = (12, 8)
            
            # 1. CLV Distribution
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Customer Lifetime Value Analysis Dashboard', fontsize=16, fontweight='bold')
            
            # CLV Histogram
            axes[0,0].hist(self.clv_df['simple_clv'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0,0].set_title('Distribution of Customer Lifetime Value')
            axes[0,0].set_xlabel('CLV (₹)')
            axes[0,0].set_ylabel('Number of Customers')
            axes[0,0].axvline(self.clv_df['simple_clv'].mean(), color='red', linestyle='--', 
                             label=f'Mean: ₹{self.clv_df["simple_clv"].mean():,.0f}')
            axes[0,0].legend()
            
            # CLV vs Monthly Profit
            scatter = axes[0,1].scatter(self.clv_df['monthly_profit'], self.clv_df['simple_clv'], 
                                      alpha=0.6, c=self.clv_df['churn_probability'], cmap='RdYlBu_r')
            axes[0,1].set_title('CLV vs Monthly Profit (colored by Churn Risk)')
            axes[0,1].set_xlabel('Monthly Profit (₹)')
            axes[0,1].set_ylabel('CLV (₹)')
            plt.colorbar(scatter, ax=axes[0,1], label='Churn Probability')
            
            # Customer Segments
            if 'segment_name' in self.clv_df.columns:
                segment_counts = self.clv_df['segment_name'].value_counts()
                axes[1,0].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%')
                axes[1,0].set_title('Customer Segmentation')
            
            # CLV by Segment
            if 'segment_name' in self.clv_df.columns:
                sns.boxplot(data=self.clv_df, x='segment_name', y='simple_clv', ax=axes[1,1])
                axes[1,1].set_title('CLV Distribution by Customer Segment')
                axes[1,1].set_xlabel('Customer Segment')
                axes[1,1].set_ylabel('CLV (₹)')
                axes[1,1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            if save_plots:
                plt.savefig('clv_dashboard.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # 2. Segment Analysis
            if self.segments is not None:
                fig, axes = plt.subplots(2, 2, figsize=(15, 12))
                fig.suptitle('Customer Segment Analysis', fontsize=16, fontweight='bold')
                
                # Average CLV by Segment
                segment_clv = self.clv_df.groupby('segment_name')['simple_clv'].mean().sort_values(ascending=False)
                axes[0,0].bar(segment_clv.index, segment_clv.values, color='lightcoral')
                axes[0,0].set_title('Average CLV by Segment')
                axes[0,0].set_ylabel('Average CLV (₹)')
                axes[0,0].tick_params(axis='x', rotation=45)
                
                # Customer Count by Segment
                segment_counts = self.clv_df['segment_name'].value_counts()
                axes[0,1].bar(segment_counts.index, segment_counts.values, color='lightgreen')
                axes[0,1].set_title('Customer Count by Segment')
                axes[0,1].set_ylabel('Number of Customers')
                axes[0,1].tick_params(axis='x', rotation=45)
                
                # Churn Risk by Segment
                segment_churn = self.clv_df.groupby('segment_name')['churn_probability'].mean().sort_values(ascending=False)
                axes[1,0].bar(segment_churn.index, segment_churn.values, color='orange')
                axes[1,0].set_title('Average Churn Risk by Segment')
                axes[1,0].set_ylabel('Churn Probability')
                axes[1,0].tick_params(axis='x', rotation=45)
                
                # Monthly Profit by Segment
                segment_profit = self.clv_df.groupby('segment_name')['monthly_profit'].mean().sort_values(ascending=False)
                axes[1,1].bar(segment_profit.index, segment_profit.values, color='skyblue')
                axes[1,1].set_title('Average Monthly Profit by Segment')
                axes[1,1].set_ylabel('Monthly Profit (₹)')
                axes[1,1].tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                if save_plots:
                    plt.savefig('segment_analysis.png', dpi=300, bbox_inches='tight')
                plt.show()
            
            # 3. Feature Importance (if model exists)
            if 'clv_predictor' in self.models:
                feature_importance = pd.DataFrame({
                    'feature': self.models['clv_predictor'].feature_names_in_,
                    'importance': self.models['clv_predictor'].feature_importances_
                }).sort_values('importance', ascending=False).head(10)
                
                plt.figure(figsize=(10, 6))
                sns.barplot(data=feature_importance, y='feature', x='importance', palette='viridis')
                plt.title('Top 10 Most Important Features for CLV Prediction')
                plt.xlabel('Feature Importance')
                if save_plots:
                    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
                plt.show()
            
            logger.info("✅ Visualizations generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")
            raise
    
    def generate_insights_report(self):
        """Generate actionable insights for bank management"""
        try:
            print("\n" + "="*80)
            print("CUSTOMER LIFETIME VALUE ANALYSIS REPORT")
            print("="*80)
            
            # Overall CLV Statistics
            print("\n📊 OVERALL CLV STATISTICS")
            print("-" * 40)
            print(f"Total Customers Analyzed: {len(self.clv_df):,}")
            print(f"Average CLV: ₹{self.clv_df['simple_clv'].mean():,.2f}")
            print(f"Median CLV: ₹{self.clv_df['simple_clv'].median():,.2f}")
            print(f"Total Portfolio CLV: ₹{self.clv_df['simple_clv'].sum():,.2f}")
            print(f"Average Monthly Profit per Customer: ₹{self.clv_df['monthly_profit'].mean():,.2f}")
            
            # Top Value Customers
            print("\n💎 TOP VALUE CUSTOMERS")
            print("-" * 40)
            top_customers = self.clv_df.nlargest(10, 'simple_clv')[['customer_id', 'simple_clv', 'monthly_profit']]
            print(top_customers.to_string(index=False))
            
            # Customer Segments Analysis
            if 'segment_name' in self.clv_df.columns:
                print("\n🎯 CUSTOMER SEGMENT ANALYSIS")
                print("-" * 40)
                segment_analysis = self.clv_df.groupby('segment_name').agg({
                    'customer_id': 'count',
                    'simple_clv': ['mean', 'sum'],
                    'monthly_profit': 'mean',
                    'churn_probability': 'mean'
                }).round(2)
                
                # Flatten column names
                segment_analysis.columns = ['Customer_Count', 'Avg_CLV', 'Total_CLV', 'Avg_Monthly_Profit', 'Avg_Churn_Risk']
                segment_analysis = segment_analysis.sort_values('Total_CLV', ascending=False)
                print(segment_analysis)
            
            # Risk Analysis
            print("\n⚠️ RISK ANALYSIS")
            print("-" * 40)
            high_risk_customers = self.clv_df[self.clv_df['churn_probability'] > 0.5]
            print(f"High Risk Customers (>50% churn probability): {len(high_risk_customers):,}")
            print(f"CLV at Risk: ₹{high_risk_customers['simple_clv'].sum():,.2f}")
            print(f"Average CLV of High Risk Customers: ₹{high_risk_customers['simple_clv'].mean():,.2f}")
            
            # Profitability Analysis
            print("\n💰 PROFITABILITY ANALYSIS")
            print("-" * 40)
            profitable_customers = self.clv_df[self.clv_df['monthly_profit'] > 0]
            unprofitable_customers = self.clv_df[self.clv_df['monthly_profit'] <= 0]
            
            print(f"Profitable Customers: {len(profitable_customers):,} ({len(profitable_customers)/len(self.clv_df)*100:.1f}%)")
            print(f"Unprofitable Customers: {len(unprofitable_customers):,} ({len(unprofitable_customers)/len(self.clv_df)*100:.1f}%)")
            print(f"Average Profit of Profitable Customers: ₹{profitable_customers['monthly_profit'].mean():,.2f}")
            print(f"Average Loss of Unprofitable Customers: ₹{unprofitable_customers['monthly_profit'].mean():,.2f}")
            
            # Management Recommendations
            print("\n🎯 MANAGEMENT RECOMMENDATIONS")
            print("-" * 40)
            print("1. RETENTION STRATEGIES:")
            print("   • Focus retention efforts on high-value, high-risk customers")
            print("   • Implement targeted offers for customers with churn probability > 30%")
            print("   • Develop loyalty programs for Champions and High Value segments")
            
            print("\n2. ACQUISITION STRATEGIES:")
            print("   • Target customer profiles similar to Champions segment")
            print("   • Optimize acquisition costs based on predicted CLV")
            print("   • Focus on customers with high monthly profit potential")
            
            print("\n3. PRODUCT STRATEGIES:")
            print("   • Cross-sell additional products to high CLV customers")
            print("   • Review pricing for unprofitable customer segments")
            print("   • Develop premium products for high-value segments")
            
            print("\n4. RISK MANAGEMENT:")
            print("   • Monitor customers with declining payment ratios")
            print("   • Implement early warning systems for churn risk")
            print("   • Consider credit limit adjustments for high-risk customers")
            
            # ROI Calculations
            print("\n📈 POTENTIAL ROI SCENARIOS")
            print("-" * 40)
            if len(high_risk_customers) > 0:
                retention_cost = 500  # Assumed cost per customer for retention campaign
                retention_rate_improvement = 0.2  # 20% improvement in retention
                
                potential_clv_saved = high_risk_customers['simple_clv'].sum() * retention_rate_improvement
                campaign_cost = len(high_risk_customers) * retention_cost
                roi = (potential_clv_saved - campaign_cost) / campaign_cost * 100
                
                print(f"Retention Campaign ROI Analysis:")
                print(f"  • Target Customers: {len(high_risk_customers):,}")
                print(f"  • Campaign Cost: ₹{campaign_cost:,.2f}")
                print(f"  • Potential CLV Saved: ₹{potential_clv_saved:,.2f}")
                print(f"  • Estimated ROI: {roi:.1f}%")
            
            print("\n" + "="*80)
            
        except Exception as e:
            logger.error(f"Error generating insights report: {str(e)}")
            raise
    
    def save_results(self, output_file='clv_results.csv'):
        """Save CLV analysis results"""
        try:
            self.clv_df.to_csv(output_file, index=False)
            logger.info(f"Results saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise
    
    def run_complete_analysis(self, discount_rate=0.1, prediction_months=36, n_segments=5, save_plots=True):
        """Run the complete CLV analysis pipeline"""
        try:
            print("🚀 Starting Customer Lifetime Value Analysis...")
            print("="*60)
            
            # Load data
            if not self.load_data():
                return False
            
            # Calculate CLV metrics
            self.calculate_clv_metrics(discount_rate, prediction_months)
            
            # Perform customer segmentation (non-fatal — continue if it fails)
            try:
                self.perform_customer_segmentation(n_segments)
            except Exception as seg_e:
                logger.warning(f"Customer segmentation failed but continuing pipeline: {seg_e}")
                # continue without segments

            # Generate visualizations
            self.generate_visualizations(save_plots)
            
            # Generate insights report
            self.generate_insights_report()
            
            # Save results
            self.save_results()
            
            print("\n✅ CLV Analysis completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in complete analysis: {str(e)}")
            return False

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Credit Card Customer Lifetime Value Analysis')
    parser.add_argument('--data-file', type=str, default='syntheticdata.csv', 
                       help='Path to synthetic data CSV file (default: syntheticdata.csv)')
    parser.add_argument('--discount-rate', type=float, default=0.1, 
                       help='Annual discount rate for NPV calculation (default: 0.1)')
    parser.add_argument('--prediction-months', type=int, default=36, 
                       help='Number of months for CLV prediction (default: 36)')
    parser.add_argument('--segments', type=int, default=5, 
                       help='Number of customer segments (default: 5)')
    parser.add_argument('--no-plots', action='store_true', 
                       help='Skip generating and saving plots')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.discount_rate < 0 or args.discount_rate > 1:
        logger.error("Discount rate must be between 0 and 1")
        sys.exit(1)
    
    if args.prediction_months <= 0:
        logger.error("Prediction months must be positive")
        sys.exit(1)
    
    if args.segments < 2:
        logger.error("Number of segments must be at least 2")
        sys.exit(1)
    
    # Run analysis
    analyzer = CLVAnalyzer(args.data_file)
    success = analyzer.run_complete_analysis(
        discount_rate=args.discount_rate,
        prediction_months=args.prediction_months,
        n_segments=args.segments,
        save_plots=not args.no_plots
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
