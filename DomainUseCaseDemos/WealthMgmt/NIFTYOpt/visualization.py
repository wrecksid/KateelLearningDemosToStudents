"""
Visualization Module for Portfolio Optimization
Advanced plotting and charting functions for portfolio analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class PortfolioVisualizer:
    """
    Comprehensive visualization class for portfolio analysis
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize visualizer
        
        Args:
            figsize: Default figure size
        """
        self.figsize = figsize
        
    def plot_efficient_frontier(self, 
                              efficient_df: pd.DataFrame,
                              monte_carlo_df: pd.DataFrame = None,
                              optimized_portfolios: Dict = None,
                              save_path: str = None) -> None:
        """
        Plot efficient frontier with Monte Carlo simulation
        
        Args:
            efficient_df: Efficient frontier data
            monte_carlo_df: Monte Carlo simulation results
            optimized_portfolios: Dictionary of optimized portfolios
            save_path: Path to save the plot
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot Monte Carlo simulation if provided
        if monte_carlo_df is not None and not monte_carlo_df.empty:
            scatter = ax.scatter(monte_carlo_df['Volatility'], monte_carlo_df['Return'],
                               c=monte_carlo_df['Sharpe_Ratio'], cmap='viridis',
                               alpha=0.6, s=10, label='Random Portfolios')
            plt.colorbar(scatter, ax=ax, label='Sharpe Ratio')
        
        # Plot efficient frontier
        if not efficient_df.empty:
            ax.plot(efficient_df['Volatility'], efficient_df['Return'],
                   'r-', linewidth=3, label='Efficient Frontier')
        
        # Plot optimized portfolios
        if optimized_portfolios:
            colors = {'sharpe': 'gold', 'min_vol': 'green', 'max_return': 'blue'}
            markers = {'sharpe': '*', 'min_vol': 'o', 'max_return': '^'}
            
            for obj_type, portfolio in optimized_portfolios.items():
                if portfolio:
                    ax.scatter(portfolio['volatility'], portfolio['expected_return'],
                             color=colors.get(obj_type, 'red'), 
                             marker=markers.get(obj_type, 'o'),
                             s=200, label=f'{obj_type.replace("_", " ").title()} Portfolio',
                             edgecolors='black', linewidth=2)
        
        ax.set_xlabel('Volatility (Risk)', fontsize=12)
        ax.set_ylabel('Expected Return', fontsize=12)
        ax.set_title('Efficient Frontier - NIFTY 50 Portfolio Optimization', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format axes as percentages
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_portfolio_allocation(self, 
                                weights: np.array, 
                                stock_names: List[str],
                                title: str = "Portfolio Allocation",
                                min_weight: float = 0.01,
                                save_path: str = None) -> None:
        """
        Plot portfolio allocation pie chart
        
        Args:
            weights: Portfolio weights
            stock_names: List of stock names
            title: Chart title
            min_weight: Minimum weight to display separately
            save_path: Path to save the plot
        """
        # Create allocation dataframe
        allocation_df = pd.DataFrame({
            'Stock': stock_names,
            'Weight': weights
        }).sort_values('Weight', ascending=False)
        
        # Group small allocations
        significant = allocation_df[allocation_df['Weight'] >= min_weight]
        others_weight = allocation_df[allocation_df['Weight'] < min_weight]['Weight'].sum()
        
        if others_weight > 0:
            others_row = pd.DataFrame({'Stock': ['Others'], 'Weight': [others_weight]})
            plot_data = pd.concat([significant, others_row], ignore_index=True)
        else:
            plot_data = significant
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=self.figsize)
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(plot_data)))
        wedges, texts, autotexts = ax.pie(plot_data['Weight'], 
                                         labels=plot_data['Stock'],
                                         autopct='%1.1f%%',
                                         startangle=90,
                                         colors=colors)
        
        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_risk_return_scatter(self, 
                               returns_df: pd.DataFrame,
                               weights: np.array = None,
                               sector_mapping: Dict = None,
                               save_path: str = None) -> None:
        """
        Plot individual stock risk-return scatter
        
        Args:
            returns_df: Stock returns dataframe
            weights: Portfolio weights (optional)
            sector_mapping: Stock to sector mapping
            save_path: Path to save the plot
        """
        # Calculate individual stock metrics
        stock_metrics = []
        
        for stock in returns_df.columns:
            stock_returns = returns_df[stock].dropna()
            annual_return = stock_returns.mean() * 252
            annual_vol = stock_returns.std() * np.sqrt(252)
            
            stock_metrics.append({
                'Stock': stock,
                'Return': annual_return,
                'Volatility': annual_vol,
                'Sector': sector_mapping.get(stock, 'Unknown') if sector_mapping else 'Unknown',
                'Weight': weights[returns_df.columns.get_loc(stock)] if weights is not None else 0
            })
        
        metrics_df = pd.DataFrame(stock_metrics)
        
        # Create scatter plot
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if sector_mapping:
            sectors = metrics_df['Sector'].unique()
            colors = plt.cm.tab10(np.linspace(0, 1, len(sectors)))
            
            for i, sector in enumerate(sectors):
                sector_data = metrics_df[metrics_df['Sector'] == sector]
                scatter = ax.scatter(sector_data['Volatility'], sector_data['Return'],
                                   c=[colors[i]], label=sector, s=100, alpha=0.7)
        else:
            ax.scatter(metrics_df['Volatility'], metrics_df['Return'], s=100, alpha=0.7)
        
        # Highlight portfolio holdings if weights provided
        if weights is not None:
            significant_holdings = metrics_df[metrics_df['Weight'] > 0.02]  # >2%
            for _, stock in significant_holdings.iterrows():
                ax.annotate(stock['Stock'].replace('.NS', ''), 
                          (stock['Volatility'], stock['Return']),
                          xytext=(5, 5), textcoords='offset points',
                          fontsize=8, fontweight='bold')
        
        ax.set_xlabel('Volatility (Risk)', fontsize=12)
        ax.set_ylabel('Expected Return', fontsize=12)
        ax.set_title('Individual Stock Risk-Return Profile', fontsize=14, fontweight='bold')
        
        if sector_mapping:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        ax.grid(True, alpha=0.3)
        
        # Format axes as percentages
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_correlation_heatmap(self, 
                               correlation_matrix: pd.DataFrame,
                               save_path: str = None) -> None:
        """
        Plot correlation heatmap
        
        Args:
            correlation_matrix: Stock correlation matrix
            save_path: Path to save the plot
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Create heatmap
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=False, cmap='coolwarm',
                   center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title('Stock Correlation Matrix', fontsize=14, fontweight='bold')
        
        # Clean up tick labels
        ax.set_xticklabels([label.get_text().replace('.NS', '') for label in ax.get_xticklabels()], 
                          rotation=45, ha='right')
        ax.set_yticklabels([label.get_text().replace('.NS', '') for label in ax.get_yticklabels()], 
                          rotation=0)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_portfolio_performance(self, 
                                 returns_df: pd.DataFrame,
                                 weights: np.array,
                                 benchmark_returns: pd.Series = None,
                                 save_path: str = None) -> None:
        """
        Plot portfolio performance over time
        
        Args:
            returns_df: Stock returns dataframe
            weights: Portfolio weights
            benchmark_returns: Benchmark returns (optional)
            save_path: Path to save the plot
        """
        # Calculate portfolio returns
        portfolio_returns = (returns_df * weights).sum(axis=1)
        portfolio_cumulative = (1 + portfolio_returns).cumprod()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1]*1.2))
        
        # Cumulative returns plot
        ax1.plot(portfolio_cumulative.index, portfolio_cumulative.values, 
                label='Portfolio', linewidth=2)
        
        if benchmark_returns is not None:
            benchmark_cumulative = (1 + benchmark_returns).cumprod()
            ax1.plot(benchmark_cumulative.index, benchmark_cumulative.values,
                    label='NIFTY 50', linewidth=2, alpha=0.8)
        
        ax1.set_title('Cumulative Returns Comparison', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Cumulative Return')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Rolling volatility plot
        rolling_vol = portfolio_returns.rolling(window=30).std() * np.sqrt(252)
        ax2.plot(rolling_vol.index, rolling_vol.values, 
                color='red', alpha=0.7, linewidth=1)
        ax2.fill_between(rolling_vol.index, rolling_vol.values, alpha=0.3, color='red')
        
        ax2.set_title('30-Day Rolling Volatility', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Volatility')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        # Format y-axis as percentages
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_interactive_dashboard(self, 
                                   efficient_df: pd.DataFrame,
                                   monte_carlo_df: pd.DataFrame,
                                   optimized_portfolios: Dict) -> go.Figure:
        """
        Create interactive Plotly dashboard
        
        Args:
            efficient_df: Efficient frontier data
            monte_carlo_df: Monte Carlo simulation results
            optimized_portfolios: Dictionary of optimized portfolios
            
        Returns:
            Plotly figure object
        """
        fig = go.Figure()
        
        # Add Monte Carlo scatter
        if not monte_carlo_df.empty:
            fig.add_trace(go.Scatter(
                x=monte_carlo_df['Volatility'],
                y=monte_carlo_df['Return'],
                mode='markers',
                marker=dict(
                    size=4,
                    color=monte_carlo_df['Sharpe_Ratio'],
                    colorscale='Viridis',
                    colorbar=dict(title="Sharpe Ratio"),
                    opacity=0.6
                ),
                name='Random Portfolios',
                hovertemplate='Return: %{y:.2%}<br>Volatility: %{x:.2%}<br>Sharpe: %{marker.color:.3f}<extra></extra>'
            ))
        
        # Add efficient frontier
        if not efficient_df.empty:
            fig.add_trace(go.Scatter(
                x=efficient_df['Volatility'],
                y=efficient_df['Return'],
                mode='lines',
                line=dict(color='red', width=3),
                name='Efficient Frontier',
                hovertemplate='Return: %{y:.2%}<br>Volatility: %{x:.2%}<extra></extra>'
            ))
        
        # Add optimized portfolios
        colors = {'sharpe': 'gold', 'min_vol': 'green', 'max_return': 'blue'}
        symbols = {'sharpe': 'star', 'min_vol': 'circle', 'max_return': 'triangle-up'}
        
        for obj_type, portfolio in optimized_portfolios.items():
            if portfolio:
                fig.add_trace(go.Scatter(
                    x=[portfolio['volatility']],
                    y=[portfolio['expected_return']],
                    mode='markers',
                    marker=dict(
                        symbol=symbols.get(obj_type, 'circle'),
                        size=15,
                        color=colors.get(obj_type, 'red'),
                        line=dict(color='black', width=2)
                    ),
                    name=f'{obj_type.replace("_", " ").title()} Portfolio',
                    hovertemplate=f'Return: %{{y:.2%}}<br>Volatility: %{{x:.2%}}<br>Sharpe: {portfolio["sharpe_ratio"]:.3f}<extra></extra>'
                ))
        
        # Update layout
        fig.update_layout(
            title='Interactive Efficient Frontier - NIFTY 50 Portfolio Optimization',
            xaxis_title='Volatility (Risk)',
            yaxis_title='Expected Return',
            hovermode='closest',
            template='plotly_white',
            width=900,
            height=600
        )
        
        # Format axes as percentages
        fig.update_xaxes(tickformat='.1%')
        fig.update_yaxes(tickformat='.1%')
        
        return fig

# Example usage
if __name__ == "__main__":
    # Create sample data for testing
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-01-01', freq='D')
    returns = pd.DataFrame(
        np.random.normal(0.001, 0.02, (len(dates), 5)),
        index=dates,
        columns=['STOCK1.NS', 'STOCK2.NS', 'STOCK3.NS', 'STOCK4.NS', 'STOCK5.NS']
    )
    
    # Sample data for testing
    efficient_df = pd.DataFrame({
        'Return': np.linspace(0.08, 0.18, 50),
        'Volatility': np.linspace(0.12, 0.25, 50),
        'Sharpe_Ratio': np.random.normal(0.6, 0.2, 50)
    })
    
    monte_carlo_df = pd.DataFrame({
        'Return': np.random.normal(0.12, 0.05, 1000),
        'Volatility': np.random.normal(0.18, 0.04, 1000),
        'Sharpe_Ratio': np.random.normal(0.5, 0.3, 1000)
    })
    
    optimized_portfolios = {
        'sharpe': {'expected_return': 0.15, 'volatility': 0.18, 'sharpe_ratio': 0.75},
        'min_vol': {'expected_return': 0.10, 'volatility': 0.12, 'sharpe_ratio': 0.42}
    }
    
    # Initialize visualizer
    viz = PortfolioVisualizer()
    
    # Test plots
    print("Testing visualization functions...")
    
    # Efficient frontier plot
    viz.plot_efficient_frontier(efficient_df, monte_carlo_df, optimized_portfolios)
    
    # Portfolio allocation plot
    weights = np.array([0.3, 0.25, 0.2, 0.15, 0.1])
    stock_names = ['STOCK1', 'STOCK2', 'STOCK3', 'STOCK4', 'STOCK5']
    viz.plot_portfolio_allocation(weights, stock_names)
    
    print("Visualization tests completed!")
