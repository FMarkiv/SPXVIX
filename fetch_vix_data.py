"""
Fetch VIX and VIX3M historical data.

Tries three sources in order:
  1. Yahoo Finance (yfinance) - longest VIX3M history (~2002)
  2. CBOE CDN (direct CSV)   - authoritative source
  3. FRED (direct CSV)       - most stable endpoint

Usage:
    pip install yfinance pandas
    python fetch_vix_data.py

Output:
    VIX.csv   - CBOE Volatility Index daily data since 1990
    VIX3M.csv - CBOE 3-Month Volatility Index daily data since ~2002-2007
"""

import pandas as pd

# --- Source 1: Yahoo Finance (yfinance) ---

def fetch_yfinance(ticker, start_date):
    """Download from Yahoo Finance via yfinance."""
    import yfinance as yf
    print(f"  Trying Yahoo Finance ({ticker})...")
    df = yf.download(ticker, start=start_date, auto_adjust=False)
    if df.empty:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


# --- Source 2: CBOE CDN ---

CBOE_URLS = {
    "VIX": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
    "VIX3M": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv",
}

def fetch_cboe(name):
    """Download directly from CBOE CDN."""
    print(f"  Trying CBOE CDN ({name})...")
    url = CBOE_URLS[name]
    df = pd.read_csv(url, parse_dates=["DATE"], index_col="DATE")
    df.index.name = "Date"
    df.columns = [c.capitalize() for c in df.columns]
    return df


# --- Source 3: FRED ---

FRED_SERIES = {
    "VIX": "VIXCLS",
    "VIX3M": "VXVCLS",
}

def fetch_fred(name):
    """Download from FRED direct CSV endpoint (no API key needed)."""
    series = FRED_SERIES[name]
    print(f"  Trying FRED ({series})...")
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    df = pd.read_csv(url, parse_dates=["DATE"], index_col="DATE", na_values=".")
    df.index.name = "Date"
    df.columns = ["Close"]
    df = df.dropna()
    return df


# --- Main logic ---

def fetch_and_save(name, filename, yf_ticker, yf_start):
    """Try each source in order until one succeeds."""
    print(f"\nFetching {name}...")

    # Try yfinance first (longest history for VIX3M)
    try:
        df = fetch_yfinance(yf_ticker, yf_start)
        if df is not None and not df.empty:
            df.to_csv(filename)
            print(f"  Saved {filename}: {len(df)} rows, {df.index.min().date()} to {df.index.max().date()} (Yahoo Finance)")
            return True
    except Exception as e:
        print(f"  Yahoo Finance failed: {e}")

    # Try CBOE
    try:
        df = fetch_cboe(name)
        if df is not None and not df.empty:
            df.to_csv(filename)
            print(f"  Saved {filename}: {len(df)} rows, {df.index.min().date()} to {df.index.max().date()} (CBOE)")
            return True
    except Exception as e:
        print(f"  CBOE failed: {e}")

    # Try FRED
    try:
        df = fetch_fred(name)
        if df is not None and not df.empty:
            df.to_csv(filename)
            print(f"  Saved {filename}: {len(df)} rows, {df.index.min().date()} to {df.index.max().date()} (FRED)")
            return True
    except Exception as e:
        print(f"  FRED failed: {e}")

    print(f"  ERROR: All sources failed for {name}.")
    return False


if __name__ == "__main__":
    # VIX: available from Jan 1990
    fetch_and_save("VIX", "VIX.csv", "^VIX", "1990-01-01")

    # VIX3M: yfinance has data from ~2002, CBOE/FRED from Dec 2007
    fetch_and_save("VIX3M", "VIX3M.csv", "^VIX3M", "2002-01-01")

    print("\nDone.")
