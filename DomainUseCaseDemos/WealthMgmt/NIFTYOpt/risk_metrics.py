"""
Risk Metrics Module for Portfolio Optimization
Comprehensive risk measurement and analysis functions
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class RiskMetrics:
    """
    Comprehensive risk analysis class
    """
    
    def __init__(self, confidence_level: float = 0.05):
        """
        Initialize RiskMetrics
        
        Args:
            confidence_level: Confidence level for VaR calculations (default 5%)
        """
        self.confidence_level = confidence_level
        
    def calculate_portfolio_metrics(self, 
                                  returns: pd.DataFrame, 
                                  weights: np.array,
                                  risk_free_rate: float = 0.065) -> Dict:
        """
        Calculate comprehensive portfolio metrics
        
        Args:
            returns: DataFrame with stock returns
            weights: Portfolio weights
            risk_free_rate: Risk-free rate (annual)
            
        Returns:
            Dictionary with portfolio metrics
        """
        try:
            # Portfolio returns
            portfolio_returns = (returns * weights).sum(axis=1)
            
            # Annual metrics
            annual_return = portfolio_returns.mean() * 252
            annual_volatility = portfolio_returns.std() * np.sqrt(252)
            
            # Risk-adjusted metrics
            excess_return = annual_return - risk_free_rate
            sharpe_ratio = excess_return / annual_volatility if annual_volatility != 0 else 0
            
            # Downside metrics
            downside_returns = portfolio_returns[portfolio_returns < 0]
            downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
            sortino_ratio = excess_return / downside_volatility if downside_volatility != 0 else 0
            
            # Maximum drawdown
            cumulative_returns = (1 + portfolio_returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            # Value at Risk (VaR) and Conditional VaR
            var_95 = np.percentile(portfolio_returns, self.confidence_level * 100)
            cvar_95 = portfolio_returns[portfolio_returns <= var_95].mean()
            
            # Skewness and Kurtosis
            skewness = stats.skew(portfolio_returns)
            kurtosis = stats.kurtosis(portfolio_returns)
            
            # Beta (if benchmark provided)
            metrics = {
                'annual_return': annual_return,
                'annual_volatility': annual_volatility,
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio,
                'max_drawdown': max_drawdown,
                'var_95': var_95,
                'cvar_95': cvar_95,
                'skewness': skewness,
                'kurtosis': kurtosis,
                'total_return': (1 + portfolio_returns).prod() - 1,
                'win_rate': (portfolio_returns > 0).sum() / len(portfolio_returns),
                'best_day': portfolio_returns.max(),
                'worst_day': portfolio_returns.min()
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating portfolio metrics: {e}")
            return {}
    
    def calculate_individual_metrics(self, returns: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate individual stock metrics
        
        Args:
            returns: DataFrame with stock returns
            
        Returns:
            DataFrame with individual stock metrics
        """
        metrics_df = pd.DataFrame(index=returns.columns)
        
        for stock in returns.columns:
            stock_returns = returns[stock].dropna()
            
            if len(stock_returns) == 0:
                continue
                
            metrics_df.loc[stock, 'Annual Return'] = stock_returns.mean() * 252
            metrics_df.loc[stock, 'Annual Volatility'] = stock_returns.std() * np.sqrt(252)
            metrics_df.loc[stock, 'Sharpe Ratio'] = (stock_returns.mean() * 252 - 0.065) / (stock_returns.std() * np.sqrt(252))
            metrics_df.loc[stock, 'Max Drawdown'] = self._calculate_max_drawdown(stock_returns)
            metrics_df.loc[stock, 'VaR 95%'] = np.percentile(stock_returns, 5)
            metrics_df.loc[stock, 'Skewness'] = stats.skew(stock_returns)
            metrics_df.loc[stock, 'Kurtosis'] = stats.kurtosis(stock_returns)
        
        return metrics_df.round(4)
    
    def _calculate_max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown for a return series"""
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        return drawdown.min()
    
    def correlation_analysis(self, returns: pd.DataFrame) -> Dict:
        """
        Perform correlation analysis
        
        Args:
            returns: DataFrame with stock returns
            
        Returns:
            Dictionary with correlation metrics
        """
        corr_matrix = returns.corr()
        
        # Average correlation
        avg_correlation = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()
        
        # Highest correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Stock1': corr_matrix.columns[i],
                    'Stock2': corr_matrix.columns[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs)
        highest_corr = corr_df.nlargest(10, 'Correlation')
        lowest_corr = corr_df.nsmallest(10, 'Correlation')
        
        return {
            'correlation_matrix': corr_matrix,
            'average_correlation': avg_correlation,
            'highest_correlations': highest_corr,
            'lowest_correlations': lowest_corr
        }
    
    def sector_analysis(self, returns: pd.DataFrame, sector_mapping: Dict) -> pd.DataFrame:
        """
        Analyze risk metrics by sector
        
        Args:
            returns: DataFrame with stock returns
            sector_mapping: Dictionary mapping stocks to sectors
            
        Returns:
            DataFrame with sector-wise metrics
        """
        sector_metrics = []
        
        sectors = set(sector_mapping.values())
        
        for sector in sectors:
            sector_stocks = [stock for stock, sec in sector_mapping.items() if sec == sector and stock in returns.columns]
            
            if not sector_stocks:
                continue
                
            sector_returns = returns[sector_stocks].mean(axis=1)  # Equal weight sector return
            
            metrics = {
                'Sector': sector,
                'Stocks Count': len(sector_stocks),
                'Annual Return': sector_returns.mean() * 252,
                'Annual Volatility': sector_returns.std() * np.sqrt(252),
                'Sharpe Ratio': (sector_returns.mean() * 252 - 0.065) / (sector_returns.std() * np.sqrt(252)),
                'Max Drawdown': self._calculate_max_drawdown(sector_returns),
                'VaR 95%': np.percentile(sector_returns, 5)
            }
            
            sector_metrics.append(metrics)
        
        return pd.DataFrame(sector_metrics).round(4)
    
    def stress_testing(self, returns: pd.DataFrame, weights: np.array) -> Dict:
        """
        Perform stress testing scenarios
        
        Args:
            returns: DataFrame with stock returns
            weights: Portfolio weights
            
        Returns:
            Dictionary with stress test results
        """
        portfolio_returns = (returns * weights).sum(axis=1)
        
        # Historical stress scenarios
        worst_day = portfolio_returns.min()
        worst_week = portfolio_returns.rolling(5).sum().min()
        worst_month = portfolio_returns.rolling(21).sum().min()
        
        # Monte Carlo stress testing
        np.random.seed(42)
        n_simulations = 10000
        
        # Simulate extreme market conditions
        stress_returns = []
        for _ in range(n_simulations):
            # Random shock to correlations and volatilities
            shock_multiplier = np.random.normal(1, 0.3, len(weights))
            shocked_weights = weights * shock_multiplier
            shocked_weights = shocked_weights / shocked_weights.sum()  # Renormalize
            
            sim_return = np.random.multivariate_normal(
                returns.mean().values,
                returns.cov().values * 2  # Double the covariance (stress scenario)
            )
            
            portfolio_return = np.dot(shocked_weights, sim_return)
            stress_returns.append(portfolio_return)
        
        stress_returns = np.array(stress_returns)
        
        return {
            'worst_day_historical': worst_day,
            'worst_week_historical': worst_week,
            'worst_month_historical': worst_month,
            'stress_var_95': np.percentile(stress_returns, 5),
            'stress_var_99': np.percentile(stress_returns, 1),
            'stress_expected_shortfall': stress_returns[stress_returns <= np.percentile(stress_returns, 5)].mean()
        }

# Example usage
if __name__ == "__main__":
    # Create sample data for testing
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-01-01', freq='D')
    returns = pd.DataFrame(
        np.random.normal(0.001, 0.02, (len(dates), 5)),
        index=dates,
        columns=['STOCK1', 'STOCK2', 'STOCK3', 'STOCK4', 'STOCK5']
    )
    
    # Equal weights
    weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    
    # Initialize risk metrics
    risk_calc = RiskMetrics()
    
    # Calculate portfolio metrics
    portfolio_metrics = risk_calc.calculate_portfolio_metrics(returns, weights)
    print("Portfolio Metrics:")
    for key, value in portfolio_metrics.items():
        print(f"{key}: {value:.4f}")
    
    # Individual stock metrics
    individual_metrics = risk_calc.calculate_individual_metrics(returns)
    print("\nIndividual Stock Metrics:")
    print(individual_metrics)
    
    # Correlation analysis
    corr_analysis = risk_calc.correlation_analysis(returns)
    print(f"\nAverage Correlation: {corr_analysis['average_correlation']:.4f}")
    print("Highest Correlations:")
    print(corr_analysis['highest_correlations'])
    print("Lowest Correlations:")
    print(corr_analysis['lowest_correlations'])
    # Sector analysis
    sector_mapping = {
        'STOCK1': 'Technology',
        'STOCK2': 'Finance',
        'STOCK3': 'Healthcare',
        'STOCK4': 'Consumer Goods',
        'STOCK5': 'Energy'
    }
    sector_metrics = risk_calc.sector_analysis(returns, sector_mapping)
    print("\nSector Metrics:")
    print(sector_metrics)
