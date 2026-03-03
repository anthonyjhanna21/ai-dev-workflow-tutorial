# Research: ShopSmart Sales Analytics Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-03
**Status**: Complete — all NEEDS CLARIFICATION resolved

## Technology Stack Decisions

### Language & Runtime

- **Decision**: Python 3.11+
- **Rationale**: Mandated by PRD and Constitution Tech Stack Constraints. Required by Streamlit.
- **Alternatives considered**: N/A — mandated

### Dashboard Framework

- **Decision**: Streamlit (latest stable)
- **Rationale**: Mandated by PRD. Converts Python functions into interactive web pages with no
  frontend code. Native `st.metric()` and `st.columns()` cover all Phase 1 layout needs.
- **Alternatives considered**: N/A — mandated

### Visualization Library

- **Decision**: Plotly Express (`plotly.express`) — subset of Plotly, latest stable
- **Rationale**: Mandated by PRD. `px.line()` and `px.bar()` are the simplest APIs for trend and
  bar charts. No raw `go.Figure()` construction needed for Phase 1.
- **Alternatives considered**: `plotly.graph_objects` — more control but unnecessary complexity;
  violates Constitution Principle I (Simplicity First)

### Data Processing

- **Decision**: Pandas (latest stable)
- **Rationale**: Mandated by PRD. `pd.read_csv()` for loading; `groupby().sum()` for category
  and region aggregations; `resample('D').sum()` for daily time series.
- **Alternatives considered**: N/A — mandated

### Dependency Management

- **Decision**: `pip` + `venv` with `requirements.txt`
- **Rationale**: User selected. Standard Python tooling; universally supported; minimal onboarding
  instructions needed for workshop participants.
- **Alternatives considered**: `uv` — faster resolver but requires separate install; less
  beginner-friendly

### KPI Display

- **Decision**: `st.metric()` inside `st.columns(2)`
- **Rationale**: User selected. Built-in Streamlit widget renders a labeled value in a professional
  card format with zero custom CSS. The `delta` parameter is left unused — no comparison period in
  Phase 1 scope.
- **Alternatives considered**: Custom markdown strings — same visual result but more code;
  violates Constitution Principle I

### Sales Trend Chart

- **Decision**: `px.line()` with `x='date'`, `y='total_amount'` on daily-aggregated data
- **Rationale**: Line chart is explicitly required by PRD FR-2. Daily granularity selected by user.
  Pandas `resample('D').sum()` produces the daily totals series.
- **Alternatives considered**: `px.area()` — fills under line; same data but adds visual weight
  without additional information

### Category & Region Bar Charts

- **Decision**: `px.bar()` vertical orientation; `x=category/region`, `y=total_amount`;
  data pre-sorted descending before charting
- **Rationale**: User selected vertical bars. `sort_values('total_amount', ascending=False)` before
  `px.bar()` satisfies PRD FR-004/FR-005 (sorted highest to lowest).
- **Alternatives considered**: `orientation='h'` (horizontal) — better for long labels but user
  chose vertical

### Chart Layout (Category + Region)

- **Decision**: `st.columns(2)` with one chart per column; `use_container_width=True` on each
- **Rationale**: User selected side-by-side layout. `st.columns(2)` is the standard Streamlit
  two-column pattern; no custom CSS required. `use_container_width=True` ensures charts fill
  their column responsively.
- **Alternatives considered**: Sequential vertical layout — more scrolling; explicitly rejected

### Color Palette

- **Decision**: `px.colors.qualitative.Safe` (Plotly's colorblind-safe qualitative palette)
- **Rationale**: Constitution Principle III mandates colorblind-safe palettes. `Safe` is
  documented by Plotly as designed for accessibility. Applied via `color_discrete_sequence` on
  bar charts. The trend line chart uses a single neutral color (no multi-color encoding needed).
- **Alternatives considered**: `px.colors.qualitative.Plotly` (default) — not verified
  colorblind-safe; `px.colors.qualitative.Colorblind` — also valid but `Safe` is more broadly
  referenced in accessibility contexts

### Single-File Architecture

- **Decision**: All application logic in `app.py` at repository root; helper functions within
  the same file are permitted to reduce repetition
- **Rationale**: Constitution Principle V mandates single-file deployment. `streamlit run app.py`
  is the complete and only start command.
- **Alternatives considered**: Module-based structure — explicitly prohibited by Principle V

## Key API Patterns

### Data Loading & Aggregation

```python
import pandas as pd

df = pd.read_csv('data/sales-data.csv', parse_dates=['date'])

# KPIs
total_sales = df['total_amount'].sum()
total_orders = len(df)

# Daily trend
df_daily = df.resample('D', on='date')['total_amount'].sum().reset_index()

# Category breakdown (sorted)
df_category = df.groupby('category')['total_amount'].sum().reset_index()
df_category = df_category.sort_values('total_amount', ascending=False)

# Region breakdown (sorted)
df_region = df.groupby('region')['total_amount'].sum().reset_index()
df_region = df_region.sort_values('total_amount', ascending=False)
```

### KPI Cards

```python
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
```

### Chart Construction

```python
import plotly.express as px

# Trend line chart
fig_trend = px.line(
    df_daily, x='date', y='total_amount',
    title='Sales Trend',
    labels={'date': 'Date', 'total_amount': 'Sales ($)'}
)

# Category bar chart
fig_category = px.bar(
    df_category, x='category', y='total_amount',
    title='Sales by Category',
    labels={'category': 'Category', 'total_amount': 'Sales ($)'},
    color='category',
    color_discrete_sequence=px.colors.qualitative.Safe
)

# Region bar chart
fig_region = px.bar(
    df_region, x='region', y='total_amount',
    title='Sales by Region',
    labels={'region': 'Region', 'total_amount': 'Sales ($)'},
    color='region',
    color_discrete_sequence=px.colors.qualitative.Safe
)
```

### Side-by-Side Chart Layout

```python
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_category, use_container_width=True)
with col2:
    st.plotly_chart(fig_region, use_container_width=True)
```
