# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A tutorial that teaches a professional AI-assisted development workflow. Participants build and deploy a Streamlit sales analytics dashboard by following the documents in `v2/`. The repository contains tutorial documentation, a sample dataset, and a PRD — not the dashboard source code itself (students create that during the workshop).

## Repository structure

```
prd/ecommerce-analytics.md   # Product requirements document students build from
data/sales-data.csv          # Sample dataset (~482 orders, 12 months, 5 categories, 4 regions)
v2/pre-work-setup.md         # Part 1: account setup and tool installation (60–90 min async)
v2/workshop-build-deploy.md  # Part 2: spec-kit → Jira → code → deploy (3-hour live workshop)
v2/README.md                 # v2 overview
v1/                          # Original two-session version (reference only)
```

## The workflow being taught

```
PRD → spec-kit → Jira → Code → Commit → Push → Deploy
```

1. Read `prd/ecommerce-analytics.md`
2. Run spec-kit to generate constitution, specification, plan, and tasks
3. Create Jira issues from the tasks
4. Implement each issue with Claude Code using `/speckit.implement`
5. Commit (include Jira key like `ECOM-1` in the message), push, update Jira
6. Merge feature branch to `main`, deploy to Streamlit Community Cloud

## Key commands

### Starting and stopping the dashboard (student's project, not in this repo)
```bash
source venv/bin/activate        # macOS — activate virtual environment
# venv\Scripts\activate         # Windows
streamlit run app.py            # Run at http://localhost:8501
# Ctrl+C to stop
```

### spec-kit (run in terminal, not inside Claude Code)
```bash
specify init . --ai claude      # One-time: initialize spec-kit for the project
```

### spec-kit slash commands (run inside Claude Code)
```
/speckit.constitution           # Generate project constitution
/speckit.specify @prd/ecommerce-analytics.md   # Generate specification from PRD
/speckit.plan                   # Generate implementation plan
/speckit.tasks                  # Break plan into actionable tasks
/speckit.implement              # Implement a specific Jira issue
```

### Jira MCP (run in terminal, not inside Claude Code)
```bash
# One-time: register the Atlassian MCP server
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
```

### Claude Code
```bash
claude                          # Start Claude Code
/mcp                            # Check MCP servers / re-authenticate Atlassian
/output-style explanatory       # Verbose output mode for learning
```

## Dashboard tech stack (what students build)

- **Python 3.11+** with `venv` or `uv` for dependency management
- **Streamlit** — dashboard framework
- **Plotly** — interactive charts
- **Pandas** — data processing
- **Data source** — `data/sales-data.csv` (columns: `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`)

## Jira project conventions

- Project key: `ECOM`
- Issue keys in commit messages: e.g., `ECOM-1: Set up project structure`
- Workflow states: To Do → In Progress → Done
- After each commit: add a Jira comment with commit hash, branch name, and GitHub link

## spec-kit artifacts (created during the workshop)

Generated files live under `.specify/` and `specs/`:
- `.specify/memory/constitution.md` — project principles
- `specs/[feature-name]/spec.md` — detailed requirements
- `specs/[feature-name]/plan.md` — technical approach
- `specs/[feature-name]/tasks.md` — implementation task list

## Deployment

Students deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) from the `main` branch of their GitHub fork. The app file is `app.py` (or whatever name spec-kit generates). A working reference deployment: https://sales-dashboard-greg-lontok.streamlit.app/

## Active Technologies
- Python 3.11+ + Streamlit (latest stable), Plotly Express (latest stable), (001-sales-dashboard)
- CSV file — `data/sales-data.csv` (read-only; no writes) (001-sales-dashboard)

## Recent Changes
- 001-sales-dashboard: Added Python 3.11+ + Streamlit (latest stable), Plotly Express (latest stable),
