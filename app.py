import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Portfolio Risk Analytics & Health Engine", layout="wide")

st.title("🏥 Portfolio Risk Analytics & Health Engine")
st.caption("A Full-Stack FinTech Dashboard for Real-Time Systematic Risk & Volatility Assessment.")

# Sidebar Configuration (Restored to Previous Layout)
st.sidebar.header("👤 Investor Configuration")
investor_name = st.sidebar.text_input("Investor Name", placeholder="Type your name here...")

st.sidebar.subheader("⚡ Quick Test Presets (Optional)")
st.sidebar.caption("Click a preset to auto-fill sample stocks, or leave blank to enter manually:")

col_p1, col_p2 = st.sidebar.columns(2)

# Session State for Presets
if "tickers_val" not in st.session_state:
    st.session_state.tickers_val = ""
    st.session_state.weights_val = ""

if col_p1.button("💻 Tech Portfolio"):
    st.session_state.tickers_val = "TCS.NS, INFY.NS, RELIANCE.NS"
    st.session_state.weights_val = "0.40, 0.40, 0.20"
    st.rerun()

if col_p2.button("🚗 Auto/Steel"):
    st.session_state.tickers_val = "TATAMOTORS.NS, TATASTEEL.NS, HDFCBANK.NS"
    st.session_state.weights_val = "0.50, 0.30, 0.20"
    st.rerun()

if st.sidebar.button("🧹 Clear All Fields"):
    st.session_state.tickers_val = ""
    st.session_state.weights_val = ""
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Ticker Format Rules:")
st.sidebar.markdown("- **Indian NSE Stocks:** Append `.NS` (e.g., `TATASTEEL.NS`, `RELIANCE.NS`)")
st.sidebar.markdown("- **Market Benchmark:** Uses `^NSEI` (Nifty 50)")

# Main Form Container (Placeholders used, no hardcoded default values)
with st.container():
    st.subheader("📊 Define Asset Weights & Tickers")
    st.info("💡 Tip: Asset weights must sum up to exactly 1.0 (e.g., 0.40 + 0.30 + 0.30 = 1.0)")

    tickers_input = st.text_input(
        "Stock Tickers (Comma Separated)", 
        value=st.session_state.tickers_val,
        placeholder="e.g. RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS"
    )
    
    weights_input = st.text_input(
        "Asset Weights (Comma Separated)", 
        value=st.session_state.weights_val,
        placeholder="e.g. 0.40, 0.30, 0.20, 0.10"
    )

    analyze_btn = st.button("🩺 Execute Live Health Audit")

# Execution & Results Section
if analyze_btn:
    try:
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
        weights = [float(w.strip()) for w in weights_input.split(",") if w.strip()]
    except ValueError:
        st.error("Invalid input! Ensure weights are numbers separated by commas.")
        tickers, weights = [], []

    if not tickers:
        st.error("Please enter at least one stock ticker!")
    elif len(tickers) != len(weights):
        st.error(f"Error: Entered {len(tickers)} tickers but {len(weights)} weights. Count must match!")
    else:
        api_url = "http://127.0.0.1:8000/analyze_portfolio"
        payload = {"tickers": tickers, "weights": weights}

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()

                if investor_name:
                    st.success(f"Audit Complete for Investor: **{investor_name}**")

                if data.get("critical_warning"):
                    st.error(data["critical_warning"])
                else:
                    st.success("✅ Portfolio Weight Validation Passed ($\sum w_i = 1.0$). Sector Allocation Optimal.")

                res_col1, res_col2 = st.columns([3, 2])

                with res_col1:
                    st.subheader("Asset Risk Profiles")
                    df_profiles = pd.DataFrame(data["asset_profiles"]).T
                    st.dataframe(df_profiles, use_container_width=True)

                    csv_data = df_profiles.to_csv().encode('utf-8')
                    st.download_button(
                        label="📥 Download Risk Audit Report (CSV)",
                        data=csv_data,
                        file_name="portfolio_risk_report.csv",
                        mime="text/csv"
                    )

                with res_col2:
                    st.subheader("Sector Allocation Breakdown")
                    fig = px.pie(
                        names=list(data["sector_distribution"].keys()),
                        values=list(data["sector_distribution"].values()),
                        hole=0.4
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"API Error: {response.json().get('detail')}")
        except Exception as e:
            st.error(f"Failed to connect to FastAPI backend: {e}. Ensure Uvicorn server is running on port 8000.")