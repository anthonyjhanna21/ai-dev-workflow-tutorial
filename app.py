import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

# Load data
df = pd.read_csv("data/sales-data.csv", parse_dates=["date"])

# KPI metrics
total_sales = df["total_amount"].sum()
total_orders = len(df)

# Daily sales trend (one row per calendar day)
df_daily = df.resample("D", on="date")["total_amount"].sum().reset_index()

# Category breakdown (sorted highest to lowest)
df_category = (
    df.groupby("category")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

# Region breakdown (sorted highest to lowest)
df_region = (
    df.groupby("region")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

# --- KPI Cards (US1) ---
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
