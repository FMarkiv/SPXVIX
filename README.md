# SPXVIX
VIX vs S&P 500

## Data Files

- `SP500.csv`: S&P 500 time series since 12-30-1927 (source: Yahoo Finance)
- `DJA.csv`: DOW time series since 05-02-1885 (converted to Yahoo Finance format)
- `DJA-orig.csv`: DOW time series original format (source: measuringworth.com)
- `VIX.csv`: CBOE Volatility Index daily data since 1990
- `VIX3M.csv`: CBOE 3-Month Volatility Index daily data since 2007
- `dow.ipynb`: Conversion tool for DJA from measuringworth format to Yahoo Finance format

## Fetching VIX Data

```bash
pip install yfinance pandas
python fetch_vix_data.py
```

This downloads `VIX.csv` and `VIX3M.csv` from Yahoo Finance.
