# Data Model: ShopSmart Sales Analytics Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-03
**Source**: `data/sales-data.csv` (read-only; no writes performed)

## Entities

### Transaction (raw source data)

Represents a single sales order. This is the base entity from which all aggregations are derived.

| Field          | Type    | Description                          | Example            |
|----------------|---------|--------------------------------------|--------------------|
| `date`         | Date    | Transaction date (parsed from string)| 2024-01-15         |
| `order_id`     | String  | Unique order identifier              | ORD-001234         |
| `product`      | String  | Product name                         | Wireless Headphones|
| `category`     | String  | Product category (5 values)          | Electronics        |
| `region`       | String  | Geographic region (4 values)         | North              |
| `quantity`     | Integer | Units sold in this order             | 2                  |
| `unit_price`   | Decimal | Price per unit                       | 49.99              |
| `total_amount` | Decimal | Total transaction value (qty × price)| 99.98              |

**Volume**: ~482 rows, 12 months of history
**Used by**: All derived entities below

---

### KPI (computed at load time)

Two scalar values derived from all transactions. Displayed as metric cards.

| Field          | Type    | Derivation                    | Display Format  |
|----------------|---------|-------------------------------|-----------------|
| `total_sales`  | Float   | `SUM(total_amount)` over all rows | `$678,450`  |
| `total_orders` | Integer | `COUNT(*)` of all rows        | `482`           |

**No state transitions** — computed once on startup, displayed as static values.

---

### DailySales (aggregated series for trend chart)

One row per calendar date. Used as the data series for the line chart.

| Field          | Type  | Derivation                                  |
|----------------|-------|---------------------------------------------|
| `date`         | Date  | Calendar date (daily granularity)           |
| `total_amount` | Float | `SUM(total_amount)` for all transactions on that date |

**Sort order**: Ascending by `date` (natural time series order)
**Zero-sales days**: Appear as `0.0` data points to maintain a continuous line

---

### CategorySales (aggregated for category bar chart)

One row per product category. Used as the data series for the category bar chart.

| Field          | Type   | Derivation                                         |
|----------------|--------|----------------------------------------------------|
| `category`     | String | Product category name (one of 5 known values)      |
| `total_amount` | Float  | `SUM(total_amount)` for all transactions in category|

**Sort order**: Descending by `total_amount`; alphabetical tiebreaker
**Cardinality**: Always 5 rows (Electronics, Audio, Wearables, Smart Home, Accessories)

---

### RegionSales (aggregated for region bar chart)

One row per geographic region. Used as the data series for the regional bar chart.

| Field          | Type   | Derivation                                        |
|----------------|--------|---------------------------------------------------|
| `region`       | String | Region name (one of 4 known values)               |
| `total_amount` | Float  | `SUM(total_amount)` for all transactions in region|

**Sort order**: Descending by `total_amount`; alphabetical tiebreaker
**Cardinality**: Always 4 rows (North, South, East, West)

---

## Data Flow

```text
data/sales-data.csv
       │
       ▼
  pd.read_csv()
  (parse_dates=['date'])
       │
       ├──► KPI: .sum() / len()             → st.metric() cards
       │
       ├──► DailySales: .resample('D').sum() → px.line() trend chart
       │
       ├──► CategorySales: .groupby().sum()  → px.bar() category chart
       │
       └──► RegionSales: .groupby().sum()    → px.bar() region chart
```

## Validation Rules

Per Constitution Principle IV (Data Trust), no runtime schema validation is performed.
The following rules are assumed to be satisfied by the source file:

- `date` column is parseable by Pandas `parse_dates`
- `total_amount` column contains non-null numeric values
- `category` column contains only the 5 known category names
- `region` column contains only the 4 known region names
- No duplicate `order_id` values (not validated; not used in aggregations)
