# Contract: CSV Input Schema

**Feature**: 001-sales-dashboard
**Date**: 2026-03-03
**Type**: Data input contract (read-only)
**File**: `data/sales-data.csv`

## Purpose

This document defines the expected structure of the CSV data file that the dashboard reads on
startup. It is the sole external interface contract for this project — there are no APIs,
webhooks, or user-provided inputs.

## Schema

| Column         | Type    | Format                  | Required | Notes                          |
|----------------|---------|-------------------------|----------|--------------------------------|
| `date`         | Date    | `YYYY-MM-DD`            | Yes      | Parseable by Pandas `parse_dates` |
| `order_id`     | String  | `ORD-XXXXXX`            | Yes      | Not used in aggregations       |
| `product`      | String  | Free text               | Yes      | Not used in aggregations       |
| `category`     | String  | One of 5 known values   | Yes      | Used for category bar chart    |
| `region`       | String  | One of 4 known values   | Yes      | Used for regional bar chart    |
| `quantity`     | Integer | Positive integer        | Yes      | Not used in aggregations       |
| `unit_price`   | Decimal | Positive decimal        | Yes      | Not used in aggregations       |
| `total_amount` | Decimal | Positive decimal        | Yes      | Primary aggregation field      |

## Allowed Values

### `category` (must be one of):
- `Electronics`
- `Audio`
- `Wearables`
- `Smart Home`
- `Accessories`

### `region` (must be one of):
- `North`
- `South`
- `East`
- `West`

## Example Row

```csv
date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-15,ORD-001234,Wireless Headphones,Audio,North,2,49.99,99.98
```

## Contract Guarantees

The dashboard **assumes** (does not validate) that:

1. The file exists at `data/sales-data.csv` relative to the working directory
2. The header row matches the column names above exactly
3. All rows contain non-null values for `date` and `total_amount`
4. The `date` column contains valid dates parseable by Pandas
5. The `total_amount` column contains positive numeric values

Violation of any guarantee results in a native Streamlit/Pandas error (per Constitution
Principle IV: Data Trust).

## Notes

- Columns `order_id`, `product`, `quantity`, and `unit_price` are present in the file but
  are not used by any Phase 1 aggregation. They are loaded with the full DataFrame and
  ignored thereafter.
- No output contracts exist — the dashboard renders directly in the browser via Streamlit
  and produces no data artifacts.
