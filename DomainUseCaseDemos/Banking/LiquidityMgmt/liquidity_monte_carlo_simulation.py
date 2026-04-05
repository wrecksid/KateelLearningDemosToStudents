#!/usr/bin/env python3
"""
Liquidity Management Monte Carlo Simulation

This script demonstrates liquidity risk management using Monte Carlo simulations
to forecast cash flows and liquidity positions for financial institutions.

Author: Financial Analytics Course
Version: 1.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import sys
import warnings
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Optional
from pathlib import Path

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Ensure console stdout uses UTF-8 (helps printing symbols like ₹ on Windows)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    # Some environments don't support reconfigure; ignore failures
    pass


class LiquidityMonteCarloSimulator:
    """
    Monte Carlo Simulator for Liquidity Management Analysis.
    
    This class performs Monte Carlo simulations to:
    - Forecast future cash flows
    - Estimate liquidity positions
    - Calculate Value at Risk (VaR) for liquidity
    - Analyze stress scenarios
    """
    
    def __init__(self, data_file: str):
        """
        Initialize the simulator with transaction data.
        
        Args:
            data_file (str): Path to CSV file containing transaction data
        """
        self.data_file = data_file
        self.df = None
        self.daily_flows = None
        self.simulation_results = None
        
    def load_data(self) -> bool:
        """
        Load and preprocess transaction data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Loading data from {self.data_file}...")
            
            # Load CSV data
            self.df = pd.read_csv(self.data_file)
            
            # Validate required columns
            required_columns = ['transaction_date', 'transaction_type', 'amount_inr']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert date column
            self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
            
            # Create signed amounts (positive for inflows, negative for outflows)
            self.df['net_amount'] = self.df.apply(
                lambda row: row['amount_inr'] if row['transaction_type'] == 'inflow' 
                else -row['amount_inr'], axis=1
            )
            
            print(f"✅ Loaded {len(self.df)} transactions")
            print(f"Date range: {self.df['transaction_date'].min()} to {self.df['transaction_date'].max()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def analyze_historical_patterns(self) -> Dict:
        """
        Analyze historical cash flow patterns.
        
        Returns:
            dict: Statistical summary of historical patterns
        """
        try:
            # Aggregate daily cash flows
            self.daily_flows = self.df.groupby('transaction_date')['net_amount'].sum().reset_index()
            self.daily_flows.set_index('transaction_date', inplace=True)
            
            # Calculate statistics
            stats = {
                'mean_daily_flow': self.daily_flows['net_amount'].mean(),
                'std_daily_flow': self.daily_flows['net_amount'].std(),
                'min_daily_flow': self.daily_flows['net_amount'].min(),
                'max_daily_flow': self.daily_flows['net_amount'].max(),
                'total_inflows': self.df[self.df['transaction_type'] == 'inflow']['amount_inr'].sum(),
                'total_outflows': self.df[self.df['transaction_type'] == 'outflow']['amount_inr'].sum(),
                'net_position': self.df['net_amount'].sum()
            }
            
            return stats
            
        except Exception as e:
            print(f"Error analyzing historical patterns: {e}")
            return {}
    
    def run_monte_carlo_simulation(self, num_simulations: int = 1000, 
                                  forecast_days: int = 30, 
                                  initial_cash: float = 10000000) -> np.ndarray:
        """
        Run Monte Carlo simulation for liquidity forecasting.
        
        Args:
            num_simulations (int): Number of simulation runs
            forecast_days (int): Number of days to forecast
            initial_cash (float): Initial cash position in INR
            
        Returns:
            np.ndarray: Simulation results matrix
        """
        try:
            print(f"Running {num_simulations} Monte Carlo simulations...")
            
            # Calculate historical parameters
            mean_flow = self.daily_flows['net_amount'].mean()
            std_flow = self.daily_flows['net_amount'].std()
            
            # Initialize results matrix
            results = np.zeros((num_simulations, forecast_days + 1))
            results[:, 0] = initial_cash  # Set initial cash position
            
            # Run simulations
            for sim in range(num_simulations):
                cash_position = initial_cash
                
                for day in range(1, forecast_days + 1):
                    # Generate random daily cash flow
                    daily_flow = np.random.normal(mean_flow, std_flow)
                    cash_position += daily_flow
                    results[sim, day] = cash_position
                
                # Progress indicator
                if sim % 100 == 0:
                    print(f"Completed {sim} simulations...")
            
            self.simulation_results = results
            print("✅ Monte Carlo simulation completed")
            
            return results
            
        except Exception as e:
            print(f"Error running Monte Carlo simulation: {e}")
            return np.array([])
    
    def calculate_risk_metrics(self, confidence_levels: List[float] = [0.95, 0.99]) -> Dict:
        """
        Calculate liquidity risk metrics from simulation results.
        
        Args:
            confidence_levels (list): Confidence levels for VaR calculation
            
        Returns:
            dict: Risk metrics including VaR and probability of shortfall
        """
        try:
            if self.simulation_results is None:
                raise ValueError("No simulation results available. Run simulation first.")
            
            # Get final cash positions
            final_positions = self.simulation_results[:, -1]
            
            # Calculate Value at Risk (VaR)
            var_metrics = {}
            for confidence in confidence_levels:
                var_value = np.percentile(final_positions, (1 - confidence) * 100)
                var_metrics[f'VaR_{int(confidence*100)}%'] = var_value
            
            # Calculate probability of liquidity shortfall
            shortfall_prob = (final_positions < 0).mean() * 100
            
            # Calculate expected shortfall (Conditional VaR)
            shortfall_positions = final_positions[final_positions < np.percentile(final_positions, 5)]
            expected_shortfall = shortfall_positions.mean() if len(shortfall_positions) > 0 else 0
            
            metrics = {
                'var_metrics': var_metrics,
                'probability_of_shortfall': shortfall_prob,
                'expected_shortfall': expected_shortfall,
                'mean_final_position': final_positions.mean(),
                'std_final_position': final_positions.std()
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating risk metrics: {e}")
            return {}
    
    def create_visualizations(self, save_plots: bool = True) -> None:
        """
        Create comprehensive visualizations of the analysis.
        
        Args:
            save_plots (bool): Whether to save plots to files
        """
        try:
            # Set up the plotting environment
            fig = plt.figure(figsize=(20, 15))
            
            # 1. Historical Daily Cash Flows
            plt.subplot(2, 3, 1)
            plt.plot(self.daily_flows.index, self.daily_flows['net_amount'], alpha=0.7, linewidth=1)
            plt.title('Historical Daily Cash Flows', fontsize=14, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Net Cash Flow (INR)')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            
            # 2. Distribution of Daily Cash Flows
            plt.subplot(2, 3, 2)
            plt.hist(self.daily_flows['net_amount'], bins=30, alpha=0.7, edgecolor='black')
            plt.title('Distribution of Daily Cash Flows', fontsize=14, fontweight='bold')
            plt.xlabel('Net Cash Flow (INR)')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            # 3. Monte Carlo Simulation Paths (sample)
            plt.subplot(2, 3, 3)
            sample_paths = self.simulation_results[:50, :]  # Show only 50 paths for clarity
            days = np.arange(sample_paths.shape[1])
            
            for i in range(sample_paths.shape[0]):
                plt.plot(days, sample_paths[i, :], alpha=0.3, linewidth=0.5)
            
            # Add percentile bands
            percentiles = np.percentile(self.simulation_results, [5, 50, 95], axis=0)
            plt.plot(days, percentiles[1, :], 'r-', linewidth=2, label='Median')
            plt.fill_between(days, percentiles[0, :], percentiles[2, :], alpha=0.2, label='90% Confidence Band')
            
            plt.title('Monte Carlo Simulation Paths', fontsize=14, fontweight='bold')
            plt.xlabel('Days')
            plt.ylabel('Cash Position (INR)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 4. Final Position Distribution
            plt.subplot(2, 3, 4)
            final_positions = self.simulation_results[:, -1]
            plt.hist(final_positions, bins=50, alpha=0.7, edgecolor='black', density=True)
            plt.axvline(np.percentile(final_positions, 5), color='red', linestyle='--', label='5% VaR')
            plt.axvline(np.percentile(final_positions, 1), color='darkred', linestyle='--', label='1% VaR')
            plt.axvline(final_positions.mean(), color='green', linestyle='-', label='Mean')
            plt.title('Distribution of Final Cash Positions', fontsize=14, fontweight='bold')
            plt.xlabel('Final Cash Position (INR)')
            plt.ylabel('Density')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 5. Risk Metrics Visualization
            plt.subplot(2, 3, 5)
            confidence_levels = [0.90, 0.95, 0.99]
            var_values = [np.percentile(final_positions, (1-conf)*100) for conf in confidence_levels]
            
            plt.bar([f'{int(conf*100)}%' for conf in confidence_levels], var_values, alpha=0.7)
            plt.title('Value at Risk by Confidence Level', fontsize=14, fontweight='bold')
            plt.xlabel('Confidence Level')
            plt.ylabel('VaR (INR)')
            plt.grid(True, alpha=0.3)
            
            # 6. Probability of Shortfall Over Time
            plt.subplot(2, 3, 6)
            shortfall_probs = []
            days = range(1, self.simulation_results.shape[1])
            
            for day in days:
                shortfall_prob = (self.simulation_results[:, day] < 0).mean() * 100
                shortfall_probs.append(shortfall_prob)
            
            plt.plot(days, shortfall_probs, linewidth=2, marker='o', markersize=4)
            plt.title('Probability of Liquidity Shortfall Over Time', fontsize=14, fontweight='bold')
            plt.xlabel('Days')
            plt.ylabel('Probability of Shortfall (%)')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_plots:
                plt.savefig('liquidity_monte_carlo_analysis.png', dpi=300, bbox_inches='tight')
                print("📊 Plots saved as 'liquidity_monte_carlo_analysis.png'")
            
            plt.show()
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
    
    def generate_report(self, stats: Dict, risk_metrics: Dict) -> str:
        """
        Generate a comprehensive analysis report.
        
        Args:
            stats (dict): Historical statistics
            risk_metrics (dict): Risk metrics from simulation
            
        Returns:
            str: Formatted report
        """
        try:
            report = f"""
{'='*80}
LIQUIDITY MANAGEMENT MONTE CARLO SIMULATION REPORT
{'='*80}

EXECUTIVE SUMMARY
{'-'*40}
This report presents the results of Monte Carlo simulation analysis for liquidity 
management. The analysis is based on historical transaction data and provides 
insights into future cash flow patterns and liquidity risk.

HISTORICAL ANALYSIS
{'-'*40}
• Average Daily Cash Flow: ₹{stats.get('mean_daily_flow', 0):,.2f}
• Daily Cash Flow Volatility: ₹{stats.get('std_daily_flow', 0):,.2f}
• Minimum Daily Flow: ₹{stats.get('min_daily_flow', 0):,.2f}
• Maximum Daily Flow: ₹{stats.get('max_daily_flow', 0):,.2f}
• Total Inflows: ₹{stats.get('total_inflows', 0):,.2f}
• Total Outflows: ₹{stats.get('total_outflows', 0):,.2f}
• Net Position: ₹{stats.get('net_position', 0):,.2f}

RISK METRICS
{'-'*40}
• Mean Final Cash Position: ₹{risk_metrics.get('mean_final_position', 0):,.2f}
• Standard Deviation: ₹{risk_metrics.get('std_final_position', 0):,.2f}
• Probability of Liquidity Shortfall: {risk_metrics.get('probability_of_shortfall', 0):.2f}%
• Expected Shortfall: ₹{risk_metrics.get('expected_shortfall', 0):,.2f}

VALUE AT RISK (VAR)
{'-'*40}"""
            
            for var_type, var_value in risk_metrics.get('var_metrics', {}).items():
                report += f"\n• {var_type}: ₹{var_value:,.2f}"
            
            report += f"""

MANAGEMENT RECOMMENDATIONS
{'-'*40}
1. LIQUIDITY BUFFER: Maintain a minimum cash buffer of ₹{abs(risk_metrics.get('expected_shortfall', 0)) * 1.5:,.0f}
   to cover potential shortfalls with adequate safety margin.

2. MONITORING: Implement daily cash position monitoring with alert thresholds at
   95% and 99% confidence levels.

3. CONTINGENCY PLANNING: Develop contingency funding plans for scenarios where
   cash position falls below critical thresholds.

4. STRESS TESTING: Conduct regular stress tests using different market scenarios
   to validate liquidity adequacy.

BUSINESS APPLICATIONS
{'-'*40}
• Treasury Management: Optimize cash allocation and investment decisions
• Risk Management: Set appropriate liquidity risk limits and controls
• Regulatory Compliance: Meet Basel III liquidity coverage ratio requirements
• Strategic Planning: Inform business growth and expansion decisions

{'='*80}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
            """
            
            return report
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return "Error generating report"


def main():
    """Main function to handle command line execution."""
    parser = argparse.ArgumentParser(
        description='Liquidity Management Monte Carlo Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python liquidity_monte_carlo_simulation.py --data synthetic_liquidity_data.csv
  python liquidity_monte_carlo_simulation.py --data data.csv --simulations 5000 --days 60
        """
    )
    
    parser.add_argument('--data', type=str, default='synthetic_liquidity_data.csv',
                       help='Path to CSV data file (default: synthetic_liquidity_data.csv)')
    parser.add_argument('--simulations', type=int, default=1000,
                       help='Number of Monte Carlo simulations (default: 1000)')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days to forecast (default: 30)')
    parser.add_argument('--initial-cash', type=float, default=10000000,
                       help='Initial cash position in INR (default: 10,000,000)')
    parser.add_argument('--save-plots', action='store_true',
                       help='Save plots to file')
    
    args = parser.parse_args()
    
    try:
        print("🏦 Starting Liquidity Management Monte Carlo Simulation...")
        print("="*60)
        
        # Initialize simulator
        simulator = LiquidityMonteCarloSimulator(args.data)
        
        # Load and analyze data
        if not simulator.load_data():
            sys.exit(1)
        
        # Analyze historical patterns
        print("\n📊 Analyzing historical patterns...")
        stats = simulator.analyze_historical_patterns()
        
        # Run Monte Carlo simulation
        print(f"\n🎲 Running Monte Carlo simulation...")
        results = simulator.run_monte_carlo_simulation(
            num_simulations=args.simulations,
            forecast_days=args.days,
            initial_cash=args.initial_cash
        )
        
        if len(results) == 0:
            print("❌ Simulation failed")
            sys.exit(1)
        
        # Calculate risk metrics
        print("\n📈 Calculating risk metrics...")
        risk_metrics = simulator.calculate_risk_metrics()
        
        # Generate visualizations
        print("\n📊 Creating visualizations...")
        simulator.create_visualizations(save_plots=args.save_plots)
        
        # Generate and display report
        print("\n📋 Generating analysis report...")
        report = simulator.generate_report(stats, risk_metrics)
        print(report)
        
        # Save report to file (use UTF-8 encoding to support currency symbols)
        with open('liquidity_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("💾 Report saved as 'liquidity_analysis_report.txt'")
        
        print("\n✅ Analysis completed successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
