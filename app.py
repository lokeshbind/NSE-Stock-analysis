import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from symbols_loader import get_nse_symbols

st.title("📊 NSE Stock Analyzer with All NSE Symbols")

# Load all NSE symbols
tickers = get_nse_symbols()

if not tickers:
    st.warning("⚠️ Failed to load NSE symbols. Please check your internet connection or NSE site availability.")
    st.stop()
else:
    selected_tickers = st.multiselect(
        "Select stocks to analyze (or type)", 
        tickers, 
        default=tickers[:10]
    )

selected_tickers = st.multiselect(
    "Select stocks to analyze (or type)", 
    tickers, 
    default=tickers[:10]
)

# Choose month range for analysis
start_month = st.selectbox("Start Month", list(range(1, 13)), index=5)  # Default June
end_month = st.selectbox("End Month", list(range(1, 13)), index=5)      # Default June

# Minimum years with ≥10% gain in selected months
min_years = st.slider("Minimum Years with ≥10% Gain", 1, 10, 7)

if st.button("Run Analysis"):
    with st.spinner("Fetching data and analyzing..."):
        today = date.today()
        years = list(range(today.year - 10, today.year))
        results = []

        for ticker in selected_tickers:
            try:
                stock = yf.Ticker(ticker)
                success_count = 0
                yearly_returns = []

                for year in years:
                    start = date(year, start_month, 1)
                    # Use 28 as safe day (to avoid month-end errors)
                    end = date(year, end_month, 28)
                    df = stock.history(start=start, end=end)

                    if df.empty or len(df) < 2:
                        yearly_returns.append(None)
                        continue

                    start_price = df.iloc[0]['Close']
                    end_price = df.iloc[-1]['Close']
                    pct_change = ((end_price - start_price) / start_price) * 100
                    yearly_returns.append(round(pct_change, 2))

                    if pct_change >= 10:
                        success_count += 1

                valid_returns = [r for r in yearly_returns if r is not None]
                if success_count >= min_years and len(valid_returns) >= min_years:
                    avg_return = round(sum(valid_returns) / len(valid_returns), 2)
                    results.append({
                        'Ticker': ticker,
                        'Success_Count': success_count,
                        'Avg_Return': avg_return,
                        'Yearly_Returns': yearly_returns
                    })
            except Exception as e:
                st.error(f"Error with {ticker}: {e}")

        if results:
            result_df = pd.DataFrame(results)
            result_df.sort_values(by='Success_Count', ascending=False, inplace=True)
            st.success(f"Found {len(result_df)} stock(s) meeting your criteria.")
            st.dataframe(result_df)
        else:
            st.warning("No stocks met the criteria.")
