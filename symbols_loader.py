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
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = pd.read_csv(StringIO(response.text))
        # Filter only equity shares with 'EQ' series
        data = data[data[' SERIES '] == 'EQ']
        # Clean and append suffix
        data['Symbol'] = data['SYMBOL'].str.strip() + '.NS'
        return sorted(data['Symbol'].tolist())
    except Exception as e:
        print("Failed to fetch NSE symbols:", e)
        return []
if __name__ == "__main__":
    print(get_nse_symbols())
