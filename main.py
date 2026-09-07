from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List

app = FastAPI(title="Portfolio Risk Analytics Engine")

class PortfolioInput(BaseModel):
    tickers: List[str]
    weights: List[float]

@app.post("/analyze_portfolio")
def analyze_portfolio(portfolio: PortfolioInput):
    # Weight Sum Validation Guardrail
    if not np.isclose(sum(portfolio.weights), 1.0, atol=1e-2):
        raise HTTPException(status_code=400, detail="Portfolio weights must sum up to 1.0")

    tickers = [t.strip().upper() for t in portfolio.tickers]
    benchmark = "^NSEI"
    all_tickers = list(set(tickers + [benchmark]))

    try:
        # Live market data download
        df = yf.download(all_tickers, period="1y", auto_adjust=True)
        
        # Pandas MultiIndex Fix (Resolves the KeyError)
        if isinstance(df.columns, pd.MultiIndex):
            data = df["Close"]
        else:
            data = df["Close"] if "Close" in df else df
            
        returns = data.pct_change().dropna()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market API connection failed: {str(e)}")

    if benchmark not in returns.columns:
        raise HTTPException(status_code=500, detail="Benchmark market data unavailable.")

    market_returns = returns[benchmark]
    market_variance = np.var(market_returns)

    asset_profiles = {}
    sector_weights = {}

    for ticker, weight in zip(tickers, portfolio.weights):
        if ticker not in returns.columns:
            raise HTTPException(status_code=400, detail=f"Invalid or untraded ticker: {ticker}")

        # Live Dynamic Sector Fetching directly from Yahoo Finance API
        try:
            live_ticker_info = yf.Ticker(ticker).info
            sector = live_ticker_info.get("sector", "Diversified / General")
        except Exception:
            sector = "Diversified / General"

        stock_returns = returns[ticker]
        covariance = np.cov(stock_returns, market_returns)[0][1]
        
        # Zero-Variance Guardrail
        beta = float(covariance / market_variance) if market_variance != 0 else 1.0
        volatility = float(np.std(stock_returns) * np.sqrt(252))

        asset_profiles[ticker] = {
            "Beta": round(beta, 2),
            "Annualized Volatility": f"{round(volatility * 100, 2)}%",
            "Sector": sector
        }

        sector_weights[sector] = sector_weights.get(sector, 0.0) + weight

    # Cluster Risk Guardrail (> 50%)
    critical_warning = None
    for sector, sec_weight in sector_weights.items():
        if sec_weight > 0.50:
            critical_warning = f"⚠️ CRITICAL RISK WARNING: High Concentration in {sector} ({sec_weight*100:.1f}%)"

    return {
        "asset_profiles": asset_profiles,
        "sector_distribution": sector_weights,
        "critical_warning": critical_warning
    }