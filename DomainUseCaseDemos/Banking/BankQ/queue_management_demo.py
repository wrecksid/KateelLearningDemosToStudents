# queue_management_demo.py
"""
Queue Design and Management Demo

Reads syntheticdata.csv, analyzes queue delays, service efficiency,
provides visualizations and management insights for bank branch.

Usage:
- Run after generating syntheticdata.csv with the provided generator.
- Explore adjustable parameters of analysis in the Jupyter notebook version.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def load_data(file='syntheticdata.csv'):
    try:
        df = pd.read_csv(file, parse_dates=['arrival_time', 'service_start_time'])
        return df
    except Exception as e:
        print(f"Error loading data file: {e}", file=sys.stderr)
        raise

def analyze_queue(df):
    """
    Analyze queue metrics such as waiting times, service times, throughput.
    """
    # Compute wait time (service start - arrival)
    df['wait_time_sec'] = (df['service_start_time'] - df['arrival_time']).dt.total_seconds()

    # Basic stats
    stats = {
        'avg_wait_time_sec': df['wait_time_sec'].mean(),
        'median_wait_time_sec': df['wait_time_sec'].median(),
        'max_wait_time_sec': df['wait_time_sec'].max(),
        'avg_service_time_sec': df['service_duration_sec'].mean(),
        'total_customers': len(df),
    }
    return stats, df

def plot_wait_times(df):
    """
    Plot distribution of wait times and highlight queue delays.
    """
    plt.figure(figsize=(10,6))
    sns.histplot(df['wait_time_sec'], bins=50, kde=True, color='skyblue')
    plt.title('Distribution of Customer Wait Times (seconds)')
    plt.xlabel('Wait Time (seconds)')
    plt.ylabel('Number of Customers')
    plt.grid(True)
    plt.show()

def plot_service_over_time(df):
    """
    Plot how arrivals and service starts vary over the day.
    """
    df['arrival_hour'] = df['arrival_time'].dt.hour
    df['service_start_hour'] = df['service_start_time'].dt.hour

    plt.figure(figsize=(12,6))
    sns.countplot(x='arrival_hour', data=df, label='Arrival Time', color='orange', alpha=0.6)
    sns.countplot(x='service_start_hour', data=df, label='Service Start Time', color='blue', alpha=0.6)
    plt.legend(['Arrival Time', 'Service Start Time'])
    plt.title('Hourly Distribution of Customer Arrivals and Service Start')
    plt.xlabel('Hour of Day')
    plt.ylabel('Count')
    plt.show()

def run_demo():
    print("Loading synthetic data...")
    df = load_data()

    print("Analyzing queue data...")
    stats, df = analyze_queue(df)

    print("\nQueue Analysis Summary:")
    print(f"Total customers served: {stats['total_customers']}")
    print(f"Average wait time (sec): {stats['avg_wait_time_sec']:.2f}")
    print(f"Median wait time (sec): {stats['median_wait_time_sec']:.2f}")
    print(f"Maximum wait time (sec): {stats['max_wait_time_sec']:.2f}")
    print(f"Average service duration (sec): {stats['avg_service_time_sec']:.2f}")

    print("\nGenerating plots...")
    plot_wait_times(df)
    plot_service_over_time(df)

    print("\nManagement Insights:")
    print("""
    1. Average wait time helps determine if the current number of tellers meets customer demand.
    2. Peak arrival hours identified can be used to allocate additional staff.
    3. Maximum wait time signals if service levels meet acceptable limits or require improvement.
    4. The shape of the wait time distribution enables understanding of queue congestion patterns.
    5. Transaction type and amount analysis (to be added in extended versions) can refine queue priority logic.
    """)

if __name__ == "__main__":
    run_demo()
