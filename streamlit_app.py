import streamlit as st
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

today = date(2025, 4, 19)
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")

# --- Data Fetching ---
@st.cache_data
def fetch_top_n_market_cap(date_str, n=10):
    # Using a list of well-known large-cap companies as a starting point
    # as directly fetching historical top market cap data is complex.
    # This list can be expanded or modified.
    large_cap_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK.A", "TSM", "TSLA", "LLY", "JPM", "V", "XOM", "MA"]
    data = yf.download(large_cap_tickers, start=date_str, end=date_str)
    if not data.empty:
        latest_prices = data['Adj Close'].iloc[-1]
        market_caps = {}
        for ticker, price in latest_prices.items():
            try:
                # Get shares outstanding (approximation using info)
                ticker_info = yf.Ticker(ticker).info
                shares_outstanding = ticker_info.get('sharesOutstanding')
                if shares_outstanding:
                    market_caps[ticker] = price * shares_outstanding
            except Exception as e:
                print(f"Could not fetch shares outstanding for {ticker}: {e}")

        market_cap_df = pd.DataFrame(list(market_caps.items()), columns=['Ticker', 'Market Cap'])
        market_cap_df_sorted = market_cap_df.sort_values(by='Market Cap', ascending=False).head(n)
        return market_cap_df_sorted
    else:
        return pd.DataFrame({'Ticker': [], 'Market Cap': []})

@st.cache_data
def fetch_company_info(tickers):
    info = {}
    for ticker in tickers:
        try:
            company = yf.Ticker(ticker)
            info[ticker] = {
                'sector': company.info.get('sector', 'N/A'),
                'industry': company.info.get('industry', 'N/A'),
                'longBusinessSummary': company.info.get('longBusinessSummary', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            info[ticker] = {'sector': 'N/A', 'industry': 'N/A', 'longBusinessSummary': 'N/A'}
    return pd.DataFrame.from_dict(info, orient='index')

top_companies_df = fetch_top_n_market_cap(yesterday_str)

if not top_companies_df.empty:
    top_tickers = top_companies_df['Ticker'].tolist()
    company_info_df = fetch_company_info(top_tickers)
    company_info_df['Ticker'] = company_info_df.index
    merged_df = pd.merge(top_companies_df, company_info_df, on='Ticker')
else:
    st.error("Could not fetch top companies data.")
    st.stop()

# --- Streamlit Dashboard ---
st.title(f"Top 10 Companies by Market Capitalization ({yesterday_str})")
st.subheader("Visual Comparison")

# 1. Bar Chart of Market Capitalization
fig_market_cap = px.bar(merged_df, x='Ticker', y='Market Cap', title='Market Capitalization of Top 10 Companies',
                        labels={'Market Cap': 'Market Capitalization (USD)'})
st.plotly_chart(fig_market_cap)

# 2. Bar Chart of Companies by Sector
sector_counts = merged_df['sector'].value_counts().reset_index()
sector_counts.columns = ['Sector', 'Number of Companies']
fig_sector = px.bar(sector_counts, x='Sector', y='Number of Companies', title='Number of Top Companies per Sector',
                    labels={'Number of Companies': 'Count'})
st.plotly_chart(fig_sector)

# 3. Bar Chart of Companies by Industry (Top 5)
industry_counts = merged_df['industry'].value_counts().head(5).reset_index()
industry_counts.columns = ['Industry', 'Number of Companies']
fig_industry = px.bar(industry_counts, x='Industry', y='Number of Companies', title='Number of Top Companies per Industry (Top 5)',
                      labels={'Number of Companies': 'Count'})
st.plotly_chart(fig_industry)

# 4. Scatter Plot of Market Cap vs. Sector (using categorical color)
fig_scatter_sector = px.scatter(merged_df, x='Ticker', y='Market Cap', color='sector',
                                title='Market Capitalization by Sector',
                                labels={'Market Cap': 'Market Capitalization (USD)'})
st.plotly_chart(fig_scatter_sector)

# 5. Scatter Plot of Market Cap vs. Industry (using categorical color)
fig_scatter_industry = px.scatter(merged_df, x='Ticker', y='Market Cap', color='industry',
                                  title='Market Capitalization by Industry',
                                  labels={'Market Cap': 'Market Capitalization (USD)'})
st.plotly_chart(fig_scatter_industry)

# 6. Table of Company Information
st.subheader("Company Information")
st.dataframe(merged_df[['Ticker', 'Market Cap', 'sector', 'industry']])

# 7. Text Display of Business Summaries (Expandable)
st.subheader("Business Summaries")
for index, row in merged_df.iterrows():
    with st.expander(f"Summary for {row['Ticker']}"):
        st.write(row['longBusinessSummary'])

# --- Dataset as of Today ---
st.subheader(f"Top 10 Companies Data (as of {today.strftime('%Y-%m-%d')})")
today_df = fetch_top_n_market_cap(today.strftime("%Y-%m-%d"))
if not today_df.empty:
    st.dataframe(today_df)
else:
    st.info("Today's market data might not be fully available yet.")
