# interest_rate_risk_management.py
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path='syntheticdata.csv'):
    try:
        df = pd.read_csv(file_path, parse_dates=['AccountOpenDate', 'LastTransactionDate'])
        return df
    except Exception as e:
        print(f"Error reading data from {file_path}: {e}", file=sys.stderr)
        raise

def analyze_interest_rate_distribution(df):
    plt.figure(figsize=(10,6))
    sns.histplot(df['InterestRate'], bins=30, kde=True)
    plt.title("Distribution of Interest Rates Across Accounts")
    plt.xlabel("Interest Rate (%)")
    plt.ylabel("Number of Accounts")
    plt.grid(True)
    plt.show()

def exposure_by_account_type(df):
    exposure = df.groupby('AccountType')['Balance'].sum().sort_values(ascending=False)
    plt.figure(figsize=(8,5))
    exposure.plot(kind='bar')
    plt.ylabel('Total Balance (Exposure)')
    plt.title('Exposure by Account Type')
    plt.grid(axis='y')
    plt.show()
    print("Exposure by Account Type:\n", exposure)

def sensitivity_to_rate_change(df, change_pct=0.01):
    """
    Calculate the change in interest expense / income if rates change by change_pct (absolute).
    Assuming balance represents amount on which interest accrues.
    """
    df_copy = df.copy()
    df_copy['OriginalInterest'] = df_copy['Balance'] * df_copy['InterestRate'] / 100
    df_copy['NewInterest'] = df_copy['Balance'] * (df_copy['InterestRate'] + change_pct*100) / 100
    df_copy['InterestChange'] = df_copy['NewInterest'] - df_copy['OriginalInterest']

    total_original = df_copy['OriginalInterest'].sum()
    total_new = df_copy['NewInterest'].sum()
    total_change = df_copy['InterestChange'].sum()

    print(f"Total Interest Payment at current rates: ₹{total_original:,.2f}")
    print(f"Total Interest Payment if rates change by {change_pct*100:.2f} pct points: ₹{total_new:,.2f}")
    print(f"Change in Interest Payment: ₹{total_change:,.2f}")

    plt.figure(figsize=(10,6))
    sns.boxplot(y='InterestChange', data=df_copy)
    plt.title(f'Interest Payment Sensitivity to a Rate Change of {change_pct*100:.2f} Percentage Points')
    plt.ylabel('Change in Interest Payment (₹)')
    plt.show()

def main():
    print("Loading synthetic financial data...")
    df = load_data()

    print("\nAnalyzing Interest Rate Distribution")
    analyze_interest_rate_distribution(df)

    print("\nCalculating Exposure by Account Type")
    exposure_by_account_type(df)

    print("\nCalculating Sensitivity to Interest Rate Changes")
    sensitivity_to_rate_change(df, change_pct=0.01)  # 1% increase example

    print("\nInterest Rate Risk Management Demo Completed.")

if __name__ == '__main__':
    main()
