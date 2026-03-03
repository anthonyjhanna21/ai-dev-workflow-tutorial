# Implementation Plan: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-sales-dashboard/spec.md`

## Summary

Build a single-file Streamlit web dashboard that reads `data/sales-data.csv` and displays:
two KPI metric cards (Total Sales, Total Orders), a daily sales trend line chart, and two
side-by-side bar charts (sales by category and sales by region). All logic lives in `app.py`.
The deployed dashboard is publicly accessible via Streamlit Community Cloud.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit (latest stable), Plotly Express (latest stable),
Pandas (latest stable)
**Storage**: CSV file — `data/sales-data.csv` (read-only; no writes)
**Testing**: None — no testing framework required for Phase 1 (Constitution Principle I)
**Target Platform**: Web browser; local via `streamlit run app.py`; deployed via Streamlit
Community Cloud
**Project Type**: Single-file web dashboard
**Performance Goals**: Full page usable within 5 seconds (SC-002); charts render within 2
seconds of data load (PRD NFR-1)
**Constraints**: All logic in `app.py` (Principle V); no Phase 2 features (Principle II);
colorblind-safe palettes (Principle III); no data validation (Principle IV)
**Scale/Scope**: ~482 transaction rows; 4 charts; 2 KPIs; 1 developer; public deployment

## Constitution Check

*GATE: Must pass before implementation. Re-checked after design phase.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Simplicity First | `st.metric()` + `px.line()` + `px.bar()` — simplest viable APIs; no custom abstractions | ✅ PASS |
| II. Phase 1 Scope Lock | Only FR-001 through FR-011 implemented; no Phase 2 features scaffolded or hinted | ✅ PASS |
| III. Accessibility by Default | `px.colors.qualitative.Safe` palette on bar charts; descriptive axis labels on all charts; `use_container_width=True` for responsive sizing | ✅ PASS |
| IV. Data Trust | `pd.read_csv()` called directly; no try/except, no schema validation, no type coercion guards | ✅ PASS |
| V. Single-File Deployment | All logic in `app.py`; only supporting files are `requirements.txt` and `data/sales-data.csv` | ✅ PASS |

**Result**: All gates pass. No complexity violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-sales-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 — technology decisions and API patterns
├── data-model.md        # Phase 1 — entity definitions and data flow
├── quickstart.md        # Phase 1 — local setup and verification steps
├── contracts/
│   └── csv-schema.md    # Phase 1 — CSV input contract
├── checklists/
│   └── requirements.md  # Spec quality validation checklist
└── tasks.md             # Phase 2 output (/speckit.tasks — not yet created)
```

### Source Code (repository root)

```text
app.py                   # All application logic (Streamlit entry point)
requirements.txt         # Runtime dependencies (streamlit, plotly, pandas)
data/
└── sales-data.csv       # Sales transaction data (read-only input)
```

**Structure Decision**: Single-file layout per Constitution Principle V. No `src/`, `lib/`,
or helper module files. All Pandas aggregations and Plotly/Streamlit rendering live in `app.py`.
Helper functions within `app.py` are permitted to reduce repetition.

## Implementation Approach

### Data Loading (shared foundation)

```python
df = pd.read_csv('data/sales-data.csv', parse_dates=['date'])
```

No validation. If the file is missing or malformed, Streamlit displays a native error.

### KPI Computation

```python
total_sales = df['total_amount'].sum()
total_orders = len(df)
```

### Aggregations

```python
# Daily trend
df_daily = df.resample('D', on='date')['total_amount'].sum().reset_index()

# Category breakdown (sorted descending)
df_category = (df.groupby('category')['total_amount']
                 .sum()
                 .reset_index()
                 .sort_values('total_amount', ascending=False))

# Region breakdown (sorted descending)
df_region = (df.groupby('region')['total_amount']
               .sum()
               .reset_index()
               .sort_values('total_amount', ascending=False))
```

### Dashboard Layout

```text
┌─────────────────────────────────────────────────────────────┐
│  st.title("ShopSmart Sales Dashboard")                      │
├────────────────────────┬────────────────────────────────────┤
│  st.metric             │  st.metric                         │
│  "Total Sales"         │  "Total Orders"                    │
│  $678,450              │  482                               │
├─────────────────────────────────────────────────────────────┤
│  st.plotly_chart(fig_trend)  [full width]                   │
│  px.line — daily sales, 12-month range                      │
├────────────────────────┬────────────────────────────────────┤
│  st.plotly_chart       │  st.plotly_chart                   │
│  px.bar — by category  │  px.bar — by region                │
│  [use_container_width] │  [use_container_width]             │
└────────────────────────┴────────────────────────────────────┘
```

### Chart Specifications

| Chart | Type | X-axis | Y-axis | Sort | Color |
|-------|------|--------|--------|------|-------|
| Sales Trend | `px.line` | `date` (daily) | `total_amount` | Ascending date | Single neutral |
| By Category | `px.bar` | `category` | `total_amount` | Descending value | `px.colors.qualitative.Safe` |
| By Region | `px.bar` | `region` | `total_amount` | Descending value | `px.colors.qualitative.Safe` |

### Streamlit Layout Pattern

```python
# KPI cards
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")

# Trend chart (full width)
st.plotly_chart(fig_trend, use_container_width=True)

# Side-by-side bar charts
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_category, use_container_width=True)
with col2:
    st.plotly_chart(fig_region, use_container_width=True)
```

## Deployment

- **Local**: `streamlit run app.py` (after `pip install -r requirements.txt`)
- **Production**: Streamlit Community Cloud — repo: student's GitHub fork, branch: `main`,
  file: `app.py`
- **Data**: `data/sales-data.csv` must be committed to the repository (not `.gitignore`d)

## Post-Design Constitution Check

Re-evaluated after Phase 1 design:

| Principle | Post-Design Validation | Status |
|-----------|----------------------|--------|
| I. Simplicity First | No new abstractions introduced in design phase | ✅ PASS |
| II. Phase 1 Scope Lock | No Phase 2 patterns introduced in data model or contracts | ✅ PASS |
| III. Accessibility by Default | `Safe` palette, labeled axes, and `use_container_width` confirmed in all chart specs | ✅ PASS |
| IV. Data Trust | No validation logic appears in data flow diagram or aggregation patterns | ✅ PASS |
| V. Single-File Deployment | Project structure confirms `app.py` is the sole source file | ✅ PASS |
