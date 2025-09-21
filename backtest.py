# pip install yfinance pandas numpy
import yfinance as yf, pandas as pd, numpy as np
import time
import warnings
warnings.filterwarnings("ignore")

def fetch_prices(ticker, start):
    """Fetch price data with retry logic and better error handling"""
    for i in range(3):
        try:
            print(f"Fetching data for {ticker}...")
            df = yf.Ticker(ticker).history(start=start, auto_adjust=True, period="max")
            if df.empty:
                print(f"No data found for {ticker}")
                return None
            if "Close" in df.columns:
                return df["Close"].to_frame(ticker)
            return None
        except Exception as e:
            print(f"Error fetching {ticker} (attempt {i+1}): {e}")
            if i == 2:
                return None
            time.sleep(1 + i)
    return None

def download_sleeves(ticker_map, start="2014-01-01"):
    """Download data with fallback tickers and better error handling"""
    
    # Updated ticker mapping with fallbacks
    fallback_tickers = {
        "equity": ["NIFTYBEES.NS", "^NSEI", "INFY.NS", "TCS.NS"],  # Nifty ETF, Nifty Index, or large stocks
        "bonds": ["NETFLTGILT.NS", "GOLDBEES.NS", "KOTAKBANK.NS"],  # Government bonds or gold/bank as proxy
        "cash": ["LIQUIDBEES.NS", "ICICIBANK.NS", "HDFC.NS"]  # Liquid fund or stable stocks
    }
    
    successful_downloads = {}
    
    for sleeve, primary_ticker in ticker_map.items():
        print(f"\nTrying to fetch {sleeve} data...")
        
        # Try primary ticker first
        data = fetch_prices(primary_ticker, start)
        if data is not None and not data.empty:
            data.columns = [sleeve]
            successful_downloads[sleeve] = data
            print(f"✓ Successfully fetched {sleeve} using {primary_ticker}")
            continue
        
        # Try fallback tickers
        if sleeve in fallback_tickers:
            for fallback_ticker in fallback_tickers[sleeve]:
                print(f"  Trying fallback: {fallback_ticker}")
                data = fetch_prices(fallback_ticker, start)
                if data is not None and not data.empty:
                    data.columns = [sleeve]
                    successful_downloads[sleeve] = data
                    print(f"✓ Successfully fetched {sleeve} using fallback {fallback_ticker}")
                    break
        
        if sleeve not in successful_downloads:
            print(f"✗ Failed to fetch data for {sleeve}")
    
    if not successful_downloads:
        raise ValueError("No market data could be downloaded. Please check your internet connection.")
    
    if len(successful_downloads) < 3:
        print(f"Warning: Only {len(successful_downloads)} out of 3 asset classes downloaded successfully")
        # Create synthetic data for missing assets
        if "cash" not in successful_downloads and successful_downloads:
            print("Creating synthetic cash data (0.5% monthly return)")
            sample_data = list(successful_downloads.values())[0]
            cash_data = pd.DataFrame(index=sample_data.index, columns=["cash"])
            cash_data["cash"] = (1.005 ** (np.arange(len(cash_data)) / 12)).cumprod()
            successful_downloads["cash"] = cash_data
    
    # Combine all successful downloads
    frames = list(successful_downloads.values())
    prices = pd.concat(frames, axis=1)
    
    # Handle case where some assets might have different date ranges
    prices = prices.dropna()
    
    if prices.empty:
        raise ValueError("No overlapping data found between assets")
    
    print(f"\nData summary:")
    print(f"Date range: {prices.index[0].strftime('%Y-%m-%d')} to {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"Assets: {list(prices.columns)}")
    print(f"Data points: {len(prices)}")
    
    return prices
def cagr(curve, periods_per_year=12):
    n_years = (curve.index[-1] - curve.index[0]).days/365.25
    return curve.iloc[-1]**(1/n_years)-1

def max_drawdown(curve):
    peak = curve.cummax()
    dd = curve/peak - 1.0
    return dd.min()
def time_to_recover(curve):
    # Longest number of months from any peak to when it’s reattained
    peaks = curve.cummax()
    longest = 0
    start_peak = None
    for i in range(1, len(curve)):
        if curve.iloc[i] < peaks.iloc[i-1]:
            # we are below a peak – start timing if not already
            if start_peak is None:
                start_peak = peaks.iloc[i-1]
                start_date = curve.index[i-1]
        else:
            # we recovered (>= previous peak)
            if start_peak is not None:
                months = (curve.index[i] - start_date).days // 30
                longest = max(longest, months)
                start_peak = None
    return longest if longest > 0 else None

if __name__=="__main__":
    tickers = {
    "equity": "NIFTYBEES.NS",     # Nifty 50
    "bonds":  "NETFLTGILT.NS",    # 8-13y G-Sec (long gilt)
    "cash":   "LIQUIDBEES.NS"     # cash proxy
    }
    weights = {"equity":0.60, "bonds":0.35, "cash":0.05}  # e.g., Balanced baseline

    prices = yf.download(list(tickers.values()), start="2007-01-01", auto_adjust=True)["Close"].dropna()
    prices.columns = {v:k for k,v in tickers.items()}  # rename to sleeves

# Monthly returns (use last business day)
    mclose = prices.resample("M").last()
    rets   = mclose.pct_change().dropna()

# Monthly rebalance to target weights (constant-mix)
    port_rets = (rets * pd.Series(weights)).sum(axis=1)

# Equity curve (₹1 start)
    curve = (1 + port_rets).cumprod()
