"""
Portfolio Optimizer - Main Module
Comprehensive portfolio optimization using Modern Portfolio Theory
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional
import warnings
import logging

# Import custom modules
from data_fetcher import DataFetcher
from risk_metrics import RiskMetrics
from nifty50_tickers import NIFTY50_TICKERS, SECTOR_MAPPING

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortfolioOptimizer:
    """
    Comprehensive Portfolio Optimization Engine
    """
    
    def __init__(self, risk_free_rate: float = 0.065):
        """
        Initialize Portfolio Optimizer
        
        Args:
            risk_free_rate: Risk-free rate (Indian 10Y G-Sec yield)
        """
        self.risk_free_rate = risk_free_rate
        self.data_fetcher = DataFetcher(risk_free_rate)
        self.risk_metrics = RiskMetrics()
        self.returns = None
        self.mean_returns = None
        self.cov_matrix = None
        self.num_assets = 0
        
    def load_data(self, tickers: List[str], period: str = "2y") -> None:
        """
        Load and prepare data for optimization
        
        Args:
            tickers: List of stock symbols
            period: Data period
        """
        try:
            logger.info("Loading stock data...")
            
            # Fetch price data
            prices = self.data_fetcher.fetch_stock_data(tickers, period)
            
            # Calculate returns
            self.returns = self.data_fetcher.calculate_returns(prices)
            
            # Calculate expected returns and covariance matrix
            self.mean_returns = self.returns.mean()
            self.cov_matrix = self.returns.cov()
            self.num_assets = len(self.returns.columns)
            
            logger.info(f"Data loaded successfully for {self.num_assets} assets")
            logger.info(f"Data range: {self.returns.index[0]} to {self.returns.index[-1]}")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def portfolio_performance(self, weights: np.array) -> Tuple[float, float, float]:
        """
        Calculate portfolio performance metrics
        
        Args:
            weights: Portfolio weights
            
        Returns:
            Tuple of (return, volatility, sharpe_ratio)
        """
        portfolio_return = np.sum(self.mean_returns * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def negative_sharpe_ratio(self, weights: np.array) -> float:
        """Objective function to minimize (negative Sharpe ratio)"""
        _, _, sharpe = self.portfolio_performance(weights)
        return -sharpe
    
    def portfolio_volatility(self, weights: np.array) -> float:
        """Calculate portfolio volatility"""
        return np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
    
    def optimize_portfolio(self, objective: str = 'sharpe') -> Dict:
        """
        Optimize portfolio based on objective
        
        Args:
            objective: Optimization objective ('sharpe', 'min_vol', 'max_return')
            
        Returns:
            Dictionary with optimization results
        """
        try:
            # Constraints and bounds
            constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            bounds = tuple((0, 0.3) for _ in range(self.num_assets))  # Max 30% in any single stock
            
            # Initial guess (equal weights)
            initial_guess = np.array([1/self.num_assets] * self.num_assets)
            
            # Optimization based on objective
            if objective == 'sharpe':
                result = minimize(self.negative_sharpe_ratio, initial_guess,
                                method='SLSQP', bounds=bounds, constraints=constraints)
            elif objective == 'min_vol':
                result = minimize(self.portfolio_volatility, initial_guess,
                                method='SLSQP', bounds=bounds, constraints=constraints)
            elif objective == 'max_return':
                result = minimize(lambda x: -np.sum(self.mean_returns * x) * 252, initial_guess,
                                method='SLSQP', bounds=bounds, constraints=constraints)
            else:
                raise ValueError("Invalid objective. Choose 'sharpe', 'min_vol', or 'max_return'")
            
            if not result.success:
                logger.warning("Optimization did not converge properly")
            
            # Calculate performance metrics
            optimal_weights = result.x
            performance = self.portfolio_performance(optimal_weights)
            
            # Create results dictionary
            results = {
                'weights': optimal_weights,
                'expected_return': performance[0],
                'volatility': performance[1],
                'sharpe_ratio': performance[2],
                'objective': objective,
                'success': result.success,
                'message': result.message if hasattr(result, 'message') else 'Optimization completed'
            }
            
            logger.info(f"Optimization completed - {objective.upper()}")
            logger.info(f"Expected Return: {performance[0]:.2%}")
            logger.info(f"Volatility: {performance[1]:.2%}")
            logger.info(f"Sharpe Ratio: {performance[2]:.4f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in portfolio optimization: {e}")
            raise
    
    def generate_efficient_frontier(self, num_portfolios: int = 100) -> pd.DataFrame:
        """
        Generate efficient frontier
        
        Args:
            num_portfolios: Number of portfolios to generate
            
        Returns:
            DataFrame with efficient frontier data
        """
        try:
            logger.info("Generating efficient frontier...")
            
            # Get min and max possible returns
            min_vol_portfolio = self.optimize_portfolio('min_vol')
            max_ret_portfolio = self.optimize_portfolio('max_return')
            
            min_ret = min_vol_portfolio['expected_return']
            max_ret = max_ret_portfolio['expected_return']
            
            target_returns = np.linspace(min_ret, max_ret, num_portfolios)
            
            efficient_portfolios = []
            
            for target_return in target_returns:
                try:
                    # Constraints for target return
                    constraints = [
                        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                        {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) * 252 - target_return}
                    ]
                    
                    bounds = tuple((0, 0.3) for _ in range(self.num_assets))
                    initial_guess = np.array([1/self.num_assets] * self.num_assets)
                    
                    result = minimize(self.portfolio_volatility, initial_guess,
                                    method='SLSQP', bounds=bounds, constraints=constraints)
                    
                    if result.success:
                        weights = result.x
                        ret, vol, sharpe = self.portfolio_performance(weights)
                        
                        efficient_portfolios.append({
                            'Return': ret,
                            'Volatility': vol,
                            'Sharpe_Ratio': sharpe,
                            'Weights': weights
                        })
                        
                except:
                    continue
            
            efficient_df = pd.DataFrame(efficient_portfolios)
            logger.info(f"Generated {len(efficient_df)} efficient portfolios")
            
            return efficient_df
            
        except Exception as e:
            logger.error(f"Error generating efficient frontier: {e}")
            return pd.DataFrame()
    
    def monte_carlo_simulation(self, num_simulations: int = 10000) -> pd.DataFrame:
        """
        Monte Carlo simulation for portfolio optimization
        
        Args:
            num_simulations: Number of random portfolios to generate
            
        Returns:
            DataFrame with simulation results
        """
        try:
            logger.info(f"Running Monte Carlo simulation with {num_simulations} portfolios...")
            
            np.random.seed(42)
            results = []
            
            for _ in range(num_simulations):
                # Generate random weights
                weights = np.random.random(self.num_assets)
                weights = weights / np.sum(weights)
                
                # Calculate performance
                ret, vol, sharpe = self.portfolio_performance(weights)
                
                results.append({
                    'Return': ret,
                    'Volatility': vol,
                    'Sharpe_Ratio': sharpe,
                    'Weights': weights
                })
            
            results_df = pd.DataFrame(results)
            logger.info("Monte Carlo simulation completed")
            
            return results_df
            
        except Exception as e:
            logger.error(f"Error in Monte Carlo simulation: {e}")
            return pd.DataFrame()
    
    def create_portfolio_summary(self, optimized_portfolios: Dict) -> pd.DataFrame:
        """
        Create comprehensive portfolio summary
        
        Args:
            optimized_portfolios: Dictionary of optimized portfolios
            
        Returns:
            DataFrame with portfolio summary
        """
        summary_data = []
        
        for obj_type, portfolio in optimized_portfolios.items():
            if portfolio:
                weights = portfolio['weights']
                
                # Calculate comprehensive metrics
                portfolio_metrics = self.risk_metrics.calculate_portfolio_metrics(
                    self.returns, weights, self.risk_free_rate
                )
                
                summary_data.append({
                    'Portfolio Type': obj_type.replace('_', ' ').title(),
                    'Expected Return': f"{portfolio['expected_return']:.2%}",
                    'Volatility': f"{portfolio['volatility']:.2%}",
                    'Sharpe Ratio': f"{portfolio['sharpe_ratio']:.4f}",
                    'Max Drawdown': f"{portfolio_metrics.get('max_drawdown', 0):.2%}",
                    'VaR (95%)': f"{portfolio_metrics.get('var_95', 0):.2%}",
                    'Win Rate': f"{portfolio_metrics.get('win_rate', 0):.2%}",
                    'Top Holdings': self._get_top_holdings(weights)
                })
        
        return pd.DataFrame(summary_data)
    
    def _get_top_holdings(self, weights: np.array, top_n: int = 5) -> str:
        """Get top portfolio holdings as string"""
        holdings = pd.Series(weights, index=self.returns.columns)
        top_holdings = holdings.nlargest(top_n)
        
        holdings_str = ", ".join([f"{stock}: {weight:.1%}" 
                                for stock, weight in top_holdings.items()])
        return holdings_str
    
    def generate_allocation_report(self, weights: np.array) -> pd.DataFrame:
        """
        Generate detailed allocation report
        
        Args:
            weights: Portfolio weights
            
        Returns:
            DataFrame with allocation details
        """
        allocation_df = pd.DataFrame({
            'Stock': self.returns.columns,
            'Weight': weights,
            'Sector': [SECTOR_MAPPING.get(stock, 'Unknown') for stock in self.returns.columns]
        })
        
        # Add individual stock metrics
        individual_metrics = self.risk_metrics.calculate_individual_metrics(self.returns)
        allocation_df = allocation_df.merge(individual_metrics, left_on='Stock', right_index=True, how='left')
        
        # Sort by weight
        allocation_df = allocation_df.sort_values('Weight', ascending=False)
        
        return allocation_df

def main():
    """Main execution function"""
    try:
        print("=== NIFTY 50 Portfolio Optimization Demo ===")
        print("Initializing portfolio optimizer...")
        
        # Initialize optimizer
        optimizer = PortfolioOptimizer()
        
        # Load data (using top 20 NIFTY stocks for demo)
        demo_tickers = NIFTY50_TICKERS[:20]  # Limit for demo purposes
        print(f"Loading data for {len(demo_tickers)} stocks...")
        
        optimizer.load_data(demo_tickers, period="2y")
        
        print("\n=== OPTIMIZATION RESULTS ===")
        
        # Optimize portfolios with different objectives
        objectives = ['sharpe', 'min_vol', 'max_return']
        optimized_portfolios = {}
        
        for obj in objectives:
            print(f"\nOptimizing for {obj.replace('_', ' ').title()}...")
            result = optimizer.optimize_portfolio(obj)
            optimized_portfolios[obj] = result
        
        # Create portfolio summary
        summary = optimizer.create_portfolio_summary(optimized_portfolios)
        print("\n=== PORTFOLIO SUMMARY ===")
        print(summary.to_string(index=False))
        
        # Generate detailed allocation for Sharpe optimal portfolio
        if 'sharpe' in optimized_portfolios:
            sharpe_weights = optimized_portfolios['sharpe']['weights']
            allocation_report = optimizer.generate_allocation_report(sharpe_weights)
            
            print("\n=== MAXIMUM SHARPE RATIO PORTFOLIO ALLOCATION ===")
            significant_holdings = allocation_report[allocation_report['Weight'] > 0.01]  # >1%
            print(significant_holdings[['Stock', 'Weight', 'Sector', 'Annual Return', 'Annual Volatility', 'Sharpe Ratio']].to_string(index=False))
        
        # Calculate sector allocation
        if 'sharpe' in optimized_portfolios:
            allocation_df = optimizer.generate_allocation_report(sharpe_weights)
            sector_allocation = allocation_df.groupby('Sector')['Weight'].sum().sort_values(ascending=False)
            
            print("\n=== SECTOR ALLOCATION (Max Sharpe Portfolio) ===")
            for sector, weight in sector_allocation.items():
                if weight > 0.01:  # Show sectors with >1% allocation
                    print(f"{sector}: {weight:.2%}")
        
        print("\n=== DEMO COMPLETED SUCCESSFULLY ===")
        print("For detailed analysis and visualizations, run the Jupyter notebook.")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
