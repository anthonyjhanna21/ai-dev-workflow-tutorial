# Quickstart: ShopSmart Sales Analytics Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-03

## Prerequisites

- Python 3.11 or higher installed
- `data/sales-data.csv` present at the repository root

## Local Setup

### 1. Create and activate a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`.

## Expected `requirements.txt`

```
streamlit
plotly
pandas
```

## Verification Checklist

After running `streamlit run app.py`, confirm:

- [ ] Page loads without errors in the terminal
- [ ] Two KPI cards visible: "Total Sales" (~$678,450) and "Total Orders" (482)
- [ ] Line chart shows a 12-month daily sales trend
- [ ] Two bar charts appear side by side: "Sales by Category" and "Sales by Region"
- [ ] Each bar chart shows bars sorted from highest to lowest
- [ ] Hovering over any chart element shows a tooltip with exact values

## Stop the Dashboard

Press `Ctrl+C` in the terminal to stop the Streamlit server.

## Deployment to Streamlit Community Cloud

1. Push `app.py` and `requirements.txt` to the `main` branch of your GitHub fork
2. Log in to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo, branch `main`, file `app.py`
4. Click **Deploy** — your public URL will be generated automatically

> **Note**: `data/sales-data.csv` must also be committed to the repository for the deployed
> app to load data correctly.
