# 🏥 Portfolio Risk Analytics & Health Engine

A decoupled, microservice-based FinTech application designed for real-time portfolio risk assessment, financial health metrics computation, and sector concentration auditing.

---

## 📌 Project Overview
The **Portfolio Risk Analytics & Health Engine** evaluates multi-asset portfolio exposure relative to market benchmark data (`^NSEI` - Nifty 50). It leverages statistical linear regression to assess systematic risk ($\beta$) and standard deviation modeling for annualized volatility ($\sigma$), automatically triggering cluster risk alerts when sector allocations exceed conservative thresholds (>50%).

---

## 🏗️ System Architecture
The application follows a clean **Decoupled Microservice Architecture**:
* **Backend Service (FastAPI):** Exposes high-performance RESTful APIs to calculate financial parameters ($\beta$, $\sigma$), parse ticker metrics, and execute portfolio health validation logic.
* **Frontend Dashboard (Streamlit):** Serves as an interactive web interface featuring input parameter forms, preset shortcuts, asset profiling dataframes, and dynamic Plotly visual charts.

## ✨ Key Features
* **Dynamic Multi-Asset Parsing:** Supports unlimited assets via comma-separated inputs with string-parsing validation.
* **Systematic Risk Modeling ($\beta$):** Computes asset Beta via Ordinary Least Squares (OLS) covariance against benchmark returns:
  $$\beta_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$$
* **Annualized Volatility Calculation ($\sigma$):** Scales standard deviation across 252 trading days:
  $$\sigma_{\text{annual}} = \sigma_{\text{daily}} \times \sqrt{252}$$
* **Cluster Risk Audit Guardrail:** Monitors allocation concentrations and triggers visual critical warnings if any sector exceeds 50% total portfolio weight.
* **CSV Export:** One-click functionality to download full audited risk profiles.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Frontend:** Streamlit, Plotly Express
* **Data Processing & Analytics:** Pandas, NumPy, YFinance

---

## 🚀 How to Run Locally

### 1. Install Dependencies

```bash

pip install -r requirements.txt

```

### 2. Start Backend API (Terminal 1)

```bash

uvicorn main:app --reload

```

- API Base: `http://127.0.0.1:8000`

- Interactive Docs: `http://127.0.0.1:8000/docs`


### 3. Start Frontend Dashboard (Terminal 2)

```bash

streamlit run app.py

```

- Web Application: `http://localhost:8501`

---

## 👤 Author

- **Course/Project ID:** TDDS037A

- **Developer:** Samiksha Kanade
