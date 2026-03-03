<!--
Sync Impact Report
==================
Version change: 0.0.0 → 1.0.0 (initial ratification — template → filled constitution)

Added sections:
  - Core Principles (I. Simplicity First, II. Phase 1 Scope Lock,
    III. Accessibility by Default, IV. Data Trust, V. Single-File Deployment)
  - Tech Stack Constraints
  - Development Standards
  - Governance

Removed sections: N/A (initial creation from blank template)
Modified principles: N/A

Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — Constitution Check gate language
    ("[Gates determined based on constitution file]") correctly defers to this
    document; no edits required.
  - ✅ .specify/templates/spec-template.md — Scope/requirements sections align
    with Phase 1 Scope Lock (Principle II); no edits required.
  - ✅ .specify/templates/tasks-template.md — Generic src/ path conventions are
    instructional; generated tasks for this project MUST use app.py per
    Principle V. No template edits required.

Follow-up TODOs: None. All placeholders resolved.
-->

# ShopSmart E-Commerce Analytics Constitution

## Core Principles

### I. Simplicity First (NON-NEGOTIABLE)

All implementation decisions MUST choose the simplest option that satisfies the
Phase 1 requirement. No abstractions, helper modules, utilities, or scaffolding
may be introduced unless a Phase 1 requirement cannot be met without them. Every
line of code beyond the minimum MUST be explicitly justified against a concrete
Phase 1 functional requirement from the PRD.

**Rationale**: This is a single-developer, time-boxed dashboard. Complexity
introduced now will not be maintained, and there is no Phase 2 team to inherit
abstractions. YAGNI (You Aren't Gonna Need It) is the default decision rule.

### II. Phase 1 Scope Lock (NON-NEGOTIABLE)

The dashboard MUST implement only the four Phase 1 requirements from the PRD:
KPI cards (Total Sales, Total Orders), Sales Trend line chart, Category bar chart,
and Regional bar chart loaded from CSV. Any feature listed under Phase 2 in the
PRD — including filters, authentication, database integration, export, email
alerts, drill-down, or mobile-responsive design — MUST NOT be implemented,
scaffolded, commented-as-future-work, or structurally hinted at in code.

**Rationale**: Scope creep is the highest-probability, highest-impact risk
identified in the PRD risk register. This principle enforces the PRD's own
boundary as a non-negotiable rule rather than a guideline.

### III. Accessibility by Default

All charts and KPI displays MUST use colorblind-safe color palettes. All chart
axes, legends, labels, and tooltips MUST include descriptive text — no
color-only encodings. Font sizes MUST remain at Streamlit and Plotly defaults
or larger. No purely decorative visual elements that reduce data clarity may
be introduced.

**Rationale**: The dashboard serves executive stakeholders with varied visual
abilities. The PRD requires "no training required for basic usage" (NFR-2) and
"professional appearance suitable for executive presentations" (NFR-2). Accessible
design satisfies both simultaneously.

### IV. Data Trust

The application MUST load `data/sales-data.csv` directly without schema
validation, type coercion guards, or try/except wrappers around the data loading
path. If the file is missing or structurally malformed, Streamlit's native error
display is the accepted and sufficient failure mode.

**Rationale**: The dataset is static, controlled, and authored by the project
team. Defensive validation adds code complexity and maintenance burden with no
benefit for the Phase 1 use case, violating Principle I.

### V. Single-File Deployment

All application logic MUST reside in `app.py` at the repository root. No
separate helper modules, sub-packages, or `src/` directories may be created.
The complete set of project files is: `app.py`, `requirements.txt`,
`data/sales-data.csv`, and spec-kit artifacts under `.specify/` and `specs/`.
The command `streamlit run app.py` MUST be the complete and only command needed
to start the dashboard.

**Rationale**: Multi-file structures complicate Streamlit Community Cloud
deployment and add navigation overhead for a single-developer project. The
deployment command itself serves as the integration test for this principle.

## Tech Stack Constraints

The following technologies are mandated by the PRD and MUST NOT be substituted
without a constitution amendment:

| Layer              | Technology | Requirement   |
|--------------------|------------|---------------|
| Language           | Python     | 3.11+         |
| Dashboard framework | Streamlit | Latest stable |
| Visualization      | Plotly     | Latest stable |
| Data processing    | Pandas     | Latest stable |
| Data source        | CSV file   | `data/sales-data.csv` |

No additional runtime dependencies may be added to `requirements.txt` without
documenting which specific Phase 1 functional requirement necessitates them.

## Development Standards

- **Entry point**: `app.py` at repository root; `streamlit run app.py` MUST
  start the dashboard with no additional setup beyond dependency installation.
- **Functions within `app.py`**: Intra-file helper functions are permitted to
  reduce repetition but MUST NOT be extracted into separate files.
- **Comments**: Add comments only where logic is non-obvious. Do not add
  docstrings to every function — clarity from naming is preferred.
- **Performance**: Dashboard MUST load within 5 seconds and charts MUST render
  within 2 seconds of data load (PRD NFR-1).
- **Browser targets**: Chrome, Firefox, Safari, Edge. No browser-specific
  workarounds permitted (PRD NFR-4).
- **Deployment target**: Streamlit Community Cloud, deployed from the `main`
  branch of the student's GitHub fork, file `app.py`.
- **Commit convention**: Include the Jira issue key (e.g., `ECOM-1`) in every
  commit message title. After each commit, add a Jira comment with the commit
  hash, branch name, and GitHub link.

## Governance

This constitution supersedes all other development guidance for the ShopSmart
E-Commerce Analytics project. All specifications, plans, and task lists MUST
be validated against Principles I–V before implementation begins.

**Amendment procedure**: Any amendment requires (1) a documented reason, (2) a
version increment per the policy below, and (3) a Sync Impact Report listing all
affected templates and artifacts.

**Versioning policy**:
- MAJOR: Backward-incompatible change — principle removal or redefinition.
- MINOR: New principle or section added, or materially expanded guidance.
- PATCH: Clarifications, wording refinements, typo fixes.

**Compliance review**: Every implementation plan MUST include a Constitution
Check step verifying adherence to all five principles before coding begins.
Any deviation from a principle MUST be documented in the plan's Complexity
Tracking table with a justification and rejected simpler alternatives.

**Version**: 1.0.0 | **Ratified**: 2026-03-03 | **Last Amended**: 2026-03-03
