"""
Banking Customer Segmentation Analysis
=====================================

This module implements comprehensive customer segmentation techniques for banking,
including RFM analysis, K-means clustering, and business insights generation.

Author: AI/ML Finance Course
Version: 1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import logging
import argparse
import sys
from pathlib import Path
from typing import Tuple, Dict, List, Optional

# Configure logging and warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class CustomerSegmentation:
    """
    Comprehensive customer segmentation analysis for banking customers.
    
    This class implements multiple segmentation approaches including:
    - RFM (Recency, Frequency, Monetary) Analysis
    - K-means clustering with optimal cluster selection
    - Customer profiling and business insights
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the customer segmentation analyzer.
        
        Args:
            data_path (str): Path to the customer data CSV file
        """
        self.data_path = data_path
        self.data = None
        self.processed_data = None
        self.clusters = None
        self.scaler = StandardScaler()
        self.optimal_clusters = None
        
        # Set plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
    def load_data(self, data_path: str = None) -> pd.DataFrame:
        """
        Load customer data from CSV file.
        
        Args:
            data_path (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded customer data
        """
        try:
            if data_path:
                self.data_path = data_path
            
            if not self.data_path:
                raise ValueError("No data path provided")
            
            if not Path(self.data_path).exists():
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            self.data = pd.read_csv(self.data_path)
            logger.info(f"Loaded {len(self.data)} customer records from {self.data_path}")
            
            # Basic data validation
            required_columns = ['customer_id', 'annual_income', 'account_balance', 
                              'monthly_transactions', 'credit_score']
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def perform_rfm_analysis(self) -> pd.DataFrame:
        """
        Perform RFM (Recency, Frequency, Monetary) analysis.
        
        Returns:
            pd.DataFrame: Data with RFM scores and segments
        """
        try:
            if self.data is None:
                raise ValueError("No data loaded. Call load_data() first.")
            
            logger.info("Performing RFM analysis...")
            
            # Create RFM features (using existing scores from synthetic data)
            rfm_data = self.data.copy()
            
            # Normalize RFM scores to 1-5 scale
            rfm_data['R_Score'] = pd.qcut(rfm_data['recency_score'], 5, labels=[1,2,3,4,5])
            rfm_data['F_Score'] = pd.qcut(rfm_data['frequency_score'].rank(method='first'), 5, labels=[1,2,3,4,5])
            rfm_data['M_Score'] = pd.qcut(rfm_data['monetary_score'], 5, labels=[1,2,3,4,5])
            
            # Convert to numeric
            rfm_data['R_Score'] = rfm_data['R_Score'].astype(int)
            rfm_data['F_Score'] = rfm_data['F_Score'].astype(int)
            rfm_data['M_Score'] = rfm_data['M_Score'].astype(int)
            
            # Create RFM combined score
            rfm_data['RFM_Score'] = (rfm_data['R_Score'].astype(str) + 
                                   rfm_data['F_Score'].astype(str) + 
                                   rfm_data['M_Score'].astype(str))
            
            # Define customer segments based on RFM scores
            def segment_customers(row):
                if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
                    return 'Champions'
                elif row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3:
                    return 'Loyal Customers'
                elif row['R_Score'] >= 4 and row['F_Score'] >= 2:
                    return 'Potential Loyalists'
                elif row['R_Score'] >= 4 and row['F_Score'] <= 2:
                    return 'New Customers'
                elif row['R_Score'] <= 2 and row['F_Score'] >= 3:
                    return 'At Risk'
                elif row['R_Score'] <= 2 and row['F_Score'] <= 2 and row['M_Score'] >= 3:
                    return 'Cannot Lose Them'
                elif row['R_Score'] <= 2 and row['F_Score'] <= 2 and row['M_Score'] <= 2:
                    return 'Lost Customers'
                else:
                    return 'Others'
            
            rfm_data['RFM_Segment'] = rfm_data.apply(segment_customers, axis=1)
            
            self.rfm_data = rfm_data
            logger.info("RFM analysis completed successfully")
            
            return rfm_data
            
        except Exception as e:
            logger.error(f"Error in RFM analysis: {e}")
            raise
    
    def prepare_clustering_data(self) -> np.ndarray:
        """
        Prepare data for K-means clustering.
        
        Returns:
            np.ndarray: Scaled feature matrix for clustering
        """
        try:
            if self.data is None:
                raise ValueError("No data loaded. Call load_data() first.")
            
            logger.info("Preparing data for clustering...")
            
            # Select features for clustering
            clustering_features = [
                'age', 'annual_income', 'account_balance', 'credit_score',
                'monthly_transactions', 'num_products', 'tenure_years',
                'recency_score', 'frequency_score', 'monetary_score'
            ]
            
            # Check if all features exist
            missing_features = [f for f in clustering_features if f not in self.data.columns]
            if missing_features:
                logger.warning(f"Missing features for clustering: {missing_features}")
                clustering_features = [f for f in clustering_features if f in self.data.columns]
            
            # Handle missing values
            cluster_data = self.data[clustering_features].copy()
            cluster_data = cluster_data.fillna(cluster_data.median())
            
            # Remove outliers using IQR method
            Q1 = cluster_data.quantile(0.25)
            Q3 = cluster_data.quantile(0.75)
            IQR = Q3 - Q1
            
            # Keep data within 1.5 * IQR
            outlier_condition = ~((cluster_data < (Q1 - 1.5 * IQR)) | 
                                (cluster_data > (Q3 + 1.5 * IQR))).any(axis=1)
            cluster_data = cluster_data[outlier_condition]
            
            # Scale features
            scaled_data = self.scaler.fit_transform(cluster_data)
            
            self.processed_data = cluster_data
            self.scaled_data = scaled_data
            
            logger.info(f"Prepared {scaled_data.shape[0]} samples with {scaled_data.shape[1]} features")
            
            return scaled_data
            
        except Exception as e:
            logger.error(f"Error preparing clustering data: {e}")
            raise
    
    def find_optimal_clusters(self, max_clusters: int = 10) -> int:
        """
        Find optimal number of clusters using elbow method and silhouette analysis.
        
        Args:
            max_clusters (int): Maximum number of clusters to test
            
        Returns:
            int: Optimal number of clusters
        """
        try:
            if self.scaled_data is None:
                self.prepare_clustering_data()
            
            logger.info("Finding optimal number of clusters...")
            
            # Calculate metrics for different cluster numbers
            cluster_range = range(2, max_clusters + 1)
            inertias = []
            silhouette_scores = []
            calinski_scores = []
            
            for k in cluster_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(self.scaled_data)
                
                inertias.append(kmeans.inertia_)
                silhouette_scores.append(silhouette_score(self.scaled_data, cluster_labels))
                calinski_scores.append(calinski_harabasz_score(self.scaled_data, cluster_labels))
            
            # Find optimal clusters using elbow method
            # Calculate rate of change in inertia
            inertia_diff = np.diff(inertias)
            inertia_diff2 = np.diff(inertia_diff)
            
            # Find elbow point
            elbow_point = np.argmax(inertia_diff2) + 2
            
            # Choose optimal clusters based on silhouette score
            optimal_silhouette = cluster_range[np.argmax(silhouette_scores)]
            
            # Use average of elbow and silhouette methods
            self.optimal_clusters = int((elbow_point + optimal_silhouette) / 2)
            
            # Visualization
            fig, axes = plt.subplots(1, 3, figsize=(18, 5))
            
            # Elbow curve
            axes[0].plot(cluster_range, inertias, 'bo-')
            axes[0].axvline(x=elbow_point, color='red', linestyle='--', 
                          label=f'Elbow at k={elbow_point}')
            axes[0].set_xlabel('Number of Clusters')
            axes[0].set_ylabel('Inertia')
            axes[0].set_title('Elbow Method')
            axes[0].legend()
            axes[0].grid(True)
            
            # Silhouette scores
            axes[1].plot(cluster_range, silhouette_scores, 'go-')
            axes[1].axvline(x=optimal_silhouette, color='red', linestyle='--',
                          label=f'Best silhouette at k={optimal_silhouette}')
            axes[1].set_xlabel('Number of Clusters')
            axes[1].set_ylabel('Silhouette Score')
            axes[1].set_title('Silhouette Analysis')
            axes[1].legend()
            axes[1].grid(True)
            
            # Calinski-Harabasz scores
            axes[2].plot(cluster_range, calinski_scores, 'mo-')
            axes[2].set_xlabel('Number of Clusters')
            axes[2].set_ylabel('Calinski-Harabasz Score')
            axes[2].set_title('Calinski-Harabasz Index')
            axes[2].grid(True)
            
            plt.tight_layout()
            plt.show()
            
            logger.info(f"Optimal number of clusters determined: {self.optimal_clusters}")
            
            return self.optimal_clusters
            
        except Exception as e:
            logger.error(f"Error finding optimal clusters: {e}")
            raise
    
    def perform_kmeans_clustering(self, n_clusters: int = None) -> pd.DataFrame:
        """
        Perform K-means clustering on customer data.
        
        Args:
            n_clusters (int): Number of clusters (if None, uses optimal clusters)
            
        Returns:
            pd.DataFrame: Data with cluster assignments
        """
        try:
            if self.scaled_data is None:
                self.prepare_clustering_data()
            
            if n_clusters is None:
                if self.optimal_clusters is None:
                    self.find_optimal_clusters()
                n_clusters = self.optimal_clusters
            
            logger.info(f"Performing K-means clustering with {n_clusters} clusters...")
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(self.scaled_data)
            
            # Add cluster labels to original data
            clustered_data = self.processed_data.copy()
            clustered_data['Cluster'] = cluster_labels
            
            # Calculate cluster centers in original scale
            cluster_centers = pd.DataFrame(
                self.scaler.inverse_transform(kmeans.cluster_centers_),
                columns=self.processed_data.columns
            )
            cluster_centers['Cluster'] = range(n_clusters)
            
            self.clusters = clustered_data
            self.cluster_centers = cluster_centers
            self.kmeans_model = kmeans
            
            # Print cluster summary
            print(f"\n{'='*60}")
            print("CLUSTERING SUMMARY")
            print(f"{'='*60}")
            print(f"Number of clusters: {n_clusters}")
            print(f"Total customers clustered: {len(clustered_data)}")
            print(f"Silhouette score: {silhouette_score(self.scaled_data, cluster_labels):.3f}")
            print(f"\nCluster distribution:")
            print(clustered_data['Cluster'].value_counts().sort_index())
            
            return clustered_data
            
        except Exception as e:
            logger.error(f"Error in K-means clustering: {e}")
            raise
    
    def analyze_clusters(self) -> Dict[int, Dict]:
        """
        Analyze and profile each cluster.
        
        Returns:
            Dict[int, Dict]: Cluster profiles and characteristics
        """
        try:
            if self.clusters is None:
                raise ValueError("No clustering performed. Call perform_kmeans_clustering() first.")
            
            logger.info("Analyzing cluster characteristics...")
            
            cluster_profiles = {}
            
            for cluster_id in sorted(self.clusters['Cluster'].unique()):
                cluster_data = self.clusters[self.clusters['Cluster'] == cluster_id]
                
                profile = {
                    'size': len(cluster_data),
                    'percentage': len(cluster_data) / len(self.clusters) * 100,
                    'characteristics': {
                        'avg_age': cluster_data['age'].mean(),
                        'avg_income': cluster_data['annual_income'].mean(),
                        'avg_balance': cluster_data['account_balance'].mean(),
                        'avg_credit_score': cluster_data['credit_score'].mean(),
                        'avg_transactions': cluster_data['monthly_transactions'].mean(),
                        'avg_products': cluster_data['num_products'].mean(),
                        'avg_tenure': cluster_data['tenure_years'].mean(),
                    }
                }
                
                # Business interpretation
                if (profile['characteristics']['avg_income'] > 80000 and 
                    profile['characteristics']['avg_balance'] > 50000):
                    profile['business_label'] = 'High-Value Customers'
                    profile['strategy'] = 'Premium services, wealth management, exclusive offers'
                    
                elif (profile['characteristics']['avg_age'] < 35 and
                      profile['characteristics']['avg_income'] < 50000):
                    profile['business_label'] = 'Young Professionals'
                    profile['strategy'] = 'Digital banking, career-building products, competitive rates'
                    
                elif profile['characteristics']['avg_tenure'] > 15:
                    profile['business_label'] = 'Long-term Loyal'
                    profile['strategy'] = 'Retention programs, loyalty rewards, referral incentives'
                    
                elif profile['characteristics']['avg_transactions'] < 5:
                    profile['business_label'] = 'Low-Engagement'
                    profile['strategy'] = 'Activation campaigns, simplified products, education'
                    
                else:
                    profile['business_label'] = 'Standard Customers'
                    profile['strategy'] = 'Cross-selling, product bundling, satisfaction surveys'
                
                cluster_profiles[cluster_id] = profile
            
            self.cluster_profiles = cluster_profiles
            
            return cluster_profiles
            
        except Exception as e:
            logger.error(f"Error analyzing clusters: {e}")
            raise
    
    def visualize_clusters(self) -> None:
        """Create comprehensive visualizations of customer clusters."""
        try:
            if self.clusters is None:
                raise ValueError("No clustering performed. Call perform_kmeans_clustering() first.")
            
            logger.info("Creating cluster visualizations...")
            
            # 1. PCA visualization
            pca = PCA(n_components=2, random_state=42)
            pca_data = pca.fit_transform(self.scaled_data)
            
            plt.figure(figsize=(20, 15))
            
            # PCA scatter plot
            plt.subplot(2, 3, 1)
            scatter = plt.scatter(pca_data[:, 0], pca_data[:, 1], 
                                c=self.clusters['Cluster'], cmap='viridis', alpha=0.6)
            plt.xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.2%} variance)')
            plt.ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.2%} variance)')
            plt.title('Customer Clusters (PCA View)')
            plt.colorbar(scatter)
            
            # Income vs Balance colored by cluster
            plt.subplot(2, 3, 2)
            scatter = plt.scatter(self.clusters['annual_income'], self.clusters['account_balance'],
                                c=self.clusters['Cluster'], cmap='viridis', alpha=0.6)
            plt.xlabel('Annual Income ($)')
            plt.ylabel('Account Balance ($)')
            plt.title('Income vs Balance by Cluster')
            plt.colorbar(scatter)
            
            # Age vs Credit Score
            plt.subplot(2, 3, 3)
            scatter = plt.scatter(self.clusters['age'], self.clusters['credit_score'],
                                c=self.clusters['Cluster'], cmap='viridis', alpha=0.6)
            plt.xlabel('Age')
            plt.ylabel('Credit Score')
            plt.title('Age vs Credit Score by Cluster')
            plt.colorbar(scatter)
            
            # Cluster size distribution
            plt.subplot(2, 3, 4)
            cluster_counts = self.clusters['Cluster'].value_counts().sort_index()
            plt.bar(cluster_counts.index, cluster_counts.values)
            plt.xlabel('Cluster')
            plt.ylabel('Number of Customers')
            plt.title('Cluster Size Distribution')
            
            # Average characteristics by cluster
            plt.subplot(2, 3, 5)
            avg_income = self.clusters.groupby('Cluster')['annual_income'].mean()
            plt.bar(avg_income.index, avg_income.values)
            plt.xlabel('Cluster')
            plt.ylabel('Average Income ($)')
            plt.title('Average Income by Cluster')
            
            # Products vs Transactions
            plt.subplot(2, 3, 6)
            scatter = plt.scatter(self.clusters['num_products'], self.clusters['monthly_transactions'],
                                c=self.clusters['Cluster'], cmap='viridis', alpha=0.6)
            plt.xlabel('Number of Products')
            plt.ylabel('Monthly Transactions')
            plt.title('Products vs Transactions by Cluster')
            plt.colorbar(scatter)
            
            plt.tight_layout()
            plt.show()
            
            # Create detailed cluster comparison
            self._create_cluster_comparison_chart()
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
            raise
    
    def _create_cluster_comparison_chart(self) -> None:
        """Create detailed cluster comparison charts."""
        try:
            if self.cluster_profiles is None:
                self.analyze_clusters()
            
            # Prepare data for comparison
            comparison_data = []
            for cluster_id, profile in self.cluster_profiles.items():
                comparison_data.append({
                    'Cluster': f"Cluster {cluster_id}",
                    'Business_Label': profile['business_label'],
                    'Size': profile['size'],
                    'Percentage': profile['percentage'],
                    **profile['characteristics']
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Create subplot figure
            fig, axes = plt.subplots(2, 3, figsize=(20, 12))
            
            # Income comparison
            axes[0, 0].bar(comparison_df['Cluster'], comparison_df['avg_income'])
            axes[0, 0].set_title('Average Income by Cluster')
            axes[0, 0].set_ylabel('Income ($)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Balance comparison
            axes[0, 1].bar(comparison_df['Cluster'], comparison_df['avg_balance'])
            axes[0, 1].set_title('Average Balance by Cluster')
            axes[0, 1].set_ylabel('Balance ($)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Age comparison
            axes[0, 2].bar(comparison_df['Cluster'], comparison_df['avg_age'])
            axes[0, 2].set_title('Average Age by Cluster')
            axes[0, 2].set_ylabel('Age (years)')
            axes[0, 2].tick_params(axis='x', rotation=45)
            
            # Credit score comparison
            axes[1, 0].bar(comparison_df['Cluster'], comparison_df['avg_credit_score'])
            axes[1, 0].set_title('Average Credit Score by Cluster')
            axes[1, 0].set_ylabel('Credit Score')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Products comparison
            axes[1, 1].bar(comparison_df['Cluster'], comparison_df['avg_products'])
            axes[1, 1].set_title('Average Products by Cluster')
            axes[1, 1].set_ylabel('Number of Products')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            # Cluster size pie chart
            axes[1, 2].pie(comparison_df['Percentage'], labels=comparison_df['Business_Label'], 
                          autopct='%1.1f%%', startangle=90)
            axes[1, 2].set_title('Customer Distribution by Segment')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            logger.error(f"Error creating comparison chart: {e}")
            raise
    
    def generate_business_insights(self) -> str:
        """
        Generate comprehensive business insights and recommendations.
        
        Returns:
            str: Formatted business insights report
        """
        try:
            if self.cluster_profiles is None:
                self.analyze_clusters()
            
            logger.info("Generating business insights...")
            
            insights = []
            insights.append("="*80)
            insights.append("CUSTOMER SEGMENTATION BUSINESS INSIGHTS")
            insights.append("="*80)
            insights.append("")
            
            # Overall summary
            total_customers = sum(profile['size'] for profile in self.cluster_profiles.values())
            insights.append(f"EXECUTIVE SUMMARY")
            insights.append("-" * 40)
            insights.append(f"• Total customers analyzed: {total_customers:,}")
            insights.append(f"• Number of distinct segments: {len(self.cluster_profiles)}")
            insights.append("")
            
            # Cluster details
            for cluster_id, profile in self.cluster_profiles.items():
                insights.append(f"SEGMENT {cluster_id}: {profile['business_label'].upper()}")
                insights.append("-" * 50)
                insights.append(f"• Size: {profile['size']:,} customers ({profile['percentage']:.1f}%)")
                insights.append(f"• Average Income: ${profile['characteristics']['avg_income']:,.0f}")
                insights.append(f"• Average Balance: ${profile['characteristics']['avg_balance']:,.0f}")
                insights.append(f"• Average Age: {profile['characteristics']['avg_age']:.1f} years")
                insights.append(f"• Average Credit Score: {profile['characteristics']['avg_credit_score']:.0f}")
                insights.append(f"• Average Products: {profile['characteristics']['avg_products']:.1f}")
                insights.append(f"• Average Tenure: {profile['characteristics']['avg_tenure']:.1f} years")
                insights.append("")
                insights.append("RECOMMENDED STRATEGY:")
                insights.append(f"• {profile['strategy']}")
                insights.append("")
                
                # Revenue opportunity calculation
                estimated_revenue = (profile['characteristics']['avg_balance'] * 0.02 + 
                                   profile['characteristics']['avg_products'] * 50) * profile['size']
                insights.append(f"ESTIMATED ANNUAL REVENUE OPPORTUNITY: ${estimated_revenue:,.0f}")
                insights.append("")
            
            # Cross-segment insights
            insights.append("CROSS-SEGMENT INSIGHTS")
            insights.append("-" * 40)
            
            # Find highest value segment
            highest_value = max(self.cluster_profiles.items(), 
                              key=lambda x: x[1]['characteristics']['avg_balance'])
            insights.append(f"• Highest value segment: {highest_value[1]['business_label']} "
                           f"(${highest_value[1]['characteristics']['avg_balance']:,.0f} avg balance)")
            
            # Find largest segment
            largest_segment = max(self.cluster_profiles.items(), 
                                key=lambda x: x[1]['size'])
            insights.append(f"• Largest segment: {largest_segment[1]['business_label']} "
                           f"({largest_segment[1]['percentage']:.1f}% of customers)")
            
            # Find growth opportunity
            youngest_segment = min(self.cluster_profiles.items(), 
                                 key=lambda x: x[1]['characteristics']['avg_age'])
            insights.append(f"• Growth opportunity: {youngest_segment[1]['business_label']} "
                           f"(avg age {youngest_segment[1]['characteristics']['avg_age']:.1f})")
            
            insights.append("")
            
            # Actionable recommendations
            insights.append("ACTIONABLE RECOMMENDATIONS")
            insights.append("-" * 40)
            insights.append("1. IMMEDIATE ACTIONS (Next 30 days):")
            insights.append("   • Launch targeted campaigns for each segment")
            insights.append("   • Review product offerings for underserved segments")
            insights.append("   • Implement segment-specific communication strategies")
            insights.append("")
            
            insights.append("2. SHORT-TERM INITIATIVES (Next 90 days):")
            insights.append("   • Develop segment-specific product bundles")
            insights.append("   • Create loyalty programs for high-value customers")
            insights.append("   • Implement retention strategies for at-risk segments")
            insights.append("")
            
            insights.append("3. LONG-TERM STRATEGY (Next 12 months):")
            insights.append("   • Build predictive models for segment migration")
            insights.append("   • Develop lifecycle marketing automation")
            insights.append("   • Establish segment-specific KPIs and monitoring")
            insights.append("")
            
            report = "\n".join(insights)
            
            # Save report to file
            with open("customer_segmentation_insights.txt", "w") as f:
                f.write(report)
            
            print(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating business insights: {e}")
            raise
    
    def export_results(self, filename: str = "customer_segments.csv") -> None:
        """
        Export segmentation results to CSV.
        
        Args:
            filename (str): Output filename
        """
        try:
            if self.clusters is None:
                raise ValueError("No clustering performed. Call perform_kmeans_clustering() first.")
            
            # Merge with original data for complete export
            export_data = self.data.copy()
            cluster_mapping = dict(zip(self.processed_data.index, self.clusters['Cluster']))
            export_data['Cluster'] = export_data.index.map(cluster_mapping)
            
            # Add cluster labels
            if hasattr(self, 'cluster_profiles'):
                label_mapping = {k: v['business_label'] for k, v in self.cluster_profiles.items()}
                export_data['Segment_Label'] = export_data['Cluster'].map(label_mapping)
            
            export_data.to_csv(filename, index=False)
            logger.info(f"Results exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            raise

def main():
    """Main function to run customer segmentation analysis from command line."""
    try:
        parser = argparse.ArgumentParser(
            description="Perform customer segmentation analysis on banking data"
        )
        parser.add_argument(
            '--data', type=str, default='synthetic_bank_data.csv',
            help='Path to customer data CSV file (default: synthetic_bank_data.csv)'
        )
        parser.add_argument(
            '--clusters', type=int, default=None,
            help='Number of clusters (default: auto-determine optimal)'
        )
        parser.add_argument(
            '--output', type=str, default='customer_segments.csv',
            help='Output filename for results (default: customer_segments.csv)'
        )
        
        args = parser.parse_args()
        
        # Initialize segmentation analyzer
        segmenter = CustomerSegmentation()
        
        # Load data
        segmenter.load_data(args.data)
        
        # Perform RFM analysis
        segmenter.perform_rfm_analysis()
        
        # Perform clustering
        segmenter.perform_kmeans_clustering(args.clusters)
        
        # Analyze clusters
        segmenter.analyze_clusters()
        
        # Create visualizations
        segmenter.visualize_clusters()
        
        # Generate business insights
        segmenter.generate_business_insights()
        
        # Export results
        segmenter.export_results(args.output)
        
        print("\n" + "="*60)
        print("CUSTOMER SEGMENTATION ANALYSIS COMPLETED")
        print("="*60)
        print(f"Results saved to: {args.output}")
        print("Business insights saved to: customer_segmentation_insights.txt")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
