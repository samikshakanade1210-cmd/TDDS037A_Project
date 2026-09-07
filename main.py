# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import yfinance as yf
# import pandas as pd
# import numpy as np
# from scipy.stats import linregress

# app = FastAPI(
#     title="Portfolio Risk Analytics Engine",
#     description="A Stateless Computational Microservice for Financial Risk & Valuation Analytics",
#     version="2.0.0"
# )

# class PortfolioInput(BaseModel):
#     user_name: str
#     tickers: list[str]
#     weights: list[float]

# @app.get("/")
# def home():
#     return {"message": "Portfolio Risk Analytics API Engine is Live!"}

# @app.post("/analyze")
# def analyze_portfolio(data: PortfolioInput):
#     if not (0.99 <= sum(data.weights) <= 1.01):
#         raise HTTPException(
#             status_code=422, 
#             detail="Portfolio weights must sum up to exactly 1.0 (100%)."
#         )
    
#     if len(data.tickers) != len(data.weights):
#         raise HTTPException(
#             status_code=422, 
#             detail="Number of tickers provided does not match number of weights."
#         )

#     # --- BENCHMARK DOWNLOAD FIX ---
#     benchmark_ticker = "^NSEI"
#     try:
#         benchmark_df = yf.download(benchmark_ticker, period="1y", progress=False)
#         # Handle single/multi-index columns cleanly
#         if 'Adj Close' in benchmark_df.columns:
#             benchmark_data = benchmark_df['Adj Close']
#         elif 'Close' in benchmark_df.columns:
#             benchmark_data = benchmark_df['Close']
#         else:
#             benchmark_data = benchmark_df.iloc[:, 0]
            
#         benchmark_returns = benchmark_data.pct_change().dropna()
#         if isinstance(benchmark_returns, pd.DataFrame):
#             benchmark_returns = benchmark_returns.iloc[:, 0]
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Failed to fetch benchmark market data: {str(e)}"
#         )

#     asset_analysis = {}
#     portfolio_beta = 0.0
#     sector_distribution = {}

#     for i, ticker in enumerate(data.tickers):
#         try:
#             stock = yf.Ticker(ticker)
#             info = stock.info
            
#             stock_df = yf.download(ticker, period="1y", progress=False)
#             if 'Adj Close' in stock_df.columns:
#                 stock_data = stock_df['Adj Close']
#             elif 'Close' in stock_df.columns:
#                 stock_data = stock_df['Close']
#             else:
#                 stock_data = stock_df.iloc[:, 0]
                
#             stock_returns = stock_data.pct_change().dropna()
#             if isinstance(stock_returns, pd.DataFrame):
#                 stock_returns = stock_returns.iloc[:, 0]
            
#             combined_df = pd.concat([stock_returns, benchmark_returns], axis=1).dropna()
#             combined_df.columns = ['stock', 'market']
            
#             # Linear Regression OLS for Beta
#             slope, _, _, _, _ = linregress(combined_df['market'], combined_df['stock'])
#             beta = round(float(slope), 2)
            
#             # Annualized Volatility
#             daily_vol = combined_df['stock'].std()
#             annualized_vol = round(float(daily_vol * np.sqrt(252) * 100), 2)
            
#             portfolio_beta += data.weights[i] * beta
            
#             sector = info.get("sector", "Technology/Services")
#             sector_distribution[sector] = sector_distribution.get(sector, 0.0) + (data.weights[i] * 100)

#             if beta > 1.2:
#                 risk_label = "High Aggressive Risk"
#             elif beta < 0.8:
#                 risk_label = "Low Defensive Risk"
#             else:
#                 risk_label = "Moderate Market Risk"

#             asset_analysis[ticker] = {
#                 "Company Name": info.get("longName", ticker),
#                 "Sector": sector,
#                 "Current Price": f"INR {info.get('currentPrice', info.get('regularMarketPrice', 0.0))}",
#                 "Calculated Beta (β)": beta,
#                 "Annualized Volatility": f"{annualized_vol}%",
#                 "Risk Profile": risk_label,
#                 "Weight Assigned": f"{round(data.weights[i] * 100, 2)}%"
#             }

#         except Exception as e:
#             asset_analysis[ticker] = {"Error": f"Failed to compute metrics: {str(e)}"}

#     concentration_warning = "Safe: Portfolio is well-diversified across sectors."
#     for sector, weight in sector_distribution.items():
#         if weight > 50.0:
#             concentration_warning = f"CRITICAL WARNING: High sector concentration in {sector} ({round(weight, 2)}%). Systemic risk detected!"

#     return {
#         "status": "Success",
#         "client_name": data.user_name,
#         "overall_portfolio_beta": round(portfolio_beta, 2),
#         "sector_concentration_status": concentration_warning,
#         "sector_breakdown": sector_distribution,
#         "individual_assets": asset_analysis
#     }

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import yfinance as yf
# import numpy as np
# import pandas as pd
# from typing import List, Dict

# app = FastAPI(title="Portfolio Risk Analytics API")

# # Hardcoded fallback mapping for fast, reliable sector lookup
# SECTOR_MAP = {
#     "TCS.NS": "Information Technology",
#     "INFY.NS": "Information Technology",
#     "RELIANCE.NS": "Energy",
#     "HDFCBANK.NS": "Financial Services",
#     "ICICIBANK.NS": "Financial Services",
#     "TATAMOTORS.NS": "Automobile"
# }

# class PortfolioInput(BaseModel):
#     tickers: List[str]
#     weights: List[float]
#     benchmark: str = "^NSEI"
#     period: str = "1y"

# def validate_portfolio(weights: List[float]):
#     total_weight = sum(weights)
#     if not np.isclose(total_weight, 1.0, atol=1e-2):
#         raise HTTPException(
#             status_code=400, 
#             detail=f"Sum of portfolio weights must equal 1.0! Current sum: {round(total_weight, 2)}"
#         )

# def calculate_metrics(tickers: List[str], weights: List[float], benchmark: str, period: str):
#     all_tickers = list(set(tickers + [benchmark]))
    
#     # Download data safely handling MultiIndex columns
#     data = yf.download(all_tickers, period=period, progress=False)
    
#     if 'Adj Close' in data:
#         df = data['Adj Close']
#     elif 'Close' in data:
#         df = data['Close']
#     else:
#         raise HTTPException(status_code=400, detail="Failed to fetch price data from Yahoo Finance.")

#     returns = df.pct_change().dropna()
    
#     # Annualized Volatility calculation
#     daily_vol = returns[tickers].std()
#     annualized_vol = daily_vol * np.sqrt(252)
    
#     # OLS Beta calculation relative to Benchmark
#     benchmark_returns = returns[benchmark]
#     betas = {}
    
#     for ticker in tickers:
#         stock_returns = returns[ticker]
#         covariance = np.cov(stock_returns, benchmark_returns)[0][1]
#         market_variance = np.var(benchmark_returns)
#         beta = covariance / market_variance if market_variance != 0 else 1.0
#         betas[ticker] = float(beta)
        
#     return annualized_vol, betas

# def analyze_sector_and_profile(tickers: List[str], weights: List[float], betas: Dict, vols: pd.Series):
#     sector_weights = {}
#     asset_profiles = {}
    
#     for ticker, weight in zip(tickers, weights):
#         # Use fallback dictionary if yfinance info is empty/rate-limited
#         sector = SECTOR_MAP.get(ticker.upper(), "Other Services")
#         sector_weights[sector] = sector_weights.get(sector, 0.0) + weight
        
#         beta = betas[ticker]
#         vol = float(vols[ticker])
        
#         # Risk profiling categorization
#         if beta > 1.2 and vol > 0.25:
#             profile = "High Aggressive"
#         elif beta < 0.8 and vol < 0.15:
#             profile = "Low Defensive"
#         else:
#             profile = "Moderate"
            
#         asset_profiles[ticker] = {
#             "sector": sector, 
#             "profile": profile, 
#             "beta": round(beta, 2), 
#             "volatility": round(vol, 4)
#         }
        
#     # Sector concentration check (>50%)
#     critical_warning = None
#     for sector, sec_weight in sector_weights.items():
#         if sec_weight > 0.50:
#             critical_warning = f"CRITICAL WARNING: Sector '{sector}' accounts for {round(sec_weight*100, 1)}% of allocation (>50% Limit)!"
            
#     return sector_weights, asset_profiles, critical_warning

# @app.post("/analyze_portfolio")
# def analyze_portfolio_endpoint(portfolio: PortfolioInput):
#     validate_portfolio(portfolio.weights)
#     vols, betas = calculate_metrics(portfolio.tickers, portfolio.weights, portfolio.benchmark, portfolio.period)
#     sec_weights, profiles, warning = analyze_sector_and_profile(portfolio.tickers, portfolio.weights, betas, vols)
    
#     return {
#         "asset_profiles": profiles,
#         "sector_distribution": sec_weights,
#         "critical_warning": warning
#     }

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import numpy as np
import pandas as pd
from typing import List, Dict

app = FastAPI(title="Portfolio Risk Analytics API")

SECTOR_MAP = {
    "TCS.NS": "Information Technology",
    "INFY.NS": "Information Technology",
    "RELIANCE.NS": "Energy",
    "HDFCBANK.NS": "Financial Services",
    "ICICIBANK.NS": "Financial Services",
    "TATAMOTORS.NS": "Automobile",
    "TATASTEEL.NS": "Basic Materials"
}

class PortfolioInput(BaseModel):
    tickers: List[str]
    weights: List[float]
    benchmark: str = "^NSEI"
    period: str = "1y"

def validate_portfolio(weights: List[float]):
    total_weight = sum(weights)
    if not np.isclose(total_weight, 1.0, atol=1e-2):
        raise HTTPException(
            status_code=400, 
            detail=f"Sum of portfolio weights must equal 1.0! Current sum: {round(total_weight, 2)}"
        )

def calculate_metrics(tickers: List[str], weights: List[float], benchmark: str, period: str):
    all_tickers = list(set(tickers + [benchmark]))
    data = yf.download(all_tickers, period=period, progress=False)
    
    if 'Adj Close' in data:
        df = data['Adj Close']
    elif 'Close' in data:
        df = data['Close']
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch market data.")

    returns = df.pct_change().dropna()
    daily_vol = returns[tickers].std()
    annualized_vol = daily_vol * np.sqrt(252)
    
    benchmark_returns = returns[benchmark]
    betas = {}
    
    for ticker in tickers:
        stock_returns = returns[ticker]
        covariance = np.cov(stock_returns, benchmark_returns)[0][1]
        market_variance = np.var(benchmark_returns)
        beta = covariance / market_variance if market_variance != 0 else 1.0
        betas[ticker] = float(beta)
        
    return annualized_vol, betas

def analyze_sector_and_profile(tickers: List[str], weights: List[float], betas: Dict, vols: pd.Series):
    sector_weights = {}
    asset_profiles = {}
    
    for ticker, weight in zip(tickers, weights):
        sector = SECTOR_MAP.get(ticker.upper(), "Other Services")
        sector_weights[sector] = sector_weights.get(sector, 0.0) + weight
        
        beta = betas[ticker]
        vol = float(vols[ticker])
        
        if beta > 1.2 and vol > 0.25:
            profile = "High Aggressive"
        elif beta < 0.8 and vol < 0.15:
            profile = "Low Defensive"
        else:
            profile = "Moderate"
            
        asset_profiles[ticker] = {
            "sector": sector, 
            "profile": profile, 
            "beta": round(beta, 2), 
            "volatility": round(vol, 4)
        }
        
    critical_warning = None
    for sector, sec_weight in sector_weights.items():
        if sec_weight > 0.50:
            critical_warning = f"CRITICAL WARNING: Sector '{sector}' accounts for {round(sec_weight*100, 1)}% of allocation (>50% Limit)!"
            
    return sector_weights, asset_profiles, critical_warning

@app.post("/analyze_portfolio")
def analyze_portfolio_endpoint(portfolio: PortfolioInput):
    validate_portfolio(portfolio.weights)
    vols, betas = calculate_metrics(portfolio.tickers, portfolio.weights, portfolio.benchmark, portfolio.period)
    sec_weights, profiles, warning = analyze_sector_and_profile(portfolio.tickers, portfolio.weights, betas, vols)
    
    return {
        "asset_profiles": profiles,
        "sector_distribution": sec_weights,
        "critical_warning": warning
    }