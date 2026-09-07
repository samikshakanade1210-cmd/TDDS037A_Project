# import streamlit as st
# import requests
# import pandas as pd

# # Page setup
# st.set_page_config(page_title="Portfolio Risk Analytics Engine", layout="wide")

# st.title("🏥 Portfolio Risk Analytics & Health Engine")
# st.markdown("A Full-Stack FinTech Dashboard for Real-Time Systematic Risk & Volatility Assessment.")

# # Initialize session state keys for inputs (starts empty by default)
# if "ticker1" not in st.session_state:
#     st.session_state["ticker1"] = ""
#     st.session_state["ticker2"] = ""
#     st.session_state["ticker3"] = ""
#     st.session_state["w1"] = 0.00
#     st.session_state["w2"] = 0.00
#     st.session_state["w3"] = 0.00

# # --- SIDEBAR CONFIGURATION ---
# st.sidebar.header("👤 Investor Configuration")

# # Empty investor name field by default
# user_name = st.sidebar.text_input(
#     "Investor Name", 
#     value="", 
#     placeholder="Type your name here..."
# )

# st.sidebar.markdown("---")
# st.sidebar.subheader("⚡ Quick Test Presets (Optional)")
# st.sidebar.caption("Click a preset to auto-fill sample stocks, or leave blank to enter manually:")

# col_p1, col_p2 = st.sidebar.columns(2)

# if col_p1.button("💻 Tech Portfolio"):
#     st.session_state["ticker1"] = "TCS.NS"
#     st.session_state["ticker2"] = "INFY.NS"
#     st.session_state["ticker3"] = "HCLTECH.NS"
#     st.session_state["w1"], st.session_state["w2"], st.session_state["w3"] = 0.40, 0.30, 0.30
#     st.rerun()

# if col_p2.button("🚗 Auto/Steel"):
#     st.session_state["ticker1"] = "TATAMOTORS.NS"
#     st.session_state["ticker2"] = "TATASTEEL.NS"
#     st.session_state["ticker3"] = "RELIANCE.NS"
#     st.session_state["w1"], st.session_state["w2"], st.session_state["w3"] = 0.50, 0.30, 0.20
#     st.rerun()

# if st.sidebar.button("🧹 Clear All Fields"):
#     st.session_state["ticker1"] = ""
#     st.session_state["ticker2"] = ""
#     st.session_state["ticker3"] = ""
#     st.session_state["w1"], st.session_state["w2"], st.session_state["w3"] = 0.00, 0.00, 0.00
#     st.rerun()

# st.sidebar.markdown("---")
# st.sidebar.markdown("### 📌 Ticker Format Rules:")
# st.sidebar.markdown("- **Indian NSE Stocks:** Append `.NS` (e.g., `TATASTEEL.NS`, `RELIANCE.NS`)")
# st.sidebar.markdown("- **Market Benchmark:** Uses `^NSEI` (Nifty 50)")

# # Main Portfolio Form Input
# with st.form("portfolio_form"):
#     st.subheader("📊 Define Asset Weights & Tickers")
#     st.info("💡 Tip: Asset weights must sum up to exactly 1.0 (e.g., 0.40 + 0.30 + 0.30 = 1.0)")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         ticker1 = st.text_input("Stock Ticker 1", value=st.session_state["ticker1"], placeholder="e.g. RELIANCE.NS").upper()
#         ticker2 = st.text_input("Stock Ticker 2", value=st.session_state["ticker2"], placeholder="e.g. TCS.NS").upper()
#         ticker3 = st.text_input("Stock Ticker 3", value=st.session_state["ticker3"], placeholder="e.g. INFY.NS").upper()
    
#     with col2:
#         weight1 = st.number_input("Weight Asset 1", value=st.session_state["w1"], min_value=0.0, max_value=1.0, step=0.05, format="%.2f")
#         weight2 = st.number_input("Weight Asset 2", value=st.session_state["w2"], min_value=0.0, max_value=1.0, step=0.05, format="%.2f")
#         weight3 = st.number_input("Weight Asset 3", value=st.session_state["w3"], min_value=0.0, max_value=1.0, step=0.05, format="%.2f")
        
#     submit_btn = st.form_submit_button(label="🩺 Execute Live Health Audit")

# # Form submission logic & validation
# if submit_btn:
#     # Retain manually typed inputs in session state
#     st.session_state["ticker1"] = ticker1
#     st.session_state["ticker2"] = ticker2
#     st.session_state["ticker3"] = ticker3
#     st.session_state["w1"] = weight1
#     st.session_state["w2"] = weight2
#     st.session_state["w3"] = weight3

#     # 1. Strict Name Check
#     if not user_name.strip():
#         st.warning("⚠️ Please enter your Investor Name in the sidebar on the left before executing the audit!")
#     # 2. Tickers Check
#     elif not ticker1 or not ticker2 or not ticker3:
#         st.warning("⚠️ Please fill in all three stock tickers.")
#     # 3. Weights Check
#     elif round(weight1 + weight2 + weight3, 2) != 1.00:
#         st.error(f"❌ Sum of weights is {round(weight1 + weight2 + weight3, 2)}. Total weight must equal exactly 1.00 (100%).")
#     else:
#         payload = {
#             "user_name": user_name,
#             "tickers": [ticker1, ticker2, ticker3],
#             "weights": [weight1, weight2, weight3]
#         }
        
#         st.info("🔄 Connecting to FastAPI Microservice Backend & streaming live Yahoo Finance data...")
        
#         try:
#             response = requests.post("http://127.0.0.1:8000/analyze", json=payload)
            
#             if response.status_code == 200:
#                 result = response.json()
                
#                 st.success(f"✅ Risk Audit Complete for {result['client_name']}!")
                
#                 # Executive Summary Metrics
#                 st.subheader("📊 Executive Metrics Summary")
#                 m1, m2 = st.columns(2)
#                 with m1:
#                     st.metric(label="Overall Portfolio Beta (Systematic Risk)", value=result["overall_portfolio_beta"])
#                 with m2:
#                     warning_text = result["sector_concentration_status"]
#                     if "CRITICAL" in warning_text:
#                         st.error(f"⚠️ {warning_text}")
#                     else:
#                         st.success(f"✅ {warning_text}")

#                 st.markdown("---")

#                 # Sector Breakdown Chart
#                 st.subheader("🍕 Sector Allocation Breakdown")
#                 sector_data = result["sector_breakdown"]
#                 df_sector = pd.DataFrame(list(sector_data.items()), columns=["Sector", "Allocation %"])
#                 st.bar_chart(data=df_sector, x="Sector", y="Allocation %")

#                 # Individual Asset Breakdown Table
#                 st.subheader("📋 Individual Asset Health & Risk Details")
#                 assets_dict = result["individual_assets"]
#                 df_assets = pd.DataFrame.from_dict(assets_dict, orient='index')
#                 st.dataframe(df_assets, use_container_width=True)

#                 # Export to CSV Button
#                 st.markdown("---")
#                 csv_data = df_assets.to_csv(index=True).encode('utf-8')
#                 st.download_button(
#                     label="📥 Export Risk Audit Report (.CSV)",
#                     data=csv_data,
#                     file_name=f"{user_name.strip().replace(' ', '_')}_Portfolio_Risk_Report.csv",
#                     mime="text/csv"
#                 )

#             else:
#                 err_msg = response.json().get("detail", "Validation Failed")
#                 st.error(f"❌ Backend Validation Error: {err_msg}")
                
#         except requests.exceptions.ConnectionError:
#             st.error("❌ Could not reach FastAPI Backend! Make sure 'uvicorn main:app --reload' is running in Terminal 1.")

# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="Portfolio Risk Analytics Engine", layout="wide")
# st.title("📊 Real-Time Portfolio Risk Analytics Engine")

# st.sidebar.header("Portfolio Inputs")
# tickers_input = st.sidebar.text_input("Tickers (Comma Separated)", "TCS.NS, RELIANCE.NS, INFY.NS")
# weights_input = st.sidebar.text_input("Weights (Comma Separated)", "0.4, 0.4, 0.2")

# try:
#     tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
#     weights = [float(w.strip()) for w in weights_input.split(",") if w.strip()]
# except ValueError:
#     st.sidebar.error("Invalid input! Ensure weights are numbers.")

# if st.sidebar.button("Analyze Portfolio Risk"):
#     if len(tickers) != len(weights):
#         st.error("Error: Number of tickers must match the number of weights!")
#     else:
#         api_url = "http://127.0.0.1:8000/analyze_portfolio"
#         payload = {"tickers": tickers, "weights": weights}
        
#         try:
#             response = requests.post(api_url, json=payload)
#             if response.status_code == 200:
#                 data = response.json()
                
#                 # Render Sector Warning Alert Box
#                 if data.get("critical_warning"):
#                     st.error(data["critical_warning"])
#                 else:
#                     st.success("Portfolio weight validation passed (Sum = 100%). Diversification parameters optimal.")
                
#                 col1, col2 = st.columns([3, 2])
                
#                 with col1:
#                     st.subheader("Asset Risk Profiles")
#                     df_profiles = pd.DataFrame(data["asset_profiles"]).T
#                     st.dataframe(df_profiles, use_container_width=True)
                    
#                     csv_data = df_profiles.to_csv().encode('utf-8')
#                     st.download_button(
#                         label="📥 Download Risk Audit Report (CSV)",
#                         data=csv_data,
#                         file_name="portfolio_risk_report.csv",
#                         mime="text/csv"
#                     )
                    
#                 with col2:
#                     st.subheader("Sector Allocation Breakdown")
#                     fig = px.pie(
#                         names=list(data["sector_distribution"].keys()), 
#                         values=list(data["sector_distribution"].values()),
#                         hole=0.4
#                     )
#                     st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.error(f"API Error: {response.json().get('detail')}")
#         except Exception as e:
#             st.error(f"Failed to connect to FastAPI backend: {e}. Is FastAPI server running?")


# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="Portfolio Risk Analytics & Health Engine", layout="wide")

# st.title("🏥 Portfolio Risk Analytics & Health Engine")
# st.caption("A Full-Stack FinTech Dashboard for Real-Time Systematic Risk & Volatility Assessment.")

# # Sidebar Configuration
# st.sidebar.header("👤 Investor Configuration")
# investor_name = st.sidebar.text_input("Investor Name", placeholder="Type your name here...")

# st.sidebar.subheader("⚡ Quick Test Presets (Optional)")
# st.sidebar.caption("Click a preset to auto-fill sample stocks, or leave blank to enter manually:")

# col_p1, col_p2 = st.sidebar.columns(2)

# # Session State for Presets
# if "t1" not in st.session_state:
#     st.session_state.t1, st.session_state.w1 = "", 0.00
#     st.session_state.t2, st.session_state.w2 = "", 0.00
#     st.session_state.t3, st.session_state.w3 = "", 0.00

# if col_p1.button("💻 Tech Portfolio"):
#     st.session_state.t1, st.session_state.w1 = "TCS.NS", 0.40
#     st.session_state.t2, st.session_state.w2 = "INFY.NS", 0.40
#     st.session_state.t3, st.session_state.w3 = "RELIANCE.NS", 0.20

# if col_p2.button("🚗 Auto/Steel"):
#     st.session_state.t1, st.session_state.w1 = "TATAMOTORS.NS", 0.50
#     st.session_state.t2, st.session_state.w2 = "TATASTEEL.NS", 0.30
#     st.session_state.t3, st.session_state.w3 = "HDFCBANK.NS", 0.20

# if st.sidebar.button("🧹 Clear All Fields"):
#     st.session_state.t1, st.session_state.w1 = "", 0.00
#     st.session_state.t2, st.session_state.w2 = "", 0.00
#     st.session_state.t3, st.session_state.w3 = "", 0.00

# st.sidebar.markdown("---")
# st.sidebar.subheader("📌 Ticker Format Rules:")
# st.sidebar.markdown("- **Indian NSE Stocks:** Append `.NS` (e.g., `TATASTEEL.NS`, `RELIANCE.NS`)")
# st.sidebar.markdown("- **Market Benchmark:** Uses `^NSEI` (Nifty 50)")

# # Main Form Container
# with st.container():
#     st.subheader("📊 Define Asset Weights & Tickers")
#     st.info("💡 Tip: Asset weights must sum up to exactly 1.0 (e.g., 0.40 + 0.30 + 0.30 = 1.0)")

#     col1, col2 = st.columns([2, 1])
#     with col1:
#         t1 = st.text_input("Stock Ticker 1", value=st.session_state.t1, placeholder="e.g. RELIANCE.NS")
#     with col2:
#         w1 = st.number_input("Weight Asset 1", min_value=0.0, max_value=1.0, value=float(st.session_state.w1), step=0.05)

#     col3, col4 = st.columns([2, 1])
#     with col3:
#         t2 = st.text_input("Stock Ticker 2", value=st.session_state.t2, placeholder="e.g. TCS.NS")
#     with col4:
#         w2 = st.number_input("Weight Asset 2", min_value=0.0, max_value=1.0, value=float(st.session_state.w2), step=0.05)

#     col5, col6 = st.columns([2, 1])
#     with col5:
#         t3 = st.text_input("Stock Ticker 3", value=st.session_state.t3, placeholder="e.g. INFY.NS")
#     with col6:
#         w3 = st.number_input("Weight Asset 3", min_value=0.0, max_value=1.0, value=float(st.session_state.w3), step=0.05)

#     analyze_btn = st.button("🩺 Execute Live Health Audit")

# # Execution & Results Section
# if analyze_btn:
#     tickers = [t.strip().upper() for t in [t1, t2, t3] if t.strip()]
#     weights = [w for t, w in zip([t1, t2, t3], [w1, w2, w3]) if t.strip()]

#     if not tickers:
#         st.error("Please enter at least one stock ticker!")
#     else:
#         api_url = "http://127.0.0.1:8000/analyze_portfolio"
#         payload = {"tickers": tickers, "weights": weights}

#         try:
#             response = requests.post(api_url, json=payload)
#             if response.status_code == 200:
#                 data = response.json()

#                 if investor_name:
#                     st.success(f"Audit Complete for Investor: **{investor_name}**")

#                 if data.get("critical_warning"):
#                     st.error(data["critical_warning"])
#                 else:
#                     st.success("✅ Portfolio Weight Validation Passed ($\sum w_i = 1.0$). Sector Allocation Optimal.")

#                 res_col1, res_col2 = st.columns([3, 2])

#                 with res_col1:
#                     st.subheader("Asset Risk Profiles")
#                     df_profiles = pd.DataFrame(data["asset_profiles"]).T
#                     st.dataframe(df_profiles, use_container_width=True)

#                     csv_data = df_profiles.to_csv().encode('utf-8')
#                     st.download_button(
#                         label="📥 Download Risk Audit Report (CSV)",
#                         data=csv_data,
#                         file_name="portfolio_risk_report.csv",
#                         mime="text/csv"
#                     )

#                 with res_col2:
#                     st.subheader("Sector Allocation Breakdown")
#                     fig = px.pie(
#                         names=list(data["sector_distribution"].keys()),
#                         values=list(data["sector_distribution"].values()),
#                         hole=0.4
#                     )
#                     st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.error(f"API Error: {response.json().get('detail')}")
#         except Exception as e:
#             st.error(f"Failed to connect to FastAPI backend: {e}. Ensure Uvicorn server is running on port 8000.")

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

if col_p2.button("🚗 Auto/Steel"):
    st.session_state.tickers_val = "TATAMOTORS.NS, TATASTEEL.NS, HDFCBANK.NS"
    st.session_state.weights_val = "0.50, 0.30, 0.20"

if st.sidebar.button("🧹 Clear All Fields"):
    st.session_state.tickers_val = ""
    st.session_state.weights_val = ""

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