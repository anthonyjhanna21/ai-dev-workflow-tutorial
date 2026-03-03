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

# --- Sales Trend Line Chart (US2) ---
fig_trend = px.line(df_daily, x="date", y="total_amount", title="Sales Trend", labels={"date": "Date", "total_amount": "Sales ($)"})
st.plotly_chart(fig_trend, use_container_width=True)

# --- Sales by Category Bar Chart (US3) ---
fig_category = px.bar(df_category, x="category", y="total_amount", title="Sales by Category", labels={"category": "Category", "total_amount": "Sales ($)"}, color="category", color_discrete_sequence=px.colors.qualitative.Safe)

# --- Sales by Region Bar Chart (US4) ---
fig_region = px.bar(df_region, x="region", y="total_amount", title="Sales by Region", labels={"region": "Region", "total_amount": "Sales ($)"}, color="region", color_discrete_sequence=px.colors.qualitative.Safe)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_category, use_container_width=True)
with col2:
    st.plotly_chart(fig_region, use_container_width=True)
