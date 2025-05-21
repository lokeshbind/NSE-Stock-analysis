print("symbols_loader.py started")

# rest of your code below...
import pandas as pd
import requests
from io import StringIO

def get_nse_symbols():
    url = "https://www1.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/",
    }
    try:
        print("Fetching symbols from NSE...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"HTTP Status Code: {response.status_code}")

        data = pd.read_csv(StringIO(response.text))
        print(f"Total rows fetched: {len(data)}")

        # Filter only equity shares with 'EQ' series
        data = data[data[' SERIES '] == 'EQ']
        print(f"Rows after filtering 'EQ' series: {len(data)}")

        data['Symbol'] = data['SYMBOL'].str.strip() + '.NS'
        symbols = sorted(data['Symbol'].tolist())
        print(f"Total symbols processed: {len(symbols)}")

        return symbols
    except Exception as e:
        print("Failed to fetch NSE symbols:", e)
        return []

if __name__ == "__main__":
    symbols = get_nse_symbols()
    print(symbols)
