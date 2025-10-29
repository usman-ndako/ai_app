# Day 34 — AI Financial Analyzer

Lightweight Streamlit app for uploading financial data, generating KPIs, visual analytics, Prophet forecasts, and AI-driven executive summaries (Groq).

## Files
- app.py — Main Streamlit application (upload data, run AI analysis, forecasting).
- requirements.txt — Python dependencies.
- executive_summary.txt — Example executive summary output.
- financial_summary.txt — Example textual report.

## Features
- Automatic detection of date and revenue/amount columns.
- KPI cards, daily aggregation, and Plotly visualizations.
- Prophet-based forecasting with confidence intervals.
- Optional Groq AI integration for executive summaries (requires API key).
- Exportable reports (TXT/CSV/JSON).

## Quick start (Windows)
1. Create and activate virtual environment:
    .venv\Scripts\activate
2. Install dependencies:
    pip install -r requirements.txt
3. Run the app:
    streamlit run app.py

## Usage
- Upload a CSV or XLSX containing a date column and a numeric revenue/sales column.
- Enter your Groq API key in the sidebar to enable AI insights (https://console.groq.com).
- For reliable forecasting, provide >= 14 days of historical data.

## Troubleshooting
- "Critical columns missing": ensure recognizable date and amount column names (e.g., date, sales, revenue, amount).
- Prophet errors: remove NaNs and ensure `ds` (date) and `y` (value) columns exist.
- API errors: verify Groq key and network access.

## Notes
- This repository is demo/educational code. Adapt and secure API keys and data handling for production.
- Modify app.py to customize column detection, visuals, or model configuration.

## License
Refer to your project license. This folder contains sample/demo code.