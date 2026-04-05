"""
NIFTY 50 Stock Tickers for Yahoo Finance
Updated as of July 2025
"""

NIFTY50_TICKERS = [
    'RELIANCE.NS',      # Reliance Industries
    'HDFCBANK.NS',      # HDFC Bank
    'TCS.NS',           # Tata Consultancy Services
    'ICICIBANK.NS',     # ICICI Bank
    'BHARTIARTL.NS',    # Bharti Airtel
    'SBIN.NS',          # State Bank of India
    'INFY.NS',          # Infosys
    'HINDUNILVR.NS',    # Hindustan Unilever
    'LT.NS',            # Larsen & Toubro
    'ITC.NS',           # ITC
    'HCLTECH.NS',       # HCL Technologies
    'BAJFINANCE.NS',    # Bajaj Finance
    'SUNPHARMA.NS',     # Sun Pharmaceutical
    'ONGC.NS',          # Oil & Natural Gas Corporation
    'KOTAKBANK.NS',     # Kotak Mahindra Bank
    'AXISBANK.NS',      # Axis Bank
    'ASIANPAINT.NS',    # Asian Paints
    'MARUTI.NS',        # Maruti Suzuki
    'NESTLEIND.NS',     # Nestle India
    'WIPRO.NS',         # Wipro
    'ULTRACEMCO.NS',    # UltraTech Cement
    'TECHM.NS',         # Tech Mahindra
    'TITAN.NS',         # Titan Company
    'COALINDIA.NS',     # Coal India
    'NTPC.NS',          # NTPC
    'POWERGRID.NS',     # Power Grid Corporation
    'BAJAJFINSV.NS',    # Bajaj Finserv
    'M&M.NS',           # Mahindra & Mahindra
    'JSWSTEEL.NS',      # JSW Steel
    'TATASTEEL.NS',     # Tata Steel
    'INDUSINDBK.NS',    # IndusInd Bank
    'ADANIENT.NS',      # Adani Enterprises
    'HINDALCO.NS',      # Hindalco Industries
    'GRASIM.NS',        # Grasim Industries
    'CIPLA.NS',         # Cipla
    'DIVISLAB.NS',      # Divi's Laboratories
    'DRREDDY.NS',       # Dr. Reddy's Laboratories
    'EICHERMOT.NS',     # Eicher Motors
    'HEROMOTOCO.NS',    # Hero MotoCorp
    'BRITANNIA.NS',     # Britannia Industries
    'APOLLOHOSP.NS',    # Apollo Hospitals
    'BAJAJ-AUTO.NS',    # Bajaj Auto
    'BPCL.NS',          # Bharat Petroleum
    'TATAMOTORS.NS',    # Tata Motors
    'SHRIRAMFIN.NS',    # Shriram Finance
    'TATACONSUM.NS',    # Tata Consumer Products
    'ADANIPORTS.NS',    # Adani Ports
    'UPL.NS',           # UPL Limited
    'LTIM.NS',          # LTIMindtree
    'TRENT.NS'          # Trent
]

# Sector mapping for analysis
SECTOR_MAPPING = {
    'RELIANCE.NS': 'Energy', 'HDFCBANK.NS': 'Financials', 'TCS.NS': 'IT',
    'ICICIBANK.NS': 'Financials', 'BHARTIARTL.NS': 'Telecom', 'SBIN.NS': 'Financials',
    'INFY.NS': 'IT', 'HINDUNILVR.NS': 'FMCG', 'LT.NS': 'Infrastructure',
    'ITC.NS': 'FMCG', 'HCLTECH.NS': 'IT', 'BAJFINANCE.NS': 'Financials',
    'SUNPHARMA.NS': 'Pharma', 'ONGC.NS': 'Energy', 'KOTAKBANK.NS': 'Financials',
    'AXISBANK.NS': 'Financials', 'ASIANPAINT.NS': 'Paints', 'MARUTI.NS': 'Auto',
    'NESTLEIND.NS': 'FMCG', 'WIPRO.NS': 'IT', 'ULTRACEMCO.NS': 'Cement',
    'TECHM.NS': 'IT', 'TITAN.NS': 'Consumer Durables', 'COALINDIA.NS': 'Mining',
    'NTPC.NS': 'Power', 'POWERGRID.NS': 'Power', 'BAJAJFINSV.NS': 'Financials',
    'M&M.NS': 'Auto', 'JSWSTEEL.NS': 'Steel', 'TATASTEEL.NS': 'Steel',
    'INDUSINDBK.NS': 'Financials', 'ADANIENT.NS': 'Conglomerate', 'HINDALCO.NS': 'Metals',
    'GRASIM.NS': 'Chemicals', 'CIPLA.NS': 'Pharma', 'DIVISLAB.NS': 'Pharma',
    'DRREDDY.NS': 'Pharma', 'EICHERMOT.NS': 'Auto', 'HEROMOTOCO.NS': 'Auto',
    'BRITANNIA.NS': 'FMCG', 'APOLLOHOSP.NS': 'Healthcare', 'BAJAJ-AUTO.NS': 'Auto',
    'BPCL.NS': 'Energy', 'TATAMOTORS.NS': 'Auto', 'SHRIRAMFIN.NS': 'Financials',
    'TATACONSUM.NS': 'FMCG', 'ADANIPORTS.NS': 'Infrastructure', 'UPL.NS': 'Chemicals',
    'LTIM.NS': 'IT', 'TRENT.NS': 'Retail'
}
