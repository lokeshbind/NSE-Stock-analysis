import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

st.title("📈 NSE Stock Analyzer – June Returns")
st.write("Analyze Indian stocks that consistently gained **10%+ in June** over the past 10 years.")

tickers = st.text_area("Enter NSE Ticker Symbols (comma-separated, like INFY.NS, RELIANCE.NS)", 
                       "RELIANCE.NS, HDFCBANK.NS, TCS.NS, SBIN.NS").split(',')

tickers = [t.strip().upper() for t in tickers if t.strip()]

min_years = st.slider("Minimum Years with ≥10% Gain in June", min_value=1, max_value=10, value=7)

if st.button("Run Analysis"):
    with st.spinner("Fetching data..."):
        today = date.today()
        years = list(range(today.year - 10, today.year))
        results = []

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                success_count = 0
                yearly_returns = []

                for year in years:
                    start = date(year, 6, 1)
                    end = date(year, 6, 30)
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
                        'Avg_June_Return': avg_return,
                        'Yearly_June_Returns': yearly_returns
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

