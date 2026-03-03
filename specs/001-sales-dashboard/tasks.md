---

description: "Task list for ShopSmart Sales Analytics Dashboard"
---

# Tasks: ShopSmart Sales Analytics Dashboard

**Input**: Design documents from `/specs/001-sales-dashboard/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: No test tasks — not requested in specification (Constitution Principle I: Simplicity First)

**Organization**: Tasks are grouped by user story to enable independent implementation and
testing of each story. All code lives in `app.py` (Constitution Principle V).

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (logically independent, different concerns)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in all descriptions

## Path Conventions

- Single file: `app.py` at repository root
- Data: `data/sales-data.csv` (read-only)
- Dependencies: `requirements.txt` at repository root

---

## Phase 1: Setup

**Purpose**: Project initialization — create the two files needed to run the app

- [x] T001 Create `app.py` at repository root with `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` and `st.title("ShopSmart Sales Dashboard")`
- [x] T002 [P] Create `requirements.txt` at repository root containing three lines: `streamlit`, `plotly`, `pandas`

---

## Phase 2: Foundational (Blocking Prerequisite)

**Purpose**: Load and aggregate all data — MUST complete before any user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete. All four aggregations
are computed here and used by US1–US4.

- [x] T003 Add data loading and all aggregations to `app.py`: `pd.read_csv('data/sales-data.csv', parse_dates=['date'])`, then compute `total_sales = df['total_amount'].sum()`, `total_orders = len(df)`, `df_daily` (resample daily), `df_category` (groupby category, sort descending), `df_region` (groupby region, sort descending)

**Checkpoint**: Foundation ready — run `streamlit run app.py` and confirm no errors before proceeding

---

## Phase 3: User Story 1 - KPI Metrics at a Glance (Priority: P1) 🎯 MVP

**Goal**: Display Total Sales and Total Orders as metric cards visible without scrolling

**Independent Test**: Open the dashboard. Two metric cards appear at the top: "Total Sales"
showing a dollar-formatted value (~$678,450) and "Total Orders" showing an integer count (482).
Both values match manual calculations from the CSV.

- [x] T004 [US1] Render KPI cards in `app.py`: create `col1, col2 = st.columns(2)`, then `col1.metric("Total Sales", f"${total_sales:,.0f}")` and `col2.metric("Total Orders", f"{total_orders:,}")`

**Checkpoint**: US1 complete — `streamlit run app.py` shows two correctly formatted metric cards ✅

---

## Phase 4: User Story 2 - Sales Trend Over Time (Priority: P2)

**Goal**: Display a daily sales line chart showing the full 12-month trend

**Independent Test**: Below the KPI cards, a line chart appears with dates on the X-axis and
sales amounts on the Y-axis. Each data point represents one calendar day. Hovering shows the
exact date and dollar value.

- [ ] T005 [US2] Build trend figure in `app.py`: `fig_trend = px.line(df_daily, x='date', y='total_amount', title='Sales Trend', labels={'date': 'Date', 'total_amount': 'Sales ($)'})`
- [ ] T006 [US2] Add trend chart to `app.py` layout below KPI cards: `st.plotly_chart(fig_trend, use_container_width=True)`

**Checkpoint**: US2 complete — trend chart visible below KPI cards with interactive tooltips ✅

---

## Phase 5: User Story 3 - Sales by Product Category (Priority: P3)

**Goal**: Display a vertical bar chart of sales by category, sorted highest to lowest,
using a colorblind-safe palette

**Independent Test**: A bar chart with 5 bars appears in the left half of the page. Bars are
sorted from highest to lowest sales. Each bar has a distinct colorblind-safe color. Hovering
shows the category name and exact sales total.

- [ ] T007 [US3] Build category figure in `app.py`: `fig_category = px.bar(df_category, x='category', y='total_amount', title='Sales by Category', labels={'category': 'Category', 'total_amount': 'Sales ($)'}, color='category', color_discrete_sequence=px.colors.qualitative.Safe)`
- [ ] T008 [US3] Create two-column layout in `app.py` and add category chart to left column: `col1, col2 = st.columns(2)` then `with col1: st.plotly_chart(fig_category, use_container_width=True)`

**Checkpoint**: US3 complete — category bar chart visible in left column with 5 sorted bars ✅

---

## Phase 6: User Story 4 - Sales by Geographic Region (Priority: P4)

**Goal**: Display a vertical bar chart of sales by region, sorted highest to lowest,
side by side with the category chart

**Independent Test**: A bar chart with 4 bars appears in the right column, alongside the
category chart. Both charts are visible simultaneously without scrolling. Hovering over
any bar shows the region name and exact sales total.

- [ ] T009 [P] [US4] Build region figure in `app.py`: `fig_region = px.bar(df_region, x='region', y='total_amount', title='Sales by Region', labels={'region': 'Region', 'total_amount': 'Sales ($)'}, color='region', color_discrete_sequence=px.colors.qualitative.Safe)`
- [ ] T010 [US4] Add region chart to right column of the existing `st.columns(2)` block in `app.py`: `with col2: st.plotly_chart(fig_region, use_container_width=True)`

**Checkpoint**: US4 complete — region bar chart visible in right column alongside category chart ✅

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Accessibility audit, layout polish, and deployment verification

- [ ] T011 [P] Review and polish page layout in `app.py`: confirm `st.title()` is present and readable, add `st.markdown("---")` dividers between sections if needed, verify overall visual hierarchy matches PRD layout spec (KPIs → trend → side-by-side charts)
- [ ] T012 [P] Audit all three chart figures in `app.py` for Constitution Principle III compliance: verify each `px.bar()`/`px.line()` call has descriptive `labels={}` dict, `title=` argument, and `px.colors.qualitative.Safe` on bar charts (no color-only encoding of meaning)
- [ ] T013 Run through `specs/001-sales-dashboard/quickstart.md` verification checklist end-to-end against the running `app.py`: confirm all 6 checklist items pass (KPI values, trend chart, category chart, region chart, tooltips, no terminal errors)
- [ ] T014 Deploy to Streamlit Community Cloud: push `app.py`, `requirements.txt`, and `data/sales-data.csv` to `main` branch, create new app at share.streamlit.io pointing to `app.py`, verify public URL loads within 5 seconds (SC-002), share URL with stakeholder

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001 must exist before T003 can be written)
- **US1 (Phase 3)**: Depends on Foundational — BLOCKS on T003
- **US2 (Phase 4)**: Depends on Foundational — can start after T003; independent of US1
- **US3 (Phase 5)**: Depends on Foundational — can start after T003; independent of US1, US2
- **US4 (Phase 6)**: Depends on US3 (T008 creates the `st.columns(2)` that T010 uses)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

- **US1 (P1)**: T003 → T004
- **US2 (P2)**: T003 → T005 → T006
- **US3 (P3)**: T003 → T007 → T008
- **US4 (P4)**: T003 → T007 → T008 → T009 → T010 *(T010 writes into the columns created by T008)*

### Within Each User Story

- Compute task (figure creation) before render task (st.plotly_chart)
- Story complete and checkpointed before moving to next priority

### Parallel Opportunities

- T001 and T002 (Setup): Different files — run in parallel
- T007 and T009 (figure creation): Independent px.bar() calls — run in parallel
- T011 and T012 (Polish): Different concerns — run in parallel

---

## Parallel Example: Setup Phase

```bash
# Both can be done simultaneously:
Task T001: "Create app.py with st.set_page_config() and st.title()"
Task T002: "Create requirements.txt with streamlit, plotly, pandas"
```

## Parallel Example: Chart Figure Creation

```bash
# T007 and T009 create independent figure objects — no dependency:
Task T007: "Build category bar chart figure with px.bar() and Safe palette"
Task T009: "Build region bar chart figure with px.bar() and Safe palette"
# Then T008 and T010 must run sequentially (share same st.columns block)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001, T002)
2. Complete Phase 2: Foundational (T003) — critical blocker
3. Complete Phase 3: US1 (T004)
4. **STOP and VALIDATE**: Two metric cards visible with correct values
5. Deploy or demo if ready — this is a working dashboard

### Incremental Delivery

1. T001–T002 → T003 → Foundation ready
2. T004 → KPI cards ✅ Demo to Finance Manager
3. T005–T006 → Trend chart ✅ Demo to CEO
4. T007–T008 → Category chart ✅ Demo to Marketing Director
5. T009–T010 → Region chart ✅ Demo to Regional Manager
6. T011–T014 → Polish + Deploy ✅ Share public URL

---

## Notes

- [P] tasks = logically independent; a single developer can reorder them freely
- [Story] label maps every task to a specific user story for Jira traceability
- All tasks target `app.py` — no module extraction permitted (Principle V)
- T010 depends on T008 because they share the same `st.columns(2)` code block
- Commit after each checkpoint with Jira key (e.g., `ECOM-1: implement KPI cards`)
- After each commit, add a Jira comment with commit hash, branch name, and GitHub link
