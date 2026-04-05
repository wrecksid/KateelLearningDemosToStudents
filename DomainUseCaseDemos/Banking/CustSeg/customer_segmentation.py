"""
Bank Customer Segmentation Analysis
==================================

This module performs customer segmentation analysis on bank customer data
using various machine learning techniques including K-Means clustering,
RFM analysis, and advanced segmentation methods.

Author: AI Assistant
License: MIT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import logging
import argparse
import os

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
plt.style.use('default')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CustomerSegmentation:
    """
    A comprehensive customer segmentation analysis class for banking data.
    
    This class provides various segmentation techniques including:
    - K-Means clustering
    - RFM (Recency, Frequency, Monetary) analysis
    - Advanced behavioral segmentation
    - Customer lifetime value segmentation
    """
    
    def __init__(self, data_path=None, df=None):
        """
        Initialize the customer segmentation analyzer.
        
        Args:
            data_path (str): Path to the CSV file containing customer data
            df (pd.DataFrame): Customer data DataFrame (alternative to data_path)
        """
        try:
            if df is not None:
                self.df = df.copy()
            elif data_path and os.path.exists(data_path):
                self.df = pd.read_csv(data_path)
                logger.info(f"Loaded data from {data_path}")
            else:
                raise ValueError("Either data_path or df must be provided")
            
            self.df_processed = None
            self.scaler = StandardScaler()
            self.segmentation_results = {}
            
            logger.info(f"Initialized segmentation analysis with {len(self.df)} records")
            
        except Exception as e:
            logger.error(f"Error initializing CustomerSegmentation: {str(e)}")
            raise
    
    def preprocess_data(self):
        """
        Preprocess the customer data for segmentation analysis.
        
        Returns:
            pd.DataFrame: Processed data ready for segmentation
        """
        try:
            logger.info("Preprocessing customer data...")
            
            df = self.df.copy()
            
            # Handle missing values
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
            
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                if col not in ['customer_id', 'name']:
                    df[col] = df[col].fillna(df[col].mode()[0])
            
            # Create additional features for segmentation
            df['income_to_balance_ratio'] = df['annual_income'] / (df['account_balance'] + 1)
            df['transaction_frequency'] = df['monthly_transactions'] * 12
            df['products_per_tenure'] = df['num_products'] / (df['tenure_years'] + 1)
            df['clv_per_year'] = df['customer_lifetime_value'] / (df['tenure_years'] + 1)
            
            # Age groups
            df['age_group'] = pd.cut(df['age'], 
                                   bins=[0, 30, 45, 60, 100], 
                                   labels=['Young', 'Middle', 'Senior', 'Elder'])
            
            # Income groups
            df['income_group'] = pd.cut(df['annual_income'], 
                                      bins=[0, 300000, 800000, 1500000, float('inf')], 
                                      labels=['Low', 'Medium', 'High', 'Premium'])
            
            self.df_processed = df
            logger.info("Data preprocessing completed")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in data preprocessing: {str(e)}")
            raise
    
    def perform_kmeans_segmentation(self, n_clusters=4, features=None):
        """
        Perform K-Means clustering for customer segmentation.
        
        Args:
            n_clusters (int): Number of clusters
            features (list): Features to use for clustering
            
        Returns:
            dict: Clustering results including labels and metrics
        """
        try:
            logger.info(f"Performing K-Means segmentation with {n_clusters} clusters...")
            
            if self.df_processed is None:
                self.preprocess_data()
            
            if features is None:
                features = ['annual_income', 'account_balance', 'credit_score', 
                           'num_products', 'tenure_years', 'monthly_transactions',
                           'digital_engagement_score', 'customer_lifetime_value']
            
            # Prepare data for clustering
            X = self.df_processed[features].copy()
            X_scaled = self.scaler.fit_transform(X)
            
            # Perform K-Means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            # Calculate metrics
            silhouette_avg = silhouette_score(X_scaled, cluster_labels)
            calinski_score = calinski_harabasz_score(X_scaled, cluster_labels)
            
            # Add cluster labels to dataframe
            self.df_processed['kmeans_cluster'] = cluster_labels
            
            # Generate cluster profiles
            cluster_profiles = self._generate_cluster_profiles('kmeans_cluster', features)
            
            results = {
                'method': 'K-Means',
                'n_clusters': n_clusters,
                'labels': cluster_labels,
                'silhouette_score': silhouette_avg,
                'calinski_score': calinski_score,
                'cluster_centers': kmeans.cluster_centers_,
                'profiles': cluster_profiles,
                'features_used': features
            }
            
            self.segmentation_results['kmeans'] = results
            logger.info(f"K-Means segmentation completed. Silhouette Score: {silhouette_avg:.3f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in K-Means segmentation: {str(e)}")
            raise
    
    def perform_rfm_segmentation(self):
        """
        Perform RFM (Recency, Frequency, Monetary) analysis.
        
        Returns:
            dict: RFM segmentation results
        """
        try:
            logger.info("Performing RFM segmentation...")
            
            if self.df_processed is None:
                self.preprocess_data()
            
            df = self.df_processed.copy()
            
            # Calculate RFM metrics
            # Recency: Days since last transaction (simulated)
            df['recency'] = np.random.exponential(30, len(df))  # Days since last transaction
            
            # Frequency: Monthly transactions * 12 (annual frequency)
            df['frequency'] = df['monthly_transactions'] * 12
            
            # Monetary: Account balance + annual income as proxy for monetary value
            df['monetary'] = df['account_balance'] + (df['annual_income'] * 0.1)
            
            # Calculate RFM scores (1-5 scale)
            df['R_score'] = pd.qcut(df['recency'], q=5, labels=[5,4,3,2,1], duplicates='drop')
            df['F_score'] = pd.qcut(df['frequency'], q=5, labels=[1,2,3,4,5], duplicates='drop')
            df['M_score'] = pd.qcut(df['monetary'], q=5, labels=[1,2,3,4,5], duplicates='drop')
            
            # Convert to numeric
            df['R_score'] = pd.to_numeric(df['R_score'], errors='coerce')
            df['F_score'] = pd.to_numeric(df['F_score'], errors='coerce')
            df['M_score'] = pd.to_numeric(df['M_score'], errors='coerce')
            
            # Calculate RFM score
            df['RFM_score'] = df['R_score'].astype(str) + df['F_score'].astype(str) + df['M_score'].astype(str)
            
            # Create RFM segments
            def rfm_segment(row):
                if row['R_score'] >= 4 and row['F_score'] >= 4 and row['M_score'] >= 4:
                    return 'Champions'
                elif row['R_score'] >= 3 and row['F_score'] >= 3 and row['M_score'] >= 3:
                    return 'Loyal Customers'
                elif row['R_score'] >= 3 and row['F_score'] >= 2:
                    return 'Potential Loyalists'
                elif row['R_score'] >= 4 and row['F_score'] <= 2:
                    return 'New Customers'
                elif row['R_score'] <= 2 and row['F_score'] >= 3:
                    return 'At Risk'
                elif row['R_score'] <= 2 and row['F_score'] <= 2 and row['M_score'] >= 3:
                    return 'Cannot Lose Them'
                elif row['R_score'] <= 2 and row['F_score'] <= 2 and row['M_score'] <= 2:
                    return 'Lost Customers'
                else:
                    return 'Others'
            
            df['rfm_segment'] = df.apply(rfm_segment, axis=1)
            
            # Update processed dataframe
            self.df_processed = df
            
            # Generate segment profiles
            segment_profiles = df.groupby('rfm_segment').agg({
                'annual_income': ['mean', 'count'],
                'account_balance': 'mean',
                'customer_lifetime_value': 'mean',
                'recency': 'mean',
                'frequency': 'mean',
                'monetary': 'mean',
                'is_churned': 'mean'
            }).round(2)
            
            results = {
                'method': 'RFM',
                'segments': df['rfm_segment'].unique(),
                'segment_counts': df['rfm_segment'].value_counts(),
                'profiles': segment_profiles
            }
            
            self.segmentation_results['rfm'] = results
            logger.info("RFM segmentation completed")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in RFM segmentation: {str(e)}")
            raise
    
    def _generate_cluster_profiles(self, cluster_column, features):
        """Generate detailed profiles for each cluster."""
        try:
            profiles = {}
            
            for cluster in self.df_processed[cluster_column].unique():
                cluster_data = self.df_processed[self.df_processed[cluster_column] == cluster]
                
                profile = {
                    'size': len(cluster_data),
                    'percentage': len(cluster_data) / len(self.df_processed) * 100,
                    'characteristics': {}
                }
                
                # Numerical features
                for feature in features:
                    if feature in self.df_processed.columns:
                        profile['characteristics'][feature] = {
                            'mean': cluster_data[feature].mean(),
                            'median': cluster_data[feature].median(),
                            'std': cluster_data[feature].std()
                        }
                
                # Additional insights
                profile['avg_age'] = cluster_data['age'].mean()
                profile['churn_rate'] = cluster_data['is_churned'].mean()
                profile['top_cities'] = cluster_data['city'].value_counts().head(3).to_dict()
                profile['education_dist'] = cluster_data['education'].value_counts(normalize=True).to_dict()
                
                profiles[f'Cluster_{cluster}'] = profile
            
            return profiles
            
        except Exception as e:
            logger.warning(f"Error generating cluster profiles: {str(e)}")
            return {}
    
    def find_optimal_clusters(self, max_clusters=10, features=None):
        """
        Find optimal number of clusters using elbow method and silhouette analysis.
        
        Args:
            max_clusters (int): Maximum number of clusters to test
            features (list): Features to use for clustering
            
        Returns:
            dict: Results with optimal cluster suggestions
        """
        try:
            logger.info(f"Finding optimal number of clusters (up to {max_clusters})...")
            
            if self.df_processed is None:
                self.preprocess_data()
            
            if features is None:
                features = ['annual_income', 'account_balance', 'credit_score', 
                           'num_products', 'tenure_years', 'monthly_transactions',
                           'digital_engagement_score']
            
            X = self.df_processed[features]
            X_scaled = self.scaler.fit_transform(X)
            
            inertias = []
            silhouette_scores = []
            k_range = range(2, max_clusters + 1)
            
            for k in k_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(X_scaled)
                
                inertias.append(kmeans.inertia_)
                silhouette_avg = silhouette_score(X_scaled, kmeans.labels_)
                silhouette_scores.append(silhouette_avg)
            
            # Find optimal k using silhouette score
            optimal_k = k_range[np.argmax(silhouette_scores)]
            
            results = {
                'k_range': list(k_range),
                'inertias': inertias,
                'silhouette_scores': silhouette_scores,
                'optimal_k': optimal_k,
                'max_silhouette_score': max(silhouette_scores)
            }
            
            logger.info(f"Optimal number of clusters: {optimal_k}")
            return results
            
        except Exception as e:
            logger.error(f"Error finding optimal clusters: {str(e)}")
            raise
    
    def visualize_segments(self, method='kmeans', save_plots=True):
        """
        Create comprehensive visualizations for customer segments.
        
        Args:
            method (str): Segmentation method ('kmeans' or 'rfm')
            save_plots (bool): Whether to save plots to files
        """
        try:
            logger.info(f"Creating visualizations for {method} segmentation...")
            
            if method == 'kmeans':
                cluster_col = 'kmeans_cluster'
                title_prefix = 'K-Means'
            elif method == 'rfm':
                cluster_col = 'rfm_segment'
                title_prefix = 'RFM'
            else:
                raise ValueError("Method must be 'kmeans' or 'rfm'")
            
            if cluster_col not in self.df_processed.columns:
                raise ValueError(f"Segmentation method '{method}' not performed yet")
            
            # Create multiple visualizations
            fig, axes = plt.subplots(2, 3, figsize=(20, 12))
            fig.suptitle(f'{title_prefix} Customer Segmentation Analysis', fontsize=16, fontweight='bold')
            
            # 1. Segment distribution
            segment_counts = self.df_processed[cluster_col].value_counts()
            axes[0,0].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%')
            axes[0,0].set_title('Segment Distribution')
            
            # 2. Income vs Balance by segment
            for segment in self.df_processed[cluster_col].unique():
                segment_data = self.df_processed[self.df_processed[cluster_col] == segment]
                axes[0,1].scatter(segment_data['annual_income'], segment_data['account_balance'], 
                                label=f'{segment}', alpha=0.6)
            axes[0,1].set_xlabel('Annual Income (₹)')
            axes[0,1].set_ylabel('Account Balance (₹)')
            axes[0,1].set_title('Income vs Account Balance by Segment')
            axes[0,1].legend()
            
            # 3. Age distribution by segment
            self.df_processed.boxplot(column='age', by=cluster_col, ax=axes[0,2])
            axes[0,2].set_title('Age Distribution by Segment')
            axes[0,2].set_xlabel('Segment')
            
            # 4. Credit score by segment
            self.df_processed.boxplot(column='credit_score', by=cluster_col, ax=axes[1,0])
            axes[1,0].set_title('Credit Score by Segment')
            axes[1,0].set_xlabel('Segment')
            
            # 5. Customer lifetime value by segment
            self.df_processed.boxplot(column='customer_lifetime_value', by=cluster_col, ax=axes[1,1])
            axes[1,1].set_title('Customer Lifetime Value by Segment')
            axes[1,1].set_xlabel('Segment')
            
            # 6. Churn rate by segment
            churn_by_segment = self.df_processed.groupby(cluster_col)['is_churned'].mean()
            axes[1,2].bar(churn_by_segment.index, churn_by_segment.values)
            axes[1,2].set_title('Churn Rate by Segment')
            axes[1,2].set_xlabel('Segment')
            axes[1,2].set_ylabel('Churn Rate')
            axes[1,2].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            if save_plots:
                plt.savefig(f'{method}_segmentation_analysis.png', dpi=300, bbox_inches='tight')
                logger.info(f"Saved visualization to {method}_segmentation_analysis.png")
            
            plt.show()
            
            # Additional 3D visualization for K-Means
            if method == 'kmeans':
                self._create_3d_cluster_plot(save_plots)
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {str(e)}")
            raise
    
    def _create_3d_cluster_plot(self, save_plots=True):
        """Create 3D cluster visualization."""
        try:
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            
            colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
            
            for i, cluster in enumerate(self.df_processed['kmeans_cluster'].unique()):
                cluster_data = self.df_processed[self.df_processed['kmeans_cluster'] == cluster]
                ax.scatter(cluster_data['annual_income'], 
                          cluster_data['account_balance'], 
                          cluster_data['credit_score'],
                          c=colors[i % len(colors)], 
                          label=f'Cluster {cluster}',
                          alpha=0.6)
            
            ax.set_xlabel('Annual Income (₹)')
            ax.set_ylabel('Account Balance (₹)')
            ax.set_zlabel('Credit Score')
            ax.set_title('3D K-Means Cluster Visualization')
            ax.legend()
            
            if save_plots:
                plt.savefig('kmeans_3d_clusters.png', dpi=300, bbox_inches='tight')
                logger.info("Saved 3D cluster plot to kmeans_3d_clusters.png")
            
            plt.show()
            
        except Exception as e:
            logger.warning(f"Error creating 3D plot: {str(e)}")
    
    def generate_business_insights(self, method='kmeans'):
        """
        Generate actionable business insights from segmentation analysis.
        
        Args:
            method (str): Segmentation method to analyze
            
        Returns:
            dict: Business insights and recommendations
        """
        try:
            logger.info(f"Generating business insights for {method} segmentation...")
            
            if method not in self.segmentation_results:
                raise ValueError(f"Segmentation method '{method}' not performed yet")
            
            insights = {
                'summary': {},
                'segment_insights': {},
                'recommendations': {},
                'risk_analysis': {}
            }
            
            # Overall summary
            insights['summary'] = {
                'total_customers': len(self.df_processed),
                'average_clv': self.df_processed['customer_lifetime_value'].mean(),
                'overall_churn_rate': self.df_processed['is_churned'].mean(),
                'total_segments': len(self.segmentation_results[method].get('profiles', {}))
            }
            
            if method == 'kmeans':
                cluster_col = 'kmeans_cluster'
            else:
                cluster_col = 'rfm_segment'
            
            # Segment-specific insights
            for segment in self.df_processed[cluster_col].unique():
                segment_data = self.df_processed[self.df_processed[cluster_col] == segment]
                
                insights['segment_insights'][str(segment)] = {
                    'size': len(segment_data),
                    'avg_income': segment_data['annual_income'].mean(),
                    'avg_balance': segment_data['account_balance'].mean(),
                    'avg_clv': segment_data['customer_lifetime_value'].mean(),
                    'churn_rate': segment_data['is_churned'].mean(),
                    'avg_products': segment_data['num_products'].mean(),
                    'digital_engagement': segment_data['digital_engagement_score'].mean(),
                    'dominant_age_group': segment_data['age_group'].mode()[0] if not segment_data['age_group'].empty else 'Unknown'
                }
            
            # Generate recommendations
            insights['recommendations'] = self._generate_recommendations(method, insights['segment_insights'])
            
            # Risk analysis
            insights['risk_analysis'] = self._analyze_risks(insights['segment_insights'])
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating business insights: {str(e)}")
            raise
    
    def _generate_recommendations(self, method, segment_insights):
        """Generate business recommendations based on segment analysis."""
        recommendations = {}
        
        for segment, data in segment_insights.items():
            recs = []
            
            # High value, low churn
            if data['avg_clv'] > 100000 and data['churn_rate'] < 0.1:
                recs.append("VIP Treatment: Provide premium services and exclusive offers")
                recs.append("Loyalty Programs: Implement rewards to maintain satisfaction")
            
            # High churn risk
            elif data['churn_rate'] > 0.3:
                recs.append("Retention Campaign: Immediate intervention required")
                recs.append("Personalized Offers: Create targeted retention offers")
                recs.append("Customer Success: Assign dedicated relationship managers")
            
            # Low engagement
            elif data['digital_engagement'] < 50:
                recs.append("Digital Onboarding: Improve digital literacy programs")
                recs.append("Omnichannel Support: Provide multiple touchpoints")
            
            # High income, low products
            elif data['avg_income'] > 800000 and data['avg_products'] < 2:
                recs.append("Cross-selling: Promote premium products and services")
                recs.append("Investment Advisory: Offer wealth management services")
            
            # Default recommendations
            else:
                recs.append("Regular Engagement: Maintain consistent communication")
                recs.append("Product Education: Educate about available services")
            
            recommendations[segment] = recs
        
        return recommendations
    
    def _analyze_risks(self, segment_insights):
        """Analyze risks for each segment."""
        risk_analysis = {}
        
        for segment, data in segment_insights.items():
            risk_level = "Low"
            risk_factors = []
            
            if data['churn_rate'] > 0.25:
                risk_level = "High"
                risk_factors.append("High churn rate")
            
            if data['avg_clv'] < 50000:
                if risk_level == "Low":
                    risk_level = "Medium"
                risk_factors.append("Low customer lifetime value")
            
            if data['digital_engagement'] < 40:
                if risk_level == "Low":
                    risk_level = "Medium"
                risk_factors.append("Low digital engagement")
            
            risk_analysis[segment] = {
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'priority': 1 if risk_level == "High" else 2 if risk_level == "Medium" else 3
            }
        
        return risk_analysis
    
    def export_results(self, filename='segmentation_results.csv'):
        """
        Export segmentation results to CSV.
        
        Args:
            filename (str): Output filename
        """
        try:
            if self.df_processed is not None:
                self.df_processed.to_csv(filename, index=False)
                logger.info(f"Results exported to {filename}")
                print(f"✅ Segmentation results exported to {filename}")
            else:
                raise ValueError("No processed data available to export")
                
        except Exception as e:
            logger.error(f"Error exporting results: {str(e)}")
            raise

def main():
    """Main function to run customer segmentation analysis."""
    parser = argparse.ArgumentParser(description='Bank Customer Segmentation Analysis')
    parser.add_argument('--data', type=str, default='bank_customer_data.csv', 
                       help='Path to customer data CSV file')
    parser.add_argument('--method', type=str, default='both', 
                       choices=['kmeans', 'rfm', 'both'],
                       help='Segmentation method to use')
    parser.add_argument('--clusters', type=int, default=4, 
                       help='Number of clusters for K-Means')
    parser.add_argument('--output', type=str, default='segmentation_results.csv',
                       help='Output filename for results')
    
    args = parser.parse_args()
    
    try:
        print("🏦 Bank Customer Segmentation Analysis")
        print("=" * 50)
        
        # Initialize segmentation
        segmentation = CustomerSegmentation(data_path=args.data)
        
        # Preprocess data
        segmentation.preprocess_data()
        print(f"✅ Preprocessed {len(segmentation.df_processed)} customer records")
        
        # Perform segmentation based on method
        if args.method in ['kmeans', 'both']:
            print(f"\n🔍 Performing K-Means segmentation with {args.clusters} clusters...")
            
            # Find optimal clusters first
            optimal_results = segmentation.find_optimal_clusters()
            print(f"📊 Suggested optimal clusters: {optimal_results['optimal_k']}")
            
            # Perform K-Means with specified clusters
            kmeans_results = segmentation.perform_kmeans_segmentation(n_clusters=args.clusters)
            print(f"✅ K-Means completed - Silhouette Score: {kmeans_results['silhouette_score']:.3f}")
            
            # Visualize K-Means results
            segmentation.visualize_segments(method='kmeans')
            
            # Generate business insights
            kmeans_insights = segmentation.generate_business_insights(method='kmeans')
            print(f"\n📈 K-Means Business Insights:")
            print(f"Total Customers: {kmeans_insights['summary']['total_customers']}")
            print(f"Average CLV: ₹{kmeans_insights['summary']['average_clv']:,.0f}")
            print(f"Overall Churn Rate: {kmeans_insights['summary']['overall_churn_rate']:.1%}")
        
        if args.method in ['rfm', 'both']:
            print(f"\n🔍 Performing RFM segmentation...")
            
            # Perform RFM analysis
            rfm_results = segmentation.perform_rfm_segmentation()
            print(f"✅ RFM completed - {len(rfm_results['segments'])} segments identified")
            
            # Visualize RFM results
            segmentation.visualize_segments(method='rfm')
            
            # Generate business insights
            rfm_insights = segmentation.generate_business_insights(method='rfm')
            print(f"\n📈 RFM Business Insights:")
            for segment, count in rfm_results['segment_counts'].items():
                print(f"{segment}: {count} customers ({count/len(segmentation.df_processed)*100:.1f}%)")
        
        # Export results
        segmentation.export_results(args.output)
        
        print(f"\n🎯 Segmentation Analysis Completed Successfully!")
        print("Check the generated visualizations and exported CSV for detailed results.")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
