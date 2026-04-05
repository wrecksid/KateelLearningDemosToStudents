"""
Data Fetcher Module for Portfolio Optimization
Fetches real-time stock data from Yahoo Finance with comprehensive error handling
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataFetcher:
    """
    Comprehensive data fetching class for Yahoo Finance data
    """
    
    def __init__(self, risk_free_rate: float = 0.065):
        """
        Initialize DataFetcher
        
        Args:
            risk_free_rate: Current risk-free rate (Indian 10Y G-Sec yield ~6.5%)
        """
        self.risk_free_rate = risk_free_rate
        self.data_cache = {}
        
    def fetch_stock_data(self, 
                        tickers: List[str], 
                        period: str = "2y",
                        interval: str = "1d") -> pd.DataFrame:
        """
        Fetch stock price data for given tickers with error handling
        
        Args:
            tickers: List of stock symbols
            period: Data period (1y, 2y, 5y, max)
            interval: Data interval (1d, 1wk, 1mo)
            
        Returns:
            DataFrame with adjusted closing prices
        """
        try:
            logger.info(f"Fetching data for {len(tickers)} stocks over {period} period")
            
            # Download data
            data = yf.download(tickers, period=period, interval=interval, 
                             group_by='ticker', auto_adjust=True, 
                             prepost=True, threads=True)
            
            if data.empty:
                raise ValueError("No data retrieved from Yahoo Finance")
                
            # Extract adjusted closing prices
            if len(tickers) == 1:
                prices = data['Close'].to_frame()
                prices.columns = tickers
            else:
                prices = pd.DataFrame()
                for ticker in tickers:
                    try:
                        if ticker in data.columns.levels[0]:
                            prices[ticker] = data[ticker]['Close']
                        else:
                            logger.warning(f"No data found for {ticker}")
                    except KeyError:
                        logger.warning(f"Error processing {ticker}")
                        continue
            
            # Remove columns with insufficient data
            min_data_points = 252  # 1 year of trading days
            prices = prices.dropna(thresh=len(prices) * 0.7, axis=1)  # Keep columns with 70% data
            # Use explicit forward/backward fill methods for compatibility across pandas versions
            prices = prices.ffill().bfill()
            
            if prices.empty:
                raise ValueError("No valid price data after cleaning")
                
            logger.info(f"Successfully fetched data for {len(prices.columns)} stocks")
            logger.info(f"Date range: {prices.index[0]} to {prices.index[-1]}")
            
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching stock data: {str(e)}")
            raise
    
    def calculate_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily returns from price data
        
        Args:
            prices: DataFrame with stock prices
            
        Returns:
            DataFrame with daily returns
        """
        try:
            returns = prices.pct_change().dropna()
            
            # Remove extreme outliers (beyond 3 standard deviations)
            for col in returns.columns:
                mean = returns[col].mean()
                std = returns[col].std()
                returns[col] = returns[col].clip(lower=mean - 3*std, upper=mean + 3*std)
            
            logger.info(f"Calculated returns for {len(returns.columns)} stocks")
            logger.info(f"Return data from {returns.index[0]} to {returns.index[-1]}")
            
            return returns
            
        except Exception as e:
            logger.error(f"Error calculating returns: {str(e)}")
            raise
    
    def get_stock_info(self, tickers: List[str]) -> Dict:
        """
        Get additional stock information (sector, market cap, etc.)
        
        Args:
            tickers: List of stock symbols
            
        Returns:
            Dictionary with stock information
        """
        stock_info = {}
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                stock_info[ticker] = {
                    'name': info.get('longName', ticker),
                    'sector': info.get('sector', 'Unknown'),
                    'industry': info.get('industry', 'Unknown'),
                    'market_cap': info.get('marketCap', 0),
                    'currency': info.get('currency', 'INR')
                }
                
            except Exception as e:
                logger.warning(f"Could not fetch info for {ticker}: {str(e)}")
                stock_info[ticker] = {
                    'name': ticker,
                    'sector': 'Unknown',
                    'industry': 'Unknown',
                    'market_cap': 0,
                    'currency': 'INR'
                }
        
        return stock_info
    
    def validate_data_quality(self, returns: pd.DataFrame) -> Dict:
        """
        Validate data quality and provide statistics
        
        Args:
            returns: DataFrame with returns data
            
        Returns:
            Dictionary with data quality metrics
        """
        quality_metrics = {}
        
        for col in returns.columns:
            series = returns[col]
            quality_metrics[col] = {
                'missing_data_pct': series.isnull().sum() / len(series) * 100,
                'zero_returns_pct': (series == 0).sum() / len(series) * 100,
                'extreme_values': ((series.abs() > 0.15).sum()),  # Returns > 15%
                'data_points': len(series),
                'start_date': series.index[0],
                'end_date': series.index[-1]
            }
        
        return quality_metrics
    
    def get_market_data(self, benchmark: str = "^NSEI") -> pd.DataFrame:
        """
        Get benchmark market data (NIFTY 50)
        
        Args:
            benchmark: Benchmark symbol
            
        Returns:
            DataFrame with benchmark data
        """
        try:
            benchmark_data = yf.download(benchmark, period="2y", interval="1d")
            benchmark_returns = benchmark_data['Adj Close'].pct_change().dropna()
            
            logger.info(f"Fetched benchmark data for {benchmark}")
            return benchmark_returns.to_frame('NIFTY50')
            
        except Exception as e:
            logger.error(f"Error fetching benchmark data: {str(e)}")
            return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    from nifty50_tickers import NIFTY50_TICKERS
    
    # Initialize data fetcher
    fetcher = DataFetcher()
    
    # Fetch data for first 10 NIFTY stocks (for testing)
    test_tickers = NIFTY50_TICKERS[:10]
    
    try:
        # Fetch price data
        prices = fetcher.fetch_stock_data(test_tickers, period="1y")
        print(f"Fetched price data shape: {prices.shape}")
        
        # Calculate returns
        returns = fetcher.calculate_returns(prices)
        print(f"Returns data shape: {returns.shape}")
        
        # Get stock info
        stock_info = fetcher.get_stock_info(test_tickers)
        print(f"Stock info for {len(stock_info)} stocks")
        
        # Validate data quality
        quality = fetcher.validate_data_quality(returns)
        print("Data quality check completed")
        
    except Exception as e:
        print(f"Error: {e}")
