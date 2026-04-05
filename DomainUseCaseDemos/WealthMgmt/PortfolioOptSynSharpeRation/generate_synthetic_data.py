"""
Portfolio Optimization - Synthetic Data Generator
===============================================

This module generates synthetic financial data for portfolio optimization analysis.
The data includes historical stock prices, returns, and market indicators for multiple assets.

Author: AI Assistant for Financial Analytics Course
Date: July 2025
"""

import pandas as pd
import numpy as np
from faker import Faker
import argparse
import logging
import sys
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PortfolioDataGenerator:
    """
    Generates synthetic portfolio data for financial analysis.
    
    This class creates realistic financial time series data including:
    - Multiple asset returns
    - Market indicators
    - Risk-free rates
    - Asset metadata
    """
    
    def __init__(self, locale='en_IN', seed=42):
        """
        Initialize the data generator.
        
        Parameters:
        -----------
        locale : str, default 'en_IN'
            Locale for faker library
        seed : int, default 42
            Random seed for reproducibility
        """
        self.fake = Faker(locale)
        Faker.seed(seed)
        np.random.seed(seed)
        self.locale = locale
        
    def generate_asset_metadata(self, n_assets=20):
        """
        Generate metadata for financial assets.
        
        Parameters:
        -----------
        n_assets : int, default 20
            Number of assets to generate
            
        Returns:
        --------
        pd.DataFrame
            Asset metadata including symbols, names, sectors, market cap
        """
        try:
            sectors = ['Technology', 'Healthcare', 'Finance', 'Consumer Goods', 
                      'Energy', 'Utilities', 'Real Estate', 'Materials', 
                      'Telecommunications', 'Industrials']
            
            assets = []
            for i in range(n_assets):
                asset = {
                    'symbol': f"STOCK_{i+1:02d}",
                    'company_name': self.fake.company(),
                    'sector': np.random.choice(sectors),
                    'market_cap': np.random.lognormal(mean=10, sigma=1.5),  # in millions
                    'listing_date': self.fake.date_between(start_date='-10y', end_date='-1y')
                }
                assets.append(asset)
                
            return pd.DataFrame(assets)
            
        except Exception as e:
            logger.error(f"Error generating asset metadata: {str(e)}")
            raise
    
    def generate_market_data(self, start_date, end_date, n_assets=20):
        """
        Generate synthetic market data with realistic price movements.
        
        Parameters:
        -----------
        start_date : str or datetime
            Start date for data generation
        end_date : str or datetime  
            End date for data generation
        n_assets : int, default 20
            Number of assets
            
        Returns:
        --------
        pd.DataFrame
            Market data with prices and returns
        """
        try:
            # Create date range
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            date_range = date_range[date_range.dayofweek < 5]  # Remove weekends
            
            n_days = len(date_range)
            logger.info(f"Generating data for {n_days} trading days and {n_assets} assets")
            
            # Generate asset metadata
            asset_metadata = self.generate_asset_metadata(n_assets)
            
            # Initialize price matrix
            data = []
            
            # Market parameters
            market_volatility = 0.15
            risk_free_rate = 0.06
            
            for idx, row in asset_metadata.iterrows():
                symbol = row['symbol']
                sector = row['sector']
                
                # Sector-specific parameters
                sector_params = self._get_sector_parameters(sector)
                
                # Generate price series using geometric Brownian motion
                initial_price = np.random.uniform(50, 500)
                mu = sector_params['expected_return']
                sigma = sector_params['volatility']
                
                # Generate daily returns
                dt = 1/252  # Daily time step
                shocks = np.random.normal(0, 1, n_days)
                returns = mu * dt + sigma * np.sqrt(dt) * shocks
                
                # Calculate prices
                prices = [initial_price]
                for i in range(1, n_days):
                    price = prices[-1] * np.exp(returns[i])
                    prices.append(price)
                
                # Create data for this asset
                for i, date in enumerate(date_range):
                    data.append({
                        'date': date,
                        'symbol': symbol,
                        'company_name': row['company_name'],
                        'sector': sector,
                        'market_cap': row['market_cap'],
                        'price': round(prices[i], 2),
                        'daily_return': round(returns[i], 6) if i > 0 else 0,
                        'volume': np.random.randint(10000, 1000000),
                        'risk_free_rate': risk_free_rate / 252,  # Daily risk-free rate
                        'market_return': round(np.random.normal(0.08/252, market_volatility/np.sqrt(252)), 6)
                    })
            
            df = pd.DataFrame(data)
            
            # Add some market-wide events (crashes, rallies)
            df = self._add_market_events(df, date_range)
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating market data: {str(e)}")
            raise
    
    def _get_sector_parameters(self, sector):
        """Get sector-specific financial parameters."""
        sector_params = {
            'Technology': {'expected_return': 0.12, 'volatility': 0.25},
            'Healthcare': {'expected_return': 0.10, 'volatility': 0.18},
            'Finance': {'expected_return': 0.09, 'volatility': 0.22},
            'Consumer Goods': {'expected_return': 0.08, 'volatility': 0.15},
            'Energy': {'expected_return': 0.07, 'volatility': 0.30},
            'Utilities': {'expected_return': 0.06, 'volatility': 0.12},
            'Real Estate': {'expected_return': 0.08, 'volatility': 0.20},
            'Materials': {'expected_return': 0.09, 'volatility': 0.25},
            'Telecommunications': {'expected_return': 0.07, 'volatility': 0.16},
            'Industrials': {'expected_return': 0.09, 'volatility': 0.19}
        }
        return sector_params.get(sector, {'expected_return': 0.08, 'volatility': 0.20})
    
    def _add_market_events(self, df, date_range):
        """Add market-wide events to make data more realistic."""
        try:
            # Add a few market crashes/rallies
            n_events = max(1, len(date_range) // 500)  # About 1 event per 2 years
            event_dates = np.random.choice(date_range[100:-100], n_events, replace=False)
            
            for event_date in event_dates:
                event_magnitude = np.random.uniform(-0.15, 0.10)  # -15% to +10%
                event_mask = df['date'] == event_date
                df.loc[event_mask, 'daily_return'] += event_magnitude
                df.loc[event_mask, 'market_return'] += event_magnitude
                
            return df
            
        except Exception as e:
            logger.warning(f"Error adding market events: {str(e)}")
            return df
    
    def generate_dataset(self, n_rows=10000, start_date='2020-01-01', end_date='2024-12-31', 
                        n_assets=20, filename='syntheticdata.csv'):
        """
        Generate complete synthetic dataset for portfolio optimization.
        
        Parameters:
        -----------
        n_rows : int, default 10000
            Target number of rows (will be approximated based on assets and dates)
        start_date : str, default '2020-01-01'
            Start date for data
        end_date : str, default '2024-12-31'  
            End date for data
        n_assets : int, default 20
            Number of assets
        filename : str, default 'syntheticdata.csv'
            Output filename
            
        Returns:
        --------
        pd.DataFrame
            Generated dataset
        """
        try:
            # Calculate date range to approximately match n_rows
            business_days_per_year = 252
            years_needed = n_rows / (n_assets * business_days_per_year)
            
            if years_needed > 5:
                logger.warning(f"Requested {n_rows} rows requires {years_needed:.1f} years of data. Adjusting...")
                years_needed = 5
                
            # Adjust end date if needed
            start_dt = pd.to_datetime(start_date)
            calculated_end = start_dt + timedelta(days=int(years_needed * 365))
            end_dt = min(pd.to_datetime(end_date), calculated_end)
            
            logger.info(f"Generating data from {start_dt.date()} to {end_dt.date()}")
            logger.info(f"Assets: {n_assets}, Expected rows: ~{int(years_needed * n_assets * business_days_per_year)}")
            
            # Generate the data
            df = self.generate_market_data(start_dt, end_dt, n_assets)
            
            # Save to CSV
            df.to_csv(filename, index=False)
            logger.info(f"Dataset saved to {filename}")
            logger.info(f"Final dataset shape: {df.shape}")
            logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
            logger.info(f"Assets: {df['symbol'].nunique()}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error generating dataset: {str(e)}")
            raise

def main():
    """Main function to run the data generator."""
    parser = argparse.ArgumentParser(description='Generate synthetic portfolio data')
    parser.add_argument('--rows', type=int, default=10000, 
                       help='Target number of rows (default: 10000)')
    parser.add_argument('--assets', type=int, default=20,
                       help='Number of assets (default: 20)')
    parser.add_argument('--start-date', type=str, default='2020-01-01',
                       help='Start date (default: 2020-01-01)')
    parser.add_argument('--end-date', type=str, default='2024-12-31',
                       help='End date (default: 2024-12-31)')
    parser.add_argument('--filename', type=str, default='syntheticdata.csv',
                       help='Output filename (default: syntheticdata.csv)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed (default: 42)')
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = PortfolioDataGenerator(locale='en_IN', seed=args.seed)
        
        # Generate dataset
        df = generator.generate_dataset(
            n_rows=args.rows,
            start_date=args.start_date,
            end_date=args.end_date,
            n_assets=args.assets,
            filename=args.filename
        )
        
        print(f"\n✅ Successfully generated {len(df)} rows of synthetic portfolio data")
        print(f"📁 Saved to: {args.filename}")
        print(f"📊 Assets: {df['symbol'].nunique()}")
        print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        
    except Exception as e:
        logger.error(f"Failed to generate data: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
