
# 📊 Large Cap Financial Dashboard

An elegant, interactive Streamlit-based dashboard that provides a deep dive into the financial profiles of leading large-cap companies. This project goes beyond surface-level analytics—merging insightful data with beautiful visualizations for investors, analysts, and curious minds alike.

---

## ✨ Features

- **Real-Time Data Fetching**: Harnesses the power of [Yahoo Finance](https://finance.yahoo.com) via `yfinance` to pull real-time data for a curated list of large-cap tickers.
- **Interactive Visualizations**: Leverages Plotly Express and Graph Objects for rich, dynamic charts.
- **In-Depth Comparisons**: View financial metrics like:
  - Market Capitalization
  - Employees
  - Dividend Yield
  - Earnings Quarterly Growth
  - Payout Ratio
  - Risk-Adjusted Dividend
  - Custom Value Index
- **Custom Radar Charts**: Select a company and instantly view its comparative financial profile via a radar chart.
- **User-Friendly Interface**: Built with Streamlit’s wide-layout for a seamless dual-column experience.

---

## 📌 Technologies Used

- **Python**
- **Streamlit**
- **Plotly**
- **Pandas**
- **YFinance**

---

## 🧠 The Custom Value Index

To bring a nuanced view of performance and sustainability, this dashboard introduces a **Custom Value Index** calculated as:

```
(Earnings Growth + Dividend Yield) / (Overall Risk × Payout Ratio)
```

This metric attempts to balance potential rewards with risks and obligations—an insightful blend for modern-day investors.

---

## 📦 Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/large-cap-financial-dashboard.git
cd large-cap-financial-dashboard
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```

---

## 🔍 Ticker Coverage

Includes an elite selection of large-cap tickers from various sectors:

```
AAPL, MSFT, NVDA, AMZN, GOOGL, META, AVGO, TSLA, NFLX, ORCL, CRM, CSCO, IBM, PLTR, INTU, V, MA
```

---

## 🎯 Ideal For

- Financial analysts & advisors
- Retail investors exploring fundamentals
- Students learning about financial data
- Dashboard lovers & data storytellers

---

## 📈 Dashboard

[**View My Dashboard Here**](https://kn-dashboards-stockmarketanalysiscapitalizationdata.streamlit.app/)

---

## 💡 Final Thought

> Data is only as powerful as its interpretation. This dashboard strives to offer clarity amidst complexity—where insight meets interface.


Enjoy the analysis!🍻
