import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Large Cap Financial Dashboard", layout="wide")
st.title("📈 Large Cap Financial Dashboard")

# Color scales
risk_colorscale = [[0.0, "green"], [0.5, "yellow"], [1.0, "red"]]
payout_colorscale = [[0.0, "red"], [0.5, "yellow"], [1.0, "green"]]

# -----------------------------
# Fetch data
# -----------------------------
large_cap_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "NFLX", "ORCL", "CRM", "CSCO", "IBM", "PLTR", "INTU", "V", "MA"]
info = {}

for ticker in large_cap_tickers:
    try:
        company = yf.Ticker(ticker)
        data = company.info
        info[ticker] = {
            'Ticker': ticker,
            'Sector': data.get('sector', 'N/A'),
            'Industry': data.get('industry', 'N/A'),
            'Market Cap': data.get('marketCap', 'N/A'),
            'Display Name': data.get('shortName', 'N/A'),
            'Employees': data.get('fullTimeEmployees', 'N/A'),
            'Overall Risk': data.get('overallRisk', 'N/A'),
            'Earnings Quarterly Growth': data.get('earningsQuarterlyGrowth', 'N/A'),
            'Payout Ratio': data.get('payoutRatio', 'N/A'),
            'Dividend Yield': data.get('dividendYield', 'N/A')
        }
    except Exception as e:
        st.warning(f"Error fetching info for {ticker}: {e}")

df = pd.DataFrame.from_dict(info, orient='index')
df = df[df.apply(lambda row: all(val != 'N/A' for val in row), axis=1)]
df = df.sort_values(by='Market Cap', ascending=False).head(10)

# Type conversion
df['Market Cap'] = df['Market Cap'].astype(float) / 1e9  # Billions
df['Employees'] = df['Employees'].astype(int)
df['Dividend Yield'] = df['Dividend Yield'].astype(float)
df['Payout Ratio'] = df['Payout Ratio'].astype(float)
df['Earnings Quarterly Growth'] = df['Earnings Quarterly Growth'].astype(float)
df['Overall Risk'] = df['Overall Risk'].astype(int)

# Derived columns
df['Risk-Adjusted Dividend'] = df['Dividend Yield'] / df['Overall Risk']
df['Value Index'] = (df['Earnings Quarterly Growth'] + df['Dividend Yield']) / (df['Overall Risk'] * df['Payout Ratio'])

# -----------------------------
# Helper: Bar Chart
# -----------------------------
def bar_chart(x, y, color, title, color_scale=None):
    fig = px.bar(df, x=x, y=y, color=color, 
                 color_continuous_scale=color_scale if color_scale else None,
                 title=title, hover_name="Display Name")
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    return fig

# -----------------------------
# First 8 charts (in columns)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Market Capitalization by Company (Billion $)")
    st.plotly_chart(bar_chart("Display Name", "Market Cap", "Industry", "Market Cap by Industry"), use_container_width=True)

    st.subheader("3. Dividend Yield by Risk")
    st.plotly_chart(bar_chart("Display Name", "Dividend Yield", "Overall Risk", "Dividend Yield vs Risk", color_scale=risk_colorscale), use_container_width=True)

    st.subheader("5. Quarterly Earnings Growth by Risk")
    st.plotly_chart(bar_chart("Display Name", "Earnings Quarterly Growth", "Overall Risk", "Earnings Growth vs Risk", color_scale=risk_colorscale), use_container_width=True)

    st.subheader("7. Market Cap vs Employees")
    fig7 = px.scatter(
        df, x="Market Cap", y="Employees", size="Dividend Yield", color="Overall Risk",
        color_continuous_scale=risk_colorscale, hover_name="Display Name",
        title="Market Cap vs Employees (Bubble Size = Dividend Yield)"
    )
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("9. Custom Value Index")
    st.plotly_chart(bar_chart("Display Name", "Value Index", "Overall Risk", "Value Index of Companies", color_scale=risk_colorscale), use_container_width=True)

with col2:
    st.subheader("2. Employees by Company")
    st.plotly_chart(bar_chart("Display Name", "Employees", "Industry", "Employees by Industry"), use_container_width=True)

    st.subheader("4. Quarterly Earnings Growth by Industry")
    st.plotly_chart(bar_chart("Display Name", "Earnings Quarterly Growth", "Industry", "Earnings Growth by Industry"), use_container_width=True)

    st.subheader("6. Earnings Growth by Payout Ratio")
    st.plotly_chart(bar_chart("Display Name", "Earnings Quarterly Growth", "Payout Ratio", "Earnings Growth vs Payout Ratio", color_scale=payout_colorscale), use_container_width=True)

    st.subheader("8. Risk-Adjusted Dividend Yield")
    st.plotly_chart(bar_chart("Display Name", "Risk-Adjusted Dividend", "Overall Risk", "Dividend ÷ Risk", color_scale=risk_colorscale), use_container_width=True)

    st.subheader("🔍 Radar Chart: Company Financial Profile")
    radar_company = st.selectbox("Choose a Company for Radar Chart", df["Display Name"])
    row = df[df["Display Name"] == radar_company].iloc[0]

    radar_data = {
        'Market Cap': row['Market Cap'] / df['Market Cap'].max(),
        'Employees': row['Employees'] / df['Employees'].max(),
        'Dividend Yield': row['Dividend Yield'] / df['Dividend Yield'].max(),
        'Earnings Growth': row['Earnings Quarterly Growth'] / df['Earnings Quarterly Growth'].max(),
        'Payout Ratio': row['Payout Ratio'] / df['Payout Ratio'].max()
    }

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=list(radar_data.values()),
        theta=list(radar_data.keys()),
        fill='toself',
        name=radar_company
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                            showlegend=False, title=f"{radar_company} Profile Radar")
    st.plotly_chart(fig_radar, use_container_width=True)
