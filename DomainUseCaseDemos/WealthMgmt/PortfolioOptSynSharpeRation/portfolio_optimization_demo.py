"""
Portfolio Optimization Demo
==========================

This module demonstrates portfolio optimization techniques using Modern Portfolio Theory.
It includes efficient frontier calculation, risk-return optimization, and Sharpe ratio maximization.

Author: AI Assistant for Financial Analytics Course
Date: July 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
import argparse
import logging
import sys
import warnings
from datetime import datetime
import os

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set style for plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PortfolioOptimizer:
    """
    Portfolio optimization using Modern Portfolio Theory.
    
    This class implements various portfolio optimization techniques including:
    - Mean-variance optimization
    - Efficient frontier calculation
    - Sharpe ratio maximization
    - Risk parity
    """
    
    def __init__(self, data_file='syntheticdata.csv'):
        """
        Initialize the portfolio optimizer.
        
        Parameters:
        -----------
        data_file : str, default 'syntheticdata.csv'
            Path to the synthetic data file
        """
        self.data_file = data_file
        self.returns_data = None
        self.mean_returns = None
        self.cov_matrix = None
        self.risk_free_rate = None
        self.assets = None
        
    def load_and_prepare_data(self):
        """Load and prepare data for portfolio optimization."""
        try:
            logger.info(f"Loading data from {self.data_file}")
            
            if not os.path.exists(self.data_file):
                raise FileNotFoundError(f"Data file {self.data_file} not found. Please run generate_synthetic_data.py first.")
            
            # Load data
            df = pd.read_csv(self.data_file)
            df['date'] = pd.to_datetime(df['date'])
            
            logger.info(f"Loaded {len(df)} rows of data")
            logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
            logger.info(f"Number of assets: {df['symbol'].nunique()}")
            
            # Pivot to get returns matrix
            returns_pivot = df.pivot(index='date', columns='symbol', values='daily_return')
            returns_pivot = returns_pivot.dropna()
            
            # Store data
            self.returns_data = returns_pivot
            self.mean_returns = returns_pivot.mean() * 252  # Annualized returns
            self.cov_matrix = returns_pivot.cov() * 252     # Annualized covariance
            self.risk_free_rate = df['risk_free_rate'].iloc[0] * 252  # Annualized
            self.assets = list(returns_pivot.columns)
            
            logger.info("Data preparation completed successfully")
            
            # Display summary statistics
            self._display_summary_stats(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _display_summary_stats(self, df):
        """Display summary statistics of the data."""
        print("\n" + "="*60)
        print("PORTFOLIO DATA SUMMARY")
        print("="*60)
        
        print(f"📊 Dataset Overview:")
        print(f"   • Total observations: {len(df):,}")
        print(f"   • Number of assets: {df['symbol'].nunique()}")
        print(f"   • Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        print(f"   • Trading days: {len(df['date'].unique()):,}")
        
        print(f"\n📈 Return Statistics (Annualized):")
        print(f"   • Mean return range: {self.mean_returns.min():.2%} to {self.mean_returns.max():.2%}")
        print(f"   • Average volatility: {np.sqrt(np.diag(self.cov_matrix)).mean():.2%}")
        print(f"   • Risk-free rate: {self.risk_free_rate:.2%}")
        
        print(f"\n🏢 Sector Distribution:")
        sector_counts = df.groupby('symbol')['sector'].first().value_counts()
        for sector, count in sector_counts.head().items():
            print(f"   • {sector}: {count} assets")
    
    def calculate_portfolio_performance(self, weights):
        """
        Calculate portfolio return, volatility, and Sharpe ratio.
        
        Parameters:
        -----------
        weights : array-like
            Portfolio weights
            
        Returns:
        --------
        tuple
            (return, volatility, sharpe_ratio)
        """
        try:
            weights = np.array(weights)
            
            # Portfolio return
            portfolio_return = np.sum(weights * self.mean_returns)
            
            # Portfolio volatility
            portfolio_variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
            portfolio_volatility = np.sqrt(portfolio_variance)
            
            # Sharpe ratio
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            
            return portfolio_return, portfolio_volatility, sharpe_ratio
            
        except Exception as e:
            logger.error(f"Error calculating portfolio performance: {str(e)}")
            raise
    
    def optimize_sharpe_ratio(self):
        """
        Optimize portfolio for maximum Sharpe ratio.
        
        Returns:
        --------
        dict
            Optimization results
        """
        try:
            logger.info("Optimizing for maximum Sharpe ratio...")
            
            n_assets = len(self.assets)
            
            # Objective function (negative Sharpe ratio for minimization)
            def negative_sharpe(weights):
                _, volatility, sharpe = self.calculate_portfolio_performance(weights)
                return -sharpe
            
            # Constraints
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Weights sum to 1
            bounds = tuple((0, 1) for _ in range(n_assets))  # Long-only
            
            # Initial guess (equal weights)
            initial_guess = np.array([1/n_assets] * n_assets)
            
            # Optimize
            result = minimize(negative_sharpe, initial_guess, method='SLSQP',
                            bounds=bounds, constraints=constraints)
            
            if not result.success:
                logger.warning("Optimization did not converge successfully")
            
            # Calculate performance
            optimal_weights = result.x
            ret, vol, sharpe = self.calculate_portfolio_performance(optimal_weights)
            
            optimization_result = {
                'weights': optimal_weights,
                'return': ret,
                'volatility': vol,
                'sharpe_ratio': sharpe,
                'success': result.success
            }
            
            logger.info(f"Optimal Sharpe ratio: {sharpe:.4f}")
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error optimizing Sharpe ratio: {str(e)}")
            raise
    
    def optimize_minimum_variance(self):
        """
        Optimize portfolio for minimum variance.
        
        Returns:
        --------
        dict
            Optimization results
        """
        try:
            logger.info("Optimizing for minimum variance...")
            
            n_assets = len(self.assets)
            
            # Objective function (portfolio variance)
            def portfolio_variance(weights):
                return np.dot(weights.T, np.dot(self.cov_matrix, weights))
            
            # Constraints
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = tuple((0, 1) for _ in range(n_assets))
            
            # Initial guess
            initial_guess = np.array([1/n_assets] * n_assets)
            
            # Optimize
            result = minimize(portfolio_variance, initial_guess, method='SLSQP',
                            bounds=bounds, constraints=constraints)
            
            # Calculate performance
            optimal_weights = result.x
            ret, vol, sharpe = self.calculate_portfolio_performance(optimal_weights)
            
            optimization_result = {
                'weights': optimal_weights,
                'return': ret,
                'volatility': vol,
                'sharpe_ratio': sharpe,
                'success': result.success
            }
            
            logger.info(f"Minimum variance: {vol:.4f}")
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error optimizing minimum variance: {str(e)}")
            raise
    
    def calculate_efficient_frontier(self, n_portfolios=100):
        """
        Calculate the efficient frontier.
        
        Parameters:
        -----------
        n_portfolios : int, default 100
            Number of portfolios to calculate
            
        Returns:
        --------
        pd.DataFrame
            Efficient frontier data
        """
        try:
            logger.info(f"Calculating efficient frontier with {n_portfolios} portfolios...")
            
            # Target returns
            min_ret = self.mean_returns.min()
            max_ret = self.mean_returns.max()
            target_returns = np.linspace(min_ret, max_ret, n_portfolios)
            
            efficient_portfolios = []
            
            n_assets = len(self.assets)
            
            for target_ret in target_returns:
                # Objective function (minimize variance)
                def portfolio_variance(weights):
                    return np.dot(weights.T, np.dot(self.cov_matrix, weights))
                
                # Constraints
                constraints = [
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights sum to 1
                    {'type': 'eq', 'fun': lambda x: np.sum(x * self.mean_returns) - target_ret}  # Target return
                ]
                bounds = tuple((0, 1) for _ in range(n_assets))
                
                # Initial guess
                initial_guess = np.array([1/n_assets] * n_assets)
                
                try:
                    result = minimize(portfolio_variance, initial_guess, method='SLSQP',
                                    bounds=bounds, constraints=constraints)
                    
                    if result.success:
                        weights = result.x
                        ret, vol, sharpe = self.calculate_portfolio_performance(weights)
                        
                        efficient_portfolios.append({
                            'return': ret,
                            'volatility': vol,
                            'sharpe_ratio': sharpe,
                            'weights': weights
                        })
                except:
                    continue
            
            efficient_frontier = pd.DataFrame(efficient_portfolios)
            logger.info(f"Calculated {len(efficient_frontier)} efficient portfolios")
            
            return efficient_frontier
            
        except Exception as e:
            logger.error(f"Error calculating efficient frontier: {str(e)}")
            raise
    
    def plot_efficient_frontier(self, efficient_frontier, sharpe_optimal, min_var_optimal):
        """Plot the efficient frontier with optimal portfolios."""
        try:
            plt.figure(figsize=(12, 8))
            
            # Plot efficient frontier
            plt.scatter(efficient_frontier['volatility'], efficient_frontier['return'], 
                       c=efficient_frontier['sharpe_ratio'], cmap='viridis', alpha=0.7, s=50)
            plt.colorbar(label='Sharpe Ratio')
            
            # Plot optimal portfolios
            plt.scatter(sharpe_optimal['volatility'], sharpe_optimal['return'], 
                       color='red', s=200, marker='*', label='Max Sharpe Ratio', edgecolors='black')
            plt.scatter(min_var_optimal['volatility'], min_var_optimal['return'], 
                       color='blue', s=200, marker='*', label='Min Variance', edgecolors='black')
            
            # Plot individual assets
            individual_returns = self.mean_returns.values
            individual_volatilities = np.sqrt(np.diag(self.cov_matrix))
            plt.scatter(individual_volatilities, individual_returns, 
                       color='gray', alpha=0.6, s=30, label='Individual Assets')
            
            plt.xlabel('Volatility (Standard Deviation)')
            plt.ylabel('Expected Return')
            plt.title('Efficient Frontier - Portfolio Optimization')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('efficient_frontier.png', dpi=300, bbox_inches='tight')
            plt.show()
            
        except Exception as e:
            logger.error(f"Error plotting efficient frontier: {str(e)}")
            raise
    
    def plot_portfolio_composition(self, portfolio_result, title):
        """Plot portfolio composition pie chart."""
        try:
            weights = portfolio_result['weights']
            
            # Convert to pandas Series indexed by asset names for convenient selection
            weights_series = pd.Series(np.array(weights), index=self.assets)
            significant_weights = weights_series[weights_series > 0.01]
            
            # Fallback: if no weights exceed threshold, use top 5 by weight
            if significant_weights.empty:
                logger.warning("No assets exceed 1% threshold; showing top 5 holdings instead")
                significant_weights = weights_series.nlargest(5)

            if len(significant_weights) > 10:
                # Group smaller weights
                top_weights = significant_weights.nlargest(9)
                top_assets = top_weights.index.tolist()
                other_weight = significant_weights.drop(top_weights.index).sum()

                plot_weights = list(top_weights.values) + [other_weight]
                plot_assets = top_assets + ['Others']
            else:
                plot_weights = significant_weights.values.tolist()
                plot_assets = significant_weights.index.tolist()
            
            plt.figure(figsize=(10, 8))
            colors = plt.cm.Set3(np.linspace(0, 1, len(plot_weights)))
            
            wedges, texts, autotexts = plt.pie(plot_weights, labels=plot_assets, autopct='%1.1f%%',
                                              colors=colors, startangle=90)
            
            plt.title(f'{title}\nExpected Return: {portfolio_result["return"]:.2%}, '
                     f'Volatility: {portfolio_result["volatility"]:.2%}, '
                     f'Sharpe Ratio: {portfolio_result["sharpe_ratio"]:.3f}')
            
            plt.axis('equal')
            plt.tight_layout()
            
            # Save plot
            filename = title.lower().replace(' ', '_').replace('-', '_') + '_composition.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.show()
            
        except Exception as e:
            logger.error(f"Error plotting portfolio composition: {str(e)}")
            raise
    
    def generate_portfolio_report(self, sharpe_optimal, min_var_optimal, efficient_frontier):
        """Generate a comprehensive portfolio analysis report."""
        try:
            print("\n" + "="*80)
            print("PORTFOLIO OPTIMIZATION REPORT")
            print("="*80)
            
            print(f"\n🎯 OPTIMAL PORTFOLIOS SUMMARY")
            print("-" * 40)
            
            print(f"\n📈 Maximum Sharpe Ratio Portfolio:")
            print(f"   • Expected Return: {sharpe_optimal['return']:.2%}")
            print(f"   • Volatility: {sharpe_optimal['volatility']:.2%}")
            print(f"   • Sharpe Ratio: {sharpe_optimal['sharpe_ratio']:.4f}")
            
            print(f"\n📉 Minimum Variance Portfolio:")
            print(f"   • Expected Return: {min_var_optimal['return']:.2%}")
            print(f"   • Volatility: {min_var_optimal['volatility']:.2%}")
            print(f"   • Sharpe Ratio: {min_var_optimal['sharpe_ratio']:.4f}")
            
            # Top holdings
            print(f"\n🏆 TOP HOLDINGS - Maximum Sharpe Ratio Portfolio:")
            sharpe_weights = pd.Series(sharpe_optimal['weights'], index=self.assets)
            top_holdings = sharpe_weights.nlargest(5)
            for asset, weight in top_holdings.items():
                if weight > 0.01:  # Only show weights > 1%
                    print(f"   • {asset}: {weight:.1%}")
            
            print(f"\n🛡️ TOP HOLDINGS - Minimum Variance Portfolio:")
            minvar_weights = pd.Series(min_var_optimal['weights'], index=self.assets)
            top_holdings = minvar_weights.nlargest(5)
            for asset, weight in top_holdings.items():
                if weight > 0.01:
                    print(f"   • {asset}: {weight:.1%}")
            
            # Efficient frontier stats
            print(f"\n📊 EFFICIENT FRONTIER STATISTICS:")
            print(f"   • Number of efficient portfolios: {len(efficient_frontier)}")
            print(f"   • Return range: {efficient_frontier['return'].min():.2%} to {efficient_frontier['return'].max():.2%}")
            print(f"   • Volatility range: {efficient_frontier['volatility'].min():.2%} to {efficient_frontier['volatility'].max():.2%}")
            print(f"   • Maximum Sharpe ratio: {efficient_frontier['sharpe_ratio'].max():.4f}")
            
            # Risk-return comparison
            equal_weight_return = self.mean_returns.mean()
            equal_weight_vol = np.sqrt(np.dot(np.ones(len(self.assets))/len(self.assets), 
                                             np.dot(self.cov_matrix, np.ones(len(self.assets))/len(self.assets))))
            equal_weight_sharpe = (equal_weight_return - self.risk_free_rate) / equal_weight_vol
            
            print(f"\n⚖️ COMPARISON WITH EQUAL-WEIGHT PORTFOLIO:")
            print(f"   • Equal-weight return: {equal_weight_return:.2%}")
            print(f"   • Equal-weight volatility: {equal_weight_vol:.2%}")
            print(f"   • Equal-weight Sharpe ratio: {equal_weight_sharpe:.4f}")
            
            print(f"\n💡 IMPROVEMENT FROM OPTIMIZATION:")
            sharpe_improvement = (sharpe_optimal['sharpe_ratio'] - equal_weight_sharpe) / equal_weight_sharpe * 100
            vol_reduction = (equal_weight_vol - min_var_optimal['volatility']) / equal_weight_vol * 100
            print(f"   • Sharpe ratio improvement: {sharpe_improvement:.1f}%")
            print(f"   • Volatility reduction (min-var): {vol_reduction:.1f}%")
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def run_optimization_demo(self):
        """Run the complete portfolio optimization demonstration."""
        try:
            print("🚀 Starting Portfolio Optimization Demo...")
            
            # Load data
            self.load_and_prepare_data()
            
            # Optimize portfolios
            sharpe_optimal = self.optimize_sharpe_ratio()
            min_var_optimal = self.optimize_minimum_variance()
            
            # Calculate efficient frontier
            efficient_frontier = self.calculate_efficient_frontier()
            
            # Generate visualizations
            print("\n📊 Generating visualizations...")
            self.plot_efficient_frontier(efficient_frontier, sharpe_optimal, min_var_optimal)
            self.plot_portfolio_composition(sharpe_optimal, "Maximum Sharpe Ratio Portfolio")
            self.plot_portfolio_composition(min_var_optimal, "Minimum Variance Portfolio")
            
            # Generate report
            self.generate_portfolio_report(sharpe_optimal, min_var_optimal, efficient_frontier)
            
            print(f"\n✅ Portfolio optimization demo completed successfully!")
            print(f"📁 Charts saved as PNG files in current directory")
            
            return {
                'sharpe_optimal': sharpe_optimal,
                'min_var_optimal': min_var_optimal,
                'efficient_frontier': efficient_frontier
            }
            
        except Exception as e:
            logger.error(f"Error running optimization demo: {str(e)}")
            raise

def main():
    """Main function to run the portfolio optimization demo."""
    parser = argparse.ArgumentParser(description='Portfolio Optimization Demo')
    parser.add_argument('--data-file', type=str, default='syntheticdata.csv',
                       help='Path to synthetic data file (default: syntheticdata.csv)')
    
    args = parser.parse_args()
    
    try:
        # Initialize optimizer
        optimizer = PortfolioOptimizer(data_file=args.data_file)
        
        # Run demo
        results = optimizer.run_optimization_demo()
        
        print("\n" + "="*60)
        print("🏦 REAL-WORLD APPLICATIONS FOR BANKS")
        print("="*60)
        print("""
        This portfolio optimization framework can be used by banks for:
        
        1. 💰 ASSET MANAGEMENT:
           • Optimize client portfolios based on risk tolerance
           • Create model portfolios for different investor profiles
           • Rebalance portfolios to maintain target allocations
        
        2. 🏛️ TREASURY MANAGEMENT:
           • Optimize bank's own investment portfolio
           • Manage liquidity across different asset classes
           • Hedge interest rate and credit risks
        
        3. 📋 PRODUCT DEVELOPMENT:
           • Design structured products and investment funds
           • Create risk-targeted investment solutions
           • Develop robo-advisor algorithms
        
        4. 🎯 RISK MANAGEMENT:
           • Set position limits and concentration limits
           • Stress test portfolios under different scenarios
           • Calculate Value-at-Risk (VaR) for trading books
        
        5. 💼 WEALTH MANAGEMENT:
           • Provide personalized investment advice
           • Create tax-efficient portfolio strategies
           • Implement ESG (Environmental, Social, Governance) constraints
        """)
        
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
