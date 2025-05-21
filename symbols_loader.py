import pandas as pd
import requests
from io import StringIO

def get_nse_symbols():
    url = "https://www1.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        data = pd.read_csv(StringIO(response.text))
        data['Symbol'] = data['SYMBOL'].str.strip() + '.NS'
        return sorted(data['Symbol'].tolist())
    except Exception as e:
        print("Failed to fetch NSE symbols:", e)
        return []

