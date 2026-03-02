"""
Fetch VIX and VIX3M historical data from Yahoo Finance.

Usage:
    pip install yfinance pandas
    python fetch_vix_data.py

Output:
    VIX.csv   - CBOE Volatility Index (^VIX) daily data since 1990
    VIX3M.csv - CBOE 3-Month Volatility Index (^VIX3M) daily data since 2007
"""

import yfinance as yf
import pandas as pd


def fetch_and_save(ticker, filename, start_date):
    print(f"Downloading {ticker}...")
    df = yf.download(ticker, start=start_date, auto_adjust=False)

    if df.empty:
        print(f"ERROR: No data returned for {ticker}. Check your internet connection.")
        return False

    # Flatten multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.to_csv(filename)
    print(f"Saved {filename}: {len(df)} rows, {df.index.min().date()} to {df.index.max().date()}")
    return True


if __name__ == "__main__":
    # VIX data available from ~Jan 1990
    fetch_and_save("^VIX", "VIX.csv", "1990-01-01")

    # VIX3M data available from ~Dec 2007
    fetch_and_save("^VIX3M", "VIX3M.csv", "2007-01-01")

    print("\nDone.")
